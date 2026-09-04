---
title: From IWR6843 Configuration to 3D People-Tracking Output
title_en: From IWR6843 Configuration to 3D People-Tracking Output
description: A system-integration case spanning IWR6843 EVM setup, DSS processing, dual UART, and Visualizer output.
date: 2026-09-04 12:00:00 +0900
updated: 2026-09-04 12:00:00 +0900
lang: en
translation_key: mmwave-visualizer-people-tracking
permalink: /en/blog/2026/09/04/mmwave-visualizer-people-tracking/
alternate_url: /blog/2026/09/04/mmwave-visualizer-people-tracking/
alternate_lang: ko
primary_category: rf-radar-signal
subcategory: radar-signal-processing
series: fmcw-radar-signal-processing
series_order: 6
post_type: project-log
practical: true
difficulty: advanced
study_status: published
evidence_status: HARDWARE_AND_RUNTIME_SCREENS
tools: [IWR6843ISK, IWR6843AOP, TI Radar Toolbox, Code Composer Studio, SYS/BIOS, UART]
hardware: [IWR6843 EVM]
software_versions: []
source_materials:
  - { title: TI Radar Toolbox project archive and Visualizer captures, type: project-archive, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/mmwave-visualizer", file_reference: curated configuration and images, pages: "", used_for: system architecture and runtime-output review }
prerequisites: [radar-basics, range-fft, beamforming, uart]
learning_objectives: [sensor configuration, DSS MSS data path, dual UART, 3D tracking output]
related_projects: [mmwave-visualizer]
related_posts: [radar-candidate-timing]
tags: [mmwave, iwr6843, people-tracking, visualizer, uart, system-integration]
cover_image: /assets/images/projects/mmwave-visualizer/lab-setup.webp
thumbnail: /assets/images/projects/mmwave-visualizer/people-tracking.webp
image_alt: IWR6843 radar on a stand in the 3D People Tracking test environment
draft: false
revision_history:
  - { date: 2026-09-04, change: "Written by cross-checking hardware photos, runtime screens, and build artifacts" }
toc:
  - { id: setup, title: Test setup }
  - { id: processing, title: Radar processing }
  - { id: handoff, title: DSS and MSS }
  - { id: uart, title: Two UART links }
  - { id: output, title: Visualizer output }
  - { id: scope, title: Current scope }
---

## Test setup {#setup}

I mounted the IWR6843-family EVM on a stand and aligned its height and orientation
with the direction of movement. Mounting pose and the observation region affect
whether points leave the display or floor clutter dominates, so I adjusted the
physical setup while watching the GUI output.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/lab-setup.webp' | relative_url }}" alt="IWR6843 EVM on a stand beside the PC Visualizer environment" width="1200" height="1600"><figcaption>The test setup combines the IWR6843 EVM, interface board, and Visualizer.</figcaption></figure>

## Radar processing {#processing}

The retained DSS project shows range and Doppler processing followed by 2D
Capon/MVDR beamforming and dynamic/static CFAR. Those stages produce point-cloud
and target-list outputs with angle, Doppler, and SNR information. I mapped each
GUI point back to the sequence from chirps through detection instead of treating
the screen as a standalone sensor output.

## DSS-to-MSS handoff {#handoff}

The C674x DSS build and SYS/BIOS configuration handle radar processing. Results
then move through shared memory and a mailbox toward the MSS data path. The
retained package contains an MSS binary but not its matching source, so I focused
on the interface between DSS output and the serial packet consumed by the GUI.

## Two UART links {#uart}

I separated the CLI and data ports during connection. The CLI uses 115200 bps for
sensor configuration, while the data port uses 921600 bps for point-cloud and
target packets. A swapped port or mismatched baud rate can let configuration pass
while the screen stalls—or leave incoming data undecodable. This distinction
helped isolate hardware, firmware, and PC-application issues.

## Visualizer output {#output}

After changing sensor position, FOV, range, boundary, and detection thresholds,
I compared target IDs and bounding boxes over time in the 3D tracking view. I
also inspected the range profile, point cloud, and vital-sign display.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/people-tracking.webp' | relative_url }}" alt="People Tracking runtime view with a target ID and 3D bounding box" width="1080" height="1080"><figcaption>One frame from the run, with the target ID and position updated together.</figcaption></figure>

## Current scope {#scope}

The central outcome is a system-level understanding of hardware, DSP build,
communication settings, and GUI output—not a from-scratch radar algorithm. An
18.17-second run shows a tracked 3D target in motion. Vital-sign numbers are UI
function outputs only; medical performance, vehicle CAN/LIN integration, and
environmental/EMC testing remain outside this stage.
