from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
COURSE = SRC / "_data" / "courses" / "2025-generative-models.yml"


def course_text() -> str:
    return COURSE.read_text(encoding="utf-8")


def scalar(name: str) -> str:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+)$", course_text())
    return match.group(1).strip().strip('"\'') if match else ""


def require(tokens: list[str]) -> list[str]:
    content = course_text()
    return [f"course data missing {token}" for token in tokens if token not in content]


def private_sources_not_republished() -> bool:
    return scalar("materialization_status") == "PRIVATE_SOURCE_LINKS_NOT_REPUBLISHED"
