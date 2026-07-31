#!/usr/bin/env python3
import re
from _common import fail, public_text

content = public_text()
patterns = {
    "local user path": r"(?i)[A-Z]:\\Users\\",
    "student identifier": r"(?i)(?:student\s*id|학번)\s*[:=]\s*\d{6,}",
    "raw certificate": r"(?i)certificate.*\.(?:pdf|png|jpg)",
    "competition data link": r"(?i)(?:train|test|sample_submission)\.(?:csv|zip)",
    "license file": r"(?i)license\.dat",
}
errors = [f"publication boundary violation: {name}" for name, pattern in patterns.items() if re.search(pattern, content)]
raise SystemExit(fail(errors))
