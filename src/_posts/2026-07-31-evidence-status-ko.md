---
title: 프로젝트 결과에 SOURCE·EXECUTED·MEASURED·BLOCKED를 표시하는 기준
title_en: Criteria for SOURCE, EXECUTED, MEASURED, and BLOCKED project results
description: 자료 provenance와 별개로 source 존재, software 실행, hardware 측정, tool 차단 상태를 판정하는 기준.
date: 2026-07-31 00:10:00 +0900
updated: 2026-08-01 18:10:00 +0900
study_date: 2026-07-31
lang: ko
translation_key: evidence-status
permalink: /blog/2026/07/31/evidence-status/
alternate_url: /en/blog/2026/07/31/evidence-status/
alternate_lang: en
primary_category: portfolio-methodology
subcategory: evidence-status
series: engineering-record-provenance
series_order: 2
post_type: methodology
difficulty: beginner
study_status: published
evidence_status: SOURCE_AVAILABLE
tools: [GitHub, Icarus Verilog, GHDL, Quartus, Jekyll]
hardware: [BGT60TR13C, STM32F411, Raspberry Pi]
software_versions: []
source_materials:
  - { title: Public engineering project pages, type: portfolio-data, public_url: /projects/, file_reference: site data, pages: "", used_for: status examples }
  - { title: Security and verification policy, type: policy, public_url: /security/, file_reference: public page, pages: "", used_for: blocked and platform-limit language }
prerequisites: [source provenance]
learning_objectives: [source와 실행 구분, simulation과 measurement 구분, blocked 상태 유지]
related_projects: [fpga-delay-logic, fmcw-radar, drowsiness-monitor, ppg-hrv]
related_posts: [coursework-evidence-levels]
tags: [evidence-status, reproducibility, systemverilog, fmcw-radar]
cover_image: /assets/images/projects/fpga-architecture.webp
thumbnail: /assets/images/projects/fpga-architecture.webp
image_alt: FPGA delay logic의 세 architecture와 독립 검증 흐름
draft: false
revision_history:
  - { date: 2026-07-31, change: 최초 공개 }
  - { date: 2026-08-01, change: provenance 글과 분리하고 실제 프로젝트 판정표 추가 }
toc:
  - { id: two-axes, title: Provenance와 Status는 다른 축 }
  - { id: criteria, title: 네 상태의 판정 기준 }
  - { id: examples, title: 실제 프로젝트 예시 }
  - { id: badges, title: Badge 표시 규칙 }
  - { id: limits, title: 남아 있는 한계 }
---

## Provenance와 Status는 다른 축 {#two-axes}

Archive·Rerun·Redraw·Proposal은 자료가 어디에서 왔는지를 말한다. SOURCE·EXECUTED·MEASURED·BLOCKED는 해당 주장까지 무엇을 확인했는지를 말한다. 예를 들어 과거 Cadence 화면은 `Existing Archive + SOURCE AVAILABLE`일 수 있고, Icarus regression log는 `Rerun + EXECUTED`일 수 있다.

두 축을 분리하면 “source가 있으니 실행됐다”거나 “사진이 있으니 성능을 측정했다”는 점프를 막을 수 있다.

## 네 상태의 판정 기준 {#criteria}

| Status | 최소 근거 | 대표 질문 |
|---|---|---|
| SOURCE AVAILABLE | 공개 source, 문서, 입력 설명 | 무엇을 검토하거나 재현할 수 있는가? |
| EXECUTED | 환경, 명령·절차, 관찰 결과 | 명시한 조건에서 실제로 실행했는가? |
| MEASURED | 장비·조건·단위·결과·원자료 경계 | 물리량 또는 성능을 실제로 측정했는가? |
| BLOCKED | 필요한 도구·원본·권한과 실패 이유 | 무엇이 없어서 판정을 멈췄는가? |

`BLOCKED`는 실패를 숨기는 상태가 아니다. Quartus report가 없으면 timing·power·Fmax를 비워 두고 필요한 report를 적는다. GitHub Pages에서 설정할 수 없는 header는 `PLATFORM LIMITATION`으로 분리한다.

## 실제 프로젝트 예시 {#examples}

### FPGA Delay Logic

Public SystemVerilog source와 testbench가 있고 Icarus regression에서 Project 1의 20 checks, Project 2의 26 equivalence checks, Project 3의 3 scenarios가 실행됐다. 따라서 functional simulation은 EXECUTED다. Quartus synthesis, timing, power, Fmax, numerical PPA는 report가 없어 BLOCKED다.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="Shift Register, Circular Queue, Memory-Based Driver Checker 구조의 FPGA delay logic" width="1200" height="517" loading="lazy"></picture><figcaption>구조도는 설계 설명 근거다. 실행 판정은 별도 regression log에 연결한다.</figcaption></figure>

### FMCW Radar Cardiac Timing

분석 source, acquisition firmware, 설정 문서와 privacy-reviewed hardware 사진은 SOURCE + HARDWARE를 지원한다. 논문 보고 기준 600초 동시취득과 848개 대응 beat가 있다. 다만 AO·AC는 radar morphology에서 얻은 candidate timing이며, echo·ICG·PCG 독립 reference가 없는 상태에서 direct valve measurement나 임상 성능으로 표시하지 않는다.

### Two-node Drowsiness Monitor

C/C++ source, TCP/IP·file IPC·GPIO·I2C 경로, 실제 prototype 사진은 통합 존재를 지원한다. latency, sensitivity, specificity, false-alarm rate 측정 근거는 없어 수치 badge를 만들지 않는다.

### PPG-HRV Cognitive Load

논문 Abstract가 보고한 AUC 0.85와 F1 0.82는 `PAPER_REPORTED`다. 별도 fold CSV의 평가 조건과 합치지 않는다. 논문 수치는 존재하지만 현재 환경 재학습 결과라고 부르지 않는다.

## Badge 표시 규칙 {#badges}

- Badge는 가장 강한 상태 하나로 전체 프로젝트를 덮지 않는다.
- 기능 simulation, synthesis, hardware measurement를 항목별로 나눈다.
- 논문 수치는 `PAPER_REPORTED` 출처를 붙인다.
- BLOCKED 항목은 필요한 도구·report·reference를 함께 표시한다.
- `PASS`는 실제 검사 또는 실행 결과가 있을 때만 사용한다.

## 남아 있는 한계 {#limits}

이 기준은 공개 근거를 읽기 쉽게 만드는 기록 체계이지 완전한 재현성 보증이 아니다. 외부 repository가 변경되거나 원본 장비·license가 사라지면 재실행이 막힐 수 있다. 상태를 갱신할 때는 기존 증거를 지우지 않고 날짜와 검증 방법을 추가한다.
