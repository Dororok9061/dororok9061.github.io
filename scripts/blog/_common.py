from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
POSTS = SRC / "_posts"


def front_matter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing front matter")
    _, header, body = text.split("---", 2)
    data: dict[str, object] = {}
    for line in header.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            data[key] = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
        elif value in {"true", "false"}:
            data[key] = value == "true"
        else:
            data[key] = value.strip("'\"")
    return data, body


def post_records() -> list[tuple[Path, dict[str, object], str]]:
    return [(path, *front_matter(path)) for path in sorted(POSTS.glob("*.md"))]


def top_ids(path: Path) -> set[str]:
    return set(re.findall(r"(?m)^- id:\s*([^\s]+)", path.read_text(encoding="utf-8")))


def taxonomy() -> dict[str, set[str]]:
    text = (SRC / "_data" / "blog_taxonomy.yml").read_text(encoding="utf-8")
    result: dict[str, set[str]] = {}
    current = ""
    for line in text.splitlines():
        top = re.match(r"^- id:\s*([^\s]+)", line)
        if top:
            current = top.group(1)
            result[current] = set()
            continue
        child = re.match(r"^\s{4}- \{ id:\s*([^,\s]+)", line)
        if child and current:
            result[current].add(child.group(1))
    return result


def series_ids() -> set[str]:
    return top_ids(SRC / "_data" / "blog_series.yml")


def fail(errors: list[str]) -> int:
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"{len(errors)} blocking finding(s)")
        return 1
    print("PASS")
    return 0


def asset_paths(text: str) -> set[str]:
    return set(re.findall(r"(?:srcset|src|thumbnail|cover_image):?\s*[\"']?(/assets/[^\s\"')]+)", text))
