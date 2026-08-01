#!/usr/bin/env python3
from pathlib import Path

from _common import SRC, fail
from _course_common import private_sources_not_republished

figure_dir = SRC / "assets" / "images" / "learning" / "generative"
figures = sorted(figure_dir.glob("*.svg"))
errors = []
if len(figures) != 5:
    errors.append("expected five original generative-model diagrams")
if not private_sources_not_republished():
    errors.append("private-source publication boundary changed")
if any(Path(path).suffix.lower() != ".svg" for path in figures):
    errors.append("generative-model diagrams must remain original SVG redraws")
print(f"Figure coverage: {len(figures)} original SVG redraws; source figures are not republished")
raise SystemExit(fail(errors))
