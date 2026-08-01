---
layout: page
title: Coursework Portfolio
eyebrow: Electrical Engineering Coursework
lead: Undergraduate assignments and laboratories organized by domain, with design, execution, and measurement described separately.
description: Electrical engineering coursework across VHDL, power, control, RF, and sensors.
permalink: /en/coursework/
lang: en
alternate_url: /coursework/
alternate_lang: ko
---

## Digital logic and FPGA

I reread the VHDL from my controller-logic assignment, following an overlapping `101` Mealy FSM and a decoder-based 8-to-1 multiplexer at source level. The saved multiplexer references a `dec_3to8` unit that is not in the archive, so I do not present it as a successful fresh compile.

- [Reading the Mealy 101 Detector and 8-to-1 MUX Sources](/en/blog/2026/08/01/controller-logic-mealy-mux/)
- [SystemVerilog delay-logic architecture comparison](/en/blog/2026/07/31/fpga-architecture-equivalence/)

## Control and motor drives

I redrew the DC motor, H-bridge, and nested current and speed PI loops from my motor-control report. The 10 kHz and 30 kHz torque-ripple values remain archived PSIM simulation results, not physical motor measurements.

- [Cascaded PI Control and Field Weakening for a DC Motor in PSIM](/en/blog/2026/08/01/dc-motor-cascaded-pi-field-weakening/)

## RF and microwave

I connected a 3.5 GHz alumina microstrip calculation to saved Cadence views of a Wilkinson divider and branch-line hybrid. I replaced screenshots that exposed local paths with new public diagrams.

- [From a 3.5 GHz Microstrip to Wilkinson and Branch-Line Networks](/en/blog/2026/08/01/rf-passive-microstrip-divider-hybrid/)

## PADS and PCB design

I treated the saved six-pin SOIC Decal Wizard capture and a separate PPG design capture as two examples. The saved material does not establish a part relationship between them, so I did not merge them into one artifact.

- [Reading an SOIC Footprint and a PPG Schematic as Separate PADS Examples](/en/blog/2026/08/01/pads-footprint-ppg-schematic/)

## Topics I will continue

I will next revisit the transformer calculation, automatic-control exercises, and the AESA/SAR sensing proposal. Before copying any value from a saved report, I will recalculate its units and input assumptions.

- [Coursework project page](/en/projects/coursework/)
- [Full coursework repository](https://github.com/Tontonjeong/electrical-engineering-coursework-portfolio)
