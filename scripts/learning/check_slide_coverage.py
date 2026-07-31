#!/usr/bin/env python3
from _common import fail
from _course_common import blocked_materialization, scalar

errors = [] if int(scalar("source_pptx_count")) > 0 and blocked_materialization() else ["slide coverage has neither materialized slides nor an explicit blocker"]
print("Slide coverage: BLOCKED_SOURCE_MATERIALIZATION; not reported as mapped")
raise SystemExit(fail(errors))
