---
title: Biomedical AI에서 metric provenance를 보존하기
description: 논문 요약과 code archive의 AUC·F1 결과를 평가 조건 없이 합치지 않는 이유.
date: 2026-07-31 00:50:00 +0900
categories: [biomedical-ai]
lang: ko
permalink: /blog/2026/07/31/biomedical-metric-provenance/
alternate_url: /en/blog/2026/07/31/biomedical-metric-provenance/
alternate_lang: en
---

같은 모델 이름과 같은 metric 이름을 사용해도 dataset split, fold 구성,
preprocessing, aggregation 단위가 다르면 수치는 직접 비교할 수 없습니다.

논문 PDF의 summary metric과 별도 code archive의 fold CSV는 각각 provenance를
유지해야 합니다. 평균 AUC나 F1을 표시할 때는 계산 source, fold 수, 대상
sample과 exclusion을 함께 연결해야 합니다.

[PPG–HRV project page](/projects/ppg-hrv/)는 서로 다른 평가 조건의 수치를
하나의 성능 결과로 합치지 않습니다.
