#!/usr/bin/env python3
from _common import blocks, fail, field

errors = []
for block in blocks("src/_data/learning_programs.yml"):
    program_id = block.splitlines()[0].split(":", 1)[1].strip()
    if "CERTIFICATE_VERIFIED" in field(block, "completion_status") and field(block, "certificate") != "VERIFIED_PRIVATE_ORIGINAL":
        errors.append(f"{program_id}: certificate claim has no private-original verification record")
raise SystemExit(fail(errors))
