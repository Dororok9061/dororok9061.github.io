#!/usr/bin/env python3
"""Reject LinkedIn tracking URLs and private/internal Notion URLs."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = "https://www.linkedin.com/in/hyeongrok-ryu-842231224/"
linkedin = re.compile(r"https://(?:www\.)?linkedin\.com/[^\s\"'<>)]*")
private_notion = re.compile(r"https?://(?:app\.)?notion\.(?:com|so|site)/", re.I)
errors: list[str] = []
seen = 0
for path in ROOT.rglob("*"):
    relative = path.relative_to(ROOT)
    if not path.is_file() or any(part in {".git", "_site", "work", "vendor"} for part in relative.parts):
        continue
    if path.suffix.lower() not in {".md", ".html", ".yml", ".yaml", ".json", ".txt"}:
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

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)
print(f"PASS: {seen} LinkedIn reference(s) use the canonical URL; internal Notion URLs: 0")
