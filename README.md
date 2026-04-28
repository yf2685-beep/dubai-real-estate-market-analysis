# Dubai Real Estate Market Analysis
## HCDS Final Project — Team 3

> Numerical analysis of 54,289 Dubai Land Department transactions (Feb–Apr 2026): price dynamics before and after the Feb 28 geopolitical conflict marker, area-level demand patterns, off-plan vs. ready property trends, and property-type breakdowns.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=flat)
![Course](https://img.shields.io/badge/NYU-Human--Centered%20Data%20Science-57068C?style=flat)

---

## Research Questions

1. How did transaction volume and prices evolve across the Feb–Apr 2026 period?
2. What measurable impact, if any, did the Feb 28 conflict marker have on market activity?
3. Which areas and property types drive market activity — and which lead on price?
4. How do off-plan and ready properties differ in price trend and volume?
5. What are the key statistical patterns in pricing, area size, and bedroom configuration?

---

## Key Findings

- **54,289 total transactions** (41,899 sales, 10,632 mortgages, 1,758 gifts) over 83 days
- **Price distribution is right-skewed** — median sale price (~1.6M AED) is well below the mean (~3.6M AED), driven by ultra-premium outliers in Palm Jumeirah, Downtown Dubai, and DIFC
- **Off-plan dominates**: ~69% of sales are off-plan, indicating Dubai's developer-led supply model persists under conflict conditions
- **Volume held post-conflict**: daily sales volume showed no sustained decline after Feb 28, though weekly variance increased
- **Top volume areas**: Jumeirah Village Circle, Madinat Al Mataar, Business Bay — mid-market, high-density residential
- **Top price areas**: Palm Jumeirah, Downtown Dubai, Dubai Marina — 3–5× emirate median
- **Bedroom demand**: 1BR units dominate by count (17,253 sales); studios are the second-largest segment — investor-oriented demand
- **Metro proximity premium**: stations near premium corridors (Burj Khalifa/Dubai Mall, DIFC) correlate with 3–4× higher median prices than outer-district stations

---

## Human-Centered Reflections

This analysis was conducted in the context of an HCDS course. Three critical data decisions are documented in the notebook:

1. **Median vs. mean**: We use median throughout for price analysis. The 2–3× gap between mean and median is not a statistical footnote — it determines whether policy recommendations favor developers or residents.

2. **Pre/post split asymmetry**: The "pre-conflict" window is 27 days; the "post-conflict" is 56 days. Raw count comparisons are misleading — we normalize to daily rates.

3. **Missing data is not random**: `NEAREST_METRO_EN` nulls cluster in outer districts; `MASTER_PROJECT_EN` nulls cluster in Land transactions. These gaps encode geographic and administrative inequalities in the data infrastructure itself.

---

## Analysis Structure

```
Dubai_Market_Analysis.ipynb
├── 0. Setup & Configuration
├── 1. Data Loading & Preprocessing
│   └── Type conversions, outlier capping (top 0.5%), period labeling
├── 2. Transaction Volume Over Time
│   └── Daily bar + 7-day rolling avg, weekly by transaction type
├── 3. Price Distribution Analysis
│   └── Histogram (mean vs median), box plot by property type
├── 4. Price Over Time & Pre/Post Conflict
│   └── Rolling median price, daily volume, Mann-Whitney U test
│   └── Bar chart comparison: price, daily volume, off-plan share
├── 5. Geographic Analysis
│   └── Top 15 areas by volume, by median price, by price/sqm
├── 6. Property & Sub-Type Analysis
│   └── Pie chart (Unit/Land/Building), violin by sub-type
├── 7. Off-Plan vs Ready Analysis
│   └── Weekly volume, median price, 14-day rolling share %
├── 8. Room Configuration Analysis
│   └── Volume and median price by bedroom type (Studio → 6BR)
├── 9. Area vs Price Scatter & Correlation
│   └── Scatter (colored by price/sqm), Pearson r, correlation heatmap
├── 10. Metro Influence
│    └── Median price by nearest metro station (top 12)
├── 11. Monthly Summary
│    └── Count, total value, median price, off-plan share by month
└── 12. Key Findings & Human-Centered Reflection
```

---

## Generated Figures

All figures are saved to the `figures/` directory when the notebook runs:

| File | Description |
|------|-------------|
| `fig01_transaction_volume_over_time.png` | Daily transaction count with conflict marker |
| `fig02_weekly_volume_by_type.png` | Weekly volume by Sales/Mortgage/Gifts |
| `fig03_price_distribution.png` | Histogram + box plot by property type |
| `fig04_price_and_volume_over_time.png` | Rolling median price + daily sales volume |
| `fig05_pre_post_conflict_comparison.png` | Pre/post bar comparison (price, volume, off-plan) |
| `fig06_top_areas_volume.png` | Top 15 areas by sales count |
| `fig07_top_areas_price.png` | Top 15 areas by median price |
| `fig08_top_areas_price_per_sqm.png` | Top 15 areas by price per sqm |
| `fig09_property_type_distribution.png` | Pie chart + sub-type bar chart |
| `fig10_price_by_subtype.png` | Violin plot: price by sub-type |
| `fig11_offplan_vs_ready.png` | Weekly volume, median price, rolling share % |
| `fig12_room_configuration_analysis.png` | Volume and price by bedroom count |
| `fig13_area_vs_price_scatter.png` | Area vs price scatter (colored by price/sqm) |
| `fig14_correlation_heatmap.png` | Correlation matrix of numeric features |
| `fig15_price_by_metro.png` | Median price by nearest metro station |
| `fig16_monthly_summary.png` | 2×2 monthly aggregated summary |

---

## Dataset

Dubai Land Department (DLD) open transaction data downloaded April 24, 2026.  
**22 columns**, 54,289 rows, date range: Feb 1 – Apr 24, 2026.

Key columns:
- `INSTANCE_DATE` — transaction date/time
- `GROUP_EN` — transaction type (Sales / Mortgage / Gifts)
- `IS_OFFPLAN_EN` — Off-Plan or Ready
- `AREA_EN` — district name
- `PROP_TYPE_EN` — Unit / Land / Building
- `TRANS_VALUE` — transaction value (AED)
- `ACTUAL_AREA` — property area (sqm)
- `ROOMS_EN` — bedroom configuration

---

## How to Run

```bash
# Install dependencies
pip install pandas matplotlib seaborn scipy numpy jupyter

# Generate all figures as standalone script (no Jupyter needed)
python generate_figures.py

# Or run the full notebook
jupyter notebook Dubai_Market_Analysis.ipynb
```

Place `transactions-2026-04-24.csv` in the same directory as the notebook before running.

---

## Team

**HCDS Final Project — Team 3**  
NYU · Human-Centered Data Science · Spring 2026
