---
layout: rf-calculator
title: Microstrip 초기값 계산
description: zero-thickness closed-form 근사로 유효 유전율, Z0, 유도파장, 90도 길이를 계산한다.
lang: ko
permalink: /tools/rf/microstrip/
calculator_id: microstrip
tool_order: 5
formulas: ["epsilon_eff ≈ (epsilon_r+1)/2 + (epsilon_r-1)/(2 sqrt(1+12h/W))", "Z0 = closed-form function of W/h and epsilon_eff"]
example: alumina εr=9.9, h=0.5 mm, W=0.4815 mm를 넣어 내 과제의 50 Ω 초기값과 비교할 수 있다.
interpretation: conductor thickness, roughness, loss, dispersion, solder mask, launch가 빠진 초기 근사다. Cadence·EM·VNA 결과를 대신하지 않는다.
related_post: /blog/rf/transmission-lines/
related_label: 전송선·Microstrip 비교 공부글
---
