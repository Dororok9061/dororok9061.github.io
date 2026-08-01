#!/usr/bin/env python3
"""Compatibility entry point for the canonical public-voice check."""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).resolve().parents[1] / "blog" / "check_human_study_voice.py"), run_name="__main__")
