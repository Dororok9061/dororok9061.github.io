---
title: 설계 파일, 재실행 결과와 실제 측정을 섞지 않는 방법
title_en: How I keep design files, reruns, and physical measurements separate
description: 남아 있는 파일과 새 실행 로그, 실제 장비 측정을 프로젝트 설명에 연결한 방법.
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

예전 과제 폴더를 열면 source, 화면 캡처, 보고서, 새 실행 로그가 한곳에 섞여 있었다. 나는 파일이 있다는 이유만으로 “다시 실행했다”고 쓰지 않기로 했다. 생성 시점과 도구를 먼저 적고, 현재 환경에서 실행한 것은 명령과 새 로그를 따로 묶었다.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="Shift Register, Circular Queue, Memory-Based Driver Checker 구조의 FPGA delay logic" width="1200" height="517" loading="lazy"></picture><figcaption>구조도는 설계 차이를 설명하고, 실제 동작 확인은 regression log가 맡는다.</figcaption></figure>

## 세 종류를 나눈 기준 {#three}

첫째는 설계와 당시 화면이다. 회로, RTL, Cadence 캡처가 남아 있으면 무엇을 만들었는지 설명할 수 있다. 둘째는 새 실행이다. 도구 버전, 명령, 입력, 출력 로그가 함께 있어야 현재 환경에서 돌린 결과라고 적었다. 셋째는 장비 측정이다. 장비명, 설정, 단위와 원자료가 없으면 simulation 수치를 물리 측정으로 바꾸지 않았다.

## 프로젝트에 적용한 예 {#examples}

### FPGA Delay Logic

SystemVerilog source와 testbench를 Icarus로 실행해 Project 1의 20개 check, Project 2의 26개 equivalence check, Project 3의 3개 scenario를 확인했다. Quartus timing·power·Fmax report는 찾지 못했으므로 그 수치를 쓰지 않았다.

### FMCW Radar

분석 코드, 취득 firmware, 설정 문서와 hardware 사진을 확인했다. 논문에는 600초 동시취득과 848개 대응 beat가 보고돼 있다. Radar morphology에서 얻은 AO·AC 후보 시점을 valve의 직접 측정값이나 임상 성능으로 부르지 않았다.

### PPG-HRV

논문 초록의 AUC 0.85와 F1 0.82는 논문에 보고된 값으로 적었다. 별도 fold CSV와 섞거나 현재 환경에서 재학습한 수치처럼 쓰지 않았다.

## 수치를 쓰는 방법 {#writing}

수치 옆에는 어디서 나온 값인지 한 문장으로 붙였다. simulation pass 수, 논문 보고 지표, 장비 측정값을 서로 다른 표나 문장에 놓았다. 실행하지 않은 합성이나 장비 시험은 빈칸을 억지로 채우지 않고 다음에 필요한 report와 조건을 메모했다.

## 계속 확인할 부분 {#limits}

외부 저장소, licensed tool, 물리 장비는 나중에 사용할 수 없게 될 수 있다. 그래서 새로 실행할 때마다 기존 파일을 덮어쓰지 않고 날짜가 붙은 로그와 환경 정보를 추가한다. 이 방식은 모든 결과의 영구 재현을 보장하지 않지만, 내가 어디까지 직접 확인했는지는 다시 따라갈 수 있게 한다.
