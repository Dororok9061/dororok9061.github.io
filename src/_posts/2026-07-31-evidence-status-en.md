---
title: Why this portfolio separates evidence states
description: A record-keeping model that keeps Source Available, Executed, Measured, and BLOCKED distinct.
date: 2026-07-31 00:11:00 +0900
categories: [systems-engineering]
lang: en
permalink: /en/blog/2026/07/31/evidence-status/
alternate_url: /blog/2026/07/31/evidence-status/
alternate_lang: ko
---

The presence of source code does not prove that it was executed in a stated
environment. Execution, synthesis, numerical PPA, and hardware measurement also
require different evidence.

This portfolio uses four base states:

- **SOURCE AVAILABLE** — public source and documentation exist.
- **EXECUTED** — results were reproduced in the stated environment.
- **MEASURED** — measurement conditions and results are both public.
- **BLOCKED** — the required tool, source, or report is unavailable.

The distinction does not hide incomplete work. It acts as an engineering
interface for deciding where reproduction can begin and what the next
verification step requires.
