#!/usr/bin/env python3
"""Check that structured course/track data produces complete public pages."""

from __future__ import annotations

from html import unescape
from pathlib import Path
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
FIELDS = (
    "order|slug|title_ko|title_en|image|alt_ko|alt_en|body_ko|body_en|concepts"
)


def blocks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    starts = list(re.finditer(r"(?m)^- id:\s*([^\s]+)\s*$", text))
    return [
        (match.group(1), text[match.start() : starts[index + 1].start() if index + 1 < len(starts) else len(text)])
        for index, match in enumerate(starts)
    ]


def section(block: str, name: str) -> str:
    match = re.search(rf"(?ms)^  {re.escape(name)}:[ \t]*(.*?)(?=^  [a-z_]+:|\Z)", block)
    return match.group(1) if match else ""


def records(value: str) -> list[str]:
    starts = list(re.finditer(r"(?m)^    - ", value))
    return [
        value[match.start() : starts[index + 1].start() if index + 1 < len(starts) else len(value)]
        for index, match in enumerate(starts)
    ]


def field(record: str, name: str) -> str:
    multiline = re.search(rf"(?m)^\s+-?\s*{re.escape(name)}:\s*(.*?)\s*$", record)
    if multiline:
        return multiline.group(1).strip(" \"'")
    inline = re.search(
        rf"(?:{{|,)\s*{re.escape(name)}:\s*(.*?)(?=,\s*(?:{FIELDS}):|\s*}}\s*$)",
        record,
        re.S,
    )
    return inline.group(1).strip(" \"'") if inline else ""


def concept_count(record: str) -> int:
    inline = field(record, "concepts")
    if inline.startswith("[") and inline.endswith("]"):
        return len([item for item in inline[1:-1].split(",") if item.strip()])
    return len(re.findall(r"(?m)^\s{8}- ", record))


def course_concepts(record: str, lang: str) -> list[str]:
    return [
        match.group(1).strip(" \"'")
        for match in re.finditer(rf"(?:{{|,)\s*{lang}:\s*([^,}}\n]+)", record)
    ]


def track_concepts(record: str) -> list[str]:
    value = field(record, "concepts")
    if value.startswith("[") and value.endswith("]"):
        return [item.strip(" \"'") for item in value[1:-1].split(",") if item.strip()]
    return []


def built(site: Path, *parts: str) -> bool:
    return site.joinpath(*parts, "index.html").is_file()


