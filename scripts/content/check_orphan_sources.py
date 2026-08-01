#!/usr/bin/env python3
"""Check source descriptors and audited public assets reach their public pages."""

from __future__ import annotations

import csv
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_data(self, data: str) -> None:
        self.values.append(data)


def built_path(site: Path, url: str) -> Path:
    clean = url.split("#", 1)[0].split("?", 1)[0].strip("/")
    if not clean:
        return site / "index.html"
    if clean.endswith(".html"):
        return site / clean
    return site / clean / "index.html"


def rendered_text(path: Path) -> str:
    parser = Text()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return re.sub(r"\s+", " ", unescape(" ".join(parser.values))).strip()


def inline_objects(section: str) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for raw in re.findall(r"(?m)^\s+-\s*\{(.*)\}\s*$", section):
        values: dict[str, str] = {}
        for match in re.finditer(r"(?:^|,)\s*([a-z_]+):\s*(?:\"([^\"]*)\"|'([^']*)'|([^,}]*))", raw):
            values[match.group(1)] = next(value for value in match.groups()[1:] if value is not None).strip()
        result.append(values)
    return result


def blocks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    starts = list(re.finditer(r"(?m)^- id:\s*([^\s]+)\s*$", text))
    return [
        (match.group(1), text[match.start() : starts[index + 1].start() if index + 1 < len(starts) else len(text)])
        for index, match in enumerate(starts)
    ]


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "src"
    site = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "_site"
    errors: list[str] = []
    descriptor_count = 0

    for path in sorted((src / "_posts").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        header = text.split("---", 2)[1]
        if re.search(r"(?m)^(?:draft:\s*true|published:\s*false)\s*$", header):
            continue
        permalink_match = re.search(r"(?m)^permalink:\s*(\S+)", header)
        if not permalink_match:
            continue
        page = built_path(site, permalink_match.group(1))
        if not page.is_file():
            errors.append(f"{path.name}: built permalink is missing")
            continue
        page_text = rendered_text(page)
        source_match = re.search(r"(?ms)^source_materials:[ \t]*(.*?)(?=^[a-z_]+:|\Z)", header)
        sources = inline_objects(source_match.group(1)) if source_match else []
        for source in sources:
            descriptor_count += 1
            title, kind = source.get("title", ""), source.get("type", "")
            if not title or not kind:
                errors.append(f"{path.name}: source descriptor lacks title or type")
            elif title not in page_text:
                errors.append(f"{path.name}: source descriptor is not rendered: {title}")
            public_url = source.get("public_url", "")
            if public_url.startswith("/") and not built_path(site, public_url).is_file():
                errors.append(f"{path.name}: internal source URL is missing: {public_url}")

    for track_id, block in blocks(src / "_data" / "engineering_tracks.yml"):
        source_match = re.search(r"(?ms)^  sources:[ \t]*(.*?)(?=^  [a-z_]+:|\Z)", block)
        sources = inline_objects(source_match.group(1)) if source_match else []
        for lang in ("", "en/"):
            page = built_path(site, f"/{lang}study/{track_id}/")
            if not page.is_file():
                continue
            page_text = rendered_text(page)
            for source in sources:
                descriptor_count += 1
                if not source.get("title") or not source.get("url"):
                    errors.append(f"track {track_id}: source descriptor lacks title or URL")
                elif source["title"] not in page_text:
                    errors.append(f"track {track_id}: source descriptor is not rendered: {source['title']}")

    audit_path = ROOT / "docs" / "qa" / "ASSET_PROVENANCE_AUDIT.csv"
    source_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in src.rglob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".md", ".yml", ".yaml"}
    )
    if not audit_path.is_file():
        errors.append("asset provenance audit is missing")
    else:
        with audit_path.open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                asset, public_url = row["primary_asset"], row["public_url"]
                if asset not in source_text:
                    errors.append(f"audit asset is orphaned: {asset}")
                page = built_path(site, public_url)
                if not page.is_file():
                    errors.append(f"audit public URL is missing: {public_url}")
                elif asset not in page.read_text(encoding="utf-8", errors="replace"):
                    errors.append(f"audit asset is not rendered at {public_url}: {asset}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {descriptor_count} source descriptors and audited assets reach public pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
