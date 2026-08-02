#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[2]
catalog = json.loads((root / "src/_data/rfdh_study_series.yml").read_text(encoding="utf-8"))
articles = catalog.get("articles", [])
series = catalog.get("series", [])
errors = []
counts = Counter(item.get("group") for item in articles)
if len(articles) != 32 or counts != Counter({"core": 12, "smith-chart": 10, "circuit-blocks": 10}):
    errors.append(f"unexpected depth: {len(articles)} {dict(counts)}")
for item in articles:
    for key in ("title_ko", "title_en"):
        if len(item.get(key, "")) < 5:
            errors.append(f"{item.get('id')}: shallow {key}")
    for key in ("focus_ko", "focus_en", "concept_ko", "concept_en", "example_ko", "example_en", "connection_ko", "connection_en", "caution_ko", "caution_en"):
        if len(item.get(key, "")) < 20:
            errors.append(f"{item.get('id')}: shallow {key}")
    if len(item.get("formulas", [])) < 2 or len(item.get("figures", [])) < 2 or not item.get("sources"):
        errors.append(f"{item.get('id')}: formula, visual, or source depth missing")
    if not item.get("url_ko", "").startswith("/blog/rf/") or not item.get("url_en", "").startswith("/en/blog/rf/"):
        errors.append(f"{item.get('id')}: route mismatch")
article_ids = {item.get("id") for item in articles}
expected_series = {
    "rfdh-rf-foundations", "rf-impedance-sparameters", "smith-chart-matching",
    "rf-linearity", "rf-circuit-blocks",
}
if {item.get("id") for item in series} != expected_series:
    errors.append("five required RF series are not defined")
for item in series:
    if not item.get("article_ids") or not set(item["article_ids"]).issubset(article_ids):
        errors.append(f"{item.get('id')}: empty or invalid series membership")
    for key in ("title_ko", "title_en", "description_ko", "description_en"):
        if len(item.get(key, "")) < 10:
            errors.append(f"{item.get('id')}: shallow {key}")
if errors:
    raise SystemExit("\n".join(errors))
print("RF category depth: PASS (32 bilingual articles, 5 bilingual series)")
