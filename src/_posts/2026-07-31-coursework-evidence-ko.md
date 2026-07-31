---
title: 전공 프로젝트 결과를 기록할 때 Archive·Rerun·Redraw·Proposal을 구분한 기준
title_en: Separating Archive, Rerun, Redraw, and Proposal in coursework records
description: Vivado·GHDL·PSIM·Python·Cadence·PowerWorld·AESA-SAR 사례를 같은 결과처럼 표시하지 않는 기록 기준.
date: 2026-07-31 01:00:00 +0900
updated: 2026-08-01 18:00:00 +0900
study_date: 2026-07-31
lang: ko
translation_key: coursework-evidence-levels
permalink: /blog/2026/07/31/coursework-evidence-levels/
alternate_url: /en/blog/2026/07/31/coursework-evidence-levels/
alternate_lang: en
primary_category: portfolio-methodology
subcategory: source-provenance
series: engineering-record-provenance
series_order: 1
post_type: methodology
difficulty: beginner
study_status: published
evidence_status: SOURCE_DERIVED
tools: [Vivado, GHDL, PSIM, Python, Cadence Virtuoso, PowerWorld]
hardware: []
software_versions: [GHDL version recorded in coursework repository]
source_materials:
  - title: Electrical Engineering Coursework Portfolio
    type: public-project
    public_url: https://tontonjeong.github.io/electrical-engineering-coursework-portfolio/
    file_reference: public repository only
    pages: ""
    used_for: 과목별 결과와 evidence state 비교
  - title: Coursework project page
    type: portfolio-page
    public_url: /projects/coursework/
    file_reference: site data
    pages: ""
    used_for: 공개 경계와 관련 프로젝트 연결
prerequisites: [source provenance, reproducibility]
learning_objectives: [과거 archive와 재실행 결과 구분, 재작성 그림과 측정 결과 구분, proposal 공개 경계 기록]
related_projects: [coursework]
related_posts: [evidence-status]
tags: [source-provenance, ghdl, cadence, powerworld]
cover_image: /assets/images/projects/coursework-hero.webp
thumbnail: /assets/images/projects/coursework-hero.webp
image_alt: VHDL, 전력, 제어, RF, 센서 과제를 evidence 상태별로 묶은 Coursework 구조도
draft: false
revision_history:
  - date: 2026-07-31
    change: 최초 공개
  - date: 2026-08-01
    change: 과목별 사례, 판단표, 공개 절차와 실제 시각자료를 추가
toc:
  - { id: why, title: 이 기준을 만든 이유, title_en: Why this distinction exists }
  - { id: definitions, title: 네 상태의 정의, title_en: Four provenance states }
  - { id: cases, title: 실제 과목별 사례, title_en: Coursework cases }
  - { id: workflow, title: 공개 판단 절차, title_en: Publication workflow }
  - { id: template, title: 기록 Template, title_en: Record template }
  - { id: limits, title: 확인하지 못한 내용, title_en: Unverified items }
---

## 이 기준을 만든 이유 {#why}

전공과목 폴더에는 서로 다른 시점과 환경에서 만든 자료가 함께 남습니다. Vivado 파형은 당시 화면만 있고, VHDL source는 GHDL로 다시 실행할 수 있으며, Cadence 결과는 기존 archive 화면만 남아 있을 수 있습니다. 보고서의 계산식을 Python으로 다시 계산한 결과와 직접 계측한 값도 같은 종류가 아닙니다.

파일이 존재한다는 이유만으로 모두 “실험 완료”라고 표시하면 독자는 재현 가능한 범위를 판단할 수 없습니다. 그래서 자료의 출처를 먼저 분류하고, 실행·측정 상태는 별도의 Evidence Status로 기록합니다.

<figure>
  <picture><source srcset="/assets/images/projects/coursework-hero.webp" type="image/webp"><img src="/assets/images/projects/coursework-hero.jpg" alt="VHDL, Power, Control, RF, Sensor Systems를 evidence 상태와 함께 연결한 전공과목 포트폴리오 구조도" width="1200" height="570" loading="lazy"></picture>
  <figcaption>분야는 내용 분류이고 Archive·Rerun·Redraw·Proposal은 자료 provenance다. 둘을 한 badge로 합치지 않는다.</figcaption>
</figure>

