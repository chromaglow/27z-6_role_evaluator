import csv
import time
from pathlib import Path
from geopy.geocoders import Nominatim

IN_PATH = Path(r"data/normalized/facility_geocodes.csv")
OUT_CANDIDATE = Path(r"data/normalized/facility_geocodes_REFRESH_CANDIDATE.csv")
OUT_CHANGES = Path(r"data/normalized/geocode_refresh_changes.csv")
OUT_UNRESOLVED = Path(r"data/normalized/geocode_refresh_unresolved.csv")

# Be polite to OSM. 1 second is usually OK; increase if you get throttled.
SLEEP_SECONDS = 1.5

# If notes contain any of these tokens, we assume the current location is intentional
# (centroid/approx placement) and we do NOT replace lat/lon.
SKIP_IF_NOTES_CONTAIN = [
    "CENTROID",
    "APPROX",
    "APPROX_AREA",
    "OK TO APPROX",
    "REMOTE_CLUSTER",
]

def norm(s: str) -> str:
    return (s or "").strip()

def upper(s: str) -> str:
    return norm(s).upper()

def build_query(row: dict) -> str:
    street = norm(row.get("streetAddress"))
    city = norm(row.get("city"))
    state = norm(row.get("state"))
    zipc = norm(row.get("zip"))

    parts = []
    if street:
        parts.append(street)
    if city:
        parts.append(city)
    if state or zipc:
        parts.append(" ".join([p for p in [state, zipc] if p]))

    return ", ".join(parts)

def main():
    with IN_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Preserve whatever columns exist in the input
    fieldnames = list(rows[0].keys()) if rows else []
    required = ["facilityId", "lat", "lon", "source", "notes", "streetAddress", "city", "state", "zip"]
    missing_cols = [c for c in required if c not in fieldnames]
    if missing_cols:
        raise SystemExit(f"Missing required columns in {IN_PATH}: {missing_cols}")

    geolocator = Nominatim(user_agent="27z6_facility_geocode_refresh_v1", timeout=10)


    changes = []
    unresolved = []
    out_rows = []

    for i, row in enumerate(rows, start=1):
        fid = norm(row.get("facilityId"))
        old_lat = norm(row.get("lat"))
        old_lon = norm(row.get("lon"))
        notes = upper(row.get("notes"))

        # Default: keep existing
        new_lat = old_lat
        new_lon = old_lon
        new_source = row.get("source", "")
        new_notes = row.get("notes", "")

        # Skip geocoding if notes indicate intentional approximation/cluster
        if any(tok in notes for tok in SKIP_IF_NOTES_CONTAIN):
            out_rows.append(row)
            continue

        query = build_query(row)

        if not query or query.count(",") < 1:
            # Not enough info to geocode
            unresolved.append({
                "facilityId": fid,
                "reason": "insufficient address fields to geocode",
                "query": query,
            })
            out_rows.append(row)
            continue

        try:
            loc = geolocator.geocode(query)
        except Exception as e:
            unresolved.append({
                "facilityId": fid,
                "reason": f"geocode error: {e}",
                "query": query,
            })
            out_rows.append(row)
            time.sleep(SLEEP_SECONDS)
            continue

        if not loc:
            unresolved.append({
                "facilityId": fid,
                "reason": "no geocode result",
                "query": query,
            })
            out_rows.append(row)
            time.sleep(SLEEP_SECONDS)
            continue

        new_lat = f"{loc.latitude:.6f}"
        new_lon = f"{loc.longitude:.6f}"

        # Update row
        row["lat"] = new_lat
        row["lon"] = new_lon
        row["source"] = "OpenStreetMap Nominatim (refresh)"
        if new_notes:
            row["notes"] = f"{new_notes} | refreshed from address: {query}"
        else:
            row["notes"] = f"refreshed from address: {query}"

        # Record changes if lat/lon moved meaningfully
        if old_lat != new_lat or old_lon != new_lon:
            changes.append({
                "facilityId": fid,
                "old_lat": old_lat,
                "old_lon": old_lon,
                "new_lat": new_lat,
                "new_lon": new_lon,
                "query": query,
            })

        out_rows.append(row)
        time.sleep(SLEEP_SECONDS)

    # Write candidate output
    with OUT_CANDIDATE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    if changes:
        with OUT_CHANGES.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(changes[0].keys()))
            w.writeheader()
            w.writerows(changes)

    if unresolved:
        with OUT_UNRESOLVED.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(unresolved[0].keys()))
            w.writeheader()
            w.writerows(unresolved)

    print(f"OK: wrote {OUT_CANDIDATE}")
    print(f"changes: {len(changes)}  unresolved: {len(unresolved)}  total: {len(rows)}")

if __name__ == "__main__":
    main()
