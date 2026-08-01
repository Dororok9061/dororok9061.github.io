#!/usr/bin/env python3
"""Validate generated coursework and PADS/STM32/mmWave study hubs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _common import ROOT, SRC, fail


COURSES = SRC / "_data" / "coursework_courses.yml"
TRACKS = SRC / "_data" / "engineering_tracks.yml"


def course_routes(text: str) -> list[tuple[str, int, str]]:
    routes: list[tuple[str, int, str]] = []
    course_id = ""
    order: int | None = None
    for line in text.splitlines():
        top = re.match(r"^- id:\s*([^\s]+)", line)
        if top:
            course_id = top.group(1)
            continue
        unit_order = re.match(r"^    - order:\s*(\d+)", line)
        if unit_order:
            order = int(unit_order.group(1))
            continue
        slug = re.match(r"^      slug:\s*([^\s]+)", line)
        if slug and course_id and order is not None:
            routes.append((course_id, order, slug.group(1)))
            order = None
    return routes


def track_routes(text: str) -> list[tuple[str, str]]:
    routes: list[tuple[str, str]] = []
    track_id = ""
    block_unit = False
    for line in text.splitlines():
        top = re.match(r"^- id:\s*([^\s]+)", line)
        if top:
            track_id = top.group(1)
            continue
        unit = re.match(r"^    - \{ order:\s*\d+, slug:\s*([^,\s]+)", line)
        if unit and track_id:
            routes.append((track_id, unit.group(1)))
            block_unit = False
            continue
        if re.match(r"^    - order:\s*\d+", line):
            block_unit = True
            continue
        slug = re.match(r"^      slug:\s*([^\s]+)", line)
        if slug and track_id and block_unit:
            routes.append((track_id, slug.group(1)))
            block_unit = False
    return routes


def main() -> int:
    course_text = COURSES.read_text(encoding="utf-8")
    track_text = TRACKS.read_text(encoding="utf-8")
    errors: list[str] = []
    course_ids = re.findall(r"(?m)^- id:\s*([^\s]+)", course_text)
    track_ids = re.findall(r"(?m)^- id:\s*([^\s]+)", track_text)
    courses = course_routes(course_text)
    tracks = track_routes(track_text)
    if len(course_ids) != 11:
        errors.append(f"expected 11 coursework hubs, found {len(course_ids)}")
    if len(courses) != 120:
        errors.append(f"expected 120 source-supported coursework units, found {len(courses)}")
    if any(course_id == "embedded-systems" for course_id, _, _ in courses):
        errors.append("embedded-systems must not publish generic units without course files")
    if len(track_ids) != 3:
        errors.append(f"expected 3 engineering tracks, found {len(track_ids)}")
    if len(tracks) != 24:
        errors.append(f"expected 24 engineering track units, found {len(tracks)}")

    assets = set(re.findall(r"(?m)^\s+(?:thumbnail|image):\s*(/assets/\S+)", course_text + "\n" + track_text))
    for asset in sorted(assets):
        if not (SRC / asset.lstrip("/")).is_file():
            errors.append(f"missing study asset {asset}")

    if len(set(course_ids)) != len(course_ids):
        errors.append("duplicate coursework id")
    if len(set(track_ids)) != len(track_ids):
        errors.append("duplicate engineering track id")
    if len(set(courses)) != len(courses):
        errors.append("duplicate coursework unit route")
    if len(set(tracks)) != len(tracks):
        errors.append("duplicate engineering track route")

    stm32_facts = (
        "실험 사진 22장",
        "STM 사용법 40장",
        "3쪽 KiCad 회로도",
        "ADC·TIM1·UART 코드",
        "TIM1 update interrupt",
        "/assets/images/study/stm32/stm32-prototype-overview.webp",
        "/assets/images/study/stm32/biosignal-schematic.webp",
    )
    for fact in stm32_facts:
        if fact not in track_text:
            errors.append(f"missing source-faithful STM32 fact: {fact}")
    for fact in ("정지사진 19장과 영상 99개", "twenty board sets", "stm32f411-board-overview.webp", "f411_1-contact-sheet.webp"):
        if fact.lower() in track_text.lower():
            errors.append(f"obsolete PCB-inspection STM32 fact remains: {fact}")

    if len(sys.argv) > 1:
        site = Path(sys.argv[1])
        for course_id in course_ids:
            for prefix in ("", "en"):
                route = site / prefix / "coursework" / course_id / "index.html"
                if not route.is_file():
                    errors.append(f"missing generated route {route.relative_to(site)}")
        for course_id, order, slug in courses:
            segment = f"week-{order:02d}-{slug}"
            for prefix in ("", "en"):
                route = site / prefix / "coursework" / course_id / segment / "index.html"
                if not route.is_file():
                    errors.append(f"missing generated route {route.relative_to(site)}")
        for track_id in track_ids:
            for prefix in ("", "en"):
                route = site / prefix / "study" / track_id / "index.html"
                if not route.is_file():
                    errors.append(f"missing generated route {route.relative_to(site)}")
        for track_id, slug in tracks:
            for prefix in ("", "en"):
                route = site / prefix / "study" / track_id / slug / "index.html"
                if not route.is_file():
                    errors.append(f"missing generated route {route.relative_to(site)}")

    if not errors:
        print(f"PASS: {len(course_ids)} courses, {len(courses)} units, {len(track_ids)} tracks, {len(tracks)} track pages")
    return fail(errors)


if __name__ == "__main__":
    raise SystemExit(main())
