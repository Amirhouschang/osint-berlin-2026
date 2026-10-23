"""
Fehlende Polizeimeldungen 2026 nachholen
========================================

Projekt:  berlin-osint-2026
Problem:  Das Archiv auf berlin.de listet nicht alle Meldungen (höchste Nr. 1399,
          aber nur 988 im Archiv; Juni fast leer).
Lösung:   Links zu Meldungen aus drei weiteren Quellen sammeln und die Meldungen
          dann direkt von berlin.de abrufen:
          1. Wayback Machine (CDX-API): Liste aller archivierten Meldungs-URLs
          2. Common Crawl (Index-API): offenes Webarchiv, ein Index pro Monat
          3. Unterseiten der Polizeimeldungen (Zeugen gesucht, Tötungsdelikte usw.)

Die neuen Meldungen landen in derselben Datenbank (data/raw/polizeimeldungen_2026.db)
mit der Spalte quelle = "wayback", "commoncrawl" oder "unterseite". Meldungen, die
schon drin sind, werden übersprungen.

Voraussetzung
-------------
scrape_polizeimeldungen.py liegt im selben Ordner (Funktionen werden von dort importiert).

Start
-----
    python find_missing_meldungen.py                 # alle Quellen
    python find_missing_meldungen.py commoncrawl     # nur eine Quelle

Hinweis
-------
Bei Meldungen aus diesen Quellen ist nur das Datum bekannt, nicht die Uhrzeit
(die Uhrzeit steht nur in der Archivliste). datum_zeit wird dann auf 00:00 gesetzt
und uhrzeit_bekannt = 0.
"""

import json
import sys
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from tqdm import tqdm

from scrape_polizeimeldungen import (
    BASE_URL, DB_PATH, DELAY_SECONDS, START_DATE, END_DATE, ID_RE, DETAIL_RE, TIMEOUT,
    check_robots, get_html, init_db, parse_detail_page, session,
)

# ---------------------------------------------------------------------------
# 1. Einstellungen
# ---------------------------------------------------------------------------

CDX_URL = "https://web.archive.org/cdx/search/cdx"

# Common Crawl: Liste aller Monatsindizes; genutzt werden nur die Indizes aus 2026
CC_COLLINFO = "https://index.commoncrawl.org/collinfo.json"
CC_YEAR = "2026"

# Unterseiten, auf denen Meldungen zusätzlich gelistet werden
UNTERSEITEN = [
    "https://www.berlin.de/polizei/polizeimeldungen/fakten-hintergruende/",
    "https://www.berlin.de/polizei/polizeimeldungen/zeugen-gesucht/",
    "https://www.berlin.de/polizei/polizeimeldungen/gesuchte-personen/",
    "https://www.berlin.de/polizei/polizeimeldungen/toetungsdelikte/",
    "https://www.berlin.de/polizei/polizeimeldungen/vermisste/",
    "https://www.berlin.de/polizei/polizeimeldungen/unbekannte-tote/",
    "https://www.berlin.de/polizei/polizeimeldungen/sachfahndung/",
]

# Die erste Meldung 2026 hat die ID 1629630. Kleinere IDs werden nicht abgerufen (spart Anfragen),
# weil die Wayback Machine auch viele ältere Meldungen liefert. Achtung: Die Polizei nutzt teils
# alte Seiten mit kleineren IDs für neue Meldungen weiter (9 solche Meldungen kamen über das Archiv
# in die Daten). Solche Meldungen findet dieses Skript nicht. Wer sie sucht, setzt MIN_ID_2026 = 0,
# dann entscheidet nur das Datum der Meldung (Prüfung weiter unten), bei deutlich mehr Abrufen.
MIN_ID_2026 = 1629000

# ---------------------------------------------------------------------------
# 2. Datenbank um zwei Spalten erweitern
# ---------------------------------------------------------------------------

def add_columns(con) -> None:
    """Fügt die Spalten quelle und uhrzeit_bekannt hinzu, falls sie fehlen."""
    spalten = [r[1] for r in con.execute("PRAGMA table_info(meldungen)")]
    if "quelle" not in spalten:
        con.execute("ALTER TABLE meldungen ADD COLUMN quelle TEXT DEFAULT 'archiv'")
    if "uhrzeit_bekannt" not in spalten:
        con.execute("ALTER TABLE meldungen ADD COLUMN uhrzeit_bekannt INTEGER DEFAULT 1")
    # bereits gespeicherte Orte mit mehreren Zeilen auf die erste Zeile kürzen
    con.execute(
        """
        UPDATE meldungen
        SET ereignisort = trim(substr(ereignisort, 1, instr(ereignisort, char(10)) - 1))
        WHERE instr(ereignisort, char(10)) > 0
        """
    )
    con.commit()


