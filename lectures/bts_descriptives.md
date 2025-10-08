# BTS Data in Pandas: Descriptives & BI Warm-ups
**Duration:** 35–45 minutes · **Dataset:** BTS T-100 Segment (domestic slice)  
**Audience:** Intro BA/BI with Python · **Dependencies:** pandas, numpy, matplotlib

---

## Learning Objectives
- Load a realistic aviation dataset into a DataFrame with sensible dtypes.
- Run first-pass descriptives (shape, schema, NA/dupes, distributions).
- Build a few business-meaningful KPIs (load factor, passengers/flight).
- Produce simple, readable plots (matplotlib) without styling.

## Assumptions (Fields)
We’ll assume these columns exist:  
`YEAR, MONTH, CARRIER, ORIGIN, DEST, FLIGHTS, PASSENGERS, DISTANCE, RPM, ASM`

---

## 0) Setup (2–3 min)
```python
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
pd.__version__, np.__version__
```
```python
# Update path as needed (small, curated CSV)
PATH = "data/bts_samples/t100_segment_sample.csv"
df = pd.read_csv(PATH, low_memory=False)
```

---

## 1) Data Familiarization (4–5 min)
```python
df.shape, df.columns.tolist()
```
```python
df.info()
```
```python
df.head(3)
```
```python
df.dtypes.value_counts()
```
**Instructor notes:** Call out object vs numeric; highlight likely cast targets (e.g., YEAR, MONTH to int16).

---

## 2) Basic Hygiene (5 min)
```python
df.isna().sum().sort_values(ascending=False).head(10)
```
```python
df.duplicated().sum()
```
```python
df.select_dtypes(include="number").describe()
```
**Instructor notes:** Decide whether to drop or fill; show one tiny, explicit fix:
```python
# Example: replace negative/implausible DISTANCE with NaN (if present), then drop
df.loc[df['DISTANCE'] <= 0, 'DISTANCE'] = np.nan
df = df.dropna(subset=['DISTANCE', 'FLIGHTS', 'PASSENGERS'])
```

---

## 3) Univariate Distributions (5 min)
```python
df['PASSENGERS'].hist(bins=30); plt.title("Passenger distribution"); plt.show()
```
```python
df['DISTANCE'].plot(kind='box'); plt.title("Stage length (boxplot)"); plt.show()
```
```python
df['CARRIER'].value_counts().head(10)
```
**Instructor notes:** Skewness is common; boxplot hints at outliers/long-haul tails.

---

## 4) BI-Flavored Aggregations (6–7 min)
```python
df.groupby('CARRIER')['PASSENGERS'].sum().sort_values(ascending=False).head(10)
```
```python
df.groupby('ORIGIN')['FLIGHTS'].sum().nlargest(10)
```
```python
route_summary = (
    df.groupby(['ORIGIN','DEST'])
      .agg(PAX=('PASSENGERS','sum'), FLIGHTS=('FLIGHTS','sum'), DIST=('DISTANCE','mean'))
      .reset_index()
)
route_summary.head(10)
```
**Instructor notes:** Interpret: traffic concentration, airport intensity, key routes.

---

## 5) Derived Metrics & Ratios (6–7 min)
```python
df['LOAD_FACTOR'] = df['RPM'] / df['ASM']
df['AVG_PAX_PER_FLIGHT'] = df['PASSENGERS'] / df['FLIGHTS']
df[['LOAD_FACTOR','AVG_PAX_PER_FLIGHT']].describe()
```
```python
# Network-level weighted average stage length (by passengers)
avg_stage_len = (df['DISTANCE'] * df['PASSENGERS']).sum() / df['PASSENGERS'].sum()
avg_stage_len
```
**Instructor notes:** Tie each ratio to business meaning (utilization, productivity).

---

## 6) Temporal Trend (optional, 4–5 min)
```python
df['DATE'] = pd.to_datetime(df['YEAR'].astype(str) + df['MONTH'].astype(str), format='%Y%m')
monthly = df.groupby('DATE')['PASSENGERS'].sum()
monthly.plot(); plt.title("Monthly passengers"); plt.show()
```
**Instructor notes:** Seasonality, disruptions, recovery curves.

---

## 7) Exploratory Correlations (3–4 min)
```python
df[['DISTANCE','PASSENGERS','LOAD_FACTOR','AVG_PAX_PER_FLIGHT']].corr()
```
**Instructor notes:** Emphasize *exploratory*; correlation ≠ causation.

---

## 8) Mini “Dashlet” Examples (3–4 min)
```python
top_carriers = df.groupby('CARRIER')['PASSENGERS'].sum().sort_values(ascending=False).head(5)
top_carriers.plot(kind='bar'); plt.title("Top carriers by passengers"); plt.tight_layout(); plt.show()
```
```python
top_routes = (route_summary.sort_values('PAX', ascending=False)
              .head(10)[['ORIGIN','DEST','PAX','FLIGHTS','DIST']])
top_routes
```
```python
df.plot.scatter(x='DISTANCE', y='LOAD_FACTOR', alpha=0.3); plt.title("Distance vs Load Factor"); plt.show()
```

---

## 9) Quick Numpy Checks (2–3 min)
```python
float(np.mean(df['PASSENGERS'])), np.percentile(df['DISTANCE'], [25, 50, 75])
```
```python
np.corrcoef(df['DISTANCE'], df['PASSENGERS'])
```

---

## 10) Save a Small Artifact (1–2 min)
```python
out = top_routes.copy()
out.to_csv("artifacts/top_routes_sample.csv", index=False)
```
**Instructor notes:** Close the loop—create a product students can hand off.

---

## Common Pitfalls & Guardrails
- **Mixed dtypes** in numeric columns → cast explicitly if needed (`pd.to_numeric(errors='coerce')`).
- **Divide-by-zero** in ratios (`FLIGHTS == 0`, `ASM == 0`) → filter or guard with `.replace(0, np.nan)`.
- **Plot readability** → one chart per cell; default matplotlib; no custom colors/styles.
- **Heavy files** → teach on small, curated slices (≤ 10 MB) for reliability.

---

## Exit Ticket (2 minutes)
- What’s the difference between *total passengers* and *average passengers per flight*?
- Why weight average stage length by passengers instead of a simple mean?
- Name one actionable question your dashboard could answer tomorrow.

---

## Next Steps (Homework)
- Join airport names (lookup table) to improve readability.
- Add a *carrier-route* heatmap **as a table** (no extra viz libs), sorted by passengers.
- Create a one-page memo: top 5 carriers, top 10 routes, and one KPI trend (one plot).

---

## Appendix: Minimal Dtype Tuning (optional)
```python
dtype_map = {
    'YEAR': 'int16', 'MONTH': 'int8', 'FLIGHTS': 'int32',
    'PASSENGERS': 'int32', 'DISTANCE': 'float32',
    'RPM': 'float32', 'ASM': 'float32'
}
df = pd.read_csv(PATH, dtype=dtype_map, low_memory=False)
```