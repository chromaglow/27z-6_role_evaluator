import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_notice.py <path_to_notice.json>")
        sys.exit(2)

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))

    # Top-level checks
    assert "version" in data and isinstance(data["version"], str)
    assert "generatedAt" in data and isinstance(data["generatedAt"], str)
    assert "notice" in data and isinstance(data["notice"], dict)

    notice = data["notice"]

    required_notice_keys = [
        "noticeId",
        "source",
        "jurisdiction",
        "separationDates",
        "facilities",
        "jobTitleImpacts"
    ]

    for key in required_notice_keys:
        assert key in notice, f"Missing notice.{key}"

    assert isinstance(notice["facilities"], list), "facilities must be a list"
    assert isinstance(notice["jobTitleImpacts"], list), "jobTitleImpacts must be a list"

    # Facility IDs must be unique
    facility_ids = [f["facilityId"] for f in notice["facilities"]]
    assert len(facility_ids) == len(set(facility_ids)), "Duplicate facilityId found"

    # Job impacts must reference known facilities
    known = set(facility_ids)
    for job in notice["jobTitleImpacts"]:
        assert job["facilityId"] in known, (
            f"jobTitleImpact references unknown facilityId: {job['facilityId']}"
        )

    print(
        f"OK: {path} "
        f"(facilities={len(notice['facilities'])}, "
        f"jobTitleImpacts={len(notice['jobTitleImpacts'])})"
    )

if __name__ == "__main__":
    main()
