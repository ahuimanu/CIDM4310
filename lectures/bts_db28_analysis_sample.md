# DB28 Exploratory Analysis — From Counts to Insights

## 1. Context
Dataset: T-100 Domestic Segment (DB28)
Fields: YEAR, MONTH, CARRIER, ORIGIN, DEST, PASSENGERS, FLIGHTS, DISTANCE, RPM, ASM

Objective: Move past .describe() into interpretive analytics — patterns, ratios, and insights that hint at business questions.

---

## 2. Analysis Focus
We’ll explore three escalating BI questions:

| Level | Question | Technique |
|:--|:--|:--|
| A | Which carriers dominate total passenger traffic? | Group & aggregate |
| B | What is the relationship between distance and load factor? | Derived metrics + scatter correlation |
| C | Which routes show under- or over-utilization? | KPI benchmarking + conditional filters |

---

## 3. Representative Code Blocks

### A. Carrier Market Shares
``` python
carrier_pax = (
    df.groupby('CARRIER')['PASSENGERS']
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)
carrier_pax['SHARE'] = carrier_pax['PASSENGERS'] / carrier_pax['PASSENGERS'].sum()
carrier_pax.head(10)
```

Interpretation: Concentration insight (e.g., top 5 carriers hold ~80% of traffic).
Potential teaching point: Industry consolidation and market dominance.

---

### B. Distance vs. Load Factor
``` python
df['LOAD_FACTOR'] = df['RPM'] / df['ASM']
subset = df[['DISTANCE','LOAD_FACTOR']].dropna()
subset.plot.scatter(x='DISTANCE', y='LOAD_FACTOR', alpha=0.3)
subset.corr()
```

Interpretation:
- Positive correlation → long-haul efficiency.
- Flat/negative correlation → regional saturation or operational imbalance.
Teaching point: Introduces relationship testing and efficiency analysis.

---

### C. Route Utilization Benchmark
``` python
route_summary = (
    df.groupby(['ORIGIN','DEST'])
      .agg(PAX=('PASSENGERS','sum'),
           FLIGHTS=('FLIGHTS','sum'),
           DIST=('DISTANCE','mean'),
           ASM=('ASM','sum'),
           RPM=('RPM','sum'))
      .reset_index()
)
route_summary['LOAD_FACTOR'] = route_summary['RPM'] / route_summary['ASM']
mean_lf = route_summary['LOAD_FACTOR'].mean()
route_summary['PERF_VS_AVG'] = route_summary['LOAD_FACTOR'] - mean_lf
```

# Highlight top and bottom routes by performance
``` python
over_under = {
    'Underperformers': route_summary.sort_values('PERF_VS_AVG').head(5),
    'Outperformers': route_summary.sort_values('PERF_VS_AVG', ascending=False).head(5)
}
```

Interpretation: Identify inefficient or standout routes — a foundation for network decisions and profit optimization.

---

## 4. Discussion Points
- Does higher distance always yield better load factors? Why or why not?
- What structural or market factors could explain route underperformance?
- How would seasonal demand or aircraft assignment affect these metrics?

---

## 5. Teaching Summary
Concept Progression
1. Aggregation → Ranking: Market structure insight.
2. Derived Ratios → Relationships: Efficiency vs. scale.
3. Benchmarking → Performance Classification: Actionable insights.

BI Linkage
Moves from what happened → why it happened → what to do next.

---

## 6. Optional Extensions
- Add trend analysis by month to spot seasonality.
- Join with ASQP data to relate reliability to load factor.
- Calculate route yield: FARE_PER_MILE = REVENUE / DISTANCE (if available).

---

## 7. Deliverable
Notebook: notebooks/bts_db28_analysis_sample.ipynb
Includes cells, visualizations, and narrative Markdown matching this outline.