---
title: Reading the Mealy 101 Detector and 8-to-1 MUX Sources
title_en: Reading the Mealy 101 Detector and 8-to-1 MUX Sources
description: My source-level review of overlapping 101 transitions and a decoder-based multiplexer from stored VHDL coursework.
date: 2026-08-01 11:01:00 +0900
updated: 2026-08-01 11:01:00 +0900
study_date: 2024-11-22
lang: en
translation_key: controller-logic-mealy-mux
permalink: /en/blog/2026/08/01/controller-logic-mealy-mux/
alternate_url: /blog/2026/08/01/controller-logic-mealy-mux/
alternate_lang: ko
primary_category: major-foundations
subcategory: controller-logic
series: vhdl-foundations
series_order: 7
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: SOURCE_REVIEWED_NOT_RERUN
tools: [VHDL, Vivado]
hardware: []
software_versions: []
source_materials:
  - { title: Controller Logic coursework VHDL source, type: local-coursework, public_url: "", file_reference: mealy.vhd and mux_8to1.vhd, pages: "", used_for: state transitions and source structure }
prerequisites: [digital-logic, vhdl]
learning_objectives: [Mealy state transition, overlapping sequence detection, multiplexer selection]
related_projects: [fpga-delay-logic]
related_posts: [fpga-architecture-equivalence]
tags: [vhdl, mealy-fsm, sequence-detector, multiplexer]
cover_image: /assets/images/study/coursework/controller-logic-waveform.webp
thumbnail: /assets/images/study/coursework/controller-logic-waveform.webp
image_alt: Vivado waveform showing Mealy 101 states and output for a 01010101 input
draft: false
revision_history:
  - { date: 2026-08-01, change: Written from the stored VHDL and testbench stimulus }
toc:
  - { id: source, title: Starting from source }
  - { id: states, title: Finding 101 with three states }
  - { id: stimulus, title: Tracing 01010101 }
  - { id: mux, title: Writing a standalone MUX }
  - { id: rerun, title: What I will check next }
  - { id: navigation, title: Previous and next }
---

## Starting from source {#source}

I reopened the stored <code>mealy.vhd</code>, <code>mealy_tb.vhd</code>, and <code>mux_8to1.vhd</code> files from my 2024 coursework. I focused on the entity, architecture, and stimulus that I had written instead of the Vivado cache and generated executables.

<figure>
  <img src="{{ '/assets/images/learning/coursework/controller-logic-mealy-mux.svg' | relative_url }}" alt="Three-state overlapping Mealy 101 detector beside an eight-input multiplexer selection map" width="1200" height="630">
  <figcaption>The left panel traces the overlapping detector; the right panel rewrites the same selection function without a decoder dependency.</figcaption>
</figure>

## Finding 101 with three states {#states}

The transition path uses three states. <code>st0</code> has no useful prefix, <code>st1</code> means the latest bit is 1, and <code>st2</code> means the latest two bits are 10. A 1 in <code>st2</code> completes 101 and asserts <code>dout</code>. Returning to <code>st1</code> preserves that final 1 as the start of an overlapping pattern.

<figure>
  <table>
    <thead><tr><th>Current state</th><th>Input 0</th><th>Input 1</th><th>Output 1</th></tr></thead>
    <tbody>
      <tr><td>st0</td><td>st0</td><td>st1</td><td>-</td></tr>
      <tr><td>st1</td><td>st2</td><td>st1</td><td>-</td></tr>
      <tr><td>st2</td><td>st2</td><td>st1</td><td>on input 1</td></tr>
    </tbody>
  </table>
  <figcaption>The <code>st2 → st1</code> transition is the step that keeps overlapping detections possible.</figcaption>
</figure>

## Tracing 01010101 {#stimulus}

The stored testbench deasserts reset and applies <code>01010101</code> at 20 ns intervals. Following the table by hand completes 101 at the fourth, sixth, and eighth input positions. I did not rerun GHDL or Vivado simulation while writing this note, so these are source-level expectations rather than a new waveform result.

<figure><img src="{{ '/assets/images/study/coursework/controller-logic-waveform.webp' | relative_url }}" alt="Saved waveform showing 01010101 input, st0 st1 st2 states, and dout pulses" width="1200" height="514"><figcaption>I followed the saved input and state transitions together.</figcaption></figure>

## Writing a standalone MUX {#mux}

The original <code>mux_8to1.vhd</code> instantiates a <code>dec_3to8</code> component and combines decoded lines with AND and OR gates. The decoder source was not present in the stored bundle I reviewed. I therefore rewrote the same truth table as a dependency-free study example.

<figure>
  <pre><code class="language-vhdl">with sel select
  y &lt;= a when "000",
       b when "001",
       c when "010",
       d when "011",
       e when "100",
       f when "101",
       g when "110",
       h when others;</code></pre>
  <figcaption>This example explains the selection function; it does not alter or prove a build of the archived project.</figcaption>
</figure>

## What I will check next {#rerun}

On the next run I will place <code>present_state</code>, <code>next_state</code>, and <code>dout</code> beside the input at each clock edge. For the MUX, I will exercise all select values on the standalone version first and compare the structural version only after recovering its decoder source.

## Previous and next {#navigation}

- [Previous: coursework overview]({{ '/en/coursework/' | relative_url }})
- [Series: VHDL Digital Logic Foundations]({{ '/en/blog/series/vhdl-foundations/' | relative_url }})
- [Next: shift-register and circular-queue verification]({{ '/en/blog/2026/07/31/fpga-architecture-equivalence/' | relative_url }})
