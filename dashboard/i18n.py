"""
i18n.py – texts of the dashboard in German and English
=======================================================
Everything the reader sees is defined here:
  UI          – interface texts, chart titles and notes under the charts
  CATEGORIES  – the twelve categories of the police reports (section 4 of the notebook)
  TOPICS      – the twelve topics (sections 5.7, 5.8 and 7.7)
  EVENTS      – the four events of section 5.1
  WEEKDAYS, MONTHS
Names of districts and places stay in German.
"""

LANGS = {"de": "Deutsch", "en": "English"}

MONTHS = {
    "de": ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"],
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}
WEEKDAYS = {
    "Mo": {"de": "Mo", "en": "Mon"}, "Di": {"de": "Di", "en": "Tue"}, "Mi": {"de": "Mi", "en": "Wed"},
    "Do": {"de": "Do", "en": "Thu"}, "Fr": {"de": "Fr", "en": "Fri"}, "Sa": {"de": "Sa", "en": "Sat"},
    "So": {"de": "So", "en": "Sun"},
}

# the order is the order of the colours in the charts (most frequent first)
CATEGORIES = {
    "Verkehr": {"de": "Verkehr", "en": "Traffic"},
    "Gewalt": {"de": "Gewalt", "en": "Violence"},
    "Politisch motiviert": {"de": "Politisch motiviert", "en": "Politically motivated"},
    "Raub und Diebstahl": {"de": "Raub und Diebstahl", "en": "Robbery and theft"},
    "Schusswaffen und OK": {"de": "Schusswaffen und OK", "en": "Firearms and OC"},
    "Brand und Sachbeschädigung": {"de": "Brand und Sachbeschädigung", "en": "Arson and criminal damage"},
    "Vermisste und Fahndung": {"de": "Vermisste und Fahndung", "en": "Missing and wanted persons"},
    "Drogen": {"de": "Drogen", "en": "Drugs"},
    "Betrug": {"de": "Betrug", "en": "Fraud"},
    "Einsatzlage und Versammlung": {"de": "Einsatzlage und Versammlung", "en": "Operations and assemblies"},
    "Prävention und Service": {"de": "Prävention und Service", "en": "Prevention and service"},
    "Sonstiges": {"de": "Sonstiges", "en": "Other"},
}
CATEGORY_COLORS = {
    "Verkehr": "#2a78d6", "Gewalt": "#eb6834", "Politisch motiviert": "#1baf7a", "Raub und Diebstahl": "#eda100",
    "Schusswaffen und OK": "#e87ba4", "Brand und Sachbeschädigung": "#008300", "Vermisste und Fahndung": "#7a5195",
    "Drogen": "#00a3b4", "Betrug": "#b05a2a", "Einsatzlage und Versammlung": "#5c6bc0",
    "Prävention und Service": "#c3c2b7", "Sonstiges": "#a3a29b",
}

TOPICS = {
    "Nahost-Konflikt": {"de": "Nahost-Konflikt", "en": "Middle East conflict"},
    "Antisemitismus": {"de": "Antisemitismus", "en": "Antisemitism"},
    "Rechtsextremismus": {"de": "Rechtsextremismus", "en": "Right-wing extremism"},
    "Linksextremismus": {"de": "Linksextremismus", "en": "Left-wing extremism"},
    "Rassismus": {"de": "Rassismus", "en": "Racism"},
    "Queerfeindlichkeit": {"de": "Queerfeindlichkeit", "en": "Anti-queer hostility"},
    "Versammlungen": {"de": "Versammlungen", "en": "Assemblies"},
    "Messer": {"de": "Messer", "en": "Knives"},
    "Gewalt gegen Polizei": {"de": "Gewalt gegen Polizei", "en": "Violence against police"},
    "Schusswaffe durch Polizei": {"de": "Schusswaffe durch Polizei", "en": "Firearm use by police"},
    "Taser/DEIG durch Polizei": {"de": "Taser/DEIG durch Polizei", "en": "Taser use by police"},
    "Vorwürfe gegen Polizei": {"de": "Vorwürfe gegen Polizei", "en": "Allegations against police"},
}
POLICE_TOPICS = ["Gewalt gegen Polizei", "Schusswaffe durch Polizei", "Taser/DEIG durch Polizei", "Vorwürfe gegen Polizei"]

EVENTS = {
    "Brandanschlag auf Stromkabel": {"de": "Brandanschlag auf Stromkabel", "en": "Arson attack on power cables"},
    "1. Mai": {"de": "1. Mai", "en": "1 May"},
    "Anschlag im Umfeld des CSD": {"de": "Anschlag im Umfeld des CSD", "en": "Attack near the CSD (Pride)"},
    "Wahl zum Abgeordnetenhaus": {"de": "Wahl zum Abgeordnetenhaus", "en": "Berlin state election"},
}

COLOR_POLICE = "#7a7a7a"
COLOR_MEDIA = "#2a78d6"
COLOR_KBO = "#e34948"

