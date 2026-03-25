"""
generate_report.py
Generates a polished PDF portfolio report for the Global Flood Risk & Exposure Engine project.
Run: python generate_report.py
Output: outputs/flood_risk_report.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import os

os.makedirs("outputs", exist_ok=True)
OUTPUT = "outputs/flood_risk_report.pdf"

# ─── COLOUR PALETTE ───────────────────────────────────────────────
C_BG         = colors.HexColor("#080c14")
C_CARD       = colors.HexColor("#0d1422")
C_BORDER     = colors.HexColor("#1e2d45")
C_BLUE       = colors.HexColor("#3b82f6")
C_AMBER      = colors.HexColor("#f59e0b")
C_TEAL       = colors.HexColor("#14b8a6")
C_RED        = colors.HexColor("#ef4444")
C_TEXT       = colors.HexColor("#e2e8f0")
C_MUTED      = colors.HexColor("#64748b")
C_DIM        = colors.HexColor("#334155")
C_WHITE      = colors.white

# ─── PAGE DIMENSIONS ─────────────────────────────────────────────
W, H = A4   # 595.27 x 841.89 pts
MARGIN_L = 2.0 * cm
MARGIN_R = 2.0 * cm
MARGIN_T = 2.2 * cm
MARGIN_B = 2.0 * cm
CONTENT_W = W - MARGIN_L - MARGIN_R

# ─── STYLES ──────────────────────────────────────────────────────
def S(name, **kw):
    base = {
        "fontName": "Helvetica",
        "fontSize": 10,
        "leading": 14,
        "textColor": C_TEXT,
        "spaceAfter": 0,
        "spaceBefore": 0,
    }
    base.update(kw)
    return ParagraphStyle(name, **base)

s_h1       = S("h1",  fontName="Helvetica-Bold", fontSize=22, leading=26,
               textColor=C_WHITE, spaceAfter=6)
s_h2       = S("h2",  fontName="Helvetica-Bold", fontSize=13, leading=17,
               textColor=C_TEXT, spaceBefore=14, spaceAfter=4)
s_h3       = S("h3",  fontName="Helvetica-Bold", fontSize=10, leading=13,
               textColor=C_BLUE, spaceBefore=8, spaceAfter=3)
s_body     = S("body", fontSize=9, leading=14, textColor=C_MUTED, spaceAfter=6)
s_caption  = S("cap",  fontSize=7.5, leading=10, textColor=C_DIM,
               spaceAfter=4, alignment=TA_CENTER)
s_label    = S("lbl",  fontName="Helvetica-Bold", fontSize=7, leading=9,
               textColor=C_MUTED, spaceAfter=2)
s_metric   = S("met",  fontName="Helvetica-Bold", fontSize=20, leading=24,
               textColor=C_WHITE)
s_metric_s = S("mets", fontSize=8, leading=10, textColor=C_MUTED)
s_tag      = S("tag",  fontName="Helvetica-Bold", fontSize=7, leading=9,
               textColor=C_BLUE)
s_insight  = S("ins",  fontSize=8.5, leading=13, textColor=C_MUTED, spaceAfter=4)
s_footer   = S("ft",   fontSize=7, textColor=C_DIM, alignment=TA_CENTER)
s_toc      = S("toc",  fontSize=9, leading=14, textColor=C_MUTED, spaceAfter=3)
s_right    = S("rt",   fontSize=8, textColor=C_DIM, alignment=TA_RIGHT)

# ─── CANVAS BACKGROUNDS ──────────────────────────────────────────
def cover_background(c, doc):
    c.saveState()
    # Full dark background
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Blue accent strip left
    c.setFillColor(C_BLUE)
    c.rect(0, 0, 4, H, fill=1, stroke=0)
    # Subtle grid dots
    c.setFillColor(C_BORDER)
    for x in range(int(MARGIN_L), int(W - MARGIN_R), 22):
        for y in range(int(MARGIN_B), int(H - MARGIN_T), 22):
            c.circle(x, y, 0.7, fill=1, stroke=0)
    # Bottom rule
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.5)
    c.line(MARGIN_L, 2.8*cm, W - MARGIN_R, 2.8*cm)
    c.restoreState()

def page_background(c, doc):
    c.saveState()
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Thin left accent
    c.setFillColor(C_BLUE)
    c.rect(0, 0, 2, H, fill=1, stroke=0)
    # Page number
    c.setFillColor(C_DIM)
    c.setFont("Helvetica", 7)
    c.drawCentredString(W/2, 1.4*cm, f"Global Flood Risk & Exposure Engine  —  Abhinav  —  Page {doc.page}")
    # Top rule
    c.setStrokeColor(C_BORDER)
    c.setLineWidth(0.3)
    c.line(MARGIN_L, H - MARGIN_T + 4, W - MARGIN_R, H - MARGIN_T + 4)
    c.restoreState()

# ─── HELPER FLOWABLES ────────────────────────────────────────────
def rule(color=C_BORDER, w=1):
    return HRFlowable(width="100%", thickness=w, color=color, spaceAfter=6, spaceBefore=6)

def sp(h=6):
    return Spacer(1, h)

def kpi_table(data):
    """data: list of (label, value, sub, accent_hex)"""
    cell_w = CONTENT_W / len(data)

    inner_tables = []
    for label, value, sub, acc in data:
        inner = Table(
            [
                [Paragraph(f'<font color="{acc}"><b>{label}</b></font>', s_label)],
                [Paragraph(value, s_metric)],
                [Paragraph(sub,   s_metric_s)],
            ],
            colWidths=[cell_w - 16],
            style=TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), C_CARD),
                ("TOPPADDING",    (0,0),(-1,-1), 10),
                ("BOTTOMPADDING", (0,0),(-1,-1), 10),
                ("LEFTPADDING",   (0,0),(-1,-1), 12),
                ("RIGHTPADDING",  (0,0),(-1,-1), 8),
                ("LINEABOVE",     (0,0),(-1,0),  2, colors.HexColor(acc)),
            ])
        )
        inner_tables.append(inner)

    t = Table(
        [inner_tables],
        colWidths=[cell_w for _ in data],
        style=TableStyle([
            ("LEFTPADDING",  (0,0),(-1,-1), 4),
            ("RIGHTPADDING", (0,0),(-1,-1), 4),
            ("TOPPADDING",   (0,0),(-1,-1), 0),
            ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ])
    )
    return t

def insight_box(text, accent=C_BLUE):
    t = Table(
        [[Paragraph(text, s_insight)]],
        colWidths=[CONTENT_W - 24],
        style=TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), C_CARD),
            ("LEFTPADDING",  (0,0),(-1,-1), 14),
            ("RIGHTPADDING", (0,0),(-1,-1), 12),
            ("TOPPADDING",   (0,0),(-1,-1), 10),
            ("BOTTOMPADDING",(0,0),(-1,-1), 10),
            ("LINEBEFORE",   (0,0),(-1,-1), 3, accent),
        ])
    )
    return t

def section_badge(text, color=C_BLUE):
    t = Table(
        [[Paragraph(f'<font color="white"><b>{text}</b></font>', s_label)]],
        style=TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), color),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ("TOPPADDING",    (0,0),(-1,-1), 3),
            ("BOTTOMPADDING", (0,0),(-1,-1), 3),
            ("ROUNDEDCORNERS",[4]),
        ])
    )
    return t

def data_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [CONTENT_W / len(headers)] * len(headers)
    data = [[Paragraph(f'<b>{h}</b>', s_label) for h in headers]] + \
           [[Paragraph(str(c), s_body) for c in row] for row in rows]
    style = TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), C_CARD),
        ("BACKGROUND",    (0,1),(-1,-1), C_BG),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [C_BG, colors.HexColor("#0a0f1a")]),
        ("TEXTCOLOR",     (0,0),(-1,-1), C_MUTED),
        ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("LINEBELOW",     (0,0),(-1,0), 0.5, C_BLUE),
        ("LINEBELOW",     (0,1),(-1,-1), 0.3, C_BORDER),
        ("GRID",          (0,0),(-1,-1), 0, colors.transparent),
    ])
    return Table(data, colWidths=col_widths, style=style)

# ─── BUILD STORY ─────────────────────────────────────────────────
story = []

# ══════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════
story.append(sp(90))
story.append(Paragraph("PORTFOLIO PROJECT", S("cvtag", fontName="Helvetica-Bold",
    fontSize=8, textColor=C_BLUE, spaceBefore=0, spaceAfter=6, letterSpacing=2)))
story.append(Paragraph("Global Flood Risk\n& Exposure Engine", S("cvh1",
    fontName="Helvetica-Bold", fontSize=32, leading=36, textColor=C_WHITE, spaceAfter=10)))
story.append(rule(C_BLUE, 1))
story.append(sp(10))
story.append(Paragraph(
    "A data intelligence project analysing 2.6 million urban flash flood events "
    "across 150+ countries using Google's Groundsource open dataset. This work "
    "demonstrates end-to-end capability in geospatial data engineering, machine "
    "learning, and translating raw data into actionable risk intelligence for "
    "infrastructure planning, insurance, and climate policy.",
    S("cvdesc", fontSize=10, leading=16, textColor=C_MUTED, spaceAfter=16)
))
story.append(sp(16))
cover_meta = Table(
    [[
        Paragraph("AUTHOR", s_label),
        Paragraph("DATASET", s_label),
        Paragraph("TOOLS", s_label),
        Paragraph("YEAR", s_label),
    ],[
        Paragraph("Abhinav\nMSc Business Analytics\nAston University", s_body),
        Paragraph("Google Groundsource\n2.6M records · 150+ countries\n2000–2026", s_body),
        Paragraph("Python · Pandas · Scikit-learn\nShapely · Plotly · Streamlit\nReportLab", s_body),
        Paragraph("2025–2026", s_body),
    ]],
    colWidths=[CONTENT_W/4]*4,
    style=TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), C_CARD),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("LINEABOVE",     (0,0),(-1,0),  1, C_BORDER),
        ("LINEBELOW",     (0,-1),(-1,-1),1, C_BORDER),
        ("LINEBEFORE",    (0,0),(0,-1),  1, C_BORDER),
        ("LINEAFTER",     (-1,0),(-1,-1),1, C_BORDER),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, C_BORDER),
    ])
)
story.append(cover_meta)
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# SECTION 1 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════
story.append(section_badge("01 · EXECUTIVE SUMMARY", C_BLUE))
story.append(sp(6))
story.append(Paragraph("Executive Summary", s_h1))
story.append(rule())

story.append(Paragraph(
    "Urban flash floods are among the most destructive and least systematically "
    "monitored natural hazards globally. Physical gauge infrastructure exists for "
    "riverine floods — but urban flash floods, which inundate streets within minutes "
    "of extreme rainfall, have historically lacked a unified global observation record.",
    s_body))
story.append(sp(4))
story.append(Paragraph(
    "This project leverages Google's Groundsource dataset — 2.6 million AI-extracted "
    "flood event records derived from 5 million news articles across 150+ countries — "
    "to build a comprehensive global flood risk intelligence platform. The analysis "
    "spans data engineering, geospatial processing, exploratory analysis, spatial risk "
    "scoring, machine learning, and interactive visualisation.",
    s_body))
story.append(sp(12))

# KPIs
kpis = [
    ("TOTAL EVENTS",       "2.6M",   "2000 – Feb 2026",     "#3b82f6"),
    ("AREA AFFECTED",      "376M km²","Larger than Russia",  "#f59e0b"),
    ("RISK GRID CELLS",    "10,628", "1° × 1° resolution",  "#14b8a6"),
    ("RECURRENCE ACCURACY","97.7%",  "F1 Score: 98.84%",    "#ef4444"),
]
story.append(kpi_table(kpis))
story.append(sp(14))

story.append(Paragraph("Key Findings", s_h2))
story.append(insight_box(
    "<b>261× growth in monitored flood events</b> from 2000 to 2024 — with 2024 being the peak "
    "year at 402,012 recorded events. While the media ecosystem partly explains this trend, "
    "the 167× rise in total affected area confirms physical escalation in high-exposure zones.",
    C_BLUE
))
story.append(sp(6))
story.append(insight_box(
    "<b>Java, Indonesia represents the world's highest compound flood risk.</b> Three of the top "
    "six risk grid cells globally cluster on the same island arc — a convergence of dense urban "
    "development, volcanic topography, and tropical monsoon cycles.",
    C_AMBER
))
story.append(sp(6))
story.append(insight_box(
    "<b>Event frequency is the dominant recurrence predictor (63.2% feature importance).</b> "
    "Once a location has flooded, it will flood again within 180 days in 97.7% of cases — "
    "a finding with direct implications for insurance underwriting and infrastructure investment prioritisation.",
    C_TEAL
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# SECTION 2 — DATA & METHODOLOGY
# ══════════════════════════════════════════════════════
story.append(section_badge("02 · DATA & METHODOLOGY", C_TEAL))
story.append(sp(6))
story.append(Paragraph("Data & Methodology", s_h1))
story.append(rule())

story.append(Paragraph("Source Dataset — Google Groundsource", s_h2))
story.append(Paragraph(
    "Groundsource is a scalable pipeline developed by Google Research that applies the "
    "Gemini large language model to transform unstructured global news into structured "
    "flood event records. Over 5 million news articles from more than 150 countries were "
    "processed, filtered, translated, and spatiotemporally aggregated to produce 2,646,302 "
    "individual flood observations at daily resolution from 2000 to the present.",
    s_body))
story.append(sp(8))

story.append(Paragraph("Raw Schema", s_h3))
schema_rows = [
    ["uuid",       "String",   "Unique identifier per flood record"],
    ["area_km2",   "Float32",  "Flooded area in square kilometres"],
    ["geometry",   "WKB Binary","Polygon boundary of the flooded region"],
    ["start_date", "Date",     "First day of the flood event"],
    ["end_date",   "Date",     "Last day of the flood event"],
]
story.append(data_table(
    ["Column", "Type", "Description"],
    schema_rows,
    col_widths=[4*cm, 3*cm, CONTENT_W - 7*cm]
))
story.append(sp(10))

story.append(Paragraph("Engineering Pipeline", s_h2))
steps = [
    ("1. Load & Inspect",
     "Dataset loaded from Parquet using PyArrow for columnar memory efficiency. "
     "Initial footprint: 1,349 MB. Date parsing, dtype validation, and quality audit performed."),
    ("2. Coordinate Extraction",
     "Raw WKB binary geometries parsed using Shapely in batches of 100,000. "
     "Polygon centroids extracted to latitude/longitude. Geometry column dropped — "
     "memory reduced to 309 MB."),
    ("3. Feature Engineering",
     "Seven new features derived: year, month, quarter, day_of_week, duration_days, "
     "season (Winter/Spring/Summer/Fall), and size_category (Small/Medium/Large/Catastrophic)."),
    ("4. Spatial Grid System",
     "10,628 unique 1°×1° grid cells created by rounding coordinates to the nearest degree. "
     "Per-cell metrics aggregated: event frequency, total area, and average event size."),
    ("5. Risk Scoring",
     "Three per-cell metrics normalised to 0–100 using MinMaxScaler and combined into a "
     "composite Risk Score for global cell ranking."),
]
for title, desc in steps:
    story.append(Paragraph(title, s_h3))
    story.append(Paragraph(desc, s_body))
    story.append(sp(4))

story.append(PageBreak())

# ══════════════════════════════════════════════════════
# SECTION 3 — KEY FINDINGS
# ══════════════════════════════════════════════════════
story.append(section_badge("03 · KEY FINDINGS", C_AMBER))
story.append(sp(6))
story.append(Paragraph("Key Findings", s_h1))
story.append(rule())

story.append(Paragraph("Temporal Trends", s_h2))
story.append(Paragraph(
    "Annual flood event monitoring grew by 261× between 2000 and 2024, reaching a peak "
    "of 402,012 events in 2024. Total flooded area grew 167× over the same period, peaking "
    "at 54.1 million km² in 2024. While the media ecosystem growth partially inflates early-"
    "period undercounting, the physical escalation trend is statistically robust when "
    "cross-referenced against the dataset's 85–100% recall validation against GDACS and the "
    "Dartmouth Flood Observatory.",
    s_body))
story.append(sp(8))

story.append(Paragraph("Seasonal & Size Distribution", s_h2))
seasonal_data = [
    ["Summer (Jun–Aug)", "909,952", "34.4%", "Primary monsoon window — highest global exposure"],
    ["Fall (Sep–Nov)",   "753,300", "28.5%", "Secondary peak driven by Atlantic hurricane season"],
    ["Winter (Dec–Feb)", "533,593", "20.2%", "Persistent activity in tropical low-latitude zones"],
    ["Spring (Mar–May)", "449,457", "17.0%", "Lowest volume — snowmelt flood signal in N. Hemisphere"],
]
story.append(data_table(
    ["Season", "Events", "Share", "Business Implication"],
    seasonal_data,
    col_widths=[3*cm, 2.5*cm, 1.8*cm, CONTENT_W - 7.3*cm]
))
story.append(sp(8))

size_data = [
    ["Small",         "< 100 km²",     "2,291,305", "86.6%", "High frequency, localised — neighbourhood-level exposure"],
    ["Medium",        "100–1,000 km²", "238,202",   "9.0%",  "District-level — critical infrastructure risk zone"],
    ["Large",         "1,000–10,000",  "116,795",   "4.4%",  "Regional impact — multi-asset insurance exposure"],
    ["Catastrophic",  "> 10,000 km²",  "0",         "0.0%",  "None recorded in dataset period"],
]
story.append(data_table(
    ["Category", "Area Range", "Events", "Share", "Implication"],
    size_data,
    col_widths=[2.5*cm, 2.8*cm, 2*cm, 1.5*cm, CONTENT_W - 8.8*cm]
))
story.append(sp(10))

story.append(Paragraph("Top 5 Highest-Risk Grid Cells", s_h2))
risk_data = [
    ["1", "-6°N 107°E", "Java, Indonesia",  "67.54", "Very high event density + large area per event"],
    ["2", "11°N 107°E", "S. Vietnam",       "42.10", "Mekong Delta: seasonal inundation + urban growth"],
    ["3", "-7°N 108°E", "Java, Indonesia",  "40.90", "Compounding adjacent-cell risk from Cell #1"],
    ["4", "19°N -99°W", "Mexico City",      "40.84", "Urban impermeability + basin geography"],
    ["5", "14°N 101°E", "C. Thailand",      "37.23", "Chao Phraya floodplain — critical agri-industrial zone"],
]
story.append(data_table(
    ["Rank", "Grid", "Region", "Score", "Risk Driver"],
    risk_data,
    col_widths=[1.2*cm, 2.5*cm, 3.5*cm, 2*cm, CONTENT_W - 9.2*cm]
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# SECTION 4 — MACHINE LEARNING
# ══════════════════════════════════════════════════════
story.append(section_badge("04 · MACHINE LEARNING", C_RED))
story.append(sp(6))
story.append(Paragraph("Machine Learning", s_h1))
story.append(rule())

story.append(Paragraph("Flood Recurrence Prediction (RandomForest)", s_h2))
story.append(Paragraph(
    "A binary classification model was built to predict whether a flood event will be followed "
    "by another in the same grid cell within 180 days. The prediction task was structured as "
    "a time-ordered lookup per cell: for each event, a target label was generated by checking "
    "whether any subsequent event occurred within the 180-day window.",
    s_body))
story.append(sp(6))

story.append(Paragraph("Model Configuration", s_h3))
config_data = [
    ["Algorithm",     "RandomForestClassifier (scikit-learn)"],
    ["Trees",         "50 estimators, max_depth=10"],
    ["Training Set",  "421,707 records (20% stratified sample)"],
    ["Test Set",      "105,427 records"],
    ["Class Balance", "97.7% positive (will recur), 2.3% negative"],
    ["Sampling",      "Stratified 20% sample to manage 2.6M scale"],
]
story.append(data_table(
    ["Parameter", "Value"],
    config_data,
    col_widths=[4*cm, CONTENT_W - 4*cm]
))
story.append(sp(10))

story.append(Paragraph("Performance Metrics", s_h3))
perf_kpis = [
    ("ACCURACY",  "97.70%", "Overall",          "#3b82f6"),
    ("PRECISION", "97.75%", "Predicted positives","#14b8a6"),
    ("RECALL",    "99.95%", "True positives",    "#f59e0b"),
    ("F1 SCORE",  "98.84%", "Harmonic mean",     "#ef4444"),
]
story.append(kpi_table(perf_kpis))
story.append(sp(12))

story.append(Paragraph("Feature Importance", s_h3))
fi_data = [
    ["1", "Event Frequency",  "63.21%", "Location's historical flood count — dominant predictor"],
    ["2", "Avg Event Size",   "16.39%", "Grid cell's average flooded area — proxies geographic exposure"],
    ["3", "Area (km²)",       "12.59%", "Individual event magnitude"],
    ["4", "Month",             "4.98%", "Seasonal signal — modest but consistent"],
    ["5", "Duration (days)",   "2.82%", "Event duration — least predictive feature"],
]
story.append(data_table(
    ["Rank", "Feature", "Importance", "Interpretation"],
    fi_data,
    col_widths=[1.2*cm, 3.5*cm, 2.5*cm, CONTENT_W - 7.2*cm]
))
story.append(sp(10))

story.append(insight_box(
    "<b>Transparency note — class imbalance caveat.</b> The dataset is highly imbalanced: "
    "97.7% of events are labelled as 'will recur'. A naive classifier that predicts "
    "'will recur' for every observation would achieve 97.7% accuracy by default. "
    "The confusion matrix reveals this: 2,366 false positives versus only 61 true negatives, "
    "meaning the model rarely correctly identifies a non-recurring location. "
    "In a production context, class rebalancing (SMOTE or class weights) and "
    "precision-at-low-threshold evaluation would be the appropriate next steps.",
    C_AMBER
))
story.append(sp(10))

story.append(Paragraph("Spatial Clustering (MiniBatchKMeans)", s_h2))
story.append(Paragraph(
    "All 2.6M records were clustered into 5 groups using MiniBatchKMeans — an "
    "approximate k-means variant designed for datasets that do not fit in memory "
    "simultaneously. Features used: area_km2, duration_days, latitude, longitude, month. "
    "PCA reduction to 2 components explains 45.8% of variance.",
    s_body))
story.append(sp(6))

cluster_data = [
    ["C0 — Large Coastal",        "52.0", "0.44", "-0.06°",  "6",  "Near-equatorial coastal, brief but large-area events"],
    ["C1 — Seasonal Inland",      "84.1", "3.36", "+21.7°",  "7",  "Tropical inland, multi-day duration, peak July"],
    ["C2 — Micro Urban",          "44.9", "0.48", "+12.3°",  "8",  "Dense urban nodes, high frequency, small area"],
    ["C3 — Tropical Persistent",  "71.2", "2.10", "+5.8°",   "7",  "Persistent wet-season flooding, large area"],
    ["C4 — High-Lat Brief",       "38.5", "0.65", "+48.2°",  "5",  "Mid-latitude spring events, shorter duration"],
]
story.append(data_table(
    ["Cluster", "Avg Area\n(km²)", "Avg Dur\n(days)", "Avg Lat", "Peak\nMonth", "Profile"],
    cluster_data,
    col_widths=[3.2*cm, 2*cm, 2*cm, 1.8*cm, 1.8*cm, CONTENT_W - 10.8*cm]
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════
# SECTION 5 — OUTPUTS & PORTFOLIO NOTE
# ══════════════════════════════════════════════════════
story.append(section_badge("05 · DELIVERABLES & SKILLS", C_TEAL))
story.append(sp(6))
story.append(Paragraph("Project Deliverables", s_h1))
story.append(rule())

story.append(Paragraph("Technical Outputs", s_h2))
outputs = [
    ["Jupyter Notebook",       "main.ipynb",                        "Full analysis pipeline — 48 cells"],
    ["Cleaned Dataset",        "groundsource_with_coords.parquet",  "309 MB optimised Parquet"],
    ["Streamlit Dashboard",    "app.py",                            "4-page interactive portfolio app"],
    ["PDF Report",             "flood_risk_report.pdf",             "This document"],
    ["Static Visualisations",  "*.png (4 charts)",                  "Publication-ready Matplotlib figures"],
    ["Interactive Charts",     "*.html (7 Plotly charts)",          "Embeddable HTML with hover/zoom"],
    ["ML Model",               "flood_recurrence_model.pkl",        "Serialised RandomForest (joblib)"],
    ["Analysis Summary",       "flood_analysis_summary.json",       "Machine-readable findings export"],
]
story.append(data_table(
    ["Deliverable", "Filename", "Notes"],
    outputs,
    col_widths=[4*cm, 5.5*cm, CONTENT_W - 9.5*cm]
))
story.append(sp(12))

story.append(Paragraph("Demonstrated Skills", s_h2))
skills = [
    ["Data Engineering",        "Parquet ingestion, WKB geometry parsing, batch processing, dtype optimisation, memory profiling"],
    ["Geospatial Analysis",     "Shapely WKB parsing, centroid extraction, 1°×1° spatial grid design, choropleth risk mapping"],
    ["Feature Engineering",     "Temporal decomposition, duration calculation, seasonal categorisation, spatial aggregation"],
    ["Machine Learning",        "MiniBatchKMeans clustering, PCA dimensionality reduction, RandomForest classification, stratified sampling, class imbalance awareness"],
    ["Data Visualisation",      "Matplotlib/Seaborn static charts, Plotly interactive dashboards, Mapbox geospatial scatter, sunburst hierarchy charts"],
    ["Business Translation",    "Risk scoring framework, policy-actionable insights, insurance underwriting implications, infrastructure planning signals"],
    ["Software Engineering",    "Modular notebook structure, ReportLab PDF generation, Streamlit app development, joblib model serialisation"],
]
story.append(data_table(
    ["Skill Domain", "Applied Techniques"],
    skills,
    col_widths=[4.5*cm, CONTENT_W - 4.5*cm]
))
story.append(sp(14))

story.append(rule(C_BLUE))
story.append(sp(6))
story.append(Paragraph(
    "Abhinav  ·  MSc Business Analytics, Aston University (2026)  ·  Business Consultant, Blackmont Consulting",
    S("final", fontSize=8, textColor=C_MUTED, alignment=TA_CENTER)
))
story.append(Paragraph(
    "Project source available on GitHub  ·  Built with Python, Pandas, Scikit-learn, Plotly, Streamlit, ReportLab",
    S("final2", fontSize=7, textColor=C_DIM, alignment=TA_CENTER)
))

# ─── BUILD ───────────────────────────────────────────
doc = BaseDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=MARGIN_L,
    rightMargin=MARGIN_R,
    topMargin=MARGIN_T,
    bottomMargin=MARGIN_B,
)

# Two page templates: cover (no header/footer) and body
cover_frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W, H - MARGIN_T - MARGIN_B, id='cover')
body_frame  = Frame(MARGIN_L, MARGIN_B + 0.8*cm, CONTENT_W, H - MARGIN_T - MARGIN_B - 0.8*cm, id='body')

doc.addPageTemplates([
    PageTemplate(id='Cover', frames=[cover_frame], onPage=cover_background),
    PageTemplate(id='Body',  frames=[body_frame],  onPage=page_background),
])

# Switch to body template after first page
from reportlab.platypus import NextPageTemplate
story.insert(1, NextPageTemplate('Body'))

doc.build(story)
print(f"✅ Report saved to: {OUTPUT}")
