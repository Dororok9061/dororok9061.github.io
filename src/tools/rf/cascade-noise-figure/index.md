---
layout: rf-calculator
title: Cascaded Noise Figure
description: 세 stage의 gain과 noise figure를 linear 값으로 바꿔 Friis 식을 계산한다.
lang: ko
permalink: /tools/rf/cascade-noise-figure/
calculator_id: cascade-noise-figure
tool_order: 4
formulas: ["F_total = F1 + (F2-1)/G1 + (F3-1)/(G1 G2)", "NF_dB = 10 log10(F)"]
example: NF1=2 dB, G1=15 dB, NF2=8 dB이면 두 단만 보아도 전체 NF는 약 2.437 dB다.
interpretation: dB noise figure를 그대로 더하지 않는다. gain도 dB에서 linear available gain으로 바꾼 뒤 식에 넣는다.
related_post: /blog/rf/noise-figure-cascade/
related_label: Cascade Noise Figure 공부글
---
