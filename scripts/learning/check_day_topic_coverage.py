#!/usr/bin/env python3
import re

from _common import fail
from _course_common import course_text

content = course_text()
errors = []
days = [int(day) for day in re.findall(r"(?m)^  - day: (\d+)$", content)]
topic_ids = re.findall(r"(?m)^      - \{ id: ([^,]+),", content)
if days != [1, 2, 3, 4, 5]:
    errors.append("editorial study sequence must contain Days 1-5 once and in order")
if content.count("mapping_status: EDITORIAL_STUDY_SEQUENCE") != 5:
    errors.append("each Day must be labelled as an editorial study sequence")
if len(topic_ids) != 12 or len(set(topic_ids)) != 12:
    errors.append("expected 12 unique topic pages across the five-day sequence")
if "source_heading_count: 38" not in content:
    errors.append("source-page heading inventory changed")
raise SystemExit(fail(errors))
