# Flood Risk Intelligence Platform

**AI-powered flood risk intelligence platform built on 2.6M global events**

![Dashboard Preview](assets/dashboard_preview.png)

## Project Overview
This repository contains a full-stack data product designed to predict, cluster, and analyze global flood events. By processing historical meteorological variables, this tool provides actionable intelligence for risk mitigation, urban planning, and insurance risk modeling.

The primary model processes over 2.6 million historical flood records to detect patterns and predict future vulnerabilities with **97.7% accuracy** (note: metric accounts for significant class imbalance via stratified sampling and SMOTE).

## Dataset
**Google Research Groundsource dataset (2026)**
The core analysis is built on this extensive dataset. It is not hosted in this repository due to its scale (~300MB). Please see `data/README.md` for download and integration instructions.

## Key Outcomes
*   **Predictive Modeling**: High-precision models that distinguish between high-risk recurrence zones and anomalous events.
*   **Interactive Analytics**: Plotly-driven interactive mapping of global flood hot spots.
*   **Clustering**: Unsupervised PCA clustering to categorize flood profiles by severity, duration, and seasonality.

## Business Applications
*   **Insurance Underwriting**: Dynamically adjust premiums based on geographically localized, AI-verified risk scores.
*   **Disaster Response Logistics**: Pre-position emergency resources by predicting high-probability seasonal flood zones.
*   **Urban Development**: Inform infrastructure scaling based on long-term flood pattern clustering.

## Project Structure
The repository is modularized for clarity and rapid replication:

```text
flood-risk-intelligence/
├── app/               # Streamlit dashboard product layer
├── notebook/          # Core analysis, modeling, and evaluation (main.ipynb)
├── outputs/           # Precomputed artifacts and visualizations
│   ├── charts/        # Key static plots (Severity, Seasonality)
│   └── interactive/   # Interactive Plotly HTML maps and clusters
├── assets/            # README embeds and visual assets
└── data/              # Location for local datasets (ignored by git)
```

## Quickstart

### 1. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/Abhinav15s/Flood-risk-intelligence.git
cd Flood-risk-intelligence
pip install -r requirements.txt
```

### 2. Fetch Data
Download the data as outlined in `data/README.md`.

### 3. Run the Dashboard
Launch the Streamlit intelligence dashboard:
```bash
streamlit run app/app.py
```