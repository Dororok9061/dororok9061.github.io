---
title: 설계 파일, 재실행 결과와 실제 측정을 섞지 않는 방법
title_en: How I keep design files, reruns, and physical measurements separate
description: 남아 있는 파일과 새 실행 로그, 실제 장비 측정을 프로젝트 설명에 연결한 방법.
date: 2026-07-31 00:10:00 +0900
updated: 2026-09-17 12:00:00 +0900
study_date: 2026-07-31
lang: ko
translation_key: evidence-status
permalink: /blog/2026/07/31/evidence-status/
alternate_url: /en/blog/2026/07/31/evidence-status/
alternate_lang: en
primary_category: portfolio-methodology
subcategory: evidence-status
series: engineering-record-lineage
series_order: 2
post_type: methodology
difficulty: beginner
study_status: published
evidence_status: SOURCE_AVAILABLE
tools: [GitHub, Icarus Verilog, GHDL, Quartus, Jekyll]
hardware: [BGT60TR13C, STM32F411, Raspberry Pi]
software_versions: []
source_materials:
  - { title: Public engineering project pages, type: portfolio-data, public_url: /projects/, file_reference: site data, pages: "", used_for: project examples }
  - { title: Security and verification policy, type: policy, public_url: /security/, file_reference: public page, pages: "", used_for: platform limits }
prerequisites: [source provenance]
learning_objectives: [source와 실행 구분, simulation과 measurement 구분, 확인하지 못한 수치 표시]
related_projects: [fpga-delay-logic, fmcw-radar, drowsiness-monitor, ppg-hrv]
related_posts: [coursework-evidence-levels]
tags: [evidence-status, reproducibility, systemverilog, fmcw-radar]
cover_image: /assets/images/projects/fpga-architecture.webp
thumbnail: /assets/images/projects/fpga-architecture.webp
image_alt: FPGA delay logic의 세 architecture와 독립 확인 흐름
draft: false
published: false
revision_history:
  - { date: 2026-07-31, change: 최초 공개 }
  - { date: 2026-08-01, change: 상태 코드 중심 글을 실제 기록 방법 중심으로 다시 작성 }
toc:
  - { id: start, title: 파일을 찾은 뒤 먼저 한 일 }
  - { id: three, title: 세 종류를 나눈 기준 }
  - { id: examples, title: 프로젝트에 적용한 예 }
  - { id: writing, title: 수치를 쓰는 방법 }
  - { id: limits, title: 계속 확인할 부분 }
---

## 파일을 찾은 뒤 먼저 한 일 {#start}

설계 파일·저장 화면·보고서·새 실행 로그는 생성 시점과 도구 정보를 기준으로 분류한다. 실행 묶음에는 명령·입력·출력 로그를 포함한다.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="Shift Register, Circular Queue, Memory-Based Driver Checker 구조의 FPGA delay logic" width="1200" height="517" loading="lazy"></picture><figcaption>구조도는 설계 차이를 설명하고, 실제 동작 확인은 regression log가 맡는다.</figcaption></figure>

## 세 종류를 나눈 기준 {#three}

자료 유형은 세 가지다. 설계·기존 화면은 회로와 구현 구조, 재실행은 도구 버전·명령·입출력, 장비 측정은 장비명·설정·단위·원자료를 기준으로 기록한다.

## 프로젝트에 적용한 예 {#examples}

### FPGA Delay Logic

7월 Icarus 기록: Project 1의 20 checks, Project 2의 26 equivalence checks, Project 3의 3 scenarios. 평가 유형: 기능 시뮬레이션.

[9월 GTKWave·RTL·테스트벤치 실행 기록](/projects/fpga-delay-logic/#gallery)

### FMCW Radar

자료: 분석 코드·취득 firmware·설정 문서·hardware 사진. 논문 결과: 600초 동시취득·848개 대응 beat·Radar morphology 기반 AO·AC 후보 시점.

### PPG-HRV

논문 Abstract·Conclusion 지표: AUC 0.99·F1 0.992. 별도 fold CSV에는 해당 코드 실행의 평가 조건을 표기한다.

## 수치를 쓰는 방법 {#writing}

수치는 실행 로그·논문·계측 원자료의 출처와 연결한다. 후속 합성·장비 시험에는 필요한 report와 조건을 명시한다.

## 계속 확인할 부분 {#limits}

실행 이력은 날짜별 로그·도구 환경·입력 파일로 보관한다. 이전 결과를 유지하고 새 실행 자료를 추가하는 방식이다.