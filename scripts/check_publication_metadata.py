#!/usr/bin/env python3
"""Validate the two evidence-backed conference-proceedings records."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/_data/publications.yml").read_text(encoding="utf-8")
required = [
    "id: cics25-cnn-hrv",
    "CNN 기반 HRV 분석을 통한 인지 과제 수행 능력 예측에 관한 연구",
    "Classification of Cognitive Task Performance using HRV Features: A Convolutional Neural Network Approach",
    "Hyeong-Rok Ryu\n    - Woo-Seok Kang\n    - Kyung-Ho Kim",
    "venue_ko: CICS’25 정보 및 제어 학술대회",
    "pages: 291–292",
    "dbpia_url: https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12564300",
    "dbpia_record_status: VERIFIED_PRESENT",
    "dbpia_url_status: VERIFIED_EXACT",
    "value: \"0.85\"",
    "value: \"0.82\"",
    "id: kiee2026-fmcw-aoac",
    "2026년도 대한전기학회 제57회 하계학술대회",
    "pages: 2413–2414",
    "page_verification_status: VERIFIED_FROM_PROCEEDINGS_PDF",
    "dbpia_record_status: NOT_FOUND_BY_EXACT_TITLE_SEARCH",
    "dbpia_url_status: NOT_VERIFIED",
    "value: 600 s",
    "value: \"848\"",
]
errors = [f"missing metadata: {item}" for item in required if item not in text]
if text.count("type: Conference Proceedings Paper") != 2:
    errors.append("expected exactly two Conference Proceedings Paper records")
if text.count("presentation_type: Poster Presentation") != 2:
    errors.append("expected exactly two Poster Presentation records")
if text.count("user_author_position: 1") != 2:
    errors.append("expected first-author position for both records")
for banned in ("Journal Article", "SCI Paper", "SCIE Paper", "KCI Journal", "Peer-Reviewed Journal"):
    if banned in text:
        errors.append(f"misclassification found: {banned}")
if text.count("dbpia_record_status:") != 2 or text.count("dbpia_url_status:") != 2:
    errors.append("each publication must separate DBpia record and exact-URL status")
if text.count("dbpia_url: \"\"") != 1:
    errors.append("only the FMCW DBpia URL may remain blank")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)
print("PASS: two first-author proceedings records, page ranges, and separate DBpia record/URL statuses are consistent")
