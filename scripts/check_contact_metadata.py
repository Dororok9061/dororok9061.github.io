#!/usr/bin/env python3
"""Validate approved public contact metadata and bilingual page wiring."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
profile = (ROOT / "src/_data/profile.yml").read_text(encoding="utf-8")
required = {
    "email": "email: hnryu0515@gmail.com",
    "linkedin": "linkedin: https://www.linkedin.com/in/hyeongrok-ryu-842231224/",
    "graduation": "expected_graduation_iso: 2027-02-25",
    "availability": "available_from_iso: 2027-01",
    "degree": "B.S. Candidate in Electrical and Electronic Engineering, Dankook University",
    "public Notion URL": "public_notion_url: https://fierce-rodent-308.notion.site/Engineering-Portfolio-FPGA-Radar-Embedded-Systems-Biomedical-AI-3ab518ac7a598121b666e4c7cce8324c",
    "public Notion status": "public_notion_status: VERIFIED_PUBLIC_2026-08-01",
}
errors = [f"profile missing {name}" for name, value in required.items() if value not in profile]

for relative in ("src/contact/index.md", "src/en/contact/index.md"):
    if not (ROOT / relative).is_file():
        errors.append(f"missing {relative}")

render_sources = "\n".join(
    path.read_text(encoding="utf-8")
    for path in (ROOT / "src/_layouts").glob("*.html")
)
for token in ("mailto:{{ profile.email }}", "{{ profile.linkedin }}", "{{ profile.expected_graduation_", "{{ profile.available_from_"):
    if token not in render_sources:
        errors.append(f"layouts do not render {token}")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)
print("PASS: approved contact, degree, dates, and verified public Notion metadata are wired to KO/EN pages")
