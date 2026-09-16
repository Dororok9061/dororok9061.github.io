---
layout: project
project_id: stm32f411-ppg-pcb
title: STM32F411 PPG Analog Front-End PCB
description: A KiCad PCB integrating two SFH7070 optical sensors, OPA2333 front ends, and STM32F411 through fabrication outputs.
permalink: /en/projects/stm32f411-ppg-pcb/
lang: en
alternate_url: /projects/stm32f411-ppg-pcb/
alternate_lang: ko
---

Two SFH7070 sensor signals pass through OPA2333 amplification/filter stages into STM32F411 ADC A0/A1. The two-layer board includes a 5-V input, 3.3-V LDO, 8-MHz/32.768-kHz clocks, SWD, UART, and bottom-side ground copper.

- [Schematic, PCB, Gerber, and drill sources](https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/stm32f411-ppg-pcb/source)
- [Power, analog signal, and routing design](/en/blog/2026/09/04/stm32f411-ppg-pcb/)
- [STM32 sensor-acquisition notes](/en/blog/series/stm32-sensor-acquisition/)
