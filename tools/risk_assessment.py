#!/usr/bin/env python3
"""
risk_assessment.py

CLI helper for "enter facility + title => risk context".

Works even if facility geocodes are empty. If geocodes are populated later,
we can extend this to do nearest-facility queries.

Data sources:
- data/exports/impacts_by_facility.csv   (row-level truth)
- data/exports/facility_rollup.csv       (impact-driven facility totals)
- data/normalized/facility_geocodes.json (currently empty, reserved for later)

Usage:
  python tools\risk_assessment.py --facility SEA40 --title "Program Manager III"
"""

from __future__ import annotations

import math
import argparse
import csv
import json
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def load_csv(path: str) -> List[Dict[str, str]]:
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def to_int(x: Optional[str]) -> int:
    if x is None:
        return 0
    s = str(x).strip()
    if s == "":
        return 0
    try:
        return int(float(s))
    except ValueError:
        return 0


def load_geocodes_csv(path: str) -> dict:
    """
    Returns: dict[facilityId] -> (lat, lon)
    """
    geos = {}
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            fid = (r.get("facilityId") or "").strip()
            if not fid:
                continue
            try:
                lat = float(r.get("lat"))
                lon = float(r.get("lon"))
            except (TypeError, ValueError):
                continue
            geos[fid] = (lat, lon)
    return geos


def haversine_km(a, b) -> float:
    """
    Distance between (lat, lon) points in km
    """
    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


    
    if x is None:
        return 0
    s = str(x).strip()
    if s == "":
        return 0
    try:
        return int(float(s))
    except ValueError:
        return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--facility", required=True, help="FacilityId, e.g. SEA40 or REMOTE_WA")
    ap.add_argument("--title", required=True, help="Job title canonical string (exact match)")
    ap.add_argument("--impacts", default=r"data\exports\impacts_by_facility.csv")
    ap.add_argument("--facility_rollup", default=r"data\exports\facility_rollup.csv")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--geocodes", default=r"data\normalized\facility_geocodes.csv")
    ap.add_argument("--nearest", type=int, default=10)
    ap.add_argument("--radius_km", type=float, default=None)

    # ✅ THIS LINE MUST COME BEFORE ANY args.* ACCESS
    args = ap.parse_args()

    facility = args.facility.strip()
    title = args.title.strip()


    impacts = load_csv(args.impacts)
    fac_rollup = load_csv(args.facility_rollup)

    # Facility rollup lookup
    fac_meta = None
    for r in fac_rollup:
        if (r.get("facilityId") or "").strip() == facility:
            fac_meta = r
            break

    # Direct match: title at facility
    direct_total = 0
    direct_notice_ids = set()
    for r in impacts:
        if (r.get("facilityId") or "").strip() != facility:
            continue
        t = (r.get("jobTitleCanonical") or r.get("jobTitle") or "").strip()
        if t != title:
            continue
        direct_total += to_int(r.get("affectedCount"))
        nid = (r.get("noticeId") or "").strip()
        if nid:
            direct_notice_ids.add(nid)

    # Facility: top titles (by affected)
    by_title = defaultdict(int)
    for r in impacts:
        if (r.get("facilityId") or "").strip() != facility:
            continue
        t = (r.get("jobTitleCanonical") or r.get("jobTitle") or "").strip()
        if not t:
            continue
        by_title[t] += to_int(r.get("affectedCount"))

    top_titles_here = sorted(by_title.items(), key=lambda x: x[1], reverse=True)[: args.top]

    # Fallback "nearest": where else does this title appear (top facilities for this title)
    title_by_fac = defaultdict(int)
    title_notice_ids = defaultdict(set)
    for r in impacts:
        t = (r.get("jobTitleCanonical") or r.get("jobTitle") or "").strip()
        if t != title:
            continue
        fid = (r.get("facilityId") or "").strip()
        if not fid:
            continue
        title_by_fac[fid] += to_int(r.get("affectedCount"))
        nid = (r.get("noticeId") or "").strip()
        if nid:
            title_notice_ids[fid].add(nid)

    top_facilities_for_title = sorted(title_by_fac.items(), key=lambda x: x[1], reverse=True)[: args.top]

    # Print report
    print("")
    print("RISK ASSESSMENT (geo=unavailable; using dataset distribution fallback)")
    print(f"Facility: {facility}")
    print(f"Title:    {title}")
    print("")

    if fac_meta:
        print("Facility totals (impact-driven):")
        print(f"  totalAffected: {fac_meta.get('totalAffected')}")
        print(f"  jobTitleCount: {fac_meta.get('jobTitleCount')}")
        print(f"  noticeCount:   {fac_meta.get('noticeCount')}")
    else:
        print("Facility totals (impact-driven):")
        print("  (facility not found in facility_rollup.csv; it may be zero-impact or not present)")

    print("")
    print("Direct match at your facility:")
    print(f"  affectedCount: {direct_total}")
    print(f"  notices:       {sorted(direct_notice_ids) if direct_notice_ids else '[]'}")

    print("")
    print(f"Top titles at {facility} (by affected):")
    if top_titles_here:
        for t, n in top_titles_here:
            print(f"  {n:>5}  {t}")
    else:
        print("  (no impact rows for this facility)")

    print("")
    print(f"Where else this title appears (top facilities for '{title}'):")
    if top_facilities_for_title:
        for fid, n in top_facilities_for_title:
            ns = sorted(title_notice_ids[fid])
            print(f"  {n:>5}  {fid}  notices={ns}")
    else:
        print("  (title not found in impacts dataset)")

    print("")
    print("Next upgrade: populate data/normalized/facility_geocodes.json to enable nearest-facility + map output.")
    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
