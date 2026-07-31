#!/usr/bin/env python3
from _common import SRC, fail
from _course_common import scalar

raw = list(SRC.rglob("*.ipynb"))
errors = []
if int(scalar("source_notebook_count")) != 2:
    errors.append("source notebook inventory changed")
if raw:
    errors.append("raw notebook found in public source tree")
raise SystemExit(fail(errors))