UI = {
    "de": {
        "title": "OSINT Berlin 2026",
        "subtitle": ("Lagebild aus offenen Quellen: Pressemitteilungen der Polizei Berlin und deutschsprachige "
                     "Online-Medien, **1. Januar bis 21. Oktober 2026**. Alle Zahlen stammen aus dem Notebook des "
                     "Projekts. Das Dashboard zeigt veröffentlichte Meldungen und Artikel, keine Kriminalstatistik."),
        "kpi_reports": "Polizeimeldungen", "kpi_articles": "Medienartikel (Auswahl)", "kpi_sources": "Medienquellen",
        "kpi_period": "Zeitraum", "kpi_period_value": "01.01. bis 21.10.2026",
        "tab_overview": "Überblick", "tab_police": "Polizeimeldungen", "tab_map": "Bezirke und Karte",
        "tab_media": "Medien", "tab_compare": "Vergleich", "tab_force": "Gewalt und Polizei", "tab_about": "Methodik",
        # common
        "month": "Monat", "reports": "Meldungen", "articles": "Artikel", "share_pct": "Anteil in %",
        "police": "Polizeimeldungen", "media": "Medienartikel", "all": "Alle",
        "per_month": "pro Monat", "per_day": "pro Tag", "avg7": "Durchschnitt über 7 Tage",
        "show_events": "Ereignisse zeigen", "district": "Bezirk", "all_districts": "Alle Bezirke",
        "categories": "Kategorien", "topic": "Thema", "value": "Wert",
        "src_police": "Quelle: Polizei Berlin, Pressemitteilungen 2026 (berlin.de, ergänzt über Wayback Machine und Common Crawl), eigene Auswertung.",
        "src_media": "Quelle: GDELT Global Knowledge Graph über Google BigQuery, deutschsprachige Online-Artikel mit Berlin-Bezug, Auswahl zu Polizei und Kriminalität (Notebook 7.4), eigene Auswertung.",
        "src_both": "Quellen: Polizei Berlin, Pressemitteilungen 2026, und GDELT Global Knowledge Graph (Google BigQuery), eigene Auswertung.",
        "period_note": "Zeitraum: 01.01. bis 21.10.2026, Oktober unvollständig.",
        "term_cat": "„Schusswaffen und OK“ = Schusswaffen und Organisierte Kriminalität. „Sonstiges“ = keine der übrigen Kategorien trifft zu.",
        "term_kbo": "kbO = kriminalitätsbelasteter Ort, von der Polizei Berlin festgelegt (§ 17a ASOG Bln).",
        # overview
        "ov_chart": "Polizeimeldungen und Medienartikel pro Monat (Anteil jedes Monats an der Summe)",
        "ov_chart_note": ("Damit beide Reihen auf eine Skala passen, zeigt jede Linie den Anteil des Monats an ihrer "
                          "Summe von Januar bis Oktober. Grau hinterlegt: Monate der vier Ereignisse."),
        "ov_facts": "Kernaussagen (aus den Daten berechnet)",
        "fact_top_police": "Häufigste Kategorie der Polizeimeldungen: **{cat}** ({pct} %).",
        "fact_top_district": "Die meisten Meldungen je Einwohner: **{d}** ({v} je 100.000 Einwohner, Berlin: {b}).",
        "fact_peak_media": "Stärkster Medientag: **{day}** mit {n} Artikeln.",
        "fact_corr": "Polizei und Medien laufen nicht gleich: Korrelation der Wochenwerte Pearson {r}, Spearman {s} (0 = kein Zusammenhang).",
        "fact_csd": "Zum Anschlag im Umfeld des CSD: {p} Polizeimeldung, aber {m} Medienartikel. Die erste Polizeimeldung dazu (Nr. 905) fehlt in den Daten.",
        "fact_coverage": "Erfasst sind geschätzt {c} % aller Meldungen der Polizei Berlin (über die Meldungsnummern).",
        "ov_how": ("**So liest man das Dashboard:** Jeder Reiter beantwortet eine Frage. Unter jedem Diagramm stehen "
                   "Quelle, Zeitraum, Grundlage und die Erklärung der Begriffe. Die Sprache lässt sich oben rechts "
                   "umschalten. Methoden und Grenzen stehen im Reiter „Methodik“."),
        # police
        "po_q": "**Worüber berichtet die Polizei Berlin, und wann?**",
        "po_month": "Polizeimeldungen pro Monat nach Kategorie",
        "po_month_note": "Kategorie: endgültige Kategorie aus Notebook 4.8 (lokales Sprachmodell {model}, geprüft an 100 manuell kategorisierten Meldungen). Monat der Veröffentlichung.",
        "po_day": "Polizeimeldungen pro Tag",
        "po_day_note": "Datum der Veröffentlichung, nicht der Tat. Gestrichelt: die vier Ereignisse.",
        "po_week": "Veröffentlichung nach Wochentag", "po_hour": "Veröffentlichung nach Uhrzeit",
        "po_time_note": "Die Uhrzeit ist nur bei Meldungen aus dem Archiv auf berlin.de bekannt ({n} Meldungen). Stunde 10 = 10:00 bis 10:59 Uhr.",
        "po_cov": "Abdeckung pro Monat (geschätzt über die Meldungsnummern)",
        "po_cov_note": "Abdeckung = vorhandene Meldungsnummern geteilt durch die Spanne von der kleinsten bis zur größten Nummer des Monats.",
        "po_filter_note": "Der Bezirksfilter gilt für das Monatsdiagramm. Meldungen ohne einzelnen Bezirk (berlinweit, überregional) erscheinen nur bei „Alle Bezirke“.",
        "hour": "Stunde", "weekday": "Wochentag", "coverage": "Abdeckung in %",
        # map
        "ma_q": "**Wo kommen die Meldungen vor?**",
        "ma_metric": "Bezirke einfärben nach",
        # surroundings of the districts
        "su_head": "Umfeld der Bezirke: Bevölkerung, Einkommen und Erwerbsbeteiligung",
        "su_warn": ("**Wichtig beim Lesen:** Diese Zahlen beschreiben Bezirke, nicht Menschen. Sie zeigen, in welchem Umfeld "
                    "Meldungen veröffentlicht werden, aber nicht, wer Taten begeht oder Opfer wird. Polizeimeldungen nennen die "
                    "Herkunft von Beteiligten nur selten, und viele Beteiligte wohnen nicht im Bezirk. Für die "
                    "Staatsangehörigkeit von Tatverdächtigen ist die Polizeiliche Kriminalstatistik (PKS) die richtige Quelle."),
        "su_choose": "Merkmal", "su_her": "Staatsangehörigkeit und Migrationshintergrund", "su_ein": "Haushaltseinkommen",
        "su_erw": "Erwerbstätige und Erwerbslose",
        "su_erw_right": "Bevölkerung von 15 bis unter 65 Jahren nach Erwerbsbeteiligung ({year})",
        "su_e1": "Erwerbstätige", "su_e2": "Erwerbslose", "su_e3": "Nichterwerbspersonen", "su_e_quote": "Erwerbslosenquote",
        "su_erw_note": ("Erwerbsbeteiligung: Amt für Statistik Berlin-Brandenburg, Ergebnisse des Mikrozensus in Berlin {year} "
                        "(Erstergebnis), Tabelle 7.3. Sortiert nach Meldungen je Einwohner."),
        "su_erw_unsure": ("Die Zahl der Erwerbslosen ist je Bezirk klein: Bei {n} Bezirken hat sie laut Amt nur eingeschränkten "
                          "Aussagewert, für {calc} wird sie nicht ausgewiesen und ist hier als Erwerbspersonen minus Erwerbstätige berechnet."),
        "su_erw_def": ("Erwerbstätige = bezahlte Arbeit von mindestens einer Stunde pro Woche, auch Selbstständige. Erwerbslose = "
                       "ohne Arbeit, aktiv auf Arbeitssuche und sofort verfügbar (ILO, nicht gleich den Arbeitslosen der "
                       "Bundesagentur für Arbeit). Nichterwerbspersonen = weder erwerbstätig noch erwerbslos, z. B. Schüler, "
                       "Studierende, Rentner. Erwerbslosenquote = Erwerbslose geteilt durch Erwerbspersonen."),
        "su_left": "Polizeimeldungen je 100.000 Einwohner",
        "su_her_right": "Einwohner nach Staatsangehörigkeit und Migrationshintergrund (30.06.2026)",
        "su_ein_right": "Haushalte nach monatlichem Haushaltsnettoeinkommen ({year})",
        "su_share": "Anteil im Bezirk in %",
        "su_g_ohne": "Deutsche ohne Migrationshintergrund", "su_g_mit": "Deutsche mit Migrationshintergrund",
        "su_g_ausl": "Ausländerinnen und Ausländer",
        "su_s1": "unter 1.500 €", "su_s2": "1.500 bis 2.000 €", "su_s3": "2.000 bis 3.000 €", "su_s4": "3.000 bis 4.000 €",
        "su_s5": "4.000 € und mehr",
        "su_t_head": "Zusammenhang mit den Meldungen je Einwohner (Spearman: 1 = gleiche Rangfolge, 0 = kein Zusammenhang, negativ = umgekehrte Rangfolge)",
        "su_t_share": "Merkmal", "su_t_all": "alle 12 Bezirke", "su_t_wo": "ohne {top2}",
        "su_t_mh": "mit Migrationshintergrund (zusammen)",
        "su_t_note": ("p = Zufallstest: Anteil zufälliger Zuordnungen der Bezirke mit mindestens so starkem Zusammenhang. "
                      "Je größer p, desto eher kann der Zusammenhang Zufall sein, ab etwa 0,05 gilt er als nicht gesichert. Mit 12 Bezirken lassen sich Lage in der "
                      "Innenstadt, Besucher, Alter und soziale Lage nicht voneinander trennen."),
        "su_her_note": ("Einwohner: Amt für Statistik Berlin-Brandenburg, Statistischer Bericht A I 5 (hj 1/26), Tabelle 7, "
                        "Stichtag 30.06.2026. Sortiert nach Meldungen je Einwohner."),
        "su_mh_def": ("Migrationshintergrund (Einwohnerregister): ausländische Staatsangehörigkeit, zweite Staatsangehörigkeit, "
                      "Geburt im Ausland, Einbürgerung oder Optionskennzeichen, oder unter 18 Jahre mit mindestens einem "
                      "Elternteil mit Migrationshintergrund an derselben Adresse. Ausländer haben immer einen Migrationshintergrund."),
        "su_ein_note": ("Einkommen: Amt für Statistik Berlin-Brandenburg, Ergebnisse des Mikrozensus in Berlin {year} "
                        "(Erstergebnis), Tabelle 7.5. Sortiert nach Meldungen je Einwohner."),
        "su_ein_def": ("Haushaltsnettoeinkommen = monatliches Nettoeinkommen aller Mitglieder eines Haushalts, nicht nach "
                       "Haushaltsgröße gewichtet. Mikrozensus = Stichprobe von rund 1 % der Haushalte, Werte je Bezirk sind "
                       "deshalb ungenauer als Zahlen aus dem Melderegister."),
        "ma_m_abs": "Zahl der Meldungen", "ma_m_rel": "Meldungen je 100.000 Einwohner",
        "ma_map": "Karte: Bezirke nach {metric} und Orte mit mindestens 3 Meldungen",
        "ma_metric_help": "Die Auswahl ändert die Farbe der Bezirke und die Zahl unter jedem Bezirksnamen. Die Punkte bleiben gleich.",
        "ma_map_note": ("Bezirke: je dunkler, desto höher der gewählte Wert, die Zahl unter dem Namen ist dieser Wert. Punkte: Orte, die in mindestens 3 Meldungen genannt werden, "
                        "Größe = Zahl der Meldungen, rot = kbO. Bezirksgrenzen: Geodatenportal Berlin, ALKIS "
                        "(Datenlizenz Deutschland Zero 2.0). Koordinaten: OpenStreetMap über Nominatim (ODbL)."),
        "ma_rel": "Polizeimeldungen je 100.000 Einwohner nach Bezirk",
        "ma_rel_note": ("Einwohner: Amt für Statistik Berlin-Brandenburg, Statistischer Bericht A I 5 (hj 1/26), Stichtag {date}, "
                        "melderechtlich registrierte Einwohner. Besucher und Pendler sind nicht enthalten, das betrifft vor "
                        "allem Mitte und Friedrichshain-Kreuzberg. Gestrichelt: Berlin insgesamt ({b})."),
        "ma_heat": "Anteil der Kategorien je Bezirk in %",
        "ma_heat_note": "Jede Zeile ergibt 100 %. Nur Meldungen mit einem einzelnen Bezirk.",
        "ma_kbo": "Kriminalitätsbelastete Orte: Polizeimeldungen und Medienartikel",
        "ma_kbo_note": "Gezählt: Polizeimeldungen, deren Titel oder Text den Ort nennt, und Medienartikel, deren Titel ihn nennt. Die Liste gilt seit dem 01.07.2026, gezählt wird das ganze Jahr. Kein blauer Balken = kein Medientitel nennt diesen Ort.",
        "per_100k": "je 100.000 Einwohner", "residents": "Einwohner", "rank": "Rang",
        "point_label": "{ort}: {n} Meldungen, meist {cat}",
        # media
        "me_q": "**Worüber berichten die Medien zu Polizei und Kriminalität in Berlin?**",
        "me_month": "Medienartikel pro Monat nach Kategorie",
        "me_month_note": ("Kategorie: dieselben Regeln wie bei der Polizei (Notebook 4.3), nur auf den Titel angewendet. "
                          "„Sonstiges“ = der Titel enthält ein Auswahlwort (z. B. Anschlag, Polizei, Demo), aber keine Kategorie trifft zu."),
        "me_day": "Medienartikel pro Tag",
        "me_day_note": "Datum laut GDELT. Gestrichelt: die vier Ereignisse. Ein Ereignis erzeugt oft Hunderte Artikel.",
        "me_sources": "Die 15 Quellen mit den meisten Artikeln",
        "me_sources_note": "Quelle = Website laut GDELT. Anteil = Anteil an allen Berlin-Artikeln dieser Website. {u} verschiedene Titel bei {n} Artikeln: derselbe Titel erscheint oft in mehreren Medien.",
        "me_places": "Orte in Medientiteln",
        "me_places_note": "Gezählt: Artikel, deren Titel den Namen nennt. Bezirksteile einzeln (z. B. Kreuzberg), „Mitte“ wird nicht gesucht, weil es auch ein Alltagswort ist. Rot = kbO.",
        "me_places_kind": "Zeigen", "kind_district": "Bezirke", "kind_place": "Orte",
        "share_of_source": "Anteil an allen Berlin-Artikeln der Quelle in %",
        # compare
        "co_q": "**Wo unterscheiden sich Polizeimeldungen und Medien?**",
        "co_cat": "Kategorien: gleiche Methode bei Polizei und Medien (nur Titel)",
        "co_cat_note": "Bei beiden wurden die Regeln aus Notebook 4.3 nur auf den Titel angewendet. Polizeititel nennen den politischen Hintergrund oft erst im Text, deshalb ist „Politisch motiviert“ bei der Polizei hier kleiner als mit der endgültigen Kategorie ({p} %).",
        "co_topics": "Themen: Anteil in den Medien geteilt durch Anteil in den Polizeimeldungen",
        "co_topics_note": ("Faktor über 1 (blau): Das Thema nimmt in den Medien mehr Raum ein. Polizei: Suchwörter in Titel und Text, "
                           "Medien: nur im Titel. Bei Schusswaffe und Vorwürfen gegen Polizei beruht der Faktor auf sehr kleinen Zahlen."),
        "co_factor": "Faktor (1 = gleich)",
        "co_brackets": "In Klammern: Anzahl Polizeimeldungen / Anzahl Medienartikel zum Thema.",
        "co_events": "Die vier Ereignisse: Polizeimeldungen und Medienartikel mit Bezug",
        "co_events_note": "Gleiche Suchwörter und gleicher Zeitraum wie im Notebook (5.4): Brandanschlag und CSD-Anschlag 0 bis 28 Tage danach, 1. Mai und Wahl 7 Tage davor bis 7 Tage danach.",
        "co_places": "Orte: Anteil an Meldungen bzw. Artikeln mit Ortsangabe",
        "co_places_note": "Medientitel nennen selten einen Ort, die Anteile beziehen sich deshalb nur auf Meldungen bzw. Artikel mit Ortsangabe (ohne Bezirke). Die Medien konzentrieren sich auf wenige bekannte Orte.",
        "ev_event": "Ereignis", "ev_date": "Datum", "ev_police": "Polizeimeldungen", "ev_media": "Medienartikel",
        "ev_titles": "verschiedene Titel", "ev_next": "Artikel am Tag danach",
        # force
        "fo_q": "**Gewalt gegen Polizei und Gewalt durch die Polizei: Meldungen und Medien im Vergleich**",
        "fo_warn": ("**Wichtig beim Lesen:** Eine Polizeimeldung beschreibt meist einen Fall. Über einen Fall erscheinen aber oft "
                    "Dutzende Medienartikel. Eine hohe Medienlinie heißt deshalb nicht, dass es viele Fälle gab. "
                    "Ob ein Einsatz rechtmäßig war, lässt sich aus Meldungen und Titeln nicht ablesen."),
        "fo_chart": "{topic} pro Monat",
        "fo_police_line": "Polizeimeldungen (meist 1 Fall je Meldung)", "fo_media_line": "Medienartikel (oft viele Artikel je Fall)",
        "fo_facts": ("Laut Polizeimeldungen gab es im ganzen Zeitraum **{s} Schusswaffeneinsätze der Polizei**, davon **{t} tödlich**. "
                     "{w} Meldungen nennen einen Waffeneinsatz der Polizei (Schusswaffe oder Taser/DEIG), {g} davon auch "
                     "einen Angriff auf Polizeikräfte (Gewalt gegen Polizei, ohne reinen Widerstand)."),
        "fo_shots": "Schusswaffeneinsätze der Polizei laut Polizeimeldungen",
        "fo_shots_note": "Nur Nummer, Datum, Bezirk und Ausgang laut Meldung. Die Meldungen stehen im Archiv der Polizei Berlin auf berlin.de.",
        "fo_nr": "Meldung Nr.", "fo_date": "Datum", "fo_fatal": "tödlich laut Meldung", "yes": "ja", "no": "nein",
        "fo_def": {
            "Gewalt gegen Polizei": "Tätlicher Angriff, Angriff oder verletzte Polizeikräfte, ohne reinen Widerstand.",
            "Schusswaffe durch Polizei": "Die Polizei schießt, z. B. „Schusswaffengebrauch“, „Polizei erschießt“, „Schussabgabe eines Polizeibeamten“.",
            "Taser/DEIG durch Polizei": "Einsatz eines Distanzelektroimpulsgeräts (DEIG, „Taser“) durch die Polizei. Eine bloße Androhung zählt nicht.",
            "Vorwürfe gegen Polizei": "Z. B. „Polizeigewalt“, „Körperverletzung im Amt“, „rassistische Polizeikontrolle“ sowie Tod in Gewahrsam oder nach einem Polizeieinsatz. Waffeneinsatz allein ist kein Vorwurf.",
        },
        "no_district": "ohne einzelnen Bezirk",
        "missing": "Datei fehlt: `{file}`. Bitte im Notebook Abschnitt 9.1 ausführen.",
        "about": """
### Worum es geht
Das Projekt erstellt ein Lagebild der öffentlichen Sicherheit in Berlin von Januar bis Oktober 2026, nur aus offenen Quellen,
und vergleicht Polizeimeldungen mit der Medienberichterstattung. Es ist ein technischer Überblick, keine wissenschaftliche Tiefenanalyse.

### Daten
- **Polizeimeldungen:** {reports} Pressemitteilungen der Polizei Berlin (Archiv auf berlin.de, ergänzt über Wayback Machine,
  Common Crawl und die Meldungsnummern). Geschätzte Abdeckung: {coverage} % aller Meldungen.
- **Medien:** {all_articles} deutschsprachige Online-Artikel mit Berlin-Bezug aus dem GDELT Global Knowledge Graph (Google BigQuery).
  Davon {articles} Artikel zu Polizei und Kriminalität in Berlin, ausgewählt über den Titel.
- **Einwohner:** Amt für Statistik Berlin-Brandenburg, Statistischer Bericht A I 5 (hj 1/26), Stichtag 30.06.2026, Tabelle 3 (Einwohner) und Tabelle 7 (Migrationshintergrund).
- **Haushaltseinkommen und Erwerbsbeteiligung:** Amt für Statistik Berlin-Brandenburg, Ergebnisse des Mikrozensus in Berlin 2025 (Erstergebnis), Tabellen 7.3 und 7.5.
- **Karte:** Geodatenportal Berlin (ALKIS Bezirke), OpenStreetMap (Nominatim), kbO-Liste der Polizei Berlin.

### Methoden
- **Kategorien:** Regeln (Suchwörter) und ein lokales Sprachmodell ({model}, über Ollama). Geprüft an 100 manuell
  kategorisierten Meldungen: Sprachmodell 94 % richtig, Regeln 83 %.
- **Themen:** Suchwörter in Titel und Text (Polizei) bzw. im Titel (Medien). Alle Muster stehen im Notebook.
- **Orte:** Python findet Straßen, Plätze und Bahnhöfe im Text und sucht ihre Koordinaten bei OpenStreetMap.
- **Vergleich:** Wo möglich wird bei Polizei und Medien dieselbe Methode verwendet. Verglichen werden Anteile, nicht absolute Zahlen.

### Grenzen
- Polizeimeldungen sind **keine Kriminalstatistik**. Die Polizei veröffentlicht nur eine Auswahl. Für Fallzahlen ist die PKS die richtige Quelle.
- Gezählt werden **Meldungen und Artikel, nicht Fälle**. Über einen Fall erscheinen oft viele Artikel, und derselbe Titel erscheint in mehreren Medien.
- Medienartikel werden **nur über den Titel** ausgewählt und eingeordnet. „Berlin“ steht in Titeln auch für Senat oder Bundespolitik.
- GDELT erfasst nur Online-Artikel, die es gefunden hat. Bezahlschranken, Fernsehen und Radio fehlen teilweise.
- Datum und Uhrzeit der Polizeimeldungen beziehen sich auf die **Veröffentlichung**, nicht auf die Tat.
- Ob ein Waffeneinsatz der Polizei rechtmäßig war, lässt sich aus Meldungen und Titeln **nicht** ablesen.
- Bevölkerung, Einkommen und Erwerbsbeteiligung gelten für **Bezirke, nicht für Personen**. Sie zeigen nicht, wer Taten begeht oder Opfer wird. Mit 12 Bezirken lassen sich Lage, Herkunft und soziale Lage nicht voneinander trennen.
- Das Dashboard enthält nur Zahlen, keine Texte von Meldungen oder Artikeln (Datenschutz, Urheberrecht).

### Mehr
Code, Notebook und alle Erklärungen: [GitHub-Repository des Projekts](https://github.com/Amirhouschang/osint-berlin-2026).
""",
    },
    "en": {
        "title": "OSINT Berlin 2026",
        "subtitle": ("Situation picture from open sources: press releases of the Berlin police and German-language "
                     "online media, **1 January to 21 October 2026**. All figures come from the project notebook. "
                     "The dashboard shows published reports and articles, not crime statistics."),
        "kpi_reports": "Police reports", "kpi_articles": "Media articles (selection)", "kpi_sources": "Media sources",
        "kpi_period": "Period", "kpi_period_value": "1 Jan to 21 Oct 2026",
        "tab_overview": "Overview", "tab_police": "Police reports", "tab_map": "Districts and map",
        "tab_media": "Media", "tab_compare": "Comparison", "tab_force": "Violence and police", "tab_about": "Methods",
        "month": "Month", "reports": "Reports", "articles": "Articles", "share_pct": "Share in %",
        "police": "Police reports", "media": "Media articles", "all": "All",
        "per_month": "per month", "per_day": "per day", "avg7": "7-day average",
        "show_events": "Show events", "district": "District", "all_districts": "All districts",
        "categories": "Categories", "topic": "Topic", "value": "Value",
        "src_police": "Source: Berlin police, press releases 2026 (berlin.de, completed via Wayback Machine and Common Crawl), own analysis.",
        "src_media": "Source: GDELT Global Knowledge Graph via Google BigQuery, German-language online articles related to Berlin, selection on police and crime (notebook 7.4), own analysis.",
        "src_both": "Sources: Berlin police, press releases 2026, and GDELT Global Knowledge Graph (Google BigQuery), own analysis.",
        "period_note": "Period: 1 Jan to 21 Oct 2026, October incomplete.",
        "term_cat": "“Firearms and OC” = firearms and organised crime. “Other” = none of the other categories applies.",
        "term_kbo": "kbO = crime hotspot (“kriminalitätsbelasteter Ort”), designated by the Berlin police (§ 17a ASOG Bln).",
        "ov_chart": "Police reports and media articles per month (share of each month in the total)",
        "ov_chart_note": ("To put both series on one scale, each line shows the share of the month in its total from "
                          "January to October. Grey: months of the four events."),
        "ov_facts": "Key findings (calculated from the data)",
        "fact_top_police": "Most frequent category of the police reports: **{cat}** ({pct} %).",
        "fact_top_district": "Most reports per resident: **{d}** ({v} per 100,000 residents, Berlin: {b}).",
        "fact_peak_media": "Strongest media day: **{day}** with {n} articles.",
        "fact_corr": "Police and media do not move together: correlation of the weekly values Pearson {r}, Spearman {s} (0 = no relation).",
        "fact_csd": "On the attack near the CSD: {p} police report, but {m} media articles. The first police report on it (no. 905) is missing from the data.",
        "fact_coverage": "An estimated {c} % of all reports of the Berlin police are covered (based on the report numbers).",
        "ov_how": ("**How to read the dashboard:** each tab answers one question. Below every chart you find the source, "
                   "period, basis and the explanation of the terms. Switch the language at the top right. Methods and "
                   "limitations are in the tab “Methods”."),
        "po_q": "**What does the Berlin police report on, and when?**",
        "po_month": "Police reports per month by category",
        "po_month_note": "Category: final category from notebook 4.8 (local language model {model}, checked against 100 manually categorised reports). Month of publication.",
        "po_day": "Police reports per day",
        "po_day_note": "Date of publication, not of the offence. Dashed: the four events.",
        "po_week": "Publication by weekday", "po_hour": "Publication by time of day",
        "po_time_note": "The time is only known for reports from the archive on berlin.de ({n} reports). Hour 10 = 10:00 to 10:59.",
        "po_cov": "Coverage per month (estimated from the report numbers)",
        "po_cov_note": "Coverage = available report numbers divided by the range from the lowest to the highest number of the month.",
        "po_filter_note": "The district filter applies to the monthly chart. Reports without a single district (Berlin-wide, supra-regional) only appear under “All districts”.",
        "hour": "Hour", "weekday": "Weekday", "coverage": "Coverage in %",
        "ma_q": "**Where do the reports occur?**",
        "ma_metric": "Colour districts by",
        # surroundings of the districts
        "su_head": "Surroundings of the districts: population, income and labour force status",
        "su_warn": ("**Important:** these figures describe districts, not people. They show in which surroundings reports "
                    "are published, but not who commits offences or becomes a victim. Police reports rarely name the origin "
                    "of the people involved, and many of them do not live in the district. For the nationality of suspects, "
                    "the Police Crime Statistics (PKS) are the right source."),
        "su_choose": "Feature", "su_her": "Nationality and migration background", "su_ein": "Household income",
        "su_erw": "Employed and unemployed",
        "su_erw_right": "Population aged 15 to under 65 by labour force status ({year})",
        "su_e1": "Employed", "su_e2": "Unemployed", "su_e3": "Not in the labour force", "su_e_quote": "Unemployment rate",
        "su_erw_note": ("Labour force status: Office for Statistics Berlin-Brandenburg, results of the microcensus in Berlin {year} "
                        "(first results), table 7.3. Sorted by reports per resident."),
        "su_erw_unsure": ("The number of unemployed per district is small: for {n} districts the office marks it as of limited "
                          "reliability, for {calc} it is not published and is calculated here as labour force minus employed."),
        "su_erw_def": ("Employed = paid work of at least one hour per week, including self-employed. Unemployed = without work, "
                       "actively looking and available at once (ILO definition, not the same as registered unemployment of the "
                       "Federal Employment Agency). Not in the labour force = neither employed nor unemployed, e.g. pupils, "
                       "students, pensioners. Unemployment rate = unemployed divided by labour force."),
        "su_left": "Police reports per 100,000 residents",
        "su_her_right": "Residents by nationality and migration background (30 Jun 2026)",
        "su_ein_right": "Households by monthly net household income ({year})",
        "su_share": "Share in the district in %",
        "su_g_ohne": "Germans without migration background", "su_g_mit": "Germans with migration background",
        "su_g_ausl": "Foreign nationals",
        "su_s1": "under €1,500", "su_s2": "€1,500 to €2,000", "su_s3": "€2,000 to €3,000", "su_s4": "€3,000 to €4,000",
        "su_s5": "€4,000 and more",
        "su_t_head": "Relation to reports per resident (Spearman: 1 = same ranking, 0 = no relation, negative = reverse ranking)",
        "su_t_share": "Feature", "su_t_all": "all 12 districts", "su_t_wo": "without {top2}",
        "su_t_mh": "with migration background (total)",
        "su_t_note": ("p = random test: share of random assignments of the districts with at least as strong a relation. "
                      "The larger p, the more likely the relation is chance; above about 0.05 it is not considered reliable. With 12 districts, inner-city location, visitors, "
                      "age and social situation cannot be separated."),
        "su_her_note": ("Residents: Office for Statistics Berlin-Brandenburg, statistical report A I 5 (hj 1/26), table 7, "
                        "reference date 30 Jun 2026. Sorted by reports per resident."),
        "su_mh_def": ("Migration background (population register): foreign nationality, second nationality, born abroad, "
                      "naturalisation or option status, or under 18 with at least one parent with migration background at "
                      "the same address. Foreign nationals always have a migration background."),
        "su_ein_note": ("Income: Office for Statistics Berlin-Brandenburg, results of the microcensus in Berlin {year} "
                        "(first results), table 7.5. Sorted by reports per resident."),
        "su_ein_def": ("Net household income = monthly net income of all members of a household, not weighted by household "
                       "size. Microcensus = sample of about 1 % of households, so district values are less precise than "
                       "figures from the population register."),
        "ma_m_abs": "Number of reports", "ma_m_rel": "Reports per 100,000 residents",
        "ma_map": "Map: districts by {metric} and places with at least 3 reports",
        "ma_metric_help": "The choice changes the colour of the districts and the number below each district name. The dots stay the same.",
        "ma_map_note": ("Districts: the darker, the higher the chosen value, the number below the name is this value. Dots: places named in at least 3 reports, size = number "
                        "of reports, red = kbO. District borders: Geoportal Berlin, ALKIS (Data licence Germany Zero 2.0). "
                        "Coordinates: OpenStreetMap via Nominatim (ODbL)."),
        "ma_rel": "Police reports per 100,000 residents by district",
        "ma_rel_note": ("Residents: Office for Statistics Berlin-Brandenburg, statistical report A I 5 (hj 1/26), reference date "
                        "{date}, registered residents. Visitors and commuters are not included, which mainly affects Mitte "
                        "and Friedrichshain-Kreuzberg. Dashed: Berlin as a whole ({b})."),
        "ma_heat": "Share of the categories per district in %",
        "ma_heat_note": "Each row adds up to 100 %. Only reports with a single district.",
        "ma_kbo": "Crime hotspots (kbO): police reports and media articles",
        "ma_kbo_note": "Counted: police reports whose title or text names the place, and media articles whose title names it. The list applies since 1 July 2026, the whole year is counted. No blue bar = no media title names this place.",
        "per_100k": "per 100,000 residents", "residents": "Residents", "rank": "Rank",
        "point_label": "{ort}: {n} reports, mostly {cat}",
        "me_q": "**What do the media report on police and crime in Berlin?**",
        "me_month": "Media articles per month by category",
        "me_month_note": ("Category: the same rules as for the police (notebook 4.3), applied to the title only. "
                          "“Other” = the title contains a selection word (e.g. attack, police, demo), but no category applies."),
        "me_day": "Media articles per day",
        "me_day_note": "Date according to GDELT. Dashed: the four events. One event often produces hundreds of articles.",
        "me_sources": "The 15 sources with the most articles",
        "me_sources_note": "Source = website according to GDELT. Share = share of all Berlin articles of this website. {u} different titles for {n} articles: the same title often appears in several media.",
        "me_places": "Places in media titles",
        "me_places_note": "Counted: articles whose title names the place. Parts of district names separately (e.g. Kreuzberg); “Mitte” is not searched because it is also an everyday word. Red = kbO.",
        "me_places_kind": "Show", "kind_district": "Districts", "kind_place": "Places",
        "share_of_source": "Share of all Berlin articles of the source in %",
        "co_q": "**Where do police reports and media differ?**",
        "co_cat": "Categories: same method for police and media (title only)",
        "co_cat_note": "For both, the rules of notebook 4.3 were applied to the title only. Police titles often name the political background only in the text, so “Politically motivated” is smaller here than with the final category ({p} %).",
        "co_topics": "Topics: share in the media divided by share in the police reports",
        "co_topics_note": ("Factor above 1 (blue): the topic takes up more space in the media. Police: search words in title and text, "
                           "media: title only. For firearm use and allegations against police, the factor rests on very small numbers."),
        "co_factor": "Factor (1 = equal)",
        "co_brackets": "In brackets: number of police reports / number of media articles on the topic.",
        "co_events": "The four events: police reports and media articles related to them",
        "co_events_note": "Same search words and period as in the notebook (5.4): arson attack and CSD attack 0 to 28 days after, 1 May and election 7 days before to 7 days after.",
        "co_places": "Places: share of reports or articles that name a place",
        "co_places_note": "Media titles rarely name a place, so the shares only refer to reports or articles with a place (without districts). The media concentrate on a few well-known places.",
        "ev_event": "Event", "ev_date": "Date", "ev_police": "Police reports", "ev_media": "Media articles",
        "ev_titles": "different titles", "ev_next": "articles on the day after",
        "fo_q": "**Violence against police and use of force by police: reports and media compared**",
        "fo_warn": ("**Important:** a police report usually describes one case. But one case often produces dozens of media "
                    "articles. A high media line therefore does not mean that there were many cases. Whether an operation "
                    "was lawful cannot be read from reports and titles."),
        "fo_chart": "{topic} per month",
        "fo_police_line": "Police reports (mostly 1 case per report)", "fo_media_line": "Media articles (often many per case)",
        "fo_facts": ("According to the police reports, there were **{s} cases of firearm use by the police** in the whole period, **{t} of them fatal**. "
                     "{w} reports mention the use of a weapon by the police (firearm or Taser), {g} of them also an attack "
                     "on police officers (violence against police, without mere resistance)."),
        "fo_shots": "Firearm use by the police according to police reports",
        "fo_shots_note": "Only number, date, district and outcome according to the report. The reports are in the archive of the Berlin police on berlin.de.",
        "fo_nr": "Report no.", "fo_date": "Date", "fo_fatal": "fatal according to report", "yes": "yes", "no": "no",
        "fo_def": {
            "Gewalt gegen Polizei": "Physical assault, attack or injured police officers, without mere resistance.",
            "Schusswaffe durch Polizei": "The police fire a weapon, e.g. “Schusswaffengebrauch”, “Polizei erschießt”, “Schussabgabe eines Polizeibeamten”.",
            "Taser/DEIG durch Polizei": "Use of a conducted energy device (DEIG, “Taser”) by the police. A mere threat does not count.",
            "Vorwürfe gegen Polizei": "E.g. “Polizeigewalt” (police violence), “Körperverletzung im Amt” (bodily harm in office), “racist police check”, and death in custody or after a police operation. Use of a weapon alone is no allegation.",
        },
        "no_district": "no single district",
        "missing": "File missing: `{file}`. Please run section 9.1 of the notebook.",
        "about": """
### What it is about
The project builds a picture of public safety in Berlin from January to October 2026 from open sources only and compares
police reports with media coverage. It is a technical overview, not an in-depth scientific analysis.

### Data
- **Police reports:** {reports} press releases of the Berlin police (archive on berlin.de, completed via Wayback Machine,
  Common Crawl and the report numbers). Estimated coverage: {coverage} % of all reports.
- **Media:** {all_articles} German-language online articles related to Berlin from the GDELT Global Knowledge Graph (Google BigQuery).
  Of these, {articles} articles on police and crime in Berlin, selected via the title.
- **Residents:** Office for Statistics Berlin-Brandenburg, statistical report A I 5 (hj 1/26), reference date 30 June 2026, table 3 (residents) and table 7 (migration background).
- **Household income and labour force status:** Office for Statistics Berlin-Brandenburg, results of the microcensus in Berlin 2025 (first results), tables 7.3 and 7.5.
- **Map:** Geoportal Berlin (ALKIS districts), OpenStreetMap (Nominatim), kbO list of the Berlin police.

### Methods
- **Categories:** rules (search words) and a local language model ({model}, via Ollama). Checked against 100 manually
  categorised reports: language model 94 % correct, rules 83 %.
- **Topics:** search words in title and text (police) or in the title (media). All patterns are in the notebook.
- **Places:** Python finds streets, squares and stations in the text and looks up their coordinates on OpenStreetMap.
- **Comparison:** where possible, the same method is used for police and media. Shares are compared, not absolute numbers.

### Limitations
- Police reports are **not crime statistics**. The police only publish a selection. For case numbers, the PKS is the right source.
- **Reports and articles are counted, not cases.** One case often produces many articles, and the same title appears in several media.
- Media articles are selected and classified **by their title only**. “Berlin” in titles can also stand for the Senate or federal politics.
- GDELT only covers online articles it has found. Paywalls, TV and radio are partly missing.
- Date and time of the police reports refer to the **publication**, not to the offence.
- Whether a use of force by the police was lawful **cannot** be read from reports and titles.
- Population, income and labour force status apply to **districts, not to persons**. They do not show who commits offences or becomes a victim. With 12 districts, location, origin and social situation cannot be separated.
- The dashboard only contains numbers, no texts of reports or articles (data protection, copyright).

### More
Code, notebook and all explanations: [GitHub repository of the project](https://github.com/Amirhouschang/osint-berlin-2026).
""",
    },
}
