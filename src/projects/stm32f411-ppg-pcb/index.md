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

두 SFH7070 센서의 광학 신호를 OPA2333 아날로그 회로에서 증폭·필터링해 STM32F411 ADC A0/A1에 입력한다. 5 V 입력·3.3 V LDO·8 MHz/32.768 kHz clock·SWD·UART와 하단 GND plane을 갖춘 2-layer 보드다.

- [회로·PCB·Gerber·drill 원본](https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/stm32f411-ppg-pcb/source)
- [전원·아날로그 신호·배선 설계 기록](/blog/2026/09/04/stm32f411-ppg-pcb/)
- [STM32 센서 취득 학습·구현 기록](/blog/series/stm32-sensor-acquisition/)
