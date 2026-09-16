---
layout: project
project_id: solarcell-mppt-pcb
title: Solar-Cell Multichannel Measurement and MPPT PCB
description: PCB analysis of power, measurement, and communication paths across an STM32F401 mainboard and multichannel current/voltage modules.
permalink: /en/projects/solarcell-mppt-pcb/
lang: en
alternate_url: /projects/solarcell-mppt-pcb/
alternate_lang: ko
---

The STM32F401 mainboard records cover its 12-V input, 5-V/3.3-V rails, USB/UART, and measurement-module connectors. The module separates eight-channel current sensing, ADC, voltage amplification, and DAC paths.

- [Mainboard/module schematics and BOM](https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/solarcell-mppt-pcb/source)
- [Power, measurement, and communication design](/en/blog/2026/09/04/solarcell-mppt-pcb/)

Reference for the 12-channel MPPT structure: the public work by Kelzenberg, Loke, and Atwater.
