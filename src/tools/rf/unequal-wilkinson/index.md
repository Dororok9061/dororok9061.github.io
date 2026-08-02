---
layout: rf-calculator
title: Unequal-Split Wilkinson
description: P2:P3 power ratio와 system impedance에서 두 quarter-wave arm과 isolation resistor 초기값을 계산한다.
lang: ko
permalink: /tools/rf/unequal-wilkinson/
calculator_id: unequal-wilkinson
tool_order: 7
formulas: ["K = sqrt(P2/P3)", "Z02 = Z0 sqrt(K(1+K^2))", "Z03 = Z0 sqrt((1+K^2)/K^3)", "R = Z0(K + 1/K)"]
example: P2:P3=1이면 K=1, 두 arm은 모두 70.71 Ω이고 resistor는 100 Ω가 되어 equal Wilkinson으로 돌아간다.
interpretation: port 2와 port 3의 ratio 정의를 뒤집으면 arm 값도 바뀐다. 실제 microstrip width와 junction discontinuity는 EM tuning이 필요하다.
related_post: /blog/rf/block-08-coupler-divider/
related_label: Coupler·Divider·Combiner 공부글
---
