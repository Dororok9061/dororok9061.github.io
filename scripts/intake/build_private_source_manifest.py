#!/usr/bin/env python3
"""Build a private, hash-based source ledger without publishing source files."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from pathlib import Path


CODE_EXTENSIONS = {".c", ".cc", ".cpp", ".h", ".hpp", ".py", ".v", ".vhd", ".vhdl", ".sv", ".m"}
IMAGE_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
NOTEBOOK_SUFFIXES = (".ipynb", ".ipynb의 사본")
SENSITIVE = re.compile(r"(?:api[_ -]?key|credential|password|secret|token|license|certificate|수료증|자격증)", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def topic_hint(relative: str) -> str:
    value = relative.lower()
    rules = (
        (("센서",), "sensor-engineering"),
        (("고주파", "mmwave", "fmcw", "radar"), "rf-mmwave-radar"),
        (("pads",), "pcb-pads"),
        (("자동제어", "제어공학", "control"), "control-systems"),
        (("전동기", "전기기기", "motor"), "machines-and-drives"),
        (("디지털 통신", "communication"), "digital-communications"),
        (("전자회로",), "electronic-circuits"),
        (("컨트롤로직", "logic"), "digital-logic-fpga"),
        (("실습_13", "실습_12", "실습_11", "bert", "gpt", "gemini", "huggingface", "이론_11", "이론_13", "이론_14"), "outta-transformers-foundation-models"),
        (("실습_9", "이론9", "rnn", "seq2seq"), "outta-rnn-seq2seq"),
        (("실습_8", "이론_8", "embedding", "오토인코더", "워드임베딩"), "outta-embeddings-autoencoders"),
        (("실습_7", "이론_7", "언어_모델"), "outta-language-models"),
        (("실습_4", "이론4", "cnn", "데이터로더", "전이학습", "nested-02"), "outta-cnn-data-transfer"),
        (("실습_3", "이론3", "approximator"), "outta-neural-networks"),
        (("실습1", "실습2", "이론 1", "이론 2", "선형_회귀", "자동미분"), "outta-ml-foundations"),
        (("프로젝트", "nested-01", "nested-03"), "outta-projects"),
    )
    for terms, topic in rules:
        if any(term in value for term in terms):
            return topic
    return "source-review"


def classify(path: Path, relative: str, duplicate_of: str | None) -> tuple[str, str]:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if path.stat().st_size == 0:
        return "F_EMPTY", "E_PRIVATE_MASTER"
    if duplicate_of:
        return "F_DUPLICATE", "E_PRIVATE_MASTER"
    if SENSITIVE.search(name) or suffix in {".dat", ".lic", ".key", ".pem", ".p12", ".pfx"}:
        return "PRIVATE_SENSITIVE", "E_PRIVATE_MASTER"
    if name.endswith(NOTEBOOK_SUFFIXES):
        return "NOTEBOOK_REVIEW", "A_BLOG_SOURCE+C_SANITIZED_NOTEBOOK+E_PRIVATE_MASTER"
    if suffix in CODE_EXTENSIONS:
        return "CODE_REVIEW", "A_BLOG_SOURCE+C_SANITIZED_CODE+E_PRIVATE_MASTER"
    if suffix in {".pdf", ".ppt", ".pptx"}:
        return "INSTRUCTIONAL_SOURCE", "A_BLOG_SOURCE+B_NOTION_SOURCE+E_PRIVATE_MASTER"
    if suffix in IMAGE_EXTENSIONS:
        if "nested-02" in relative.lower():
            return "DATASET_IMAGE", "A_AGGREGATE_STUDY_SOURCE+E_PRIVATE_MASTER"
        return "IMAGE_REVIEW", "A_BLOG_SOURCE+D_PUBLIC_VISUAL_IF_RIGHTS_CLEAR+E_PRIVATE_MASTER"
    if suffix in {".zip", ".7z", ".rar"}:
        return "SOURCE_ARCHIVE", "E_PRIVATE_MASTER"
    return "SUPPORT_OR_DATA", "A_AGGREGATE_STUDY_SOURCE+E_PRIVATE_MASTER"


def build(root: Path) -> list[dict]:
    root = root.resolve(strict=True)
    seen: dict[str, str] = {}
    records = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if "manifests" in path.relative_to(root).parts:
            continue
        relative = path.relative_to(root).as_posix()
        digest = sha256(path)
        duplicate_of = seen.get(digest)
        classification, destinations = classify(path, relative, duplicate_of)
        records.append(
            {
                "relative_path": relative,
                "bytes": path.stat().st_size,
                "sha256": digest,
                "classification": classification,
                "destinations": destinations,
                "topic": topic_hint(relative),
                "duplicate_of": duplicate_of or "",
            }
        )
        seen.setdefault(digest, relative)
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    args = parser.parse_args()
    if args.json.exists() or args.csv.exists():
        raise FileExistsError("refusing to overwrite an existing manifest")

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    lock_path = args.json.with_name(f"{args.json.name}.lock")
    json_pending = args.json.with_name(f"{args.json.name}.pending")
    csv_pending = args.csv.with_name(f"{args.csv.name}.pending")
    if json_pending.exists() or csv_pending.exists():
        raise FileExistsError("pending manifest exists; archive it before retrying")
    with lock_path.open("x", encoding="utf-8") as handle:
        handle.write(f"root={args.root.resolve()}\n")
        handle.write(f"json={args.json.resolve()}\n")
        handle.write(f"csv={args.csv.resolve()}\n")

    records = build(args.root)
    summary = {
        "root": str(args.root.resolve()),
        "file_count": len(records),
        "total_bytes": sum(record["bytes"] for record in records),
        "records": records,
    }
    with json_pending.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    with csv_pending.open("x", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys() if records else ["relative_path"])
        writer.writeheader()
        writer.writerows(records)
    if args.json.exists() or args.csv.exists():
        raise FileExistsError("manifest output appeared during build; pending files were preserved")
    json_pending.rename(args.json)
    csv_pending.rename(args.csv)
    lock_path.rename(lock_path.with_name(f"{lock_path.name}.completed-{time.time_ns()}"))
    print(json.dumps({"file_count": summary["file_count"], "total_bytes": summary["total_bytes"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
