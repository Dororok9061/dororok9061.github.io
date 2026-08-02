#!/usr/bin/env python3
import csv
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
index = (root / "src/_data/rfdh_source_index.yml").read_text(encoding="utf-8")
rows = list(csv.DictReader((root / "docs/internal/RFDH_TOPIC_COVERAGE.csv").open(encoding="utf-8-sig")))
errors = []
ids = re.findall(r"^  - id: \"([^\"]+)\"$", index, re.M)
urls = re.findall(r"^    url: \"(https://rfdh\.com/[^\"]+)\"$", index, re.M)
if len(rows) != 116 or len(ids) != 116 or len(urls) != 116:
    errors.append(f"expected 116 mappings; csv={len(rows)} ids={len(ids)} urls={len(urls)}")
if len(set(ids)) != len(ids) or len(set(urls)) != len(urls):
    errors.append("source ids or URLs are not unique")
for field in ("main_questions", "key_terms", "equations", "related_coursework", "related_blog_ko", "status", "last_reviewed"):
    if index.count(f"    {field}:") != 116:
        errors.append(f"{field}: incomplete per-page mapping")
if errors:
    raise SystemExit("\n".join(errors))
print("RFDH page mapping: PASS (116/116)")
