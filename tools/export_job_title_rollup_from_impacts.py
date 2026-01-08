import csv
import os
import sys
from collections import defaultdict

def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/export_job_title_rollup_from_impacts.py <impacts_by_facility.csv> <out.csv>")
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    totals = defaultdict(int)        # title -> total affected
    facilities = defaultdict(set)    # title -> set(facilityId)
    notices = defaultdict(set)       # title -> set(noticeId)

    with open(in_path, "r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        required = {"noticeId", "facilityId", "jobTitleCanonical", "affectedCount"}
        missing = required - set(r.fieldnames or [])
        if missing:
            raise KeyError(f"Missing required columns in {in_path}: {sorted(missing)}. Found: {r.fieldnames}")

        for row in r:
            title = (row.get("jobTitleCanonical") or "").strip()
            if not title:
                # fallback if canonical missing
                title = (row.get("jobTitleRaw") or row.get("jobTitle") or "").strip()
            if not title:
                continue

            notice_id = (row.get("noticeId") or "").strip()
            facility_id = (row.get("facilityId") or "").strip()
            count = int(row.get("affectedCount") or 0)

            totals[title] += count
            if facility_id:
                facilities[title].add(facility_id)
            if notice_id:
                notices[title].add(notice_id)

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    all_titles = sorted(totals.keys())

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["jobTitleCanonical", "totalAffected", "facilityCount", "noticeCount"])
        for t in all_titles:
            w.writerow([t, totals[t], len(facilities[t]), len(notices[t])])

    print(f"OK: wrote {out_path}")
    print(f"  titles={len(all_titles)}")
    print(f"  rows={len(all_titles)}")

if __name__ == "__main__":
    main()
