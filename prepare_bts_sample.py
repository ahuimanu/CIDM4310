"""
prepare_bts_sample.py — Minimal helper utilities to ingest BTS files and curate teaching samples.
Python-only (no bash). Assumes URLs from BTS PREZIP or local CSV paths.

Usage pattern (inside a notebook):
    from notebooks._helpers.prepare_bts_sample import fetch_zip_to, extract_zip, load_trim_save

    # Example for DB28 CSV already downloaded:
    load_trim_save(
        src_csv="data/bts_ingest/T100_segment_2025_01.csv",
        dst_csv="data/bts_samples/t100_segment_sample.csv",
        columns=["YEAR","MONTH","CARRIER","ORIGIN","DEST","FLIGHTS","PASSENGERS","DISTANCE","ASM","RPM"],
        filters={"YEAR":[2025], "MONTH":[1,2,3], "CARRIER": None}  # None means no filter
    )
"""
from __future__ import annotations
import os, io, csv, json, typing as t
import zipfile
from dataclasses import dataclass

import pandas as pd

@dataclass
class IngestConfig:
    src_csv: str
    dst_csv: str
    columns: t.List[str]
    filters: t.Dict[str, t.Optional[t.List[t.Union[str,int,float]]]]

def ensure_dir(p: str) -> None:
    os.makedirs(os.path.dirname(p), exist_ok=True)

def fetch_zip_to(url: str, dst_zip_path: str) -> str:
    """
    Download a ZIP file from BTS PREZIP to a local path.
    Note: requires internet; wrap in try/except in your notebook.
    """
    import requests
    ensure_dir(dst_zip_path)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dst_zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return dst_zip_path

def extract_zip(zip_path: str, dst_dir: str) -> t.List[str]:
    """Extract all files; return list of extracted file paths."""
    ensure_dir(os.path.join(dst_dir, "_placeholder"))
    out_paths = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            target = os.path.join(dst_dir, os.path.basename(name))
            with zf.open(name) as src, open(target, "wb") as dst:
                dst.write(src.read())
            out_paths.append(target)
    return out_paths

def load_trim_save(src_csv: str, dst_csv: str, columns: t.List[str], filters: t.Dict[str, t.Optional[t.List[t.Union[str,int,float]]]]) -> str:
    """
    Load a (possibly large) CSV, select columns and filters, and write to a smaller CSV.
    """
    ensure_dir(dst_csv)
    usecols = columns
    df_iter = pd.read_csv(src_csv, usecols=usecols, low_memory=False, chunksize=250_000)
    frames = []
    for chunk in df_iter:
        # Apply filters
        for col, allowed in (filters or {}).items():
            if allowed is None or col not in chunk.columns:
                continue
            chunk = chunk[chunk[col].isin(allowed)]
        frames.append(chunk)
    if not frames:
        pd.DataFrame(columns=columns).to_csv(dst_csv, index=False)
        return dst_csv
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(dst_csv, index=False)
    return dst_csv
