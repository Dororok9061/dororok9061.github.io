---
layout: rf-calculator
title: Reflection Coefficient · Return Loss · VSWR
description: 복소 부하와 기준 임피던스에서 Γ, return loss, VSWR, mismatch loss를 계산한다.
lang: ko
permalink: /tools/rf/reflection-vswr/
calculator_id: reflection-vswr
tool_order: 2
formulas: ["Gamma = (Z_L - Z_0)/(Z_L + Z_0)", "VSWR = (1 + |Gamma|)/(1 - |Gamma|)", "RL = -20 log10(|Gamma|)"]
example: Z0=50 Ω, ZL=75+j25 Ω이면 복소 Γ의 크기와 위상을 먼저 구한 뒤 return loss와 VSWR을 계산한다.
interpretation: VSWR과 return loss는 |Γ|만 보여준다. mismatch 방향과 phase를 보려면 복소 Γ 또는 Smith chart가 필요하다.
related_post: /blog/rf/reflection-vswr/
related_label: 반사 관계 공부글
---
