#!/usr/bin/env python3
"""Validate the sanitized full-source ledger against its private manifest."""

from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import hashlib
import json
import os
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
CSV_MAP = ROOT / "docs" / "internal" / "FULL_SOURCE_TO_PAGE_MAP.csv"
JSON_MAP = ROOT / "docs" / "internal" / "FULL_SOURCE_TO_PAGE_MAP.json"
FIELDS = (
    "source_id",
    "source_path",
    "sha256",
    "file_type",
    "course",
    "project",
    "day",
    "topic",
    "page_slide_sheet_cell",
    "extracted_visual",
    "blog_url",
    "notion_url",
    "github_url",
    "private_master_path",
    "disposition",
    "bytes",
)
EXPECTED_SOURCE_COUNT = 6380
EXPECTED_TOTAL_BYTES = 3137214983
EXPECTED_PUBLIC_COUNT = 492
EXPECTED_MANIFEST_SHA256 = "6B6FD14AB0E80AC1338DE9877F1214BAA9676248CC31671BBFC445AEEC5B89A0"
DISPOSITIONS = {
    "Private Master",
    "Blog Source",
    "Sanitized Notebook",
    "Sanitized Code",
    "Public Visual Pending Rights Review",
}
FILE_TYPE_BY_CLASSIFICATION = {
    "CODE_REVIEW": "code",
    "DATASET_IMAGE": "dataset-image",
    "F_DUPLICATE": "duplicate",
    "IMAGE_REVIEW": "image",
    "INSTRUCTIONAL_SOURCE": "instructional-document",
    "NOTEBOOK_REVIEW": "notebook",
    "PRIVATE_SENSITIVE": "private-sensitive",
    "SOURCE_ARCHIVE": "archive",
    "SUPPORT_OR_DATA": "support-or-data",
}
PAGE_BY_TOPIC = {
    "control-systems": "/coursework/automatic-control/",
    "digital-communications": "/coursework/digital-communications/",
    "digital-logic-fpga": "/blog/category/fpga-rtl-dv/",
    "machines-and-drives": "/coursework/electrical-machines/",
    "outta-cnn-data-transfer": "/blog/2026/08/01/outta-cnn-pytorch/",
    "outta-embeddings-autoencoders": "/blog/2026/08/01/outta-language-model-embedding/",
    "outta-language-models": "/blog/2026/08/01/outta-language-model-embedding/",
    "outta-ml-foundations": "/blog/2026/08/01/outta-data-autodiff-regression/",
    "outta-neural-networks": "/blog/2026/08/01/outta-neural-network-classification/",
    "outta-projects": "/learning/bootcamps/outta-basic-2024/",
    "outta-rnn-seq2seq": "/blog/2026/08/01/outta-rnn-seq2seq/",
    "outta-transformers-foundation-models": "/blog/2026/08/01/outta-bert-huggingface-gemini/",
    "pcb-pads": "/study/pads/",
    "rf-mmwave-radar": "/study/mmwave/",
    "sensor-engineering": "/coursework/",
    "source-review": "/blog/",
}
COURSE_BY_TOPIC = {
    "control-systems": "Automatic Control",
    "digital-communications": "Digital Communications",
    "digital-logic-fpga": "Controller Logic Design",
    "machines-and-drives": "Electrical Machines",
    "outta-cnn-data-transfer": "OUTTA Basic 2024",
    "outta-embeddings-autoencoders": "OUTTA Basic 2024",
    "outta-language-models": "OUTTA Basic 2024",
    "outta-ml-foundations": "OUTTA Basic 2024",
    "outta-neural-networks": "OUTTA Basic 2024",
    "outta-projects": "OUTTA Basic 2024",
    "outta-rnn-seq2seq": "OUTTA Basic 2024",
    "outta-transformers-foundation-models": "OUTTA Basic 2024",
    "pcb-pads": "PADS / PCB Design",
    "rf-mmwave-radar": "RF / mmWave Radar",
    "sensor-engineering": "Sensor Engineering",
    "source-review": "",
}
PROJECT_BY_TOPIC = {
    "outta-projects": "OUTTA P-1 / P-2 / P-3",
    "pcb-pads": "PADS / PPG Board",
    "rf-mmwave-radar": "mmWave / FMCW Radar",
}
ID_RE = re.compile(r"src-[0-9a-f]{64}(?:-[0-9]{4})?")
SAFE_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9-]*")
LEAK_RE = re.compile(r"(?i)(?:(?:^|[^a-z0-9])[a-z]:[\\/]|\\\\|/users/|/home/|onedrive|file://|relative_path)")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest().upper()


