---
title: 68030·Z80 하드웨어에서 레거시-현대 Bridge까지
title_en: From 68030 and Z80 Hardware to a Legacy-Modern Bridge
description: Macintosh Color Classic과 Olympic-S를 CPU·메모리·버스·RGBS·카세트·SCSI 계층으로 분석하고 계측 전 확인할 경계를 정리한 기록.
date: 2026-09-08 18:10:00 +0900
updated: 2026-09-08 18:10:00 +0900
lang: ko
translation_key: legacy-embedded-system-interfaces
permalink: /blog/2026/09/08/legacy-embedded-system-interfaces/
alternate_url: /en/blog/2026/09/08/legacy-embedded-system-interfaces/
alternate_lang: en
primary_category: major-foundations
subcategory: embedded-systems
series: legacy-embedded-systems
series_order: 1
post_type: project-log
practical: true
difficulty: advanced
study_status: published
evidence_status: HARDWARE_MANUAL_ANALYSIS
tools: [MC68030, Z80, RGBS, SCSI, BlueSCSI, Raspberry Pi]
hardware: [Macintosh Color Classic, Olympic-S, vintage CRT, National RQ-8050]
software_versions: [Classic Mac OS System 7.5.1]
source_materials:
  - { title: Legacy Embedded System Architecture and Mixed-Signal Interface Research, type: source-portfolio, public_url: "https://github.com/Dororok9061/dororok9061.github.io/tree/main/project-archives/legacy-embedded-system", file_reference: 23-page technical portfolio PDF, pages: "1-23", used_for: architecture interface evidence and test boundaries }
  - { title: Macintosh Color Classic Technical Specifications, type: vendor-documentation, public_url: "https://support.apple.com/en-la/112200", file_reference: Apple Support, pages: "", used_for: processor memory video and interface specifications }
  - { title: BlueSCSI Toolbox and Wi-Fi DaynaPORT, type: project-documentation, public_url: "https://bluescsi.com/docs/Toolbox", file_reference: BlueSCSI documentation, pages: "", used_for: shared-folder and SCSI bridge architecture }
  - { title: Olympic-S operation manual scan, type: source-manual, public_url: "https://oldcrap.org/wp-content/uploads/2024/09/olympic-s-manual.pdf", file_reference: scanned manual, pages: "", used_for: memory cassette RGBS and expansion-interface specifications }
prerequisites: [computer-architecture, digital-interfaces, analog-signals]
learning_objectives: [분산형 보드 아키텍처 읽기, mixed-signal interface requirement 정의, 증거 수준 분리, legacy-modern bridge 검증 계획]
related_projects: [legacy-embedded-system]
related_posts: [embedded-data-path, pads-footprint-ppg-schematic]
tags: [legacy-computing, embedded-systems, mixed-signal, rgbs, scsi, reverse-engineering]
cover_image: /assets/images/projects/legacy-embedded-system/system-map.webp
thumbnail: /assets/images/projects/legacy-embedded-system/system-map.webp
image_alt: Olympic-S, Macintosh Color Classic, BlueSCSI와 Raspberry Pi를 연산·저장·영상·통신 계층으로 비교한 통합 시스템 표
draft: false
revision_history:
  - { date: 2026-09-08, change: 23쪽 기술 포트폴리오의 확인·추정·후속 측정 범위를 분리해 최초 공개 }
toc:
  - { id: question, title: 수집품을 실험 플랫폼으로 바꾼 질문 }
  - { id: architecture, title: 68030과 Z80 보드 읽기 }
  - { id: interfaces, title: RGBS·카세트·SCSI }
  - { id: bridge, title: 레거시-현대 Bridge }
  - { id: evidence, title: 증거 등급과 검증 계획 }
  - { id: value, title: 현대 직무로 번역되는 역량 }
  - { id: boundary, title: 완료 범위와 다음 계측 }
---

## 수집품을 실험 플랫폼으로 바꾼 질문 {#question}

