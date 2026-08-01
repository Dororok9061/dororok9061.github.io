---
title: How I keep design files, reruns, and physical measurements separate
title_en: How I keep design files, reruns, and physical measurements separate
description: A practical way to connect surviving files, fresh logs, and physical measurements to project explanations.
date: 2026-07-31 00:11:00 +0900
updated: 2026-08-01 18:11:00 +0900
study_date: 2026-07-31
lang: en
translation_key: evidence-status
permalink: /en/blog/2026/07/31/evidence-status/
alternate_url: /blog/2026/07/31/evidence-status/
alternate_lang: ko
primary_category: portfolio-methodology
subcategory: evidence-status
series: engineering-record-provenance
series_order: 2
post_type: methodology
difficulty: beginner
study_status: published
evidence_status: SOURCE_AVAILABLE
tools: [GitHub, Icarus Verilog, GHDL, Quartus, Jekyll]
hardware: [BGT60TR13C, STM32F411, Raspberry Pi]
software_versions: []
source_materials:
  - { title: Public engineering project pages, type: portfolio-data, public_url: /en/projects/, file_reference: site data, pages: "", used_for: project examples }
  - { title: Security and verification policy, type: policy, public_url: /en/security/, file_reference: public page, pages: "", used_for: platform limits }
prerequisites: [source provenance]
learning_objectives: [separate source from execution, separate simulation from measurement, leave unmeasured values unset]
related_projects: [fpga-delay-logic, fmcw-radar, drowsiness-monitor, ppg-hrv]
related_posts: [coursework-evidence-levels]
tags: [evidence-status, reproducibility, systemverilog, fmcw-radar]
cover_image: /assets/images/projects/fpga-architecture.webp
thumbnail: /assets/images/projects/fpga-architecture.webp
image_alt: Three FPGA delay-logic architectures connected to an independent checking flow
draft: false
published: false
revision_history:
  - { date: 2026-07-31, change: Initial publication }
  - { date: 2026-08-01, change: Rewrote the note around practical documentation instead of status codes }
toc:
  - { id: start, title: What I do after finding a file }
  - { id: three, title: Three kinds of material }
  - { id: examples, title: Project examples }
  - { id: writing, title: How I report numbers }
  - { id: limits, title: What still needs checking }
---

## What I do after finding a file {#start}

Old coursework folders mix source, screenshots, reports, and fresh logs. I do not call a project rerun merely because a file exists. I record when and how it was created, then bind any current execution to its command and new log.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="Shift register, circular queue, and memory-based driver-checker structures" width="1200" height="517" loading="lazy"></picture><figcaption>The diagram explains architecture; regression logs establish the behavior I actually ran.</figcaption></figure>

## Three kinds of material {#three}

Design files and historical screens explain what existed. Fresh runs need a tool version, command, input, and output. Physical measurements need an instrument, settings, units, and raw-data context. A simulation number does not become a measurement simply because a prototype photograph also exists.

## Project examples {#examples}

### FPGA Delay Logic

I ran the public SystemVerilog testbenches with Icarus: 20 checks for Project 1, 26 equivalence checks for Project 2, and three file-driven scenarios for Project 3. I found no Quartus timing, power, Fmax, or resource report, so I did not publish those numbers.

### FMCW Radar

I reviewed analysis source, acquisition firmware, configuration files, and hardware photographs. The paper reports 600 seconds of concurrent acquisition and 848 corresponding beats. Radar morphology supplies candidate AO/AC timings, not direct valve measurements or clinical performance.

### PPG-HRV

The abstract reports AUC 0.85 and F1 0.82. I keep those as paper-reported values rather than merging them with a separate fold archive or calling them a current retraining result.

## How I report numbers {#writing}

Every number gets a short source statement. Simulation checks, paper metrics, and physical measurements live in separate sentences or tables. When synthesis or hardware testing was not run, I leave the number unset and note the report and conditions needed for the next run.

## What still needs checking {#limits}

Repositories, licensed tools, and hardware may later become unavailable. I therefore keep older material and add date-stamped logs and environment details for new work. This does not promise permanent reproducibility, but it preserves the line between what I inspected and what I executed.
