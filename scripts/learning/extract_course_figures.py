#!/usr/bin/env python3
from _common import fail
from _course_common import blocked_materialization

errors = [] if blocked_materialization() else ["figure extraction lacks an explicit source-material blocker"]
print("Figure extraction: BLOCKED; no private or third-party source figure is published")
raise SystemExit(fail(errors))