빈티지 컴퓨터를 켜 보는 데서 끝내지 않고, 세대가 다른 임베디드 시스템의
아키텍처와 신호를 비교하는 실험 플랫폼으로 다시 읽었다. Macintosh Color
Classic은 68030 기반 32-bit 시스템이고, Olympic-S는 Z80 계열 CPU와 RAM·ROM,
TTL/glue logic이 PCB 위에 분산된 8-bit 시스템이다. 두 장비 사이에는 저장장치,
영상, 통신 방식뿐 아니라 전압·동기·종단에 대한 전제가 다르다.

핵심 질문은 “어떤 케이블이 꽂히는가”가 아니라 “어떤 신호가 어느 기준 전위와
level로 이동하며, 무엇을 연결 전에 측정해야 하는가”였다. 그래서 PCB marking,
OS 화면, 원문 매뉴얼, 기능 이력을 같은 표에 넣고 확인 수준을 따로 표시했다.

## 68030과 Z80 보드 읽기 {#architecture}

Color Classic에서는 MC68030FE16B, onboard DRAM과 30-pin SIMM, VRAM module,
Apple/VLSI custom ASIC, Zilog SCC 계열 serial controller와 accelerator board를
기능 블록으로 나눴다. System 7.5.1의 10,240K 표시는 사진에서 직접 확인했다.
VRAM module은 보이지만 총량은 diagnostic capture가 없으므로 512 KB라고
확정하지 않았다.

Olympic-S에서는 Z80-compatible CPU, 48 KB RAM, 16 KB ROM, 대량의 DIP TTL,
speaker와 64-contact connector를 대응시켰다. 현대 MCU/SoC 내부에 들어간 address
decode, display timing, mux와 glue logic이 PCB 위에 분리돼 있어 address·data·control
bus를 logic analyzer로 따라갈 수 있는 구조다.

<figure><picture><source srcset="/assets/images/projects/legacy-embedded-system/system-map.webp" type="image/webp"><img src="/assets/images/projects/legacy-embedded-system/system-map.jpg" alt="Olympic-S Z80과 Color Classic 68030을 현대 Raspberry Pi·BlueSCSI 계층과 비교한 표" width="1180" height="790" loading="lazy"></picture><figcaption>연산·메모리·저장·영상·통신을 같은 layer로 맞춰 본 통합 시스템 지도. 표의 현대 확장은 설계안이며 구현 완료 결과가 아니다.</figcaption></figure>

## RGBS·카세트·SCSI {#interfaces}

Olympic-S의 CTV DIN-5는 원문 매뉴얼에서 Sync, Ground, Green, Blue, Red로 확인했다.
따라서 composite나 RF 입력만 있는 TV는 직결 대상이 아니다. RGB와 외부 sync를
받는 monitor가 가장 단순하지만, pin 기능이 맞아도 amplitude, polarity, common,
75 Ω termination을 오실로스코프와 멀티미터로 확인한 뒤 연결해야 한다.

<figure><picture><source srcset="/assets/images/projects/legacy-embedded-system/rgbs-interface.webp" type="image/webp"><img src="/assets/images/projects/legacy-embedded-system/rgbs-interface.jpg" alt="Olympic-S RGBS 신호와 DIN-5 pinout, RGB monitor 또는 변환 경로를 나타낸 도식" width="1180" height="640" loading="lazy"></picture><figcaption>화면 크기보다 먼저 input topology와 전기 조건을 확인하도록 바꾼 RGBS 검증 흐름.</figcaption></figure>

카세트 경로는 1200 bit/s digital data를 audio-frequency waveform으로 바꿔 기록하고,
재생 시 analog front end와 comparator를 거쳐 pulse로 복원하는 mixed-signal interface다.
National RQ-8050 기준으로 LOAD는 recorder CMT OUT에서 computer tape input으로,
SAVE는 computer tape output에서 recorder CMT IN으로 향한다. 이 방향은 문서로
정리했지만 실제 round-trip은 아직 남아 있다.

Color Classic의 SCSI는 BlueSCSI를 통해 SD card disk image와 `/shared` file path로
확장할 수 있다. ADB는 keyboard/mouse HMI, RS-422 serial은 외부 계측·bridge 후보로
분류했다. 동일한 “외부 포트”라도 storage, HMI, serial instrumentation의 역할이
서로 다르므로 한 개의 I/O 목록으로 뭉치지 않았다.

## 레거시-현대 Bridge {#bridge}

