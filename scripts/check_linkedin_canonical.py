#!/usr/bin/env python3
"""Reject LinkedIn tracking URLs and private/internal Notion URLs."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://www.linkedin.com/in/hyeongrok-ryu-842231224/"
linkedin = re.compile(r"https://(?:www\.)?linkedin\.com/[^\s\"'<>)]*")
private_notion = re.compile(r"https?://(?:app\.)?notion\.(?:com|so|site)/", re.I)
SKIPPED_PARTS = {".git", "_site", "work", "vendor"}
TEXT_SUFFIXES = {".md", ".html", ".yml", ".yaml", ".json", ".txt"}


def scan_root(root: Path) -> tuple[int, list[str]]:
    """Scan repository files while applying exclusions to repo-relative paths."""
    errors: list[str] = []
    seen = 0
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if not path.is_file() or any(part in SKIPPED_PARTS for part in relative.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for url in linkedin.findall(text):
            seen += 1
            if url != CANONICAL:
                errors.append(f"{relative}: non-canonical LinkedIn URL")
        if private_notion.search(text):
            errors.append(f"{relative}: internal or unverified Notion URL")
    if not seen:
        errors.append("no LinkedIn URL found")
    return seen, errors


def main() -> int:
    seen, errors = scan_root(ROOT)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {seen} LinkedIn reference(s) use the canonical URL; internal Notion URLs: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
