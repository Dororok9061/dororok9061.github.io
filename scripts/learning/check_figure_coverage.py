#!/usr/bin/env python3
from _common import fail
from _course_common import blocked_materialization

errors = [] if blocked_materialization() else ["figure coverage blocker missing"]
print("Figure coverage: BLOCKED_SOURCE_MATERIALIZATION; public figure count remains zero")
raise SystemExit(fail(errors))
