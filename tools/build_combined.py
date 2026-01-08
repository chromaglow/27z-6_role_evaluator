import json
import sys
from datetime import datetime, timezone

def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_address_best_effort(notes: str):
    """
    notes often looks like:
      '320 108th Ave NE, Bellevue, WA 98004'
    We'll do best-effort parsing into {line1, city, state, postalCode?}.
    """
    notes = (notes or "").strip()
    line1, city, state, postal = "", "", "", None

    parts = [p.strip() for p in notes.split(",")]
    if len(parts) >= 1:
        line1 = parts[0]
    if len(parts) >= 2:
        city = parts[1]
    if len(parts) >= 3:
        # "WA 98004" or "WA"
        st_parts = parts[2].split()
        if len(st_parts) >= 1:
            state = st_parts[0]
        if len(st_parts) >= 2:
            postal = st_parts[1]

    return {
        "line1": line1,
        "city": city,
        "state": state,
        **({"postalCode": postal} if postal else {}),
    }

def load_notice(path):
    with open(path, "r", encoding="utf-8") as f:
        blob = json.load(f)
    # normalized file shape: { version, generatedAt, notice: {...} }
    return blob["notice"]

def main():
    if len(sys.argv) != 4:
        print("Usage: python tools/build_combined.py data/normalized/notice_1.json data/normalized/notice_2.json data/normalized/combined.json")
        sys.exit(2)

    notice1_path, notice2_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    n1 = load_notice(notice1_path)
    n2 = load_notice(notice2_path)

    notices = [n1, n2]

    # ----- Build deduped Facility[] definitions -----
    # FacilityImpact has: {noticeId, facilityId, affectedApprox, notes, ...}
    # We create Facility definitions from the first seen impact that has notes.
    facility_defs = {}

    for n in notices:
        for imp in n.get("facilities", []):
            fid = imp["facilityId"]
            if fid not in facility_defs:
                notes = imp.get("notes", "") or ""
                addr = parse_address_best_effort(notes)

                # Label best-effort: "SEA104 - Bellevue, WA" etc
                label_city = addr.get("city", "").strip()
                label_state = addr.get("state", "").strip()
                suffix = ""
                if label_city and label_state:
                    suffix = f" - {label_city}, {label_state}"
                elif label_city:
                    suffix = f" - {label_city}"
                elif label_state:
                    suffix = f" - {label_state}"

                facility_defs[fid] = {
                    "facilityId": fid,
                    "label": f"{fid}{suffix}",
                    "address": addr,
                }

    # If you keep REMOTE_WA as a synthetic facilityId, define it here too (in case notes parsing is empty).
    if "REMOTE_WA" in facility_defs:
        # make sure it has a reasonable label/address
        facility_defs["REMOTE_WA"]["label"] = "REMOTE_WA - Remote, WA"
        facility_defs["REMOTE_WA"]["address"] = {
            "line1": "",
            "city": "",
            "state": "WA",
        }

    facilities = sorted(facility_defs.values(), key=lambda x: x["facilityId"])


    # ----- Build jobTitles indexes -----
    # We want:
    # - jobTitles.canonicalTitles = list[dict] with counts and facility coverage
    # - jobTitles.byFacility      = dict[facilityId] -> list[str] of titles present at that facility

    from collections import defaultdict

    title_to_total = defaultdict(int)      # title -> total affectedCount across all notices/facilities
    title_to_facilities = defaultdict(set) # title -> set of facilityIds where it appears
    by_facility = defaultdict(set)         # facilityId -> set of titles present

    for n in notices:
        for row in n.get("jobTitleImpacts", []):
            fid = row.get("facilityId")
            title = row.get("jobTitleCanonical") or row.get("jobTitle") or row.get("jobTitleRaw")
            if not title:
                raise KeyError(
                    f"Missing job title field in jobTitleImpacts row. Keys={list(row.keys())}"
                )

            # affectedCount is required for aggregation; default to 0 if absent
            count = int(row.get("affectedCount", 0))

            title_to_total[title] += count

            if fid:
                title_to_facilities[title].add(fid)
                by_facility[fid].add(title)

    canonical_titles = []
    for title in sorted(title_to_total.keys()):
        facs = title_to_facilities[title]
        canonical_titles.append({
            "jobTitleCanonical": title,
            "affectedCount": title_to_total[title],
            "facilityCount": len(facs),
            "facilityIds": sorted(facs),
        })

    combined = {
        "version": "1.0.0",
        "generatedAt": utc_now_iso(),
        "notices": notices,
        "facilities": facilities,
        "jobTitles": {
            "canonicalTitles": canonical_titles,
            "byFacility": {fid: sorted(list(titles)) for fid, titles in by_facility.items()},
        },
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"OK: wrote {out_path}")
    print(f"  notices={len(notices)}")
    print(f"  facilities={len(facilities)}")
    print(f"  canonicalTitles={len(combined['jobTitles']['canonicalTitles'])}")


if __name__ == "__main__":
    main()
