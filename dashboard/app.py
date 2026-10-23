"""
app.py – Interactive dashboard: OSINT Berlin 2026 (police reports and media, 1 Jan – 21 Oct 2026)
=================================================================================================

RUN (in the project folder):
  pip install -r dashboard/requirements.txt
  streamlit run dashboard/app.py

WHAT IT SHOWS (languages: Deutsch, English – switch at the top right)
  Overview             – key figures, police and media per month, key findings calculated from the data
  Police reports       – categories per month (filter by district), reports per day, time of publication, coverage
  Districts and map    – map of districts and places, reports per 100,000 residents, categories per district, kbO
  Media                – categories per month, articles per day, sources, places in titles
  Comparison           – categories, topics, the four events and places: police and media side by side
  Violence and police  – violence against police and use of force by police, per month, police and media
  Methods              – data, methods, limitations

DATA
  Only the finished tables in dashboard/data/ are read (numbers, no texts of reports or articles).
  They are written by section 9.1 of the notebook osint_berlin_2026.ipynb.
  DATA_DIR (environment variable) can point to another folder. All texts are in dashboard/i18n.py.
"""

import json
import math
import os
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import sample_colorscale
import streamlit as st

from i18n import (CATEGORIES, CATEGORY_COLORS, COLOR_KBO, COLOR_MEDIA, COLOR_POLICE, EVENTS, LANGS, MONTHS,
                  POLICE_TOPICS, TOPICS, UI, WEEKDAYS)

HERE = Path(__file__).resolve().parent
DATA = Path(os.environ.get("DATA_DIR", HERE / "data"))
GRID = "rgba(128,128,128,0.2)"
GREY = "rgba(128,128,128,0.95)"
EVENT_FILL = "rgba(128,128,128,0.10)"

st.set_page_config(page_title="OSINT Berlin 2026", page_icon="📊", layout="wide")


# ----------------------------------------------------------------------------------------------------------------
# data
# ----------------------------------------------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def read_csv(name):
    path = DATA / name
    return pd.read_csv(path, encoding="utf-8") if path.exists() else None


@st.cache_data(show_spinner=False)
def read_json(name):
    path = DATA / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def ring_area(ring):
    """Signed area of a ring (shoelace formula): positive = counter-clockwise."""
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1])) / 2


def rewind(geojson):
    """plotly draws GeoJSON with d3-geo, which expects the outer ring clockwise and holes counter-clockwise
    (the opposite of the GeoJSON standard). Without this the districts are not drawn."""
    def fix(polygon):
        return [r if (ring_area(r) < 0) == (i == 0) else r[::-1] for i, r in enumerate(polygon)]
    for f in geojson["features"]:
        g = f["geometry"]
        if g["type"] == "Polygon":
            g["coordinates"] = fix(g["coordinates"])
        elif g["type"] == "MultiPolygon":
            g["coordinates"] = [fix(p) for p in g["coordinates"]]
    return geojson


