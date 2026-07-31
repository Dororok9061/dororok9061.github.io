#!/usr/bin/env python3
from _common import fail, post_records

records = {str(data.get("permalink")): (path, data) for path, data, _ in post_records()}
errors = []
for path, data, _ in post_records():
    alternate = str(data.get("alternate_url", ""))
    if alternate not in records:
        errors.append(f"{path.name}: alternate post missing {alternate}")
    elif records[alternate][1].get("translation_key") != data.get("translation_key"):
        errors.append(f"{path.name}: alternate translation key mismatch")
raise SystemExit(fail(errors))
