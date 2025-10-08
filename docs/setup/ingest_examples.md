# In-Notebook Data Ingest Examples (DB28 / T-100)
Purpose: demonstrate two reliable patterns to bring BTS DB28 data into your class notebook and curate a small teaching CSV.

## A) Trim a Locally-Available CSV (fastest path)
from notebooks._helpers.prepare_bts_sample import load_trim_save

# Example: collapse a large DB28 CSV to a small, filtered teaching set.
src_csv = "data/bts_ingest/T100_segment_2025_01.csv"   # <-- update to your raw file
dst_csv = "data/bts_samples/t100_segment_sample.csv"

columns = ["YEAR","MONTH","CARRIER","ORIGIN","DEST","FLIGHTS","PASSENGERS","DISTANCE","ASM","RPM"]
filters = {"YEAR":[2025], "MONTH":[1,2,3], "CARRIER": None}   # Q1 example; set to [6] for June

_ = load_trim_save(src_csv=src_csv, dst_csv=dst_csv, columns=columns, filters=filters)
print("Wrote sample:", dst_csv)

## B) Fetch from BTS PREZIP → Extract → Trim
from notebooks._helpers.prepare_bts_sample import fetch_zip_to, extract_zip, load_trim_save
import os

# 1) Paste a valid PREZIP ZIP URL for T-100 Segment monthly data
#    (Find it at https://transtats.bts.gov/PREZIP/ — filenames vary by month.)
prezip_url = "<PASTE_T100_SEGMENT_PREZIP_URL_ZIP>"   # <-- replace with the actual ZIP URL
zip_path = "data/bts_ingest/t100_segment_2025_01.zip"
csv_dir = "data/bts_ingest"

try:
    fetch_zip_to(prezip_url, zip_path)
    extracted = extract_zip(zip_path, csv_dir)
    print("Extracted:", extracted)

    # 2) Choose the extracted CSV (assumes first CSV is the DB28 file)
    src_csv = next((p for p in extracted if p.lower().endswith(".csv")), None)
    if not src_csv:
        raise FileNotFoundError("No CSV found in ZIP. Check the PREZIP URL.")

    # 3) Trim to a small teaching sample (June 2025 example)
    columns = ["YEAR","MONTH","CARRIER","ORIGIN","DEST","FLIGHTS","PASSENGERS","DISTANCE","ASM","RPM"]
    filters = {"YEAR":[2025], "MONTH":[6], "CARRIER": None}
    dst_csv = "data/bts_samples/t100_segment_sample.csv"

    load_trim_save(src_csv=src_csv, dst_csv=dst_csv, columns=columns, filters=filters)
    print("Wrote sample:", dst_csv)
except Exception as e:
    print("NOTE:", e)
    print("This example requires a valid PREZIP URL and internet access.")

## Notes & Guardrails
- Keep raw files in data/bts_ingest/ and curated teaching slices in data/bts_samples/.
- Always constrain columns and time windows to keep class runs fast and deterministic.
- If DB28 column names differ across vintages, adjust the columns list accordingly.
- For full 2025Q1 + June 2025 runs, repeat the trim step per month (Jan–Mar and Jun).

## Helper Module
A minimal helper is available at notebooks/_helpers/prepare_bts_sample.py with:
- fetch_zip_to(url, dst_zip_path): download a PREZIP ZIP (requires internet).
- extract_zip(zip_path, dst_dir): extract all files; returns extracted paths.
- load_trim_save(src_csv, dst_csv, columns, filters): column- and filter-aware curating.