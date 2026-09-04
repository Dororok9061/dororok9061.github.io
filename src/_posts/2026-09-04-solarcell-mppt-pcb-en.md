---
title: Power, Measurement, and Communication Paths in a Multichannel Solar-Cell PCB
title_en: Power, Measurement, and Communication Paths in a Multichannel Solar-Cell PCB
description: Design analysis of power, ADC, DAC, and USB/UART paths across an STM32F401 mainboard and eight-channel measurement module.
date: 2026-09-04 12:10:00 +0900
updated: 2026-09-04 12:10:00 +0900
lang: en
translation_key: solarcell-mppt-pcb
permalink: /en/blog/2026/09/04/solarcell-mppt-pcb/
alternate_url: /blog/2026/09/04/solarcell-mppt-pcb/
alternate_lang: ko
primary_category: pcb-pads
subcategory: schematic
series: pads-pcb-design
series_order: 7
post_type: project-log
practical: true
difficulty: advanced
study_status: published
evidence_status: DESIGN_ARCHIVE
tools: [PADS Logic, PADS Layout, STM32F401, AD7997, AD5629R, OPA703]
hardware: [Solar-cell measurement mainboard, Measurement module]
software_versions: []
source_materials:
  - { title: Solar-cell mainboard and measurement-module design archive, type: project-archive, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/solarcell-mppt-pcb", file_reference: curated schematic PCB and BOM files, pages: "", used_for: circuit and PCB analysis }
  - { title: Low-cost Open-source 12-channel MPPT Data Logger for Solar Cell Research, type: paper, public_url: "https://doi.org/10.1109/PVSC43889.2021.9519025", file_reference: external reference only, pages: "", used_for: 12-channel MPPT architecture reference }
prerequisites: [electronic-circuits, adc, uart, power-electronics]
learning_objectives: [power tree, current sensing, voltage measurement, ADC DAC path, PCB handoff]
related_projects: [solarcell-mppt-pcb]
related_posts: [pads-footprint-ppg-schematic]
tags: [solar-cell, mppt, stm32f401, current-sensing, adc, dac, pads]
cover_image: /assets/images/projects/solarcell-mppt-pcb/mainboard-schematic.webp
thumbnail: /assets/images/projects/solarcell-mppt-pcb/mainboard-schematic.webp
image_alt: STM32F401 mainboard schematic with power communication and measurement-module connections
draft: false
revision_history:
  - { date: 2026-09-04, change: Separated the roles of the circuit PCB BOM and published MPPT paper }
toc:
  - { id: purpose, title: Design purpose }
  - { id: mainboard, title: Mainboard }
  - { id: measurement, title: Measurement module }
  - { id: data, title: Control and data }
  - { id: pcb, title: PCB artifacts }
  - { id: scope, title: Attribution and next tests }
---

## Design purpose {#purpose}

Comparing several solar-cell channels under the same conditions requires
per-channel current/voltage sensing, a setpoint path, shared power, and MCU
communication. I traced each function through the STM32F401 mainboard and
measurement-module files, focusing on where signals begin and which connector
carries them.

## STM32F401 mainboard {#mainboard}

The 12-V input feeds 5-V and 3.3-V rails for the MCU and peripheral circuitry.
The STM32F401 is accompanied by SWD, USB, and UART, while three connectors carry
ADC/DAC buses, power, and address signals to measurement modules. Drawing the
power tree before adding digital interfaces made power and communication faults
easier to separate.

<figure><img src="{{ '/assets/images/projects/solarcell-mppt-pcb/mainboard-schematic.webp' | relative_url }}" alt="Mainboard schematic with STM32F401, 12-V input, USB UART, and three module connectors" width="1600" height="1132"><figcaption>Mainboard view combining shared power, MCU, communication, and three module interfaces.</figcaption></figure>

## Eight-channel measurement module {#measurement}

Eight current channels enter the module and an AD7997 ADC gathers them for the
MCU. Another stored sheet contains OPA703 voltage paths and an AD5629R DAC, so
measurement and actuation follow different signal chains. I read the circuit as
input, conditioning, conversion, and communication rather than as a list of
part numbers.

<figure><img src="{{ '/assets/images/projects/solarcell-mppt-pcb/current-sensing.webp' | relative_url }}" alt="Schematic with an AD7997 and eight current-sensing channels" width="1600" height="1132"><figcaption>Measurement-module sheet where eight current channels converge at the ADC.</figcaption></figure>

## Control and data paths {#data}

The measurement direction runs from a cell channel through analog conditioning,
ADC, MCU, and USB/UART. The control direction sends an MCU setpoint through the
DAC to a channel-control path. Treating command and measurement separately makes
missing nets easier to spot when comparing connector pins and names.

```text
Measurement : Cell -> Analog path -> ADC -> MCU -> USB/UART
Control     : MCU setpoint -> DAC -> Channel control path
```

## PCB and BOM artifacts {#pcb}

I compared the PADS schematics, PCB files, and parts list to match the major ICs
and connectors. The public archive contains the STM32F401 mainboard and
measurement-module schematic/PCB files plus the BOM. Installers, vendor PDFs,
and temporary conversion products are excluded because they are not necessary
to understand the design.

## Attribution and next tests {#scope}

The 12-channel MPPT concept references the 2021 IEEE PVSC paper by Kelzenberg,
Loke, and Atwater. The paper and original-author Gerbers are linked rather than
republished. Design files alone cannot establish accuracy, efficiency,
temperature drift, or production yield. Before fabrication, current datasheets,
reference voltage, and channel protection need a fresh review; calibration and
load sweeps follow after assembly.
