#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments" / "outta-basic-2024"
EXPECTED_ROWS = {"p1": 7172, "p2": 5364, "p3": 300}
errors = []

for project, expected_rows in EXPECTED_ROWS.items():
    report_path = BASE / "results" / f"{project}_results.json"
    notebook_path = BASE / "notebooks" / f"{project}_improved.ipynb"
    if not report_path.is_file() or not notebook_path.is_file():
        errors.append(f"{project}: missing report or notebook")
        continue
    report = json.loads(report_path.read_text(encoding="utf-8"))
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    if report.get("evidence_status") != "LOCAL_STRATIFIED_HOLDOUT_REPRODUCED":
        errors.append(f"{project}: invalid evidence status")
    if report.get("leaderboard_status") != "NOT_VERIFIED_NO_AUTHENTICATED_KAGGLE_SUBMISSION":
        errors.append(f"{project}: leaderboard boundary lost")
    if report.get("improved", {}).get("accuracy", -1) <= report.get("baseline", {}).get("accuracy", 1):
        errors.append(f"{project}: improved accuracy does not exceed baseline")
    submission = report.get("submission", {})
    if submission.get("rows") != expected_rows:
        errors.append(f"{project}: unexpected submission row count")
    if not re.fullmatch(r"[0-9a-f]{64}", submission.get("sha256", "")):
        errors.append(f"{project}: missing submission SHA-256")
    code_cells = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") == "code"]
    if not code_cells or any(output.get("output_type") == "error" for cell in code_cells for output in cell.get("outputs", [])):
        errors.append(f"{project}: notebook execution missing or contains an error")
    notebook_text = notebook_path.read_text(encoding="utf-8").lower()
    for forbidden in ("AIzaSy", "c:\\users\\user", "kaggle.json"):
        if forbidden.lower() in notebook_text:
            errors.append(f"{project}: forbidden private or secret token in notebook")

if (BASE / "results" / "submission_p1_improved.csv").exists():
    errors.append("submission files must not be committed")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("PASS: OUTTA rerun reports and sanitized notebooks")
