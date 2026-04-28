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

## Data Analysis & Conclusions

### 1. Market Overview
The dataset covers **54,289 transactions** (41,691 sales, 10,632 mortgages, 1,758 gifts) across 83 days from February 1 to April 24, 2026. February recorded the highest activity — **16,957 sales totaling AED 50.7 billion** — while volume declined month-on-month through March (13,438 sales, AED 37.4B) and April (11,296 sales, AED 32.7B), likely reflecting the typical seasonal slowdown as Ramadan approached.

### 2. Price Distribution Is Highly Skewed
The median sale price is **AED 1.68 million**, but the mean is **AED 2.90 million** — a 1.73× gap driven by ultra-premium outliers (skewness = 4.76). This means headline "average price" figures routinely overstate what a typical buyer pays by nearly 75%. For any policy or affordability analysis, the median is the only honest reference point.

![Price distribution](figures/fig03_price_distribution.png)

### 3. Conflict Marker: Volume Dropped, Prices Held
After the February 28 geopolitical conflict marker, **daily sales volume fell from 647.8 to 443.7 transactions/day (−32%)**, but median prices showed virtually no change (AED 1.68M both periods, p = 0.147 — statistically insignificant). This suggests the conflict suppressed transaction activity but did not trigger a price correction, consistent with Dubai's reputation as a market with sticky seller expectations. Notably, the **off-plan share rose from 62.2% pre-conflict to 72.0% post-conflict**, suggesting buyers shifted toward developer deals (typically with flexible payment plans) as financial uncertainty increased.

![Pre vs post conflict comparison](figures/fig05_pre_post_conflict_comparison.png)

### 4. Off-Plan Dominates — but Ready Commands a Premium
**68% of all sales are off-plan**, reflecting Dubai's developer-led supply model. Counterintuitively, **ready properties have a higher median price (AED 1.80M) than off-plan (AED 1.65M)**. This is not a paradox: off-plan properties are often sold early at a discount to attract investors, while ready units in established locations command a premium for immediate occupancy.

![Off-plan vs ready analysis](figures/fig11_offplan_vs_ready.png)

### 5. Volume Leaders ≠ Price Leaders
The highest-volume areas — Jumeirah Village Circle (2,729 sales), Madinat Al Mataar (2,586), Al Yelayiss 1 (2,014) — are mid-market, high-density residential districts. The highest-price areas — Palm Jabal Ali (AED 26M median), Trade Center Second (AED 15.3M), Marsa Dubai (AED 48,755/sqm) — are premium waterfront and business corridors. These two lists share almost no overlap, confirming that Dubai's market is structurally bifurcated between an investor-driven volume segment and a luxury segment.

![Top areas by volume](figures/fig06_top_areas_volume.png)
![Top areas by median price](figures/fig07_top_areas_price.png)

### 6. Metro Proximity Creates a 6.5× Price Gap
Transactions near premium metro stations (Mina Seyahi: AED 4.5M median; Palm Jumeirah: AED 4.2M; Financial Centre: AED 4.0M) are priced **6–7× higher** than those near outer-district stations (Rashidiya: AED 0.69M; Sharaf DG: AED 1.03M). Infrastructure access is not just a convenience — it is a primary driver of property valuation in Dubai.

![Price by metro station](figures/fig15_price_by_metro.png)

### 7. 1BR Units Drive Volume; Size Strongly Predicts Price
Among unit sales, **1BR apartments lead with 13,883 transactions**, followed by 2BR (8,534) and Studios (8,268) — a profile consistent with investor-driven demand rather than family end-use. Property area is a strong predictor of price: **Pearson r = 0.793** (p < 0.001), meaning size explains approximately 63% of the variance in unit prices. The remaining 37% is attributable to location, finishes, and proximity to amenities.

![Room configuration analysis](figures/fig12_room_configuration_analysis.png)
![Area vs price scatter](figures/fig13_area_vs_price_scatter.png)

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

### Transaction Volume Over Time
![Daily transaction volume with conflict marker](figures/fig01_transaction_volume_over_time.png)

### Weekly Volume by Transaction Type
![Weekly volume by Sales/Mortgage/Gifts](figures/fig02_weekly_volume_by_type.png)

### Price Distribution
![Price histogram and box plot by property type](figures/fig03_price_distribution.png)

### Price & Volume Over Time
![Rolling median price and daily sales volume](figures/fig04_price_and_volume_over_time.png)

### Pre vs Post Conflict Comparison
![Bar chart comparison of price, volume, and off-plan share](figures/fig05_pre_post_conflict_comparison.png)

### Top Areas by Sales Volume
![Top 15 areas by transaction count](figures/fig06_top_areas_volume.png)

### Top Areas by Median Price
![Top 15 areas by median sale price](figures/fig07_top_areas_price.png)

### Top Areas by Price per sqm
![Top 15 areas by price per square meter](figures/fig08_top_areas_price_per_sqm.png)

### Property Type Distribution
![Pie chart and sub-type bar chart](figures/fig09_property_type_distribution.png)

### Price by Property Sub-Type
![Violin plot of price by sub-type](figures/fig10_price_by_subtype.png)

### Off-Plan vs Ready Analysis
![Weekly volume, median price, and rolling off-plan share](figures/fig11_offplan_vs_ready.png)

### Room Configuration Analysis
![Volume and price by bedroom count](figures/fig12_room_configuration_analysis.png)

### Area vs Price Scatter
![Scatter plot colored by price per sqm](figures/fig13_area_vs_price_scatter.png)

### Correlation Heatmap
![Correlation matrix of numeric features](figures/fig14_correlation_heatmap.png)

### Price by Nearest Metro Station
![Median price by nearest metro station](figures/fig15_price_by_metro.png)

### Monthly Summary
![2x2 monthly aggregated summary](figures/fig16_monthly_summary.png)

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
