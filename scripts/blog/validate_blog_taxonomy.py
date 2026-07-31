#!/usr/bin/env python3
from _common import fail, post_records, taxonomy

tree = taxonomy()
errors = []
if len(tree) != 11:
    errors.append(f"expected 11 top categories including external-learning, found {len(tree)}")
for path, data, _ in post_records():
    primary = str(data.get("primary_category", ""))
    sub = str(data.get("subcategory", ""))
    if primary not in tree:
        errors.append(f"{path.name}: unknown primary_category {primary}")
    elif sub not in tree[primary]:
        errors.append(f"{path.name}: unknown subcategory {primary}/{sub}")
raise SystemExit(fail(errors))