def manifest_path(argument: str | None) -> Path | None:
    value = argument or os.environ.get("PRIVATE_SOURCE_MANIFEST")
    return Path(value) if value else None


def read_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("records")
    if not isinstance(records, list):
        raise ValueError("private manifest has no records list")
    if data.get("file_count") != len(records):
        raise ValueError("private manifest file_count differs from records")
    if data.get("total_bytes") != sum(int(row["bytes"]) for row in records):
        raise ValueError("private manifest byte total differs from records")
    return data


def disposition(raw: str) -> str:
    upper = raw.upper()
    if not any(marker in upper for marker in ("PUBLIC", "BLOG", "SANITIZED")):
        return "Private Master"
    if "SANITIZED_NOTEBOOK" in upper:
        return "Sanitized Notebook"
    if "SANITIZED_CODE" in upper:
        return "Sanitized Code"
    if "PUBLIC_VISUAL" in upper:
        return "Public Visual Pending Rights Review"
    return "Blog Source"


def build_rows(manifest: dict) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in manifest["records"]:
        sha = str(record["sha256"]).upper()
        if not re.fullmatch(r"[0-9A-F]{64}", sha):
            raise ValueError("private manifest contains an invalid SHA-256")
        groups[sha].append(record)

    rows: list[dict] = []
    for sha, records in sorted(groups.items()):
        ordered = sorted(records, key=lambda row: str(row["relative_path"]))
        for index, record in enumerate(ordered, 1):
            suffix = f"-{index:04d}" if len(ordered) > 1 else ""
            source_id = f"src-{sha.lower()}{suffix}"
            current_disposition = disposition(str(record["destinations"]))
            topic = str(record["topic"])
            if current_disposition == "Private Master":
                blog_url = ""
            else:
                try:
                    blog_url = PAGE_BY_TOPIC[topic]
                except KeyError as error:
                    raise ValueError("public source has no allowlisted topic page") from error
            try:
                file_type = FILE_TYPE_BY_CLASSIFICATION[str(record["classification"])]
            except KeyError as error:
                raise ValueError("private manifest contains an unknown classification") from error
            rows.append(
                {
                    "source_id": source_id,
                    "source_path": f"private://{source_id}",
                    "sha256": sha,
                    "file_type": file_type,
                    "course": COURSE_BY_TOPIC.get(topic, ""),
                    "project": PROJECT_BY_TOPIC.get(topic, ""),
                    "day": "",
                    "topic": topic,
                    "page_slide_sheet_cell": "",
                    "extracted_visual": "",
                    "blog_url": blog_url,
                    "notion_url": "",
                    "github_url": "",
                    "private_master_path": f"private://{source_id}",
                    "disposition": current_disposition,
                    "bytes": int(record["bytes"]),
                }
            )
    return sorted(rows, key=lambda row: row["source_id"])


