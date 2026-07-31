"""Build small, secret-free review notebooks from verified rerun reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import nbformat
from nbclient import NotebookClient


PROJECTS = {
    "p1": {
        "title": "OUTTA Basic P1 — improved image classification",
        "script": "p1_improved.py",
        "command": """data_root = os.environ.get('OUTTA_P1_ROOT')
if RUN_FULL_RERUN:
    if not data_root:
        raise RuntimeError('Set OUTTA_P1_ROOT to the dataset directory')
    subprocess.run([sys.executable, 'p1_improved.py', '--data-root', data_root, '--output-dir', 'work/p1'], check=True)
else:
    print('Review mode: set RUN_FULL_RERUN=True and OUTTA_P1_ROOT to reproduce.')""",
    },
    "p2": {
        "title": "OUTTA Basic P2 — improved fake-job classification",
        "script": "p2_improved.py",
        "command": """required = ['OUTTA_P2_TRAIN', 'OUTTA_P2_TEST', 'OUTTA_P2_SAMPLE']
paths = {name: os.environ.get(name) for name in required}
if RUN_FULL_RERUN:
    missing = [name for name, value in paths.items() if not value]
    if missing:
        raise RuntimeError(f'Set environment variables: {missing}')
    subprocess.run([sys.executable, 'p2_improved.py', '--train-csv', paths['OUTTA_P2_TRAIN'], '--test-csv', paths['OUTTA_P2_TEST'], '--sample-csv', paths['OUTTA_P2_SAMPLE'], '--output-dir', 'work/p2'], check=True)
else:
    print('Review mode: set RUN_FULL_RERUN=True and the three OUTTA_P2_* paths to reproduce.')""",
    },
    "p3": {
        "title": "OUTTA Basic P3 — improved music-genre classification",
        "script": "p3_improved.py",
        "command": """data_root = os.environ.get('OUTTA_P3_ROOT')
if RUN_FULL_RERUN:
    if not data_root:
        raise RuntimeError('Set OUTTA_P3_ROOT to the dataset directory')
    subprocess.run([sys.executable, 'p3_improved.py', '--data-root', data_root, '--output-dir', 'work/p3'], check=True)
else:
    print('Review mode: set RUN_FULL_RERUN=True and OUTTA_P3_ROOT to reproduce.')""",
    },
}


def build(project: str, config: dict[str, str], report: dict, output: Path) -> None:
    report_json = json.dumps(report, ensure_ascii=False)
    notebook = nbformat.v4.new_notebook(
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": report["runtime"]["python"]},
        }
    )
    notebook.cells = [
        nbformat.v4.new_markdown_cell(
            f"# {config['title']}\n\n"
            "This is a sanitized derivative notebook. The supplied original remains unchanged. "
            "Course datasets, raw course cells, credentials, and Kaggle account data are not embedded. "
            "Reported scores are local holdout evidence, not leaderboard scores."
        ),
        nbformat.v4.new_code_cell(
            "import json, os, subprocess, sys\n"
            f"result = json.loads({report_json!r})\n"
            "print('Evidence:', result['evidence_status'])\n"
            "print('Baseline:', result['baseline'])\n"
            "print('Improved:', result['improved'])\n"
            "print('Leaderboard:', result['leaderboard_status'])\n"
            "assert result['evidence_status'] == 'LOCAL_STRATIFIED_HOLDOUT_REPRODUCED'\n"
            "assert result['improved']['accuracy'] > result['baseline']['accuracy']"
        ),
        nbformat.v4.new_markdown_cell(
            "## Full rerun\n\n"
            f"The maintained implementation is `{config['script']}`. Set local dataset paths through "
            "environment variables, then opt in below. Generated datasets, caches, models, and submissions stay outside Git."
        ),
        nbformat.v4.new_code_cell("RUN_FULL_RERUN = False\n" + config["command"]),
    ]
    client = NotebookClient(notebook, timeout=120, kernel_name="python3")
    executed = client.execute(cwd=str(output.parent))
    nbformat.write(executed, output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("notebooks"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for project, config in PROJECTS.items():
        report_path = args.results_root / project / f"{project}_results.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        build(project, config, report, args.output_dir / f"{project}_improved.ipynb")


if __name__ == "__main__":
    main()
