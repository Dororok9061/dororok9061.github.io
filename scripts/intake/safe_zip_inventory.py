#!/usr/bin/env python3
"""Inventory a ZIP safely and optionally extract it into a private work folder."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path, PurePosixPath


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def unsafe_name(name: str) -> bool:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    return (
        not normalized
        or path.is_absolute()
        or ".." in path.parts
        or any(":" in part for part in path.parts)
    )


def is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = info.external_attr >> 16
    return stat.S_ISLNK(mode)


def inspect_archive(
    archive: Path,
    *,
    max_members: int,
    max_total_bytes: int,
    max_member_bytes: int,
    max_ratio: float,
) -> dict:
    members: list[dict] = []
    findings: list[str] = []
    total_uncompressed = 0

    with zipfile.ZipFile(archive) as source:
        infos = source.infolist()
        if len(infos) > max_members:
            findings.append(f"member limit exceeded: {len(infos)} > {max_members}")

        for info in infos:
            total_uncompressed += info.file_size
            ratio = info.file_size / max(info.compress_size, 1)
            item_findings = []
            if unsafe_name(info.filename):
                item_findings.append("unsafe path")
            if is_symlink(info):
                item_findings.append("symbolic link")
            if info.flag_bits & 0x1:
                item_findings.append("encrypted")
            if info.file_size > max_member_bytes:
                item_findings.append("member size limit exceeded")
            if ratio > max_ratio and info.file_size > 1024 * 1024:
                item_findings.append("compression ratio limit exceeded")
            members.append(
                {
                    "path": info.filename,
                    "directory": info.is_dir(),
                    "compressed_bytes": info.compress_size,
                    "uncompressed_bytes": info.file_size,
                    "compression_ratio": round(ratio, 2),
                    "findings": item_findings,
                }
            )
            findings.extend(f"{info.filename}: {finding}" for finding in item_findings)

    if total_uncompressed > max_total_bytes:
        findings.append(
            f"total size limit exceeded: {total_uncompressed} > {max_total_bytes}"
        )

    return {
        "archive": str(archive.resolve()),
        "sha256": sha256(archive),
        "compressed_bytes": archive.stat().st_size,
        "member_count": len(members),
        "total_uncompressed_bytes": total_uncompressed,
        "findings": findings,
        "members": members,
    }


def extract_archive(archive: Path, destination: Path, report: dict) -> None:
    if report["findings"]:
        raise ValueError("refusing extraction because archive findings are present")
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()

    with zipfile.ZipFile(archive) as source:
        for info in source.infolist():
            relative = PurePosixPath(info.filename.replace("\\", "/"))
            target = destination.joinpath(*relative.parts)
            resolved = target.resolve()
            if resolved != root and root not in resolved.parents:
                raise ValueError(f"refusing path outside destination: {info.filename}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.open(info, "r") as reader, target.open("xb") as writer:
                shutil.copyfileobj(reader, writer, length=1024 * 1024)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--extract-to", type=Path)
    parser.add_argument("--max-members", type=int, default=20_000)
    parser.add_argument("--max-total-bytes", type=int, default=20 * 1024**3)
    parser.add_argument("--max-member-bytes", type=int, default=8 * 1024**3)
    parser.add_argument("--max-ratio", type=float, default=1_000.0)
    args = parser.parse_args()

    archive = args.archive.resolve(strict=True)
    report = inspect_archive(
        archive,
        max_members=args.max_members,
        max_total_bytes=args.max_total_bytes,
        max_member_bytes=args.max_member_bytes,
        max_ratio=args.max_ratio,
    )
    if args.extract_to:
        extract_archive(archive, args.extract_to, report)
        report["extracted_to"] = str(args.extract_to.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("sha256", "member_count", "total_uncompressed_bytes", "findings")}, ensure_ascii=False))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
