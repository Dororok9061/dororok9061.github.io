from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "intake" / "safe_zip_inventory.py"
SPEC = importlib.util.spec_from_file_location("safe_zip_inventory", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class SafeZipInventoryTests(unittest.TestCase):
    def test_rejects_traversal_and_windows_drive_paths(self) -> None:
        self.assertTrue(MODULE.unsafe_name("../secret.txt"))
        self.assertTrue(MODULE.unsafe_name("C:/secret.txt"))
        self.assertTrue(MODULE.unsafe_name("C:secret.txt"))
        self.assertTrue(MODULE.unsafe_name("notes.txt:hidden-stream"))
        self.assertFalse(MODULE.unsafe_name("Day 1/slides.pdf"))

    def test_inspects_and_extracts_regular_zip(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / "course.zip"
            with zipfile.ZipFile(archive, "w") as target:
                target.writestr("Day 1/notes.txt", "study")
            report = MODULE.inspect_archive(
                archive,
                max_members=10,
                max_total_bytes=1024,
                max_member_bytes=1024,
                max_ratio=100,
            )
            self.assertEqual([], report["findings"])
            destination = root / "extracted"
            MODULE.extract_archive(archive, destination, report)
            self.assertEqual("study", (destination / "Day 1" / "notes.txt").read_text())

    def test_refuses_extract_when_finding_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / "bad.zip"
            with zipfile.ZipFile(archive, "w") as target:
                target.writestr("../escape.txt", "no")
            report = MODULE.inspect_archive(
                archive,
                max_members=10,
                max_total_bytes=1024,
                max_member_bytes=1024,
                max_ratio=100,
            )
            with self.assertRaises(ValueError):
                MODULE.extract_archive(archive, root / "out", report)


if __name__ == "__main__":
    unittest.main()
