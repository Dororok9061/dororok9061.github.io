#!/usr/bin/env python3
from _common import fail
from _course_common import private_sources_not_republished, scalar

errors = [] if int(scalar("source_pptx_count")) == 11 and private_sources_not_republished() else ["PPTX inventory or private-source boundary changed"]
print("Slide coverage: 11 source links inventoried; private files are not republished")
raise SystemExit(fail(errors))
