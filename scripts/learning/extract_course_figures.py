#!/usr/bin/env python3
from _common import fail
from _course_common import private_sources_not_republished

errors = [] if private_sources_not_republished() else ["private-source figure boundary changed"]
print("Figure extraction skipped: private and third-party source figures are not republished")
raise SystemExit(fail(errors))
