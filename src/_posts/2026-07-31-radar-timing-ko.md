---
title: ECG 기준 Beat Alignment에서 Radar AO·AC 후보 시점을 해석한 범위
title_en: Interpretation boundary for radar AO/AC candidates after ECG-anchored beat alignment
description: ECG R-peak, SCG reference, FMCW phase morphology와 직접 판막 측정의 차이를 실제 BGT60TR13C 연구 흐름으로 정리한 기록.
date: 2026-07-31 00:30:00 +0900
updated: 2026-08-01 18:50:00 +0900
study_date: 2026-07-31
lang: ko
translation_key: radar-candidate-timing
permalink: /blog/2026/07/31/radar-candidate-timing/
alternate_url: /en/blog/2026/07/31/radar-candidate-timing/
alternate_lang: en
primary_category: rf-radar-signal
subcategory: ecg-scg-radar
series: fmcw-radar-signal-processing
series_order: 4
post_type: paper-review
difficulty: advanced
study_status: published
evidence_status: SOURCE_HARDWARE_AND_PAPER_REPORTED
tools: [Python, NumPy, SciPy]
hardware: [BGT60TR13C, STM32F411, ESP-32S, MPU6050]
software_versions: [not fully preserved]
source_materials:
  - { title: FMCW Radar AOAC Cardiac Analysis, type: public-repository, public_url: https://github.com/Dororok9061/fmcw-radar-aoac-cardiac-analysis, file_reference: analysis source and firmware, pages: "", used_for: signal flow and candidate timing boundary }
  - { title: FMCW Radar Cardiac Timing project, type: portfolio-page, public_url: /projects/fmcw-radar/, file_reference: public project data, pages: "", used_for: hardware and reported acquisition summary }
prerequisites: [fmcw-radar, phase-processing, ecg-r-peak]
learning_objectives: [ECG anchor로 multimodal beat 정렬, SCG reference와 radar morphology 구분, candidate timing 한계 기록]
related_projects: [fmcw-radar]
related_posts: []
tags: [fmcw-radar, beat-alignment, phase-processing, biomedical-signal]
cover_image: /assets/images/projects/radar-hardware.webp
thumbnail: /assets/images/projects/radar-hardware.webp
image_alt: ECG, SCG와 BGT60TR13C FMCW Radar를 동시 취득한 실제 하드웨어 구성
draft: false
revision_history:
  - { date: 2026-07-31, change: 최초 공개 }
  - { date: 2026-08-01, change: "acquisition architecture, phase·beat 과정, hardware와 waveform 근거 추가" }
toc:
  - { id: setup, title: 동시취득 System }
  - { id: phase, title: Radar Phase에서 Beat까지 }
  - { id: alignment, title: ECG R-peak 기준 Alignment }
  - { id: candidates, title: AO·AC Candidate Timing }
  - { id: evidence, title: 확인한 결과와 한계 }
  - { id: next, title: 다음 Validation }
---

## 동시취득 System {#setup}

연구 흐름은 ECG, SCG, FMCW Radar를 같은 시간 구간에서 취득한 뒤 ECG R-peak를 공통 anchor로 사용한다. Radar는 BGT60TR13C를 사용하고, STM32F411·ESP-32S·MPU6050가 acquisition과 reference signal 경로에 포함된다.

<figure><picture><source srcset="/assets/images/projects/radar-hardware.webp" type="image/webp"><img src="/assets/images/projects/radar-hardware.jpg" alt="ECG 전극, SCG sensor, BGT60TR13C Radar와 acquisition board를 배치한 실제 실험 구성" width="1200" height="800" loading="lazy"></picture><figcaption>개인정보 검토를 거친 ECG·SCG·Radar 동시취득 hardware. 사진은 구성 존재를 지원하지만 성능 측정표는 아니다.</figcaption></figure>

시간축이 어긋나면 같은 심박의 ECG, SCG, Radar morphology를 비교할 수 없다. 각 stream의 timestamp, sample rate, 시작 offset과 누락 sample 처리가 먼저 확인돼야 한다.

## Radar Phase에서 Beat까지 {#phase}

FMCW chirp에서 range FFT를 계산하고 흉부 반사 성분이 있는 range bin 또는 ROI를 선택한다. 선택한 complex sample의 phase를 unwrap하고 파장에 따른 displacement scale로 바꾸면 흉부 미세변위와 관련된 waveform을 얻을 수 있다.

ROI가 움직이거나 respiration 성분이 커지면 cardiac morphology가 바뀔 수 있다. 따라서 ROI selection, phase unwrap discontinuity, filtering, motion rejection을 candidate timing의 입력 조건으로 기록한다. 그래프의 peak 하나만 보고 valve event를 확정하지 않는다.

## ECG R-peak 기준 Alignment {#alignment}

<figure><picture><source srcset="/assets/images/projects/fmcw-waveform.webp" type="image/webp"><img src="/assets/images/projects/fmcw-waveform.jpg" alt="공통 시간축에 정렬한 ECG, SCG, FMCW Radar cardiac waveform" width="1011" height="642" loading="lazy"></picture><figcaption>ECG R-peak를 기준으로 SCG와 Radar waveform을 beat-relative axis에 배치한 예시.</figcaption></figure>

ECG R-peak index를 기준으로 앞뒤 window를 잘라 beat를 만든다. 동일 beat에서 SCG reference timing과 Radar morphology를 비교한다. Beat length가 다르면 resampling 또는 정규화 방식이 결과를 바꿀 수 있으므로 원 sample index와 변환된 beat axis를 함께 보존해야 한다.

논문에는 **600초 동시취득**과 **848개 대응 beat 분석**을 적었다. 이번 글에서도 그 수치를 논문 결과로 표시하고, 새로 다시 실행한 값처럼 바꾸지 않았다.

## AO·AC Candidate Timing {#candidates}

SCG에서 AO와 AC 관련 reference point를 구성하고, Radar waveform의 peak·slope change·detector fusion 결과 중 시간적으로 대응하는 지점을 찾는다. Signal Quality Index가 낮거나 detector가 불일치하는 beat는 별도로 처리해야 한다. Candidate Timing Interval(CTI)은 선택된 지점의 분포를 요약한다.

여기서 `AO`와 `AC` 표기는 **morphology-based candidate timing**이다. Radar가 대동맥판을 영상화한 것이 아니며, Doppler echo로 판막 개폐를 직접 확인한 것도 아니다. SCG reference와 ECG anchor에 시간적으로 대응하는 후보라는 뜻으로 제한한다.

## 확인한 결과와 한계 {#evidence}

<figure><picture><source srcset="/assets/images/projects/fmcw-experiment.webp" type="image/webp"><img src="/assets/images/projects/fmcw-experiment.jpg" alt="STM32 board, ECG electrode와 FMCW Radar가 포함된 동시취득 실험 사진" width="1000" height="1000" loading="lazy"></picture><figcaption>실험 구성과 acquisition 경로의 hardware evidence.</figcaption></figure>

남아 있는 analysis source, firmware, 설정 문서와 사진으로 실험 경로를 다시 확인했다. 600초 acquisition과 848 corresponding beats는 논문에 보고한 값이다. 임상 sensitivity·specificity와 direct valve detection은 이 실험에서 측정한 항목이 아니다.

## 다음 Validation {#next}

후보 시점을 해부학적 event에 더 가깝게 검증하려면 동기화된 echocardiography, ICG 또는 PCG 같은 독립 reference가 필요하다. Protocol에는 clock synchronization error, annotator rule, beat exclusion, inter-rater agreement와 Bland–Altman 또는 timing-error 분석을 포함해야 한다. 그 전까지 candidate라는 표현을 유지한다.
