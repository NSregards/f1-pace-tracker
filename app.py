import fastf1
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import math

st.set_page_config(page_title="F1 PACE TRACKER", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Barlow+Condensed:wght@400;500;600;700;800;900&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }
[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebarNav"] { display: none; }

.stApp {
    background-color: #080808;
    font-family: 'JetBrains Mono', monospace;
}
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 100% !important;
}

/* Top bar */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #1e1e1e;
    padding-bottom: 16px;
    margin-bottom: 24px;
}
.top-bar-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 0.12em;
    color: #ffffff;
    text-transform: uppercase;
}
.top-bar-title span { color: #e10600; }
.top-bar-sub {
    font-size: 10px;
    letter-spacing: 0.25em;
    color: #777;
    text-transform: uppercase;
    margin-top: 3px;
}
.red-tag {
    background: #e10600;
    color: #fff;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    padding: 4px 10px;
    text-transform: uppercase;
}

/* Controls row */
.controls-row {
    display: grid;
    grid-template-columns: 1fr 2fr auto;
    gap: 12px;
    align-items: end;
    margin-bottom: 20px;
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    padding: 16px 20px;
}

/* Labels */
.stSelectbox label, .stMultiSelect label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 0.25em !important;
    color: #555555 !important;
    text-transform: uppercase !important;
}

/* Select boxes */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #111111 !important;
    border: 1px solid #252525 !important;
    border-radius: 0px !important;
    color: #e8e8e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within {
    border-color: #e10600 !important;
    box-shadow: none !important;
}

/* Driver tags */
.stMultiSelect span[data-baseweb="tag"] {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 0 !important;
    color: #ffffff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em;
}

/* Button */
.stButton > button {
    background: #e10600 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 0px !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 12px 28px !important;
    width: 100% !important;
    height: 46px !important;
    transition: background 0.1s;
    margin-top: 4px;
}
.stButton > button:hover { background: #c00500 !important; }

/* Section labels */
.section-label {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #777777;
    margin: 20px 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #161616;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::before {
    content: '';
    display: inline-block;
    width: 3px;
    height: 14px;
    background: #e10600;
}

/* Driver cards */
.driver-card {
    background: #0d0d0d;
    border: 1px solid #1a1a1a;
    border-top: 2px solid;
    padding: 16px;
    font-family: 'JetBrains Mono', monospace;
    transition: border-color 0.2s;
}
.driver-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 26px;
    font-weight: 900;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.stat-label {
    font-size: 8px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #666666;
    margin-bottom: 1px;
}
.stat-value {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 10px;
    letter-spacing: 0.04em;
}
.compounds-row {
    font-size: 9px;
    letter-spacing: 0.15em;
    color: #666666;
    margin-top: 8px;
    padding-top: 10px;
    border-top: 1px solid #161616;
    text-transform: uppercase;
}

/* Legend */
.legend-bar {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #888;
    margin-top: 10px;
    padding: 10px 0;
    border-top: 1px solid #161616;
}
.legend-item { display: flex; align-items: center; gap: 6px; }
.ldot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; flex-shrink: 0; }

/* Info box */
.info-box {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-left: 2px solid #e10600;
    padding: 16px 20px;
    font-size: 12px;
    color: #555;
    letter-spacing: 0.05em;
}

