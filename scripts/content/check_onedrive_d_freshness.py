#!/usr/bin/env python3
"""Audit a sanitized OneDrive-to-D snapshot without touching OneDrive."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFESTS = (
    ROOT / "work" / "manifests" / "onedrive_d_freshness_snapshot.json",
    ROOT / "manifests" / "onedrive_d_freshness_snapshot.json",
    ROOT / "docs" / "internal" / "ONEDRIVE_D_FRESHNESS.json",
    ROOT / "docs" / "internal" / "onedrive_d_freshness_snapshot.json",
)
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Audit a prebuilt sanitized snapshot; never reads or hydrates OneDrive files."
    )
    result.add_argument("--manifest", type=Path, help="sanitized JSON snapshot on a non-OneDrive path")
    result.add_argument(
        "--strict",
        action="store_true",
        help="return nonzero unless the snapshot proves a complete SHA-256 match",
    )
    return result


def inside_onedrive(path: Path) -> bool:
    candidate = os.path.normcase(os.path.abspath(os.fspath(path)))
    for name in ("OneDriveCommercial", "OneDrive", "OneDriveConsumer"):
        root = os.environ.get(name)
        if not root:
            continue
        normalized = os.path.normcase(os.path.abspath(root)).rstrip("\\/")
        if candidate == normalized or candidate.startswith(normalized + os.sep):
            return True
    return False


def find_manifest(explicit: Path | None) -> Path | None:
    if explicit is not None:
        return explicit
    configured = os.environ.get("ONEDRIVE_D_FRESHNESS_MANIFEST")
    if configured:
        return Path(configured)
    return next((path for path in DEFAULT_MANIFESTS if path.is_file()), None)


def integer(mapping: dict[str, Any], *names: str) -> int | None:
    for name in names:
        value = mapping.get(name)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            return value
    return None


def hash_value(mapping: dict[str, Any], *names: str) -> str | None:
    for name in names:
        value = mapping.get(name)
        if isinstance(value, str) and SHA256.fullmatch(value):
            return value.lower()
    return None


def detailed_counts(data: dict[str, Any]) -> tuple[int, int, int]:
    raw_entries = data.get("entries", data.get("files", []))
    if not isinstance(raw_entries, list):
        return 0, 0, 0
    matches = mismatches = unchecked = 0
    for raw in raw_entries:
        if not isinstance(raw, dict):
            unchecked += 1
            continue
        source = raw.get("source", raw.get("onedrive", {}))
        mirror = raw.get("mirror", raw.get("d_drive", raw.get("destination", {})))
        source = source if isinstance(source, dict) else {}
        mirror = mirror if isinstance(mirror, dict) else {}
        source_hash = hash_value(source, "sha256", "hash") or hash_value(
            raw, "source_sha256", "onedrive_sha256"
        )
        mirror_hash = hash_value(mirror, "sha256", "hash") or hash_value(
            raw, "mirror_sha256", "d_sha256", "destination_sha256"
        )
        if source_hash is None or mirror_hash is None:
            unchecked += 1
        elif source_hash == mirror_hash:
            matches += 1
        else:
            mismatches += 1
    return matches, mismatches, unchecked


def audit(data: Any) -> tuple[str, str]:
    if not isinstance(data, dict) or data.get("sanitized") is not True:
        return "NOT_CHECKED", "manifest is not explicitly marked sanitized"

    comparison = data.get("comparison", {})
    source = data.get("source", {})
    mirror = data.get("d_mirror", data.get("mirror", {}))
    comparison = comparison if isinstance(comparison, dict) else {}
    source = source if isinstance(source, dict) else {}
    mirror = mirror if isinstance(mirror, dict) else {}

    raw_entries = data.get("entries", data.get("files", []))
    entry_count = len(raw_entries) if isinstance(raw_entries, list) else None
    source_files = integer(source, "file_count", "files")
    mirror_files = integer(mirror, "file_count", "files")
    if source_files is None:
        source_files = entry_count
    if mirror_files is None:
        mirror_files = entry_count
    missing = integer(comparison, "missing_in_mirror", "missing_in_d") or 0
    extra = integer(comparison, "extra_in_mirror", "extra_in_d") or 0
    size_mismatches = integer(comparison, "size_mismatches", "size_mismatch") or 0
    source_newer = integer(comparison, "source_newer", "source_newer_count") or 0
    aggregate_hashes = integer(comparison, "sha256_compared", "hash_compared") or 0
    aggregate_hash_mismatches = integer(
        comparison, "sha256_mismatches", "hash_mismatches"
    ) or 0
    hash_matches, hash_mismatches, unchecked = detailed_counts(data)
    compared = max(aggregate_hashes, hash_matches + hash_mismatches)
    mismatches = max(aggregate_hash_mismatches, hash_mismatches)

    if missing or size_mismatches or source_newer or mismatches:
        return (
            "INCOMPLETE",
            f"missing={missing}, size_mismatch={size_mismatches}, "
            f"source_newer={source_newer}, sha256_mismatch={mismatches}",
        )
    if source_files is None:
        return "NOT_CHECKED", "snapshot lacks source file count"
    if mirror_files is not None and mirror_files < source_files:
        return "INCOMPLETE", f"source_files={source_files}, mirror_files={mirror_files}"
    if source_files == 0:
        return "NOT_CHECKED", "snapshot contains no source files"
    if compared != source_files or unchecked:
        return (
            "NOT_CHECKED",
            f"metadata snapshot has {source_files} source files but only {compared} SHA-256 comparisons",
        )
    if extra:
        return "PASS", f"all {source_files} source files match by SHA-256; mirror_extra={extra}"
    return "PASS", f"all {source_files} source files match by SHA-256"


def main() -> int:
    args = parser().parse_args()
    manifest = find_manifest(args.manifest)
    if manifest is None:
        status, detail = "NOT_CHECKED", "sanitized snapshot manifest is absent"
    elif inside_onedrive(manifest):
        status, detail = "NOT_CHECKED", "refusing to open a manifest inside OneDrive"
    elif not manifest.is_file():
        status, detail = "NOT_CHECKED", "sanitized snapshot manifest is absent"
    else:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            status, detail = "NOT_CHECKED", "sanitized snapshot manifest is unreadable or invalid"
        else:
            status, detail = audit(data)
    print(f"{status}: {detail}")
    return int(args.strict and status != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
