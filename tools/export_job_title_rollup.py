import csv
import json
import os
import sys
from collections import defaultdict

def canonical_title_from_row(row: dict) -> str:
    # notice_1 rows have jobTitleCanonical
    if "jobTitleCanonical" in row and row["jobTitleCanonical"]:
        return row["jobTitleCanonical"].strip()
    # notice_2 rows have jobTitle
    if "jobTitle" in row and row["jobTitle"]:
        return str(row["jobTitle"]).strip()
    # fallback
    if "jobTitleRaw" in row and row["jobTitleRaw"]:
        return str(row["jobTitleRaw"]).strip()
    raise KeyError(f"Missing job title fields in row. Keys={list(row.keys())}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/export_job_title_rollup.py <combined.json> <out.csv>")
        sys.exit(1)

    combined_path = sys.argv[1]
    out_path = sys.argv[2]

    with open(combined_path, "r", encoding="utf-8") as f:
        combined = json.load(f)

    notices = combined.get("notices", [])
    titles_index = combined.get("jobTitles", {}).get("canonicalTitles", [])

    totals = defaultdict(int)          # title -> total affected
    facilities = defaultdict(set)      # title -> set(facilityId)
    notices_seen = defaultdict(set)    # title -> set(noticeId)

    for n in notices:
        notice_id = n.get("noticeId") or n.get("notice", {}).get("noticeId")
        impacts = n.get("jobTitleImpacts", [])

        for row in impacts:
            title = canonical_title_from_row(row)
            fid = row.get("facilityId")
            cnt = int(row.get("affectedCount", 0))

            totals[title] += cnt
            if fid:
                facilities[title].add(fid)
            if notice_id:
                notices_seen[title].add(notice_id)

    # Ensure directory exists
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Build the full title list:
    # - titles_index should already contain all canonical titles
    # - but union anyway to be safe
    all_titles = sorted(set(titles_index) | set(totals.keys()))

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["jobTitleCanonical", "totalAffected", "facilityCount", "noticeCount"])
        for t in all_titles:
            w.writerow([
                t,
                totals.get(t, 0),
                len(facilities.get(t, set())),
                len(notices_seen.get(t, set())),
            ])

    print(f"OK: wrote {out_path}")
    print(f"  titles={len(all_titles)}")
    print(f"  rows={len(all_titles)}")

if __name__ == "__main__":
    main()
