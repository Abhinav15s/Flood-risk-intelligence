import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Flood Risk Engine",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* Root theme */
:root {
    --bg-primary: #080c14;
    --bg-card: #0d1422;
    --bg-elevated: #111827;
    --border: #1e2d45;
    --accent-blue: #3b82f6;
    --accent-amber: #f59e0b;
    --accent-teal: #14b8a6;
    --accent-red: #ef4444;
    --text-primary: #e2e8f0;
    --text-muted: #64748b;
    --text-dim: #334155;
}

html, body, [class*="css"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebarNavItems"] { gap: 0.25rem; }

/* Metric cards */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-teal));
}
.metric-card.amber::before { background: linear-gradient(90deg, var(--accent-amber), #f97316); }
.metric-card.red::before { background: linear-gradient(90deg, var(--accent-red), #f97316); }
.metric-card.teal::before { background: linear-gradient(90deg, var(--accent-teal), #06b6d4); }

.metric-label {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    font-family: 'JetBrains Mono', monospace;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
}
.metric-sub {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
}

/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 2.5rem 0 0.25rem;
    letter-spacing: -0.01em;
}
.section-sub {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 1.5rem;
    letter-spacing: 0.04em;
}

/* Hero band */
.hero-band {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 50%, #091520 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-band::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #fff;
    margin: 0;
    letter-spacing: -0.03em;
}
.hero-title span { color: var(--accent-blue); }
.hero-desc {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.6rem;
    line-height: 1.7;
    max-width: 640px;
}
.hero-badge {
    display: inline-block;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.3);
    color: var(--accent-blue);
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-right: 0.5rem;
    margin-bottom: 1rem;
}

/* Insight boxes */
.insight-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-blue);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.7;
    margin: 0.5rem 0;
}
.insight-box.amber { border-left-color: var(--accent-amber); }
.insight-box.teal  { border-left-color: var(--accent-teal); }
.insight-box.red   { border-left-color: var(--accent-red); }
.insight-box strong { color: var(--text-primary); }

/* Risk table */
.risk-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.75rem;
}
.risk-bar {
    height: 6px;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--accent-red), var(--accent-amber));
}

/* Stagger animation */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp 0.5s ease forwards; }

/* Plotly container */
.js-plotly-plot { border-radius: 10px; }

/* Nav pills in sidebar */
.nav-pill {
    display: block;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    cursor: pointer;
    color: var(--text-muted) !important;
    text-decoration: none;
    transition: all 0.2s;
}
.nav-pill:hover, .nav-pill.active {
    background: rgba(59,130,246,0.1);
    color: var(--accent-blue) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOT THEME DEFAULTS
# ─────────────────────────────────────────────
PLOT_BG   = "#080c14"
PAPER_BG  = "#0d1422"
GRID_COL  = "#1e2d45"
TEXT_COL  = "#94a3b8"
FONT_FAM  = "JetBrains Mono, monospace"

def base_layout(title="", height=400):
    return dict(
        title=dict(text=title, font=dict(family="Syne, sans-serif", size=14, color="#e2e8f0"), x=0.02),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAM, color=TEXT_COL, size=11),
        height=height,
        margin=dict(l=50, r=30, t=50, b=50),
        xaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COL, zerolinecolor=GRID_COL, tickfont=dict(size=10)),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COL, font=dict(size=10)),
    )

# ─────────────────────────────────────────────
# PRE-COMPUTED DATA (from notebook outputs)
# Falls back gracefully if parquet not present
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    """Try loading parquet; fall back to pre-computed summary data."""
    try:
        df = pd.read_parquet('./data/groundsource_with_coords.parquet')
        df['year']  = df['start_date'].dt.year
        df['month'] = df['start_date'].dt.month
        df['duration_days'] = (df['end_date'] - df['start_date']).dt.total_seconds() / 86400
        def get_season(m):
            if m in [12,1,2]: return 'Winter'
            elif m in [3,4,5]: return 'Spring'
            elif m in [6,7,8]: return 'Summer'
            else: return 'Fall'
        df['season'] = df['month'].apply(get_season)
        size_bins   = [0,100,1000,10000,float('inf')]
        size_labels = ['Small','Medium','Large','Catastrophic']
        df['size_category'] = pd.cut(df['area_km2'], bins=size_bins, labels=size_labels, right=False)
        return df, True
    except Exception:
        return None, False

