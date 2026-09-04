---
title: IWR6843 3D People Tracking에서 설정부터 화면 출력까지
title_en: From IWR6843 Configuration to 3D People-Tracking Output
description: IWR6843 EVM의 설치, DSS 처리 구조, dual-UART와 Visualizer 출력을 따라간 시스템 통합 사례.
date: 2026-09-04 12:00:00 +0900
updated: 2026-09-04 12:00:00 +0900
lang: ko
translation_key: mmwave-visualizer-people-tracking
permalink: /blog/2026/09/04/mmwave-visualizer-people-tracking/
alternate_url: /en/blog/2026/09/04/mmwave-visualizer-people-tracking/
alternate_lang: en
primary_category: rf-radar-signal
subcategory: radar-signal-processing
series: fmcw-radar-signal-processing
series_order: 6
post_type: project-log
practical: true
difficulty: advanced
study_status: published
evidence_status: HARDWARE_AND_RUNTIME_SCREENS
tools: [IWR6843ISK, IWR6843AOP, TI Radar Toolbox, Code Composer Studio, SYS/BIOS, UART]
hardware: [IWR6843 EVM]
software_versions: []
source_materials:
  - { title: TI Radar Toolbox project archive and Visualizer captures, type: project-archive, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/mmwave-visualizer", file_reference: curated configuration and images, pages: "", used_for: system architecture and runtime-output review }
prerequisites: [radar-basics, range-fft, beamforming, uart]
learning_objectives: [sensor configuration, DSS MSS data path, dual UART, 3D tracking output]
related_projects: [mmwave-visualizer]
related_posts: [radar-candidate-timing]
tags: [mmwave, iwr6843, people-tracking, visualizer, uart, system-integration]
cover_image: /assets/images/projects/mmwave-visualizer/lab-setup.webp
thumbnail: /assets/images/projects/mmwave-visualizer/people-tracking.webp
image_alt: 스탠드에 설치한 IWR6843 레이더와 3D People Tracking 실험 환경
draft: false
revision_history:
  - { date: 2026-09-04, change: "장비 사진과 실행 화면, build artifact를 대조해 작성" }
toc:
  - { id: setup, title: 실험 환경 }
  - { id: processing, title: 레이더 처리 구조 }
  - { id: handoff, title: DSS와 MSS }
  - { id: uart, title: 두 UART }
  - { id: output, title: Visualizer 출력 }
  - { id: scope, title: 현재 확인 범위 }
---

## 실험 환경 {#setup}

IWR6843 계열 EVM을 스탠드에 세우고 사람의 이동이 들어오는 방향을 기준으로 센서
높이와 방향을 맞췄다. 같은 설정값이라도 장착 자세와 관측 영역이 달라지면 point
cloud가 화면 밖으로 나가거나 바닥 반사가 두드러질 수 있어, 설치 상태와 GUI 출력을
함께 보며 조정했다.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/lab-setup.webp' | relative_url }}" alt="스탠드에 장착한 IWR6843 EVM과 PC Visualizer 환경" width="1200" height="1600"><figcaption>IWR6843 EVM, 연결 보드와 Visualizer를 함께 둔 실험 구성.</figcaption></figure>

## 레이더 처리 구조 {#processing}

저장된 DSS project에서 range와 Doppler 처리 뒤 2D Capon/MVDR beamforming, dynamic
및 static CFAR가 이어지는 구성을 확인했다. 결과는 angle, Doppler, SNR 정보를 가진
point cloud와 target list로 정리된다. GUI의 점 하나를 센서 출력으로만 보지 않고,
chirp부터 검출 결과까지 어떤 단계가 앞에 있는지 순서대로 대응시켰다.

## DSS와 MSS 사이의 전달 {#handoff}

C674x DSS 쪽 build와 SYS/BIOS 구성은 레이더 신호처리를 담당하고, 처리 결과는
shared memory와 mailbox를 거쳐 MSS 쪽 전달 경로로 넘어간다. 보유 파일에는 MSS
binary만 있고 대응 source가 없었기 때문에 MSS 내부 수정을 작업 범위로 쓰지 않았다.
대신 DSS 출력 형식과 serial packet이 Visualizer 입력으로 이어지는 접점을 중심으로
살폈다.

## 두 UART의 역할 {#uart}

연결 단계에서는 CLI port와 data port를 분리했다. CLI는 115200 bps로 센서 설정을
전달하고, data port는 921600 bps로 point cloud와 target 정보를 보낸다. 포트를
바꾸어 연결하거나 baud rate가 맞지 않으면 설정은 들어가도 화면이 멈추거나 반대로
데이터가 해석되지 않는다. 이 구분은 센서, firmware와 PC application 사이 문제를
나눠 보는 기준이 됐다.

## Visualizer에서 본 출력 {#output}

sensor position, FOV, range, boundary와 detection threshold를 조정한 뒤 3D tracking
화면에서 target ID와 bounding box가 시간에 따라 움직이는 모습을 비교했다. 별도
화면에서는 range profile, point cloud와 vital-sign 표시도 확인했다.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/people-tracking.webp' | relative_url }}" alt="target ID와 3D bounding box가 표시된 People Tracking 실행 화면" width="1080" height="1080"><figcaption>실행 영상의 한 프레임에서 target ID와 공간 좌표가 함께 갱신된 모습.</figcaption></figure>

## 현재 확인 범위 {#scope}

이 경험의 핵심은 레이더 알고리즘을 처음부터 새로 만드는 일이 아니라 장비, DSP
build, 통신 설정과 GUI 출력을 하나의 data path로 이해한 데 있다. 18.17초 실행
영상에서는 3D target의 이동을 확인했다. vital-sign 숫자는 UI 기능 출력으로만
다뤘으며 의료 성능, 차량용 CAN/LIN 연결과 환경·EMC 시험은 다음 단계의 과제다.
