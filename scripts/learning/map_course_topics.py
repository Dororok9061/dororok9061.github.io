#!/usr/bin/env python3
from _common import fail
from _course_common import require

errors = require(["day: 1", "day: 2", "day: 3", "day: 4", "day: 5", "EDITORIAL_STUDY_SEQUENCE", "PRIVATE_SOURCE_LINKS_NOT_REPUBLISHED"])
raise SystemExit(fail(errors))