def built_text(site: Path, *parts: str) -> str:
    path = site.joinpath(*parts, "index.html")
    if not path.is_file():
        return ""
    return unescape(re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8", errors="replace")))


def meaningful_ko(value: str) -> bool:
    return len(re.findall(r"[A-Za-z0-9\uac00-\ud7a3]", value)) >= 24


def meaningful_en(value: str) -> bool:
    return len(re.findall(r"[A-Za-z0-9]+", value)) >= 8


def yaml_scalar(value: str) -> str:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return json.loads(value)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def coursework_notes(src: Path) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for path in sorted((src / "_data" / "coursework_unit_notes").glob("*.yml")):
        course_id = ""
        unit_slug = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            course_match = re.fullmatch(r"([a-z0-9-]+):", line)
            unit_match = re.fullmatch(r"  ([a-z0-9-]+):", line)
            field_match = re.fullmatch(
                r"    (body_ko|body_en|anchor_ko|anchor_en|practice_ko|practice_en):\s*(.+)", line
            )
            if course_match:
                course_id, unit_slug = course_match.group(1), ""
            elif unit_match and course_id:
                unit_slug = unit_match.group(1)
                key = (course_id, unit_slug)
                if key in result:
                    raise ValueError(f"duplicate coursework note: {course_id}/{unit_slug}")
                result[key] = {}
            elif field_match and course_id and unit_slug:
                result[(course_id, unit_slug)][field_match.group(1)] = yaml_scalar(field_match.group(2))
    return result


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "src"
    site = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "_site"
    errors: list[str] = []
    page_count = 0
    notes = coursework_notes(src)
    seen_note_bodies: set[tuple[str, str]] = set()

    for course_id, block in blocks(src / "_data" / "coursework_courses.yml"):
        kind_match = re.search(r"(?m)^  kind:\s*(\S+)", block)
        kind = kind_match.group(1) if kind_match else ""
        units = records(section(block, "units"))
        links = records(section(block, "separate_links"))
        if kind == "separated-course":
            if units or not links:
                errors.append(f"course {course_id}: separated course needs links and no generated units")
        elif not units:
            errors.append(f"course {course_id}: hub has no units")
        for lang in ("", "en"):
            prefix = (lang,) if lang else ()
            if not built(site, *prefix, "coursework", course_id):
                errors.append(f"missing built course hub: /{'en/' if lang else ''}coursework/{course_id}/")
            page_count += 1
        for unit in units:
            slug = field(unit, "slug")
            order = field(unit, "order")
            if not slug or not order or concept_count(unit) < 3:
                errors.append(f"course {course_id}: incomplete unit {slug or order or '?'}")
                continue
            note = notes.get((course_id, slug), {})
            required_note_fields = (
                "body_ko", "body_en", "anchor_ko", "anchor_en", "practice_ko", "practice_en"
            )
            if any(not note.get(name) for name in required_note_fields):
                errors.append(f"course {course_id}/{slug}: missing unit-specific bilingual note")
            elif (
                not meaningful_ko(note["body_ko"] + note["anchor_ko"] + note["practice_ko"])
                or not meaningful_en(note["body_en"] + note["anchor_en"] + note["practice_en"])
            ):
                errors.append(f"course {course_id}/{slug}: unit-specific note is too shallow")
            else:
                body_key = (note["body_ko"], note["body_en"])
                if body_key in seen_note_bodies:
                    errors.append(f"course {course_id}/{slug}: duplicate unit body")
                seen_note_bodies.add(body_key)
            route = f"week-{int(order):02d}-{slug}"
            for lang in ("", "en"):
                prefix = (lang,) if lang else ()
                if not built(site, *prefix, "coursework", course_id, route):
                    errors.append(f"missing built course unit: /{'en/' if lang else ''}coursework/{course_id}/{route}/")
                page = built_text(site, *prefix, "coursework", course_id, route)
                language = "en" if lang else "ko"
                expected = [
                    field(unit, f"title_{language}"),
                    *course_concepts(unit, language),
                    note.get(f"body_{language}", ""),
                    note.get(f"anchor_{language}", ""),
                    note.get(f"practice_{language}", ""),
                ]
                if any(value and value not in page for value in expected):
                    errors.append(f"course {course_id}/{route}: {language} unit concepts are not all rendered")
                page_count += 1

    for track_id, block in blocks(src / "_data" / "engineering_tracks.yml"):
        units = records(section(block, "units"))
        if not units:
            errors.append(f"track {track_id}: hub has no units")
        for lang in ("", "en"):
            prefix = (lang,) if lang else ()
            if not built(site, *prefix, "study", track_id):
                errors.append(f"missing built track hub: /{'en/' if lang else ''}study/{track_id}/")
            note_key = "source_note_en" if lang else "source_note_ko"
            note_match = re.search(rf"(?m)^  {note_key}:\s*(.+)$", block)
            note = note_match.group(1).strip() if note_match else ""
            if not note or note not in built_text(site, *prefix, "study", track_id):
                errors.append(f"track {track_id}: {note_key} is missing from the built hub")
            page_count += 1
        for unit in units:
            slug = field(unit, "slug")
            body_ko, body_en = field(unit, "body_ko"), field(unit, "body_en")
            if not slug:
                errors.append(f"track {track_id}: unit has no slug")
                continue
            if not meaningful_ko(body_ko) or not meaningful_en(body_en):
                errors.append(f"track {track_id}/{slug}: body is not meaningful in both languages")
            if concept_count(unit) < 3:
                errors.append(f"track {track_id}/{slug}: fewer than three concepts")
            for lang in ("", "en"):
                prefix = (lang,) if lang else ()
                if not built(site, *prefix, "study", track_id, slug):
                    errors.append(f"missing built track unit: /{'en/' if lang else ''}study/{track_id}/{slug}/")
                page = built_text(site, *prefix, "study", track_id, slug)
                language = "en" if lang else "ko"
                expected = [field(unit, f"title_{language}"), field(unit, f"body_{language}"), *track_concepts(unit)]
                if any(value and value not in page for value in expected):
                    errors.append(f"track {track_id}/{slug}: {language} unit details are not all rendered")
                page_count += 1

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {page_count} structured course and track pages align with source data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
