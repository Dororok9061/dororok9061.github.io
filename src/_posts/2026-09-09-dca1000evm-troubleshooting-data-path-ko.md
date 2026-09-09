---
title: DCA1000EVM 원시 ADC 수집 장애를 경로별로 좁힌 디버깅
title_en: Isolating a DCA1000EVM Raw-ADC Capture Failure by Data Path
description: DCA1000EVM 제어 UDP는 보이지만 원시 ADC 수신 패킷은 0인 상황에서 Wireshark·UniFlash·Tera Term과 하드웨어 측정으로 경로를 분리한 트러블슈팅 사례.
date: 2026-09-09 12:00:00 +0900
updated: 2026-09-09 12:00:00 +0900
lang: ko
translation_key: dca1000evm-troubleshooting-data-path
permalink: /blog/2026/09/09/dca1000evm-troubleshooting-data-path/
alternate_url: /en/blog/2026/09/09/dca1000evm-troubleshooting-data-path/
alternate_lang: en
primary_category: rf-radar-signal
subcategory: radar-signal-processing
series: fmcw-radar-signal-processing
series_order: 7
post_type: troubleshooting
practical: true
difficulty: advanced
study_status: published
evidence_status: HARDWARE_AND_DIAGNOSTIC_RECORDS
tools: [IWR6843ISK, DCA1000EVM, mmWave Studio, Wireshark, UniFlash, Tera Term, Oscilloscope]
hardware: [IWR6843ISK, DCA1000EVM]
software_versions: [mmWave Studio 2.1.0.0, UniFlash]
source_materials:
  - { title: DCA1000EVM troubleshooting archive, type: project-archive, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/mmwave-visualizer", file_reference: user-provided hardware photos and Wireshark/UniFlash/Tera Term/capture-log screens, pages: "portfolio pp. 15-16", used_for: "observed states, fault-isolation sequence, and unresolved result" }
  - { title: DCA1000EVM Data Capture Card User's Guide Rev. A, type: vendor-documentation, public_url: "https://www.ti.com/lit/ug/spruij4a/spruij4a.pdf", file_reference: SPRUIJ4A, pages: "3, 16-21", used_for: "LVDS, FPGA, DDR3L, Ethernet, switch, and raw-mode architecture" }
  - { title: Texas Instruments DCA1000EVM product page, type: vendor-documentation, public_url: "https://www.ti.com/tool/DCA1000EVM", file_reference: product overview, pages: "", used_for: real-time LVDS capture and 1-Gbps Ethernet streaming role }
prerequisites: [fmcw-radar, lvds, ethernet, embedded-debugging]
learning_objectives: [signal-path isolation, control-path isolation, power and thermal checks, exit criteria]
related_projects: [mmwave-visualizer]
related_posts: [mmwave-visualizer-people-tracking]
tags: [dca1000evm, iwr6843, mmwave, raw-adc, lvds, ethernet, hardware-debugging]
cover_image: /assets/images/projects/mmwave-visualizer/dca1000-setup.webp
thumbnail: /assets/images/projects/mmwave-visualizer/dca1000-setup.webp
image_alt: DCA1000EVM과 IWR6843ISK를 연결해 원시 ADC 수집 경로를 점검한 장비 구성
draft: false
revision_history:
  - { date: 2026-09-09, change: "장비 사진, mmWave Studio 상태 화면과 포트폴리오 15-16쪽을 대조해 작성" }
  - { date: 2026-09-09, change: "Wireshark, UniFlash, Tera Term과 0-packet capture log를 단계별 디버깅 증거로 추가" }
  - { date: 2026-09-09, change: "추가 runtime·ipconfig·RFDataCaptureCard·Flash Binary 화면을 포함해 고유 디버깅 화면 33장을 모두 배치" }
toc:
  - { id: symptom, title: 미수신과 발열 }
  - { id: paths, title: 데이터·제어 경로 분리 }
  - { id: observations, title: 화면과 LED 상태 }
  - { id: wireshark, title: Wireshark 제어 UDP }
  - { id: uniflash, title: UniFlash 기록 확인 }
  - { id: teraterm, title: Tera Term CLI 확인 }
  - { id: capture-log, title: 0-packet 기록 }
  - { id: inspection, title: 하드웨어 점검 }
  - { id: result, title: 중단 판단과 남은 범위 }
  - { id: competency, title: 디버깅 역량 }
---

## 원시 데이터 미수신과 보드 발열 {#symptom}

IWR6843의 원시 ADC 데이터를 PC로 받기 위해 DCA1000EVM을 연결했다. Wireshark에서는
PC와 보드 사이의 짧은 제어 UDP가 보였지만 raw capture log의 수신 packet은 0이었고,
보드 발열도 함께 나타났다. 이때 코드부터 바꾸면 설정 문제와 하드웨어 문제를 섞어 볼
가능성이 컸다. 먼저 실제 장비 상태를 남기고, 데이터가 지나가는 경로와 장치를 시작시키는
경로를 따로 따라갔다.

이 글에는 제공된 화면 가운데 내용이 완전히 같은 복사본 2장을 한 번씩만 표시하고,
서로 다른 디버깅 화면 33장을 단계별 본문에 모두 배치했다. 각 화면은 누르면 원본 크기로
확대된다.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/dca1000-setup.webp' | relative_url }}" alt="DCA1000EVM 위에 IWR6843ISK를 연결하고 전원, USB와 보드 간 케이블을 연결한 실험 구성" width="1200" height="1200"><figcaption>IWR6843ISK, DCA1000EVM, 전원·USB·보드 간 연결을 한 화면에서 확인한 구성.</figcaption></figure>

## 데이터 경로와 제어 경로를 따로 봤다 {#paths}

TI 문서의 raw mode를 기준으로 데이터 경로는 `IWR6843 ADC → LVDS → DCA1000 FPGA
→ DDR3L/packet path → Ethernet → PC`로 놓았다. 한편 장치가 이 경로를 열기까지는
전원 선택, switch와 동작 모드, FTDI·RS232·SPI 연결, reset, FPGA configuration과
capture start 순서가 필요하다. 데이터가 안 보인다는 한 증상을 두 경로로 나누니 확인할
지점이 명확해졌다.

<figure><img src="{{ '/assets/images/study/mmwave/evm-dca1000-flow.svg' | relative_url }}" alt="Radar EVM의 제어 UART와 원시 LVDS 데이터가 DCA1000과 PC로 이어지는 경로" width="1200" height="675"><figcaption>설정이 오가는 제어 경로와 원시 샘플이 이동하는 LVDS·Ethernet 경로는 같은 문제가 아니다.</figcaption></figure>

{% include dca-debug-gallery.html group="reference" %}

```text
Data path   : IWR6843 raw ADC -> LVDS -> FPGA/buffer -> Ethernet -> PC
Control path: power/mode -> FTDI/RS232/SPI -> reset/config -> capture start
```

## GUI 상태를 첫 관측점으로 삼았다 {#observations}

mmWave Studio 화면에서는 FTDI가 `Connected`였지만 장치 검출 수는 0이었고 RS232와
SPI는 `Disconnected`로 표시됐다. RF Power-up 단계에서 `ReadRegister failed with
error -11`도 확인했다. 즉 PC가 FTDI 장치를 보는 상태와 레이더 제어 통신이 성립한
상태를 같은 것으로 판단할 수 없었다.

```text
Error        : no raw ADC stream, device count 0, ReadRegister -11
Cause scope  : mode/configuration, interconnect, power, LVDS/FPGA/buffer, Ethernet
Verification : GUI state, LED labels, connector/solder inspection, oscilloscope probes
```

{% include dca-debug-gallery.html group="studio" %}

## Wireshark로 제어 UDP와 원시 데이터를 구분했다 {#wireshark}

PC의 고정 IP는 `192.168.33.30`, DCA1000EVM은 `192.168.33.180`으로 두고
`udp.port == 4096 || udp.port == 4098` 필터로 패킷을 확인했다. 화면에는 PC에서
보드의 configuration port 4096으로 향하는 길이 8·14 byte의 짧은 UDP가 반복해서
나타났다. 이는 제어 패킷이 NIC를 나갔다는 증거이지, LVDS raw sample이 Ethernet data
packet으로 돌아왔다는 증거는 아니다.

{% include dca-debug-gallery.html group="network" %}

## UniFlash로 펌웨어 기록 단계를 분리했다 {#uniflash}

UniFlash에서는 COM7의 IWR6843 대상으로 SFLASH erase와 `META_IMAGE1` download를
수행했다. console에 `Erase storage completed successfully`, `downloaded successfully
to SFLASH`, `Program Load completed successfully`가 남았다. 따라서 펌웨어 기록 단계는
성공한 관측으로 분리했다. 다만 flash 성공은 이후의 RF 설정, LVDS 출력 enable,
DCA1000 packetization과 raw capture 성공을 보장하지 않는다.

{% include dca-debug-gallery.html group="firmware" %}

## Tera Term으로 UART CLI 응답을 확인했다 {#teraterm}

Tera Term의 COM7에는 `mmwDemo:/>` prompt가 나타났지만 여러 입력 뒤에 `is not
recognized as a CLI command`가 반복됐다. 이는 serial port에서 firmware prompt를 읽을
수 있었다는 관측과, 해당 입력이 유효한 CLI command로 처리되지 않았다는 관측을 동시에
남긴다. command spelling·line ending·실행 image와 CLI state를 후보로 두되, 이 화면만으로
하나의 원인을 확정하지 않았다.

{% include dca-debug-gallery.html group="cli" %}

## Capture log로 종료 조건을 확인했다 {#capture-log}

record directory에는 configuration과 log file이 생성됐지만 raw `.bin`은 보이지 않았다.
log에는 `Number of received packets - 0`, first·last packet ID 0, duration -2 sec가
기록됐다. 이 값을 최종 판정 근거로 삼아 “Ethernet adapter가 보인다”나 “제어 packet이
있다”를 raw ADC 수집 성공으로 올려 쓰지 않았다.

{% include dca-debug-gallery.html group="capture" %}

## LED와 전원 상태를 하드웨어 관측점으로 삼았다

보드 사진에서는 여러 상태 LED가 동시에 켜진 순간을 확인했다. LED 한 장면만으로 FPGA,
DDR 또는 LVDS 고장을 확정하지 않고, 설정·시작 순서가 맞지 않아 나타난 표시일 가능성도
남겨 두었다. 발열 역시 위치와 온도를 정량화한 값이 없었으므로 고장 부품을 지목하는
근거로 사용하지 않았다.

<figure><img src="{{ '/assets/images/projects/mmwave-visualizer/dca1000-error-leds.webp' | relative_url }}" alt="DCA1000EVM의 전원, FPGA, DDR와 LVDS 관련 상태 LED가 켜진 점검 장면" width="1200" height="1200"><figcaption>LED label과 switch 상태를 확대해 다음 측정 지점을 정한 장면.</figcaption></figure>

## 전원부터 물리 경로까지 좁혔다 {#inspection}

- 5 V 입력과 보드 전원 상태, 발열 발생 시점을 먼저 확인했다.
- DIP switch, 동작 mode, reset·configuration·capture 시작 순서를 다시 맞췄다.
- 보드 간 connector, cable 접촉과 solder joint를 살펴보고 의심 구간을 납땜 보수했다.
- 오실로스코프로 접근 가능한 전원·신호 지점의 파형을 확인했다.
- PC 측 고정 IP, UDP 제어 트래픽과 0-packet capture log를 하드웨어 확인 결과와 별도로 비교했다.

이 순서는 부품을 먼저 교체하거나 소프트웨어를 무작정 수정하는 대신, 각 단계의 입력과
출력에서 다음 경계로 신호가 넘어가는지를 확인하기 위한 것이었다.

## 복구하지 못한 결과도 종료 조건으로 남겼다 {#result}

납땜 보수와 반복 설정 뒤에도 Ethernet 원시 ADC streaming은 복구되지 않았다. 제어 UDP,
flash 성공, UART prompt는 각각 확인했지만 FPGA 내부 buffer가 정상으로 샘플을 받았는지,
특정 부품이 고장 났는지는 확정하지 못했다.
따라서 DCA1000 수집 경로 사용을 중단하고, 관측한 오류 상태·점검 위치·미확정 범위를
후속 장비 점검 항목으로 남겼다.

원시 ADC capture 실패와 TI SDK 기반 3D People Tracking 실행은 서로 다른 경로다.
후자는 dual-UART로 처리된 point cloud와 target 정보를 받은 사례이며, DCA1000의
LVDS-to-Ethernet 복구 결과로 해석하지 않았다.

## 직무에 가져가는 디버깅 역량 {#competency}

이 경험에서 얻은 핵심은 실패 현상에 곧바로 원인 이름을 붙이지 않는 방법이다. flash,
UART CLI, UDP control, raw packet count, 전원·발열, connector·solder, LVDS·buffer를
단계별 관측점으로 만들었다.
또한 “확인됨”, “가능성 있음”, “아직 측정하지 못함”을 나눠 종료 판단까지 남겼다. 이 방식은
레이더·자율주행 센서 검증, 임베디드 HW bring-up, 생산·양산 불량 분석과 선행품질에서
재현 조건과 원인 범위를 좁힐 때 그대로 활용할 수 있다.
