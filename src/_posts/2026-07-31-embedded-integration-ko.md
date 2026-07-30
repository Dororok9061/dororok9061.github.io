---
title: Two-node embedded prototype에서 data path를 문서화하기
description: Raspberry Pi sensing과 analysis node 사이의 network, file IPC, GPIO, I2C 경계를 기록하는 방법.
date: 2026-07-31 00:40:00 +0900
categories: [embedded]
lang: ko
permalink: /blog/2026/07/31/embedded-data-path/
alternate_url: /en/blog/2026/07/31/embedded-data-path/
alternate_lang: en
---

센서 acquisition과 영상 분석을 서로 다른 node에 배치하면 network transfer,
file IPC, clock과 error handling이 새로운 system boundary가 됩니다. 단순한
component 목록만으로는 실제 data path를 설명할 수 없습니다.

입력 sensor, processing stage, TCP/IP transfer, GPIO·I²C alarm output을 순서대로
연결하고, 각 경계에서 확인한 source와 prototype 사진을 구분해 기록해야 합니다.
사진은 통합 존재를 보여주지만 latency나 정확도 측정은 아닙니다.

[Embedded project page](/projects/drowsiness-monitor/)에서 공개된 구현 근거와
아직 보고되지 않은 metric을 함께 확인할 수 있습니다.
