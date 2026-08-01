#!/usr/bin/env python3
"""Map stored Notebook image outputs to derived public assets by pixel similarity."""

from __future__ import annotations

import argparse
import base64
import csv
import io
import itertools
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image


def rgb_array(image: Image.Image) -> np.ndarray:
    return np.asarray(image.convert("RGB"), dtype=np.int16)


def mse(left: np.ndarray, right: np.ndarray) -> float:
    difference = left - right
    return float(np.mean(difference * difference))


def notebook_images(root: Path) -> list[dict]:
    records = []
    for path in sorted(root.rglob("*")):
        if ".ipynb" not in path.name or path.name.endswith(".ipynb"):
            continue
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell_index, cell in enumerate(notebook.get("cells", [])):
            for output_index, output in enumerate(cell.get("outputs", [])):
                data = output.get("data", {})
                for mime in ("image/png", "image/jpeg"):
                    if mime not in data:
                        continue
                    encoded = data[mime]
                    if isinstance(encoded, list):
                        encoded = "".join(encoded)
                    image = Image.open(io.BytesIO(base64.b64decode(encoded)))
                    records.append(
                        {
                            "notebook": path.name,
                            "cell_index": cell_index,
                            "output_index": output_index,
                            "mime": mime,
                            "width": image.width,
                            "height": image.height,
                            "pixels": rgb_array(image),
                        }
                    )
    return records


def public_assets(root: Path) -> list[dict]:
    records = []
    for path in sorted(root.glob("notebook-*.webp")):
        with Image.open(path) as image:
            records.append(
                {
                    "asset": path.name,
                    "width": image.width,
                    "height": image.height,
                    "pixels": rgb_array(image),
                }
            )
    return records


def assign(sources: list[dict], assets: list[dict]) -> list[dict]:
    source_groups: dict[tuple[int, int], list[dict]] = defaultdict(list)
    asset_groups: dict[tuple[int, int], list[dict]] = defaultdict(list)
    for source in sources:
        source_groups[(source["width"], source["height"])].append(source)
    for asset in assets:
        asset_groups[(asset["width"], asset["height"])].append(asset)
    if {key: len(value) for key, value in source_groups.items()} != {
        key: len(value) for key, value in asset_groups.items()
    }:
        raise ValueError("source and asset dimension distributions differ")

    mapped = []
    for size, group in source_groups.items():
        candidates = asset_groups[size]
        best = None
        for permutation in itertools.permutations(candidates):
            score = sum(mse(source["pixels"], asset["pixels"]) for source, asset in zip(group, permutation))
            if best is None or score < best[0]:
                best = (score, permutation)
        assert best is not None
        for source, asset in zip(group, best[1]):
            mapped.append(
                {
                    "asset": asset["asset"],
                    "notebook": source["notebook"],
                    "cell_index": source["cell_index"],
                    "output_index": source["output_index"],
                    "mime": source["mime"],
                    "width": source["width"],
                    "height": source["height"],
                    "pixel_mse": round(mse(source["pixels"], asset["pixels"]), 6),
                }
            )
    return sorted(mapped, key=lambda item: int(item["asset"].split("-")[1].split(".")[0]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook_root", type=Path)
    parser.add_argument("asset_root", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    args = parser.parse_args()
    if args.json.exists() or args.csv.exists():
        raise FileExistsError("refusing to overwrite an existing mapping")
    mapping = assign(notebook_images(args.notebook_root), public_assets(args.asset_root))
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with args.csv.open("x", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=mapping[0].keys())
        writer.writeheader()
        writer.writerows(mapping)
    print(json.dumps({"mapped": len(mapping), "max_pixel_mse": max(item["pixel_mse"] for item in mapping)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
