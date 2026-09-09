---
title: Isolating a DCA1000EVM Raw-ADC Capture Failure by Data Path
title_en: Isolating a DCA1000EVM Raw-ADC Capture Failure by Data Path
description: A DCA1000EVM troubleshooting case that separates visible control UDP from a zero-packet raw capture using Wireshark, UniFlash, Tera Term, and hardware checks.
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
tools: [IWR6843ISK, DCA1000EVM, mmWave Studio, Wireshark, UniFlash, Tera Term, Oscilloscope]
hardware: [IWR6843ISK, DCA1000EVM]
software_versions: [mmWave Studio 2.1.0.0, UniFlash]
source_materials:
  - { title: DCA1000EVM troubleshooting archive, type: project-archive, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/mmwave-visualizer", file_reference: user-provided hardware photos and Wireshark/UniFlash/Tera Term/capture-log screens, pages: "portfolio pp. 15-16", used_for: "observed states, fault-isolation sequence, and unresolved result" }
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
  - { date: 2026-09-09, change: "Added Wireshark, UniFlash, Tera Term, and zero-packet capture screens as staged debugging evidence" }
  - { date: 2026-09-09, change: "Placed all 36 unique debugging screens, including COM-port settings, Device Manager, and the full Studio error log" }
toc:
  - { id: symptom, title: Missing data and board heating }
  - { id: paths, title: Data and control paths }
  - { id: observations, title: GUI and LED states }
  - { id: wireshark, title: Wireshark control UDP }
  - { id: uniflash, title: UniFlash programming }
  - { id: teraterm, title: Tera Term CLI }
  - { id: capture-log, title: Zero-packet record }
  - { id: inspection, title: Hardware inspection }
  - { id: result, title: Stop decision and open scope }
  - { id: competency, title: Debugging competency }
---

## Missing raw data and board heating {#symptom}

I connected a DCA1000EVM to collect raw ADC samples from the IWR6843. Wireshark
showed short control UDP datagrams between the PC and the board, but the raw
capture log counted zero received packets and the board also heated up. Changing
code first would have mixed configuration faults with physical faults. I preserved
the observed state, then traced the sample path separately from the path that
brings the devices into capture mode.

Two byte-identical duplicate files are shown once each; all 36 distinct debugging
screens are placed directly in the staged narrative below. Each screen opens at
full size when selected.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/dca1000-setup.webp' | relative_url }}" alt="IWR6843ISK mounted on a DCA1000EVM with power, USB, and board-to-board connections" width="1200" height="1200"><figcaption>The IWR6843ISK, DCA1000EVM, power, USB, and inter-board connections in one view.</figcaption></figure>

## Separating the data path from the control path {#paths}

Using TI's raw-mode architecture, I mapped the sample path as `IWR6843 ADC →
LVDS → DCA1000 FPGA → DDR3L/packet path → Ethernet → PC`. A different sequence
selects power and operating mode, establishes FTDI, RS232, and SPI connectivity,
resets and configures the devices, and starts capture. Splitting one symptom into
these two paths produced concrete observation points.

<figure><img src="{{ '/assets/images/study/mmwave/evm-dca1000-flow.svg' | relative_url }}" alt="Control UART and raw LVDS paths from a radar EVM through DCA1000 to a host PC" width="1200" height="675"><figcaption>Control traffic and raw LVDS-to-Ethernet samples do not fail at the same boundary.</figcaption></figure>

{% include dca-debug-gallery.html group="reference" %}

```text
Data path   : IWR6843 raw ADC -> LVDS -> FPGA/buffer -> Ethernet -> PC
Control path: power/mode -> FTDI/RS232/SPI -> reset/config -> capture start
```

## Using the GUI as the first observation point {#observations}

In mmWave Studio, FTDI appeared as `Connected`, yet the detected-device count
was zero and both RS232 and SPI appeared as `Disconnected`. RF Power-up also
produced `ReadRegister failed with error -11`. PC-side FTDI enumeration was
therefore not equivalent to a working radar-control path.

```text
Error        : no raw ADC stream, device count 0, ReadRegister -11
Cause scope  : mode/configuration, interconnect, power, LVDS/FPGA/buffer, Ethernet
Verification : GUI state, LED labels, connector/solder inspection, oscilloscope probes
```

{% include dca-debug-gallery.html group="studio" %}

## Separating control UDP from raw data in Wireshark {#wireshark}

I assigned `192.168.33.30` to the PC and `192.168.33.180` to the DCA1000EVM,
then inspected `udp.port == 4096 || udp.port == 4098`. The capture repeatedly
showed short 8- and 14-byte datagrams from the PC to configuration port 4096.
This proves that control datagrams left the PC NIC; it does not prove that LVDS
samples returned as Ethernet data packets.

{% include dca-debug-gallery.html group="network" %}

## Isolating firmware programming with UniFlash {#uniflash}

Using UniFlash on COM7, I erased the IWR6843 SFLASH and downloaded `META_IMAGE1`.
The console retained `Erase storage completed successfully`, `downloaded
successfully to SFLASH`, and `Program Load completed successfully`. I therefore
recorded firmware programming as a successful stage. That result does not prove
the later RF configuration, LVDS enable, DCA1000 packetization, or raw capture.

{% include dca-debug-gallery.html group="firmware" %}

## Checking the UART CLI in Tera Term {#teraterm}

Tera Term on COM7 displayed the `mmwDemo:/>` prompt, while several inputs were
followed by `is not recognized as a CLI command`. The screen therefore preserves
two separate observations: the firmware prompt was readable over the serial port,
but those inputs were not accepted as valid commands. Command spelling, line
ending, the running image, and CLI state remained candidates; the screen does not
identify one cause by itself.

{% include dca-debug-gallery.html group="cli" %}

## Using the capture log as the stop condition {#capture-log}

The record directory contained configuration and log files, but no raw `.bin`
file. The log reported `Number of received packets - 0`, first and last packet
IDs of 0, and a duration of -2 seconds. I used this direct outcome to avoid
treating Ethernet-adapter visibility or control traffic as a successful raw capture.

{% include dca-debug-gallery.html group="capture" %}

## Using LEDs and power as hardware observation points

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
- I compared the PC's static IP, UDP control traffic, and zero-packet capture log
  independently of the physical checks.

The purpose was to verify whether each stage produced the condition required by
the next stage before replacing components or making broad software changes.

## Recording the stop decision and open scope {#result}

Ethernet raw-ADC streaming was not restored after solder rework and repeated
configuration. Control UDP, successful flashing, and a UART prompt were each
observed, but I could not establish whether the FPGA buffer was receiving valid
samples or identify a failed component. I stopped using this capture path and
retained the observed error states, probe locations, and unanswered boundaries
for a future board-level investigation.

The raw-ADC capture failure is separate from the TI SDK-based 3D People Tracking
run. The latter received processed point-cloud and target data over dual UART;
it is not evidence that the DCA1000 LVDS-to-Ethernet path recovered.

## Debugging competency carried forward {#competency}

The central lesson was not to assign a physical cause to a missing-data symptom
too early. I turned flash programming, the UART CLI, UDP control, the raw packet
count, power and heat, connectors and solder, and LVDS buffering into staged
observation points. I also kept
confirmed states, plausible causes, and unmeasured areas distinct through the
stop decision. The same approach applies to radar and autonomous-sensor
validation, embedded-hardware bring-up, production failure analysis, and
advanced-quality investigations.
