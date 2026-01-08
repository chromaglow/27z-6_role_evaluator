import csv
import collections
from pathlib import Path

CSV_PATH = Path(r"data\normalized\facility_geocodes.csv")

def main() -> int:
    if not CSV_PATH.exists():
        print(f"ERROR: missing file: {CSV_PATH}")
        return 2

    rows = list(csv.DictReader(CSV_PATH.open(newline="", encoding="utf-8-sig")))

    bad = []
    for r in rows:
        fid = (r.get("facilityId") or "").strip()
        try:
            lat = float(r.get("lat"))
            lon = float(r.get("lon"))
        except Exception:
            bad.append((fid, "parse_error", r.get("lat"), r.get("lon")))
            continue

        # continental US-ish sanity bounds
        if not (15 <= lat <= 75) or not (-175 <= lon <= -50):
            bad.append((fid, "out_of_range", lat, lon))

    m = collections.defaultdict(list)
    for r in rows:
        fid = (r.get("facilityId") or "").strip()
        try:
            lat = float(r.get("lat"))
            lon = float(r.get("lon"))
        except Exception:
            continue
        m[(lat, lon)].append(fid)

    dups = sorted(
        [(k, v) for k, v in m.items() if len(v) > 1],
        key=lambda x: len(x[1]),
        reverse=True,
    )

    print(f"rows={len(rows)}")
    print(f"bad={len(bad)}")
    print("bad sample:")
    for x in bad[:25]:
        print(" ", x)

    print(f"\nunique_points={len(m)}")
    print(f"duplicate_groups={len(dups)}")
    print("top duplicate groups:")
    for (latlon, ids) in dups[:15]:
        print(" ", latlon, "count=", len(ids), "example=", ids[:15])

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
