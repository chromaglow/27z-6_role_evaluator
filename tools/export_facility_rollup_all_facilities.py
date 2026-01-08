#!/usr/bin/env python3
"""
export_facility_rollup_all_facilities.py

Left-join combined.json facilities list to an impact-driven facility_rollup.csv
so that facilities with no impact rows appear with zeros.

Inputs:
  1) data/normalized/combined.json
  2) data/exports/facility_rollup.csv
Output:
  data/exports/facility_rollup_all_facilities.csv

Notes:
- Preserves the facility_rollup.csv header order.
- Adds one extra column at the end: hasImpacts (true/false)
- Fills numeric columns with 0 for missing facilities, leaves others blank.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from typing import Any, Dict, List, Optional, Set


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)


def _as_int(val: Any) -> Optional[int]:
    if val is None:
        return None
    s = str(val).strip()
    if s == "":
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def load_combined_facility_ids(combined_path: str) -> List[str]:
    with open(combined_path, "r", encoding="utf-8") as f:
        combined = json.load(f)

    facilities = combined.get("facilities")
    if facilities is None:
        raise ValueError("combined.json missing top-level key: 'facilities'")

    ids: Set[str] = set()

    # facilities is expected to be a list of dicts, but be defensive.
    if isinstance(facilities, list):
        for item in facilities:
            if isinstance(item, dict):
                fid = item.get("facilityId") or item.get("facility_id") or item.get("facility")
                if fid:
                    ids.add(str(fid).strip())
            elif isinstance(item, str):
                ids.add(item.strip())
    elif isinstance(facilities, dict):
        # If it's a dict keyed by facilityId
        for k in facilities.keys():
            ids.add(str(k).strip())
    else:
        raise ValueError("combined.json 'facilities' is not a list or dict")

    out = sorted([x for x in ids if x])
    if not out:
        raise ValueError("No facilityIds found in combined.json facilities")
    return out


def detect_numeric_columns(rows: List[Dict[str, str]], fieldnames: List[str], facility_col: str) -> Set[str]:
    numeric_cols: Set[str] = set()
    for col in fieldnames:
        if col == facility_col:
            continue
        # treat as numeric if >= 80% of non-empty values are numeric
        hits = 0
        total = 0
        for r in rows:
            v = (r.get(col) or "").strip()
            if v == "":
                continue
            total += 1
            if _as_int(v) is not None:
                hits += 1
        if total == 0:
            # unknown: leave non-numeric by default
            continue
        if hits / total >= 0.8:
            numeric_cols.add(col)
    return numeric_cols


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("combined_json", help="data/normalized/combined.json")
    ap.add_argument("facility_rollup_csv", help="data/exports/facility_rollup.csv")
    ap.add_argument("output_csv", help="data/exports/facility_rollup_all_facilities.csv")
    args = ap.parse_args()

    facility_ids = load_combined_facility_ids(args.combined_json)

    with open(args.facility_rollup_csv, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("facility_rollup.csv missing header row.")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Detect facility id column (expected facilityId)
    lower_map = {c.lower(): c for c in fieldnames}
    facility_col = lower_map.get("facilityid", fieldnames[0])

    # Index existing rollup rows
    rollup_by_facility: Dict[str, Dict[str, str]] = {}
    for r in rows:
        fid = (r.get(facility_col) or "").strip()
        if fid:
            rollup_by_facility[fid] = r

    numeric_cols = detect_numeric_columns(rows, fieldnames, facility_col)

    out_fieldnames = fieldnames[:]
    if "hasImpacts" not in out_fieldnames:
        out_fieldnames.append("hasImpacts")

    out_rows: List[Dict[str, str]] = []
    missing = 0

    for fid in facility_ids:
        existing = rollup_by_facility.get(fid)
        if existing:
            out = dict(existing)
            out["hasImpacts"] = "true"
        else:
            missing += 1
            out = {k: "" for k in fieldnames}
            out[facility_col] = fid
            for col in numeric_cols:
                out[col] = "0"
            out["hasImpacts"] = "false"
        out_rows.append(out)

    # Sort by totalAffected desc if present, else alphabetical
    total_col = lower_map.get("totalaffected")
    if total_col:
        out_rows.sort(key=lambda r: (_as_int(r.get(total_col, "")) or 0), reverse=True)
    else:
        out_rows.sort(key=lambda r: r.get(facility_col, ""))

    ensure_parent_dir(args.output_csv)
    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        for r in out_rows:
            writer.writerow(r)

    print("OK: wrote", args.output_csv)
    print(f"  combinedFacilities={len(facility_ids)}")
    print(f"  rollupFacilitiesWithImpacts={len(rollup_by_facility)}")
    print(f"  missingFilledWithZeros={missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