@st.cache_data(show_spinner=False)
def read_geojson(name):
    """The district borders, read once and turned into the ring direction plotly needs."""
    path = DATA / name
    return rewind(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else None


def load(name, lang):
    """Reads a table of dashboard/data; shows a message and returns None when it is missing."""
    if name.endswith(".geojson"):
        data = read_geojson(name)
    else:
        data = read_json(name) if name.endswith(".json") else read_csv(name)
    if data is None:
        st.warning(UI[lang]["missing"].format(file=f"dashboard/data/{name}"))
    return data


# ----------------------------------------------------------------------------------------------------------------
# formatting and small helpers
# ----------------------------------------------------------------------------------------------------------------
def word(w, lang):
    """Substantiv im Fließtext: im Englischen klein geschrieben."""
    return w.lower() if lang == "en" else w


def num(x, lang, digits=0):
    """Number in the format of the language: 1.272,5 (de) or 1,272.5 (en)."""
    text = f"{x:,.{digits}f}"
    return text.replace(",", "§").replace(".", ",").replace("§", ".") if lang == "de" else text


def month_label(m, lang):
    return MONTHS[lang][int(str(m)[5:7]) - 1]


def date_label(d, lang):
    d = pd.Timestamp(d)
    return d.strftime("%d.%m.%Y") if lang == "de" else d.strftime("%d %b %Y")


def cat(name, lang):
    return CATEGORIES.get(name, {}).get(lang, name)


def topic(name, lang):
    return TOPICS.get(name, {}).get(lang, name)


def note(*parts):
    """Grey text under a chart: source, period, basis, terms."""
    st.caption("  \n".join(p for p in parts if p))


def control(kind, host, label, key, lang, options=None, default=None, **kw):
    """selectbox / radio / multiselect / checkbox whose choice survives a change of language.
    Streamlit loses the selection of a widget when its labels change. Every language therefore gets its own widget
    (key + language); the language-independent choice is kept in session_state and used as its start value."""
    shared = f"choice_{key}"
    value = st.session_state.get(shared, default)
    wkey = f"{key}__{lang}"
    if kind == "checkbox":
        out = host.checkbox(label, value=bool(value), key=wkey)
    elif kind == "multiselect":
        out = host.multiselect(label, options, default=[v for v in (value or []) if v in options], key=wkey, **kw)
    else:
        index = options.index(value) if value in options else (options.index(default) if default in options else 0)
        out = getattr(host, kind)(label, options, index=index, key=wkey, **kw)
    st.session_state[shared] = out
    return out


def show(fig, lang, height, legend_top=True):
    """Common look: transparent background, legend BELOW the plot (the space above is for event labels),
    number format of the language."""
    names = [tr.name for tr in fig.data if tr.name and tr.showlegend is not False]
    rows = math.ceil(sum(len(n) * 7 + 50 for n in names) / 1100) if len(names) > 1 else 0
    bottom = 50 + 24 * rows                                           # x labels, then the legend rows
    fig.update_layout(height=height + bottom, margin=dict(l=10, r=10, t=fig.layout.margin.t or 30, b=bottom),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      legend=dict(orientation="h", yref="container", y=0, yanchor="bottom", xanchor="left", x=0),
                      separators=",." if lang == "de" else ".,", font=dict(size=13))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


def event_months(lang):
    """{month 'YYYY-MM': (number, event name)} of the four events (from ereignisse.csv)."""
    ev = read_csv("ereignisse.csv")
    if ev is None:
        return {}
    ev = ev.sort_values("datum").reset_index(drop=True)
    return {d[:7]: (i + 1, EVENTS.get(e, {}).get(lang, e)) for i, (e, d) in enumerate(zip(ev["ereignis"], ev["datum"]))}


def shade_event_months(fig, months, lang):
    """Grey band behind the months of the four events, with a number above the plot (names in the note)."""
    for m, (nr, _) in event_months(lang).items():
        if m in months:
            i = months.index(m)
            fig.add_vrect(x0=i - 0.45, x1=i + 0.45, fillcolor=EVENT_FILL, line_width=0, layer="below")
            fig.add_annotation(x=i, y=1, yref="paper", yanchor="bottom", text=str(nr), showarrow=False,
                               font=dict(size=12, color=GREY))


def event_legend(lang):
    ev = event_months(lang)
    return "  ·  ".join(f"{nr} = {name}" for nr, name in sorted(ev.values()))


def event_lines(fig, lang):
    """Dashed line at the date of each event, the name ABOVE the plot so that no data line runs through it."""
    ev = read_csv("ereignisse.csv")
    if ev is None:
        return
    for i, (e, d) in enumerate(zip(ev["ereignis"], ev["datum"])):
        fig.add_shape(type="line", x0=d, x1=d, y0=0, y1=1.06, xref="x", yref="paper",
                      line=dict(color="rgba(128,128,128,0.6)", width=1, dash="dash"))
        fig.add_annotation(x=d, y=1.06, yref="paper", yanchor="bottom", xanchor="left", xshift=2,
                           text=EVENTS.get(e, {}).get(lang, e), showarrow=False, font=dict(size=11, color=GREY))


def category_order(names):
    order = list(CATEGORIES)
    return sorted(names, key=lambda c: order.index(c) if c in order else 99)


# ----------------------------------------------------------------------------------------------------------------
# tab: overview
# ----------------------------------------------------------------------------------------------------------------
def tab_overview(lang, k):
    t = UI[lang]
    st.markdown(t["ov_how"])
    tag = load("tag.csv", lang)
    pm = load("polizei_monat.csv", lang)
    if tag is None or pm is None:
        return
    tag["monat"] = tag["datum"].str[:7]
    monthly = tag.groupby("monat")[["polizei", "medien"]].sum()
    share = monthly / monthly.sum() * 100
    months = list(share.index)

    st.markdown(f"#### {t['ov_chart']}")
    fig = go.Figure()
    for col, name, color in [("polizei", t["police"], COLOR_POLICE), ("medien", t["media"], COLOR_MEDIA)]:
        fig.add_trace(go.Scatter(x=[month_label(m, lang) for m in months], y=share[col], name=name,
                                 mode="lines+markers", line=dict(color=color, width=3), marker=dict(size=7),
                                 customdata=monthly[col], hovertemplate="%{y:.1f} %  (n = %{customdata})"))
    shade_event_months(fig, months, lang)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(title=t["share_pct"], rangemode="tozero", gridcolor=GRID)
    show(fig, lang, 400)
    note(t["ov_chart_note"], event_legend(lang), t["src_both"], t["period_note"])

    st.markdown(f"#### {t['ov_facts']}")
    total = pm.groupby("kategorie")["meldungen"].sum().sort_values(ascending=False)
    top_cat, top_n = total.index[0], total.iloc[0]
    bez = read_csv("bezirke.csv")
    ev = read_csv("ereignisse.csv")
    facts = [t["fact_top_police"].format(cat=cat(top_cat, lang), pct=num(top_n / total.sum() * 100, lang, 1))]
    if bez is not None:
        b = bez.sort_values("je_100000", ascending=False).iloc[0]
        berlin = k["meldungen_mit_bezirk"] / k["einwohner_berlin"] * 100_000
        facts.append(t["fact_top_district"].format(d=b["bezirk"], v=num(b["je_100000"], lang, 1), b=num(berlin, lang, 1)))
    peak = tag.loc[tag["medien"].idxmax()]
    facts.append(t["fact_peak_media"].format(day=date_label(peak["datum"], lang), n=num(peak["medien"], lang)))
    facts.append(t["fact_corr"].format(r=num(k["korrelation_pearson"], lang, 2), s=num(k["korrelation_spearman"], lang, 2)))
    if ev is not None and (ev["ereignis"] == "Anschlag im Umfeld des CSD").any():
        e = ev[ev["ereignis"] == "Anschlag im Umfeld des CSD"].iloc[0]
        facts.append(t["fact_csd"].format(p=int(e["polizei"]), m=num(e["medien"], lang)))
    facts.append(t["fact_coverage"].format(c=num(k["abdeckung_gesamt"], lang, 1)))
    st.markdown("\n".join(f"- {f}" for f in facts))


# ----------------------------------------------------------------------------------------------------------------
# tab: police reports
# ----------------------------------------------------------------------------------------------------------------
def stacked_months(table, value, lang, ytitle, cats):
    months = sorted(table["monat"].unique())
    wide = table.pivot_table(index="monat", columns="kategorie", values=value, aggfunc="sum").reindex(months).fillna(0)
    fig = go.Figure()
    for c in cats:
        if c in wide:
            fig.add_trace(go.Bar(x=[month_label(m, lang) for m in months], y=wide[c], name=cat(c, lang),
                                 marker_color=CATEGORY_COLORS.get(c, "#7a7a7a"), hovertemplate="%{y}"))
    sums = wide[[c for c in cats if c in wide]].sum(axis=1)
    fig.add_trace(go.Scatter(x=[month_label(m, lang) for m in months], y=sums, mode="text", text=[num(s, lang) for s in sums],
                             textposition="top center", showlegend=False, hoverinfo="skip"))
    fig.update_layout(barmode="stack", hovermode="x unified")
    fig.update_yaxes(title=ytitle, gridcolor=GRID, range=[0, sums.max() * 1.15 if len(sums) else 1])
    shade_event_months(fig, months, lang)
    return fig


def tab_police(lang, k):
    t = UI[lang]
    st.markdown(t["po_q"])
    pm = load("polizei_monat.csv", lang)
    if pm is None:
        return
    districts = sorted(d for d in pm["bezirk"].unique() if d != "ohne einzelnen Bezirk")
    c1, c2 = st.columns([1, 2])
    district = control("selectbox", c1, t["district"], "po_district", lang, ["__all__"] + districts, "__all__",
                       format_func=lambda d: t["all_districts"] if d == "__all__" else d)
    all_cats = category_order(pm["kategorie"].unique())
    chosen = control("multiselect", c2, t["categories"], "po_cats", lang, all_cats, all_cats,
                     format_func=lambda c: cat(c, lang))
    part = pm if district == "__all__" else pm[pm["bezirk"] == district]
    n = int(part.loc[part["kategorie"].isin(chosen), "meldungen"].sum())
    head = t["po_month"] + ("" if district == "__all__" else f": {district}")
    st.markdown(f"#### {head} ({num(n, lang)} {word(t['reports'], lang)})")
    if chosen:
        show(stacked_months(part, "meldungen", lang, t["reports"], chosen), lang, 430)
    note(t["po_month_note"].format(model=k["modell"]), t["term_cat"], t["po_filter_note"], event_legend(lang),
         t["src_police"], t["period_note"])

    tag = load("tag.csv", lang)
    if tag is not None:
        st.markdown(f"#### {t['po_day']}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tag["datum"], y=tag["polizei"], name=t["per_day"], mode="lines",
                                 line=dict(color="#a9c8ee", width=1)))
        fig.add_trace(go.Scatter(x=tag["datum"], y=tag["polizei"].rolling(7, center=True).mean(), name=t["avg7"],
                                 mode="lines", line=dict(color=COLOR_MEDIA, width=2.5), hovertemplate="%{y:.1f}"))
        event_lines(fig, lang)
        fig.update_layout(hovermode="x unified", margin=dict(t=60))
        fig.update_xaxes(tickformat="%d.%m." if lang == "de" else "%d %b", dtick="M1")
        fig.update_yaxes(title=t["reports"], rangemode="tozero", gridcolor=GRID)
        show(fig, lang, 380)
        note(t["po_day_note"], t["src_police"], t["period_note"] + f" n = {num(k['meldungen'], lang)}.")

    wd, hr = read_csv("wochentag.csv"), read_csv("stunde.csv")
    if wd is not None and hr is not None:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"#### {t['po_week']}")
            fig = go.Figure(go.Bar(x=[WEEKDAYS[d][lang] for d in wd["wochentag"]], y=wd["meldungen"],
                                   marker_color=COLOR_MEDIA, text=wd["meldungen"], textposition="inside",
                                   insidetextanchor="end", textfont=dict(color="white"),
                                   hovertemplate="%{x}: %{y}<extra></extra>"))      # value white at the top inside the bar
            fig.update_yaxes(title=t["reports"], gridcolor=GRID)
            show(fig, lang, 320, legend_top=False)
        with c2:
            st.markdown(f"#### {t['po_hour']}")
            fig = go.Figure(go.Bar(x=hr["stunde"], y=hr["meldungen"], marker_color=COLOR_MEDIA))
            fig.update_xaxes(title=t["hour"], dtick=2)
            fig.update_yaxes(title=t["reports"], gridcolor=GRID)
            show(fig, lang, 320, legend_top=False)
        note(t["po_time_note"].format(n=num(hr["meldungen"].sum(), lang)), t["src_police"], t["period_note"])

    cov = read_csv("abdeckung.csv")
    if cov is not None:
        st.markdown(f"#### {t['po_cov']}")
        fig = go.Figure(go.Bar(x=[month_label(m, lang) for m in cov["monat"]], y=cov["abdeckung_pct"],
                               marker_color=COLOR_MEDIA, text=[f"{num(v, lang)} %" for v in cov["abdeckung_pct"]],
                               textposition="inside", insidetextanchor="end", textfont=dict(color="white"),
                               hovertemplate="%{x}: %{y:.1f} %<extra></extra>"))   # value white at the top inside the bar
        fig.update_yaxes(title=t["coverage"], range=[0, 100], gridcolor=GRID)
        show(fig, lang, 300, legend_top=False)
        note(t["po_cov_note"], t["src_police"], t["period_note"])


