---
title: Preserving metric provenance in biomedical AI
description: Why AUC and F1 values from a paper summary and code archive cannot be merged without evaluation context.
date: 2026-07-31 00:51:00 +0900
categories: [biomedical-ai]
lang: en
permalink: /en/blog/2026/07/31/biomedical-metric-provenance/
alternate_url: /blog/2026/07/31/biomedical-metric-provenance/
alternate_lang: ko
---

Even when a model and metric share the same name, values are not directly
comparable when dataset splits, fold construction, preprocessing, or
aggregation grain differ.

Summary metrics in a paper PDF and fold CSV files in a separate code archive
must retain independent provenance. Mean AUC or F1 should remain connected to
its calculation source, fold count, sample scope, and material exclusions.

The [PPG–HRV project page](/en/projects/ppg-hrv/) does not merge values from
different evaluation conditions into one performance result.
