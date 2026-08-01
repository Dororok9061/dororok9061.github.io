#!/usr/bin/env python3
"""Reject public detail pages that contain only a title and description."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
DETAIL = re.compile(
    r"^/(?:en/)?(?:"
    r"blog/\d{4}/\d{2}/\d{2}/[^/]+|"
    r"projects/[^/]+|publications/[^/]+|"
    r"coursework/[^/]+(?:/[^/]+)?|study/[^/]+(?:/[^/]+)?|"
    r"learning/(?:competitions/[^/]+|bootcamps/[^/]+(?:/day-\d+)?)"
    r")/$"
)


class MainContent(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_main = False
        self.ignored = 0
        self.text: list[str] = []
        self.counts = {name: 0 for name in ("h1", "h2", "h3", "li", "figure", "pre", "table")}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if tag in {"nav", "script", "style", "footer"}:
            self.ignored += 1
        elif not self.ignored and tag in self.counts:
            self.counts[tag] += 1

    def handle_endtag(self, tag: str) -> None:
        if self.in_main and tag in {"nav", "script", "style", "footer"} and self.ignored:
            self.ignored -= 1
        elif tag == "main":
            self.in_main = False

    def handle_data(self, data: str) -> None:
        if self.in_main and not self.ignored:
            self.text.append(data)


def route(path: Path, site: Path) -> str:
    relative = path.relative_to(site).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return f"/{relative[:-10]}"
    return f"/{relative}"


def source_details(src: Path) -> list[Path]:
    result = list((src / "_posts").glob("*.md"))
    for root in ("projects", "publications", "learning"):
        result.extend(path for path in (src / root).rglob("*.md") if path.parent != src / root)
    return sorted(set(result))


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "src"
    site = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "_site"
    errors: list[str] = []

    for path in source_details(src):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        header = text.split("---", 2)[1]
        if re.search(r"(?m)^(?:draft:\s*true|published:\s*false)\s*$", header):
            continue
        for key in ("title", "description"):
            if not re.search(rf"(?m)^{key}:\s*\S", header):
                errors.append(f"{path.relative_to(src)}: missing {key}")

    checked = 0
    for path in sorted(site.rglob("*.html")):
        public_route = route(path, site)
        if not DETAIL.fullmatch(public_route):
            continue
        parser = MainContent()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        words = re.findall(r"[A-Za-z0-9\uac00-\ud7a3]+", " ".join(parser.text))
        substantive = sum(parser.counts[name] for name in ("h2", "h3", "li", "figure", "pre", "table"))
        structured_unit = bool(
            re.fullmatch(r"/(?:en/)?(?:coursework/[^/]+/[^/]+|study/[^/]+/[^/]+)/", public_route)
        )
        minimum_words = 80 if structured_unit else 12
        minimum_sections = 8 if structured_unit else 2
        if parser.counts["h1"] != 1:
            errors.append(f"{public_route}: expected one main heading")
        if len(words) < minimum_words or substantive < minimum_sections:
            errors.append(f"{public_route}: title/description-only detail page")
        checked += 1

    if not checked:
        errors.append("no built detail pages were checked")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {checked} public detail pages contain substantive sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
