#!/usr/bin/env python3
import re

from _common import fail, public_text

patterns = {
    "source Notion edit URL": r"app\.notion\.com/p/2025-257518ac",
    "meeting URL": r"(?:zoom\.us/j/|kaist\.zoom\.us/|pwd=)",
    "signed attachment": r"(?:X-Amz-Credential|X-Amz-Signature|prod-files-secure\.s3)",
    "private Drive or Colab": r"(?:drive\.google\.com/drive/folders/|colab\.research\.google\.com/drive/)",
    "Windows user path": r"[A-Za-z]:\\Users\\",
    "Google API key": r"\bAIza[0-9A-Za-z_-]{20,}\b",
}
content = public_text()
errors = [f"private course data detected: {name}" for name, pattern in patterns.items() if re.search(pattern, content, re.I)]
raise SystemExit(fail(errors))
