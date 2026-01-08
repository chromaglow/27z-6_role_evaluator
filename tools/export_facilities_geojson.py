#!/usr/bin/env python3
from __future__ import annotations

import math
import argparse
import csv
import json
from collections import defaultdict


def norm_fid(x: str) -> str:
    """
    Normalize facility IDs so matching is consistent across CSVs/JSON.
    """
    return (x or "").strip().upper()


def load_csv(path: str):
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def to_int(x):
    try:
        return int(float(str(x).strip()))
    except Exception:
        return 0


def load_geocodes_csv(path: str) -> dict:
    """
    Returns dict[facilityId] -> {lat, lon, source, notes}
    facilityId keys are normalized (uppercase).
    """
    geos = {}
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            fid = norm_fid(r.get("facilityId") or "")
            if not fid:
                continue
            try:
                lat = float((r.get("lat") or "").strip())
                lon = float((r.get("lon") or "").strip())
            except Exception:
                continue

            geos[fid] = {
                "lat": lat,
                "lon": lon,
                "source": (r.get("source") or "").strip(),
                "notes": (r.get("notes") or "").strip(),
            }
    return geos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--geocodes", default=r"data\normalized\facility_geocodes.csv")
    ap.add_argument("--facility_rollup", default=r"data\exports\facility_rollup_all_facilities.csv")
    ap.add_argument("--impacts", default=r"data\exports\impacts_by_facility.csv")
    ap.add_argument("--out", default=r"data\exports\facilities.geojson")
    ap.add_argument("--top_titles", type=int, default=5, help="Top titles per facility by affectedCount")
    ap.add_argument("--exclude_remote", action="store_true", default=True, help="Exclude REMOTE_WA from map output")
    args = ap.parse_args()

    geos = load_geocodes_csv(args.geocodes)
    rollup = load_csv(args.facility_rollup)
    impacts = load_csv(args.impacts)

    # Build per-facility title ranking (keyed by normalized fid)
    fac_title_totals = defaultdict(lambda: defaultdict(int))
    for r in impacts:
        fid = norm_fid(r.get("facilityId") or "")
        if not fid:
            continue
        title = (r.get("jobTitleCanonical") or r.get("jobTitle") or "").strip()
        if not title:
            continue
        fac_title_totals[fid][title] += to_int(r.get("affectedCount"))

    features = []
    missing_geo = 0
    excluded_remote = 0

    # Track how many times we see the same (lat, lon) so we can jitter duplicates
    coord_counts = {}  # (lat, lon) -> count seen so far

    for r in rollup:
        fid_raw = r.get("facilityId") or ""
        fid = norm_fid(fid_raw)
        if not fid:
            continue

        # REMOTE_WA is not a physical site; do not plot on the map
        if args.exclude_remote and fid == "REMOTE_WA":
            excluded_remote += 1
            continue

        g = geos.get(fid)
        if not g:
            missing_geo += 1
            continue

        totalAffected = to_int(r.get("totalAffected"))
        jobTitleCount = to_int(r.get("jobTitleCount"))
        noticeCount = to_int(r.get("noticeCount"))

        hasImpacts = str(r.get("hasImpacts") or "").strip().lower()
        if hasImpacts in ("true", "false"):
            hasImpacts_bool = (hasImpacts == "true")
        else:
            hasImpacts_bool = totalAffected > 0

        top_titles = sorted(
            fac_title_totals.get(fid, {}).items(),
            key=lambda x: x[1],
            reverse=True
        )[:args.top_titles]
        top_titles = [{"title": t, "affected": n} for (t, n) in top_titles]

        # Read lat/lon and jitter duplicates deterministically
        lat = float(g["lat"])
        lon = float(g["lon"])

        key = (lat, lon)
        idx = coord_counts.get(key, 0)
        coord_counts[key] = idx + 1

        is_duplicate = idx > 0
        geo_quality = "duplicate" if is_duplicate else "ok"

        # Jitter duplicates by ~60m, ~120m, ... in a simple diagonal pattern
        if is_duplicate:
            meters = 60.0 * idx
            dlat = meters / 111000.0
            denom = 111000.0 * max(0.1, math.cos(math.radians(lat)))
            dlon = meters / denom
            lat = lat + dlat
            lon = lon + dlon

        feat = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "facilityId": fid,  # normalized on output too
                "totalAffected": totalAffected,
                "jobTitleCount": jobTitleCount,
                "noticeCount": noticeCount,
                "hasImpacts": hasImpacts_bool,
                "geoSource": g.get("source", ""),
                "geoNotes": g.get("notes", ""),
                "geoQuality": geo_quality,
                "topTitles": top_titles,
            },
        }
        features.append(feat)

    fc = {"type": "FeatureCollection", "features": features}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(fc, f, indent=2)

    print(f"OK: wrote {args.out}")
    print(f"  features={len(features)}")
    print(f"  missingGeoForFacilitiesInRollup={missing_geo}")
    print(f"  excludedRemoteWA={excluded_remote}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
