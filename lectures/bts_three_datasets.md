# BTS Datasets Overview: DB28, ASQP, and DB1B for BI & Descriptives
**Duration:** 45–60 minutes  
**Goal:** Show how different BTS datasets illuminate distinct layers of airline performance—operations, reliability, and markets.  
**Libraries:** `pandas`, `numpy`, `matplotlib`

---

## 1. The Big Picture
The U.S. Bureau of Transportation Statistics (BTS) maintains multiple public datasets that, together, allow analysts to trace how an airline **operates**, **performs**, and **competes**.  
In BI/BA workflows, we often use:

| Dataset | Core Theme | Perspective | Typical Level |
|:--|:--|:--|:--|
| **T-100 / DB28** | Operations & Capacity | Supply | Flight Segment / Market |
| **ASQP** | Reliability & Service Quality | Execution | Individual Flight |
| **DB1B** | Demand & Fares | Economic | O&D Market Sample |

Each serves as a “layer” in the airline data stack.

---

## 2. DB28 (T-100 Segment / Market) — *Supply & Movement*
**Purpose:** Measure operational throughput and capacity utilization.

**Fields (typical):**  
`YEAR, MONTH, CARRIER, ORIGIN, DEST, FLIGHTS, SEATS, PASSENGERS, DISTANCE, ASM, RPM`

**Analytical Targets:**
- Flights or passengers by carrier, airport, or route  
- Load factor (`RPM / ASM`)  
- Average passengers per flight  
- Stage length and network concentration

**Code Illustrations:**
```python
# Aggregates and ratios
df.groupby('CARRIER')['PASSENGERS'].sum().sort_values(ascending=False)
df['LOAD_FACTOR'] = df['RPM'] / df['ASM']
df['AVG_PAX_PER_FLIGHT'] = df['PASSENGERS'] / df['FLIGHTS']
df[['LOAD_FACTOR','AVG_PAX_PER_FLIGHT']].describe()
```

**Key BI Takeaways:**
- Reflects airline *capacity strategy* and *utilization efficiency*.
- Excellent for network visualization and route-level dashboards.

---

## 3. ASQP — *Operational Reliability*
**Purpose:** Track on-time performance, cancellations, and delays.

**Fields (typical):**  
`YEAR, MONTH, CARRIER, ORIGIN, DEST, DEP_DELAY, ARR_DELAY, CANCELLED, DIVERTED, AIR_TIME`

**Analytical Targets:**
- On-time performance (`ARR_DELAY ≤ 15`)  
- Average arrival/departure delay  
- Cancellation and diversion rates  
- Seasonal or airport-specific reliability

**Code Illustrations:**
```python
df['ON_TIME'] = (df['ARR_DELAY'] <= 15)
df.groupby('CARRIER')['ON_TIME'].mean().sort_values(ascending=False)
df['ARR_DELAY'].hist(bins=40); plt.title("Arrival delay distribution")
```

**Key BI Takeaways:**
- Evaluates *execution reliability* and *customer experience*.
- Enables comparisons across carriers, airports, and months.

---

## 4. DB1B (Origin–Destination Survey) — *Demand & Fares*
**Purpose:** Capture economic behavior and fare structures in passenger markets.

**Fields (typical):**  
`YEAR, QUARTER, ORIGIN, DEST, PASSENGERS, FARE, DISTANCE`

**Analytical Targets:**
- Average fare by distance band or carrier  
- Market concentration (Herfindahl-Hirschman Index concept)  
- Fare per mile and elasticity approximations

**Code Illustrations:**
```python
df['FARE_PER_MILE'] = df['FARE'] / df['DISTANCE']
df.groupby('CARRIER')['FARE_PER_MILE'].mean()
df.plot.scatter(x='DISTANCE', y='FARE', alpha=0.3)
```

**Key BI Takeaways:**
- Connects *price sensitivity* with *network geography*.
- Supports yield and market share analyses.

---

## 5. Suggested Teaching Flow

| Step | Dataset | Focus | Duration | Example KPI |
|:--|:--|:--|:--|:--|
| 1 | **DB28** | Operations (supply, load factor) | 20 min | Load Factor, Flights per Carrier |
| 2 | **ASQP** | Reliability (delays, cancellations) | 15 min | On-Time %, Avg Delay |
| 3 | **DB1B** | Market Demand & Fares | 15 min | Avg Fare, Fare per Mile |

Each step builds on the same Pandas workflow:
1. Load → 2. Peek → 3. Clean → 4. Aggregate → 5. Visualize

---

## 6. Cross-Dataset Integration Ideas
- **Join DB28 + ASQP** → operational reliability vs capacity utilization.  
  *Example:* correlate load factor and on-time rate by carrier.
- **Join DB28 + DB1B** → supply vs demand strength.  
  *Example:* high-fare, high-load markets.
- **Triangulate all three** → full performance triad (capacity, reliability, yield).

```python
merged = db28.merge(asqp, on=['YEAR','MONTH','CARRIER','ORIGIN','DEST'], how='inner')
merged[['LOAD_FACTOR','ON_TIME']].corr()
```

---

## 7. Practical Guidance
- Work on **curated sample CSVs** (≤10 MB each) for speed and consistency.  
- Normalize key identifiers (`CARRIER`, `ORIGIN`, `DEST`) to uppercase strings.  
- Add README files describing filters and retained columns.  
- Keep each notebook under 15 cells for class readability.  

---

## 8. Wrap-Up Discussion Prompts
- How do *supply* (DB28) and *demand* (DB1B) differ conceptually?  
- Why is *on-time performance* (ASQP) valuable even if load factors are high?  
- Which dataset would you consult first for:  
  - network planning?  
  - marketing strategy?  
  - reliability benchmarking?

---

## 9. Deliverables
- **notebooks/**
  - `bts_db28_basics.ipynb`  
  - `bts_asqp_basics.ipynb`  
  - `bts_db1b_basics.ipynb`
- **data/bts_samples/**
  - Small CSVs (each ≤ 10 MB)
- **docs/lectures/**
  - This file → `bts_three_datasets.md`

---

## 10. Next Step (optional extensions)
- Convert aggregated summaries to dashboards in Power BI or Tableau.  
- Build correlation and regression notebooks (distance vs fare, load vs delay).  
- Introduce Parquet conversion to show storage efficiency.