#!/usr/bin/env python3
"""Build privacy-safe study images from the verified D: source copies.

The script never changes source files.  It strips metadata while creating WebP
derivatives and records SHA-256 values in a D:-resident manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


PADS_FILENAMES = (
    "스크린샷 2026-02-11 163556.png",
    "스크린샷 2026-02-11 163945.png",
    "스크린샷 2026-02-12 181422.png",
)

STM_PHOTO_EXPORTS = {
    "nucleo-f411-board.webp": "KakaoTalk_20260801_161801523_01.jpg",
    "prototype-electrodes.webp": "KakaoTalk_20260801_161730125_12.jpg",
    "prototype-analog-front-end.webp": "KakaoTalk_20260801_161730125_14.jpg",
    "prototype-adc-timer.webp": "KakaoTalk_20260801_161730125_15.jpg",
    "prototype-status-led.webp": "KakaoTalk_20260801_161730125_21.jpg",
    "prototype-powered.webp": "KakaoTalk_20260801_161801523.jpg",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def save_webp(image: Image.Image, destination: Path, *, quality: int = 82) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    clean = image.convert("RGB")
    clean.save(destination, "WEBP", quality=quality, method=6, exif=b"")


def prepare_pads(source_root: Path, output_root: Path) -> list[dict[str, object]]:
    outputs: list[dict[str, object]] = []
    names = ("pads-soic-decal-a.webp", "pads-soic-decal-b.webp", "pads-ppg-layout.webp")
    for source_name, output_name in zip(PADS_FILENAMES, names, strict=True):
        source = source_root / source_name
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as raw:
            image = ImageOps.exif_transpose(raw)
            image.thumbnail((1920, 1280), Image.Resampling.LANCZOS)
            destination = output_root / output_name
            save_webp(image, destination)
        outputs.append(
            {
                "source": source.name,
                "source_sha256": sha256(source),
                "output": destination.name,
                "output_sha256": sha256(destination),
            }
        )
    return outputs


def labelled_tile(image: Image.Image, label: str, size: tuple[int, int]) -> Image.Image:
    width, height = size
    tile = Image.new("RGB", size, "#f7f7f5")
    fitted = ImageOps.fit(image.convert("RGB"), (width, height - 34), Image.Resampling.LANCZOS)
    tile.paste(fitted, (0, 0))
    draw = ImageDraw.Draw(tile)
    draw.rectangle((0, height - 34, width, height), fill="#081526")
    draw.text((10, height - 29), label, fill="white", font=font(16))
    return tile


def prepare_stm(source_root: Path, output_root: Path) -> tuple[list[dict[str, object]], list[Path]]:
    photo_root = source_root / "ppg, ecg 회로"
    photos = sorted(photo_root.glob("*.jpg"))
    if len(photos) != 22:
        raise RuntimeError(f"Expected 22 STM32 prototype photos, found {len(photos)}")

    records: list[dict[str, object]] = []
    outputs: list[Path] = []
    selected = set(STM_PHOTO_EXPORTS.values())
    for source in photos:
        records.append(
            {
                "path": source.relative_to(source_root).as_posix(),
                "bytes": source.stat().st_size,
                "sha256": sha256(source),
                "used_as": "overview and detail" if source.name in selected else "overview",
            }
        )

    cell = (256, 188)
    columns = 6
    overview = Image.new("RGB", (1600, 900), "#ececea")
    draw = ImageDraw.Draw(overview)
    draw.rectangle((0, 0, overview.width, 88), fill="#ffffff")
    draw.text((28, 22), "STM32F411 ECG · PPG prototype · 22 source photos", fill="#081526", font=font(30))
    for index, source in enumerate(photos):
        with Image.open(source) as raw:
            image = ImageOps.exif_transpose(raw).convert("RGB")
            tile = ImageOps.fit(image, cell, Image.Resampling.LANCZOS)
        x = 24 + (index % columns) * cell[0]
        y = 104 + (index // columns) * cell[1]
        overview.paste(tile, (x, y))
    overview_path = output_root / "stm32-prototype-overview.webp"
    save_webp(overview, overview_path, quality=78)
    outputs.append(overview_path)

    for output_name, source_name in STM_PHOTO_EXPORTS.items():
        source = photo_root / source_name
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as raw:
            image = ImageOps.exif_transpose(raw).convert("RGB")
            image.thumbnail((1180, 680), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (1280, 720), "#f7f7f5")
            canvas.paste(image, ((1280 - image.width) // 2, (720 - image.height) // 2))
        destination = output_root / output_name
        save_webp(canvas, destination, quality=80)
        outputs.append(destination)
    return records, outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--pads-root", type=Path, default=Path("D:/Codex/private-master/pads/2026/사진"))
    parser.add_argument("--stm-root", type=Path, default=Path("D:/Codex/private-master/stm/2026"))
    parser.add_argument("--manifest-dir", type=Path, default=Path("D:/Codex/private-master/manifests"))
    args = parser.parse_args()

    image_root = args.repo / "src" / "assets" / "images" / "study"
    pads_outputs = prepare_pads(args.pads_root, image_root / "pads")
    stm_records, stm_outputs = prepare_stm(args.stm_root, image_root / "stm32")

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "D sources read-only; public WebP derivatives strip metadata",
        "pads": pads_outputs,
        "stm": {
            "source_files": len(stm_records),
            "source_bytes": sum(int(record["bytes"]) for record in stm_records),
            "records": stm_records,
            "outputs": [
                {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
                for path in stm_outputs
            ],
        },
    }
    args.manifest_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    manifest_path = args.manifest_dir / f"d-source-stm-pads-public-derivatives-{stamp}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"PADS outputs: {len(pads_outputs)}")
    print(f"STM inputs: {len(stm_records)}")
    print(f"STM outputs: {len(stm_outputs)}")
    print(f"Manifest: {manifest_path}")
    print(f"Manifest SHA256: {sha256(manifest_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
