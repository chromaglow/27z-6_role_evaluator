import csv
from pathlib import Path

GEOCODES_IN = Path(r"data/normalized/facility_geocodes.csv")
ADDRS_IN = Path(r"data/normalized/facility_addresses_staging_2026-01-08.csv")

GEOCODES_OUT = Path(r"data/normalized/facility_geocodes.csv")  # overwrite in-place
REPORT_OUT = Path(r"data/normalized/geocode_merge_report.csv")

NEW_FIELDS = [
    "facilityId",
    "lat",
    "lon",
    "source",
    "notes",
    "buildingName",
    "streetAddress",
    "city",
    "state",
    "zip",
]

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def main():
    geocodes = read_csv(GEOCODES_IN)
    addrs = read_csv(ADDRS_IN)

    # index addresses by normalized facilityId
    addr_by_id = {}
    for a in addrs:
        fid = (a.get("facility_id") or "").strip().upper()
        if not fid:
            continue
        addr_by_id[fid] = a

    merged = []
    report_rows = []

    for g in geocodes:
        fid = (g.get("facilityId") or "").strip().upper()
        a = addr_by_id.get(fid)

        out = {k: "" for k in NEW_FIELDS}
        out["facilityId"] = g.get("facilityId", "")
        out["lat"] = g.get("lat", "")
        out["lon"] = g.get("lon", "")
        out["source"] = g.get("source", "")
        out["notes"] = g.get("notes", "")

        if a:
            out["buildingName"] = a.get("building_name", "")
            out["streetAddress"] = a.get("street_address", "")
            out["city"] = a.get("city", "")
            out["state"] = a.get("state", "")
            out["zip"] = a.get("zip_code", "")

            # Conservative fill: only populate lat/lon if canonical is missing and staging has values.
            # (Right now staging lat/lon might be blank anyway.)
            g_lat = (out["lat"] or "").strip()
            g_lon = (out["lon"] or "").strip()
            a_lat = (a.get("latitude") or "").strip()
            a_lon = (a.get("longitude") or "").strip()

            changed = False
            if (not g_lat) and a_lat:
                out["lat"] = a_lat
                changed = True
            if (not g_lon) and a_lon:
                out["lon"] = a_lon
                changed = True

            report_rows.append({
                "facilityId": fid,
                "hadAddressRow": True,
                "latWasBlankFilled": (not g_lat) and bool(a_lat),
                "lonWasBlankFilled": (not g_lon) and bool(a_lon),
                "buildingName": out["buildingName"],
                "streetAddress": out["streetAddress"],
                "city": out["city"],
                "state": out["state"],
                "zip": out["zip"],
            })
        else:
            report_rows.append({
                "facilityId": fid,
                "hadAddressRow": False,
                "latWasBlankFilled": False,
                "lonWasBlankFilled": False,
                "buildingName": "",
                "streetAddress": "",
                "city": "",
                "state": "",
                "zip": "",
            })

        merged.append(out)

    write_csv(GEOCODES_OUT, NEW_FIELDS, merged)
    write_csv(REPORT_OUT, list(report_rows[0].keys()), report_rows)

    print(f"OK: updated {GEOCODES_OUT}")
    print(f"OK: wrote {REPORT_OUT}")
    print(f"Rows merged: {len(merged)}  address rows found: {sum(1 for r in report_rows if r['hadAddressRow'])}")

if __name__ == "__main__":
    main()