def known_ids(con) -> set[int]:
    """IDs aller Meldungen, die schon mit Volltext gespeichert sind."""
    rows = con.execute("SELECT meldung_id FROM meldungen WHERE text IS NOT NULL")
    return {r[0] for r in rows}


# ---------------------------------------------------------------------------
# 3. Links sammeln
# ---------------------------------------------------------------------------

def normalize(url: str) -> str | None:
    """Macht aus einer archivierten URL einen sauberen berlin.de-Link."""
    m = ID_RE.search(url)
    if not m:
        return None
    # alles nach ".php" abschneiden (manche Wayback-Einträge enthalten angehängten Text)
    url = url[: m.end()]
    path = urlparse(url if "://" in url else "https://" + url).path
    return urljoin(BASE_URL, path)


def links_from_wayback() -> dict[int, str]:
    """
    Fragt die CDX-API der Wayback Machine nach allen archivierten URLs unter
    /polizei/polizeimeldungen/ ab 2026. Die Antwort ist eine Textliste, eine URL pro Zeile.
    """
    params = {
        "url": "berlin.de/polizei/polizeimeldungen/",
        "matchType": "prefix",
        "from": "2026",
        "fl": "original",
        "collapse": "urlkey",          # jede URL nur einmal
        "filter": "original:.*pressemitteilung\\.[0-9]+\\.php.*",
    }
    text = get_html(CDX_URL, params=params)
    if text is None:
        print("Wayback Machine nicht erreichbar.")
        return {}

    found = {}
    for line in text.splitlines():
        url = normalize(line.strip())
        if url:
            found[int(ID_RE.search(url).group(1))] = url
    print(f"Wayback Machine: {len(found)} Meldungs-URLs gefunden")
    return found


def cc_get(url: str, params: dict) -> str | None:
    """
    Abruf für die Common-Crawl-API. Anders als get_html wird Status 404 nicht
    wiederholt, weil er dort einfach "keine Treffer in diesem Index" bedeutet.
    """
    for attempt in range(1, 4):
        try:
            time.sleep(DELAY_SECONDS)
            r = session.get(url, params=params, timeout=TIMEOUT * 4)
            if r.status_code == 200:
                return r.text
            if r.status_code == 404:
                return ""
            print(f"  Status {r.status_code} bei Common Crawl (Versuch {attempt})")
        except Exception as e:
            print(f"  Fehler bei Common Crawl: {e} (Versuch {attempt})")
        time.sleep(DELAY_SECONDS * attempt * 4)
    return None


def links_from_commoncrawl() -> dict[int, str]:
    """
    Fragt alle Common-Crawl-Monatsindizes aus 2026 nach archivierten Meldungs-URLs.
    Große Ergebnisse teilt die API in Seiten auf; die Anzahl liefert showNumPages.
    """
    info = get_html(CC_COLLINFO)
    if info is None:
        print("Common Crawl nicht erreichbar.")
        return {}
    indizes = [c for c in json.loads(info) if CC_YEAR in c["id"]]

    found = {}
    for idx in indizes:
        api = idx["cdx-api"]
        # leichte Abfrage: nur der Ordner /2026/, kein Filter auf dem Server
        # (die breite Abfrage mit Filter führte zu 504-Fehlern); gefiltert wird hier
        base = {
            "url": "www.berlin.de/polizei/polizeimeldungen/2026/*",
            "output": "json",
            "fl": "url",
        }
        # 1. Anzahl der Ergebnisseiten abfragen
        meta = cc_get(api, {**base, "showNumPages": "true"})
        if not meta:
            print(f"{idx['id']}: keine Treffer oder nicht erreichbar")
            continue
        pages = json.loads(meta).get("pages", 1)

        # 2. alle Seiten abrufen, jede Zeile ist ein JSON-Objekt mit "url"
        vorher = len(found)
        for page in range(pages):
            text = cc_get(api, {**base, "page": page})
            for line in (text or "").splitlines():
                try:
                    url = normalize(json.loads(line)["url"])
                except (ValueError, KeyError):
                    continue
                if url:
                    found[int(ID_RE.search(url).group(1))] = url
        print(f"{idx['id']}: {pages} Seite(n), {len(found) - vorher} neue URLs")

    print(f"Common Crawl: {len(found)} Meldungs-URLs gefunden")
    return found


