#!/usr/bin/env python3
"""Create consistent 16:9 course thumbnails from already reviewed visuals."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[2]
LEGACY = Path(
    "D:/Codex_Workspaces/2026-07-28/files-mentioned-by-the-user-shift/work/repos/"
    "electrical-engineering-coursework-portfolio/docs"
)
OUTPUT = REPO / "src/assets/images/study/coursework"

SOURCES = {
    "controller-logic": (LEGACY / "gallery/controller-logic/mealy-101-waveform.png", "컨트롤로직설계"),
    "automatic-control": (LEGACY / "assets/motor/speed_response_psim_archive.png", "자동제어"),
    "applied-control": (LEGACY / "assets/motor/current_response_psim_archive.png", "제어공학 응용"),
    "high-frequency-engineering": (LEGACY / "gallery/rf-microwave/wilkinson-sparameter.png", "고주파공학"),
    "electrical-machines": (LEGACY / "assets/transformer/core_tradeoff_chart.png", "전기기기"),
    "motor-control": (LEGACY / "assets/motor/torque_ripple_comparison.png", "전동기제어"),
}

DETAIL_SOURCES = {
    "controller-logic-waveform": LEGACY / "gallery/controller-logic/mealy-101-waveform.png",
    "high-frequency-wilkinson": LEGACY / "gallery/rf-microwave/wilkinson-sparameter.png",
    "high-frequency-hybrid": LEGACY / "gallery/rf-microwave/hybrid-schematic.png",
    "electrical-machines-transformer": LEGACY / "assets/transformer/core_tradeoff_chart.png",
    "motor-control-ripple": LEGACY / "assets/motor/torque_ripple_comparison.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = Path("C:/Windows/Fonts/malgunbd.ttf")
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for slug, (source, title) in SOURCES.items():
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as raw:
            image = ImageOps.exif_transpose(raw).convert("RGB")
            canvas = ImageOps.fit(image, (1200, 675), Image.Resampling.LANCZOS)
        overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle((0, 505, 1200, 675), fill=(8, 21, 38, 230))
        draw.text((48, 545), title, fill="white", font=font(46))
        result = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        destination = OUTPUT / f"{slug}.webp"
        result.save(destination, "WEBP", quality=82, method=6, exif=b"")
        print(f"{destination.name}: {digest(destination)}")
    for slug, source in DETAIL_SOURCES.items():
        if not source.is_file():
            raise FileNotFoundError(source)
        with Image.open(source) as raw:
            detail = ImageOps.exif_transpose(raw).convert("RGB")
            detail.thumbnail((1600, 1200), Image.Resampling.LANCZOS)
        destination = OUTPUT / f"{slug}.webp"
        detail.save(destination, "WEBP", quality=84, method=6, exif=b"")
        print(f"{destination.name}: {digest(destination)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
