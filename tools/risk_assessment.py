#!/usr/bin/env python3
"""
Risk Assessment CLI Tool

A command-line tool for assessing facility and job title risk based on
published layoff notice data. Provides deterministic matching and evidence-based
context without prediction or probability estimation.

Data Sources:
    - data/exports/impacts_by_facility.csv: Row-level impact data
    - data/exports/facility_rollup.csv: Facility-level aggregated totals
    - data/normalized/facility_geocodes.csv: Facility geocoding data

Usage:
    python tools/risk_assessment.py --facility SEA40 --title "Program Manager III"
    python tools/risk_assessment.py --facility SEA93 --title "SDE II" --nearest 5 --radius_km 30

Version: 1.0.0
"""

from __future__ import annotations

import argparse
import csv
import logging
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class RiskAssessmentError(Exception):
    """Base exception for risk assessment errors."""

    pass


class DataLoadError(RiskAssessmentError):
    """Raised when data files cannot be loaded."""

    pass


def load_csv(path: str) -> List[Dict[str, str]]:
    """
    Load a CSV file and return its contents as a list of dictionaries.

    Args:
        path: Path to the CSV file

    Returns:
        List of dictionaries where keys are column names and values are cell values

    Raises:
        DataLoadError: If the file cannot be read or parsed

    Example:
        >>> data = load_csv("data/exports/impacts_by_facility.csv")
        >>> print(len(data))
        150
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            raise DataLoadError(f"File not found: {path}")

        with open(file_path, "r", newline="", encoding="utf-8-sig") as f:
            data = list(csv.DictReader(f))
            logger.debug(f"Loaded {len(data)} rows from {path}")
            return data

    except FileNotFoundError as e:
        raise DataLoadError(f"File not found: {path}") from e
    except csv.Error as e:
        raise DataLoadError(f"Error parsing CSV file {path}: {e}") from e
    except Exception as e:
        raise DataLoadError(f"Unexpected error loading {path}: {e}") from e


def to_int(value: Optional[str]) -> int:
    """
    Safely convert a string value to an integer.

    Handles None, empty strings, and numeric strings (including floats).
    Returns 0 for any value that cannot be converted.

    Args:
        value: String value to convert (can be None)

    Returns:
        Integer value, or 0 if conversion fails

    Example:
        >>> to_int("42")
        42
        >>> to_int("3.14")
        3
        >>> to_int(None)
        0
        >>> to_int("")
        0
    """
    if value is None:
        return 0

    cleaned = str(value).strip()
    if not cleaned:
        return 0

    try:
        return int(float(cleaned))
    except (ValueError, TypeError):
        logger.debug(f"Could not convert '{value}' to int, returning 0")
        return 0


def load_geocodes_csv(path: str) -> Dict[str, Tuple[float, float]]:
    """
    Load facility geocoding data from CSV.

    Args:
        path: Path to the geocodes CSV file

    Returns:
        Dictionary mapping facilityId to (latitude, longitude) tuples

    Raises:
        DataLoadError: If the file cannot be loaded

    Example:
        >>> geocodes = load_geocodes_csv("data/normalized/facility_geocodes.csv")
        >>> geocodes["SEA40"]
        (47.6255, -122.3355)
    """
    geocodes: Dict[str, Tuple[float, float]] = {}

    try:
        file_path = Path(path)
        if not file_path.exists():
            logger.warning(f"Geocodes file not found: {path}")
            return geocodes

        with open(file_path, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                facility_id = (row.get("facilityId") or "").strip()
                if not facility_id:
                    continue

                try:
                    lat = float(row.get("lat", 0))
                    lon = float(row.get("lon", 0))
                    geocodes[facility_id] = (lat, lon)
                except (TypeError, ValueError) as e:
                    logger.debug(f"Invalid coordinates for {facility_id}: {e}")
                    continue

        logger.debug(f"Loaded geocodes for {len(geocodes)} facilities")
        return geocodes

    except Exception as e:
        logger.warning(f"Error loading geocodes from {path}: {e}")
        return geocodes


def haversine_km(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculate the great circle distance between two points on Earth.

    Uses the Haversine formula to compute the distance between two
    latitude/longitude coordinate pairs.

    Args:
        coord1: Tuple of (latitude, longitude) for first point
        coord2: Tuple of (latitude, longitude) for second point

    Returns:
        Distance in kilometers

    Example:
        >>> seattle = (47.6062, -122.3321)
        >>> bellevue = (47.6101, -122.2015)
        >>> distance = haversine_km(seattle, bellevue)
        >>> print(f"{distance:.2f} km")
        9.87 km
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Earth's radius in kilometers
    R = 6371.0

    # Convert to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def find_facility_metadata(
    facility_id: str, facility_rollup: List[Dict[str, str]]
) -> Optional[Dict[str, str]]:
    """
    Find metadata for a specific facility from the rollup data.

    Args:
        facility_id: The facility ID to search for
        facility_rollup: List of facility rollup records

    Returns:
        Dictionary with facility metadata, or None if not found
    """
    for record in facility_rollup:
        if (record.get("facilityId") or "").strip() == facility_id:
            return record
    return None


def calculate_direct_match(
    facility_id: str, title: str, impacts: List[Dict[str, str]]
) -> Tuple[int, Set[str]]:
    """
    Calculate direct matches for a facility and job title combination.

    Args:
        facility_id: The facility ID to match
        title: The job title to match
        impacts: List of impact records

    Returns:
        Tuple of (total_affected_count, set_of_notice_ids)
    """
    total_affected = 0
    notice_ids: Set[str] = set()

    for record in impacts:
        if (record.get("facilityId") or "").strip() != facility_id:
            continue

        record_title = (
            record.get("jobTitleCanonical") or record.get("jobTitle") or ""
        ).strip()
        if record_title != title:
            continue

        total_affected += to_int(record.get("affectedCount"))
        notice_id = (record.get("noticeId") or "").strip()
        if notice_id:
            notice_ids.add(notice_id)

    return total_affected, notice_ids


def get_top_titles_at_facility(
    facility_id: str, impacts: List[Dict[str, str]], top_n: int = 10
) -> List[Tuple[str, int]]:
    """
    Get the top job titles at a facility by affected count.

    Args:
        facility_id: The facility ID to analyze
        impacts: List of impact records
        top_n: Number of top titles to return

    Returns:
        List of (job_title, affected_count) tuples, sorted by count descending
    """
    title_counts: Dict[str, int] = defaultdict(int)

    for record in impacts:
        if (record.get("facilityId") or "").strip() != facility_id:
            continue

        title = (
            record.get("jobTitleCanonical") or record.get("jobTitle") or ""
        ).strip()
        if not title:
            continue

        title_counts[title] += to_int(record.get("affectedCount"))

    return sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]


def get_top_facilities_for_title(
    title: str, impacts: List[Dict[str, str]], top_n: int = 10
) -> Tuple[List[Tuple[str, int]], Dict[str, Set[str]]]:
    """
    Get the top facilities where a job title appears.

    Args:
        title: The job title to search for
        impacts: List of impact records
        top_n: Number of top facilities to return

    Returns:
        Tuple of:
            - List of (facility_id, affected_count) tuples
            - Dictionary mapping facility_id to set of notice_ids
    """
    facility_counts: Dict[str, int] = defaultdict(int)
    facility_notices: Dict[str, Set[str]] = defaultdict(set)

    for record in impacts:
        record_title = (
            record.get("jobTitleCanonical") or record.get("jobTitle") or ""
        ).strip()
        if record_title != title:
            continue

        facility_id = (record.get("facilityId") or "").strip()
        if not facility_id:
            continue

        facility_counts[facility_id] += to_int(record.get("affectedCount"))

        notice_id = (record.get("noticeId") or "").strip()
        if notice_id:
            facility_notices[facility_id].add(notice_id)

    top_facilities = sorted(facility_counts.items(), key=lambda x: x[1], reverse=True)[
        :top_n
    ]
    return top_facilities, facility_notices


def print_report(
    facility_id: str,
    title: str,
    facility_metadata: Optional[Dict[str, str]],
    direct_total: int,
    direct_notices: Set[str],
    top_titles: List[Tuple[str, int]],
    top_facilities: List[Tuple[str, int]],
    facility_notices: Dict[str, Set[str]],
) -> None:
    """
    Print the risk assessment report to stdout.

    Args:
        facility_id: The facility being assessed
        title: The job title being assessed
        facility_metadata: Metadata about the facility
        direct_total: Total affected count for direct matches
        direct_notices: Set of notice IDs for direct matches
        top_titles: Top job titles at the facility
        top_facilities: Top facilities for the job title
        facility_notices: Notice IDs by facility
    """
    print()
    print("=" * 80)
    print("RISK ASSESSMENT REPORT")
    print("=" * 80)
    print(f"Facility: {facility_id}")
    print(f"Title:    {title}")
    print()

    # Facility totals
    print("Facility Totals (Impact-Driven):")
    print("-" * 40)
    if facility_metadata:
        print(f"  Total Affected:    {facility_metadata.get('totalAffected', 'N/A')}")
        print(f"  Job Title Count:   {facility_metadata.get('jobTitleCount', 'N/A')}")
        print(f"  Notice Count:      {facility_metadata.get('noticeCount', 'N/A')}")
    else:
        print("  (Facility not found in rollup data)")
        print("  This may indicate zero impact or missing data")
    print()

    # Direct match
    print("Direct Match at Your Facility:")
    print("-" * 40)
    print(f"  Affected Count:    {direct_total}")
    print(f"  Notices:           {sorted(direct_notices) if direct_notices else '[]'}")
    print()

    # Top titles at facility
    print(f"Top Titles at {facility_id} (by affected count):")
    print("-" * 40)
    if top_titles:
        for job_title, count in top_titles:
            print(f"  {count:>5}  {job_title}")
    else:
        print("  (No impact data for this facility)")
    print()

    # Where else title appears
    print(f"Where Else '{title}' Appears (top facilities):")
    print("-" * 40)
    if top_facilities:
        for fid, count in top_facilities:
            notices = sorted(facility_notices.get(fid, set()))
            print(f"  {count:>5}  {fid:<15}  notices={notices}")
    else:
        print("  (Title not found in impact dataset)")
    print()

    print("=" * 80)
    print()


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Assess facility and job title risk based on layoff notice data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --facility SEA40 --title "Program Manager III"
  %(prog)s --facility SEA93 --title "SDE II" --nearest 5 --radius_km 30
  %(prog)s --facility REMOTE_WA --title "Product Manager" --top 15

For more information, see docs/SPEC.md
        """,
    )

    parser.add_argument(
        "--facility",
        required=True,
        help="Facility ID (e.g., SEA40, SEA93, REMOTE_WA)",
    )

    parser.add_argument(
        "--title",
        required=True,
        help="Job title canonical string (exact match required)",
    )

    parser.add_argument(
        "--impacts",
        default=r"data\exports\impacts_by_facility.csv",
        help="Path to impacts CSV file (default: data/exports/impacts_by_facility.csv)",
    )

    parser.add_argument(
        "--facility_rollup",
        default=r"data\exports\facility_rollup.csv",
        help="Path to facility rollup CSV (default: data/exports/facility_rollup.csv)",
    )

    parser.add_argument(
        "--geocodes",
        default=r"data\normalized\facility_geocodes.csv",
        help="Path to geocodes CSV (default: data/normalized/facility_geocodes.csv)",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to show (default: 10)",
    )

    parser.add_argument(
        "--nearest",
        type=int,
        default=10,
        help="Number of nearest facilities to show (default: 10)",
    )

    parser.add_argument(
        "--radius_km",
        type=float,
        default=None,
        help="Radius in kilometers for proximity search (optional)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the risk assessment CLI.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        args = parse_arguments()

        # Configure logging level
        if args.verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")

        # Normalize inputs
        facility_id = args.facility.strip()
        title = args.title.strip()

        logger.info("Loading data files...")

        # Load data
        impacts = load_csv(args.impacts)
        facility_rollup = load_csv(args.facility_rollup)
        geocodes = load_geocodes_csv(args.geocodes)

        logger.info(f"Loaded {len(impacts)} impact records")
        logger.info(f"Loaded {len(facility_rollup)} facility records")
        logger.info(f"Loaded {len(geocodes)} geocode records")

        # Find facility metadata
        facility_metadata = find_facility_metadata(facility_id, facility_rollup)

        # Calculate direct match
        direct_total, direct_notices = calculate_direct_match(
            facility_id, title, impacts
        )

        # Get top titles at facility
        top_titles = get_top_titles_at_facility(facility_id, impacts, args.top)

        # Get top facilities for title
        top_facilities, facility_notices = get_top_facilities_for_title(
            title, impacts, args.top
        )

        # Print report
        print_report(
            facility_id,
            title,
            facility_metadata,
            direct_total,
            direct_notices,
            top_titles,
            top_facilities,
            facility_notices,
        )

        logger.info("Assessment complete")
        return 0

    except DataLoadError as e:
        logger.error(f"Data loading error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Assessment cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=args.verbose if 'args' in locals() else False)
        return 1


if __name__ == "__main__":
    sys.exit(main())
