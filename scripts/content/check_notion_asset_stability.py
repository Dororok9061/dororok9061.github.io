#!/usr/bin/env python3
"""Validate configured public Notion and asset URL forms without network access."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "docs" / "internal" / "public_asset_stability.json"
LOCAL_PATH = re.compile(
    r"(?i)(?:(?<![a-z])[a-z]:[\\/]|\\\\|/mnt/data(?:/|$)|file:|localhost|127\.0\.0\.1)"
)
SIGNED_KEYS = {
    "awsaccesskeyid",
    "expires",
    "signature",
    "x-amz-algorithm",
    "x-amz-credential",
    "x-amz-date",
    "x-amz-expires",
    "x-amz-security-token",
    "x-amz-signature",
}
DRIVE_HOSTS = {"drive.google.com", "drive.usercontent.google.com", "docs.google.com"}


def records(manifest: dict[str, object], key: str, errors: list[str]) -> list[dict[str, str]]:
    value = manifest.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"manifest {key} must be a non-empty list")
        return []
    result: list[dict[str, str]] = []
    for index, item in enumerate(value, 1):
        if not isinstance(item, dict) or not isinstance(item.get("name"), str) or not isinstance(item.get("url"), str):
            errors.append(f"manifest {key}[{index}] needs string name and url")
        else:
            result.append({"name": item["name"], "url": item["url"]})
    return result


def common_url_errors(label: str, value: str) -> tuple[object, list[str]]:
    errors: list[str] = []
    if LOCAL_PATH.search(unquote(value)):
        errors.append(f"{label} contains a local or temporary path")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname:
        errors.append(f"{label} must be an absolute HTTPS URL")
    if parsed.username or parsed.password:
        errors.append(f"{label} embeds credentials")
    return parsed, errors


def page_errors(record: dict[str, str]) -> list[str]:
    label = f"Notion page {record['name']}"
    parsed, errors = common_url_errors(label, record["url"])
    hostname = (parsed.hostname or "").lower()
    if hostname != "notion.site" and not hostname.endswith(".notion.site"):
        errors.append(f"{label} is not a public notion.site URL")
    if parsed.query or parsed.fragment:
        errors.append(f"{label} must not use query or fragment state")
    return errors


def asset_errors(record: dict[str, str]) -> list[str]:
    label = f"Notion asset {record['name']}"
    parsed, errors = common_url_errors(label, record["url"])
    hostname = (parsed.hostname or "").lower()
    query_keys = {key.lower() for key in parse_qs(parsed.query, keep_blank_values=True)}
    if query_keys & SIGNED_KEYS or "prod-files-secure.s3" in hostname:
        errors.append(f"{label} uses a temporary signed object URL")
    if hostname in DRIVE_HOSTS or hostname.endswith(".drive.google.com"):
        errors.append(f"{label} uses a Google Drive URL whose public access cannot be guaranteed offline")
    if hostname == "tontonjeong.github.io":
        path = unquote(parsed.path)
        local = ROOT / "src" / path.removeprefix("/")
        if not path.startswith("/assets/") or not local.is_file():
            errors.append(f"{label} does not map to a repository public asset: {path}")
    return errors


def main() -> int:
    manifest_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_MANIFEST
    errors: list[str] = []
    if not manifest_path.is_file():
        print(f"FAIL: stability manifest is missing: {manifest_path}")
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read stability manifest: {exc}")
        return 1
    if not isinstance(manifest, dict):
        print("FAIL: stability manifest root must be an object")
        return 1

    pages = records(manifest, "notion_pages", errors)
    assets = records(manifest, "notion_assets", errors)
    for record in pages:
        errors.extend(page_errors(record))
    for record in assets:
        errors.extend(asset_errors(record))
    for key, values in (("notion_pages", pages), ("notion_assets", assets)):
        urls = [record["url"] for record in values]
        if len(urls) != len(set(urls)):
            errors.append(f"manifest {key} contains duplicate URLs")

    profile = ROOT / "src" / "_data" / "profile.yml"
    profile_text = profile.read_text(encoding="utf-8") if profile.is_file() else ""
    match = re.search(r"(?m)^public_notion_url:\s*(\S+)\s*$", profile_text)
    if not match:
        errors.append("src/_data/profile.yml has no public_notion_url")
    elif match.group(1) not in {record["url"] for record in pages}:
        errors.append("profile public_notion_url is absent from the stability manifest")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(
        f"PASS: {len(pages)} configured public Notion page URLs and {len(assets)} asset URLs "
        "match offline stability rules"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
