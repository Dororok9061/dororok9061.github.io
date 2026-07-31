#!/usr/bin/env python3
from _common import SRC, fail

path = SRC / "blog" / "search-index.json"
text = path.read_text(encoding="utf-8") if path.exists() else ""
required = ["title", "description", "category", "subcategory", "series", "tools", "tags", "headings", "date", "lang", "url"]
errors = [] if path.exists() else ["search-index.json missing"]
for key in required:
    if f'"{key}"' not in text:
        errors.append(f"search index missing {key}")
raise SystemExit(fail(errors))
