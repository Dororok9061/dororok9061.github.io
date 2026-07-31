---
title: Verifying cycle-delay equivalence between shift-register and circular-queue designs
title_en: Verifying cycle-delay equivalence between shift-register and circular-queue designs
description: Comparing RTL architectures with one interface contract, an independent reference model, expected cycles, and 26 regression checks.
date: 2026-07-31 00:21:00 +0900
updated: 2026-08-01 18:21:00 +0900
study_date: 2026-07-31
lang: en
translation_key: fpga-architecture-equivalence
permalink: /en/blog/2026/07/31/fpga-architecture-equivalence/
alternate_url: /blog/2026/07/31/fpga-architecture-equivalence/
alternate_lang: ko
primary_category: fpga-rtl-dv
subcategory: reference-model
series: systemverilog-delay-dv
series_order: 5
post_type: project-log
difficulty: intermediate
study_status: verified
evidence_status: EXECUTED_FUNCTIONAL_SIMULATION
tools: [SystemVerilog, Icarus Verilog, VCD]
hardware: []
software_versions: [Icarus Verilog version recorded in public CI logs]
source_materials:
  - { title: FPGA Delay Logic Design Verification, type: public-repository, public_url: https://github.com/Tontonjeong/fpga-delay-logic-design-verification, file_reference: RTL testbench and logs, pages: "", used_for: architecture contract and regression evidence }
  - { title: FPGA project detail, type: portfolio-page, public_url: /en/projects/fpga-delay-logic/, file_reference: public project data, pages: "", used_for: result and boundary summary }
prerequisites: [systemverilog, sequential-logic, testbench]
learning_objectives: [compare architectures through an external contract, build an independent model, read a cycle-aligned checker]
related_projects: [fpga-delay-logic]
related_posts: []
tags: [systemverilog, reference-model, icarus-verilog, fpga]
cover_image: /assets/images/projects/fpga-architecture.webp
thumbnail: /assets/images/projects/fpga-architecture.webp
image_alt: FPGA delay logic progressing from a shift register to circular queue and memory-based driver checker
draft: false
revision_history:
  - { date: 2026-07-31, change: Initial publication }
  - { date: 2026-08-01, change: Added interface contract, checker procedure, waveform, and 26 equivalence results }
toc:
  - { id: problem, title: Comparison problem }
  - { id: contract, title: Shared interface contract }
  - { id: reference, title: Independent reference model }
  - { id: regression, title: 26 equivalence checks }
  - { id: waveform, title: Reading the waveform }
  - { id: blocked, title: Quartus verification still blocked }
---

## Comparison problem {#problem}

Programmable delay logic emits an accepted transaction after a configured number of cycles. A shift register is direct to read but grows with depth. A circular queue implements the same behavior with read/write pointers, introducing wrap-around, occupancy, and dynamic-delay edge cases.

The comparison target is not the internal array or pointer logic. With the same input data, input valid, reset, and delay setting, both DUTs must produce the same output data, output valid, and output cycle.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="Delay logic progressing from shift register to circular queue and memory-based driver checker" width="1200" height="517" loading="lazy"></picture><figcaption>The data structure changes while the external cycle-delay contract remains fixed.</figcaption></figure>

## Shared interface contract {#contract}

The checker can describe each accepted transaction with four fields.

```systemverilog
typedef struct packed {
  logic [DATA_W-1:0] data;
  logic              valid;
  int unsigned       accepted_cycle;
  int unsigned       expected_cycle;
} expected_txn_t;
```

On an accepted input cycle, it calculates `expected_cycle = accepted_cycle + delay`. At that cycle, output valid and data are checked together. Reset must empty the expected queue and suppress stale valid output.

For dynamic delay, the model stores the delay at acceptance. Reading the current delay later would mis-handle transactions that straddle a configuration change.

## Independent reference model {#reference}

Copying the DUT's shift-register or circular-buffer logic into the model can reproduce the same defect. This model only stores transactions and expected output cycles; it has no knowledge of DUT pointers.

The driver generates reset, consecutive valid cycles, valid gaps, delay changes, and buffer wrap. The checker compares the expected queue head with both DUT outputs. A mismatch record identifies the tag, accepted cycle, expected cycle, and observed data.

## 26 equivalence checks {#regression}

The public Project 2 regression reports **26 architecture-equivalence checks passed**. The cases include DEPTH 10 and 100 with different parameters and sequences, comparing shift-register and circular-queue outputs to the reference model.

This number is the explicit checker count, not assertion count or total simulation cycles. Project 1's 20 checks and Project 3's three file-driven scenarios are separate results.

## Reading the waveform {#waveform}

<figure><picture><source srcset="/assets/images/projects/fpga-waveform.webp" type="image/webp"><img src="/assets/images/projects/fpga-waveform.jpg" alt="Verification waveform showing input valid, delay settings, output valid, and data" width="1200" height="578" loading="lazy"></picture><figcaption>Output valid and data are matched to an expected cycle calculated at input acceptance.</figcaption></figure>

Data equality alone is insufficient. Output valid one cycle early, or stale data marked valid after reset, violates the contract. File-driven scenarios keep the input vector and delay changes stable across repeated regressions.

## Quartus verification still blocked {#blocked}

Functional simulation has execution evidence. Quartus synthesis, timing, resource utilization, power, Fmax, and numerical PPA remain BLOCKED because no reports are public. The circular queue is not claimed to use fewer registers or memory resources on a target FPGA. The next verification step is a controlled synthesis of both architectures using the same device and constraints, preserving the original reports and commands.