# ----------------------------------------------------------------------------------------------------------------
# tab: districts and map
# ----------------------------------------------------------------------------------------------------------------
def district_map(geo, bez, pts, col, lang):
    """Map without a background map: the district borders as filled areas, the places as dots.
    Drawn on plain x/y axes (longitude, latitude), so it needs no map server and works everywhere."""
    t = UI[lang]
    lo, hi = bez[col].min(), bez[col].max()
    scale = [[0, "#eef4fc"], [0.5, "#86b6ef"], [1, "#0d366b"]]
    values = bez.set_index("bezirk")
    fig = go.Figure()
    for f in geo["features"]:
        name = f["properties"]["bezirk"]
        if name not in values.index:
            continue
        r = values.loc[name]
        color = sample_colorscale(scale, [(r[col] - lo) / (hi - lo) if hi > lo else 0.5])[0]
        polygons = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
        hover = (f"<b>{name}</b><br>{t['reports']}: {num(r['meldungen'], lang)}<br>{t['residents']}: "
                 f"{num(r['einwohner'], lang)}<br>{t['per_100k']}: {num(r['je_100000'], lang, 1)}")
        for poly in polygons:
            ring = poly[0]
            fig.add_trace(go.Scatter(x=[p[0] for p in ring], y=[p[1] for p in ring], fill="toself", fillcolor=color,
                                     mode="lines", line=dict(color="white", width=1.5), hoverinfo="text", text=hover,
                                     hoveron="fills", showlegend=False))
    for f in geo["features"]:                     # district name and the chosen value in the middle of the area
        name = f["properties"]["bezirk"]
        if name not in values.index:
            continue
        polygons = f["geometry"]["coordinates"] if f["geometry"]["type"] == "MultiPolygon" else [f["geometry"]["coordinates"]]
        ring = max((poly[0] for poly in polygons), key=len)
        value = num(values.loc[name, col], lang, 0 if col == "meldungen" else 1)
        fig.add_annotation(x=sum(p[0] for p in ring) / len(ring), y=sum(p[1] for p in ring) / len(ring),
                           text=name.replace("-", "-<br>") + f"<br><b>{value}</b>", showarrow=False,
                           font=dict(size=10, color="#3d3c39"), bgcolor="rgba(255,255,255,0.65)")
    for is_kbo, color in [(False, "#0d366b"), (True, COLOR_KBO)]:
        p = pts[pts["kbo"] == is_kbo]
        fig.add_trace(go.Scatter(
            x=p["lon"], y=p["lat"], mode="markers", showlegend=False,
            marker=dict(size=5 + p["meldungen"] ** 0.5 * 3, color=color, opacity=0.85, line=dict(color="white", width=0.8)),
            text=[t["point_label"].format(ort=o, n=n, cat=cat(c, lang)) for o, n, c in
                  zip(p["ort"], p["meldungen"], p["haeufigste_kategorie"])],
            hovertemplate="%{text}<extra></extra>"))
    # colour bar: an invisible point that carries the scale
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", showlegend=False, hoverinfo="skip",
                             marker=dict(colorscale=scale, cmin=lo, cmax=hi, color=[lo], showscale=True,
                                         colorbar=dict(title=t["ma_m_abs"] if col == "meldungen" else t["per_100k"],
                                                       thickness=12, len=0.6))))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1.64)   # 1 / cos(52.5°): no distortion in Berlin
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), hovermode="closest")
    return fig


