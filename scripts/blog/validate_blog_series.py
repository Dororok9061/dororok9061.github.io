#!/usr/bin/env python3
from _common import SRC, fail, post_records, series_ids

ids = series_ids()
errors = []
for path, data, _ in post_records():
    if data.get("series") not in ids:
        errors.append(f"{path.name}: unknown series {data.get('series')}")
for series_id in ids:
    doc = SRC / "_blog_series" / f"{series_id}.md"
    if not doc.exists():
        errors.append(f"missing Korean collection document for {series_id}")
raise SystemExit(fail(errors))
