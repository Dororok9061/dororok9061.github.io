---
title: Isolating a DCA1000EVM Raw-ADC Capture Failure by Data Path
title_en: Isolating a DCA1000EVM Raw-ADC Capture Failure by Data Path
description: A troubleshooting case that separates power, control, LVDS, FPGA/buffer, and Ethernet paths when IWR6843 raw ADC capture failed and the board also heated up.
date: 2026-09-09 12:00:00 +0900
updated: 2026-09-09 12:00:00 +0900
lang: en
translation_key: dca1000evm-troubleshooting-data-path
permalink: /en/blog/2026/09/09/dca1000evm-troubleshooting-data-path/
alternate_url: /blog/2026/09/09/dca1000evm-troubleshooting-data-path/
alternate_lang: ko
primary_category: rf-radar-signal
subcategory: radar-signal-processing
series: fmcw-radar-signal-processing
series_order: 7
post_type: troubleshooting
practical: true
difficulty: advanced
study_status: published
evidence_status: HARDWARE_AND_DIAGNOSTIC_RECORDS
tools: [IWR6843ISK, DCA1000EVM, mmWave Studio, Wireshark, Oscilloscope]
hardware: [IWR6843ISK, DCA1000EVM]
software_versions: [mmWave Studio 2.1.0.0]
source_materials:
  - { title: DCA1000EVM troubleshooting archive, type: project-archive, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/mmwave-visualizer", file_reference: user-provided hardware photos and runtime captures, pages: "portfolio pp. 15-16", used_for: "observed symptoms, inspection sequence, and unresolved result" }
  - { title: DCA1000EVM Data Capture Card User's Guide Rev. A, type: vendor-documentation, public_url: "https://www.ti.com/lit/ug/spruij4a/spruij4a.pdf", file_reference: SPRUIJ4A, pages: "3, 16-21", used_for: "LVDS, FPGA, DDR3L, Ethernet, switch, and raw-mode architecture" }
  - { title: Texas Instruments DCA1000EVM product page, type: vendor-documentation, public_url: "https://www.ti.com/tool/DCA1000EVM", file_reference: product overview, pages: "", used_for: real-time LVDS capture and 1-Gbps Ethernet streaming role }
prerequisites: [fmcw-radar, lvds, ethernet, embedded-debugging]
learning_objectives: [signal-path isolation, control-path isolation, power and thermal checks, exit criteria]
related_projects: [mmwave-visualizer]
related_posts: [mmwave-visualizer-people-tracking]
tags: [dca1000evm, iwr6843, mmwave, raw-adc, lvds, ethernet, hardware-debugging]
cover_image: /assets/images/projects/mmwave-visualizer/dca1000-setup.webp
thumbnail: /assets/images/projects/mmwave-visualizer/dca1000-setup.webp
image_alt: DCA1000EVM and IWR6843ISK hardware setup used to inspect the raw-ADC capture path
draft: false
revision_history:
  - { date: 2026-09-09, change: "Written from hardware photos, mmWave Studio status screens, and portfolio pages 15-16" }
toc:
  - { id: symptom, title: Missing data and board heating }
  - { id: paths, title: Data and control paths }
  - { id: observations, title: GUI and LED states }
  - { id: inspection, title: Hardware inspection }
  - { id: result, title: Stop decision and open scope }
  - { id: competency, title: Debugging competency }
---

## Missing raw data and board heating {#symptom}

I connected a DCA1000EVM to collect raw ADC samples from the IWR6843, but the
Ethernet capture did not start and the board also heated up. Changing code first
would have mixed configuration faults with physical faults. I preserved the
observed hardware state, then traced the sample path separately from the path
that brings the devices into capture mode.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/dca1000-setup.webp' | relative_url }}" alt="IWR6843ISK mounted on a DCA1000EVM with power, USB, and board-to-board connections" width="1200" height="1200"><figcaption>The IWR6843ISK, DCA1000EVM, power, USB, and inter-board connections in one view.</figcaption></figure>

## Separating the data path from the control path {#paths}

Using TI's raw-mode architecture, I mapped the sample path as `IWR6843 ADC →
LVDS → DCA1000 FPGA → DDR3L/packet path → Ethernet → PC`. A different sequence
selects power and operating mode, establishes FTDI, RS232, and SPI connectivity,
resets and configures the devices, and starts capture. Splitting one symptom into
these two paths produced concrete observation points.

<figure><img src="{{ '/assets/images/study/mmwave/evm-dca1000-flow.svg' | relative_url }}" alt="Control UART and raw LVDS paths from a radar EVM through DCA1000 to a host PC" width="1200" height="675"><figcaption>Control traffic and raw LVDS-to-Ethernet samples do not fail at the same boundary.</figcaption></figure>

```text
Data path   : IWR6843 raw ADC -> LVDS -> FPGA/buffer -> Ethernet -> PC
Control path: power/mode -> FTDI/RS232/SPI -> reset/config -> capture start
```

## Using GUI and LEDs as observation points {#observations}

In mmWave Studio, FTDI appeared as `Connected`, yet the detected-device count
was zero and both RS232 and SPI appeared as `Disconnected`. RF Power-up also
produced `ReadRegister failed with error -11`. PC-side FTDI enumeration was
therefore not equivalent to a working radar-control path.

```text
Error        : no raw ADC stream, device count 0, ReadRegister -11
Cause scope  : mode/configuration, interconnect, power, LVDS/FPGA/buffer, Ethernet
Verification : GUI state, LED labels, connector/solder inspection, oscilloscope probes
```

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/mmwave-studio-readregister-error.webp' | relative_url }}" alt="mmWave Studio showing FTDI connected, RS232 and SPI disconnected, and ReadRegister error -11" width="1200" height="509"><figcaption>The sequence stopped after FTDI enumeration and before RS232, SPI, and device detection became operational.</figcaption></figure>

Several status LEDs were illuminated simultaneously in a hardware photograph.
I used their labels to choose the next measurement points, but did not infer a
failed FPGA, DDR device, or LVDS interface from a single LED state. Board heating
also lacked a measured location and temperature, so it was treated as a symptom
rather than proof of a particular failed component.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/dca1000-error-leds.webp' | relative_url }}" alt="DCA1000EVM status LEDs near the power, FPGA, DDR, and LVDS labels during inspection" width="1200" height="1200"><figcaption>An enlarged view of LED labels and switch positions used to plan the next checks.</figcaption></figure>

## Narrowing the hardware path {#inspection}

- I checked the 5-V input, board power state, and when heating appeared.
- I revisited DIP-switch positions, operating mode, reset, configuration, and
  capture-start order.
- I inspected board-to-board connectors, cable contact, and solder joints, then
  reworked suspicious joints.
- I probed accessible power and signal points with an oscilloscope.
- I compared PC-side Ethernet and capture settings independently of the physical
  checks.

The purpose was to verify whether each stage produced the condition required by
the next stage before replacing components or making broad software changes.

## Recording the stop decision and open scope {#result}

Ethernet raw-ADC streaming was not restored after solder rework and repeated
configuration. I could not establish whether the FPGA buffer was receiving valid
samples or identify a failed component. I stopped using this capture path and
retained the observed error states, probe locations, and unanswered boundaries
for a future board-level investigation.

The raw-ADC capture failure is separate from the TI SDK-based 3D People Tracking
run. The latter received processed point-cloud and target data over dual UART;
it is not evidence that the DCA1000 LVDS-to-Ethernet path recovered.

## Debugging competency carried forward {#competency}

The central lesson was not to assign a physical cause to a missing-data symptom
too early. I turned power and heat, mode transitions, connectors and solder,
LVDS and buffering, and Ethernet into staged observation points. I also kept
confirmed states, plausible causes, and unmeasured areas distinct through the
stop decision. The same approach applies to radar and autonomous-sensor
validation, embedded-hardware bring-up, production failure analysis, and
advanced-quality investigations.