def links_from_unterseiten() -> dict[int, str]:
    """Liest alle Meldungslinks aus den Unterseiten, inklusive deren Seitennummerierung."""
    found = {}
    for start in UNTERSEITEN:
        besucht, offen = set(), [start]
        while offen and len(besucht) < 50:      # Sicherheitsgrenze pro Unterseite
            url = offen.pop()
            if url in besucht:
                continue
            besucht.add(url)
            html = get_html(url)
            if html is None:
                continue
            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a", href=True):
                href = urljoin(url, a["href"]).split("#")[0]
                if ID_RE.search(href):
                    clean = normalize(href)
                    found[int(ID_RE.search(clean).group(1))] = clean
                elif href.startswith(start) and "page_at_" in href:
                    offen.append(href)           # weitere Seite dieser Unterseite
        print(f"{start.split('/')[-2]}: {len(besucht)} Seiten gelesen")
    print(f"Unterseiten: {len(found)} Meldungs-URLs gefunden")
    return found


# ---------------------------------------------------------------------------
# 4. Datum und Ort aus der Meldung selbst lesen
# ---------------------------------------------------------------------------

def parse_date_and_place(html: str) -> tuple[datetime | None, str | None]:
    """Liest 'Polizeimeldung vom TT.MM.JJJJ' und den Ort darunter aus der Meldung."""
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.find("h1")
    if h1 is None:
        return None, None
    page_text = "\n".join(t.strip() for t in h1.find_all_next(string=True) if t.strip())
    m = DETAIL_RE.search(page_text)
    if not m:
        return None, None
    # nur die erste Zeile ist der Ort (danach folgen z. B. "Flex Text" oder Zusatzhinweise)
    ort = m.group(2).strip().split("\n")[0].strip()
    return datetime.strptime(m.group(1), "%d.%m.%Y"), ort


# ---------------------------------------------------------------------------
# 5. Hauptprogramm
# ---------------------------------------------------------------------------

def main() -> None:
    check_robots()
    con = init_db(DB_PATH)
    add_columns(con)
    vorhanden = known_ids(con)
    print(f"Schon in der Datenbank: {len(vorhanden)} Meldungen")

    kandidaten = {}
    # Quellen wählen: ohne Angabe alle, sonst z. B. "python find_missing_meldungen.py commoncrawl"
    quellen = {
        "wayback": links_from_wayback,
        "commoncrawl": links_from_commoncrawl,
        "unterseite": links_from_unterseiten,
    }
    gewaehlt = [q for q in sys.argv[1:] if q in quellen] or list(quellen)
    print(f"Quellen: {', '.join(gewaehlt)}")

    for quelle in gewaehlt:
        links = quellen[quelle]()
        for mid, url in links.items():
            if mid >= MIN_ID_2026 and mid not in vorhanden and mid not in kandidaten:
                kandidaten[mid] = (url, quelle)
    print(f"Neue Kandidaten zum Abrufen: {len(kandidaten)}")

    neu, ausserhalb, fehler = 0, 0, 0
    for mid, (url, quelle) in tqdm(sorted(kandidaten.items()), desc="Meldungen"):
        html = get_html(url)
        if html is None:
            fehler += 1
            continue
        datum, ort = parse_date_and_place(html)
        if datum is None:
            fehler += 1
            continue
        if not (START_DATE <= datum <= END_DATE):
            ausserhalb += 1                       # z. B. Meldung aus 2025
            continue

        detail = parse_detail_page(html)
        h1 = BeautifulSoup(html, "lxml").find("h1")
        con.execute(
            """
            INSERT OR REPLACE INTO meldungen
            (url, meldung_id, nr, datum_zeit, ereignisort, titel, text,
             abgerufen_am, quelle, uhrzeit_bekannt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (url, mid, detail["nr"], datum.isoformat(), ort,
             h1.get_text(" ", strip=True) if h1 else None, detail["text"],
             datetime.now().isoformat(timespec="seconds"), quelle),
        )
        con.commit()
        neu += 1

    total = con.execute("SELECT COUNT(*) FROM meldungen").fetchone()[0]
    print(f"Fertig. Neu: {neu}, außerhalb Zeitraum: {ausserhalb}, Fehler: {fehler}")
    print(f"Gesamt in der Datenbank: {total}")
    con.close()


if __name__ == "__main__":
    main()
