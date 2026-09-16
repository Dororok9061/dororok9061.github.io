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

The IWR6843 setup uses sensor height, orientation, FOV, range, and threshold settings matched to the room. C674x DSS processing and DSS–MSS transfer feed the 115200-bps CLI and 921600-bps data UART paths, ending in 3D point-cloud and target-tracking views.

- [Sensor configuration and tracking run](/en/blog/2026/09/04/mmwave-visualizer-people-tracking/)
- [DCA1000EVM raw ADC capture debugging](/en/projects/dca1000evm/)
- [TI target configuration and records](https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/mmwave-visualizer)

Software base: TI Radar Toolbox and SDK examples. Archived artifacts: DSS build records, MSS binary, and Visualizer screens.