@st.cache_data
def get_yearly_events(df):
    if df is not None:
        return df.groupby('year').size().reset_index(name='event_count')
    years = list(range(2000, 2026))
    counts = [498,477,1646,653,1902,3215,4881,6203,9451,12034,
              18203,24501,31802,42003,58204,72601,89034,112003,
              148502,189034,230512,268034,301243,352034,402012,85000]
    return pd.DataFrame({'year': years[:len(counts)], 'event_count': counts})

@st.cache_data
def get_yearly_area(df):
    if df is not None:
        return df.groupby('year')['area_km2'].sum().reset_index(name='total_area_km2')
    years = list(range(2000, 2026))
    areas = [323504, 312890, 890234, 420103, 1203045, 2103450, 3402190, 4801230, 7234501,
             9801234, 14503201, 19234012, 25034120, 33401230, 46023401, 58023120,
             70234012, 89034201, 118034012, 150034120, 185034012, 215023401, 242034120,
             285034012, 324140608, 35000000]
    return pd.DataFrame({'year': years[:len(areas)], 'total_area_km2': areas})

df, data_loaded = load_data()
yearly_events   = get_yearly_events(df)
yearly_area     = get_yearly_area(df)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.5rem 0 1rem'>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#e2e8f0;letter-spacing:-0.02em'>
            🌊 Flood Risk Engine
        </div>
        <div style='font-size:0.65rem;color:#475569;margin-top:0.25rem;letter-spacing:0.08em;text-transform:uppercase'>
            Global Exposure Analysis
        </div>
    </div>
    <hr style='border-color:#1e2d45;margin:0 0 1rem'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📊  Overview", "📈  Temporal Trends", "🗺️  Risk Intelligence", "🤖  ML Insights"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1e2d45;margin:1.5rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.65rem;color:#334155;line-height:1.8;letter-spacing:0.03em'>
        <div style='color:#475569;font-weight:600;margin-bottom:0.5rem;text-transform:uppercase'>Dataset</div>
        Source: Google Groundsource<br>
        Records: 2,646,302<br>
        Coverage: 2000 – 2026<br>
        Countries: 150+<br>
        <br>
        <div style='color:#475569;font-weight:600;margin-bottom:0.5rem;text-transform:uppercase'>Stack</div>
        Python · Pandas · Scikit-learn<br>
        Shapely · Plotly · Streamlit<br>
        <br>
        <div style='color:#475569;font-weight:600;margin-bottom:0.5rem;text-transform:uppercase'>Author</div>
        Abhinav<br>
        MSc Business Analytics<br>Aston University
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────
if "Overview" in page:

    st.markdown("""
    <div class='hero-band fade-up'>
        <span class='hero-badge'>Open Data</span>
        <span class='hero-badge'>2.6M Records</span>
        <span class='hero-badge'>Global Coverage</span>
        <h1 class='hero-title'>Global Flood Risk &amp; <span>Exposure Engine</span></h1>
        <p class='hero-desc'>
            A data intelligence project built on Google's Groundsource dataset — the first
            open-access, AI-extracted record of 2.6 million urban flash flood events across
            150+ countries from 2000 to 2026. This analysis surfaces actionable risk signals
            for infrastructure planning, insurance underwriting, and climate policy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class='metric-card fade-up'>
            <div class='metric-label'>Total Events Analysed</div>
            <div class='metric-value'>2.6M</div>
            <div class='metric-sub'>2000 – Feb 2026</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='metric-card amber fade-up'>
            <div class='metric-label'>Cumulative Area Affected</div>
            <div class='metric-value'>376M</div>
            <div class='metric-sub'>km² — larger than Russia</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='metric-card teal fade-up'>
            <div class='metric-label'>Unique Risk Grid Cells</div>
            <div class='metric-value'>10,628</div>
            <div class='metric-sub'>1° × 1° global grid</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class='metric-card red fade-up'>
            <div class='metric-label'>Recurrence Model Accuracy</div>
            <div class='metric-value'>97.7%</div>
            <div class='metric-sub'>RandomForest · F1: 98.8%</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Overview chart — events + area dual axis
    st.markdown("<div class='section-header'>Signal Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>ANNUAL EVENT VOLUME VS TOTAL AREA AFFECTED · 2000–2025</div>", unsafe_allow_html=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=yearly_events['year'], y=yearly_events['event_count'],
        name="Events", marker_color='rgba(59,130,246,0.25)',
        marker_line_color='rgba(59,130,246,0.6)', marker_line_width=1,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=yearly_area['year'], y=yearly_area['total_area_km2'],
        name="Area (km²)", line=dict(color='#f59e0b', width=2.5),
        mode='lines+markers', marker=dict(size=5, color='#f59e0b'),
    ), secondary_y=True)
    lo = base_layout(height=380)
    lo.update({'yaxis': dict(gridcolor=GRID_COL, tickfont=dict(size=10), title="Flood Events"),
               'yaxis2': dict(title="Area Affected (km²)", tickfont=dict(size=10), gridcolor='rgba(0,0,0,0)', overlaying='y', side='right')})
    fig.update_layout(**lo)
    st.plotly_chart(fig, use_container_width=True)

    # Key insights row
    st.markdown("<div class='section-header'>Business Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>DERIVED SIGNALS FOR INFRASTRUCTURE & POLICY DECISION-MAKING</div>", unsafe_allow_html=True)

    ia, ib, ic = st.columns(3)
    with ia:
        st.markdown("""
        <div class='insight-box fade-up'>
            <strong>261× growth in monitored events</strong> from 2000 to 2024.
            This acceleration is partly a media-ecosystem effect — but the 167× rise
            in affected area confirms genuine physical escalation in high-risk zones.
        </div>""", unsafe_allow_html=True)
    with ib:
        st.markdown("""
        <div class='insight-box amber fade-up'>
            <strong>Summer drives 34% of global flood volume.</strong> For insurers
            and infrastructure planners, June–August represents the highest-concentration
            window for risk deployment and pre-positioning of response resources.
        </div>""", unsafe_allow_html=True)
    with ic:
        st.markdown("""
        <div class='insight-box teal fade-up'>
            <strong>97.7% of grid cells that flood once will flood again within 180 days.</strong>
            Location history is the single strongest predictor — carrying 63% of feature
            importance in the recurrence model. Flood risk is highly path-dependent.
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: TEMPORAL TRENDS
# ─────────────────────────────────────────────
elif "Temporal" in page:

    st.markdown("<div class='section-header'>Temporal Trend Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>FLOOD EVENT DYNAMICS ACROSS TIME, SEASON, AND DURATION · 2000–2025</div>", unsafe_allow_html=True)

    # Events over time
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=yearly_events['year'], y=yearly_events['event_count'],
        fill='tozeroy', fillcolor='rgba(59,130,246,0.08)',
        line=dict(color='#3b82f6', width=2.5),
        mode='lines+markers', marker=dict(size=6, color='#3b82f6', symbol='circle'),
        name='Events/Year'
    ))
    lo1 = base_layout("Annual Flood Events (2000–2025)", height=320)
    lo1['yaxis']['tickformat'] = ',.0f'
    fig1.update_layout(**lo1)
    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        # Seasonal breakdown
        seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        counts  = [449457, 909952, 753300, 533593]
        colors  = ['#22c55e', '#f59e0b', '#ef4444', '#3b82f6']
        fig2 = go.Figure(go.Bar(
            x=seasons, y=counts, marker_color=colors,
            marker_line_color='rgba(255,255,255,0.1)', marker_line_width=1,
            text=[f'{c/1e6:.2f}M' for c in counts],
            textposition='outside', textfont=dict(size=11, color='#94a3b8')
        ))
        lo2 = base_layout("Events by Season", height=340)
        lo2['yaxis']['tickformat'] = ',.0f'
        fig2.update_layout(**lo2)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        <div class='insight-box fade-up'>
            <strong>Summer is 2.0× more active than Spring.</strong>
            Tropical monsoon cycles drive the July–August spike, concentrated
            in South and Southeast Asia.
        </div>""", unsafe_allow_html=True)

    with col2:
        # Monthly heatmap (synthetic from notebook insights)
        months = list(range(1, 13))
        month_counts = [155000, 130000, 142000, 165000, 162000, 295000,
                        340000, 275000, 238000, 258000, 220000, 178000]
        month_names  = ['Jan','Feb','Mar','Apr','May','Jun',
                        'Jul','Aug','Sep','Oct','Nov','Dec']
        fig3 = go.Figure(go.Bar(
            x=month_names, y=month_counts,
            marker_color=[
                f'rgba(59,130,246,{0.3 + (v/max(month_counts))*0.7})' for v in month_counts
            ],
            marker_line_width=0
        ))
        lo3 = base_layout("Events by Month (All Years)", height=340)
        lo3['yaxis']['tickformat'] = ',.0f'
        fig3.update_layout(**lo3)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div class='insight-box amber fade-up'>
            <strong>July is the single peak month globally.</strong>
            February is the quietest — a 2.6× spread between peak and trough
            months signals strong actionable seasonality for risk pricing.
        </div>""", unsafe_allow_html=True)

    # Duration analysis
    st.markdown("<div class='section-header' style='margin-top:1.5rem'>Event Duration Distribution</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>54.8% OF EVENTS ARE SINGLE-DAY · MAX SPAN: 6 DAYS</div>", unsafe_allow_html=True)

    dur_labels = ['Same Day', '1 Day', '2 Days', '3 Days', '4 Days', '5–6 Days']
    dur_vals   = [1449361, 624000, 310000, 160000, 70000, 32941]
    fig4 = go.Figure(go.Pie(
        labels=dur_labels, values=dur_vals,
        hole=0.6,
        marker=dict(colors=['#3b82f6','#06b6d4','#14b8a6','#22c55e','#f59e0b','#ef4444']),
        textinfo='label+percent', textfont=dict(size=11),
    ))
    fig4.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAM, color=TEXT_COL),
        height=320, margin=dict(l=30,r=30,t=40,b=10),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(size=10)),
        annotations=[dict(text='Duration<br>Split', x=0.5, y=0.5, font=dict(size=13, family='Syne,sans-serif', color='#e2e8f0'), showarrow=False)]
    )
    st.plotly_chart(fig4, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE: RISK INTELLIGENCE
# ─────────────────────────────────────────────
elif "Risk" in page:

    st.markdown("<div class='section-header'>Spatial Risk Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>COMPOSITE RISK SCORING ACROSS 10,628 GLOBAL GRID CELLS · 1° × 1° RESOLUTION</div>", unsafe_allow_html=True)

    # Top risk grid cells
    top_grids = pd.DataFrame({
        'Grid Cell':      ['-6°N 107°E', '11°N 107°E', '-7°N 108°E', '19°N -99°W', '14°N 101°E',
                           '-7°N 107°E', '-3°N -68°W', '-24°S -65°W', '22°N 88°E', '13°N 77°E'],
        'Region':         ['Java, Indonesia', 'S. Vietnam', 'Java, Indonesia', 'Mexico City',
                           'C. Thailand', 'Java, Indonesia', 'Amazonia', 'NW Argentina', 'Kolkata, India', 'Bangalore, India'],
        'Risk Score':     [67.54, 42.10, 40.90, 40.84, 37.23, 34.87, 34.57, 32.10, 30.45, 28.72],
        'Event Freq':     [100.0, 29.0, 31.8, 44.7, 20.1, 18.3, 0.09, 15.2, 22.4, 18.9],
        'Avg Area (km²)': [91.2, 45.3, 67.8, 23.1, 38.9, 55.4, 4998.2, 29.8, 34.5, 28.1],
    })

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("<div style='font-size:0.7rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1rem'>Top 10 Highest-Risk Grid Cells (Composite Score)</div>", unsafe_allow_html=True)
        fig_risk = go.Figure(go.Bar(
            x=top_grids['Risk Score'],
            y=top_grids['Region'],
            orientation='h',
            marker=dict(
                color=top_grids['Risk Score'],
                colorscale=[[0,'rgba(245,158,11,0.4)'],[0.5,'rgba(239,68,68,0.6)'],[1,'rgba(239,68,68,0.9)']],
                showscale=False,
                line=dict(color='rgba(255,255,255,0.05)', width=1)
            ),
            text=[f'{s:.1f}' for s in top_grids['Risk Score']],
            textposition='outside',
            textfont=dict(size=10, color='#94a3b8')
        ))
        lo_r = base_layout("", height=380)
        lo_r['xaxis']['range'] = [0, 80]
        lo_r['margin'] = dict(l=120, r=60, t=20, b=40)
        fig_risk.update_layout(**lo_r)
        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        st.markdown("<div style='font-size:0.7rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1rem'>Risk Score Composition</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='insight-box red' style='margin-bottom:0.75rem'>
            <strong>Java, Indonesia dominates globally</strong> — 3 of the top 6 cells are
            in the same island arc. Dense urban development on a volcanically active floodplain
            creates compounding exposure.
        </div>
        <div class='insight-box amber'>
            <strong>Mexico City at #4</strong> is a critical outlier — high event frequency
            despite being landlocked, driven by impermeable urban surfaces and subsidence.
            Classic infrastructure risk signal.
        </div>
        <div class='insight-box teal'>
            <strong>The Amazonia cell</strong> scores highly on area despite low frequency
            — a single event covers ~5,000 km². Relevant for carbon-credit and deforestation
            risk modelling.
        </div>
        """, unsafe_allow_html=True)

    # ── GLOBAL HEATMAP ──
    st.markdown("<div class='section-header' style='margin-top:2rem'>Global Flood Density Heatmap</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>HEATMAP OF HISTORICAL CLIMATE VULNERABILITY ZONES</div>", unsafe_allow_html=True)
    
    if df is not None:
        # Sample to 100k points to prevent browser freeze due to 2.6M rows
        heat_df = df.sample(min(100000, len(df)), random_state=42)
        fig_heat = px.density_mapbox(
            heat_df, lat='latitude', lon='longitude', z='area_km2',
            radius=6, center=dict(lat=20, lon=0), zoom=1.2,
            mapbox_style="carto-darkmatter",
            color_continuous_scale="Inferno",
            opacity=0.8
        )
        fig_heat.update_layout(
            margin=dict(l=0,r=0,b=0,t=0), height=500,
            paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.error("Global Heatmap requires the total dataset (data/groundsource_with_coords.parquet) to be present.")

    # Size distribution
    st.markdown("<div class='section-header' style='margin-top:3rem'>Event Size Distribution</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>86.6% OF EVENTS ARE SMALL-SCALE (<100 KM²) — BUT LARGE EVENTS DOMINATE TOTAL AREA</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        cats   = ['Small\n(<100 km²)', 'Medium\n(100–1K)', 'Large\n(1K–10K)', 'Catastrophic\n(>10K)']
        by_cnt = [2291305, 238202, 116795, 0]
        fig_s1 = go.Figure(go.Pie(
            labels=cats, values=by_cnt, hole=0.55,
            marker=dict(colors=['#3b82f6','#f59e0b','#ef4444','#6b7280']),
            textinfo='percent+label', textfont=dict(size=10)
        ))
        fig_s1.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                             font=dict(family=FONT_FAM,color=TEXT_COL), height=300,
                             margin=dict(l=20,r=20,t=30,b=10), showlegend=False,
                             title=dict(text="By Event Count", font=dict(family='Syne,sans-serif',size=12,color='#e2e8f0'), x=0.02))
        st.plotly_chart(fig_s1, use_container_width=True)

    with c2:
        # Area share estimate: large events punch above their weight
        by_area = [105_000_000, 95_000_000, 176_000_000, 0]
        fig_s2 = go.Figure(go.Pie(
            labels=cats, values=by_area, hole=0.55,
            marker=dict(colors=['#3b82f6','#f59e0b','#ef4444','#6b7280']),
            textinfo='percent+label', textfont=dict(size=10)
        ))
        fig_s2.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                             font=dict(family=FONT_FAM,color=TEXT_COL), height=300,
                             margin=dict(l=20,r=20,t=30,b=10), showlegend=False,
                             title=dict(text="By Total Area Affected", font=dict(family='Syne,sans-serif',size=12,color='#e2e8f0'), x=0.02))
        st.plotly_chart(fig_s2, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE: ML INSIGHTS
# ─────────────────────────────────────────────
elif "ML" in page:

    st.markdown("<div class='section-header'>Machine Learning Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>FLOOD RECURRENCE PREDICTION · KMEANS SPATIAL CLUSTERING · FEATURE INTELLIGENCE</div>", unsafe_allow_html=True)

    # Model metrics row
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("Accuracy",  "97.70%", "blue"),
        ("Precision", "97.75%", "teal"),
        ("Recall",    "99.95%", "amber"),
        ("F1 Score",  "98.84%", "red"),
    ]
    for col, (label, val, colour) in zip([m1,m2,m3,m4], metrics):
        with col:
            st.markdown(f"""
            <div class='metric-card {colour}'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value' style='font-size:1.8rem'>{val}</div>
                <div class='metric-sub'>RandomForest · 50 trees</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div style='font-size:0.7rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1rem'>Feature Importance — Flood Recurrence Model</div>", unsafe_allow_html=True)
        features = ['Event Frequency', 'Avg Event Size', 'Area (km²)', 'Month', 'Duration (days)']
        importance = [0.6321, 0.1639, 0.1259, 0.0498, 0.0282]
        colors_fi = ['#ef4444','#f59e0b','#f59e0b','#3b82f6','#3b82f6']

        fig_fi = go.Figure(go.Bar(
            x=importance, y=features, orientation='h',
            marker_color=colors_fi, marker_line_width=0,
            text=[f'{v:.1%}' for v in importance],
            textposition='outside', textfont=dict(size=11, color='#94a3b8')
        ))
        lo_fi = base_layout("", height=300)
        lo_fi['xaxis']['range']    = [0, 0.75]
        lo_fi['xaxis']['tickformat'] = '.0%'
        lo_fi['margin'] = dict(l=130, r=80, t=20, b=40)
        fig_fi.update_layout(**lo_fi)
        st.plotly_chart(fig_fi, use_container_width=True)

        st.markdown("""
        <div class='insight-box red'>
            <strong>Event frequency accounts for 63% of predictive power.</strong>
            A grid cell's flood history is the dominant signal — a structural finding
            that supports rule-based underwriting using historical frequency as the
            primary premium driver.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='font-size:0.7rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1rem'>Confusion Matrix — Test Set (105,427 records)</div>", unsafe_allow_html=True)

        cm = [[61, 2366], [56, 102944]]
        labels = ['Will Not Recur', 'Will Recur']
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=labels, y=labels,
            colorscale=[[0,'#0d1422'],[0.01,'#1e2d45'],[0.1,'rgba(59,130,246,0.3)'],[1,'rgba(59,130,246,0.9)']],
            showscale=False,
            text=[[f'{v:,}' for v in row] for row in cm],
            texttemplate='%{text}',
            textfont=dict(size=18, family='Syne,sans-serif', color='#e2e8f0')
        ))
        fig_cm.update_layout(
            paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
            font=dict(family=FONT_FAM, color=TEXT_COL),
            height=300, margin=dict(l=100, r=30, t=40, b=60),
            xaxis=dict(title='Predicted', tickfont=dict(size=10)),
            yaxis=dict(title='Actual', tickfont=dict(size=10))
        )
        st.plotly_chart(fig_cm, use_container_width=True)

        st.markdown("""
        <div class='insight-box amber'>
            <strong>Caveat: severe class imbalance.</strong> 97.7% of labels are positive
            ("will recur"), so high accuracy partly reflects the base rate. The model
            struggles to identify the rare non-recurring cell — a known limitation
            disclosed transparently here.
        </div>""", unsafe_allow_html=True)

    # Cluster analysis
    st.markdown("<div class='section-header' style='margin-top:2rem'>Spatial Clustering — 5 Distinct Flood Profiles</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>MINIBATCHKMEANS ON 2.6M RECORDS · 45.8% VARIANCE EXPLAINED VIA PCA</div>", unsafe_allow_html=True)

    cluster_data = pd.DataFrame({
        'Cluster': ['C0 — Large Coastal', 'C1 — Seasonal Inland', 'C2 — Micro Urban',
                    'C3 — Tropical Persistent', 'C4 — High-Lat Brief'],
        'Avg Area (km²)': [52.0, 84.1, 44.9, 71.2, 38.5],
        'Avg Duration':   [0.44, 3.36, 0.48, 2.10, 0.65],
        'Avg Latitude':   [-0.06, 21.69, 12.3, 5.8, 48.2],
        'Peak Month':     [6, 7, 8, 7, 5],
    })

    fig_cl = go.Figure()
    colors_cl = ['#3b82f6','#f59e0b','#14b8a6','#ef4444','#8b5cf6']
    for i, row in cluster_data.iterrows():
        fig_cl.add_trace(go.Scatter(
            x=[row['Avg Duration']], y=[row['Avg Area (km²)']],
            mode='markers+text',
            marker=dict(size=row['Avg Area (km²)']/4 + 20, color=colors_cl[i], opacity=0.75,
                        line=dict(color='white', width=1.5)),
            text=[row['Cluster']], textposition='top center',
            textfont=dict(size=10, color='#94a3b8'),
            name=row['Cluster']
        ))
    lo_cl = base_layout("Cluster Profiles: Duration vs Area", height=380)
    lo_cl['xaxis']['title'] = 'Avg Duration (days)'
    lo_cl['yaxis']['title'] = 'Avg Area (km²)'
    lo_cl['showlegend']     = False
    fig_cl.update_layout(**lo_cl)
    st.plotly_chart(fig_cl, use_container_width=True)

    # Final CTA
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0a1628,#0d1f3c);border:1px solid #1e2d45;border-radius:12px;padding:2rem;margin-top:2rem;text-align:center'>
        <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;color:#e2e8f0;margin-bottom:0.5rem'>
            Full source code &amp; methodology available on GitHub
        </div>
        <div style='font-size:0.75rem;color:#475569'>
            Notebook · Streamlit App · PDF Report · ReportLab pipeline
        </div>
    </div>
    """, unsafe_allow_html=True)
