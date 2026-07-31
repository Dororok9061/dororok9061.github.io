#!/usr/bin/env python3
from _common import SRC, fail

pairs = [
    ("learning/index.md", "en/learning/index.md"),
    ("learning/bootcamps/index.md", "en/learning/bootcamps/index.md"),
    ("learning/competitions/index.md", "en/learning/competitions/index.md"),
    ("learning/bootcamps/kaist-generative-models-2025/index.md", "en/learning/bootcamps/kaist-generative-models-2025/index.md"),
    ("learning/bootcamps/kaist-generative-models-2025/day-1/index.md", "en/learning/bootcamps/kaist-generative-models-2025/day-1/index.md"),
    ("learning/bootcamps/kaist-generative-models-2025/day-2/index.md", "en/learning/bootcamps/kaist-generative-models-2025/day-2/index.md"),
    ("learning/bootcamps/kaist-generative-models-2025/day-3/index.md", "en/learning/bootcamps/kaist-generative-models-2025/day-3/index.md"),
    ("learning/bootcamps/kaist-generative-models-2025/day-4/index.md", "en/learning/bootcamps/kaist-generative-models-2025/day-4/index.md"),
    ("learning/bootcamps/kaist-generative-models-2025/day-5/index.md", "en/learning/bootcamps/kaist-generative-models-2025/day-5/index.md"),
    ("learning/bootcamps/outta-basic-2024/index.md", "en/learning/bootcamps/outta-basic-2024/index.md"),
    ("learning/classroom/index.md", "en/learning/classroom/index.md"),
    ("learning/competitions/outta-basic-p1/index.md", "en/learning/competitions/outta-basic-p1/index.md"),
    ("learning/competitions/outta-basic-p2/index.md", "en/learning/competitions/outta-basic-p2/index.md"),
    ("learning/competitions/outta-basic-p3/index.md", "en/learning/competitions/outta-basic-p3/index.md"),
]
errors = [f"missing i18n pair {left} / {right}" for left, right in pairs if not (SRC / left).is_file() or not (SRC / right).is_file()]
raise SystemExit(fail(errors))
