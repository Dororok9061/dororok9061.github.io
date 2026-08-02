---
layout: rf-calculator
title: Quarter-Wave Transformer
description: 두 실수 임피던스 사이의 변환 선로 Zt와 유도파장·90도 길이를 계산한다.
lang: ko
permalink: /tools/rf/quarter-wave-transformer/
calculator_id: quarter-wave-transformer
tool_order: 3
formulas: ["Z_t = sqrt(Z_0 Z_L)", "lambda_g = c/(f sqrt(epsilon_eff))", "l = lambda_g/4"]
example: 50 Ω과 100 Ω 사이에는 70.71 Ω 변환선로가 필요하다. 길이는 물리 유전율이 아니라 해당 mode의 유효 유전율에 따른다.
interpretation: 이 계산은 lossless 단일주파수 실수 부하를 가정한다. dispersive microstrip과 complex load에는 추가 설계가 필요하다.
related_post: /blog/rf/impedance-port-matching/
related_label: 50 Ω·Port·Matching 공부글
---
