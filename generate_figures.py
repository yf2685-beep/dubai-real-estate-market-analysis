"""Run this script to regenerate all figures from transactions-2026-04-24.csv."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)
plt.rcParams.update({'figure.dpi': 120, 'savefig.bbox': 'tight', 'savefig.dpi': 150,
                     'axes.spines.top': False, 'axes.spines.right': False})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'transactions-2026-04-24.csv')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
CONFLICT_DATE = pd.Timestamp('2026-02-28')

def savefig(name):
    path = os.path.join(FIGURES_DIR, name)
    plt.savefig(path)
    plt.close()
    print(f'  Saved: {name}')

# ── Load & preprocess ─────────────────────────────────────────────────────────
print('Loading data...')
df = pd.read_csv(CSV_PATH)
df['date'] = pd.to_datetime(df['INSTANCE_DATE'])
df['week'] = df['date'].dt.to_period('W').apply(lambda r: r.start_time)
df['month'] = df['date'].dt.to_period('M').apply(lambda r: r.start_time)
df['price_m'] = df['TRANS_VALUE'] / 1_000_000
df['price_per_sqm'] = df['TRANS_VALUE'] / df['ACTUAL_AREA'].replace(0, np.nan)
df = df.sort_values('date').reset_index(drop=True)
df['period'] = np.where(df['date'] < CONFLICT_DATE, 'Pre-Conflict (Feb 1–27)', 'Post-Conflict (Feb 28–Apr 24)')

sales = df[df['GROUP_EN'] == 'Sales'].copy()
price_cap = sales['TRANS_VALUE'].quantile(0.995)
sales_clean = sales[sales['TRANS_VALUE'] <= price_cap].copy()
pre = sales_clean[sales_clean['date'] < CONFLICT_DATE]
post = sales_clean[sales_clean['date'] >= CONFLICT_DATE]
print(f'  {len(df):,} total rows | {len(sales_clean):,} cleaned sales')

# ── Fig 01: Daily transaction volume ─────────────────────────────────────────
print('Generating figures...')
daily_volume = df.groupby('date').size().reset_index(name='count')
rolling7 = daily_volume.set_index('date')['count'].rolling(7, min_periods=1).mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 5))
ax.bar(daily_volume['date'], daily_volume['count'], color='#4C72B0', alpha=0.4, width=0.8, label='Daily count')
ax.plot(rolling7['date'], rolling7['count'], color='#C44E52', lw=2, label='7-day rolling avg')
ax.axvline(CONFLICT_DATE, color='#DD8452', linestyle='--', lw=1.8, label=f'Conflict marker: {CONFLICT_DATE.date()}')
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.xticks(rotation=30, ha='right')
ax.set_title('Daily Transaction Volume — All Types (Feb–Apr 2026)', fontsize=14, fontweight='bold')
ax.set_xlabel('Date'); ax.set_ylabel('Number of Transactions'); ax.legend()
savefig('fig01_transaction_volume_over_time.png')

# ── Fig 02: Weekly volume by type ─────────────────────────────────────────────
weekly_by_type = df.groupby(['week', 'GROUP_EN']).size().reset_index(name='count')
fig, ax = plt.subplots(figsize=(14, 5))
colors_map = {'Sales': '#4C72B0', 'Mortgage': '#DD8452', 'Gifts': '#55A868'}
for grp, gdf in weekly_by_type.groupby('GROUP_EN'):
    ax.plot(gdf['week'], gdf['count'], marker='o', markersize=4, label=grp, color=colors_map.get(grp, 'gray'))
ax.axvline(CONFLICT_DATE, color='red', linestyle='--', lw=1.5, label=f'Conflict marker: {CONFLICT_DATE.date()}')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.xticks(rotation=30, ha='right')
ax.set_title('Weekly Transaction Volume by Type', fontsize=14, fontweight='bold')
ax.set_xlabel('Week'); ax.set_ylabel('Transactions'); ax.legend()
savefig('fig02_weekly_volume_by_type.png')

# ── Fig 03: Price distribution ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
ax.hist(sales_clean['price_m'], bins=60, color='#4C72B0', edgecolor='white', linewidth=0.4)
ax.axvline(sales_clean['price_m'].median(), color='#C44E52', lw=2, linestyle='--',
           label=f'Median: {sales_clean["price_m"].median():.1f}M AED')
ax.axvline(sales_clean['price_m'].mean(), color='#DD8452', lw=2,
           label=f'Mean: {sales_clean["price_m"].mean():.1f}M AED')
ax.set_title('Transaction Value Distribution (Sales)', fontweight='bold')
ax.set_xlabel('Transaction Value (Million AED)'); ax.set_ylabel('Frequency'); ax.legend()

ax2 = axes[1]
prop_types = sales_clean['PROP_TYPE_EN'].unique()
data_by_type = [sales_clean[sales_clean['PROP_TYPE_EN'] == t]['price_m'].dropna() for t in prop_types]
bp = ax2.boxplot(data_by_type, labels=prop_types, patch_artist=True, notch=True)
for patch, c in zip(bp['boxes'], ['#4C72B0', '#DD8452', '#55A868']):
    patch.set_facecolor(c); patch.set_alpha(0.7)
ax2.set_title('Price Distribution by Property Type', fontweight='bold')
ax2.set_xlabel('Property Type'); ax2.set_ylabel('Transaction Value (Million AED)')
plt.tight_layout()
savefig('fig03_price_distribution.png')

# ── Fig 04: Price & volume over time ─────────────────────────────────────────
daily_price = sales_clean.groupby('date').agg(
    median_price=('price_m', 'median'), count=('price_m', 'count')).reset_index()
daily_price['rolling_median'] = daily_price['median_price'].rolling(7, min_periods=1).mean()

fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True)
ax = axes[0]
ax.fill_between(daily_price['date'], daily_price['median_price'], alpha=0.15, color='#4C72B0')
ax.plot(daily_price['date'], daily_price['rolling_median'], color='#4C72B0', lw=2, label='7-day rolling median price')
ax.axvline(CONFLICT_DATE, color='red', linestyle='--', lw=1.5, label=f'Conflict marker: {CONFLICT_DATE.date()}')
ax.set_title('Median Transaction Price Over Time (Sales, M AED)', fontsize=13, fontweight='bold')
ax.set_ylabel('Price (Million AED)'); ax.legend()

ax2 = axes[1]
ax2.bar(daily_price['date'], daily_price['count'], color='#55A868', alpha=0.5, width=0.8, label='Daily sale count')
ax2.plot(daily_price['date'], daily_price['count'].rolling(7, min_periods=1).mean(),
         color='#2D6A4F', lw=2, label='7-day rolling avg')
ax2.axvline(CONFLICT_DATE, color='red', linestyle='--', lw=1.5)
ax2.set_title('Daily Sales Volume', fontsize=13, fontweight='bold')
ax2.set_ylabel('Number of Sales'); ax2.set_xlabel('Date')
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.xticks(rotation=30, ha='right'); ax2.legend()
plt.tight_layout()
savefig('fig04_price_and_volume_over_time.png')

# ── Fig 05: Pre/post conflict bar comparison ──────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
colors_period = ['#4C72B0', '#C44E52']
labels = ['Pre-Conflict\n(Feb 1–27)', 'Post-Conflict\n(Feb 28–Apr 24)']

axes[0].bar(labels, [pre['price_m'].median(), post['price_m'].median()],
            color=colors_period, width=0.5)
for i, v in enumerate([pre['price_m'].median(), post['price_m'].median()]):
    axes[0].text(i, v + 0.02, f'{v:.2f}M', ha='center', fontweight='bold')
axes[0].set_title('Median Sale Price (M AED)', fontweight='bold'); axes[0].set_ylabel('Million AED')

pre_daily = len(pre) / max((CONFLICT_DATE - pre['date'].min()).days, 1)
post_daily = len(post) / max((post['date'].max() - CONFLICT_DATE).days + 1, 1)
axes[1].bar(labels, [pre_daily, post_daily], color=colors_period, width=0.5)
for i, v in enumerate([pre_daily, post_daily]):
    axes[1].text(i, v + 0.5, f'{v:.1f}', ha='center', fontweight='bold')
axes[1].set_title('Avg Daily Sales Volume', fontweight='bold'); axes[1].set_ylabel('Transactions/day')

pre_op = (pre['IS_OFFPLAN_EN'] == 'Off-Plan').mean() * 100
post_op = (post['IS_OFFPLAN_EN'] == 'Off-Plan').mean() * 100
axes[2].bar(labels, [pre_op, post_op], color=colors_period, width=0.5)
for i, v in enumerate([pre_op, post_op]):
    axes[2].text(i, v + 0.5, f'{v:.1f}%', ha='center', fontweight='bold')
axes[2].set_title('Off-Plan Transaction Share (%)', fontweight='bold'); axes[2].set_ylabel('Percentage (%)')

plt.suptitle('Pre vs Post Conflict Market Comparison', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
savefig('fig05_pre_post_conflict_comparison.png')

# ── Fig 06: Top areas by volume ───────────────────────────────────────────────
area_volume = sales_clean.groupby('AREA_EN').size().nlargest(15).reset_index(name='count')
fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.barh(area_volume['AREA_EN'][::-1], area_volume['count'][::-1], color='#4C72B0', alpha=0.85)
ax.bar_label(bars, padding=3, fmt='%d')
ax.set_title('Top 15 Areas by Sales Transaction Count (Feb–Apr 2026)', fontsize=13, fontweight='bold')
ax.set_xlabel('Number of Transactions')
savefig('fig06_top_areas_volume.png')

# ── Fig 07: Top areas by median price ────────────────────────────────────────
area_price = (sales_clean.groupby('AREA_EN').filter(lambda x: len(x) >= 20)
              .groupby('AREA_EN')['price_m'].median().nlargest(15).reset_index())
fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.barh(area_price['AREA_EN'][::-1], area_price['price_m'][::-1], color='#C44E52', alpha=0.85)
ax.bar_label(bars, padding=3, fmt='%.1fM')
ax.set_title('Top 15 Areas by Median Sale Price — AED (min 20 sales)', fontsize=13, fontweight='bold')
ax.set_xlabel('Median Transaction Value (Million AED)')
savefig('fig07_top_areas_price.png')

# ── Fig 08: Top areas by price/sqm ───────────────────────────────────────────
area_psm = (sales_clean[sales_clean['price_per_sqm'].notna() & (sales_clean['price_per_sqm'] > 0)]
            .groupby('AREA_EN').filter(lambda x: len(x) >= 20)
            .groupby('AREA_EN')['price_per_sqm'].median().nlargest(15).reset_index())
fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.barh(area_psm['AREA_EN'][::-1], area_psm['price_per_sqm'][::-1], color='#DD8452', alpha=0.85)
ax.bar_label(bars, padding=3, fmt='%.0f')
ax.set_title('Top 15 Areas by Median Price per sqm (AED/sqm)', fontsize=13, fontweight='bold')
ax.set_xlabel('Price per sqm (AED)')
savefig('fig08_top_areas_price_per_sqm.png')

# ── Fig 09: Property type distribution ───────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
prop_counts = df['PROP_TYPE_EN'].value_counts()
axes[0].pie(prop_counts.values, labels=prop_counts.index, autopct='%1.1f%%',
            colors=['#4C72B0', '#DD8452', '#55A868'], startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
axes[0].set_title('Property Type Distribution\n(All Transactions)', fontweight='bold')
subtype_counts = sales_clean['PROP_SB_TYPE_EN'].value_counts().head(8)
axes[1].barh(subtype_counts.index[::-1], subtype_counts.values[::-1], color='#4C72B0', alpha=0.8)
axes[1].set_title('Top Property Sub-Types (Sales)', fontweight='bold')
axes[1].set_xlabel('Number of Transactions')
plt.tight_layout()
savefig('fig09_property_type_distribution.png')

# ── Fig 10: Price by sub-type violin ─────────────────────────────────────────
top_subtypes = sales_clean['PROP_SB_TYPE_EN'].value_counts().head(6).index
sub_df = sales_clean[sales_clean['PROP_SB_TYPE_EN'].isin(top_subtypes)]
sub_order = sub_df.groupby('PROP_SB_TYPE_EN')['price_m'].median().sort_values(ascending=False).index
fig, ax = plt.subplots(figsize=(12, 6))
sns.violinplot(data=sub_df, x='PROP_SB_TYPE_EN', y='price_m', order=sub_order,
               palette='muted', inner='quartile', ax=ax)
ax.set_title('Price Distribution by Property Sub-Type', fontsize=13, fontweight='bold')
ax.set_xlabel('Property Sub-Type'); ax.set_ylabel('Transaction Value (Million AED)')
plt.xticks(rotation=20, ha='right')
savefig('fig10_price_by_subtype.png')

# ── Fig 11: Off-plan vs ready ─────────────────────────────────────────────────
weekly_offplan = sales_clean.groupby(['week', 'IS_OFFPLAN_EN']).size().reset_index(name='count')
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

ax = axes[0]
for grp, gdf in weekly_offplan.groupby('IS_OFFPLAN_EN'):
    ax.plot(gdf['week'], gdf['count'], marker='o', markersize=4, label=grp)
ax.axvline(CONFLICT_DATE, color='red', linestyle='--', lw=1.2)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
ax.set_title('Weekly Volume: Off-Plan vs Ready', fontweight='bold')
ax.set_ylabel('Transactions'); ax.legend()

ax2 = axes[1]
offplan_price = sales_clean.groupby('IS_OFFPLAN_EN')['price_m'].median()
bars = ax2.bar(offplan_price.index, offplan_price.values, color=['#4C72B0', '#DD8452'], alpha=0.85, width=0.4)
ax2.bar_label(bars, fmt='%.2fM', padding=3, fontweight='bold')
ax2.set_title('Median Sale Price', fontweight='bold'); ax2.set_ylabel('Million AED')

ax3 = axes[2]
offplan_daily = (sales_clean.assign(is_offplan=sales_clean['IS_OFFPLAN_EN'] == 'Off-Plan')
                 .groupby('date')['is_offplan'].mean().mul(100).rolling(14, min_periods=1).mean())
ax3.plot(offplan_daily.index, offplan_daily.values, color='#C44E52', lw=2)
ax3.axvline(CONFLICT_DATE, color='red', linestyle='--', lw=1.2, label='Conflict marker')
ax3.axhline(50, color='gray', linestyle=':', lw=1)
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.setp(ax3.get_xticklabels(), rotation=30, ha='right')
ax3.set_title('Off-Plan Share % (14-day rolling)', fontweight='bold')
ax3.set_ylabel('Off-Plan %'); ax3.legend()
plt.tight_layout()
savefig('fig11_offplan_vs_ready.png')

# ── Fig 12: Room configuration ────────────────────────────────────────────────
units_sales = sales_clean[sales_clean['PROP_TYPE_EN'] == 'Unit'].copy()
room_order = ['Studio', '1 B/R', '2 B/R', '3 B/R', '4 B/R', '5 B/R', '6 B/R']
room_counts = units_sales['ROOMS_EN'].value_counts().reindex([r for r in room_order if r in units_sales['ROOMS_EN'].values])

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].bar(room_counts.index, room_counts.values, color='#4C72B0', alpha=0.85)
axes[0].set_title('Unit Sales by Bedroom Configuration', fontweight='bold')
axes[0].set_xlabel('Bedroom Type'); axes[0].set_ylabel('Number of Sales')
for i, v in enumerate(room_counts.values):
    axes[0].text(i, v + 50, f'{v:,}', ha='center', fontsize=9)

room_price = units_sales[units_sales['ROOMS_EN'].isin(room_order)].groupby('ROOMS_EN')['price_m'].median().reindex(room_order).dropna()
axes[1].bar(room_price.index, room_price.values, color='#DD8452', alpha=0.85)
axes[1].set_title('Median Sale Price by Bedroom Type (M AED)', fontweight='bold')
axes[1].set_xlabel('Bedroom Type'); axes[1].set_ylabel('Median Price (Million AED)')
for i, v in enumerate(room_price.values):
    axes[1].text(i, v + 0.02, f'{v:.2f}M', ha='center', fontsize=9)
plt.tight_layout()
savefig('fig12_room_configuration_analysis.png')

# ── Fig 13: Area vs price scatter ────────────────────────────────────────────
units_clean = units_sales[
    (units_sales['ACTUAL_AREA'] > 10) & (units_sales['ACTUAL_AREA'] < 1000) &
    (units_sales['price_m'] < 30)
].sample(min(5000, len(units_sales)), random_state=42)

fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(units_clean['ACTUAL_AREA'], units_clean['price_m'],
                     c=units_clean['price_per_sqm'].clip(0, 50000),
                     cmap='YlOrRd', alpha=0.4, s=15)
slope, intercept, r, p, _ = stats.linregress(units_clean['ACTUAL_AREA'], units_clean['price_m'])
x_line = np.linspace(units_clean['ACTUAL_AREA'].min(), units_clean['ACTUAL_AREA'].max(), 100)
ax.plot(x_line, slope * x_line + intercept, 'b-', lw=2, label=f'Linear fit (R²={r**2:.3f})')
plt.colorbar(scatter, ax=ax, label='Price per sqm (AED)')
ax.set_title('Property Area vs. Transaction Value (Unit Sales)', fontsize=13, fontweight='bold')
ax.set_xlabel('Actual Area (sqm)'); ax.set_ylabel('Transaction Value (Million AED)'); ax.legend()
savefig('fig13_area_vs_price_scatter.png')

# ── Fig 14: Correlation heatmap ───────────────────────────────────────────────
numeric_cols = {'TRANS_VALUE': 'Price (AED)', 'ACTUAL_AREA': 'Area (sqm)',
                'PROCEDURE_AREA': 'Proc. Area', 'price_per_sqm': 'Price/sqm',
                'TOTAL_BUYER': 'Buyers', 'TOTAL_SELLER': 'Sellers'}
corr_matrix = sales_clean[list(numeric_cols.keys())].rename(columns=numeric_cols).corr()
fig, ax = plt.subplots(figsize=(8, 6))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            vmin=-1, vmax=1, linewidths=0.5, ax=ax, mask=mask)
ax.set_title('Correlation Matrix — Numeric Features (Sales)', fontsize=13, fontweight='bold')
plt.tight_layout()
savefig('fig14_correlation_heatmap.png')

# ── Fig 15: Price by nearest metro ───────────────────────────────────────────
metro_price = (sales_clean[sales_clean['NEAREST_METRO_EN'].notna()]
               .groupby('NEAREST_METRO_EN').filter(lambda x: len(x) >= 100)
               .groupby('NEAREST_METRO_EN')
               .agg(median_price=('price_m', 'median'), count=('price_m', 'count'))
               .sort_values('median_price', ascending=False).head(12).reset_index())
fig, ax = plt.subplots(figsize=(11, 7))
bars = ax.barh(metro_price['NEAREST_METRO_EN'][::-1], metro_price['median_price'][::-1], color='#8172B2', alpha=0.85)
ax.bar_label(bars, labels=[f'{v:.1f}M ({n:,})' for v, n in
             zip(metro_price['median_price'][::-1], metro_price['count'][::-1])],
             padding=4, fontsize=9)
ax.set_title('Median Sale Price by Nearest Metro Station\n(top 12, min 100 sales each)', fontsize=13, fontweight='bold')
ax.set_xlabel('Median Transaction Value (Million AED)')
savefig('fig15_price_by_metro.png')

# ── Fig 16: Monthly summary ───────────────────────────────────────────────────
monthly = sales_clean.groupby('month').agg(
    count=('TRANS_VALUE', 'count'), total_value=('TRANS_VALUE', 'sum'),
    median_price=('price_m', 'median'),
    offplan_share=('IS_OFFPLAN_EN', lambda x: (x == 'Off-Plan').mean() * 100)
).reset_index()
monthly['month_label'] = monthly['month'].dt.strftime('%b %Y')
monthly['total_value_b'] = monthly['total_value'] / 1_000_000_000

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes[0, 0].bar(monthly['month_label'], monthly['count'], color='#4C72B0', alpha=0.85)
for i, v in enumerate(monthly['count']): axes[0, 0].text(i, v + 50, f'{v:,}', ha='center', fontsize=9, fontweight='bold')
axes[0, 0].set_title('Monthly Sales Count', fontweight='bold'); axes[0, 0].set_ylabel('Transactions')

axes[0, 1].bar(monthly['month_label'], monthly['total_value_b'], color='#55A868', alpha=0.85)
for i, v in enumerate(monthly['total_value_b']): axes[0, 1].text(i, v + 0.05, f'{v:.1f}B', ha='center', fontsize=9, fontweight='bold')
axes[0, 1].set_title('Monthly Total Transaction Value (B AED)', fontweight='bold'); axes[0, 1].set_ylabel('Billion AED')

axes[1, 0].plot(monthly['month_label'], monthly['median_price'], marker='o', color='#C44E52', lw=2)
axes[1, 0].fill_between(monthly['month_label'], monthly['median_price'], alpha=0.15, color='#C44E52')
axes[1, 0].set_title('Monthly Median Sale Price (M AED)', fontweight='bold'); axes[1, 0].set_ylabel('Million AED')

axes[1, 1].bar(monthly['month_label'], monthly['offplan_share'], color='#DD8452', alpha=0.85)
axes[1, 1].axhline(50, color='gray', linestyle='--', lw=1, label='50% parity')
for i, v in enumerate(monthly['offplan_share']): axes[1, 1].text(i, v + 0.5, f'{v:.1f}%', ha='center', fontsize=9)
axes[1, 1].set_title('Monthly Off-Plan Share (%)', fontweight='bold'); axes[1, 1].set_ylabel('Off-Plan %'); axes[1, 1].legend()

plt.suptitle('Monthly Market Summary — Dubai Real Estate Sales (Feb–Apr 2026)', fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
savefig('fig16_monthly_summary.png')

print('\nAll figures generated successfully!')
print(f'Output directory: {FIGURES_DIR}')
print('Files:')
for f in sorted(os.listdir(FIGURES_DIR)):
    print(f'  {f}')
