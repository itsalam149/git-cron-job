#!/usr/bin/env python3
"""
update.py - Automated Counter & Timestamp Updater

This script reads the current counter value from 'counter.txt', increments it by 1,
and writes back the updated counter alongside UTC and IST execution timestamps.

Designed for robust execution within CI/CD pipelines (such as GitHub Actions)
and local development environments.
"""

from datetime import datetime, timezone, timedelta
import os
import re
import sys
from pathlib import Path


def get_current_timestamps() -> tuple[datetime, datetime]:
    """Return current timestamps in UTC and Indian Standard Time (IST)."""
    now_utc = datetime.now(timezone.utc)
    ist_offset = timezone(timedelta(hours=5, minutes=30))
    now_ist = now_utc.astimezone(ist_offset)
    return now_utc, now_ist


def parse_counter(content: str) -> int:
    """
    Extract the numeric counter value from file content.
    
    Handles:
    - Raw integer values (e.g., '0', '  42  ')
    - Formatted lines (e.g., 'Count: 10')
    - Multi-line files with metadata
    - Empty or corrupt files (falls back safely to 0)
    """
    cleaned = content.strip()
    if not cleaned:
        print("[INFO] Counter file is empty. Initializing counter to 0.")
        return 0

    first_line = cleaned.splitlines()[0].strip()

    # Case 1: First line is a plain integer
    if first_line.isdigit():
        return int(first_line)

    # Case 2: Match 'Count: <number>' or standalone digits anywhere in the text
    match = re.search(r'(?:Count:\s*)?(\d+)', cleaned, re.IGNORECASE)
    if match:
        return int(match.group(1))

    print(f"[WARN] Unable to parse counter from content: '{cleaned[:50]}...'. Defaulting to 0.")
    return 0


def read_counter(file_path: Path) -> int:
    """Read and parse the counter from the target file."""
    if not file_path.exists():
        print(f"[INFO] '{file_path.name}' does not exist yet. It will be created with count 0.")
        return 0

    try:
        content = file_path.read_text(encoding="utf-8")
        return parse_counter(content)
    except Exception as e:
        print(f"[ERROR] Failed to read '{file_path}': {e}. Defaulting to 0.", file=sys.stderr)
        return 0


def write_counter(file_path: Path, new_count: int, now_utc: datetime, now_ist: datetime) -> None:
    """Write the updated counter and timestamp metadata to the file."""
    utc_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    ist_str = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")

    file_content = (
        f"Count: {new_count}\n"
        f"Last Updated (UTC): {utc_str}\n"
        f"Last Updated (IST): {ist_str}\n"
        f"Total Executions: {new_count}\n"
    )

    try:
        file_path.write_text(file_content, encoding="utf-8")
        print(f"[SUCCESS] Updated '{file_path.name}': Count = {new_count}")
        print(f"          UTC: {utc_str}")
        print(f"          IST: {ist_str}")
    except Exception as e:
        print(f"[ERROR] Failed to write to '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main execution flow for updating the counter file."""
    # Resolve file path relative to this script's directory
    base_dir = Path(__file__).resolve().parent
    target_file = base_dir / "counter.txt"

    print("=" * 60)
    print(" GitHub Automation: Counter & Activity Updater")
    print("=" * 60)

    now_utc, now_ist = get_current_timestamps()
    current_count = read_counter(target_file)
    new_count = current_count + 1

    print(f"[INFO] Current count : {current_count}")
    print(f"[INFO] New count     : {new_count}")

    write_counter(target_file, new_count, now_utc, now_ist)
    print("=" * 60)


if __name__ == "__main__":
    main()
