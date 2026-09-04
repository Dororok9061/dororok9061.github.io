---
layout: project
project_id: mmwave-visualizer
title: TI mmWave 3D People Tracking Visualizer
description: System integration from IWR6843 EVM configuration through DSP data flow and 3D tracking output.
permalink: /en/projects/mmwave-visualizer/
lang: en
alternate_url: /projects/mmwave-visualizer/
alternate_lang: ko
---

I installed the IWR6843 EVM in the test space and adjusted sensor height,
orientation, FOV, range, and thresholds. I then traced the C674x DSS processing
structure, DSS-to-MSS data movement, and the roles of the two UART links before
comparing live 3D point-cloud and target-tracking updates.

This work uses TI Radar Toolbox and SDK examples for integration and analysis. It
does not include new MSS source development or a medical-accuracy assessment of
the vital-sign display.
