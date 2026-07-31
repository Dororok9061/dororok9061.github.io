---
title: Sensor-to-alarm data path in a two-node Raspberry Pi drowsiness monitor
title_en: Sensor-to-alarm data path in a two-node Raspberry Pi drowsiness monitor
description: A source-backed map of the PPG node, camera/EAR node, TCP/IP, file IPC, GPIO, I2C LCD, and alarm boundaries.
date: 2026-07-31 00:41:00 +0900
updated: 2026-08-01 18:31:00 +0900
study_date: 2026-07-31
lang: en
translation_key: embedded-data-path
permalink: /en/blog/2026/07/31/embedded-data-path/
alternate_url: /blog/2026/07/31/embedded-data-path/
alternate_lang: ko
primary_category: stm32-embedded
subcategory: embedded-network
series: embedded-integration
series_order: 1
post_type: project-log
difficulty: intermediate
study_status: published
evidence_status: SOURCE_AND_PROTOTYPE
tools: [C, C++, OpenCV, TCP/IP, GPIO, I2C]
hardware: [Raspberry Pi, PPG sensor, camera, LCD, LED, buzzer]
software_versions: [not fully preserved]
source_materials:
  - { title: Sleep Monitoring and Prevention Device, type: public-repository, public_url: https://github.com/Tontonjeong/Sleep-monitoring-and-prevention-device, file_reference: C and C++ source, pages: "", used_for: module and data-path inventory }
  - { title: Drowsiness Monitor project page, type: portfolio-page, public_url: /en/projects/drowsiness-monitor/, file_reference: privacy-reviewed project evidence, pages: "", used_for: architecture and validation boundary }
prerequisites: [tcp-ip, gpio, i2c, basic image processing]
learning_objectives: [separate node roles, record packet and file-IPC boundaries, distinguish photographs from performance measurements]
related_projects: [drowsiness-monitor]
related_posts: []
tags: [embedded-systems, tcp-ip, raspberry-pi, i2c]
cover_image: /assets/images/projects/embedded-prototype.webp
thumbnail: /assets/images/projects/embedded-prototype.webp
image_alt: Drowsiness-monitoring prototype assembled from Raspberry Pi boards, an LCD, and sensor wiring
draft: false
revision_history:
  - { date: 2026-07-31, change: Initial publication }
  - { date: 2026-08-01, change: Added node roles, data path, failure boundaries, and prototype images }
toc:
  - { id: goal, title: Why use two nodes }
  - { id: nodes, title: PPG and camera nodes }
  - { id: path, title: Packet, file, GPIO, and I2C path }
  - { id: prototype, title: What the prototype proves }
  - { id: failures, title: Failures and unmeasured items }
  - { id: next, title: Next verification }
---

## Why use two nodes {#goal}

PPG acquisition and camera-based EAR processing have different timing and compute loads. Running both on one Raspberry Pi can let frame processing interfere with sensor reads and alarm timing. This prototype separates sensing and analysis, transferring state through the network and file IPC.

The split does not prove better performance. It makes each input, stored state, packet, and output boundary inspectable.

## PPG and camera nodes {#nodes}

The **PPG sensing node** reads samples and produces a physiological state. The **camera/EAR node** processes frames and calculates an eye-state signal. Public C/C++ source and architecture documentation support the existence of both paths.

The decision path combines the two states before driving alarms. A photograph cannot recover thresholds or accuracy, so module boundaries from source remain separate from wiring and assembly evidence.

<figure><picture><source srcset="/assets/images/projects/embedded-prototype.webp" type="image/webp"><img src="/assets/images/projects/embedded-prototype.jpg" alt="Drowsiness-monitoring prototype assembled with two Raspberry Pi boards, an LCD, and sensor wiring" width="984" height="560" loading="lazy"></picture><figcaption>The assembly and interfaces are visible; latency and detection accuracy are not measured by this photograph.</figcaption></figure>

## Packet, file, GPIO, and I2C path {#path}

```text
PPG sensor → sensing process → TCP/IP or shared file state
camera → frame processing → EAR state
PPG state + EAR state → decision path
decision → GPIO LED/buzzer + I2C LCD
```

A reproducible TCP/IP boundary needs message length, reconnect policy, and sender/receiver roles. File IPC needs protection against a consumer reading a partially written file, such as an atomic rename or explicit ready flag. GPIO needs active-level documentation; I2C needs the LCD address and error handling.

Public evidence confirms the named paths but does not preserve every packet schema and timeout. Packet-loss recovery and stale-file cleanup are therefore not claimed as verified behavior.

## What the prototype proves {#prototype}

<figure><picture><source srcset="/assets/images/projects/drowsiness-contact-sheet.webp" type="image/webp"><img src="/assets/images/projects/drowsiness-contact-sheet.jpg" alt="Contact sheet showing Raspberry Pi hardware, LCD, sensor wiring, and public source views" width="780" height="1100" loading="lazy"></picture><figcaption>Public source and physical-prototype evidence shown together.</figcaption></figure>

The photographs confirm Raspberry Pi hardware, LCD, sensor wiring, and assembly. The repository contains PPG-server and image/EAR-processing modules. `SOURCE + PROTOTYPE` is supported. Values visible on a screen are not used as a calibration record or performance table.

## Failures and unmeasured items {#failures}

A two-node design must handle missing frames, dropped TCP connections, stale file state, failed I2C writes, and sensor timeouts. The public material does not verify every retry and fallback path.

End-to-end latency, sensitivity, specificity, false-alarm rate, and long-duration stability are also not reported. Their state is `NOT REPORTED`, not MEASURED.

## Next verification {#next}

The next useful step is a fixed message schema with monotonic timestamps and a shared event ID in both node logs. Fault injection should disconnect the network and stop camera input to confirm that the alarm path moves to a safe state. Until then, prototype existence and performance claims remain separate.
