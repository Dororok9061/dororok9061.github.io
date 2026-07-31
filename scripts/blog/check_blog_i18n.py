#!/usr/bin/env python3
from collections import defaultdict
from _common import fail, post_records

pairs = defaultdict(list)
for path, data, _ in post_records():
    pairs[str(data.get("translation_key"))].append((path, data))
errors = []
for key, rows in pairs.items():
    langs = {row[1].get("lang") for row in rows}
    if langs != {"ko", "en"} or len(rows) != 2:
        errors.append(f"{key}: expected one KO and one EN post")
        continue
    values = {(row[1].get("series"), row[1].get("series_order"), row[1].get("evidence_status")) for row in rows}
    if len(values) != 1:
        errors.append(f"{key}: series/order/evidence mismatch")
raise SystemExit(fail(errors))
