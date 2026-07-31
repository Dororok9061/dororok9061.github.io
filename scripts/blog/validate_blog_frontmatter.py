#!/usr/bin/env python3
from _common import fail, post_records

REQUIRED = {"title", "description", "date", "updated", "lang", "translation_key", "alternate_url", "primary_category", "subcategory", "series", "series_order", "post_type", "difficulty", "study_status", "evidence_status", "tools", "source_materials", "related_projects", "tags", "draft", "revision_history", "toc"}
TYPES = {"concept", "study-note", "tutorial", "lab", "project-log", "troubleshooting", "paper-review", "tool-guide", "retrospective", "methodology"}

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
raise SystemExit(fail(errors))
