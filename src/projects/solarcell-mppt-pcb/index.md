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

12 V 입력, 5 V·3.3 V rail, STM32F401, USB/UART와 세 개 측정 모듈 커넥터를
메인보드 기준으로 추적했다. 측정 모듈에서는 8채널 전류 센싱, ADC, 전압 증폭과
DAC 경로를 기능 블록으로 나누고 회로·PCB·BOM 파일을 대조했다.

12채널 MPPT 개념은 Kelzenberg·Loke·Atwater의 공개 연구를 참고했다. 공개
저장소에는 재배포 조건이 불분명한 논문 PDF와 원저자의 Gerber를 복제하지 않고,
본 작업의 메인보드·측정 모듈 자료와 출처 링크를 담았다.
