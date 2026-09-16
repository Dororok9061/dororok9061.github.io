---
layout: project
project_id: solarcell-mppt-pcb
title: Solar Cell 다채널 측정·MPPT PCB
description: STM32F401 메인보드와 다채널 전류·전압 측정 모듈의 전원·계측·통신 경로를 분석한 PCB 프로젝트.
permalink: /projects/solarcell-mppt-pcb/
lang: ko
alternate_url: /en/projects/solarcell-mppt-pcb/
alternate_lang: en
---

STM32F401 메인보드의 12 V 입력·5 V/3.3 V rail·USB/UART·측정 모듈 커넥터를 회로와 PCB에서 추적했다. 측정 모듈은 8채널 전류 센싱·ADC·전압 증폭·DAC 경로로 구성된다.

- [메인보드·측정 모듈 회로와 BOM](https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/solarcell-mppt-pcb/source)
- [전원·계측·통신 설계 기록](/blog/2026/09/04/solarcell-mppt-pcb/)

12채널 MPPT 구조의 참고 문헌: Kelzenberg·Loke·Atwater 공개 연구.
