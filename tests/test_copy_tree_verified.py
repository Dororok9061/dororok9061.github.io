from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "intake" / "copy_tree_verified.py"
SPEC = importlib.util.spec_from_file_location("copy_tree_verified", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class CopyTreeVerifiedTests(unittest.TestCase):
    def test_copies_and_reuses_identical_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            (source / "notes.txt").write_text("study", encoding="utf-8")
            first = MODULE.copy_tree(source, destination)
            second = MODULE.copy_tree(source, destination)
            self.assertEqual("copied", first[0]["action"])
            self.assertEqual("reused", second[0]["action"])

    def test_refuses_to_overwrite_changed_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            destination.mkdir()
            (source / "notes.txt").write_text("source", encoding="utf-8")
            (destination / "notes.txt").write_text("changed", encoding="utf-8")
            with self.assertRaises(ValueError):
                MODULE.copy_tree(source, destination)


if __name__ == "__main__":
    unittest.main()
