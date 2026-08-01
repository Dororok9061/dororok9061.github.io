#!/usr/bin/env python3
"""Build privacy-safe study images from the verified D: source copies.

The script never changes source files.  It strips metadata while creating WebP
derivatives and records SHA-256 values in a D:-resident manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import shutil
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


PADS_FILENAMES = (
    "스크린샷 2026-02-11 163556.png",
    "스크린샷 2026-02-11 163945.png",
    "스크린샷 2026-02-12 181422.png",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def find_ffmpeg() -> Path:
    command = shutil.which("ffmpeg")
    if command:
        return Path(command)
    packages = Path.home() / "AppData/Local/Microsoft/WinGet/Packages"
    matches = sorted(packages.glob("Gyan.FFmpeg_*/ffmpeg-*/bin/ffmpeg.exe"))
    if matches:
        return matches[-1]
    raise FileNotFoundError("ffmpeg executable not found; pass --ffmpeg")


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


def video_frame(ffmpeg: Path, source: Path) -> Image.Image:
    command = (
        str(ffmpeg), "-v", "error", "-ss", "1", "-i", str(source),
        "-frames:v", "1", "-vf", "scale=640:-2", "-f", "image2pipe",
        "-vcodec", "mjpeg", "pipe:1",
    )
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE)
    with Image.open(io.BytesIO(result.stdout)) as frame:
        return frame.convert("RGB")


def labelled_tile(image: Image.Image, label: str, size: tuple[int, int]) -> Image.Image:
    width, height = size
    tile = Image.new("RGB", size, "#f7f7f5")
    fitted = ImageOps.fit(image.convert("RGB"), (width, height - 34), Image.Resampling.LANCZOS)
    tile.paste(fitted, (0, 0))
    draw = ImageDraw.Draw(tile)
    draw.rectangle((0, height - 34, width, height), fill="#081526")
    draw.text((10, height - 29), label, fill="white", font=font(16))
    return tile


def board_sheet(board: Path, ffmpeg: Path) -> tuple[Image.Image, list[dict[str, object]]]:
    files = sorted(path for path in board.rglob("*") if path.is_file())
    records: list[dict[str, object]] = []
    images: list[tuple[str, Image.Image]] = []
    for source in files:
        relative = source.relative_to(board.parent)
        record: dict[str, object] = {
            "path": relative.as_posix(),
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
        }
        if any(part.startswith("뒤") for part in relative.parts):
            record["used_as"] = "hashed only; rear-side identifiers withheld"
            records.append(record)
            continue
        if source.suffix.lower() == ".jpg":
            with Image.open(source) as raw:
                images.append(("still photo", ImageOps.exif_transpose(raw).convert("RGB")))
            record["used_as"] = "still photo"
        elif source.suffix.lower() == ".mp4":
            frame = video_frame(ffmpeg, source)
            label = source.parent.name.replace("_", " ")
            images.append((label, frame))
            record["used_as"] = "frame at 1 second"
        else:
            record["used_as"] = "manifest only"
        records.append(record)

    if not images:
        raise RuntimeError(f"No image sources in {board}")
    cell = (480, 304)
    columns = 3
    rows = (len(images) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell[0], rows * cell[1] + 54), "#ececea")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, canvas.width, 54), fill="#ffffff")
    draw.text((18, 14), f"STM32F411 board set · {board.name}", fill="#081526", font=font(23))
    for index, (label, image) in enumerate(images):
        x = (index % columns) * cell[0]
        y = 54 + (index // columns) * cell[1]
        canvas.paste(labelled_tile(image, label, cell), (x, y))
    return canvas, records


def prepare_stm(source_root: Path, output_root: Path, ffmpeg: Path) -> tuple[list[dict[str, object]], list[Path]]:
    records: list[dict[str, object]] = []
    board_outputs: list[Path] = []
    overview_images: list[tuple[str, Image.Image]] = []
    boards = sorted((path for path in source_root.iterdir() if path.is_dir()), key=lambda p: int(p.name.split("_")[-1]))
    for board in boards:
        sheet, board_records = board_sheet(board, ffmpeg)
        destination = output_root / f"{board.name}-contact-sheet.webp"
        save_webp(sheet, destination, quality=76)
        board_outputs.append(destination)
        records.extend(board_records)
        overview_images.append((board.name.upper(), sheet.crop((0, 54, sheet.width, sheet.height))))

    cell = (360, 230)
    columns = 4
    rows = (len(overview_images) + columns - 1) // columns
    overview = Image.new("RGB", (columns * cell[0], rows * cell[1] + 70), "#ececea")
    draw = ImageDraw.Draw(overview)
    draw.rectangle((0, 0, overview.width, 70), fill="#ffffff")
    draw.text((22, 17), "STM32F411 inspection archive · 20 board views", fill="#081526", font=font(27))
    for index, (label, image) in enumerate(overview_images):
        x = (index % columns) * cell[0]
        y = 70 + (index // columns) * cell[1]
        overview.paste(labelled_tile(image, label, cell), (x, y))
    overview_path = output_root / "stm32f411-board-overview.webp"
    save_webp(overview, overview_path, quality=78)
    board_outputs.append(overview_path)
    return records, board_outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--pads-root", type=Path, default=Path("D:/Codex/private-master/pads/2026/사진"))
    parser.add_argument("--stm-root", type=Path, default=Path("D:/OneDrive-migration-staging/단국대/pcb/stm"))
    parser.add_argument("--ffmpeg", type=Path)
    parser.add_argument("--manifest-dir", type=Path, default=Path("D:/Codex/private-master/manifests"))
    args = parser.parse_args()

    ffmpeg = args.ffmpeg or find_ffmpeg()
    if not ffmpeg.is_file():
        raise FileNotFoundError(ffmpeg)
    image_root = args.repo / "src" / "assets" / "images" / "study"
    pads_outputs = prepare_pads(args.pads_root, image_root / "pads")
    stm_records, stm_outputs = prepare_stm(args.stm_root, image_root / "stm32", ffmpeg)

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
