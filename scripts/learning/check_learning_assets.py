#!/usr/bin/env python3
import hashlib
from _common import SRC, fail

blocked = {".pdf", ".zip", ".7z", ".rar", ".ipynb", ".csv", ".wav", ".pth", ".pt"}
# The owner supplied these published papers for the portfolio on 2026-09-17.
# Permit only these exact files; private course PDFs and altered files stay blocked.
published_papers = {
    "assets/papers/cics25-cnn-hrv.pdf": "5aafd45b5cda413a8aa4b56e398d90b790b2f9f03bad9be6ee1c3ff88f717038",
    "assets/papers/kiee2026-fmcw-aoac.pdf": "3a0b9893af92a8d1330bcce34e8f459a36f2c3cb5548521da7cc037177b543ae",
    "assets/papers/kiee2026-ultrasound-smartmirror.pdf": "2866e3b2692fed811404ad948f88f8692f812887dcc7d960265065f5f08b94d2",
}
errors = []
for path in SRC.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in blocked:
        continue
    relative = path.relative_to(SRC).as_posix()
    expected = published_papers.get(relative)
    if expected and hashlib.sha256(path.read_bytes()).hexdigest() == expected:
        continue
    errors.append(relative)
raise SystemExit(fail([f"restricted course/data asset in public source: {path}" for path in errors]))