def write_maps(manifest_file: Path, manifest: dict) -> None:
    rows = build_rows(manifest)
    JSON_MAP.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "source_count": len(rows),
        "total_bytes": sum(row["bytes"] for row in rows),
        "public_record_count": sum(bool(row["blog_url"]) for row in rows),
        "source_manifest_sha256": digest(manifest_file),
        "records": rows,
    }
    JSON_MAP.write_text(
        json.dumps(payload, ensure_ascii=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    with CSV_MAP.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def read_maps() -> tuple[dict, list[dict], list[str]]:
    errors: list[str] = []
    try:
        payload = json.loads(JSON_MAP.read_text(encoding="utf-8"))
        json_rows = payload["records"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError, TypeError) as error:
        return {}, [], [f"JSON map cannot be read: {type(error).__name__}"]
    try:
        with CSV_MAP.open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream)
            if tuple(reader.fieldnames or ()) != FIELDS:
                errors.append("CSV fields differ from the map schema")
            csv_rows = list(reader)
    except FileNotFoundError:
        return payload, json_rows, errors + ["CSV map is missing"]

    normalized_csv = [dict(row, bytes=int(row["bytes"])) for row in csv_rows]
    if normalized_csv != json_rows:
        errors.append("JSON and CSV records differ")
    return payload, json_rows, errors


def validate_snapshot(payload: dict, rows: list[dict]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != 1:
        errors.append("unsupported map schema")
    if payload.get("source_count") != len(rows):
        errors.append("source_count differs from mapped records")
    if payload.get("total_bytes") != sum(row.get("bytes", 0) for row in rows):
        errors.append("total_bytes differs from mapped records")
    if payload.get("public_record_count") != sum(bool(row.get("blog_url")) for row in rows):
        errors.append("public_record_count differs from mapped records")
    if payload.get("source_count") != EXPECTED_SOURCE_COUNT:
        errors.append("mapped snapshot does not contain the expected 6380 sources")
    if payload.get("total_bytes") != EXPECTED_TOTAL_BYTES:
        errors.append("mapped snapshot byte total differs from the verified ledger")
    if payload.get("public_record_count") != EXPECTED_PUBLIC_COUNT:
        errors.append("mapped snapshot public-derivative count differs from the verified ledger")
    if payload.get("source_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
        errors.append("mapped snapshot manifest SHA-256 differs from the verified ledger")
    source_ids = [row.get("source_id", "") for row in rows]
    if len(source_ids) != len(set(source_ids)):
        errors.append("Source IDs are not unique")
    for row in rows:
        source_id = row.get("source_id", "")
        if not ID_RE.fullmatch(source_id):
            errors.append("invalid Source ID")
        sha = row.get("sha256", "")
        if not re.fullmatch(r"[0-9A-F]{64}", sha):
            errors.append("invalid source SHA-256")
        elif not re.fullmatch(rf"src-{sha.lower()}(?:-[0-9]{{4}})?", source_id):
            errors.append("Source ID is not derived from its SHA-256")
        if row.get("source_path") != f"private://{source_id}":
            errors.append("Source Path is not its private Source ID URI")
        if row.get("private_master_path") != f"private://{source_id}":
            errors.append("Private Master Path is not its private Source ID URI")
        if row.get("file_type") not in FILE_TYPE_BY_CLASSIFICATION.values():
            errors.append("file type is not allowlisted")
        if not SAFE_TOKEN_RE.fullmatch(row.get("topic", "")):
            errors.append("topic is not a safe token")
        if row.get("disposition") not in DISPOSITIONS:
            errors.append("disposition is not allowlisted")
        if not row.get("private_master_path"):
            errors.append("Source ID has no Private Master mapping")
        if any(LEAK_RE.search(str(value)) for value in row.values()):
            errors.append("map contains a local path marker")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", help="private manifest used for local verification")
    parser.add_argument("--write", action="store_true", help="regenerate sanitized maps")
    args = parser.parse_args()
    private_path = manifest_path(args.manifest)

    if args.write:
        if private_path is None or not private_path.is_file():
            print("FAIL: --write requires an accessible private manifest")
            return 1
        try:
            private_manifest = read_manifest(private_path)
            write_maps(private_path, private_manifest)
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            print(f"FAIL: map generation failed: {type(error).__name__}: {error}")
            return 1

    payload, rows, errors = read_maps()
    errors.extend(validate_snapshot(payload, rows))
    if private_path is None:
        print("DEGRADED: private manifest unavailable; validated sanitized snapshot only")
    elif not private_path.is_file():
        errors.append("configured private manifest is unavailable")
    else:
        try:
            current = read_manifest(private_path)
            if digest(private_path) != payload.get("source_manifest_sha256"):
                errors.append("private manifest SHA-256 differs from mapped snapshot")
            if current.get("file_count") != payload.get("source_count"):
                errors.append("private manifest count differs from mapped snapshot")
            if build_rows(current) != rows:
                errors.append("private manifest records differ from mapped snapshot")
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            errors.append(f"private manifest validation failed: {type(error).__name__}: {error}")

    if errors:
        for error in dict.fromkeys(errors):
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: all {len(rows)} private Source IDs have sanitized mappings with JSON/CSV parity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
