#!/usr/bin/env python3
"""Copy a source tree without overwriting and verify every file with SHA-256."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def copy_tree(source: Path, destination: Path) -> list[dict]:
    source = source.resolve(strict=True)
    if not source.is_dir():
        raise ValueError(f"source is not a directory: {source}")
    destination.mkdir(parents=True, exist_ok=True)
    records = []

    for item in sorted(source.rglob("*")):
        relative = item.relative_to(source)
        target = destination / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if not item.is_file():
            raise ValueError(f"unsupported source entry: {item}")
        source_hash = sha256(item)
        if target.exists():
            if not target.is_file():
                raise ValueError(f"destination is not a file: {target}")
            destination_hash = sha256(target)
            if source_hash != destination_hash:
                raise ValueError(f"destination differs; refusing overwrite: {target}")
            action = "reused"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            destination_hash = sha256(target)
            if source_hash != destination_hash:
                raise ValueError(f"SHA-256 mismatch after copy: {target}")
            action = "copied"
        records.append(
            {
                "relative_path": relative.as_posix(),
                "bytes": item.stat().st_size,
                "sha256": source_hash,
                "action": action,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    if args.manifest.exists():
        raise FileExistsError(f"refusing to overwrite manifest: {args.manifest}")

    records = copy_tree(args.source, args.destination)
    report = {
        "source": str(args.source.resolve()),
        "destination": str(args.destination.resolve()),
        "file_count": len(records),
        "total_bytes": sum(record["bytes"] for record in records),
        "files": records,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: report[key] for key in ("file_count", "total_bytes")},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
