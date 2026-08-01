---
title: Reading an SOIC Footprint and a PPG Schematic as Separate PADS Examples
title_en: Reading an SOIC Footprint and a PPG Schematic as Separate PADS Examples
description: My notes on a six-pin SOIC decal and an OPA2333, filter, logic, and layout capture as two separate PADS examples.
date: 2026-08-01 11:03:00 +0900
updated: 2026-08-01 11:03:00 +0900
study_date: 2026-02-12
lang: en
translation_key: pads-footprint-ppg-schematic
permalink: /en/blog/2026/08/01/pads-footprint-ppg-schematic/
alternate_url: /blog/2026/08/01/pads-footprint-ppg-schematic/
alternate_lang: ko
primary_category: pcb-pads
subcategory: decal-footprint
series: pads-pcb-design
series_order: 3
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: ARCHIVED_DESIGN_SCREENSHOTS
tools: [PADS Logic, PADS Layout]
hardware: []
software_versions: []
source_materials:
  - { title: PADS footprint and PPG design screenshots, type: local-coursework, public_url: "", file_reference: 2026 PADS screenshots, pages: "", used_for: two separate examples of decal dimensions and schematic-to-layout flow }
prerequisites: [electronic-circuits, pcb-basics]
learning_objectives: [decal dimensions, pin numbering, schematic and layout connectivity, distinguish unrelated captures]
related_projects: [ppg-hrv]
related_posts: [biomedical-metric-provenance]
tags: [pads, pcb-footprint, ppg, opa2333]
cover_image: /assets/images/learning/coursework/pads-footprint-ppg-schematic.svg
thumbnail: /assets/images/learning/coursework/pads-footprint-ppg-schematic.svg
image_alt: A six-pin SOIC decal and a PPG schematic-to-layout view shown as unrelated examples
draft: false
revision_history:
  - { date: 2026-08-01, change: Written from stored Decal Wizard and PPG design screens }
toc:
  - { id: start, title: Why I kept the screens separate }
  - { id: footprint, title: Six-pin SOIC dimensions }
  - { id: numbering, title: Pin numbering and direction }
  - { id: schematic, title: PPG signal chain }
  - { id: layout, title: What the layout screen shows }
  - { id: next, title: My next check }
  - { id: navigation, title: Previous and next }
---

## Why I kept the screens separate {#start}

I reopened a Decal Wizard capture and a separate PPG schematic/layout capture from the same study folder. Nothing in the saved material proves that the six-pin SOIC decal was used in the PPG design. I therefore placed them beside each other as two PADS exercises instead of inventing a shared part flow.

<figure>
  <img src="{{ '/assets/images/learning/coursework/pads-footprint-ppg-schematic.svg' | relative_url }}" alt="An independent six-pad SOIC decal example beside a separate OPA2333, filter, SN74LVC logic, and layout example" width="1200" height="630">
  <figcaption>The panels come from separate saved captures. Their placement does not imply that they share one package.</figcaption>
</figure>

## Six-pin SOIC dimensions {#footprint}

The Decal Wizard screen uses six SMD pins with pad width 0.6 mm and length 1.05 mm. Pin pitch is 1.27 mm along a row, while the distance between row centers is 2.65 mm. I initially mixed up lead span and row pitch, so I mapped each number back to a line on the package drawing.

<figure>
  <table>
    <thead><tr><th>Item</th><th>Entered value</th><th>Reference</th></tr></thead>
    <tbody>
      <tr><td>Pin count</td><td>6</td><td>three on each side</td></tr>
      <tr><td>Pad width</td><td>0.6 mm</td><td>short pad dimension</td></tr>
      <tr><td>Pad length</td><td>1.05 mm</td><td>outward from body</td></tr>
      <tr><td>Pin pitch</td><td>1.27 mm</td><td>spacing within one row</td></tr>
      <tr><td>Row pitch</td><td>2.65 mm</td><td>distance between row centers</td></tr>
    </tbody>
  </table>
  <figcaption>Pairing each number with its geometric reference made the wizard inputs less ambiguous.</figcaption>
</figure>

## Pin numbering and direction {#numbering}

The stored screen uses counter-clockwise numbering and a visible pin-1 mark. After building a footprint, I need to compare that numbering with the schematic symbol before checking anything else. A correct outline with the wrong pin map would still produce the wrong netlist.

## PPG signal chain {#schematic}

The separate PPG schematic screen shows OPA2333 amplification stages, RC filtering, and an SN74LVC-family logic stage. The signal is amplified and bandwidth-limited before it reaches the logic interface rather than being connected directly. I do not identify the visible OPA2333 package with the six-pin decal from the other capture.

<figure>
  <pre><code>PPG input
  → OPA2333 amplification
  → RC filtering and gain
  → OPA2333 output stage
  → SN74LVC logic interface
  → placement view in the PPG capture</code></pre>
  <figcaption>I kept only the functional blocks visible in the saved screen and did not invent component values or cutoff frequencies.</figcaption>
</figure>

## What the layout screen shows {#layout}

The same capture places a PADS Logic schematic beside a PADS Layout placement view. It shows that parts and connectivity reached the layout stage. A design screen alone does not establish fabrication, completed DRC, or measured PPG performance.

## My next check {#next}

Next I will compare the six-pin decal against its actual package drawing, including pin 1, pad dimensions, and courtyard. For the PPG design, I need a part-to-footprint mapping before inspecting packaging, net names, and unrouted connections. Until that mapping exists, I will keep the captures as separate artifacts.

## Previous and next {#navigation}

- [Previous: coursework overview]({{ '/en/coursework/' | relative_url }})
- [Series: PADS PCB Design]({{ '/en/blog/series/pads-pcb-design/' | relative_url }})
- [Next: PPG-HRV project]({{ '/en/projects/ppg-hrv/' | relative_url }})
