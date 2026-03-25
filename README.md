# 🌊 Global Flood Risk Intelligence Dashboard

[![GitHub stars](https://img.shields.io/github/stars/Abhinav15s/Flood-risk-intelligence)](https://github.com/Abhinav15s/Flood-risk-intelligence)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-brightgreen.svg)](https://share.streamlit.io/)
[![PDF Report](https://img.shields.io/badge/Report-PDF-red.svg)](outputs/flood_risk_report.pdf)

**Comprehensive analysis of 2.6M flood events** using Google's Groundsource dataset. Built 87% accurate predictive model, identified 100 highest-risk zones, and created interactive Streamlit dashboard.

---

## 📂 Repository Structure

```text
flood-risk-intelligence/        # GitHub root
├── README.md                   # Project showcase
├── requirements.txt            # Python dependencies (pip install -r requirements.txt)
├── .gitignore                  # Excludes *.parquet, *.pkl, outputs/
├── notebook/                   # Core analysis
│   └── main.ipynb              # 48-cell analysis pipeline — the technical centrepiece
├── app/                        # Streamlit dashboard
│   ├── app.py                  # 4-page portfolio dashboard
│   └── generate_report.py      # PDF report generator (ReportLab)
├── outputs/                    # Pre-generated artefacts — tracked in git
│   ├── flood_risk_report.pdf   # Portfolio PDF
│   ├── flood_analysis_summary.json # Machine-readable findings
│   └── charts/                 # Static charts + interactive Plotly files
└── assets/                     # Screenshots for README
    └── dashboard_preview.png   # Dashboard screenshot
```

## 🎯 Project Overview

**Problem:** Limited historical flood data hinders disaster preparedness  
**Solution:** AI-powered analysis of 2.6M geo-tagged events (2000-2026)  
**Impact:** Actionable risk maps for emergency agencies, insurers, urban planners

### Key Results
- 📈 **80,600% increase** in flood events (2000: 498 → 2024: 402K)
- 🎯 **87% accurate** flood recurrence prediction model
- 🗺️ **100 highest-risk zones** identified globally
- 🔍 **5 flood cluster types** discovered (monsoon, flash, river, coastal, catastrophic)

## 📊 Key Visualizations

| Temporal Trends | Risk Assessment | ML Results |
|---------------|---------------|------------|
| ![Events Trend](outputs/charts/events_per_year_trend.png) | ![Clusters](outputs/charts/flood_clusters_pca.png) | ![Confusion Matrix](outputs/charts/confusion_matrix.png) |

## 🛠️ Technical Stack
- **Languages:** Python (Pandas, Scikit-learn, Plotly)
- **Dashboard:** Streamlit
- **Reporting:** ReportLab (PDF)
- **Deployment:** GitHub Pages / Streamlit Cloud

---
*Created by [Abhinav15s](https://github.com/Abhinav15s)*