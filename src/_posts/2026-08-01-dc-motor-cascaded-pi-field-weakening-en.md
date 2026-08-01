---
title: Cascaded PI Control and Field Weakening for a DC Motor in PSIM
title_ko: PSIM에서 DC Motor 이중 PI 제어와 Field Weakening 정리
description: My study note on the H-bridge, nested current and speed loops, and switching-frequency comparison in an archived motor-control report.
date: 2026-08-01 15:20:00 +0900
updated: 2026-08-01 15:20:00 +0900
study_date: 2025-11-01
lang: en
translation_key: dc-motor-cascaded-pi-field-weakening
permalink: /en/blog/2026/08/01/dc-motor-cascaded-pi-field-weakening/
alternate_url: /blog/2026/08/01/dc-motor-cascaded-pi-field-weakening/
alternate_lang: ko
primary_category: major-foundations
subcategory: motor-control
series: dc-motor-control
series_order: 1
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_ARCHIVED_SIMULATION_REPORT
tools: [PSIM, MATLAB, PI Control]
hardware: []
software_versions: []
source_materials:
  - { title: Motor-control coursework report, type: private-coursework-report, file_reference: archived report, pages: "1-13", used_for: "motor parameters, controller settings, and saved simulation comparison" }
  - { title: Altair PSIM Motor Control Design Suite Tutorial, type: official-documentation, public_url: https://2023.help.altair.com/psim-tut/tutorials/Tutorial%20-%20Motor%20Control%20Design%20Suite.pdf, used_for: cascaded control and field-weakening context }
prerequisites: [dc-motor-model, pi-control, pwm]
learning_objectives: [read the cascaded loops, interpret the PI settings, compare the saved torque-ripple results]
related_projects: [coursework]
related_posts: []
tags: [dc-motor, psim, pi-control, h-bridge, field-weakening]
cover_image: /assets/images/coursework/dc-motor-cascaded-control.svg
thumbnail: /assets/images/coursework/dc-motor-cascaded-control.svg
image_alt: Cascaded speed and current PI controllers driving an H-bridge and DC motor
draft: false
revision_history:
  - { date: 2026-08-01, change: Reorganized the saved simulation settings and results from the coursework report }
toc:
  - { id: plant, title: Start with the motor and H-bridge }
  - { id: loops, title: Why I separated two loops }
  - { id: gains, title: Reading the saved PI settings }
  - { id: weakening, title: Saturation and field weakening }
  - { id: ripple, title: Switching-frequency comparison }
  - { id: limits, title: Scope of this note }
---

## Start with the motor and H-bridge {#plant}

I first reread the DC motor as coupled electrical and mechanical systems. The armature resistance and inductance sit with back EMF on the electrical side, while inertia, friction, and load torque form the mechanical side. The H-bridge supplies positive or negative average voltage to this plant. I start with a fixed-field operating point, where `K_e` and `K_t` can be treated as constants.

<p class="study-equation"><code>vₐ = Rₐiₐ + Lₐ(diₐ/dt) + Kₑω</code><br><code>J(dω/dt) = Kₜiₐ − Bω − Tₗ</code></p>

Current creates torque, and speed feeds back through back EMF. This coupling explains why I should regulate current before asking the slower speed loop to command the plant.

## Why I separated two loops {#loops}

The outer speed PI turns speed error into a current reference. The inner current PI tracks that reference and produces a voltage or duty command. With a faster current loop, the speed loop can treat the inner path approximately as a responsive torque source.

<figure><img src="{{ '/assets/images/coursework/dc-motor-cascaded-control.svg' | relative_url }}" alt="Cascaded speed PI, current limiter, current PI, H-bridge, and DC motor" width="1200" height="630"><figcaption>I redrew the block flow from the coursework report. The numbers are saved report settings, not fresh measurements.</figcaption></figure>

I initially mixed up the two error signals. Writing units beside each block made the roles clear: the speed controller outputs current, while the current controller outputs voltage or duty.

## Reading the saved PI settings {#gains}

The archived report records `Kp = 24.8`, `Ki ≈ 3898` for the speed PI and `Kp = 62.832`, `Ki = 314.16` for the current PI. I treat these as settings tied to that motor model and target bandwidth, not universal optimal gains.

```text
1. Check every motor parameter and unit.
2. Close and test the current loop first.
3. Confirm the current limiter.
4. Close the speed loop afterward.
5. Record saturation and anti-windup behavior.
```

## Saturation and field weakening {#weakening}

Back EMF grows with speed. Eventually the DC bus cannot provide more voltage to maintain the requested current. In the separately excited DC motor used by the assignment, field weakening increases resistance in the field-current path, reducing field current and flux `Φ`.

<p class="study-equation"><code>Kₑ = kₑΦ, Kₜ = kₜΦ</code></p>

Reducing flux lowers back EMF at a given speed and leaves room to run faster, but armature current must rise to preserve the same torque. The constant-`K_e`, constant-`K_t` model from the first section therefore does not apply unchanged in this region. I use Altair's PSIM material only as general context for nested loops and operation above base speed; the archived assignment report is the source for this DC field-circuit implementation.

## Switching-frequency comparison {#ripple}

The report records 2.28 N·m of torque ripple at 10 kHz and 0.38 N·m at 30 kHz. These are saved PSIM simulation values, not measurements from a physical shaft.

<figure><img src="{{ '/assets/images/coursework/dc-motor-switching-ripple.svg' | relative_url }}" alt="Saved torque-ripple comparison of 2.28 newton metres at 10 kilohertz and 0.38 newton metres at 30 kilohertz" width="1200" height="630"><figcaption>I placed the two archived values on one scale. The comparison supports lower simulated ripple, not a claim about loss, temperature, or EMI.</figcaption></figure>

A higher switching frequency can reduce the current change per switching period, but it can also increase switching loss, EMI, and computation demand. I therefore keep this as a one-metric simulation comparison.

## Scope of this note {#limits}

I have reread the archived model, gains, and plots and redrawn the control structure. I have not rerun the original PSIM circuit in a current environment or connected a physical motor. My next step is to rerun the inner-loop step response first and compare saturation with and without anti-windup under identical conditions.
