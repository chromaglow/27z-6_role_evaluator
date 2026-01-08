#!/usr/bin/env python3
"""
export_top_job_titles.py

Input:  job_title_rollup.csv (from export_job_title_rollup_from_impacts.py)
Output: top_job_titles.csv sorted desc by totalAffected
"""

from __future__ import annotations

import argparse
import csv
import os
from typing import Dict, List, Optional, Tuple


TITLE_CANDIDATES = ["jobTitleCanonical", "job_title_canonical", "title", "canonicalTitle"]
TOTAL_CANDIDATES = ["totalAffected", "total_affected", "affectedTotal", "affected_total", "affected", "total"]


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


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)


def detect(fieldnames: List[str], candidates: List[str], fallback_index: int) -> str:
    lower_map = {f.lower(): f for f in fieldnames}
    for c in candidates:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    if len(fieldnames) <= fallback_index:
        raise ValueError("CSV does not have enough columns to infer required field.")
    return fieldnames[fallback_index]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv")
    ap.add_argument("output_csv")
    ap.add_argument("--top", type=int, default=25, help="Default 25. Use 0 for all.")
    args = ap.parse_args()

    with open(args.input_csv, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV appears to have no header row.")
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    title_col = detect(fieldnames, TITLE_CANDIDATES, 0)
    total_col = detect(fieldnames, TOTAL_CANDIDATES, 1)

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
    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for _, r in enriched:
            writer.writerow(r)

    print("OK: wrote", args.output_csv)
    print(f"  inputRows={len(rows)}")
    print(f"  outputRows={len(enriched)}")
    print(f"  titleCol={title_col}")
    print(f"  totalAffectedCol={total_col}")
    if bad:
        print(f"  warning: {bad} rows had non-numeric totalAffected; treated as 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
