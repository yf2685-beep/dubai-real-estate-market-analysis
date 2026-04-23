# Dubai Real Estate Market Analysis

> Comprehensive analysis of Dubai property market transactions (Jan–Jun 2023): price dynamics across 80+ areas, demand patterns by property type, seasonality, and investment cluster identification.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=flat)

---

## Overview

This project analyzes 6 months of Dubai real estate sales transaction data covering **80+ locations** across the emirate. The goal was to identify investment-grade areas, understand demand distribution by property type, and surface seasonality patterns.

This work directly informed the analytics approach used later in building a production [80-location market intelligence platform](https://github.com/nkrivoshey/linkedin-agent) at Metropolitan Premium Properties.

---

## Key Findings

- **Price distribution is highly right-skewed** — median transaction price significantly below mean, driven by ultra-premium outliers in Palm Jumeirah, Downtown, and DIFC
- **Apartments dominate volume** (~70% of transactions), but villas drive average ticket size
- **Strongest demand concentration**: Jumeirah Village Circle, Business Bay, Dubai Marina — high-volume, mid-market areas with consistent Q-o-Q activity
- **Seasonal peak**: March–April showed highest transaction volume; July–August softer (Ramadan + summer)
- **Investment signal**: Off-plan transactions outpaced ready property by ~2:1 in specific corridors (Dubai Hills, Meydan), indicating speculative demand
- **Price-per-sqft leaders**: Palm Jumeirah, Downtown Dubai, Dubai Creek Harbour — 2–3× emirate median

---

## Analysis Structure

```
Krivoshey_Nikita_Real_Estate_Analysis.ipynb
├── 1. Data Loading & Preprocessing
│   └── Type conversions, missing value handling, area standardization
├── 2. Data Overview & Summary Statistics
│   └── 80+ areas, property types, transaction counts, price ranges
├── 3. Time Series Analysis
│   └── Monthly/quarterly transaction trends, seasonality
├── 4. Property Type Distribution
│   └── Apartments vs. villas vs. commercial — volume and price breakdown
├── 5. Price Distribution Analysis
│   └── Histograms, percentile mapping, outlier identification
├── 6. Location Analysis
│   └── Area-level heatmaps, volume leaders, price leaders
├── 7. Seasonal Patterns
│   └── Month-over-month demand shifts, peak season identification
├── 8. Correlation Analysis
│   └── Price vs. size, area, property type — heatmap + scatter
└── 9. Price Prediction (Baseline)
    └── Feature-based model: size, location, property type → price estimate
```

---

## Dataset

Dubai Land Department (DLD) sales transaction data, Jan–Jun 2023.  
Dataset available on Google Drive: [link](https://drive.google.com/file/d/1HtPmVOFeYprczsDIi0eOyA8qBqLW_RUE/view)

---

## How to Run

```bash
pip install pandas matplotlib seaborn scikit-learn jupyter
jupyter notebook Krivoshey_Nikita_Real_Estate_Analysis.ipynb
```

---

## Context

This analysis was part of ongoing market research while working at **Metropolitan Premium Properties** (Dubai's largest premium real estate brokerage), where I later built a production analytics platform covering the same 80+ locations — including ML-powered price forecasts, live Power BI dashboards, and a Telegram bot for broker intelligence.

---

*By [Nikita Krivoshei](https://www.linkedin.com/in/nikita-krivoshei/) · Data Analyst @ Metropolitan Premium Properties*
