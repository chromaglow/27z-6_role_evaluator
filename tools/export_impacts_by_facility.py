import json
import csv
import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/export_impacts_by_facility.py <combined.json> <out.csv>")
        sys.exit(1)

    combined_path = sys.argv[1]
    out_path = sys.argv[2]

    # Ensure output directory exists
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(combined_path, "r", encoding="utf-8") as f:
        combined = json.load(f)

    notices = combined.get("notices", [])

    rows_out = []
    for n in notices:
        notice_id = n.get("noticeId") or n.get("notice", {}).get("noticeId") or ""

        impacts = n.get("jobTitleImpacts", [])
        for r in impacts:
            facility_id = r.get("facilityId", "")
            raw = r.get("jobTitleRaw") or r.get("jobTitle") or ""
            canonical = r.get("jobTitleCanonical") or r.get("jobTitle") or ""
            count = int(r.get("affectedCount", 0))

            rows_out.append({
                "noticeId": notice_id,
                "facilityId": facility_id,
                "jobTitleRaw": raw,
                "jobTitleCanonical": canonical,
                "affectedCount": count,
            })

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["noticeId", "facilityId", "jobTitleRaw", "jobTitleCanonical", "affectedCount"])
        for r in rows_out:
            w.writerow([r["noticeId"], r["facilityId"], r["jobTitleRaw"], r["jobTitleCanonical"], r["affectedCount"]])

    print(f"OK: wrote {out_path}")
    print(f"  rows={len(rows_out)}")
    print(f"  notices={len(notices)}")

if __name__ == "__main__":
    main()
