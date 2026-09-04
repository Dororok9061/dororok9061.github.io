---
title: Solar Cell 다채널 측정 PCB의 전원·계측·통신 경로
title_en: Power, Measurement, and Communication Paths in a Multichannel Solar-Cell PCB
description: STM32F401 메인보드와 8채널 측정 모듈을 따라 전원, ADC, DAC와 USB/UART 구조를 분석한 설계 사례.
date: 2026-09-04 12:10:00 +0900
updated: 2026-09-04 12:10:00 +0900
lang: ko
translation_key: solarcell-mppt-pcb
permalink: /blog/2026/09/04/solarcell-mppt-pcb/
alternate_url: /en/blog/2026/09/04/solarcell-mppt-pcb/
alternate_lang: en
primary_category: pcb-pads
subcategory: schematic
series: pads-pcb-design
series_order: 7
post_type: project-log
practical: true
difficulty: advanced
study_status: published
evidence_status: DESIGN_ARCHIVE
tools: [PADS Logic, PADS Layout, STM32F401, AD7997, AD5629R, OPA703]
hardware: [Solar-cell measurement mainboard, Measurement module]
software_versions: []
source_materials:
  - { title: Solar-cell mainboard and measurement-module design archive, type: project-archive, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/solarcell-mppt-pcb", file_reference: curated schematic PCB and BOM files, pages: "", used_for: circuit and PCB analysis }
  - { title: Low-cost Open-source 12-channel MPPT Data Logger for Solar Cell Research, type: paper, public_url: "https://doi.org/10.1109/PVSC43889.2021.9519025", file_reference: external reference only, pages: "", used_for: 12-channel MPPT architecture reference }
prerequisites: [electronic-circuits, adc, uart, power-electronics]
learning_objectives: [power tree, current sensing, voltage measurement, ADC DAC path, PCB handoff]
related_projects: [solarcell-mppt-pcb]
related_posts: [pads-footprint-ppg-schematic]
tags: [solar-cell, mppt, stm32f401, current-sensing, adc, dac, pads]
cover_image: /assets/images/projects/solarcell-mppt-pcb/mainboard-schematic.webp
thumbnail: /assets/images/projects/solarcell-mppt-pcb/mainboard-schematic.webp
image_alt: STM32F401 메인보드와 전원·통신·측정 모듈 연결 회로도
draft: false
revision_history:
  - { date: 2026-09-04, change: 회로 PCB BOM과 공개 MPPT 논문의 역할을 나눠 정리 }
toc:
  - { id: purpose, title: 설계 목적 }
  - { id: mainboard, title: 메인보드 }
  - { id: measurement, title: 측정 모듈 }
  - { id: data, title: 제어와 데이터 }
  - { id: pcb, title: PCB 산출물 }
  - { id: scope, title: 출처와 다음 시험 }
---

## 설계 목적 {#purpose}

여러 Solar Cell 채널을 같은 조건에서 비교하려면 채널별 전류와 전압을 읽는 회로,
setpoint를 인가하는 경로, 공통 전원과 MCU 통신을 함께 구성해야 한다. 이 프로젝트는
STM32F401 메인보드와 측정 모듈 파일을 기준으로 각 기능이 어디서 시작해 어느
connector로 이어지는지 추적했다.

## STM32F401 메인보드 {#mainboard}

12 V 입력은 5 V와 3.3 V rail로 내려가 MCU와 주변 회로에 공급된다. STM32F401
주변에는 SWD, USB와 UART가 있고, 세 connector가 measurement module의 ADC와
DAC bus, 전원과 address 신호를 전달한다. 전원 tree를 먼저 그린 뒤 digital
interface를 올리니 power fault와 communication fault를 나눠 생각하기 쉬웠다.

<figure><img src="{{ '/assets/images/projects/solarcell-mppt-pcb/mainboard-schematic.webp' | relative_url }}" alt="STM32F401, 12 V 전원 입력, USB UART와 세 모듈 커넥터가 있는 메인보드 회로도" width="1600" height="1132"><figcaption>공통 전원·MCU·통신과 세 측정 모듈 접점을 한 장에서 본 메인보드.</figcaption></figure>

## 8채널 측정 모듈 {#measurement}

모듈에는 여덟 channel의 전류 신호가 들어오고 AD7997 ADC가 이를 모아 MCU 쪽으로
전달한다. 저장된 회로의 다른 sheet에는 OPA703 전압 경로와 AD5629R DAC가 있어
측정과 인가가 서로 다른 signal chain을 가진다. 회로를 부품 이름으로만 읽지 않고
input, conditioning, conversion, communication 순서로 나눴다.

<figure><img src="{{ '/assets/images/projects/solarcell-mppt-pcb/current-sensing.webp' | relative_url }}" alt="AD7997과 여덟 current-sensing channel을 표시한 회로도" width="1600" height="1132"><figcaption>여덟 전류 채널이 ADC 입력으로 모이는 measurement-module sheet.</figcaption></figure>

## 제어와 데이터 경로 {#data}

측정 방향은 cell channel에서 analog conditioning, ADC, MCU와 USB/UART로 흐른다.
제어 방향은 MCU setpoint가 DAC를 거쳐 channel control path로 이동한다. 양방향을
한 선으로 섞지 않고 command와 measurement로 나누면 connector pin과 net name을
대조할 때 빠진 경로를 찾기 쉽다.

```text
Measurement : Cell -> Analog path -> ADC -> MCU -> USB/UART
Control     : MCU setpoint -> DAC -> Channel control path
```

## PCB와 BOM 산출물 {#pcb}

PADS schematic과 PCB, parts list를 나란히 두고 주요 IC와 connector가 서로 맞는지
확인했다. 공개 archive에는 STM32F401 mainboard, measurement module의 schematic과
PCB, BOM을 담았다. 설치 프로그램, vendor PDF와 임시 변환 파일은 프로젝트를
이해하는 데 필요하지 않아 제외했다.

## 출처와 다음 시험 {#scope}

12채널 MPPT 개념은 Kelzenberg, Loke와 Atwater의 2021 IEEE PVSC 논문을 참고했다.
논문과 원저자 Gerber는 링크만 제공하고 이 저장소에서 다시 배포하지 않는다. 현재
설계 자료만으로는 계측 정확도, 효율, 온도 drift와 생산 수율을 판단할 수 없다.
제작 전에는 부품 최신 datasheet, reference voltage와 channel protection을 다시
검토하고, 제작 후에는 calibration과 load sweep 시험이 필요하다.