def surroundings(lang, k, bez):
    """Section in the districts tab: reports per resident next to the population (nationality, migration
    background) and the household income of each district. Only shares per district, no data about persons."""
    t = UI[lang]
    her, ein, erw = read_csv("bezirke_herkunft.csv"), read_csv("bezirke_einkommen.csv"), read_csv("bezirke_erwerb.csv")
    tests = {"her": read_csv("herkunft_test.csv"), "ein": read_csv("einkommen_test.csv"), "erw": read_csv("erwerb_test.csv")}
    views = [v for v, d in [("her", her), ("ein", ein), ("erw", erw)] if d is not None]
    if not views:
        return
    st.markdown(f"#### {t['su_head']}")
    st.info(t["su_warn"])
    view = control("radio", st, t["su_choose"], "su_view", lang, views, views[0], horizontal=True,
                   format_func=lambda v: t["su_" + v])
    min_label = 8                                                    # smallest share that gets a number in the bar
    if view == "her":
        data, groups = her, [("deutsche_ohne_mh_pct", t["su_g_ohne"], "#c3c2b7", "#3d3c39"),
                             ("deutsche_mit_mh_pct", t["su_g_mit"], "#86b6ef", "#0d366b"),
                             ("auslaender_pct", t["su_g_ausl"], "#2a5c9e", "white")]
        right_title, test_rows = t["su_her_right"], [("mit_mh", t["su_t_mh"]), ("auslaender", t["su_g_ausl"])]
    elif view == "erw":
        data, min_label = erw, 4
        groups = [("erwerbstaetige", t["su_e1"], "#2a5c9e", "white"), ("erwerbslose", t["su_e2"], "#f0a33a", "#3d3c39"),
                  ("nichterwerbspersonen", t["su_e3"], "#c3c2b7", "#3d3c39")]
        right_title = t["su_erw_right"].format(year=k.get("mikrozensus_jahr", ""))
        test_rows = [("erwerbslosenquote", t["su_e_quote"]), ("erwerbstaetige", t["su_e1"])]
    else:
        data = ein.rename(columns={"unter_1500": "s1", "1500_2000": "s2", "2000_3000": "s3", "3000_4000": "s4", "ab_4000": "s5"})
        groups = [("s1", t["su_s1"], "#0d366b", "white"), ("s2", t["su_s2"], "#2a5c9e", "white"),
                  ("s3", t["su_s3"], "#86b6ef", "#0d366b"), ("s4", t["su_s4"], "#c9ddf5", "#0d366b"),
                  ("s5", t["su_s5"], "#e6e5df", "#3d3c39")]
        right_title = t["su_ein_right"].format(year=k.get("mikrozensus_jahr", ""))
        test_rows = [("unter_1500", t["su_s1"]), ("ab_4000", t["su_s5"])]
    data = bez[["bezirk", "je_100000"]].merge(data, on="bezirk").sort_values("je_100000")

    fig = make_subplots(rows=1, cols=2, shared_yaxes=True, column_widths=[0.38, 0.62], horizontal_spacing=0.03,
                        subplot_titles=[t["su_left"], right_title])
    fig.add_trace(go.Bar(y=data["bezirk"], x=data["je_100000"], orientation="h", marker_color=COLOR_MEDIA, showlegend=False,
                         text=[num(v, lang, 1) for v in data["je_100000"]], textposition="inside",
                         insidetextanchor="end", textfont=dict(color="white"),
                         hovertemplate="%{y}: %{x:.1f}<extra></extra>"), row=1, col=1)
    for col, name, color, font in groups:
        fig.add_trace(go.Bar(y=data["bezirk"], x=data[col], orientation="h", name=name, marker_color=color,
                             text=[f"{num(v, lang)} %" if v >= min_label else "" for v in data[col]], textposition="inside",
                             insidetextanchor="middle", textfont=dict(color=font, size=11),
                             hovertemplate="%{y} · " + name + ": %{x:.1f} %<extra></extra>"), row=1, col=2)
    fig.update_layout(barmode="stack", margin=dict(t=40), legend_traceorder="normal")   # legend in bar order
    fig.update_xaxes(title=t["per_100k"], gridcolor=GRID, row=1, col=1)
    fig.update_xaxes(title=t["su_share"], range=[0, 100], gridcolor=GRID, row=1, col=2)
    for ann, dom in zip(fig.layout.annotations, [fig.layout.xaxis.domain, fig.layout.xaxis2.domain]):
        ann.update(x=dom[0], xanchor="left", font=dict(size=13))          # panel titles left-aligned
    show(fig, lang, 460)

    test = tests[view]
    if test is not None:
        top2 = " und ".join(k.get("ohne_top2", [])) if lang == "de" else " and ".join(k.get("ohne_top2", []))
        rows = []
        for key, label in test_rows:
            a = test[(test["anteil"] == key) & (test["bezirke"] == "alle")].iloc[0]
            o = test[(test["anteil"] == key) & (test["bezirke"] == "ohne_top2")].iloc[0]
            rows.append({t["su_t_share"]: label,
                         t["su_t_all"]: f"{num(a['spearman'], lang, 2)} (p {num(a['p'], lang, 2)})",
                         t["su_t_wo"].format(top2=top2): f"{num(o['spearman'], lang, 2)} (p {num(o['p'], lang, 2)})"})
        st.markdown(f"**{t['su_t_head']}**")
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    if view == "her":
        note(t["su_her_note"], t["su_mh_def"], t["su_t_note"], t["src_police"], t["period_note"])
    elif view == "erw":
        calc = [b for b, a in zip(erw["bezirk"], erw["angabe_erwerbslose"]) if a == "berechnet"]
        limited = int((erw["angabe_erwerbslose"] == "eingeschraenkt").sum())
        note(t["su_erw_note"].format(year=k.get("mikrozensus_jahr", "")),
             t["su_erw_unsure"].format(n=limited, calc=(" und " if lang == "de" else " and ").join(calc)),
             t["su_erw_def"], t["su_t_note"], t["src_police"], t["period_note"])
    else:
        note(t["su_ein_note"].format(year=k.get("mikrozensus_jahr", "")), t["su_ein_def"], t["su_t_note"],
             t["src_police"], t["period_note"])


