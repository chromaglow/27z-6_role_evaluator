import json
import re
import sys
from pathlib import Path
from datetime import datetime

FACILITY_RE = re.compile(
    r"(?:\u2022|\uf0b7|•)\s+([A-Z0-9]+)\s+facility\s+at\s+(.+?)\s+\(approximately\s+(\d+)\s+employee[s]?\s+affected\);",
    re.IGNORECASE
)


REMOTE_CLAUSE_RE = re.compile(
    r"plus\s+(\d+)\s+affected\s+remote\s+employees\s+residing\s+within\s+the\s+state\s+of\s+Washington",
    re.IGNORECASE
)

# Example line: "SEA106 Software Dev Engineer II 11"
JOB_LINE_RE = re.compile(r"^([A-Z0-9]+)\s+(.+?)\s+(\d+)$")

def load_pages(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    # supports both list-of-pages and {"pages":[...]} shapes if you ever change extract later
    if isinstance(data, dict) and "pages" in data:
        return data["pages"]
    if isinstance(data, list):
        return data
    raise ValueError("Unexpected pages JSON structure")

def parse_facilities(pages):
    facilities = []

    for p in pages:
        for m in FACILITY_RE.finditer(p["text"]):
            facility_id = m.group(1)
            address = m.group(2).strip()
            approx = int(m.group(3))

            facilities.append({
                "noticeId": "notice_2",
                "facilityId": facility_id,
                "affectedApprox": approx,
                "includesRemoteWA": True,
                "notes": address
            })

    return facilities


def parse_remote_clause(pages):
    for p in pages:
        m = REMOTE_CLAUSE_RE.search(p["text"])
        if m:
            count = int(m.group(1))
            return [{
                "text": f"plus {count} affected remote employees residing within the state of Washington.",
                "affectedCount": count,
                "state": "WA"
            }]
    return []

def parse_separation_dates(pages):
    # Pull the big sentence and extract "Month DD, YYYY" patterns
    date_re = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}")
    months = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    dates = []
    for p in pages:
        hits = date_re.findall(p["text"])
        # findall returns only group1 if using a capturing group; better use finditer
        for m in date_re.finditer(p["text"]):
            s = m.group(0)
            month_name, day_str, year_str = re.match(r"(\w+)\s+(\d{1,2}),\s+(\d{4})", s).groups()
            dt = datetime(int(year_str), months[month_name], int(day_str))
            dates.append(dt.strftime("%Y-%m-%d"))
    # De-dup and sort, but keep only dates that look like the separation list (you can tighten later)
    dates = sorted(set(dates))
    return dates

def parse_job_titles(pages):
    job_impacts = []
    in_table = False

    for p in pages:
        lines = [ln.strip() for ln in p["text"].splitlines() if ln.strip()]

        # table starts where we see the header
        if any("LIST OF AFFECTED JOB TITLES" in ln for ln in lines):
            in_table = True
            continue

        if not in_table:
            continue

        for ln in lines:
            # Skip headers
            if ln.startswith("Number of Affected Employees") or ln.startswith("Facility Job Title"):
                continue

            m = JOB_LINE_RE.match(ln)
            if not m:
                continue

            facility_id, title_raw, count = m.group(1), m.group(2).strip(), int(m.group(3))

            # Normalize facility id for remote rows: they appear as "Remote ..." in your pages,
            # but our regex captures facility_id as "Remote" only if the line begins with "Remote".
            # Your extracted text for remote lines starts with "Remote ..." not "RemoteFacility".
            # Those remote lines in your file start with "Remote Manager Team, Customer Service 1"
            # That WON'T match this regex because it doesn't begin with [A-Z0-9]+.
            # We'll handle remote lines separately below.

            job_impacts.append({
                "facilityId": facility_id,
                "jobTitle": title_raw,
                "affectedCount": count
            })

    # Handle remote lines (pages 25–27 in your extract) that start with "Remote ..."
    remote_impacts = []
    for p in pages:
        for ln in p["text"].splitlines():
            ln = ln.strip()
            if not ln.startswith("Remote "):
                continue
            # remote line format: "Remote <job title> <count>"
            m = re.match(r"^Remote\s+(.+?)\s+(\d+)$", ln)
            if not m:
                continue
            title_raw, count = m.group(1).strip(), int(m.group(2))
            remote_impacts.append({
                "facilityId": "REMOTE_WA",
                "jobTitle": title_raw,
                "affectedCount": count
            })

    job_impacts.extend(remote_impacts)
    return job_impacts

def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/parse_layoff2.py data/extracted/layoff2_pages.json data/normalized/notice_2.json")
        sys.exit(2)

    pages_path = Path(sys.argv[1])
    notice_path = Path(sys.argv[2])

    pages = load_pages(pages_path)
    notice = json.loads(notice_path.read_text(encoding="utf-8"))

    facilities = parse_facilities(pages)
    remote_clauses = parse_remote_clause(pages)
    separation_dates = parse_separation_dates(pages)
    job_titles = parse_job_titles(pages)

    # Add a synthetic facility entry for remote WA, if referenced in job titles
    remote_wa_count = None
    for rc in remote_clauses:
        if rc.get("state") == "WA":
            remote_wa_count = rc.get("affectedCount")
            break

    if remote_wa_count is not None:
        facilities.append({
            "noticeId": "notice_2",
            "facilityId": "REMOTE_WA",
            "affectedApprox": int(remote_wa_count),
            "includesRemoteWA": True,
            "notes": "Remote employees residing within WA (no facility address)."
        })



    notice["notice"]["facilities"] = facilities
    notice["notice"]["remoteClauses"] = remote_clauses
    notice["notice"]["separationDates"] = separation_dates
    notice["notice"]["jobTitleImpacts"] = job_titles

    notice_path.write_text(json.dumps(notice, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"OK: wrote {notice_path}")
    print(f"  facilities={len(facilities)}")
    print(f"  remoteClauses={len(remote_clauses)}")
    print(f"  separationDates={len(separation_dates)}")
    print(f"  jobTitleImpacts={len(job_titles)}")

if __name__ == "__main__":
    main()