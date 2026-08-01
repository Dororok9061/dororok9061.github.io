#!/usr/bin/env python3
from _common import fail
from _course_common import private_sources_not_republished, scalar

errors = [] if int(scalar("source_pdf_count")) == 13 and private_sources_not_republished() else ["PDF inventory or private-source boundary changed"]
print("PDF coverage: 13 source links inventoried; private files are not republished")
raise SystemExit(fail(errors))