def tab_map(lang, k):
    t = UI[lang]
    st.markdown(t["ma_q"])
    geo, bez, pts = load("bezirke.geojson", lang), load("bezirke.csv", lang), load("orte_karte.csv", lang)
    if geo is None or bez is None or pts is None:
        return
    berlin = k["meldungen_mit_bezirk"] / k["einwohner_berlin"] * 100_000

    metric = control("radio", st, t["ma_metric"], "ma_metric", lang, ["abs", "rel"], "rel", horizontal=True,
                     format_func=lambda v: t["ma_m_abs"] if v == "abs" else t["ma_m_rel"])
    col = "meldungen" if metric == "abs" else "je_100000"
    st.caption(t["ma_metric_help"])
    st.markdown(f"#### {t['ma_map'].format(metric=t['ma_m_abs'] if metric == 'abs' else t['ma_m_rel'])}")
    fig = district_map(geo, bez, pts, col, lang)
    show(fig, lang, 620, legend_top=False)
    note(t["ma_map_note"], t["term_kbo"], t["src_police"], t["period_note"])

    st.markdown(f"#### {t['ma_rel']}")
    data = bez.sort_values("je_100000")
    fig = go.Figure(go.Bar(y=data["bezirk"], x=data["je_100000"], orientation="h", marker_color=COLOR_MEDIA,
                           text=[f"{num(v, lang, 1)}  ({n} {word(t['reports'], lang)})" for v, n in zip(data["je_100000"], data["meldungen"])],
                           textposition="inside", insidetextanchor="end", textfont=dict(color="white"),
                           hovertemplate="%{x:.1f}<extra></extra>"))           # text inside: the line never crosses it
    fig.add_vline(x=berlin, line=dict(color=GREY, dash="dash", width=1), layer="below")
    fig.add_annotation(x=berlin, y=1, yref="paper", yanchor="bottom", text=f"Berlin: {num(berlin, lang, 1)}",
                       showarrow=False, font=dict(size=11, color=GREY))
    fig.update_layout(margin=dict(t=40))
    fig.update_xaxes(title=t["per_100k"], range=[0, data["je_100000"].max() * 1.05], gridcolor=GRID)
    show(fig, lang, 460, legend_top=False)
    note(t["ma_rel_note"].format(date=date_label(k["einwohner_stichtag"], lang), b=num(berlin, lang, 1)),
         t["src_police"], t["period_note"])

    surroundings(lang, k, bez)

    bk = read_csv("bezirk_kategorie.csv")
    if bk is not None:
        st.markdown(f"#### {t['ma_heat']}")
        wide = bk.pivot_table(index="bezirk", columns="kategorie", values="meldungen", aggfunc="sum").fillna(0)
        pct = wide.div(wide.sum(axis=1), axis=0) * 100
        cols = category_order(list(pct.columns))
        pct = pct.loc[bez.sort_values("meldungen", ascending=False)["bezirk"], cols]
        fig = go.Figure(go.Heatmap(z=pct.values, x=[cat(c, lang) for c in cols], y=list(pct.index),
                                   colorscale=[[0, "#f4f8fd"], [0.5, "#86b6ef"], [1, "#0d366b"]],
                                   text=[[num(v, lang) for v in row] for row in pct.values], texttemplate="%{text}",
                                   hovertemplate="%{y} · %{x}: %{z:.1f} %<extra></extra>",
                                   colorbar=dict(title="%", thickness=12)))
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(tickangle=-35)
        show(fig, lang, 560, legend_top=False)
        note(t["ma_heat_note"], t["term_cat"], t["src_police"], t["period_note"])

    kbo = read_csv("kbo_vergleich.csv")
    if kbo is not None:
        st.markdown(f"#### {t['ma_kbo']}")
        data = kbo.sort_values("polizei")
        fig = go.Figure()
        for c, name, color in [("polizei", t["police"], COLOR_POLICE), ("medien", t["media"], COLOR_MEDIA)]:
            fig.add_trace(go.Bar(y=data["kbo"], x=data[c], name=name, orientation="h", marker_color=color,
                                 text=[v if v > 0 else "" for v in data[c]],          # no lonely "0" without a bar
                                 textposition="outside", cliponaxis=False))
        fig.update_layout(barmode="group", hovermode="y unified")
        fig.update_xaxes(title=f"{t['reports']} / {t['articles']}", gridcolor=GRID,
                         range=[0, max(data["polizei"].max(), data["medien"].max()) * 1.15])
        show(fig, lang, 420)
        note(t["ma_kbo_note"], t["term_kbo"], t["src_both"], t["period_note"])


