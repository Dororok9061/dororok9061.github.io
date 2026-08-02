#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
catalog = json.loads((root / "src/_data/rfdh_study_series.yml").read_text(encoding="utf-8"))
errors = []
official_domains = ("www.itu.int", "www.keysight.com", "www.analog.com", "www.ti.com")
for item in catalog["articles"]:
    if not any(source.get("url", "").startswith("https://rfdh.com/") for source in item.get("sources", [])):
        errors.append(f"{item['id']}: RFDH attribution missing")
    official_sources = item.get("official_sources", [])
    if not official_sources:
        errors.append(f"{item['id']}: official cross-check source missing")
    for source in official_sources:
        url = source.get("url", "")
        if not url.startswith(tuple(f"https://{domain}/" for domain in official_domains)):
            errors.append(f"{item['id']}: non-official reference domain: {url}")
asset_root = root / "src/assets/images/study/rf-rfdh"
for path in asset_root.rglob("*"):
    if path.is_file() and path.suffix.lower() not in {".svg"}:
        errors.append(f"unexpected copied binary under RF redraw assets: {path}")
for path in asset_root.rglob("*.svg"):
    if "RF designhouse" in path.read_text(encoding="utf-8", errors="ignore"):
        errors.append(f"possible copied source content: {path}")
if errors:
    raise SystemExit("\n".join(errors))
print("RFDH attribution: PASS (RFDH + official references; original SVG-only public assets)")
