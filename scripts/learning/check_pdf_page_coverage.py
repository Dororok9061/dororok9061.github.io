#!/usr/bin/env python3
from _common import fail
from _course_common import blocked_materialization, scalar

errors = [] if int(scalar("source_pdf_count")) > 0 and blocked_materialization() else ["PDF page coverage has neither materialized pages nor an explicit blocker"]
print("PDF page coverage: BLOCKED_SOURCE_MATERIALIZATION; not reported as mapped")
raise SystemExit(fail(errors))
