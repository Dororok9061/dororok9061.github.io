---
title: Radar morphology의 후보 시점과 직접 측정을 구분하기
description: ECG, SCG, FMCW radar 정렬에서 candidate timing의 해석 경계를 설명합니다.
date: 2026-07-31 00:30:00 +0900
categories: [signal-processing]
lang: ko
permalink: /blog/2026/07/31/radar-candidate-timing/
alternate_url: /en/blog/2026/07/31/radar-candidate-timing/
alternate_lang: en
---

ECG R-peak를 beat anchor로 사용하면 SCG와 Radar waveform을 반복 심박 기준으로
정렬할 수 있습니다. 그러나 morphology의 peak 또는 변화점은 해부학적 event의
직접 영상이 아닙니다.

따라서 AO·AC 표기는 **candidate timing**으로 제한하고, detector fusion과 SQI가
선택한 시점의 근거를 별도로 남겨야 합니다. 독립 echo, ICG 또는 PCG reference가
없는 경우 validation boundary도 함께 공개해야 합니다.

[Radar project page](/projects/fmcw-radar/)는 분석 source와 hardware evidence가
지원하는 범위만 설명합니다.
