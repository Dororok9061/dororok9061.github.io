#!/usr/bin/env python3
from _common import fail
from _course_common import blocked_materialization, scalar

errors = [] if blocked_materialization() and int(scalar("source_pptx_count")) == 11 else ["PPTX inventory or explicit materialization blocker missing"]
print(f"PPTX inventory: {scalar('source_pptx_count')}; {scalar('materialization_status')}")
raise SystemExit(fail(errors))
