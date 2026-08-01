#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree


BLOCKED_EXTENSIONS = {
    ".dat",
    ".lic",
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".sof",
    ".pof",
    ".jic",
    ".qar",
    ".qpf",
    ".qsf",
    ".zip",
    ".7z",
    ".rar",
    ".map",
}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
}
DANGEROUS_CODE = re.compile(
    r"\b(?:innerHTML|outerHTML|insertAdjacentHTML|document\.write|eval\s*\(|new\s+Function\s*\()",
    re.IGNORECASE,
)
HTTP_RESOURCE = re.compile(
    r"(?:\b(?:src|href|action|poster)\s*=\s*[\"']\s*http://|url\(\s*[\"']?http://)",
    re.IGNORECASE,
)
# Bilingual study chapters add useful HTML and original SVG diagrams while the
# cap still prevents accidental publication of large private source artifacts.
MAX_SITE_BYTES = 8_500_000


class PageParser(HTMLParser):
    def __init__(self, relative_path: str) -> None:
        super().__init__(convert_charrefs=True)
        self.relative_path = relative_path
        self.lang = ""
        self.title_seen = False
        self.in_title = False
        self.ids: set[str] = set()
        self.fragment_links: list[str] = []
        self.local_links: list[tuple[str, str]] = []
        self.has_csp = False
        self.has_canonical = False
        self.noindex = False
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.lower(): value or "" for name, value in attrs}
        if tag == "html":
            self.lang = values.get("lang", "")
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            if values.get("http-equiv", "").lower() == "content-security-policy":
                self.has_csp = True
            if values.get("name", "").lower() == "robots" and "noindex" in values.get("content", "").lower():
                self.noindex = True
        if tag == "link" and values.get("rel", "").lower() == "canonical":
            self.has_canonical = True
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"duplicate id #{element_id}")
            self.ids.add(element_id)
        for name in values:
            if name.startswith("on"):
                self.errors.append(f"inline event handler {name} on <{tag}>")
            if name == "style":
                self.errors.append(f"inline style on <{tag}>")
        if tag == "script":
            is_structured_data = values.get("type", "").lower() == "application/ld+json"
            script_src = values.get("src", "")
            if not script_src:
                if not is_structured_data:
                    self.errors.append("inline script is not allowed")
            elif urlparse(script_src).scheme:
                self.errors.append("external script is not allowed")
        if tag == "style":
            self.errors.append("inline <style> is not allowed")
        if tag == "form":
            self.errors.append("forms are outside the approved architecture")
        if tag == "img":
            if not values.get("alt"):
                self.errors.append("image is missing non-empty alt text")
            if not values.get("width") or not values.get("height"):
                self.errors.append("image is missing width/height")
        for attr in ("href", "src", "srcset", "poster"):
            value = values.get(attr, "").strip()
            if not value:
                continue
            for candidate in value.split(","):
                target = candidate.strip().split(" ")[0]
                parsed = urlparse(target)
                if parsed.scheme in {"http", "https", "mailto", "tel", "data"}:
                    continue
                if target.startswith("#"):
                    self.fragment_links.append(unquote(target[1:]))
                else:
                    self.local_links.append((tag, target))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title and data.strip():
            self.title_seen = True


def resolve_local(root: Path, page: Path, target: str) -> Path:
    parsed = urlparse(target)
    clean_path = unquote(parsed.path)
    if clean_path.startswith("/"):
        resolved = root / clean_path.lstrip("/")
    else:
        resolved = page.parent / clean_path
    if clean_path.endswith("/"):
        resolved /= "index.html"
    return resolved


def check_site(root: Path) -> list[str]:
    errors: list[str] = []
    files = [path for path in root.rglob("*") if path.is_file()]
    total_bytes = sum(path.stat().st_size for path in files)

    # The Gem theme and preserved evidence images are counted once across the
    # whole multi-page build. Keep a tight aggregate cap while the 1 MB per-file
    # rule below prevents any single unoptimized asset from hiding inside it.
    if total_bytes > MAX_SITE_BYTES:
        errors.append(
            f"public site is {total_bytes} bytes; expected at most {MAX_SITE_BYTES} bytes"
        )

    for path in files:
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() in BLOCKED_EXTENSIONS:
            errors.append(f"{relative}: blocked file extension {path.suffix}")
        if path.stat().st_size > 1_000_000:
            errors.append(f"{relative}: public file exceeds 1 MB")

    text_files = [
        path
        for path in files
        if path.suffix.lower() in {".html", ".css", ".js", ".xml", ".txt"}
    ]
    for path in text_files:
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{relative}: possible {name}; value not printed")
        if path.suffix.lower() in {".html", ".css", ".js"}:
            if HTTP_RESOURCE.search(text):
                errors.append(f"{relative}: HTTP resource reference")
            if DANGEROUS_CODE.search(text):
                errors.append(f"{relative}: unsafe dynamic DOM/code pattern")

    html_pages = sorted(root.rglob("*.html"))
    for page in html_pages:
        relative = page.relative_to(root).as_posix()
        parser = PageParser(relative)
        parser.feed(page.read_text(encoding="utf-8"))
        errors.extend(f"{relative}: {message}" for message in parser.errors)
        if not parser.lang:
            errors.append(f"{relative}: missing html lang")
        if not parser.title_seen:
            errors.append(f"{relative}: missing title")
        if not parser.has_csp:
            errors.append(f"{relative}: missing CSP meta")
        if not parser.has_canonical and not parser.noindex:
            errors.append(f"{relative}: missing canonical URL")
        for fragment in parser.fragment_links:
            if fragment and fragment not in parser.ids:
                errors.append(f"{relative}: missing fragment target #{fragment}")
        for tag, target in parser.local_links:
            resolved = resolve_local(root, page, target)
            if not resolved.exists():
                errors.append(f"{relative}: <{tag}> references missing {target}")

    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        errors.append("sitemap.xml: missing")
    else:
        try:
            tree = ElementTree.parse(sitemap)
            locations = [
                node.text or ""
                for node in tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            ]
            if not locations or any(not location.startswith("https://tontonjeong.github.io/") for location in locations):
                errors.append("sitemap.xml: invalid or non-HTTPS location")
        except ElementTree.ParseError as error:
            errors.append(f"sitemap.xml: {error}")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
    if not root.is_dir():
        print(f"ERROR: site root not found: {root}", file=sys.stderr)
        return 2

    errors = check_site(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"{len(errors)} blocking finding(s)")
        return 1

    file_count = sum(1 for path in root.rglob("*") if path.is_file())
    total_bytes = sum(path.stat().st_size for path in root.rglob("*") if path.is_file())
    print(f"PASS: {file_count} public files, {total_bytes} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

