#!/usr/bin/env python3
import re

from _common import SRC, fail, post_records

REQUIRED = {"title", "description", "date", "updated", "lang", "translation_key", "alternate_url", "primary_category", "subcategory", "series", "series_order", "post_type", "difficulty", "study_status", "evidence_status", "tools", "source_materials", "related_projects", "tags", "thumbnail", "cover_image", "image_alt", "draft", "revision_history", "toc"}
TYPES = {"concept", "study-note", "tutorial", "lab", "project-log", "troubleshooting", "paper-review", "tool-guide", "retrospective", "methodology"}


def split_unquoted_commas(value: str) -> list[str]:
    parts: list[str] = []
    start = 0
    quote = ""
    for index, character in enumerate(value):
        if character in {"'", '"'}:
            quote = "" if quote == character else character if not quote else quote
        elif character == "," and not quote:
            parts.append(value[start:index])
            start = index + 1
    parts.append(value[start:])
    return parts


def bad_flow_map_lines(text: str) -> list[int]:
    result: list[int] = []
    for number, line in enumerate(text.splitlines(), 1):
        flow_map = re.match(r"^\s*-\s*\{(.*)\}\s*$", line)
        if flow_map and any(":" not in part for part in split_unquoted_commas(flow_map.group(1))):
            result.append(number)
    return result

errors = []
for path, data, body in post_records():
    header = path.read_text(encoding="utf-8").split("---", 2)[1]
    missing = sorted(key for key in REQUIRED if not data.get(key) and f"{key}:" not in header)
    if missing:
        errors.append(f"{path.name}: missing {', '.join(missing)}")
    if data.get("post_type") not in TYPES:
        errors.append(f"{path.name}: invalid post_type {data.get('post_type')}")
    if data.get("difficulty") not in {"beginner", "intermediate", "advanced"}:
        errors.append(f"{path.name}: invalid difficulty")
    if data.get("draft") is not False:
        errors.append(f"{path.name}: published post must set draft: false")
    for number in bad_flow_map_lines(header):
        errors.append(f"{path.name}:{number}: quote commas inside flow-map values")

series_path = SRC / "_data" / "blog_series.yml"
for number in bad_flow_map_lines(series_path.read_text(encoding="utf-8")):
    errors.append(f"{series_path.name}:{number}: quote commas inside flow-map values")
raise SystemExit(fail(errors))
