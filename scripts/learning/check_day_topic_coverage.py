#!/usr/bin/env python3
from _common import fail
from _course_common import course_text

content = course_text()
errors = []
if content.count("mapping_status: SOURCE_MAPPED") != 1:
    errors.append("expected one explicitly source-mapped Day")
if content.count("mapping_status: BLOCKED_SOURCE_DAY_HEADING_ABSENT") != 4:
    errors.append("Days 2-5 must remain explicitly blocked")
if content.count("status: STUDIED_ONLY") != 3:
    errors.append("Day 1 source-mapped topic count changed")
raise SystemExit(fail(errors))
