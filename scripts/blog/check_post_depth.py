#!/usr/bin/env python3
import re
from _common import fail, post_records

errors = []
for path, data, body in post_records():
    headings = re.findall(r"(?m)^##\s+", body)
    if len(headings) < 5:
        errors.append(f"{path.name}: fewer than five substantive sections")
    if "source_materials:" not in path.read_text(encoding="utf-8"):
        errors.append(f"{path.name}: source section absent")
    post_type = data.get("post_type")
    if post_type in {"project-log", "paper-review", "study-note"} and "<figure>" not in body:
        errors.append(f"{path.name}: source-backed visual absent")
    if post_type == "troubleshooting" and not all(word in body.lower() for word in ("error", "cause", "verification")):
        errors.append(f"{path.name}: troubleshooting structure incomplete")
raise SystemExit(fail(errors))