# ----------------------------------------------------------------------------------------------------------------
# tab: media
# ----------------------------------------------------------------------------------------------------------------
def tab_media(lang, k):
    t = UI[lang]
    st.markdown(t["me_q"])
    mm = load("medien_monat.csv", lang)
    if mm is None:
        return
    st.markdown(f"#### {t['me_month']} ({num(k['artikel_auswahl'], lang)} {word(t['articles'], lang)})")
    show(stacked_months(mm, "artikel", lang, t["articles"], category_order(mm["kategorie"].unique())), lang, 430)
    note(t["me_month_note"], t["term_cat"], event_legend(lang), t["src_media"], t["period_note"])

    tag = read_csv("tag.csv")
    if tag is not None:
        st.markdown(f"#### {t['me_day']}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tag["datum"], y=tag["medien"], name=t["per_day"], mode="lines",
                                 line=dict(color="#a9c8ee", width=1)))
        fig.add_trace(go.Scatter(x=tag["datum"], y=tag["medien"].rolling(7, center=True).mean(), name=t["avg7"],
                                 mode="lines", line=dict(color=COLOR_MEDIA, width=2.5), hovertemplate="%{y:.1f}"))
        event_lines(fig, lang)
        fig.update_layout(hovermode="x unified", margin=dict(t=60))
        fig.update_xaxes(tickformat="%d.%m." if lang == "de" else "%d %b", dtick="M1")
        fig.update_yaxes(title=t["articles"], rangemode="tozero", gridcolor=GRID)
        show(fig, lang, 380)
        note(t["me_day_note"], t["src_media"], t["period_note"])

    c1, c2 = st.columns(2)
    q = read_csv("quellen.csv")
    if q is not None:
        with c1:
            st.markdown(f"#### {t['me_sources']}")
            data = q.head(15).iloc[::-1]
            fig = go.Figure(go.Bar(y=data["quelle"], x=data["artikel"], orientation="h", marker_color=COLOR_MEDIA,
                                   text=[f"{num(a, lang)} ({num(s, lang)} %)" for a, s in zip(data["artikel"], data["anteil_pct"])],
                                   textposition="outside", cliponaxis=False))
            fig.update_xaxes(title=t["articles"], range=[0, data["artikel"].max() * 1.35], gridcolor=GRID)
            show(fig, lang, 520, legend_top=False)
            note(t["me_sources_note"].format(u=num(k["titel_verschieden"], lang), n=num(k["artikel_auswahl"], lang)),
                 t["src_media"], t["period_note"])
    mo = read_csv("medien_orte.csv")
    if mo is not None:
        with c2:
            st.markdown(f"#### {t['me_places']}")
            kind = control("radio", st, t["me_places_kind"], "me_kind", lang, ["Ort", "Bezirk"], "Ort", horizontal=True,
                           format_func=lambda v: t["kind_place"] if v == "Ort" else t["kind_district"])
            data = (mo[mo["art"] == "Bezirk"] if kind == "Bezirk" else mo[mo["art"] != "Bezirk"]).head(15).iloc[::-1]
            fig = go.Figure(go.Bar(y=data["ort"], x=data["artikel"], orientation="h", text=data["artikel"],
                                   textposition="outside", cliponaxis=False,
                                   marker_color=[COLOR_KBO if a == "kbO" else COLOR_MEDIA for a in data["art"]]))
            fig.update_xaxes(title=t["articles"], range=[0, data["artikel"].max() * 1.2], gridcolor=GRID)
            show(fig, lang, 470, legend_top=False)
            note(t["me_places_note"], t["term_kbo"], t["src_media"], t["period_note"])