## 네 상태의 정의 {#definitions}

| 상태 | 필요한 근거 | 표시할 수 있는 내용 | 표시하면 안 되는 내용 |
|---|---|---|---|
| Existing Archive | 당시 파일·화면과 생성 맥락 | 과거 환경에서 존재했던 결과 | 현재 환경 재현 PASS |
| Rerun | 명령, 도구 버전, 새 로그 | 다시 실행해 확인한 결과 | 실행하지 않은 합성·측정 |
| Portfolio Redraw | 원본 수치·구조와 재작성 규칙 | 설명을 위한 새 구조도 | 원본 계측 화면 또는 새 측정 |
| Proposal | 문제·요구·설계안 | 구현 전 설계 의도 | 구현·성능·현장 검증 |

이 표는 성능 등급이 아니다. Archive가 Rerun보다 “낮다”는 뜻도 아니다. 독자가 어떤 자료부터 재현할 수 있는지를 알려주는 출처 분류다.

## 실제 과목별 사례 {#cases}

- **Vivado 기존 파형**: 당시 캡처는 Existing Archive다. HDL source와 실행 script가 함께 있어도 동일 Vivado 환경에서 새 로그를 만들기 전에는 Rerun으로 바꾸지 않는다.
- **GHDL 재실행**: 공개 repository에서 testbench를 실행하고 PASS 로그를 얻은 항목만 Rerun이다. 원래 Vivado 화면까지 새로 검증했다는 의미는 아니다.
- **PSIM 결과**: 과제 파일과 화면이 남아 있지만 현재 환경에서 다시 실행하지 않은 항목은 Existing Archive다.
- **Python 독립 재계산**: 보고서의 식과 입력값을 독립 코드로 계산한 결과다. 계산 검산은 지원하지만 실제 hardware measurement를 대신하지 않는다.
- **Cadence S-parameter**: 기존 Wilkinson·Branch-Line 결과 화면은 Existing Cadence Archive로 표시한다. 새 simulation이나 VNA 측정이라고 부르지 않는다.
- **PowerWorld Non-Convergence**: 수렴 실패 자체가 중요한 결과일 수 있다. 실패 조건과 설정이 남아 있으면 troubleshooting evidence이며, 정상 power-flow 결과로 바꾸지 않는다.
- **AESA-SAR 설계안**: 요구와 trade-off를 정리한 Proposal이다. 구현 가능한 체계 제원이나 실제 운용 성능으로 확장하지 않는다.

## 공개 판단 절차 {#workflow}

1. 원본 파일의 소유권, 개인정보, license, 강의자료 공개 가능성을 확인한다.
2. 생성 도구와 시점을 알 수 있으면 Existing Archive로 기록한다.
3. 새 실행을 했다면 명령·version·입력·log를 묶고 Rerun으로 기록한다.
4. 설명용 그림은 원 수치와 재작성 규칙을 남기고 Portfolio Redraw로 표시한다.
5. 구현·실행 자료가 없으면 Proposal에서 멈춘다.
6. Source, Executed, Measured, BLOCKED 상태는 별도 축에서 판단한다.

이 순서를 적용하면 직접 asset URL로 접근하더라도 파일만 보고 새 실험으로 오해할 가능성이 줄어든다. 공개할 수 없는 원본은 repository에 넣지 않고 요약과 경계만 남긴다.

## 기록 Template {#template}

```text
Item:
Domain:
Provenance: Existing Archive | Rerun | Portfolio Redraw | Proposal
Source owner:
Tool and version:
Input:
Command or procedure:
Observed result:
Not verified:
Public asset:
Related project:
```

결과 한 줄보다 `Not verified`가 중요할 때가 많다. 예를 들어 GHDL functional test를 통과했더라도 Quartus timing, power, Fmax는 보고서가 없으면 BLOCKED로 남긴다.

## 확인하지 못한 내용 {#limits}

현재 공개 근거는 모든 Cadence·PSIM·PowerWorld 과제를 최신 버전에서 재실행했다는 것을 지원하지 않는다. 새 VNA 측정, production-grid validation, AESA-SAR 구현도 주장하지 않는다. 자료가 추가되면 원본을 바꾸지 않고 새 실행 묶음을 만들어 상태를 갱신한다.

[전공과목 프로젝트 전체 보기](/projects/coursework/)
