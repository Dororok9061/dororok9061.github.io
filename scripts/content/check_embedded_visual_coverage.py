#!/usr/bin/env python3
"""Validate public local-image references and recorded coursework boundaries."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
SOURCE_SUFFIXES = {".md", ".markdown", ".yml", ".yaml"}
BUILT_SUFFIXES = {".css", ".html", ".js", ".json", ".xml"}
IMAGE_SUFFIXES = {".avif", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
LOCAL_HOSTS = {"dororok9061.github.io"}
OLD_WRONG_COVERS = {
    "/assets/images/study/coursework/digital-communications.webp",
    "/assets/images/study/coursework/electronic-circuits-1.webp",
    "/assets/images/study/coursework/electronic-circuits-2.webp",
    "/assets/images/study/coursework/embedded-systems.webp",
    "/assets/images/study/coursework/power-electronics.webp",
}
ASSET_URL = re.compile(
    r"(?:(?:https?:)?//[A-Za-z0-9.-]+)?/?assets/[A-Za-z0-9_./%+~@-]+"
    r"\.(?:avif|gif|ico|jpe?g|png|svg|webp)(?:\?[^\s\"'<>)}\]]*)?(?:#[^\s\"'<>)}\]]*)?",
    re.IGNORECASE,
)
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
HTML_IMAGE = re.compile(r"\b(?:poster|src|srcset)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
CSS_IMAGE = re.compile(r"url\(\s*[\"']?([^\"')]+)", re.IGNORECASE)
YAML_IMAGE = re.compile(
    r"(?m)^\s*(?:cover_image|image|image_jpg|image_webp|thumbnail):\s*[\"']?([^\s\"']+)",
    re.IGNORECASE,
)


def candidate_urls(text: str) -> set[str]:
    """Return image-looking URL tokens without interpreting binary contents."""
    values = {match.group(0) for match in ASSET_URL.finditer(text)}
    values.update(match.group(1) for match in MARKDOWN_IMAGE.finditer(text))
    values.update(match.group(1) for match in CSS_IMAGE.finditer(text))
    values.update(match.group(1) for match in YAML_IMAGE.finditer(text))
    for match in HTML_IMAGE.finditer(text):
        values.update(part.strip().split()[0] for part in match.group(1).split(",") if part.strip())
    return values


def image_target(value: str, document: Path, root: Path) -> tuple[str, Path] | None:
    value = value.strip(" <>\"'")
    if not value or value.startswith(("data:", "{{", "#")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        if (parsed.hostname or "").lower() not in LOCAL_HOSTS:
            return None
    elif parsed.scheme:
        return None
    path = unquote(parsed.path).replace("\\", "/")
    if Path(path).suffix.lower() not in IMAGE_SUFFIXES:
        return None
    if path.startswith("/"):
        target = root / path.lstrip("/")
    elif path.startswith("assets/"):
        target = root / path
        path = f"/{path}"
    else:
        target = document.parent / path
    target = target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return path, target
    return path, target


def references(root: Path, suffixes: set[str]) -> list[tuple[Path, int, str, Path]]:
    result: list[tuple[Path, int, str, Path]] = []
    for document in sorted(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in suffixes):
        for line_number, line in enumerate(document.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for value in candidate_urls(line):
                resolved = image_target(value, document, root)
                if resolved:
                    public_path, target = resolved
                    result.append((document, line_number, public_path, target))
    return result


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def coursework_errors(src: Path) -> list[str]:
    errors: list[str] = []
    course_data = src / "_data" / "coursework_courses.yml"
    if not course_data.is_file():
        return ["src/_data/coursework_courses.yml is missing"]
    thumbnails = re.findall(r"(?m)^  thumbnail:\s*([^\s]+)\s*$", course_data.read_text(encoding="utf-8"))
    project_hashes: dict[str, Path] = {}
    project_root = src / "assets" / "images" / "projects"
    for path in project_root.rglob("*") if project_root.is_dir() else ():
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            project_hashes[digest(path)] = path
    for thumbnail in thumbnails:
        if thumbnail in OLD_WRONG_COVERS:
            errors.append(f"coursework record restores an old mismatched cover: {thumbnail}")
        if not thumbnail.startswith("/assets/images/study/coursework/"):
            errors.append(f"coursework cover crosses project/category boundary: {thumbnail}")
            continue
        path = src / thumbnail.removeprefix("/")
        if path.is_file() and digest(path) in project_hashes:
            reused = project_hashes[digest(path)].relative_to(src)
            errors.append(f"coursework cover exactly reuses project image: {thumbnail} = {reused}")

    audit = ROOT / "docs" / "qa" / "ASSET_PROVENANCE_AUDIT.csv"
    if not audit.is_file():
        errors.append("docs/qa/ASSET_PROVENANCE_AUDIT.csv is missing")
    else:
        with audit.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        for row in (row for row in rows if row.get("scope") == "course"):
            asset = row.get("primary_asset", "")
            if asset not in thumbnails:
                errors.append(f"course audit asset is not its configured thumbnail: {row.get('id', '?')} {asset}")
            if asset.startswith("/assets/images/projects/"):
                errors.append(f"course audit records cross-project reuse: {row.get('id', '?')} {asset}")
    return errors


def main() -> int:
    src = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "src"
    site = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / "_site"
    errors: list[str] = []
    if not src.is_dir():
        errors.append(f"public source directory is missing: {src}")
    if not site.is_dir():
        errors.append(f"built site directory is missing: {site}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    source_refs = references(src, SOURCE_SUFFIXES)
    built_refs = references(site, BUILT_SUFFIXES)
    for root, scope, records in ((src, "source", source_refs), (site, "built", built_refs)):
        for document, line, public_path, target in records:
            if not target.is_file():
                location = document.relative_to(root)
                errors.append(f"{scope} {location}:{line} references missing image {public_path}")
    built_paths = {public_path for _, _, public_path, _ in built_refs}
    for old_cover in sorted(OLD_WRONG_COVERS):
        if old_cover in built_paths or (site / old_cover.removeprefix("/")).is_file():
            errors.append(f"old mismatched coursework cover remains public: {old_cover}")
    errors.extend(coursework_errors(src))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(
        f"PASS: {len(source_refs)} source and {len(built_refs)} built local-image references resolve; "
        "recorded coursework mismatches are absent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