# ----------------------------------------------------------------------------------------------------------------
# tab: comparison
# ----------------------------------------------------------------------------------------------------------------
def tab_compare(lang, k):
    t = UI[lang]
    st.markdown(t["co_q"])
    kv = load("kategorien_vergleich.csv", lang)
    if kv is not None:
        st.markdown(f"#### {t['co_cat']}")
        data = kv.sort_values("polizei_titel_pct")
        fig = go.Figure()
        for c, name, color in [("polizei_titel_pct", t["police"], COLOR_POLICE), ("medien_titel_pct", t["media"], COLOR_MEDIA)]:
            fig.add_trace(go.Bar(y=[cat(x, lang) for x in data["kategorie"]], x=data[c], name=name, orientation="h",
                                 marker_color=color, text=[num(v, lang, 1) for v in data[c]], textposition="outside",
                                 cliponaxis=False, hovertemplate="%{x:.1f} %"))
        fig.update_layout(barmode="group", hovermode="y unified")
        fig.update_xaxes(title=t["share_pct"], gridcolor=GRID,
                         range=[0, max(data["polizei_titel_pct"].max(), data["medien_titel_pct"].max()) * 1.15])
        show(fig, lang, 620)
        pol = kv.loc[kv["kategorie"] == "Politisch motiviert", "polizei_endgueltig_pct"]
        note(t["co_cat_note"].format(p=num(pol.iloc[0], lang, 1) if len(pol) else "-"), t["term_cat"],
             t["src_both"], t["period_note"] + f" n = {num(k['meldungen'], lang)} / {num(k['artikel_auswahl'], lang)}.")

    tv = read_csv("themen_vergleich.csv")
    if tv is not None:
        st.markdown(f"#### {t['co_topics']}")
        data = tv.dropna(subset=["faktor"]).sort_values("faktor")
        names = [topic(x, lang) for x in data["thema"]]
        fig = go.Figure(go.Bar(
            y=names, x=data["faktor"], orientation="h",
            marker_color=[COLOR_MEDIA if v >= 1 else "#a3a29b" for v in data["faktor"]],
            hovertemplate="%{x:.2f}<extra></extra>", showlegend=False))
        # Beschriftung rechts von Balken bzw. Linie bei 1, damit kein Text auf der Linie liegt
        pad = data["faktor"].max() * 0.02
        fig.add_trace(go.Scatter(
            y=names, x=[max(v, 1) + pad for v in data["faktor"]], mode="text", textposition="middle right",
            text=[f"{num(f, lang, 2)}  ({p} / {m})" for f, p, m in zip(data["faktor"], data["polizei"], data["medien"])],
            textfont=dict(size=12), hoverinfo="skip", showlegend=False, cliponaxis=False))
        fig.add_vline(x=1, line=dict(color=GREY, width=1), layer="below")
        fig.update_xaxes(title=t["co_factor"], range=[0, data["faktor"].max() * 1.3], gridcolor=GRID)
        show(fig, lang, 520, legend_top=False)
        note(t["co_topics_note"], t["co_brackets"], t["src_both"], t["period_note"])

    ev = read_csv("ereignisse.csv")
    if ev is not None:
        st.markdown(f"#### {t['co_events']}")
        table = pd.DataFrame({
            t["ev_event"]: [EVENTS.get(e, {}).get(lang, e) for e in ev["ereignis"]],
            t["ev_date"]: [date_label(d, lang) for d in ev["datum"]],
            t["ev_police"]: ev["polizei"], t["ev_media"]: ev["medien"],
            t["ev_titles"]: ev["titel_verschieden"], t["ev_next"]: ev["medien_tag_danach"]})
        st.dataframe(table, hide_index=True, width="stretch")
        note(t["co_events_note"], t["src_both"])

    ov = read_csv("orte_vergleich.csv")
    if ov is not None:
        st.markdown(f"#### {t['co_places']}")
        data = ov.iloc[::-1]
        fig = go.Figure()
        for c, name, color in [("polizei_pct", t["police"], COLOR_POLICE), ("medien_pct", t["media"], COLOR_MEDIA)]:
            fig.add_trace(go.Bar(y=data["ort"], x=data[c], name=name, orientation="h", marker_color=color,
                                 hovertemplate="%{x:.1f} %"))
        fig.update_layout(barmode="group", hovermode="y unified")
        fig.update_xaxes(title=t["share_pct"], gridcolor=GRID)
        show(fig, lang, 640)
        note(t["co_places_note"], t["src_both"], t["period_note"])


