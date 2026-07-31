#!/usr/bin/env python3
from _common import blocks, fail, field

errors = []
for block in blocks("src/_data/competitions.yml"):
    competition_id = block.splitlines()[0].split(":", 1)[1].strip()
    for key in ("title_ko", "title_en", "platform", "visibility", "source_evidence", "submission_status", "status"):
        if not field(block, key):
            errors.append(f"{competition_id}: missing {key}")
    if field(block, "submission_status") == "NOT_VERIFIED" and (field(block, "best_score") or field(block, "rank")):
        errors.append(f"{competition_id}: unverified competition has score or rank")
raise SystemExit(fail(errors))
