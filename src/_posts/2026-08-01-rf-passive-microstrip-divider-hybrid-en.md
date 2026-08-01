---
title: From a 3.5 GHz Microstrip to Wilkinson and Branch-Line Networks
title_en: From a 3.5 GHz Microstrip to Wilkinson and Branch-Line Networks
description: My review of alumina microstrip calculations and stored Cadence divider and hybrid screens.
date: 2026-08-01 11:02:00 +0900
updated: 2026-08-01 11:02:00 +0900
study_date: 2026-06-14
lang: en
translation_key: rf-passive-microstrip-divider-hybrid
permalink: /en/blog/2026/08/01/rf-passive-microstrip-divider-hybrid/
alternate_url: /blog/2026/08/01/rf-passive-microstrip-divider-hybrid/
alternate_lang: ko
primary_category: rf-radar-signal
subcategory: s-parameter
series: rf-microwave
series_order: 3
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: ARCHIVED_SIMULATION_SCREENSHOTS
tools: [Cadence Virtuoso, Smith Chart]
hardware: []
software_versions: []
source_materials:
  - { title: RF and Microwave coursework report and screenshots, type: local-coursework, public_url: "", file_reference: "homework 2, 4, and 5", pages: "", used_for: dimensions and archived simulation markers }
prerequisites: [electromagnetics, transmission-line, s-parameter]
learning_objectives: [microstrip dimensions, insertion loss and phase, divider and hybrid topology]
related_projects: []
related_posts: [radar-candidate-timing]
tags: [microstrip, cadence-virtuoso, wilkinson-divider, branch-line-hybrid]
cover_image: /assets/images/learning/coursework/rf-passive-microstrip-divider-hybrid.svg
thumbnail: /assets/images/learning/coursework/rf-passive-microstrip-divider-hybrid.svg
image_alt: Fifty-ohm microstrip cross-section with Wilkinson and branch-line dimensions
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected coursework calculations to values visible in stored Cadence screens }
toc:
  - { id: start, title: Starting conditions }
  - { id: microstrip, title: Width and length }
  - { id: marker, title: Reading the 3.7 GHz marker }
  - { id: wilkinson, title: Wilkinson divider }
  - { id: hybrid, title: Branch-line hybrid }
  - { id: interpretation, title: Simulation-only interpretation }
  - { id: navigation, title: Previous and next }
---

## Starting conditions {#start}

I began by collecting the shared assumptions from my RF coursework: a 0.5 mm alumina substrate, relative permittivity 9.9, and a 3.5 GHz design frequency. Those values set the microstrip width, guided wavelength, and quarter-wave sections used by both passive networks.

<figure>
  <img src="{{ '/assets/images/learning/coursework/rf-passive-microstrip-divider-hybrid.svg' | relative_url }}" alt="Alumina microstrip and stored 3.7 GHz marker beside Wilkinson and branch-line dimensions" width="1200" height="630">
  <figcaption>The left panel keeps the transmission-line calculation together; the right panel compares the dimensions entered for the two networks.</figcaption>
</figure>

## Width and length {#microstrip}

The calculated width for a 50 Ω line was about 0.4815 mm. A 270° delay at 3.5 GHz is three quarters of the guided wavelength, giving a length near 24.97 mm. I initially confused the free-space wavelength with the shorter guided wavelength on alumina; separating them made the report value consistent.

<figure>
  <table>
    <thead><tr><th>Item</th><th>Value</th><th>Use</th></tr></thead>
    <tbody>
      <tr><td>Relative permittivity</td><td>9.9</td><td>Alumina</td></tr>
      <tr><td>Substrate height</td><td>0.5 mm</td><td>Shared condition</td></tr>
      <tr><td>50 Ω width</td><td>about 0.4815 mm</td><td>Microstrip calculation</td></tr>
      <tr><td>270° length</td><td>about 24.97 mm</td><td>at 3.5 GHz</td></tr>
    </tbody>
  </table>
  <figcaption>I converted µm and mm values to one unit before comparing the designs.</figcaption>
</figure>

## Reading the 3.7 GHz marker {#marker}

A stored Cadence screen marks approximately −0.095 dB insertion loss and −284.49° phase at 3.7 GHz. The accumulated phase is larger than the 270° target at 3.5 GHz, which is consistent with observing the same line at a higher frequency. These are values read from the earlier simulation screen, not instrument measurements.

## Wilkinson divider {#wilkinson}

An equal-split Wilkinson uses two theoretical 70.7 Ω quarter-wave branches. The stored design tuned the resistor from 100 Ω to 94 Ω and used branch width 270 µm and length 6.65 mm. The screen places S21 and S31 near −3 dB and S11 near −15 dB. I treat the notch position and center-frequency alignment as items to check again instead of describing the match as perfect.

<figure>
  <table>
    <thead><tr><th>Network</th><th>Transmission line</th><th>Reading from stored screen</th></tr></thead>
    <tbody>
      <tr><td>Wilkinson</td><td>70.7 Ω, W 270 µm, L 6.65 mm</td><td>S21/S31 near −3 dB, S11 near −15 dB</td></tr>
      <tr><td>Branch-line</td><td>35.35 Ω horizontal, 50 Ω vertical</td><td>center shift in split and isolation curves</td></tr>
    </tbody>
  </table>
  <figcaption>Keeping theoretical impedance and entered geometry in separate columns made the tuning step easier to follow.</figcaption>
</figure>

## Branch-line hybrid {#hybrid}

The quadrature hybrid forms a rectangle with 35.35 Ω horizontal lines and 50 Ω vertical lines. The stored dimensions were W 908 µm and L 7.0 mm horizontally, then W 483 µm and L 7.2 mm vertically. Drawing the two widths separately helped me remember why the four sides do not share one impedance.

## Simulation-only interpretation {#interpretation}

This note connects calculations in the report to earlier Cadence screens. I did not rerun the netlist or measure a fabricated network with a VNA. My next step is to recreate the same sweep and inspect marker frequency, port definitions, and dB conventions together.

## Previous and next {#navigation}

- [Previous: coursework overview]({{ '/en/coursework/' | relative_url }})
- [Series: RF and Microwave]({{ '/en/blog/series/rf-microwave/' | relative_url }})
- [Next: FMCW radar candidate timing]({{ '/en/blog/2026/07/31/radar-candidate-timing/' | relative_url }})
