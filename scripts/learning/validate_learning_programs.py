#!/usr/bin/env python3
from _common import blocks, fail, field

errors = []
seen = set()
for block in blocks("src/_data/learning_programs.yml"):
    program_id = field(block, "id") or block.splitlines()[0].split(":", 1)[1].strip()
    if program_id in seen:
        errors.append(f"duplicate program {program_id}")
    seen.add(program_id)
    for key in ("title_ko", "title_en", "provider", "type", "year", "completion_status", "certificate", "evidence_status", "project_evidence"):
        if not field(block, key):
            errors.append(f"{program_id}: missing {key}")
    if "CERTIFICATE_VERIFIED" in block and "VERIFIED_PRIVATE_ORIGINAL" not in block:
        errors.append(f"{program_id}: completion claim lacks verified private certificate record")
raise SystemExit(fail(errors))
