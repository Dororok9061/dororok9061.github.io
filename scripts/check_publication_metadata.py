#!/usr/bin/env python3
"""Validate the three source-backed conference-proceedings records."""
from pathlib import Path
import hashlib
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "src/_data/publications.yml").read_text(encoding="utf-8")
required = [
    "id: cics25-cnn-hrv",
    "CNN 기반 HRV 분석을 통한 인지 과제 수행 능력 예측에 관한 연구",
    "Classification of Cognitive Task Performance using HRV Features: A Convolutional Neural Network Approach",
    "Hyeong-Rok Ryu\n    - Woo-seok Kang\n    - Kyung-Ho Kim",
    "venue_ko: CICS’25 정보 및 제어 학술대회",
    "pages: 291–292",
    "dbpia_url: https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12564300",
    "dbpia_record_status: VERIFIED_PRESENT",
    "dbpia_url_status: VERIFIED_EXACT",
    "value: \"0.99\"",
    "value: \"0.992\"",
    "id: kiee2026-fmcw-aoac",
    "2026년도 대한전기학회 제57회 하계학술대회",
    "pages: 2413–2414",
    "page_verification_status: VERIFIED_FROM_PROCEEDINGS_PDF",
    "dbpia_record_status: NOT_FOUND_BY_EXACT_TITLE_SEARCH",
    "dbpia_url_status: NOT_VERIFIED",
    "value: 600 s",
    "value: \"848\"",
    "id: kiee2026-ultrasound-smartmirror",
    "개인용 체지방 관리를 위한 초음파 – 스마트미러 융합 기술에 대한 연구",
    "pages: 33–34",
    "user_author_position: 3",
    "author_count: 4",
]
errors = [f"missing metadata: {item}" for item in required if item not in text]
if text.count("type: Conference Proceedings Paper") != 3:
    errors.append("expected exactly three Conference Proceedings Paper records")
if text.count("presentation_type: Poster Presentation") != 2:
    errors.append("expected exactly two Poster Presentation records")
if text.count("user_author_position: 1") != 2:
    errors.append("expected first-author position for both records")
for banned in ("Journal Article", "SCI Paper", "SCIE Paper", "KCI Journal", "Peer-Reviewed Journal"):
    if banned in text:
        errors.append(f"misclassification found: {banned}")
if text.count("dbpia_record_status:") != 3 or text.count("dbpia_url_status:") != 3:
    errors.append("each publication must separate DBpia record and exact-URL status")
if text.count("dbpia_url: \"\"") + text.count("dbpia_url: ''") != 2:
    errors.append("FMCW and ultrasound DBpia URLs remain unverified")

records = {m.group(1): m.group(0) for m in re.finditer(r"(?m)^- id: ([^\n]+)\n.*?(?=^- id: |\Z)", text, re.S)}
expected = {
    "cics25-cnn-hrv": ("1", "3", "2025-10-22", "2025-10-23", "5aafd45b5cda413a8aa4b56e398d90b790b2f9f03bad9be6ee1c3ff88f717038"),
    "kiee2026-fmcw-aoac": ("1", "3", "2026-07-08", "2026-07-10", "3a0b9893af92a8d1330bcce34e8f459a36f2c3cb5548521da7cc037177b543ae"),
    "kiee2026-ultrasound-smartmirror": ("3", "4", "2026-07-08", "", "2866e3b2692fed811404ad948f88f8692f812887dcc7d960265065f5f08b94d2"),
}
for paper_id, (position, count, published, presented, digest) in expected.items():
    block = records.get(paper_id, "")
    fields = {m.group(1): m.group(2).strip().strip("\"'") for m in re.finditer(r"(?m)^  ([a-z_0-9]+): *(.*)$", block)}
    for key, value in {
        "user_author_position": position, "author_count": count,
        "published_date": published, "presentation_date": presented,
        "paper_pdf": f"/assets/papers/{paper_id}.pdf",
        "source_pdf_status": "USER_SUPPLIED_ORIGINAL", "source_pdf_pages": "2",
        "source_pdf_sha256": digest,
    }.items():
        if fields.get(key) != value:
            errors.append(f"{paper_id}: incorrect {key}")
    pdf = ROOT / "src/assets/papers" / f"{paper_id}.pdf"
    if not pdf.is_file() or hashlib.sha256(pdf.read_bytes()).hexdigest() != digest:
        errors.append(f"{paper_id}: original PDF missing or modified")
    if paper_id == "kiee2026-ultrasound-smartmirror":
        if fields.get("presentation_type") != "" or fields.get("status") != "published":
            errors.append("ultrasound paper must not inherit a poster-presentation claim")
        for author in ("손동민", "이정현", "류형록", "윤희철", "Dongmin Son", "Jeonghyun Lee", "Hyeongrok Ryu", "Heechul Yoon"):
            if f"- {author}" not in block:
                errors.append(f"ultrasound paper: missing author {author}")

if errors:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)
print("PASS: three original PDFs, two first-author papers, one third-author paper, exact dates, page ranges, and source-labeled metrics")
