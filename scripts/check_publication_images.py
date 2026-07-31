#!/usr/bin/env python3
"""Validate publication-preview presence, size, and metadata stripping."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
assets = [
    ROOT / "src/assets/img/publications/cics25_cnn_first_page.jpg",
    ROOT / "src/assets/img/publications/cics25_cnn_first_page.webp",
]
errors: list[str] = []
for asset in assets:
    if not asset.is_file():
        errors.append(f"missing {asset.relative_to(ROOT)}")
        continue
    data = asset.read_bytes()
    if len(data) > 1_000_000:
        errors.append(f"{asset.name} exceeds 1 MB")
    if b"Exif\x00\x00" in data or b"EXIF" in data[:128]:
        errors.append(f"{asset.name} contains EXIF metadata")

publications = (ROOT / "src/_data/publications.yml").read_text(encoding="utf-8")
for token in ("cover_alt_ko:", "cover_alt_en:", "cover_width: 1132", "cover_height: 1600"):
    if token not in publications:
        errors.append(f"publication image metadata missing {token}")
if "id: kiee2026-fmcw-aoac" not in publications or "cover_image: \"\"" not in publications:
    errors.append("missing FMCW source image must stay explicitly empty")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)
print("PASS: available CICS first-page previews exist, are below 1 MB, and contain no EXIF marker; FMCW preview remains blocked")
