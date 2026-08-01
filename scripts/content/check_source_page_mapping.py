#!/usr/bin/env python3
"""Check private/public dispositions and mapped public page targets."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from check_full_file_coverage import (
    CSV_MAP,
    DISPOSITIONS,
    JSON_MAP,
    LEAK_RE,
    PAGE_BY_TOPIC,
    ROOT,
    read_maps,
    validate_snapshot,
)


PUBLIC_PAGE_RE = re.compile(r"/[a-z0-9][a-z0-9/_-]*/")


def built_page(site: Path, url: str) -> Path:
    return site / url.strip("/") / "index.html"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", nargs="?", type=Path, default=ROOT / "_site")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return nonzero until page/slide/sheet/cell and visual mappings are complete",
    )
    args = parser.parse_args()
    payload, rows, errors = read_maps()
    errors.extend(validate_snapshot(payload, rows))

    raw_maps = ""
    for path in (CSV_MAP, JSON_MAP):
        try:
            raw_maps += path.read_text(encoding="utf-8")
        except FileNotFoundError:
            pass
    if LEAK_RE.search(raw_maps):
        errors.append("serialized map contains a local path marker")

    allowed_pages = set(PAGE_BY_TOPIC.values())
    public_pages: set[str] = set()
    for row in rows:
        disposition = row.get("disposition")
        blog_url = row.get("blog_url")
        if disposition not in DISPOSITIONS:
            errors.append("disposition is not allowlisted")
            continue
        if row.get("notion_url") or row.get("github_url"):
            errors.append("unverified Notion or GitHub URL is populated")
        if disposition == "Private Master":
            if blog_url:
                errors.append("private source points to a public destination")
            continue
        if not blog_url:
            errors.append("public derivative has no public page mapping")
        elif blog_url not in allowed_pages or not PUBLIC_PAGE_RE.fullmatch(blog_url):
            errors.append("public destination is not allowlisted")
        else:
            public_pages.add(blog_url)

    if args.site.is_dir():
        for page in public_pages:
            if not built_page(args.site, page).is_file():
                errors.append(f"mapped public page is absent from build: {page}")
    else:
        print("DEGRADED: built site unavailable; page existence not checked")

    if errors:
        for error in dict.fromkeys(errors):
            print(f"FAIL: {error}")
        return 1
    private_count = sum(not row["blog_url"] for row in rows)
    public_count = len(rows) - private_count
    page_detail_missing = sum(not row.get("page_slide_sheet_cell") for row in rows)
    visual_source_types = {"dataset-image", "image-review"}
    visual_detail_missing = sum(
        row.get("file_type") in visual_source_types and not row.get("extracted_visual") for row in rows
    )
    print(
        f"PASS: {private_count} Private Master records and {public_count} public-derivative records "
        f"use allowlisted destinations"
    )
    if page_detail_missing or visual_detail_missing:
        print(
            f"INCOMPLETE: page/slide/sheet/cell={page_detail_missing}, "
            f"visual-source-detail={visual_detail_missing}"
        )
        return int(args.strict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
