#!/usr/bin/env python3
from _common import fail
from _course_common import private_sources_not_republished, scalar

errors = [] if private_sources_not_republished() and int(scalar("source_pptx_count")) == 11 else ["PPTX inventory or private-source boundary changed"]
print(f"PPTX inventory: {scalar('source_pptx_count')}; {scalar('materialization_status')}")
raise SystemExit(fail(errors))
