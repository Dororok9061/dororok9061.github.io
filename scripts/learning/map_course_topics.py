#!/usr/bin/env python3
from _common import fail
from _course_common import course_text, require

errors = require(["day: 1", "day: 2", "day: 3", "day: 4", "day: 5", "SOURCE_MAPPED", "BLOCKED_SOURCE_DAY_HEADING_ABSENT", "unassigned_source_topics:"])
raise SystemExit(fail(errors))
