#!/usr/bin/env python3
from _common import fail
from _course_common import private_sources_not_republished, scalar

errors = [] if private_sources_not_republished() and int(scalar("source_pdf_count")) == 13 else ["PDF inventory or private-source boundary changed"]
print(f"PDF inventory: {scalar('source_pdf_count')}; {scalar('materialization_status')}")
raise SystemExit(fail(errors))
