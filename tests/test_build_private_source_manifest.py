from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "intake" / "build_private_source_manifest.py"
SPEC = importlib.util.spec_from_file_location("build_private_source_manifest", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class PrivateSourceManifestTests(unittest.TestCase):
    def test_maps_course_and_outta_topics(self) -> None:
        self.assertEqual("control-systems", MODULE.topic_hint("university/자동제어/lecture.pdf"))
        self.assertEqual("outta-rnn-seq2seq", MODULE.topic_hint("outta/실습_9_3_seq2seq.ipynb"))

    def test_marks_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "a.txt").write_text("same", encoding="utf-8")
            (root / "b.txt").write_text("same", encoding="utf-8")
            records = MODULE.build(root)
            self.assertEqual("", records[0]["duplicate_of"])
            self.assertEqual("F_DUPLICATE", records[1]["classification"])


if __name__ == "__main__":
    unittest.main()
