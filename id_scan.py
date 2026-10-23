"""
ID-Scan: fehlende Polizeimeldungen über die Meldungs-ID finden
==============================================================

Projekt:  berlin-osint-2026
Problem:  Für die Zeit vom 20.05. bis 09.07.2026 fehlen viele Meldungen, und weder
          Archiv noch Wayback Machine noch Common Crawl kennen sie.
Idee:     Jede Meldung hat eine ID in der URL (pressemitteilung.1674985.php). Die Seite
          ist auch ohne Jahresordner erreichbar:
              https://www.berlin.de/polizei/polizeimeldungen/pressemitteilung.<ID>.php
          IDs, die keine Polizeimeldung sind, liefern 404. Das Skript probiert alle IDs
          in einem Bereich durch und speichert jeden Treffer.

ID-Bereich
----------
Standard: 1672700 bis 1691800 (deckt etwa 90 % der bekannten Meldungen aus dem
Zeitraum 20.05. bis 09.07. ab). Rund 19.000 Abrufe, mit 1 Sekunde Pause etwa 5,5 Stunden.
Die übrigen 10 % haben ältere IDs (die Polizei nutzt teils alte Seiten weiter) und
werden damit nicht gefunden.

Start
-----
    python id_scan.py                      # Standardbereich
    python id_scan.py 1672700 1680000      # eigener Bereich

Fortsetzen
----------
Jede geprüfte ID wird in der Tabelle scan_log gespeichert. Nach einem Abbruch
(Strg + C, Rechner aus) einfach neu starten: geprüfte IDs werden übersprungen.
"""

import sys
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from scrape_polizeimeldungen import (
    BASE_URL, DB_PATH, START_DATE, END_DATE, TIMEOUT,
    check_robots, init_db, parse_detail_page, session,
)
from find_missing_meldungen import add_columns, parse_date_and_place

# ---------------------------------------------------------------------------
# 1. Einstellungen
# ---------------------------------------------------------------------------

DEFAULT_START = 1672700
DEFAULT_END = 1691800
DELAY = 1.0              # Pause zwischen Abrufen in Sekunden
PAUSE_BEI_SPERRE = 120   # Pause, wenn der Server mit 429 oder 5xx antwortet
URL_MUSTER = BASE_URL + "/polizei/polizeimeldungen/pressemitteilung.{}.php"

# ---------------------------------------------------------------------------
# 2. Protokolltabelle für geprüfte IDs
# ---------------------------------------------------------------------------

def init_scan_log(con) -> None:
    """Tabelle, in der jede geprüfte ID mit HTTP-Status steht (zum Fortsetzen)."""
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS scan_log (
            meldung_id   INTEGER PRIMARY KEY,
            status       INTEGER,     -- HTTP-Status (200, 404 ...)
            treffer      INTEGER,     -- 1 = Polizeimeldung aus dem Zeitraum gespeichert
            geprueft_am  TEXT
        )
        """
    )
    con.commit()


def ids_to_check(con, start: int, end: int) -> list[int]:
    """Alle IDs im Bereich, die weder schon gespeichert noch schon geprüft sind."""
    bekannt = {r[0] for r in con.execute("SELECT meldung_id FROM meldungen")}
    geprueft = {r[0] for r in con.execute("SELECT meldung_id FROM scan_log")}
    return [i for i in range(start, end + 1) if i not in bekannt and i not in geprueft]


# ---------------------------------------------------------------------------
# 3. Eine ID prüfen
# ---------------------------------------------------------------------------

def fetch(mid: int) -> tuple[int | None, str | None, str | None]:
    """
    Ruft eine ID ab. Rückgabe: (Status, HTML, endgültige URL).
    404 wird nicht wiederholt, das ist der Normalfall (keine Meldung).
    Status None bedeutet Netzwerkfehler.
    """
    try:
        r = session.get(URL_MUSTER.format(mid), timeout=TIMEOUT)
        return r.status_code, (r.text if r.status_code == 200 else None), r.url
    except requests.RequestException:
        return None, None, None


def save_hit(con, mid: int, html: str, url: str) -> bool:
    """Speichert eine gefundene Meldung, wenn sie aus dem Zeitraum stammt."""
    datum, ort = parse_date_and_place(html)
    if datum is None or not (START_DATE <= datum <= END_DATE):
        return False
    detail = parse_detail_page(html)
    h1 = BeautifulSoup(html, "lxml").find("h1")
    con.execute(
        """
        INSERT OR REPLACE INTO meldungen
        (url, meldung_id, nr, datum_zeit, ereignisort, titel, text,
         abgerufen_am, quelle, uhrzeit_bekannt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'id-scan', 0)
        """,
        (url, mid, detail["nr"], datum.isoformat(), ort,
         h1.get_text(" ", strip=True) if h1 else None, detail["text"],
         datetime.now().isoformat(timespec="seconds")),
    )
    return True


# ---------------------------------------------------------------------------
# 4. Hauptprogramm
# ---------------------------------------------------------------------------

def main() -> None:
    start = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_START
    end = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_END

    check_robots()
    con = init_db(DB_PATH)
    add_columns(con)
    init_scan_log(con)

    todo = ids_to_check(con, start, end)
    print(f"Bereich {start} bis {end}: {len(todo)} IDs zu prüfen "
          f"(ca. {len(todo) * DELAY / 3600:.1f} Stunden)")

    stats = {"treffer": 0}
    try:
        scan(con, tqdm(todo, desc="IDs"), stats)
    except KeyboardInterrupt:
        print("\nAbgebrochen. Fortschritt ist gespeichert, einfach neu starten.")
    finally:
        con.commit()
    total = con.execute("SELECT COUNT(*) FROM meldungen").fetchone()[0]
    print(f"Neue Meldungen in diesem Lauf: {stats['treffer']}. "
          f"Gesamt in der Datenbank: {total}")
    con.close()


def scan(con, bar, stats: dict) -> None:
    """Geht alle IDs durch; Treffer werden in stats gezählt."""
    for i, mid in enumerate(bar):
        time.sleep(DELAY)
        status, html, url = fetch(mid)

        # Server überlastet oder sperrt: länger warten, ID nicht als geprüft markieren
        if status is None or status == 429 or status >= 500:
            bar.write(f"  ID {mid}: Status {status}, Pause {PAUSE_BEI_SPERRE} s")
            time.sleep(PAUSE_BEI_SPERRE)
            continue

        ok = False
        # nur echte Polizeimeldungen zählen (Weiterleitungen auf andere Seiten nicht)
        if status == 200 and url and "/polizei/polizeimeldungen/" in url:
            ok = save_hit(con, mid, html, url)
            if ok:
                stats["treffer"] += 1
                bar.set_postfix(treffer=stats["treffer"])

        con.execute(
            "INSERT OR REPLACE INTO scan_log VALUES (?, ?, ?, ?)",
            (mid, status, int(ok), datetime.now().isoformat(timespec="seconds")),
        )
        if ok or i % 50 == 0:
            con.commit()   # Treffer sofort, sonst alle 50 IDs speichern


if __name__ == "__main__":
    main()
