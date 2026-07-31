#!/usr/bin/env python3
import re
from _common import fail, post_records

errors = []
private = re.compile(r"(?i)(?:[A-Z]:\\Users\\|/Users/|/home/|classroom\.google\.com/c/|zoom\.us/j/|drive\.google\.com/drive/folders/)")
for path, data, _ in post_records():
    header = path.read_text(encoding="utf-8").split("---", 2)[1]
    if "source_materials:\n  -" not in header:
        errors.append(f"{path.name}: no source material entry")
    if private.search(path.read_text(encoding="utf-8")):
        errors.append(f"{path.name}: private source or local path")
raise SystemExit(fail(errors))
