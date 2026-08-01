#!/usr/bin/env python3
"""Keep coursework covers in their own namespace and matched to course ids."""

from __future__ import annotations

from pathlib import Path

from provenance_common import courses, fail, public_asset


EMBEDDED_COVER = "/assets/images/study/coursework/embedded-systems-source-map.svg"
OLD_MISMATCHED_COVERS = (
    "/assets/images/study/coursework/digital-communications.webp",
    "/assets/images/study/coursework/electronic-circuits-1.webp",
    "/assets/images/study/coursework/electronic-circuits-2.webp",
    "/assets/images/study/coursework/embedded-systems.webp",
    "/assets/images/study/coursework/power-electronics.webp",
)


def main() -> int:
    records = courses()
    errors: list[str] = []
    for course in records:
        if course.thumbnail.startswith("/assets/images/projects/"):
            errors.append(f"{course.id} uses project image as coursework cover: {course.thumbnail}")
        expected_stem = "embedded-systems-source-map" if course.id == "embedded-systems" else course.id
        if Path(course.thumbnail).stem != expected_stem:
            errors.append(f"{course.id} cover slug does not match: {course.thumbnail}")
        if not public_asset(course.thumbnail).is_file():
            errors.append(f"{course.id} cover is missing: {course.thumbnail}")

    embedded = next((course for course in records if course.id == "embedded-systems"), None)
    if not embedded:
        errors.append("embedded-systems course record is missing")
    else:
        if embedded.thumbnail != EMBEDDED_COVER:
            errors.append(f"embedded-systems must use source map: {embedded.thumbnail}")
        if "/assets/images/projects/" in embedded.block:
            errors.append("embedded-systems course record reuses a project photo")
    for old_cover in OLD_MISMATCHED_COVERS:
        if (Path(__file__).resolve().parents[2] / "_site" / old_cover.removeprefix("/")).exists():
            errors.append(f"old mismatched cover remains public: {old_cover}")
    return fail(f"{len(records)} coursework covers match their categories", errors)


if __name__ == "__main__":
    raise SystemExit(main())
