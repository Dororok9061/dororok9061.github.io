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

Two SFH7070 optical-sensor signals feed OPA2333-based analog front ends and the
STM32F411 ADC A0/A1 inputs. I placed the 5-V input, 3.3-V LDO, two clocks, SWD,
and UART on the same board and completed a two-layer layout with bottom-side
ground copper.

The archive contains KiCad schematic/PCB sources plus copper, mask, paste,
silkscreen, and PTH/NPTH drill outputs. Measured PPG waveform quality, SNR,
filter cutoff, and biosignal accuracy require a separate bench-validation stage.
