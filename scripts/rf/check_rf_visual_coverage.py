#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
catalog = json.loads((root / "src/_data/rfdh_study_series.yml").read_text(encoding="utf-8"))
errors = []
used = set()
for article in catalog["articles"]:
    if len(article.get("figures", [])) < 2:
        errors.append(f"{article['id']}: fewer than two figures")
    for public_path in article.get("figures", []):
        path = root / "src" / public_path.lstrip("/")
        used.add(path)
        if not path.is_file():
            errors.append(f"{article['id']}: missing {public_path}")
for path in used:
    text = path.read_text(encoding="utf-8")
    for token in ("viewBox=", "role=\"img\"", "<title", "<desc"):
        if token not in text:
            errors.append(f"{path.name}: missing {token}")
if len(used) < 15:
    errors.append(f"only {len(used)} distinct RF visuals")
if errors:
    raise SystemExit("\n".join(errors))
print(f"RF visual coverage: PASS ({len(used)} distinct SVGs, 2/article)")
