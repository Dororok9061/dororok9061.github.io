---
title: Verifying architecture equivalence in delay logic
description: Comparing shift-register and circular-queue implementations through one cycle-delay contract.
date: 2026-07-31 00:21:00 +0900
categories: [fpga]
lang: en
permalink: /en/blog/2026/07/31/fpga-architecture-equivalence/
alternate_url: /blog/2026/07/31/fpga-architecture-equivalence/
alternate_lang: ko
---

When a delay-logic implementation changes, the comparison target is the
external contract rather than the internal data structure. Given identical
input data and valid sequences, output data, output valid, reset behavior, and
the exact cycle delay must match.

An independent reference model should not copy the DUT architecture. Tagging
input transactions and calculating expected output cycles reduces the risk of
reproducing the same design error in both the DUT and checker.

The [FPGA project page](/en/projects/fpga-delay-logic/) records both the check
counts supported by public logs and why Quartus verification remains BLOCKED.
