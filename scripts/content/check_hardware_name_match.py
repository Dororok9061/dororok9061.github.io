#!/usr/bin/env python3
"""Check source-faithful STM32 and separated embedded-system facts."""

from __future__ import annotations

import re

from provenance_common import courses, fail, track


def main() -> int:
    errors: list[str] = []
    stm32 = track("stm32")
    required_stm32 = (
        "정지사진 19장과 영상 99개를 보드 20세트로",
        "후면의 QR과 일련번호가 보이는 장면은 올리지 않았다",
        "보드 한 장을 네 화면으로 확인하기",
        "F411 1번 보드의 앞면과 근접 화면 네 장",
        "앞면 영상에서 고른 세 장을 사용했다",
        "nineteen STM32F411 still photos and ninety-nine videos into twenty board sets",
        "rear views showing QR codes or serial numbers",
        "Inspecting One Board in Four Panels",
        "three panels selected from front-view videos",
        "/assets/images/study/stm32/f411_1-contact-sheet.webp",
        "/assets/images/study/stm32/f411_20-contact-sheet.webp",
    )
    if not stm32:
        errors.append("STM32 engineering track is missing")
    else:
        for fact in required_stm32:
            if fact not in stm32:
                errors.append(f"STM32 fact missing: {fact}")
        if "118개" in stm32 or "118 STM32F411 photos and videos" in stm32:
            errors.append("STM32 source files are presented as 118 independent results")
        images = re.findall(r"image:\s*(/assets/[^,\s}]+)", stm32)
        if len(images) != 8 or any(not image.startswith("/assets/images/study/stm32/") for image in images):
            errors.append(f"expected 8 STM32 unit images in STM32 namespace, found {len(images)}")

    embedded = next((course for course in courses() if course.id == "embedded-systems"), None)
    if not embedded:
        errors.append("embedded-systems course record is missing")
    else:
        if "units: []" not in embedded.block:
            errors.append("embedded-systems must not fabricate weekly coursework units")
        link_count = len(re.findall(r"(?m)^    - title_ko:", embedded.block))
        if link_count != 3:
            errors.append(f"embedded-systems must expose 3 separate links, found {link_count}")
        if "/assets/images/projects/" in embedded.block:
            errors.append("embedded-systems coursework record uses a project photo")
    return fail("STM32 panel facts and embedded-system boundaries match public assets", errors)


if __name__ == "__main__":
    raise SystemExit(main())
