[Deutsch](README.md) | **English**

# OSINT Berlin 2026: Police Reports and Media

**Python · SQLite · BigQuery · local AI · Streamlit**

A picture of public safety in Berlin from January to October 2026, from open sources only. It is based on
**1,272 press releases of the Berlin police** and **8,807 German-language online articles** on police and crime in
Berlin from the GDELT Global Knowledge Graph. The project shows what the police report on, when and in which
districts, and where police reports and media coverage differ.

**[Open the interactive dashboard](https://osint-berlin-2026.streamlit.app/?lang=en)** · [Notebook](osint_berlin_2026.ipynb)

![Police reports and media articles per month, January to October 2026](images/polizei_medien_pro_monat.png)

**Three results at a glance**
- Police and media do not move together: the weekly values are not related (Pearson -0.21, Spearman -0.01). For the attack near the CSD (Pride) there is one police report, but 961 media articles.
- Per resident, Friedrichshain-Kreuzberg comes first (48.3 reports per 100,000 residents, Berlin 29.8). Pankow drops from rank 6 by number of reports to rank 11 per resident.
- The police publish evenly over the year, the media follow big events: January and July together bring more than a third of all articles.

> **Scope:** Police reports are not crime statistics. The police only publish a selection of their cases. The
> project describes what is published, not how much crime there is. Details: [Scope and notes](#scope-and-notes).

---

## Research questions

1. What does the Berlin police report on, and how are the reports spread across topics?
2. How does the number of reports change over the year, and do big events (arson attack on the power grid in January, 1 May, attack near the CSD in July, Berlin state election in September) cause visible peaks?
3. Which districts and places appear most often in the reports?
4. Where do police reports and media coverage differ?

## Data

| | |
|---|---|
| Period | 1 Jan to 21 Oct 2026 (October incomplete) |
| Police reports | 1,272 after cleaning, estimated coverage 90.8 % based on the report numbers |
| Media | 132,636 German-language online articles related to Berlin, of which 8,807 on police and crime from 232 sources |
| Residents and surroundings | Office for Statistics Berlin-Brandenburg: population register (30 June 2026) and microcensus 2025 |
| Language | German |

---

## Structure

The whole project is in one notebook with numbered sections, interpretations, limitations and sources (in German).

| No. | Section | Content |
|---|---|---|
| 1 | Project overview | aim, research questions, data collection |
| 2 | Data overview | size, missing values, completeness via the report numbers, duplicates |
| 3 | Cleaning | duplicates, technical remains, time columns, places of the event |
| 4 | Categorisation | rules and local language model, model comparison, manual sample |
| 5 | Over time | reports per day, the four events, election campaign, topics, violence against police |
| 6 | Districts and places | reports per resident, surroundings of the districts, places from the text, crime hotspots, map |
| 7 | Media | GDELT via BigQuery, selection by title, categories, topics, places, sources |
| 8 | Comparison | categories, time, events, topics, places, violence against and by the police |
| 9 | Dashboard | export of the tables, starting the dashboard |

### Data collection
- Three scripts of my own, all writing into one SQLite database:
  - `scrape_polizeimeldungen.py`: archive 2026 on berlin.de (988 reports, with time)
  - `find_missing_meldungen.py`: Wayback Machine, Common Crawl and sub-pages (143 more reports)
  - `id_scan.py`: direct request by report ID (146 more reports)
- Reason: the official archive does not list all reports. The highest report number up to 21 Oct 2026 is 1399, the archive only had 988 entries, and June was almost completely missing.
- All requests with pauses between them and after checking robots.txt.

### Categorisation
- 12 categories, first with rules (search words), then with a **locally run language model** (`Ollama`). The reports are not sent to a cloud.
- Four models compared: Gemma 4 (26B), Mistral Small 3.1, Qwen 3.6, Gemma 2
- Checked against 100 manually categorised reports: rules 83 % correct, models 89 to 94 %
- **Model chosen: Gemma 4**, as accurate as Mistral but more than three times faster
- Biggest gain for "politically motivated": a reference to a motive or to the state security police often only comes at the end of the text. According to the model, 13 % of the reports are politically motivated, according to the rules only 7 %.

### Media
- GDELT Global Knowledge Graph via Google BigQuery, filtered to German-language articles with a place in Berlin
- Selection by title: a Berlin reference (Berlin, districts, places from section 6) and a word on police or crime
- The same rules as for the police, so both sides can be compared
- The GDELT DOC API could not be used because of blocks, this is documented in the notebook (7.1)

### Districts and surroundings

![Police reports per 100,000 residents by district, January to October 2026](images/meldungen_je_einwohner.png)

- Next to the reports per resident, each district shows: population by nationality and migration background, net household income, and employed and unemployed people
- Friedrichshain-Kreuzberg, Mitte and Neukölln are at the top for all three features and at the same time have the most reports per resident. Without Friedrichshain-Kreuzberg and Mitte, none of the features shows a reliable relation.
- The comparison applies to districts, not to persons (see [Scope and notes](#scope-and-notes))

### Dashboard
- Interactive charts with `Plotly` in a `Streamlit` app, in German and English: [Open the dashboard](https://osint-berlin-2026.streamlit.app/?lang=en)
- Below every chart: source, period, basis and the explanation of the terms
- Only reads the finished tables in `dashboard/data/` (numbers, no texts of reports or articles); locally: `streamlit run dashboard/app.py`

---

## Tech stack

| Area | Tools |
|---|---|
| Language & environment | Python, Jupyter, conda, Linux |
| Data collection | Requests, Beautiful Soup, Wayback Machine CDX API, Common Crawl Index |
| Database | SQLite |
| Media | Google BigQuery (GDELT GKG), google-cloud-bigquery |
| Analysis | pandas, NumPy |
| Local AI | Ollama (Gemma 4, Mistral Small 3.1, Qwen 3.6, Gemma 2) |
| Map & geodata | folium, OpenStreetMap Nominatim, Geoportal Berlin |
| Visualisation | matplotlib; Plotly, Streamlit |

---

## Project structure

```
berlin_osint_2026/
├── README.md                  ← German version
├── README.en.md               ← English version
├── osint_berlin_2026.ipynb    ← the whole project
├── scrape_polizeimeldungen.py ← archive on berlin.de
├── find_missing_meldungen.py  ← Wayback Machine, Common Crawl
├── id_scan.py                 ← request by report ID
├── images/                    ← two charts for the README
├── dashboard/
│   ├── app.py                 ← Streamlit app
│   ├── i18n.py                ← all texts in German and English
│   ├── requirements.txt       ← packages of the dashboard
│   └── data/                  ← tables from section 9.1, numbers only
└── data/                      ← raw data, database and full texts (not in the repository)
```

---

## Scope and notes

> **Not crime statistics:** the police only publish a selection of their cases, mainly those of public interest or
> with a call for witnesses. Reports and articles are counted, not cases. For case numbers, the Police Crime
> Statistics (PKS) are the right source.

> **Districts, not people:** the comparisons with population, income and unemployment describe the surroundings of
> the districts. They do not show who commits offences or becomes a victim. Police reports rarely name the origin of
> the people involved, and many of them do not live in the district. With 12 districts, inner-city location,
> visitors, origin and social situation cannot be separated.

> **Media by title:** media articles are only selected and categorised by their title, police reports by title and
> text. One case often produces dozens of articles, so a high number of articles does not mean that there were many
> cases.

> **Wording:** the analysis makes no political judgement. In ongoing proceedings, suspects are referred to as
> alleged offenders. Whether a police operation was lawful cannot be read from reports and titles.

All limitations in detail: section "Limitations" in the notebook.

---

## Data protection & copyright

- only **publicly available** press releases, article metadata and official statistics
- The full texts of the police reports and the media articles are **not part of the repository**, because the reports partly describe persons (e.g. missing persons) and the articles are protected by copyright. GitHub only contains the analyses.
- The dashboard contains only numbers, no titles and no texts
- Categorisation with the language model runs **locally**
- No credentials in the code: the BigQuery login runs via the Google login in the browser. Raw data is excluded from the repository.

## Skills shown by the project

- Web scraping with several routes when a source is incomplete (archive, Wayback Machine, Common Crawl, ID requests)
- Data quality: measuring completeness, finding gaps and duplicates, documenting limitations
- SQL with SQLite and large queries in BigQuery (with dry run and local cache)
- Use and **validation** of local AI: model comparison against a manual sample
- Geodata: places from the text, coordinates, map, linking with official statistics
- Source-critical comparison of police reports and media
- Bilingual dashboard for readers without prior knowledge

## Status

All nine sections are finished. The notebook is extended and corrected when needed.

---

## Main sources

- Berlin police: police reports, archive 2026. https://www.berlin.de/polizei/polizeimeldungen/archiv/2026/
- GDELT Project: Global Knowledge Graph 2.1 in Google BigQuery. https://www.gdeltproject.org/data.html
- Office for Statistics Berlin-Brandenburg: statistical report A I 5 (hj 1/26), population register Berlin 30 June 2026. https://www.statistik-berlin-brandenburg.de/a-i-5-hj
- Office for Statistics Berlin-Brandenburg: results of the microcensus in Berlin 2025 (first results). https://www.statistik-berlin-brandenburg.de
- Berlin police: crime hotspots in Berlin (kriminalitätsbelastete Orte). https://www.berlin.de/polizei/polizeimeldungen/fakten-hintergruende/artikel.1078268.php
- Geoportal Berlin: ALKIS Berlin districts, Data licence Germany Zero 2.0. https://gdi.berlin.de/services/wfs/alkis_bezirke
- OpenStreetMap: Nominatim, data © OpenStreetMap contributors (ODbL). https://nominatim.openstreetmap.org/

All sources: section "Quellen" in the notebook.

---

## Rights

© 2026 Amirhoushang Rahmannejad. All rights reserved. Viewing and reviewing is explicitly welcome. Copying, modifying or redistributing only with my written permission.
