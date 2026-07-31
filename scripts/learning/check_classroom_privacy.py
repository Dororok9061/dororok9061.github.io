#!/usr/bin/env python3
import re
from _common import fail, public_text

patterns = {
    "Classroom class URL": r"classroom\.google\.com/c/[A-Za-z0-9_-]+",
    "private Drive folder": r"drive\.google\.com/drive/folders/",
    "private Colab drive": r"colab\.research\.google\.com/drive/",
    "Zoom meeting": r"zoom\.us/j/",
    "class code": r"(?i)class\s*code\s*[:=]\s*[A-Za-z0-9_-]{5,}",
}
content = public_text()
errors = [name for name, pattern in patterns.items() if re.search(pattern, content)]
raise SystemExit(fail([f"private {name} exposed" for name in errors]))
