#!/usr/bin/env python3
from __future__ import annotations

import csv
import json

from _common import fail
from _course_common import ROOT, scalar

counts = {
    "headings": int(scalar("source_heading_count")),
    "child_pages": int(scalar("source_child_pages")),
    "attachments": int(scalar("source_attachment_count")),
    "pptx": int(scalar("source_pptx_count")),
    "pdf": int(scalar("source_pdf_count")),
    "notebooks": int(scalar("source_notebook_count")),
    "colab_links": int(scalar("source_colab_count")),
}
errors = [] if counts["pptx"] + counts["pdf"] + counts["notebooks"] == counts["attachments"] else ["attachment type counts do not add up"]
out = ROOT / "work" / "generative-course"
out.mkdir(parents=True, exist_ok=True)
record = {"status": "CONNECTOR_SUMMARY_ONLY", "materialization": scalar("materialization_status"), "counts": counts}
(out / "source_block_inventory.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
with (out / "source_block_inventory.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle); writer.writerow(["status", *counts]); writer.writerow([record["status"], *counts.values()])
(out / "source_structure.md").write_text("# Generative course source structure\n\nOnly connector-level counts are available; block IDs and downloadable attachment URLs are not materialized.\n", encoding="utf-8")
raise SystemExit(fail(errors))
