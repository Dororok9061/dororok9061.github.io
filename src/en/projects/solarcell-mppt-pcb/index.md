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

I traced the 12-V input, 5-V/3.3-V rails, STM32F401, USB/UART, and three
measurement-module connectors from the mainboard. At module level, I decomposed
the eight-channel current-sensing, ADC, voltage-amplification, and DAC paths and
cross-checked the schematic, PCB, and BOM files.

The 12-channel MPPT concept references published work by Kelzenberg, Loke, and
Atwater. The public archive links to that source and omits the paper PDF and the
original author's Gerbers where redistribution terms were unclear.