hr { border-color: #161616 !important; }
</style>
""", unsafe_allow_html=True)

DRIVER_COLORS = [
    "#00D2FF", "#FF6B35", "#A8FF3E", "#FF3CAC",
    "#FFD700", "#C77DFF", "#00FF9C", "#FF4757",
]

# Official 2025 F1 team colours by driver code
F1_DRIVER_COLORS = {
    # Red Bull
    "VER": "#0600EF", "HAD": "#0600EF",
    # Ferrari
    "LEC": "#DC0000", "HAM": "#DC0000",
    # Mercedes
    "RUS": "#00D2BE", "ANT": "#00D2BE",
    # McLaren
    "NOR": "#FF8700", "PIA": "#FF8700",
    # Aston Martin
    "ALO": "#006F62", "STR": "#006F62",
    # Alpine
    "GAS": "#0090FF", "COL": "#0090FF",
    # Williams
    "ALB": "#005AFF", "SAI": "#005AFF",
    # Haas
    "OCO": "#B40000", "BEA": "#B40000",
    # Audi
    "HUL": "#BB0A30", "BOR": "#BB0A30",
    # Cadillac
    "BOT": "#003A8F", "PER": "#003A8F",
    # Racing Bulls
    "LAW": "#6692FF", "LIN": "#6692FF",
}
TYRE_COLORS = {
    "SOFT": "#FF3333", "MEDIUM": "#FFD700", "HARD": "#FFFFFF",
    "INTER": "#39FF14", "INTERMEDIATE": "#39FF14",
    "WET": "#00BFFF", "UNKNOWN": "#888888",
}
TYRE_SHORT = {
    "SOFT": "S", "MEDIUM": "M", "HARD": "H",
    "INTER": "I", "INTERMEDIATE": "I", "WET": "W", "UNKNOWN": "?",
}

def secs_to_ms(s):
    if pd.isna(s): return "N/A"
    m = int(s // 60)
    sec = s % 60
    return f"{m}:{sec:06.3f}"

def load_race_data(year, event_name):
    fastf1.Cache.enable_cache("f1_cache")
    session = fastf1.get_session(year, event_name, "R")
    session.load(telemetry=False, weather=False, messages=False)
    all_laps = session.laps.copy()
    sc_lap_nums, vsc_lap_nums = set(), set()
    track_status = session.track_status
    if track_status is not None and len(track_status) > 0:
        for _, lap_row in all_laps.iterrows():
            lap_start = lap_row["LapStartTime"]
            lap_end = lap_start + lap_row["LapTime"] if pd.notna(lap_row["LapTime"]) else lap_start
            overlap = track_status[
                (track_status["Time"] >= lap_start) &
                (track_status["Time"] <= lap_end)
            ]
            for status in overlap["Status"].values:
                if status in ["4", "5"]: sc_lap_nums.add(lap_row["LapNumber"])
                elif status in ["6", "7"]: vsc_lap_nums.add(lap_row["LapNumber"])
    laps = all_laps.copy()
    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()
    laps = laps[laps["LapTimeSeconds"] > 60].copy()
    laps["Compound"] = laps["Compound"].str.upper().str.strip().fillna("UNKNOWN")
    laps["IsSC"] = laps["LapNumber"].isin(sc_lap_nums)
    laps["IsVSC"] = laps["LapNumber"].isin(vsc_lap_nums)
    laps["IsNeutralised"] = laps["IsSC"] | laps["IsVSC"]
    laps = laps.sort_values(["Driver", "LapNumber"])
    laps["RollingAvg"] = laps.groupby("Driver")["LapTimeSeconds"].transform(
        lambda x: x.rolling(3, min_periods=1).mean()
    )
    laps["LapTimeDisplay"] = laps["LapTimeSeconds"].apply(secs_to_ms)
    return laps, session, sc_lap_nums, vsc_lap_nums

def get_ranges(lap_set):
    if not lap_set: return []
    sl = sorted(lap_set)
    ranges, start = [], sl[0]
    for i in range(1, len(sl)):
        if sl[i] != sl[i-1] + 1:
            ranges.append((start, sl[i-1]))
            start = sl[i]
    ranges.append((start, sl[-1]))
    return ranges

def add_band(fig, ranges, fill_color, line_color, label, y_min, y_max):
    labeled = False
    for r_start, r_end in ranges:
        fig.add_trace(go.Scatter(
            x=[r_start-0.5, r_end+0.5, r_end+0.5, r_start-0.5, r_start-0.5],
            y=[y_min, y_min, y_max, y_max, y_min],
            fill="toself", fillcolor=fill_color,
            line=dict(color=line_color, width=1),
            mode="lines", showlegend=False, hoverinfo="skip",
        ))
        if not labeled:
            fig.add_annotation(
                x=r_start+0.3, y=y_min+0.3, text=label, showarrow=False,
                font=dict(color=line_color, size=10, family="JetBrains Mono"),
                xanchor="left", yanchor="bottom",
            )
            labeled = True

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
  <div>
    <div class="top-bar-title">F1 <span>PACE</span> TRACKER</div>
    <div class="top-bar-sub">Lap-by-lap tyre performance analysis</div>
  </div>
  <div class="red-tag">Race Analysis</div>
</div>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns([1, 1.5, 3, 1])
with c1:
    year = st.selectbox("SEASON", [2025, 2024, 2023], index=0)
with c2:
    event = st.selectbox("GRAND PRIX", [
        "Australian Grand Prix", "Bahrain Grand Prix", "Saudi Arabian Grand Prix",
        "Japanese Grand Prix", "Chinese Grand Prix", "Miami Grand Prix",
        "Monaco Grand Prix", "Canadian Grand Prix", "Spanish Grand Prix",
        "British Grand Prix", "Hungarian Grand Prix", "Belgian Grand Prix",
        "Dutch Grand Prix", "Italian Grand Prix", "Singapore Grand Prix",
        "United States Grand Prix", "Mexico City Grand Prix", "Sao Paulo Grand Prix",
        "Las Vegas Grand Prix", "Abu Dhabi Grand Prix",
    ], index=0)
with c3:
    if "laps" in st.session_state:
        all_drivers = sorted(st.session_state["laps"]["Driver"].unique().tolist())
        selected_drivers = st.multiselect("DRIVERS", options=all_drivers,
                                          default=all_drivers[:4], max_selections=6)
    else:
        st.markdown('<div style="font-size:9px;letter-spacing:0.2em;color:#333;text-transform:uppercase;margin-bottom:6px;">DRIVERS</div><div style="font-size:11px;color:#333;padding:10px 0;border-bottom:1px solid #1e1e1e;">Load race data first</div>', unsafe_allow_html=True)
        selected_drivers = []
with c4:
    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    load_btn = st.button("LOAD RACE", use_container_width=True)

st.markdown("<div style='height:4px;background:linear-gradient(90deg,#e10600,transparent);margin-bottom:20px;'></div>", unsafe_allow_html=True)

if "laps" not in st.session_state and not load_btn:
    st.markdown('<div class="info-box">Select a season and grand prix above, then click LOAD RACE to begin analysis.</div>', unsafe_allow_html=True)
    st.stop()

if load_btn:
    with st.spinner(""):
        laps, session, sc_laps, vsc_laps = load_race_data(year, event)
        st.session_state.update({
            "laps": laps, "sc_laps": sc_laps,
            "vsc_laps": vsc_laps, "event": event, "year": year
        })
        st.rerun()

if "laps" not in st.session_state:
    st.stop()

laps     = st.session_state["laps"]
sc_laps  = st.session_state["sc_laps"]
vsc_laps = st.session_state["vsc_laps"]
event    = st.session_state["event"]
year     = st.session_state["year"]

if not selected_drivers:
    st.markdown('<div class="info-box">Select drivers above to view pace data.</div>', unsafe_allow_html=True)
    st.stop()

driver_color_map = {d: F1_DRIVER_COLORS.get(d, DRIVER_COLORS[i % len(DRIVER_COLORS)]) for i, d in enumerate(selected_drivers)}

all_times = laps[laps["Driver"].isin(selected_drivers)]["LapTimeSeconds"]
y_min = math.floor(all_times.min()) - 1
y_max = math.ceil(all_times.max()) + 1
spread = y_max - y_min
raw_step = spread / 10
if raw_step <= 2: step = 2
elif raw_step <= 5: step = 5
elif raw_step <= 10: step = 10
else: step = 15

tick_vals   = list(range(math.ceil(y_min/step)*step, math.ceil(y_max)+1, step))
tick_labels = [secs_to_ms(v) for v in tick_vals]
max_lap     = int(laps["LapNumber"].max())
fig = go.Figure()

add_band(fig, get_ranges(sc_laps),  "rgba(255,215,0,0.07)", "rgba(255,215,0,0.5)",  "SC",  y_min, y_max)
add_band(fig, get_ranges(vsc_laps), "rgba(255,140,0,0.07)", "rgba(255,140,0,0.5)",  "VSC", y_min, y_max)

pit_stops = []
for driver in selected_drivers:
    d = laps[laps["Driver"] == driver].copy().sort_values("LapNumber")
    stints = list(d.groupby(["Stint", "Compound"], sort=True))
    for idx, ((sn, compound), sdf) in enumerate(stints):
        if idx > 0:
            cu = str(compound).upper().strip()
            pc = str(stints[idx-1][0][1]).upper().strip()
            pit_stops.append((int(sdf["LapNumber"].iloc[0]) - 0.5, driver,
                              TYRE_SHORT.get(pc,"?"), TYRE_SHORT.get(cu,"?")))

pit_stops.sort(key=lambda p: p[0])
label_y_levels = [0.97, 0.87, 0.77, 0.67]
last_x, level_idx = -999, 0
pit_label_map = {}
for ps in pit_stops:
    x = ps[0]
    if abs(x - last_x) < 4:
        level_idx = (level_idx + 1) % len(label_y_levels)
    else:
        level_idx = 0
    pit_label_map[x] = label_y_levels[level_idx]
    last_x = x

for (x, driver, prev_short, short) in pit_stops:
    dc = driver_color_map.get(driver, "#888")
    fig.add_shape(type="line", x0=x, x1=x, y0=y_min, y1=y_max,
                  line=dict(color=dc, width=1, dash="dot"))
    fig.add_annotation(
        x=x, y=pit_label_map[x], yref="paper",
        text=f"{driver} {prev_short}>{short}",
        showarrow=False,
        font=dict(color=dc, size=9, family="JetBrains Mono"),
        bgcolor="rgba(8,8,8,0.92)",
        bordercolor=dc, borderwidth=1, borderpad=3,
        yanchor="bottom", xanchor="left",
    )

for driver in selected_drivers:
    d = laps[laps["Driver"] == driver].copy().sort_values("LapNumber")
    stints = list(d.groupby(["Stint", "Compound"], sort=True))
    dc = driver_color_map[driver]
    for idx, ((sn, compound), stint_df) in enumerate(stints):
        stint_df    = stint_df.sort_values("LapNumber")
        compound_up = str(compound).upper().strip()
        tyre_col    = TYRE_COLORS.get(compound_up, "#888888")
        normal_df   = stint_df[~stint_df["IsNeutralised"]]
        sc_df       = stint_df[stint_df["IsNeutralised"]]
        if len(normal_df):
            fig.add_trace(go.Scatter(
                x=normal_df["LapNumber"], y=normal_df["LapTimeSeconds"],
                mode="markers",
                marker=dict(color=tyre_col, size=5, opacity=0.45,
                            line=dict(color="#000", width=0.3)),
                showlegend=False, hoverinfo="skip",
            ))
        if len(sc_df):
            fig.add_trace(go.Scatter(
                x=sc_df["LapNumber"], y=sc_df["LapTimeSeconds"],
                mode="markers",
                marker=dict(color="rgba(0,0,0,0)", size=7, symbol="circle-open",
                            line=dict(color=tyre_col, width=1)),
                showlegend=False, hoverinfo="skip",
            ))
        fig.add_trace(go.Scatter(
            x=stint_df["LapNumber"], y=stint_df["RollingAvg"],
            mode="lines",
            name=driver, legendgroup=driver, showlegend=(idx == 0),
            line=dict(color=tyre_col, width=2.5),
            customdata=stint_df[["LapTimeDisplay", "Compound", "TyreLife"]].values,
            hovertemplate=(
                f"<b>{driver}</b><br>"
                "Lap %{x}  |  %{customdata[0]}<br>"
                "%{customdata[1]}  /  Tyre age %{customdata[2]} laps"
                "<extra></extra>"
            )
        ))

fig.update_layout(
    plot_bgcolor="#080808", paper_bgcolor="#080808",
    font=dict(color="#666666", family="JetBrains Mono"),
    title=dict(
        text=f"{event.upper()}  {year}",
        font=dict(size=13, color="#333333", family="JetBrains Mono"),
        x=0, pad=dict(l=0, b=10)
    ),
    xaxis=dict(
        title=dict(text="LAP", font=dict(size=9, color="#333", family="JetBrains Mono")),
        gridcolor="#111111", color="#333333", zeroline=False,
        tickfont=dict(color="#555555", size=11, family="JetBrains Mono"),
        range=[1, max_lap+1], dtick=5,
        linecolor="#1e1e1e", linewidth=1,
        ticklen=4,
    ),
    yaxis=dict(
        title=dict(text="LAP TIME", font=dict(size=9, color="#333", family="JetBrains Mono")),
        gridcolor="#111111", color="#333333",
        range=[y_max, y_min],
        tickvals=tick_vals, ticktext=tick_labels,
        tickfont=dict(color="#aaaaaa", size=11, family="JetBrains Mono"),
        ticklen=4, linecolor="#1e1e1e", linewidth=1,
    ),
    legend=dict(
        bgcolor="rgba(8,8,8,0.95)", bordercolor="#1e1e1e", borderwidth=1,
        font=dict(size=11, color="#cccccc", family="JetBrains Mono"),
        x=1.01, y=1, xanchor="left",
    ),
    hovermode="x unified", height=560,
    margin=dict(l=100, r=160, t=40, b=50),
)

st.plotly_chart(fig, use_container_width=True)

# Legend
legend_html = '<div class="legend-bar">'
legend_html += '<div class="legend-item"><div class="ldot" style="background:rgba(255,215,0,0.6)"></div>SAFETY CAR</div>'
legend_html += '<div class="legend-item"><div class="ldot" style="background:rgba(255,140,0,0.6)"></div>VIRTUAL SC</div>'
legend_html += '<div class="legend-item" style="color:#222">|</div>'
legend_html += '<div class="legend-item"><div class="ldot" style="background:#FF3333"></div>SOFT</div>'
legend_html += '<div class="legend-item"><div class="ldot" style="background:#FFD700"></div>MEDIUM</div>'
legend_html += '<div class="legend-item"><div class="ldot" style="background:#FFFFFF"></div>HARD</div>'
legend_html += '<div class="legend-item"><div class="ldot" style="background:#39FF14"></div>INTER</div>'
legend_html += '<div class="legend-item"><div class="ldot" style="background:#00BFFF"></div>WET</div>'
legend_html += '</div>'
st.markdown(legend_html, unsafe_allow_html=True)

# Driver cards
st.markdown('<div class="section-label">Driver Summary</div>', unsafe_allow_html=True)
cols = st.columns(len(selected_drivers))
for i, driver in enumerate(selected_drivers):
    d_race = laps[(laps["Driver"] == driver) & (~laps["IsNeutralised"]) & (laps["IsAccurate"] == True)]
    if len(d_race) == 0:
        d_race = laps[laps["Driver"] == driver]
    best = d_race["LapTimeSeconds"].min()
    avg  = d_race["LapTimeSeconds"].mean()
    compounds = "  >  ".join(
        laps[laps["Driver"] == driver]
        .drop_duplicates("Stint").sort_values("Stint")["Compound"].tolist()
    )
    dc = driver_color_map[driver]
    with cols[i]:
        st.markdown(f"""
        <div class="driver-card" style="border-top-color:{dc};">
            <div class="driver-name" style="color:{dc};">{driver}</div>
            <div class="stat-label">BEST LAP</div>
            <div class="stat-value">{secs_to_ms(best)}</div>
            <div class="stat-label">AVG PACE</div>
            <div class="stat-value">{secs_to_ms(avg)}</div>
            <div class="compounds-row">{compounds}</div>
        </div>
        """, unsafe_allow_html=True)
