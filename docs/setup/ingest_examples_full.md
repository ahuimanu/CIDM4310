# In-Notebook Ingest Patterns (DB28, ASQP, DB1B) — 2025 Q1 & June 2025

## DB28 — T-100 Segment (Supply & Movement)
``` python
    from notebooks._helpers.prepare_bts_sample import load_trim_save

    src_csv = "data/bts_ingest/T100_segment_2025_01.csv"      # Jan 2025 example
    dst_csv = "data/bts_samples/t100_segment_sample.csv"

    columns = ["YEAR","MONTH","CARRIER","ORIGIN","DEST","FLIGHTS","PASSENGERS","DISTANCE","ASM","RPM"]
    filters = {"YEAR":[2025], "MONTH":[1,2,3], "CARRIER": None}   # Q1; use {"MONTH":[6]} for June

    _ = load_trim_save(src_csv, dst_csv, columns, filters)
```

---
``` python
## ASQP — On-Time Performance (Reliability)
    from notebooks._helpers.prepare_bts_sample import load_trim_save

    src_csv = "data/bts_ingest/ASQP_2025_01.csv"
    dst_csv = "data/bts_samples/asqp_sample.csv"

    columns = ["YEAR","MONTH","CARRIER","ORIGIN","DEST",
               "DEP_DELAY","ARR_DELAY","CANCELLED","DIVERTED","AIR_TIME"]
    filters = {"YEAR":[2025], "MONTH":[1,2,3], "CARRIER": None}

    _ = load_trim_save(src_csv, dst_csv, columns, filters)
```
---

## DB1B — O&D Survey (Demand & Fares)
``` python
    from notebooks._helpers.prepare_bts_sample import load_trim_save

    src_csv = "data/bts_ingest/DB1B_2025_Q1.csv"
    dst_csv = "data/bts_samples/db1b_sample.csv"

    columns = ["YEAR","QUARTER","ORIGIN","DEST","PASSENGERS","FARE","DISTANCE"]
    filters = {"YEAR":[2025], "QUARTER":[1]}

    _ = load_trim_save(src_csv, dst_csv, columns, filters)
```
---

## PREZIP Pattern (any dataset)
``` python
    from notebooks._helpers.prepare_bts_sample import fetch_zip_to, extract_zip, load_trim_save

    url = "<PASTE_PREZIP_ZIP_URL>"
    zip_path = "data/bts_ingest/sample.zip"
    csv_dir = "data/bts_ingest"

    fetch_zip_to(url, zip_path)
    extracted = extract_zip(zip_path, csv_dir)
    src_csv = next((p for p in extracted if p.lower().endswith(".csv")), None)

    load_trim_save(src_csv, "data/bts_samples/sample.csv", columns, filters)
```
---

### Notes
- Column names can vary by vintage (e.g., OP_CARRIER); adjust as needed.  
- Keep raw files in data/bts_ingest/ and curated classroom slices in data/bts_samples/.  
- For June 2025 use {"YEAR":[2025], "MONTH":[6]} for DB28/ASQP.  
- DB1B is quarterly — use {"YEAR":[2025], "QUARTER":[1]} for 2025 Q1.