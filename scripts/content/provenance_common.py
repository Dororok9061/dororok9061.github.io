#!/usr/bin/env python3
"""Small stdlib helpers for public asset provenance checks."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
COURSES = SRC / "_data" / "coursework_courses.yml"
TRACKS = SRC / "_data" / "engineering_tracks.yml"
GEMFILE = ROOT / "Gemfile"
# A local asset path may be quoted or embedded in Liquid, but an external URL's
# path is preceded by the final hostname character (for example, `.com/assets`).
ASSET_RE = re.compile(r"(?<![A-Za-z0-9._-])/assets/[A-Za-z0-9_./%-]+")
PUBLIC_TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".md", ".rb", ".svg", ".xml", ".yml", ".yaml"}
THEME_ASSETS = {"/assets/style.css"}


@dataclass(frozen=True)
class Course:
    id: str
    kind: str
    thumbnail: str
    block: str


@dataclass(frozen=True)
class AssetReference:
    source: Path
    line: int
    asset: str


def yaml_blocks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    starts = list(re.finditer(r"(?m)^- id:\s*([^\s]+)\s*$", text))
    return [
        (match.group(1), text[match.start() : starts[index + 1].start() if index + 1 < len(starts) else len(text)])
        for index, match in enumerate(starts)
    ]


def scalar(block: str, name: str) -> str:
    match = re.search(rf"(?m)^  {re.escape(name)}:\s*(.*?)\s*$", block)
    return match.group(1).strip("\"'") if match else ""


def courses() -> list[Course]:
    return [
        Course(course_id, scalar(block, "kind"), scalar(block, "thumbnail"), block)
        for course_id, block in yaml_blocks(COURSES)
    ]


def track(track_id: str) -> str:
    return next((block for current_id, block in yaml_blocks(TRACKS) if current_id == track_id), "")


def asset_references() -> list[AssetReference]:
    references: list[AssetReference] = []
    for source in sorted(path for path in SRC.rglob("*") if path.is_file() and path.suffix.lower() in PUBLIC_TEXT_SUFFIXES):
        if "_plugins" in source.relative_to(SRC).parts:
            continue
        for line_number, line in enumerate(source.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            references.extend(AssetReference(source, line_number, match.group(0)) for match in ASSET_RE.finditer(line))
    return references


def public_asset(asset: str) -> Path:
    return SRC / asset.removeprefix("/")


def asset_exists(asset: str) -> bool:
    if public_asset(asset).is_file():
        return True
    gemfile = GEMFILE.read_text(encoding="utf-8")
    return asset in THEME_ASSETS and 'gem "jekyll-theme-simplex", "= 0.9.8.15"' in gemfile


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def fail(label: str, errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {label}")
    return 0
