from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def blocks(path: str) -> list[str]:
    content = text(path)
    starts = [match.start() for match in re.finditer(r"(?m)^- id:\s*", content)]
    return [content[start:(starts[index + 1] if index + 1 < len(starts) else len(content))] for index, start in enumerate(starts)]


def field(block: str, name: str) -> str:
    match = re.search(rf"(?m)^\s{{2}}{re.escape(name)}:\s*(.*)$", block)
    return match.group(1).strip().strip("'\"") if match else ""


def fail(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"{len(errors)} blocking finding(s)")
        return 1
    print("PASS")
    return 0


def public_text() -> str:
    files = [path for path in SRC.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html", ".yml", ".yaml", ".js", ".json"}]
    return "\n".join(path.read_text(encoding="utf-8") for path in files)
