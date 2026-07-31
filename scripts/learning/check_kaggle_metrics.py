#!/usr/bin/env python3
from _common import blocks, fail, field

errors = []
for block in blocks("src/_data/competitions.yml"):
    competition_id = block.splitlines()[0].split(":", 1)[1].strip()
    score, rank = field(block, "best_score"), field(block, "rank")
    if score or rank:
        if "VERIFIED" not in field(block, "submission_status"):
            errors.append(f"{competition_id}: score/rank without verified submission")
        if not field(block, "metric"):
            errors.append(f"{competition_id}: score without metric")
raise SystemExit(fail(errors))
