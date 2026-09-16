---
title: How I keep design files, reruns, and physical measurements separate
title_en: How I keep design files, reruns, and physical measurements separate
description: A practical way to connect surviving files, fresh logs, and physical measurements to project explanations.
date: 2026-07-31 00:11:00 +0900
updated: 2026-09-17 12:00:00 +0900
study_date: 2026-07-31
lang: en
translation_key: evidence-status
permalink: /en/blog/2026/07/31/evidence-status/
alternate_url: /blog/2026/07/31/evidence-status/
alternate_lang: ko
primary_category: portfolio-methodology
subcategory: evidence-status
series: engineering-record-lineage
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

Source, screenshots, reports, and run logs are classified by creation date and tool environment. Run bundles retain commands, inputs, and output logs.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="Shift register, circular queue, and memory-based driver-checker structures" width="1200" height="517" loading="lazy"></picture><figcaption>The diagram explains architecture; regression logs establish the behavior I actually ran.</figcaption></figure>

## Three kinds of material {#three}

Three record types: design files and historical screens for architecture; fresh runs with tool versions, commands, inputs, and outputs; physical measurements with instrument settings, units, and raw data.

## Project examples {#examples}

### FPGA Delay Logic

July Icarus record: Project 1, 20 checks; Project 2, 26 equivalence checks; Project 3, three scenarios. Evaluation type: functional simulation.

[September GTKWave, RTL, and testbench records](/en/projects/fpga-delay-logic/#gallery)

### FMCW Radar

Artifacts: analysis source, acquisition firmware, configuration files, and hardware photographs. Paper results: 600 seconds, 848 corresponding beats, and morphology-based AO/AC candidate timing.

### PPG-HRV

Paper abstract/conclusion: AUC 0.99 and F1 0.992. Separate fold CSVs retain the evaluation conditions of their respective code runs.

## How I report numbers {#writing}

Each result links to its run log, paper, or measurement data. Follow-up synthesis and hardware tests specify the reports and conditions required.

## What still needs checking {#limits}

Run history uses date-stamped logs, tool environments, and inputs. New execution records are added alongside the original archive.