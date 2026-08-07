#!/usr/bin/env python3
"""Check bilingual recruitment dates against one ISO-backed profile record."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
profile = (ROOT / "src/_data/profile.yml").read_text(encoding="utf-8")
required = [
    "expected_graduation_ko: 2027년 2월 25일",
    "expected_graduation_en: February 25, 2027",
    "expected_graduation_iso: 2027-02-25",
    "available_from_ko: 2027년 1월",
    "available_from_en: January 2027",
    "available_from_iso: 2027-01",
]
errors = [f"missing or mismatched {value}" for value in required if value not in profile]
for relative in ("src/_layouts/home.html", "src/_layouts/about.html", "src/_layouts/contact.html"):
    text = (ROOT / relative).read_text(encoding="utf-8")
    if "profile.expected_graduation_" not in text or "profile.available_from_" not in text:
        errors.append(f"{relative} does not render both bilingual dates")
if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)
print("PASS: KO/EN expected-graduation and availability values share the approved ISO dates")
