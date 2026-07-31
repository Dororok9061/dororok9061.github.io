#!/usr/bin/env python3
import re
from _common import fail, public_text

content = public_text()
patterns = [
    r"(?i)kaggle\.json",
    r"KAGGLE_USERNAME\s*=",
    r"KAGGLE_KEY\s*=",
    r"KAGGLE_API_TOKEN\s*=",
    r"GOOGLE_API_KEY\s*=\s*['\"][^'\"]+['\"]",
    r"\bAIza[0-9A-Za-z_-]{20,}\b",
    r'"key"\s*:\s*"[A-Za-z0-9]{20,}"',
]
errors = ["Kaggle credential pattern detected" for pattern in patterns if re.search(pattern, content)]
raise SystemExit(fail(errors))
