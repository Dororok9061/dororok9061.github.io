#!/usr/bin/env python3
from _common import ROOT, asset_paths, fail, post_records

errors = []
for path, _, body in post_records():
    text = path.read_text(encoding="utf-8")
    for asset in asset_paths(text):
        if not (ROOT / "src" / asset.lstrip("/")).is_file():
            errors.append(f"{path.name}: missing {asset}")
    if "<img" in body and not all(token in body for token in ("alt=", "width=", "height=")):
        errors.append(f"{path.name}: image missing alt or intrinsic dimensions")
raise SystemExit(fail(errors))
