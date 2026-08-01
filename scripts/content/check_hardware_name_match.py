#!/usr/bin/env python3
"""Check source-faithful STM32 and separated embedded-system facts."""

from __future__ import annotations

import re

from provenance_common import courses, fail, track


def main() -> int:
    errors: list[str] = []
    stm32 = track("stm32")
    required_stm32 = (
        "실험 사진 22장",
        "STM 사용법 40장",
        "3쪽 KiCad 회로도",
        "ADC·TIM1·UART 코드",
        "CMSIS-DSP biquad",
        "STM32F411RETx",
        "ECG는 PA0, PPG는 PA1, APG는 PA4",
        "TIM1 update interrupt",
        "저장된 출력 Cell이나 정량 정확도 기록은 없어",
        "/assets/images/study/stm32/stm32-prototype-overview.webp",
        "/assets/images/study/stm32/mcu-schematic.webp",
        "/assets/images/study/stm32/biosignal-schematic.webp",
    )
    forbidden_stm32 = (
        "정지사진 19장과 영상 99개",
        "twenty board sets",
        "board inspection",
        "stm32f411-board-overview.webp",
        "f411_1-contact-sheet.webp",
        "f411_20-contact-sheet.webp",
    )
    if not stm32:
        errors.append("STM32 engineering track is missing")
    else:
        for fact in required_stm32:
            if fact not in stm32:
                errors.append(f"STM32 fact missing: {fact}")
        for fact in forbidden_stm32:
            if fact.lower() in stm32.lower():
                errors.append(f"obsolete PCB-inspection fact remains in STM32 track: {fact}")
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
    return fail("STM32 biosignal sources and embedded-system boundaries match public assets", errors)


if __name__ == "__main__":
    raise SystemExit(main())
