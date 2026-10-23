"""
Scraper: Polizeimeldungen Berlin 2026
=====================================

Projekt:  berlin-osint-2026
Quelle:   https://www.berlin.de/polizei/polizeimeldungen/archiv/2026/
Ziel:     Alle Polizeimeldungen von Januar bis Oktober 2026 mit Datum, Uhrzeit,
          Ereignisort (Bezirk), Meldungsnummer, Titel und Volltext in einer
          SQLite-Datenbank speichern.

Ablauf
------
1. Archivseiten durchgehen (?page_at_1_1=1, 2, 3 ...), bis keine neuen Links mehr kommen.
   Aus jeder Seite: Link, Titel, Datum/Uhrzeit, Ereignisort.
2. Jede einzelne Meldung öffnen und Nummer + Volltext auslesen.
3. Alles in data/raw/polizeimeldungen_2026.db speichern.
   Bereits gespeicherte Meldungen werden übersprungen, d. h. das Skript kann nach
   einem Abbruch einfach neu gestartet werden.

Installation
------------
    pip install requests beautifulsoup4 lxml tqdm

Start
-----
    python scrape_polizeimeldungen.py

Fairness
--------
- Pause zwischen allen Anfragen (DELAY_SECONDS)
- eigener User-Agent mit Projektname
- robots.txt wird vor dem Start geprüft
"""

import re
import sqlite3
import time
import urllib.robotparser
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# ---------------------------------------------------------------------------
# 1. Einstellungen
# ---------------------------------------------------------------------------

BASE_URL = "https://www.berlin.de"
ARCHIVE_URL = "https://www.berlin.de/polizei/polizeimeldungen/archiv/2026/"
PAGE_PARAM = "page_at_1_1"          # Parameter der Seitennummerierung im Archiv

START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 10, 31, 23, 59)

DB_PATH = Path("data/raw/polizeimeldungen_2026.db")
DELAY_SECONDS = 1.5                 # Pause zwischen Anfragen
MAX_PAGES = 200                     # Sicherheitsgrenze gegen Endlosschleifen
TIMEOUT = 30

HEADERS = {
    "User-Agent": "berlin-osint-2026 (privates Forschungsprojekt; GitHub: Amirhouschang)"
}

# ---------------------------------------------------------------------------
# 2. Datenbank
# ---------------------------------------------------------------------------

