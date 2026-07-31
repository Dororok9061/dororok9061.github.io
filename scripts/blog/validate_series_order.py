#!/usr/bin/env python3
from _common import fail, post_records

seen = set()
errors = []
for path, data, _ in post_records():
    key = (data.get("lang"), data.get("series"), data.get("series_order"))
    if key in seen:
        errors.append(f"{path.name}: duplicate series order {key}")
    seen.add(key)
raise SystemExit(fail(errors))
