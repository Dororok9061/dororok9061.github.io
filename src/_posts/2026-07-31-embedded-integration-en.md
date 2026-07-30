---
title: Documenting data paths in a two-node embedded prototype
description: Recording network, file IPC, GPIO, and I2C boundaries between Raspberry Pi sensing and analysis nodes.
date: 2026-07-31 00:41:00 +0900
categories: [embedded]
lang: en
permalink: /en/blog/2026/07/31/embedded-data-path/
alternate_url: /blog/2026/07/31/embedded-data-path/
alternate_lang: ko
---

Separating sensor acquisition and vision analysis across two nodes introduces
new system boundaries: network transfer, file IPC, clocks, and error handling.
A component list alone does not describe the real data path.

Inputs, processing stages, TCP/IP transfer, and GPIO/I²C alarm outputs should be
connected in order, with source evidence separated from prototype photographs.
Photographs show integration existed; they do not measure latency or accuracy.

The [embedded project page](/en/projects/drowsiness-monitor/) presents both
public implementation evidence and the metrics that remain unreported.
