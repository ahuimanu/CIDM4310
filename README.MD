# CIDM 5310 Repo

## Fall 2025
## What's Here?

- BTS Data Examples

# Environment Setup for BTS Data Analysis

## 1. Overview
These notebooks (DB28 / ASQP / DB1B) use public BTS aviation data for descriptive and BI analysis.  
You’ll need a clean Python 3.10+ environment with a few data science libraries installed.

---

## 2. Install Required Packages
Use pip or conda to install the core stack.

```bash
pip install pandas numpy matplotlib pyarrow openpyxl
```

**Recommended additions:**
```bash
pip install notebook ipykernel seaborn
```

| Purpose | Package | Notes |
|:--|:--|:--|
| DataFrames & math | pandas, numpy | Core data handling |
| Plotting | matplotlib | Default visualization |
| Parquet I/O | pyarrow | Needed for fast binary data |
| Excel/CSV I/O | openpyxl | Optional, but useful |
| Notebooks | notebook, ipykernel | Run interactively |
| Optional styling | seaborn | Prettier default plots |

---

## 3. Folder Layout
```
notebooks/
    bts_db28_analysis_sample.ipynb
    bts_ba_basics.ipynb
data/
    bts_samples/
    bts_ingest/
docs/
    lectures/
    setup/
```

- **`bts_samples/`** → small curated CSVs used for teaching.
- **`bts_ingest/`** → location for full quarterly ingests (DB28, ASQP, DB1B).

---

## 4. Planned Data Ingest (2025Q1 + June 2025)
The upcoming full ingest will include:
- **DB28 (T-100 Segment & Market)** — 2025Q1 + June 2025 update.
- **ASQP (On-Time Performance)** — same period for reliability metrics.
- **DB1B (O&D Survey)** — 2025Q1 release for fare/demand analytics.

Each dataset will be downloaded from the **BTS PREZIP endpoints** and harmonized into SQLite or Parquet for reproducible analysis.

```bash
# Example BTS links
https://transtats.bts.gov/PREZIP/
```

---

## 5. Next Steps
1. Confirm Python environment is active (`python --version`).
2. Run `jupyter notebook notebooks/bts_db28_analysis_sample.ipynb`.
3. Validate sample CSVs load successfully before full ingest.
4. Prepare storage for ~3–5 GB of raw CSVs after full 2025 ingest.

