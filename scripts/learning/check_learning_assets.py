#!/usr/bin/env python3
from _common import SRC, fail

blocked = {".pdf", ".zip", ".7z", ".rar", ".ipynb", ".csv", ".wav", ".pth", ".pt"}
errors = [str(path.relative_to(SRC)) for path in SRC.rglob("*") if path.is_file() and path.suffix.lower() in blocked]
raise SystemExit(fail([f"restricted course/data asset in public source: {path}" for path in errors]))
