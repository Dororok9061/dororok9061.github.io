#!/usr/bin/env python3
"""Cache and inventory RFDH's public RF-study pages at a polite fixed rate.

The crawler stays on the public learning paths, skips account/community/admin
surfaces, never submits forms, and stores raw HTML outside the public site.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


SEEDS = (
    "https://rfdh.com/bas_rf.htm",
    "https://rfdh.com/bas_rf/beginer.htm",
    "https://rfdh.com/bas_rf/begin/whatisrf.php3",
    "https://rfdh.com/rfdb/msline.htm",
    "https://rfdh.com/rfdb/dbmw.htm",
    "https://rfdh.com/rfdb/filter.htm",
)
PUBLIC_PREFIXES = ("/bas_rf", "/bas_com", "/begin", "/rfdb", "/rf/", "/tool", "/tools")
PUBLIC_FILES = ("/bas_rf.htm", "/beginer.htm", "/rfdb.php3", "/rfbound.htm")
DENIED_PARTS = ("/admin", "/member", "/login", "/market", "/qna", "/board", "/bbs")
PAGE_SUFFIXES = ("", ".htm", ".html", ".php", ".php3", ".asp", ".aspx")
USER_AGENT = "Dororok9061-RF-study/1.0 (educational, low-rate; no forms)"


@dataclass
class Page:
    requested_url: str
    url: str
    status: int
    content_type: str
    charset: str
    title: str
    topic: str
    text_chars: int
    link_count: int
    image_count: int
    cached_file: str
    fetched_at: str
    error: str = ""


class StudyHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.images: list[dict[str, str]] = []
        self.frames: list[str] = []
        self.scripts: list[str] = []
        self.forms = 0
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self._title = False
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
        if tag == "title":
            self._title = True
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"])
        elif tag in {"frame", "iframe"} and values.get("src"):
            self.frames.append(values["src"])
        elif tag == "img" and values.get("src"):
            self.images.append({"src": values["src"], "alt": values.get("alt", "")})
        elif tag == "script" and values.get("src"):
            self.scripts.append(values["src"])
        elif tag == "form":
            self.forms += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._title = False
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._title:
            self.title_parts.append(data)
        if not self._skip_depth:
            value = re.sub(r"\s+", " ", data).strip()
            if value:
                self.text_parts.append(value)


def normalize(url: str, base: str = "https://rfdh.com/") -> str | None:
    value = html.unescape(url.strip())
    if not value or value.startswith(("#", "mailto:", "javascript:", "data:")):
        return None
    split = urlsplit(urljoin(base, value))
    host = split.hostname.lower() if split.hostname else ""
    if host not in {"rfdh.com", "www.rfdh.com"}:
        return None
    path = re.sub(r"/{2,}", "/", split.path or "/")
    # Query-string pages are commonly search/community endpoints. Public study
    # pages used here are stable path URLs, so queries are intentionally dropped.
    return urlunsplit(("https", "rfdh.com", path, "", ""))


def allowed(url: str) -> bool:
    path = urlsplit(url).path.lower()
    if any(part in path for part in DENIED_PARTS):
        return False
    if path.endswith(PUBLIC_FILES) or path in PUBLIC_FILES:
        return True
    if not any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES):
        return False
    suffix = Path(path).suffix.lower()
    return suffix in PAGE_SUFFIXES


def charset_for(raw: bytes, content_type: str) -> str:
    match = re.search(r"charset\s*=\s*['\"]?([\w-]+)", content_type, re.I)
    if not match:
        head = raw[:4096].decode("ascii", "ignore")
        match = re.search(r"charset\s*=\s*['\"]?([\w-]+)", head, re.I)
    name = (match.group(1) if match else "euc-kr").lower()
    aliases = {"ks_c_5601-1987": "cp949", "x-windows-949": "cp949"}
    return aliases.get(name, name)


def decode(raw: bytes, charset: str) -> tuple[str, str]:
    for candidate in dict.fromkeys((charset, "euc-kr", "cp949", "utf-8")):
        try:
            return raw.decode(candidate), candidate
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("cp949", "replace"), "cp949-replace"


def topic_for(url: str, title: str, text: str) -> str:
    haystack = f"{url} {title} {text[:3000]}".lower()
    rules = (
        ("smith-chart", ("smith", "스미스")),
        ("s-parameters", ("s-parameter", "s parameter", "s파라", "/s.htm")),
        ("power-db", ("dbm", "decibel", "데시벨", "전력변환")),
        ("transmission-lines", ("microstrip", "stripline", "waveguide", "전송선", "도파관")),
        ("matching", ("matching", "정합", "50ohm")),
        ("linearity", ("ip3", "p1db", "intermod", "비선형", "harmonic")),
        ("circuit-blocks", ("amplifier", "oscillator", "mixer", "filter", "coupler", "증폭기", "발진기", "필터")),
        ("instrumentation", ("vna", "network analyzer", "측정", "hpib")),
        ("wireless-communications", ("modulation", "통신", "무선", "/bas_com/")),
        ("foundations", ("whatisrf", "begin", "maxwell", "emwave", "impedance", "imp.htm")),
    )
    for topic, terms in rules:
        if any(term in haystack for term in terms):
            return topic
    return "rf-reference"


def equation_candidates(parts: Iterable[str]) -> list[str]:
    result: list[str] = []
    for part in parts:
        compact = re.sub(r"\s+", " ", part).strip()
        if 4 <= len(compact) <= 240 and (
            "=" in compact or re.search(r"\b(?:dB|dBm|VSWR|S11|S21|Z0|Γ|lambda|λ)\b", compact, re.I)
        ):
            if compact not in result:
                result.append(compact)
    return result[:40]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def cache_name(url: str) -> str:
    split = urlsplit(url)
    stem = re.sub(r"[^a-zA-Z0-9._-]+", "-", split.path.strip("/") or "home")[:100]
    return f"{stem}-{hashlib.sha256(url.encode()).hexdigest()[:12]}.html"


def crawl(args: argparse.Namespace) -> int:
    output = Path(args.output).resolve()
    cache = Path(args.cache).resolve()
    output.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)

    queue = deque(filter(None, (normalize(seed) for seed in args.seed)))
    queued = set(queue)
    visited: set[str] = set()
    pages: list[Page] = []
    edges: list[dict[str, str]] = []
    images: list[dict[str, str]] = []
    equations: list[dict[str, str]] = []
    calculators: list[dict[str, object]] = []
    dead: list[dict[str, object]] = []
    last_request = 0.0

    while queue and len(visited) < args.max_pages:
        requested = queue.popleft()
        if requested in visited or not allowed(requested):
            continue
        visited.add(requested)
        fetched_at = datetime.now(timezone.utc).isoformat()
        expected_cache = cache / cache_name(requested)
        if expected_cache.exists():
            raw = expected_cache.read_bytes()
            status, final_url, content_type = 200, requested, "text/html; charset=EUC-KR"
            fetched_at = datetime.fromtimestamp(expected_cache.stat().st_mtime, timezone.utc).isoformat()
            print(f"{len(visited):03d} CACHE                    {requested}", flush=True)
        else:
            wait = args.delay - (time.monotonic() - last_request)
            if wait > 0:
                time.sleep(wait)
            request = Request(requested, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.1"})
            try:
                with urlopen(request, timeout=args.timeout) as response:
                    last_request = time.monotonic()
                    raw = response.read(args.max_bytes + 1)
                    if len(raw) > args.max_bytes:
                        raise ValueError(f"response exceeds {args.max_bytes} bytes")
                    status = response.status
                    final_url = normalize(response.geturl(), requested) or requested
                    content_type = response.headers.get("Content-Type", "")
            except HTTPError as exc:
                last_request = time.monotonic()
                status, final_url, content_type, raw = exc.code, requested, exc.headers.get("Content-Type", ""), b""
                dead.append({"url": requested, "status": status, "error": str(exc)})
            except (URLError, TimeoutError, ValueError) as exc:
                last_request = time.monotonic()
                pages.append(Page(requested, requested, 0, "", "", "", "", 0, 0, 0, "", fetched_at, str(exc)))
                dead.append({"url": requested, "status": 0, "error": str(exc)})
                continue

        if status != 200 or "html" not in content_type.lower():
            pages.append(Page(requested, final_url, status, content_type, "", "", "", 0, 0, 0, "", fetched_at))
            if status != 200:
                dead.append({"url": requested, "status": status, "error": f"HTTP {status}"})
            continue

        charset = charset_for(raw, content_type)
        document, charset = decode(raw, charset)
        parser = StudyHTMLParser()
        try:
            parser.feed(document)
        except Exception as exc:  # malformed legacy markup; keep partial parse
            parse_error = f"parser: {exc}"
        else:
            parse_error = ""
        filename = cache_name(final_url)
        (cache / filename).write_bytes(raw)
        title = re.sub(r"\s+", " ", " ".join(parser.title_parts)).strip()
        # Several legacy communication-course pages literally use "제목없음"
        # in <title>, while their first content heading carries the real chapter
        # name. Prefer that heading so the inventory remains useful.
        if title in {"", "제목없음"}:
            title = next((
                part for part in parser.text_parts
                if part != "제목없음"
                and len(part) <= 120
                and re.match(r"^\d+\s*-\s*\d+\s*장?\s*[:：]", part)
            ), title)
        text = "\n".join(parser.text_parts)
        topic = topic_for(final_url, title, text)

        page_links: set[str] = set()
        for raw_link in (*parser.links, *parser.frames):
            target = normalize(raw_link, final_url)
            if not target:
                continue
            edges.append({"source": final_url, "target": target, "kind": "frame" if raw_link in parser.frames else "link"})
            page_links.add(target)
            if allowed(target) and target not in visited and target not in queued:
                queue.append(target)
                queued.add(target)
        for item in parser.images:
            source = urljoin(final_url, html.unescape(item["src"]))
            images.append({"page_url": final_url, "image_url": source, "alt": item["alt"], "topic": topic})
        for candidate in equation_candidates(parser.text_parts):
            equations.append({"page_url": final_url, "title": title, "topic": topic, "candidate": candidate})
        if parser.forms or parser.scripts or any(term in f"{title} {final_url}".lower() for term in ("calculator", "계산", "변환", "dbmw")):
            calculators.append({
                "page_url": final_url,
                "title": title,
                "forms": parser.forms,
                "scripts": " | ".join(urljoin(final_url, item) for item in parser.scripts),
                "topic": topic,
            })
        pages.append(Page(
            requested, final_url, status, content_type, charset, title, topic,
            len(text), len(page_links), len(parser.images), filename, fetched_at, parse_error,
        ))
        print(f"{len(visited):03d} {status} {topic:24s} {final_url}", flush=True)

    page_rows = [asdict(page) for page in pages]
    fields = list(Page.__dataclass_fields__)
    write_csv(output / "rfdh-pages.csv", page_rows, fields)
    (output / "rfdh-pages.json").write_text(json.dumps(page_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "rfdh-link-graph.json").write_text(json.dumps(edges, ensure_ascii=False, indent=2), encoding="utf-8")
    write_csv(output / "rfdh-images.csv", images, ["page_url", "image_url", "alt", "topic"])
    write_csv(output / "rfdh-equations.csv", equations, ["page_url", "title", "topic", "candidate"])
    write_csv(output / "rfdh-calculators.csv", calculators, ["page_url", "title", "forms", "scripts", "topic"])
    write_csv(output / "dead-links.csv", dead, ["url", "status", "error"])
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pages": len(pages),
        "successful_html_pages": sum(page.status == 200 and bool(page.cached_file) for page in pages),
        "edges": len(edges),
        "images": len(images),
        "equation_candidates": len(equations),
        "calculator_candidates": len(calculators),
        "dead_links": len(dead),
        "queue_remaining": len(queue),
        "delay_seconds": args.delay,
        "max_pages": args.max_pages,
    }
    (output / "crawl-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if not queue else 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", action="append", default=[], help="additional public seed URL")
    parser.add_argument("--output", default="work/rfdh-study")
    parser.add_argument("--cache", default=r"D:\Codex_Workspaces\2026-08-02\rfdh-complete-rf-study\cache\rfdh\public")
    parser.add_argument("--delay", type=float, default=1.5)
    parser.add_argument("--timeout", type=float, default=25.0)
    parser.add_argument("--max-pages", type=int, default=600)
    parser.add_argument("--max-bytes", type=int, default=4 * 1024 * 1024)
    args = parser.parse_args()
    args.seed = tuple(dict.fromkeys((*SEEDS, *args.seed)))
    if args.delay < 1.0:
        parser.error("--delay must be at least 1.0 second")
    return args


if __name__ == "__main__":
    raise SystemExit(crawl(parse_args()))
