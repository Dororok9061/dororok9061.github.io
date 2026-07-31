#!/usr/bin/env python3
from _common import SRC, fail

errors = []
for day in range(1, 6):
    for prefix in ("learning", "en/learning"):
        path = SRC / prefix / "bootcamps" / "kaist-generative-models-2025" / f"day-{day}" / "index.md"
        if not path.is_file(): errors.append(f"missing Day page {path.relative_to(SRC)}")
raise SystemExit(fail(errors))
