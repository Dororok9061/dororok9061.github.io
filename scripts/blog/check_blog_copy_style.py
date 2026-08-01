#!/usr/bin/env python3
import re
from _common import fail, post_records

phrases = ["본 글에서는", "살펴보도록 하겠습니다", "매우 중요한 개념입니다", "혁신적인", "값진 경험이었습니다", "깊이 이해할 수 있었습니다", "in conclusion", "highly innovative"]
private = re.compile(r"(?i)(?:[A-Z]:\\Users\\|/Users/|/home/|학번\s*[:=]\s*\d{6,}|-----BEGIN .*PRIVATE KEY-----)")
errors = []
for path, _, body in post_records():
    for phrase in phrases:
        if body.lower().count(phrase.lower()) > 1:
            errors.append(f"{path.name}: repeated generic phrase {phrase}")
    if private.search(body):
        errors.append(f"{path.name}: private path, identifier, or key marker")
    if "\\[" in body or "\\]" in body:
        errors.append(f"{path.name}: unsupported display-LaTeX delimiter; use readable HTML text")
raise SystemExit(fail(errors))