# ----------------------------------------------------------------------------------------------------------------
# tab: violence and police
# ----------------------------------------------------------------------------------------------------------------
def tab_force(lang, k):
    t = UI[lang]
    st.markdown(t["fo_q"])
    st.info(t["fo_warn"])
    tm = load("themen_monat.csv", lang)
    if tm is None:
        return
    st.markdown(t["fo_facts"].format(s=k["schuss_polizei"], t=k["schuss_toedlich"], w=k["waffe_polizei"],
                                     g=k["waffe_mit_gewalt_gegen_polizei"]))
    chosen = control("radio", st, t["topic"], "fo_topic", lang, POLICE_TOPICS, POLICE_TOPICS[1], horizontal=True,
                     format_func=lambda x: topic(x, lang))
    part = tm[tm["thema"] == chosen]
    months = sorted(part["monat"].unique())
    st.markdown(f"#### {t['fo_chart'].format(topic=topic(chosen, lang))}")
    fig = go.Figure()
    for q, name, color in [("polizei", t["fo_police_line"], COLOR_POLICE), ("medien", t["fo_media_line"], COLOR_MEDIA)]:
        s = part[part["quelle"] == q].set_index("monat")["anzahl"].reindex(months, fill_value=0)
        fig.add_trace(go.Scatter(x=[month_label(m, lang) for m in months], y=s.values, name=f"{name}: {int(s.sum())}",
                                 mode="lines+markers", line=dict(color=color, width=3), marker=dict(size=7)))
    shade_event_months(fig, months, lang)
    fig.update_layout(hovermode="x unified")
    fig.update_yaxes(title=f"{t['reports']} / {t['articles']} {t['per_month']}", rangemode="tozero", gridcolor=GRID)
    show(fig, lang, 420)
    note(f"**{topic(chosen, lang)}:** {t['fo_def'][chosen]}", event_legend(lang), t["src_both"], t["period_note"])

    sp = read_csv("schusswaffe_polizei.csv")
    if sp is not None:
        st.markdown(f"#### {t['fo_shots']}")
        table = pd.DataFrame({t["fo_nr"]: sp["nr"], t["fo_date"]: [date_label(d, lang) for d in sp["datum"]],
                              t["district"]: sp["bezirk"].fillna(t["no_district"]),
                              t["fo_fatal"]: [t["yes"] if v == "ja" else t["no"] for v in sp["toedlich"]]})
        st.dataframe(table, hide_index=True, width="stretch")
        note(t["fo_shots_note"], t["src_police"], t["period_note"])


# ----------------------------------------------------------------------------------------------------------------
# page
# ----------------------------------------------------------------------------------------------------------------
def inject_style():
    st.markdown("""<style>
.block-container {padding-top: 3.5rem; max-width: 1250px;}
h1 {font-size: 2rem !important;}
[data-testid="stMetricValue"] {font-size: 1.7rem;}
</style>""", unsafe_allow_html=True)


def main():
    if "lang" not in st.session_state:                       # first visit: language from the link (?lang=en) or German
        initial = st.query_params.get("lang", "de")
        st.session_state["lang"] = initial if initial in LANGS else "de"
    head, switch = st.columns([3, 1])
    with switch:
        lang = st.radio("Language", list(LANGS), horizontal=True, format_func=LANGS.get,
                        label_visibility="collapsed", key="lang")
    st.query_params["lang"] = lang
    inject_style()
    t = UI[lang]
    with head:
        st.title(t["title"])
    st.markdown(t["subtitle"])

    k = load("kennzahlen.json", lang)
    if k is None:
        return
    for col, (label, value) in zip(st.columns(4), [
            (t["kpi_reports"], num(k["meldungen"], lang)), (t["kpi_articles"], num(k["artikel_auswahl"], lang)),
            (t["kpi_sources"], num(k["quellen_auswahl"], lang)), (t["kpi_period"], t["kpi_period_value"])]):
        col.metric(label, value)

    tabs = st.tabs([t["tab_overview"], t["tab_police"], t["tab_map"], t["tab_media"], t["tab_compare"],
                    t["tab_force"], t["tab_about"]])
    with tabs[0]:
        tab_overview(lang, k)
    with tabs[1]:
        tab_police(lang, k)
    with tabs[2]:
        tab_map(lang, k)
    with tabs[3]:
        tab_media(lang, k)
    with tabs[4]:
        tab_compare(lang, k)
    with tabs[5]:
        tab_force(lang, k)
    with tabs[6]:
        st.markdown(t["about"].format(reports=num(k["meldungen"], lang), coverage=num(k["abdeckung_gesamt"], lang, 1),
                                      all_articles=num(k["artikel_gesamt"], lang),
                                      articles=num(k["artikel_auswahl"], lang), model=k["modell"]))


main()