def init_db(path: Path) -> sqlite3.Connection:
    """Legt die Datenbank und die Tabelle an, falls sie noch nicht existieren."""
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS meldungen (
            url           TEXT PRIMARY KEY,   -- eindeutiger Link der Meldung
            meldung_id    INTEGER,            -- interne ID aus der URL (pressemitteilung.XXXX.php)
            nr            INTEGER,            -- offizielle Meldungsnummer (Nr. 1375)
            datum_zeit    TEXT,               -- ISO-Format, aus der Archivliste
            ereignisort   TEXT,               -- Bezirk oder z. B. "berlinweit"
            titel         TEXT,
            text          TEXT,               -- Volltext der Meldung
            abgerufen_am  TEXT                -- Zeitpunkt des Abrufs
        )
        """
    )
    con.commit()
    return con


def already_saved(con: sqlite3.Connection, url: str) -> bool:
    """Prüft, ob eine Meldung mit Volltext schon in der Datenbank ist."""
    row = con.execute(
        "SELECT 1 FROM meldungen WHERE url = ? AND text IS NOT NULL", (url,)
    ).fetchone()
    return row is not None


# ---------------------------------------------------------------------------
# 3. Hilfsfunktionen für Netzwerk
# ---------------------------------------------------------------------------

session = requests.Session()
session.headers.update(HEADERS)


def check_robots() -> None:
    """Bricht ab, wenn robots.txt das Abrufen des Archivs verbietet."""
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urljoin(BASE_URL, "/robots.txt"))
    rp.read()
    if not rp.can_fetch(HEADERS["User-Agent"], ARCHIVE_URL):
        raise SystemExit("robots.txt erlaubt das Abrufen des Archivs nicht. Abbruch.")
    print("robots.txt geprüft: Abruf erlaubt.")


def get_html(url: str, params: dict | None = None) -> str | None:
    """Lädt eine Seite mit Pause und bis zu 3 Versuchen. Gibt None bei Fehler zurück."""
    for attempt in range(1, 4):
        try:
            time.sleep(DELAY_SECONDS)
            r = session.get(url, params=params, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.text
            print(f"  Status {r.status_code} bei {r.url} (Versuch {attempt})")
        except requests.RequestException as e:
            print(f"  Fehler bei {url}: {e} (Versuch {attempt})")
        time.sleep(DELAY_SECONDS * attempt * 2)  # längere Pause vor neuem Versuch
    return None


# ---------------------------------------------------------------------------
# 4. Archivseiten auslesen
# ---------------------------------------------------------------------------

DATE_RE = re.compile(r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})")
ID_RE = re.compile(r"pressemitteilung\.(\d+)\.php")


def parse_archive_page(html: str) -> list[dict]:
    """
    Liest eine Archivseite aus. Jeder Listeneintrag enthält:
    Datum + Uhrzeit, Link mit Titel und "Ereignisort: ...".
    """
    soup = BeautifulSoup(html, "lxml")
    entries = []

    for a in soup.find_all("a", href=ID_RE):
        li = a.find_parent("li")
        if li is None:
            continue
        li_text = li.get_text(" ", strip=True)

        # Datum und Uhrzeit, z. B. "16.10.2026 13:24 Uhr"
        m = DATE_RE.search(li_text)
        if not m:
            continue
        datum_zeit = datetime.strptime(f"{m.group(1)} {m.group(2)}", "%d.%m.%Y %H:%M")

        # Ereignisort steht hinter "Ereignisort:"
        ort = None
        if "Ereignisort:" in li_text:
            ort = li_text.split("Ereignisort:", 1)[1].strip()

        url = urljoin(BASE_URL, a["href"])
        entries.append(
            {
                "url": url,
                "meldung_id": int(ID_RE.search(url).group(1)),
                "titel": a.get_text(" ", strip=True),
                "datum_zeit": datum_zeit,
                "ereignisort": ort,
            }
        )
    return entries


def collect_links() -> list[dict]:
    """Geht alle Archivseiten durch, bis keine neuen Meldungen mehr erscheinen."""
    all_entries: dict[str, dict] = {}

    for page in range(1, MAX_PAGES + 1):
        html = get_html(ARCHIVE_URL, params={PAGE_PARAM: page})
        if html is None:
            print(f"Seite {page} nicht ladbar, Abbruch der Linksammlung.")
            break

        entries = parse_archive_page(html)
        new = [e for e in entries if e["url"] not in all_entries]
        print(f"Archivseite {page}: {len(entries)} Einträge, davon {len(new)} neu")

        if not new:          # keine neuen Links: letzte Seite erreicht
            break
        for e in new:
            all_entries[e["url"]] = e

    # nur Zeitraum Januar bis Oktober 2026
    result = [
        e for e in all_entries.values() if START_DATE <= e["datum_zeit"] <= END_DATE
    ]
    print(f"Gesamt im Zeitraum: {len(result)} Meldungen")
    return result


# ---------------------------------------------------------------------------
# 5. Einzelne Meldung auslesen
# ---------------------------------------------------------------------------

DETAIL_RE = re.compile(
    r"Polizeimeldung vom\s+(\d{2}\.\d{2}\.\d{4})\s+(.*?)\s+Nr\.\s*(\d+)\s+(.*)",
    re.DOTALL,
)

# Text nach dem eigentlichen Meldungstext (Kontaktblock der Pressestelle)
END_MARKERS = ["Polizei Berlin\nPressearbeit", "Pressearbeit und Erreichbarkeit"]


def parse_detail_page(html: str) -> dict:
    """
    Aufbau einer Meldung:
        Titel (h1)
        Polizeimeldung vom TT.MM.JJJJ
        Ereignisort
        Nr. XXXX
        Volltext
    Der Text wird ab der Überschrift gelesen und mit einem regulären Ausdruck zerlegt.
    """
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.find("h1")

    # Text ab der Überschrift sammeln, damit das Menü nicht mitgelesen wird
    parts = []
    if h1 is not None:
        for el in h1.find_all_next(string=True):
            t = el.strip()
            if t:
                parts.append(t)
    page_text = "\n".join(parts)

    m = DETAIL_RE.search(page_text)
    if not m:
        return {"nr": None, "text": None}

    body = m.group(4)
    for marker in END_MARKERS:
        if marker in body:
            body = body.split(marker, 1)[0]
    body = body.replace("Direkt zur Kontaktinformation", "")
    body = re.sub(r"\n{2,}", "\n", body).strip()

    return {"nr": int(m.group(3)), "text": body}


# ---------------------------------------------------------------------------
# 6. Hauptprogramm
# ---------------------------------------------------------------------------

def main() -> None:
    check_robots()
    con = init_db(DB_PATH)

    entries = collect_links()
    todo = [e for e in entries if not already_saved(con, e["url"])]
    print(f"Noch abzurufen: {len(todo)} Meldungen")

    fehler = 0
    for e in tqdm(todo, desc="Meldungen"):
        html = get_html(e["url"])
        detail = parse_detail_page(html) if html else {"nr": None, "text": None}
        if detail["text"] is None:
            fehler += 1

        con.execute(
            """
            INSERT OR REPLACE INTO meldungen
            (url, meldung_id, nr, datum_zeit, ereignisort, titel, text, abgerufen_am)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                e["url"],
                e["meldung_id"],
                detail["nr"],
                e["datum_zeit"].isoformat(),
                e["ereignisort"],
                e["titel"],
                detail["text"],
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        con.commit()  # nach jeder Meldung speichern, damit nichts verloren geht

    total = con.execute("SELECT COUNT(*) FROM meldungen").fetchone()[0]
    print(f"Fertig. {total} Meldungen in {DB_PATH}. Ohne Volltext: {fehler}")
    con.close()


if __name__ == "__main__":
    main()
