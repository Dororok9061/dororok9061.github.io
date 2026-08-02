---
layout: rf-calculator
title: Equal Power Split
description: N-way ideal split loss와 추가 insertion loss를 반영한 출력별 power를 계산한다.
lang: ko
permalink: /tools/rf/equal-split/
calculator_id: equal-split
tool_order: 6
formulas: ["L_split = 10 log10(N)", "P_each,dBm = P_in,dBm - L_split - L_extra"]
example: 20 dBm을 ideal 2-way로 나누면 각 출력은 약 16.99 dBm이다. 1 dB 추가 loss가 있으면 15.99 dBm이다.
interpretation: split loss는 에너지 분배이고 extra insertion loss는 dissipative loss다. 둘을 한 loss 원인처럼 쓰지 않는다.
related_post: /blog/rf/block-08-coupler-divider/
related_label: Coupler·Divider·Combiner 공부글
---
