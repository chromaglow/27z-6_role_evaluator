#!/usr/bin/env python3
"""
export_notice_summary_from_impacts.py

Input:  impacts_by_facility.csv (row-level canonical data)
Output: notice_summary.csv with:
  noticeId,totalAffected,totalFacilities,totalTitles
"""

from __future__ import annotations

import argparse
import csv
import os
from collections import defaultdict
from typing import Dict, Set


def ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", help="data/exports/impacts_by_facility.csv")
    ap.add_argument("output_csv", help="data/exports/notice_summary.csv")
    args = ap.parse_args()

    totals: Dict[str, int] = defaultdict(int)
    facilities: Dict[str, Set[str]] = defaultdict(set)
    titles: Dict[str, Set[str]] = defaultdict(set)

    with open(args.input_csv, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            notice = (row.get("noticeId") or "").strip()
            facility = (row.get("facilityId") or "").strip()
            title = (row.get("jobTitleCanonical") or row.get("jobTitle") or row.get("jobTitleRaw") or "").strip()
            affected = row.get("affectedCount")

            if not notice:
                continue

            try:
                n = int(affected) if affected is not None and str(affected).strip() != "" else 0
            except ValueError:
                n = 0

            totals[notice] += n
            if facility:
                facilities[notice].add(facility)
            if title:
                titles[notice].add(title)

    out_rows = []
    for notice_id in sorted(totals.keys()):
        out_rows.append({
            "noticeId": notice_id,
            "totalAffected": totals[notice_id],
            "totalFacilities": len(facilities[notice_id]),
            "totalTitles": len(titles[notice_id]),
        })

    ensure_parent_dir(args.output_csv)
    with open(args.output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["noticeId", "totalAffected", "totalFacilities", "totalTitles"])
        writer.writeheader()
        for r in out_rows:
            writer.writerow(r)

    print("OK: wrote", args.output_csv)
    print(f"  notices={len(out_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