설계한 첫 번째 경로는 현대 PC 또는 Raspberry Pi에서 만든 파일을 SD와 BlueSCSI를
통해 SCSI bus로 보내고, Color Classic을 결과 표시 HMI로 쓰는 구조다.

```text
Modern PC / Raspberry Pi → SD / BlueSCSI → SCSI bus → Color Classic GUI
```

두 번째 경로는 Classic Mac에서 입력한 power rail·BOM·trace-length constraint를
Raspberry Pi Python backend가 KiCad CSV/netlist와 대조하고 PASS/WARN/ERROR를
되돌려주는 engineering frontend다. BGA fanout, differential routing과 DRC는 현대
EDA가 담당하고, Mac은 입력·검사 실행·report 확인을 맡는다. 계산 엔진과 HMI를
분리했기 때문에 레거시 장비의 역할을 과장하지 않으면서 실제 시스템 통합 문제로
확장할 수 있다.

## 증거 등급과 검증 계획 {#evidence}

분석 결과는 다섯 등급으로 나눴다. 장비·화면·PCB에서 직접 확인한 것은 A,
반복 사용이나 교차 장비 기능 확인은 B, 원문 매뉴얼·제조사 사양은 C, 사진과
세대 정보에 근거한 추정은 D, 오실로스코프·멀티미터 측정이 필요한 것은 E다.

<figure><picture><source srcset="/assets/images/projects/legacy-embedded-system/evidence-levels.webp" type="image/webp"><img src="/assets/images/projects/legacy-embedded-system/evidence-levels.jpg" alt="직접 확인부터 후속 측정까지 다섯 단계로 구분한 증거 표" width="1180" height="610" loading="lazy"></picture><figcaption>사진상 보임과 전기적 확인을 분리해 과도한 단정을 막는 evidence matrix.</figcaption></figure>

이 분류를 적용하면 판매자가 CRT에 정상 화면을 출력한 사진은 “특정 연결이
동작했다”는 근거이지만, pinout과 signal level을 동일하게 재현했다는 증거는 아니다.
반대로 Color Classic의 10,240K 표시는 사용자 화면에서 직접 확인했으므로 사진
근거로 명확히 남길 수 있다.

## 현대 직무로 번역되는 역량 {#value}

이 작업에서 드러나는 핵심은 오래된 부품 지식 자체보다 검증 가능한 경계를 만드는
능력이다. PCB에서 compute·memory·glue logic·connector를 기능 블록으로 분리하고,
매뉴얼 사양을 physical interface requirement로 바꾸고, 연결 전에 continuity,
level, polarity, termination, ripple을 시험 항목으로 만들었다.

이 방식은 embedded HW bring-up, 차량 HMI와 gateway 검증, 방산 장비의 legacy
interface 연동, 생산기술의 입출력 검사 순서, 선행품질의 확인·추정·미검증 분리와
직접 연결된다. 특정 산업 규격 시험을 수행했다고 주장하는 것이 아니라, 서로 다른
전원·통신·표시 장치를 연결할 때 필요한 요구도 정의와 evidence-based test planning을
보여준다.

## 완료 범위와 다음 계측 {#boundary}

현재 완료된 것은 Color Classic의 부팅·메모리 표시, 주요 chip mapping, Olympic-S
매뉴얼과 PCB 사진의 architecture mapping, RGBS pin 기능, cassette I/O 방향과
BlueSCSI bridge 구조 정리다. 다음 단계는 다음 네 가지다.

1. CTV cable continuity map과 R/G/B/Sync amplitude·polarity·impedance 측정
2. known-good cassette를 사용한 RQ-8050 SAVE/LOAD round-trip
3. Color Classic → BlueSCSI/Pico-W → Raspberry Pi TCP echo test
4. KiCad CSV checker 결과를 Classic Mac GUI에 표시하는 최소 기능 구현

이 계측과 구현이 끝나기 전에는 RGBS 전기 호환, 카세트 저장 재현, DaynaPORT 연결,
engineering frontend를 완료 결과로 쓰지 않는다. 분석과 계획을 공개하되, 측정된
성과와 다음 실험을 분리하는 것이 이 프로젝트의 가장 중요한 문서화 원칙이다.
