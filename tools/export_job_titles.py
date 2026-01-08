import csv
import sys
from collections import defaultdict

def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/export_facility_rollup_from_impacts.py <impacts_by_facility.csv> <out.csv>")
        sys.exit(1)

    impacts_path = sys.argv[1]
    out_path = sys.argv[2]

    totals = defaultdict(int)
    titles = defaultdict(set)
    notices = defaultdict(set)

    with open(impacts_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row["facilityId"]
            title = row["jobTitleCanonical"]
            notice = row["noticeId"]
            count = int(row["affectedCount"])

            totals[fid] += count
            titles[fid].add(title)
            notices[fid].add(notice)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "facilityId",
            "totalAffected",
            "jobTitleCount",
            "noticeCount"
        ])

        for fid in sorted(totals.keys()):
            writer.writerow([
                fid,
                totals[fid],
                len(titles[fid]),
                len(notices[fid])
            ])

    print(f"OK: wrote {out_path}")
    print(f"  facilities={len(totals)}")

if __name__ == "__main__":
    main()
