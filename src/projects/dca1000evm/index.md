---
layout: project
project_id: dca1000evm
title: DCA1000EVM Raw ADC 디버깅
description: 제어 UDP와 0-packet ADC 수집 로그를 중심으로 LVDS·Ethernet·펌웨어·전원 경로를 분리한 진단 기록.
permalink: /projects/dca1000evm/
lang: ko
alternate_url: /en/projects/dca1000evm/
alternate_lang: en
---

제어 UDP는 관측됐고 Raw ADC capture log의 수신 수는 **0 packets**였다. 연결·설정·펌웨어·데이터 경로를 나누어 원인을 좁힌 기록이다.

- [Wireshark 패킷 필터·제어 UDP](/blog/2026/09/09/dca1000evm-troubleshooting-data-path/#wireshark)
- [UniFlash 펌웨어 기록 화면](/blog/2026/09/09/dca1000evm-troubleshooting-data-path/#uniflash)
- [Tera Term UART 응답](/blog/2026/09/09/dca1000evm-troubleshooting-data-path/#teraterm)
- [0-packet capture log](/blog/2026/09/09/dca1000evm-troubleshooting-data-path/#capture-log)
- [36개 진단 화면과 전체 점검 순서](/blog/2026/09/09/dca1000evm-troubleshooting-data-path/)
- [별도 mmWave 3D 추적 프로젝트](/projects/mmwave-visualizer/)
