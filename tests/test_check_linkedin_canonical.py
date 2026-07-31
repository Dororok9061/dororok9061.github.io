#!/usr/bin/env python3
"""Regression tests for repository-relative canonical-link scanning."""
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_linkedin_canonical.py"
SPEC = importlib.util.spec_from_file_location("check_linkedin_canonical", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CanonicalLinkScanTests(unittest.TestCase):
    def test_repository_under_work_parent_is_still_scanned(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary) / "work" / "repository"
            profile = root / "src/_data/profile.yml"
            profile.parent.mkdir(parents=True)
            profile.write_text(f"linkedin: {MODULE.CANONICAL}\n", encoding="utf-8")

            seen, errors = MODULE.scan_root(root)

            self.assertEqual(seen, 1)
            self.assertEqual(errors, [])

    def test_only_repository_relative_work_directory_is_excluded(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary) / "work" / "repository"
            profile = root / "src/_data/profile.yml"
            profile.parent.mkdir(parents=True)
            profile.write_text(f"linkedin: {MODULE.CANONICAL}\n", encoding="utf-8")
            ignored = root / "work/generated.txt"
            ignored.parent.mkdir(parents=True)
            ignored.write_text("https://linkedin.com/in/tracking-copy/\n", encoding="utf-8")

            seen, errors = MODULE.scan_root(root)

            self.assertEqual(seen, 1)
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
