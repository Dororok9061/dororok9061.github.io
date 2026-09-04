---
layout: project
project_id: stm32f411-ppg-pcb
title: STM32F411 PPG Analog Front-End PCB
description: 두 SFH7070 광학 센서와 OPA2333 front-end, STM32F411을 통합하고 제조 파일까지 출력한 KiCad PCB.
permalink: /projects/stm32f411-ppg-pcb/
lang: ko
alternate_url: /en/projects/stm32f411-ppg-pcb/
alternate_lang: en
---

두 SFH7070 센서의 작은 광학 신호를 OPA2333 기반 analog front-end로 받아
STM32F411의 ADC A0/A1에 연결했다. 5 V 입력과 3.3 V LDO, 두 clock, SWD와
UART를 같은 보드에 배치하고 bottom GND plane을 포함한 2-layer PCB로 구성했다.

KiCad 회로·PCB 원본과 copper, mask, paste, silkscreen, PTH·NPTH drill 파일이
남아 있다. 실제 PPG 파형, SNR, filter cutoff와 생체신호 정확도는 별도 측정이
필요하다.
