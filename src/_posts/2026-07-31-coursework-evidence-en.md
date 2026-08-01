---
title: Separating Archive, Rerun, Redraw, and Proposal in coursework records
title_en: Separating Archive, Rerun, Redraw, and Proposal in coursework records
description: A provenance rule for Vivado, GHDL, PSIM, Python, Cadence, PowerWorld, and AESA-SAR coursework evidence.
date: 2026-07-31 01:01:00 +0900
updated: 2026-08-01 18:01:00 +0900
study_date: 2026-07-31
lang: en
translation_key: coursework-evidence-levels
permalink: /en/blog/2026/07/31/coursework-evidence-levels/
alternate_url: /blog/2026/07/31/coursework-evidence-levels/
alternate_lang: ko
primary_category: portfolio-methodology
subcategory: source-provenance
series: engineering-record-provenance
series_order: 1
post_type: methodology
difficulty: beginner
study_status: published
evidence_status: SOURCE_DERIVED
tools: [Vivado, GHDL, PSIM, Python, Cadence Virtuoso, PowerWorld]
hardware: []
software_versions: [GHDL version recorded in coursework repository]
source_materials:
  - title: Electrical Engineering Coursework Portfolio
    type: public-project
    public_url: https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/
    file_reference: public repository only
    pages: ""
    used_for: comparing coursework evidence states
  - title: Coursework project page
    type: portfolio-page
    public_url: /en/projects/coursework/
    file_reference: site data
    pages: ""
    used_for: publication boundaries and project link
prerequisites: [source provenance, reproducibility]
learning_objectives: [separate archives from reruns, separate redraws from measurements, record proposal boundaries]
related_projects: [coursework]
related_posts: [evidence-status]
tags: [source-provenance, ghdl, cadence, powerworld]
cover_image: /assets/images/projects/coursework-hero.webp
thumbnail: /assets/images/projects/coursework-hero.webp
image_alt: Coursework map connecting VHDL, power, control, RF, and sensor work to evidence states
draft: false
revision_history:
  - { date: 2026-07-31, change: Initial publication }
  - { date: 2026-08-01, change: "Added case table, publication workflow, and source-backed visual" }
toc:
  - { id: why, title: Why this distinction exists }
  - { id: definitions, title: Four provenance states }
  - { id: cases, title: Coursework cases }
  - { id: workflow, title: Publication workflow }
  - { id: template, title: Record template }
  - { id: limits, title: Unverified items }
---

## Why this distinction exists {#why}

A coursework archive mixes artifacts created at different times and in different environments. A Vivado waveform may survive only as a historical screen, while VHDL source can be rerun with GHDL. A Cadence result may be an archived simulation, and a Python calculation may only check equations copied from a report. None of those is automatically a hardware measurement.

Treating every surviving file as “experiment completed” hides the point at which reproduction can begin. I first record how the artifact was created, then describe fresh execution and physical measurement with their own commands, logs, and conditions.

<figure><picture><source srcset="/assets/images/projects/coursework-hero.webp" type="image/webp"><img src="/assets/images/projects/coursework-hero.jpg" alt="Coursework map linking VHDL, power, control, RF, and sensor systems to evidence states" width="1200" height="570" loading="lazy"></picture><figcaption>Engineering domain and artifact provenance answer different questions and are not collapsed into one badge.</figcaption></figure>

## Four provenance states {#definitions}

| State | Required basis | Supported claim | Unsupported claim |
|---|---|---|---|
| Existing Archive | historical file or screen plus context | the result existed in the earlier environment | current reproduction passed |
| Rerun | command, tool version, fresh log | the stated execution was repeated | unrun synthesis or measurement |
| Portfolio Redraw | source values and redraw rule | a new explanatory diagram | a new measured result |
| Proposal | problem, requirements, design intent | a pre-implementation design | implementation or field performance |

These states are not a quality ranking. They tell the reader what can be inspected or reproduced.

## Coursework cases {#cases}

- An archived **Vivado waveform** remains Existing Archive until the design is rerun in a stated Vivado environment.
- A **GHDL rerun** supports only the tests represented by its fresh command and log. It does not retroactively verify the Vivado screen.
- Preserved **PSIM** files and screens remain an archive when no current execution log exists.
- An independent **Python recalculation** checks equations and inputs; it does not replace a hardware measurement.
- Historical **Cadence S-parameters** for Wilkinson and branch-line circuits are labeled Existing Cadence Archive, not a new simulation or VNA measurement.
- A **PowerWorld non-convergence** record is troubleshooting evidence when its conditions are preserved. It is not relabeled as a converged power-flow result.
- The **AESA-SAR concept** remains a Proposal. It is not an implemented system specification or operational result.

## Publication workflow {#workflow}

1. Check ownership, privacy, license terms, and whether course material may be disclosed.
2. Record tool and creation context for a surviving archive.
3. For a rerun, bind command, version, input, and fresh log.
4. Mark explanatory diagrams as redraws and retain their source values.
5. Stop at Proposal when implementation evidence is absent.
6. Evaluate source, execution, and measurement status separately.

Private originals stay outside the repository. A public summary describes the boundary without making a direct asset URL a bypass.

## Record template {#template}

```text
Item:
Domain:
Provenance: Existing Archive | Rerun | Portfolio Redraw | Proposal
Source owner:
Tool and version:
Input:
Command or procedure:
Observed result:
Not verified:
Public asset:
Related project:
```

The `Not verified` field prevents a functional simulation from silently becoming a timing, power, Fmax, or hardware claim.

## Unverified items {#limits}

The public evidence does not show that every Cadence, PSIM, or PowerWorld exercise was rerun on a current version. It also does not support new VNA measurements, production-grid validation, or an implemented AESA-SAR system. New evidence will be added as a separate execution bundle instead of rewriting the original archive.

[Open the coursework project](/en/projects/coursework/)
