---
title: 3.5 GHz Microstrip에서 Wilkinson·Branch-Line까지
title_en: From a 3.5 GHz Microstrip to Wilkinson and Branch-Line Networks
description: Alumina microstrip 계산과 저장된 Cadence divider·hybrid 화면을 수치와 회로 구조로 다시 읽은 기록.
date: 2026-08-01 11:02:00 +0900
updated: 2026-08-01 11:02:00 +0900
study_date: 2026-06-14
lang: ko
translation_key: rf-passive-microstrip-divider-hybrid
permalink: /blog/2026/08/01/rf-passive-microstrip-divider-hybrid/
alternate_url: /en/blog/2026/08/01/rf-passive-microstrip-divider-hybrid/
alternate_lang: en
primary_category: rf-radar-signal
subcategory: s-parameter
series: rf-microwave
series_order: 3
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: ARCHIVED_SIMULATION_SCREENSHOTS
tools: [Cadence Virtuoso, Smith Chart]
hardware: []
software_versions: []
source_materials:
  - { title: RF and Microwave coursework report and screenshots, type: local-coursework, public_url: "", file_reference: "homework 2, 4, and 5", pages: "", used_for: dimensions and archived simulation markers }
prerequisites: [electromagnetics, transmission-line, s-parameter]
learning_objectives: [microstrip dimensions, insertion loss and phase, divider and hybrid topology]
related_projects: []
related_posts: [radar-candidate-timing]
tags: [microstrip, cadence-virtuoso, wilkinson-divider, branch-line-hybrid]
cover_image: /assets/images/learning/coursework/rf-passive-microstrip-divider-hybrid.svg
thumbnail: /assets/images/learning/coursework/rf-passive-microstrip-divider-hybrid.svg
image_alt: 50옴 microstrip 단면과 Wilkinson divider, branch-line hybrid 치수
draft: false
revision_history:
  - { date: 2026-08-01, change: 과제 계산과 저장된 Cadence 화면의 수치를 함께 정리 }
toc:
  - { id: start, title: 3.5 GHz 조건부터 }
  - { id: microstrip, title: 폭과 길이 계산 }
  - { id: marker, title: 3.7 GHz marker 읽기 }
  - { id: wilkinson, title: Wilkinson divider }
  - { id: hybrid, title: Branch-Line hybrid }
  - { id: interpretation, title: Simulation으로만 해석 }
  - { id: navigation, title: 이전 글과 다음 글 }
---

## 3.5 GHz 조건부터 {#start}

고주파공학 과제를 다시 보면서 먼저 공통 조건을 한 줄에 모았다. 기판은 두께 0.5 mm, 상대유전율 9.9인 alumina이고 설계 중심주파수는 3.5 GHz였다. 이 조건이 microstrip 폭과 유도파장, divider와 hybrid의 λ/4 길이를 모두 결정한다.

<figure>
  <img src="{{ '/assets/images/learning/coursework/rf-passive-microstrip-divider-hybrid.svg' | relative_url }}" alt="왼쪽에는 alumina 50옴 microstrip과 3.7 GHz marker가 있고 오른쪽에는 Wilkinson divider와 branch-line hybrid 치수가 있다" width="1200" height="630">
  <figcaption>한쪽에는 전송선 계산을, 다른 쪽에는 두 수동 분배 회로의 실제 입력 치수를 배치했다.</figcaption>
</figure>

## 폭과 길이 계산 {#microstrip}

50 Ω 조건으로 계산한 선폭은 약 0.4815 mm였다. 3.5 GHz에서 270° 위상지연은 유도파장의 3/4이므로 길이는 약 24.97 mm가 된다. 처음에는 자유공간 파장을 그대로 넣었지만, alumina 위에서 짧아진 유도파장을 써야 보고서 길이와 맞았다.

<figure>
  <table>
    <thead><tr><th>항목</th><th>값</th><th>메모</th></tr></thead>
    <tbody>
      <tr><td>상대유전율</td><td>9.9</td><td>Alumina</td></tr>
      <tr><td>기판 두께</td><td>0.5 mm</td><td>공통 조건</td></tr>
      <tr><td>50 Ω 선폭</td><td>약 0.4815 mm</td><td>Microstrip 계산</td></tr>
      <tr><td>270° 선로 길이</td><td>약 24.97 mm</td><td>3.5 GHz 기준</td></tr>
    </tbody>
  </table>
  <figcaption>단위가 µm와 mm로 섞여 있어 모든 값을 mm 기준으로 먼저 비교했다.</figcaption>
</figure>

## 3.7 GHz marker 읽기 {#marker}

저장된 Cadence 화면의 3.7 GHz marker에는 insertion loss가 약 −0.095 dB, 위상이 약 −284.49°로 표시되어 있었다. 목표 3.5 GHz의 270°보다 주파수가 높아지면서 위상 누적도 더 커진 것으로 읽었다. 이 값은 당시 simulation 화면에서 옮긴 값이며 장비로 잰 수치는 아니다.

## Wilkinson divider {#wilkinson}

동일 분배 Wilkinson의 두 λ/4 branch는 이론상 약 70.7 Ω이다. 저장된 설계에서는 저항을 100 Ω에서 94 Ω로 조정했고, branch 폭 270 µm와 길이 6.65 mm를 사용했다. 화면에서 S21과 S31은 약 −3 dB, S11은 약 −15 dB 수준이었다. 나는 이 수치를 완벽한 정합이라고 부르기보다 중심주파수와 notch 위치를 다시 확인해야 하는 simulation 결과로 읽었다.

<figure>
  <table>
    <thead><tr><th>회로</th><th>전송선</th><th>저장된 화면에서 읽은 값</th></tr></thead>
    <tbody>
      <tr><td>Wilkinson</td><td>70.7 Ω, W 270 µm, L 6.65 mm</td><td>S21·S31 약 −3 dB, S11 약 −15 dB</td></tr>
      <tr><td>Branch-Line</td><td>수평 35.35 Ω, 수직 50 Ω</td><td>분배·격리 곡선의 중심 이동 확인</td></tr>
    </tbody>
  </table>
  <figcaption>이론 임피던스와 입력한 물리 치수를 따로 적어야 tuning 과정을 설명하기 쉬웠다.</figcaption>
</figure>

## Branch-Line hybrid {#hybrid}

Quadrature hybrid는 위아래 수평선에 35.35 Ω, 좌우 수직선에 50 Ω를 배치한 사각형 구조였다. 저장된 치수는 수평선 W 908 µm, L 7.0 mm, 수직선 W 483 µm, L 7.2 mm였다. 두 종류의 선폭을 바꿔 그리면 왜 네 변이 같은 임피던스가 아닌지 바로 보였다.

## Simulation으로만 해석 {#interpretation}

이번 글에서는 보고서 계산과 당시 Cadence 화면을 연결했다. 새 netlist를 실행하거나 VNA로 제작 회로를 측정하지 않았다. 다음에는 동일한 주파수 sweep 조건을 다시 만들고 marker, port 정의, dB 기준을 한 화면에서 확인할 생각이다.

## 이전 글과 다음 글 {#navigation}

- [이전: 전공과목 전체 보기]({{ '/coursework/' | relative_url }})
- [시리즈: RF · Microwave]({{ '/blog/series/rf-microwave/' | relative_url }})
- [다음: FMCW Radar 후보 시점 정리]({{ '/blog/2026/07/31/radar-candidate-timing/' | relative_url }})
