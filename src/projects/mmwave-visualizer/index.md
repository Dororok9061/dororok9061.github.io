---
layout: project
project_id: mmwave-visualizer
title: TI mmWave 3D People Tracking Visualizer
description: IWR6843 EVM 설정부터 DSP 데이터 경로와 3D 추적 출력까지 점검한 시스템 통합 프로젝트.
permalink: /projects/mmwave-visualizer/
lang: ko
alternate_url: /en/projects/mmwave-visualizer/
alternate_lang: en
---

IWR6843의 설치 높이·방향·FOV·range·threshold를 실험 공간에 맞춰 조정했다. C674x DSS 처리와 DSS–MSS 데이터 이동, CLI 115200 bps·data 921600 bps UART를 거쳐 3D point cloud와 target tracking 화면으로 이어진다.

- [센서 설정·3D 추적 실행 기록](/blog/2026/09/04/mmwave-visualizer-people-tracking/)
- [DCA1000EVM 원시 ADC 수집 디버깅](/projects/dca1000evm/)
- [TI target configuration과 자료](https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/mmwave-visualizer)

기반: TI Radar Toolbox·SDK 예제. 보관 자료: DSS build artifact·MSS 바이너리·Visualizer 화면.
