#!/usr/bin/env python3
from _common import fail
from _course_common import blocked_materialization, scalar

errors = [] if blocked_materialization() and int(scalar("source_pdf_count")) == 13 else ["PDF inventory or explicit materialization blocker missing"]
print(f"PDF inventory: {scalar('source_pdf_count')}; {scalar('materialization_status')}")
raise SystemExit(fail(errors))
