# CPB — Jupyter Notebook: BTS Data Basics (DF Loading & Descriptives)
# Version: 0.1.0  | Owner: <YOU>  | Status: Draft (ready to execute)
# Intent
#   Produce a beginner-friendly Jupyter notebook that demonstrates loading U.S. BTS aviation data
#   into pandas DataFrames and running core descriptive summaries. The notebook will serve as a
#   teaching artifact for DataFrame fundamentals (schema peek, row counts, NA audit, basic stats,
#   groupby, simple plots) using real aviation data (e.g., T-100, DB1B, ASQP).
#
# Outcomes
#   1) A single, polished notebook: notebooks/bts_df_basics.ipynb
#   2) Local sample data (small, clean slices) in data/bts_samples/ (CSV + README)
#   3) A reproducibility stub (Python-only) that can fetch/prepare data OR clearly points to
#      already-provisioned sample CSVs.
#
# Audience & Pedagogy
#   - Students and colleagues learning pandas with credible, real-world aviation data.
#   - Focus on clarity: short cells, tight headings, few dependencies, no magic.
#
# Scope (MVP)
#   - Data sources (choose one primary set for MVP; others optional links):
#       - T-100 Segment or Market (domestic slice is fine)
#       - OR DB1B (Quarterly O&D sample)
#       - OR ASQP (on-time performance fields)
#   - Notebook sections:
#       A. Title & context (what dataset is this, high-level caveats)
#       B. Environment check (Python, pandas, matplotlib, pyarrow if used)
#       C. Data acquisition (either “load from data/bts_samples/*.csv” or small scripted fetch)
#       D. Load into DataFrames (dtype control, memory notes)
#       E. Peek & schema (head(), info(), dtypes, shape)
#       F. Data hygiene (NA counts, basic imputations if educational)
#       G. Descriptives (describe(), value_counts(), unique(), simple groupby)
#       H. Mini EDA (one or two plots: hist or bar; matplotlib only, no style overrides)
#       I. Save artifacts (optionally write a tiny summary CSV)
#       J. “What we learned” (bullet recap + next steps)
#
# Non-Goals (MVP)
#   - No advanced modeling, no geospatial, no heavy joins across multiple quarters/years.
#   - No big downloads during class time; prefer small curated samples for teaching.
#
# Data Strategy
#   - Preferred: ship a few pre-curated CSVs in data/bts_samples/ (≤ 5–10 MB total).
#       * Include data/bts_samples/README.md explaining source, time window, fields kept, filters.
#   - Alternate (optional): a helper script notebooks/_helpers/prepare_bts_sample.py that:
#       * Downloads a small file (or reads from a larger local source),
#       * Selects a few columns,
#       * Filters to a small time window,
#       * Writes the teaching CSVs to data/bts_samples/.
#   - Keep columns minimal and meaningful (e.g., YEAR, QUARTER, ORIGIN, DEST, PASSENGERS, RPM, ASM).
#
# Tech Guardrails
#   - Python-only (no bash); keep dependencies minimal:
#       * pandas, pyarrow (optional if Parquet), matplotlib
#   - Plots: matplotlib only, one chart per cell, do not set custom colors or global styles.
#   - Notebook must run top-to-bottom without edits on a fresh env.
#   - File paths relative to repo root (assume notebook lives in notebooks/).
#
# File/Folder Layout
#   - notebooks/
#       - bts_df_basics.ipynb                 # the teaching notebook
#       - _helpers/prepare_bts_sample.py      # optional tiny prep script
#   - data/
#       - bts_samples/
#           - t100_segment_sample.csv         # or db1b_sample.csv / asqp_sample.csv
#           - README.md                       # provenance + columns + filters
#
# Content Requirements (Notebook)
#   - Title cell with dataset name, months/quarters covered, and one-paragraph context.
#   - “Setup” cell: import, version printouts (pandas.__version__), path constants.
#   - “Load” cell(s): pd.read_csv(..., dtype=...), low_memory=False notes as needed.
#   - “Peek” cell(s): df.shape, df.head(3), df.info(), df.dtypes
#   - “Hygiene” cell(s): df.isna().sum().sort_values(), quick fill or drop explained briefly.
#   - “Descriptives” cell(s): df.describe(include='all'), value_counts() of a key dimension
#   - “Groupby examples”:
#       * Simple total by ORIGIN (top 10)
#       * Simple route-level summary (if both ORIGIN/DEST exist)
#   - “Mini EDA”:
#       * Histogram of a numeric column (e.g., PASSENGERS)
#       * Bar chart of top N routes or airports
#   - “Export” cell (optional): write a small CSV of a summary table (e.g., top routes)
#   - “Recap & Next Steps” markdown cell: 5–8 bullets
#
# Acceptance Criteria (Definition of Done)
#   - ✅ Repo contains the files/folders listed above.
#   - ✅ Notebook executes end-to-end on a clean environment and finishes in < 30s on typical laptop.
#   - ✅ No external secrets or tokens required; data loads from data/bts_samples/ by default.
#   - ✅ Plots render and are legible with default matplotlib style; no custom styles/colors.
#   - ✅ Clear explanations accompany each major step (1–3 sentences per block).
#   - ✅ data/bts_samples/README.md documents provenance, filters, and retained columns.
#
# Data Provenance Notes (fill in when selecting the dataset)
#   - Dataset: <T-100 Segment | T-100 Market | DB1B | ASQP>
#   - Time Window: <e.g., 2023Q1 only>  (keep small)
#   - Columns kept: <list>
#   - Filters applied: <e.g., domestic only, top 20 airports, etc.>
#   - Source page(s): <high-level description or reference; avoid bare URLs in the notebook>
#
# Risks & Mitigations
#   - Risk: Students’ machines differ → Provide tiny CSVs and avoid heavy dependencies.
#   - Risk: Column drift across BTS vintages → Lock sample columns in README; show dtype setting.
#   - Risk: Run-order errors → Keep execution linear; no hidden state or side-effect cells.
#
# Review Checklist (Mentor/Owner sign-off)
#   - Content clarity (novice-friendly, minimal jargon)
#   - Repro (fresh env run passes)
#   - Data ethics (public, licensed, cited at high level)
#   - Pedagogical flow (each section has a purpose)
#
# Next Iterations (post-MVP, optional)
#   - Add Parquet sample & dtype discussion (memory/perf)
#   - Add simple join example (e.g., map airport names)
#   - Add seaborn/altair “compare & contrast” (separate notebook)
#
# Execution Notes
#   - Keep the notebook small and reliable; resist scope creep.
#   - Prefer curated sample files over live, full-data downloads in class contexts.
#   - No pytest; if tests are desired later, use unittest for any helper scripts (separate from the notebook).
#
# Sign-off
#   - Owner: <name/date>
#   - Reviewer: <name/date>