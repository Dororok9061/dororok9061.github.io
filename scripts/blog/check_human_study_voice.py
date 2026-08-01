#!/usr/bin/env python3
"""Reject audit-report wording from public study pages."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLIC_SUFFIXES = {".html", ".markdown", ".md"}
EXCLUDED_PARTS = {
    ".git",
    "manifests",
    "scripts",
    "work",
}
EXCLUDED_NAMES = {"ci logs", "ci-logs", "ci_logs"}
EXCLUDED_PATHS = {
    ("docs", "qa"),
    ("docs", "security"),
}

FORBIDDEN = (
    "실제로 누락이 없으면",
    "누락이 있다면",
    "다음 형식으로 작성",
    "해당 자료",
    "해당 사용자",
    "공개 경계",
    "증거 경계",
    "근거 기록",
    "로컬 자료 감사",
    "기록합니다",
    "연결합니다",
    "관리합니다",
    "구분합니다",
    "근거를 연결합니다",
    "공개 근거",
    "검증 가능한",
    "지원하는 범위",
    "확인한 파일 안에서",
    "범위를 제한합니다",
    "주장하지 않습니다",
    "확대 해석하지 않습니다",
    "본 사이트에는",
    "이 정적 사이트에는",
    "한곳에서 확인할 수 있습니다",
    "저널로 분류하지 않습니다",
    "URL 검증 상태",
    "페이지 범위를 확인했습니다",
    "Evidence Status",
    "Remaining Source Materials",
    "Public Impact",
    "Exact Next Action",
    "SOURCE_INCOMPLETE",
    "UNDER_VERIFICATION",
    "CERTIFICATE_VERIFIED",
    "BLOCKED",
    "Section은 공개하지 않음",
    "검증 가능한 근거",
    "서로 다른 근거 단계",
    "현재 truthful status",
    "planned 상태",
    "수료증으로 확인한",
    "분리하여 기록합니다",
    "본 글에서는",
    "살펴보도록 하겠습니다",
    "매우 중요한",
    "혁신적인",
    "값진 경험",
    "깊이 이해",
    "최적의 솔루션",
    "미래를 선도",
    "Public Evidence",
    "Validation Boundary",
    "Documentation Policy",
    "provenance",
    "source-backed",
    "archived evidence",
    "privacy-reviewed",
    "traceable",
    "evidence boundary",
    "within supported scope",
    "not claimed",
    "separated provenance",
)


def public_files(path: Path):
    if path.is_file():
        if path.suffix.lower() in PUBLIC_SUFFIXES:
            yield path
        return
    for candidate in path.rglob("*"):
        if not candidate.is_file() or candidate.suffix.lower() not in PUBLIC_SUFFIXES:
            continue
        relative_parts_tuple = tuple(
            part.lower() for part in candidate.relative_to(path).parts
        )
        relative_parts = set(relative_parts_tuple)
        if relative_parts & EXCLUDED_PARTS or relative_parts & EXCLUDED_NAMES:
            continue
        if any(
            relative_parts_tuple[index : index + len(excluded)] == excluded
            for excluded in EXCLUDED_PATHS
            for index in range(len(relative_parts_tuple) - len(excluded) + 1)
        ):
            continue
        yield candidate


def is_unpublished(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False
    header = parts[1]
    return any(
        line.strip().casefold() in {"draft: true", "published: false"}
        for line in header.splitlines()
    )


def main(argv: list[str]) -> int:
    roots = [Path(item) for item in argv] or [ROOT / "src", ROOT / "_site"]
    findings: list[str] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in public_files(root):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            text = path.read_text(encoding="utf-8", errors="replace")
            if is_unpublished(text):
                continue
            folded = text.casefold()
            for phrase in FORBIDDEN:
                needle = phrase.casefold()
                start = 0
                while True:
                    index = folded.find(needle, start)
                    if index < 0:
                        break
                    line = text.count("\n", 0, index) + 1
                    findings.append(f"{path}:{line}: {phrase}")
                    start = index + len(needle)
    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        print(f"{len(findings)} public study-voice finding(s)")
        return 1
    print(f"PASS: {len(seen)} public Markdown/HTML files use reader-facing language")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
