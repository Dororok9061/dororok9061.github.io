#!/usr/bin/env python3
"""Check practical-post visuals and conservative image/category alignment."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
FIELDS = "order|slug|title_ko|title_en|image|alt_ko|alt_en|body_ko|body_en|concepts"


def split_front_matter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return "", text
    _, header, body = text.split("---", 2)
    return header, body


def scalar(header: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.*?)\s*$", header)
    return match.group(1).strip(" \"'") if match else ""


def blocks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    starts = list(re.finditer(r"(?m)^- id:\s*([^\s]+)\s*$", text))
    return [
        (match.group(1), text[match.start() : starts[index + 1].start() if index + 1 < len(starts) else len(text)])
        for index, match in enumerate(starts)
    ]


def unit_images(block: str) -> list[str]:
    units = re.search(r"(?ms)^  units:[ \t]*(.*?)(?=^  [a-z_]+:|\Z)", block)
    if not units:
        return []
    text = units.group(1)
    return re.findall(r"(?m)^\s+image:\s*(\S+)", text) + re.findall(
        r"(?:\{|,)\s*image:\s*([^,\n}]+)", text
    )


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "src"
    _site = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "_site"
    errors: list[str] = []
    practical = 0

    for path in sorted((src / "_posts").glob("*.md")):
        header, body = split_front_matter(path)
        if re.search(r"(?m)^(?:draft:\s*true|published:\s*false)\s*$", header):
            continue
        cover, thumbnail = scalar(header, "cover_image"), scalar(header, "thumbnail")
        if cover != thumbnail:
            errors.append(f"{path.name}: cover_image and thumbnail describe different assets")
        explicit_practical = bool(
            re.search(r"(?m)^post_type:\s*tutorial\s*$", header)
            or re.search(r"(?m)^(?:practical|tutorial):\s*true\s*$", header)
            or re.search(r"type:\s*(?:practical|tutorial|lab-notebook|exercise-notebook)\b", header)
        )
        if explicit_practical:
            practical += 1
            code_blocks = len(re.findall(r"(?m)^```|{%-?\s*highlight\b|<pre\b", body))
            visuals = len(re.findall(r"<figure\b|<img\b|!\[[^]]*\]\(", body))
            if code_blocks < 1:
                errors.append(f"{path.name}: practical tutorial has no code block")
            if visuals < 1:
                errors.append(f"{path.name}: practical tutorial has no visual")

    for course_id, block in blocks(src / "_data" / "coursework_courses.yml"):
        thumbnail_match = re.search(r"(?m)^  thumbnail:\s*(\S+)", block)
        thumbnail = thumbnail_match.group(1) if thumbnail_match else ""
        if not thumbnail.startswith("/assets/images/study/coursework/"):
            errors.append(f"course {course_id}: cover is outside coursework image namespace")

    track_count = 0
    for track_id, block in blocks(src / "_data" / "engineering_tracks.yml"):
        for image in unit_images(block):
            image = image.strip(" \"'")
            match = re.match(r"/assets/images/study/([^/]+)/", image)
            if match and match.group(1) != track_id:
                errors.append(f"track {track_id}: unit uses {match.group(1)} study asset {image}")
            track_count += 1

    if not _site.is_dir():
        errors.append("built site is missing")
    if practical == 0:
        errors.append("no explicit practical tutorial was checked")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {practical} explicit practical tutorials and {track_count} track visuals are aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
