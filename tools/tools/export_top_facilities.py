#!/usr/bin/env python3
"""
export_top_facilities.py

Input:  facility_rollup.csv (from export_facility_rollup_from_impacts.py)
Output: top_facilities.csv (sorted desc by total affected)

Robustness:
- Attempts to find facility id column and total affected column by common names.
- Falls back to "first numeric column" as totalAffected if needed.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from typing import Dict, List, Tuple, Optional


FACILITY_ID_CANDIDATES = ["facilityId", "facility_id", "facility", "site", "code"]
TOTAL_AFFECTED_CANDIDATES = ["totalAffected", "total_affected", "affectedTotal", "affected_total", "affected", "total"]


def _as_int(val: str) -> Optional[int]:
    if val is None:
        return None
    s = str(val).strip()
    if s == "":
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def detect_columns(fieldnames: List[str]) -> Tuple[str, str]:
    # facility id column
    lower_map = {f.lower(): f for f in fieldnames}

    facility_col = None
    for cand in FACILITY_ID_CANDIDATES:
        if cand.lower() in lower_map:
            facility_col = lower_map[cand.lower()]
            break

    # total affected column
    total_col = None
    for cand in TOTAL_AFFECTED_CANDIDATES:
        if cand.lower() in lower_map:
            total_col = lower_map[cand.lower()]
            break

    # Fallbacks
    if facility_col is None:
        # assume first column is facility identifier
        facility_col = fieldnames[0]

    if total_col is None:
        # pick the first column (not facility) that looks numeric in most rows later
        # for now choose the second column as a best guess, and validate while reading
        if len(fieldnames) < 2:
            raise ValueError("CSV does not have enough columns to infer totalAffected.")
        total_col = fieldnames[1]

    return facility_col, total_col


def read_rows(path: str) -> Tuple[List[Dict[str, str]], List[str]]:
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV appears to have no header row (fieldnames missing).")
        rows = list(reader)
        return rows, list(reader.fieldnames)


def choose_total_affected_column(rows: List[Dict[str, str]], fieldnames: List[str], facility_col: str, suggested_total_col: str) -> str:
    # If suggested_total_col is numeric for most rows, accept it.
    numeric_hits = 0
    total = 0
    for r in rows:
        if suggested_total_col not in r:
            continue
        total += 1
        if _as_int(r.get(suggested_total_col, "")) is not None:
            numeric_hits += 1
    if total > 0 and numeric_hits / total >= 0.8:
        return suggested_total_col

    # Otherwise find first column (excluding facility_col) that is numeric for most rows.
    best_col = None
    best_ratio = -1.0
    for col in fieldnames:
        if col == facility_col:
            continue
        hits = 0
        tot = 0
        for r in rows:
            if col not in r:
                continue
            tot += 1
            if _as_int(r.get(col, "")) is not None:
                hits += 1
        ratio = (hits / tot) if tot else 0.0
        if ratio > best_ratio:
            best_ratio = ratio
            best_col = col

    if best_col is None:
        raise ValueError("Could not infer a numeric totalAffected column.")
    return best_col


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", help="Path to facility_rollup.csv")
    ap.add_argument("output_csv", help="Path to top_facilities.csv")
    ap.add_argument("--top", type=int, default=15, help="How many rows to keep (default 15). Use 0 for all.")
    args = ap.parse_args()

    rows, fieldnames = read_rows(args.input_csv)
    facility_col, total_col_guess = detect_columns(fieldnames)
    total_col = choose_total_affected_column(rows, fieldnames, facility_col, total_col_guess)

    # Normalize / compute sort key
    enriched: List[Tuple[int, Dict[str, str]]] = []
    bad = 0
    for r in rows:
        t = _as_int(r.get(total_col, ""))
        if t is None:
            bad += 1
            t = 0
        enriched.append((t, r))

    enriched.sort(key=lambda x: x[0], reverse=True)

    if args.top and args.top > 0:
        enriched = enriched[: args.top]

    ensure_parent_dir(args.output_csv)

    # Output columns: preserve original header ordering, but ensure facility/total exist.
    out_fieldnames = fieldnames[:]
    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        for _, r in enriched:
            writer.writerow(r)

    print("OK: wrote", args.output_csv)
    print(f"  inputRows={len(rows)}")
    print(f"  outputRows={len(enriched)}")
    print(f"  facilityCol={facility_col}")
    print(f"  totalAffectedCol={total_col}")
    if bad:
        print(f"  warning: {bad} rows had non-numeric totalAffected; treated as 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
