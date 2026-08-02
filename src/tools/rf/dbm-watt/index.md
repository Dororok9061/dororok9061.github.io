---
layout: rf-calculator
title: dBm ↔ Watt 변환
description: 1 mW 기준의 dBm과 watt를 양방향으로 계산한다.
lang: ko
permalink: /tools/rf/dbm-watt/
calculator_id: dbm-watt
tool_order: 1
formulas: ["P_dBm = 10 log10(P_mW)", "P_W = 10^((P_dBm - 30)/10)"]
example: 20 dBm은 100 mW, 즉 0.1 W다. 30 dBm은 1 W이며 10 dB 증가할 때 전력은 열 배가 된다.
interpretation: dBm은 절대 power level이고 dB는 ratio다. S21의 dB 값만으로 output dBm을 정하지 않는다.
related_post: /blog/rf/db-dbm-power/
related_label: dB와 dBm 계산 공부글
---
