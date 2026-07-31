---
title: Criteria for SOURCE, EXECUTED, MEASURED, and BLOCKED project results
title_en: Criteria for SOURCE, EXECUTED, MEASURED, and BLOCKED project results
description: A status model that separates source presence, software execution, hardware measurement, and blocked verification from artifact provenance.
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
  - { title: Public engineering project pages, type: portfolio-data, public_url: /en/projects/, file_reference: site data, pages: "", used_for: status examples }
  - { title: Security and verification policy, type: policy, public_url: /en/security/, file_reference: public page, pages: "", used_for: blocked and platform-limit language }
prerequisites: [source provenance]
learning_objectives: [separate source from execution, separate simulation from measurement, retain blocked states]
related_projects: [fpga-delay-logic, fmcw-radar, drowsiness-monitor, ppg-hrv]
related_posts: [coursework-evidence-levels]
tags: [evidence-status, reproducibility, systemverilog, fmcw-radar]
cover_image: /assets/images/projects/fpga-architecture.webp
thumbnail: /assets/images/projects/fpga-architecture.webp
image_alt: Three FPGA delay-logic architectures connected to an independent verification flow
draft: false
revision_history:
  - { date: 2026-07-31, change: Initial publication }
  - { date: 2026-08-01, change: Separated status from provenance and added project-level decisions }
toc:
  - { id: two-axes, title: Provenance and status are separate axes }
  - { id: criteria, title: Criteria for four states }
  - { id: examples, title: Project examples }
  - { id: badges, title: Badge rules }
  - { id: limits, title: Remaining limits }
---

## Provenance and status are separate axes {#two-axes}

Archive, Rerun, Redraw, and Proposal describe where an artifact came from. SOURCE, EXECUTED, MEASURED, and BLOCKED describe how far a specific claim was verified. A historical Cadence screen can be `Existing Archive + SOURCE AVAILABLE`; a fresh Icarus regression log can be `Rerun + EXECUTED`.

Keeping the axes separate prevents two common jumps: source code does not prove execution, and a prototype photograph does not prove measured performance.

## Criteria for four states {#criteria}

| Status | Minimum evidence | Decision question |
|---|---|---|
| SOURCE AVAILABLE | public source, documentation, and input description | What can be inspected or reproduced? |
| EXECUTED | environment, command or procedure, and observed output | Was it run under the stated conditions? |
| MEASURED | instrument, conditions, units, result, and raw-data boundary | Was a physical quantity or performance metric measured? |
| BLOCKED | missing tool, source, permission, or reference plus reason | Why must verification stop? |

BLOCKED is not a disguised PASS. Missing Quartus reports leave timing, power, Fmax, and numerical PPA blocked. A control unavailable on GitHub Pages is recorded as a platform limitation.

## Project examples {#examples}

### FPGA Delay Logic

Public RTL and testbenches are present. Icarus regressions executed 20 Project 1 checks, 26 Project 2 equivalence checks, and three Project 3 scenarios. Functional simulation is therefore EXECUTED. Quartus synthesis, timing, power, Fmax, and numerical PPA remain BLOCKED because no reports are available.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="FPGA delay logic progressing from shift register to circular queue and memory-based driver checker" width="1200" height="517" loading="lazy"></picture><figcaption>The diagram explains the structures; the execution status comes from separate regression logs.</figcaption></figure>

### FMCW Radar Cardiac Timing

Analysis source, acquisition firmware, configuration documents, and privacy-reviewed hardware photographs support SOURCE + HARDWARE. Paper-reported evidence covers 600 seconds of concurrent acquisition and 848 corresponding beats. Radar-derived AO/AC values remain morphology-based candidate timings, not direct valve measurements or clinical performance.

### Two-node Drowsiness Monitor

C/C++ source, TCP/IP/file-IPC/GPIO/I2C paths, and physical prototype photographs support the integration claim. No public evidence quantifies latency, sensitivity, specificity, or false-alarm rate.

### PPG-HRV Cognitive Load

The paper abstract reports AUC 0.85 and F1 0.82. Those values are `PAPER_REPORTED` and are not merged with a separate fold-result archive or described as a current retraining result.

## Badge rules {#badges}

- Do not let one strongest state cover an entire project.
- Track functional simulation, synthesis, and hardware measurement separately.
- Label paper metrics as `PAPER_REPORTED`.
- Pair BLOCKED with the missing tool, report, or reference.
- Use PASS only for an actual test or execution result.

## Remaining limits {#limits}

This model makes public evidence readable; it does not guarantee permanent reproducibility. External repositories, hardware, or licensed tools may become unavailable. Status updates retain earlier evidence and add a date and verification method rather than erasing history.
