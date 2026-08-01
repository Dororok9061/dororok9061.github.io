---
title: PSIM에서 DC Motor 이중 PI 제어와 Field Weakening 정리
title_en: Cascaded PI Control and Field Weakening for a DC Motor in PSIM
description: 전동기제어 과제 보고서의 H-bridge, 전류·속도 이중루프와 스위칭 주파수 비교를 다시 읽고 정리한 기록.
date: 2026-08-01 15:20:00 +0900
updated: 2026-08-01 15:20:00 +0900
study_date: 2025-11-01
lang: ko
translation_key: dc-motor-cascaded-pi-field-weakening
permalink: /blog/2026/08/01/dc-motor-cascaded-pi-field-weakening/
alternate_url: /en/blog/2026/08/01/dc-motor-cascaded-pi-field-weakening/
alternate_lang: en
primary_category: major-foundations
subcategory: motor-control
series: dc-motor-control
series_order: 1
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_ARCHIVED_SIMULATION_REPORT
tools: [PSIM, MATLAB, PI Control]
hardware: []
software_versions: []
source_materials:
  - { title: 전동기제어 과제 보고서, type: private-coursework-report, file_reference: archived report, pages: "1-13", used_for: "motor parameters, controller settings, and saved simulation comparison" }
  - { title: Altair PSIM Motor Control Design Suite Tutorial, type: official-documentation, public_url: https://2023.help.altair.com/psim-tut/tutorials/Tutorial%20-%20Motor%20Control%20Design%20Suite.pdf, used_for: cascaded control and field-weakening context }
prerequisites: [dc-motor-model, pi-control, pwm]
learning_objectives: [이중루프 구조 해석, PI gain 의미 확인, 저장된 torque ripple 비교 읽기]
related_projects: [coursework]
related_posts: []
tags: [dc-motor, psim, pi-control, h-bridge, field-weakening]
cover_image: /assets/images/coursework/dc-motor-cascaded-control.svg
thumbnail: /assets/images/coursework/dc-motor-cascaded-control.svg
image_alt: 속도 PI와 전류 PI가 H-bridge와 DC motor를 제어하는 이중루프 구조
draft: false
revision_history:
  - { date: 2026-08-01, change: 저장된 과제 보고서의 시뮬레이션 설정과 결과를 재정리 }
toc:
  - { id: plant, title: 모터와 H-bridge부터 보기 }
  - { id: loops, title: 두 제어루프를 나눈 이유 }
  - { id: gains, title: 보고서의 PI 설정 읽기 }
  - { id: weakening, title: 포화와 Field Weakening }
  - { id: ripple, title: 스위칭 주파수 비교 }
  - { id: limits, title: 이번 기록의 범위 }
---

## 모터와 H-bridge부터 보기 {#plant}

먼저 과제 보고서에서 DC Motor를 전기계와 기계계로 나눠 다시 읽었다. 전기계는 전기자 저항·인덕턴스와 역기전력으로, 기계계는 관성·마찰과 부하토크로 표현했다. H-bridge는 이 plant에 양·음의 평균 전압을 만들어 주는 구동부다.

전기자 회로는 먼저 자속이 일정한 기준 동작점으로 정리했다. 이때만 `K_e`와 `K_t`를 상수처럼 둘 수 있다.

<p class="study-equation"><code>vₐ = Rₐiₐ + Lₐ(diₐ/dt) + Kₑω</code><br><code>J(dω/dt) = Kₜiₐ − Bω − Tₗ</code></p>

두 식을 같이 보면 전류가 토크를 만들고, 속도가 다시 역기전력으로 전류에 영향을 준다. 속도 명령만 바로 PWM에 연결하는 대신 전류를 안쪽에서 먼저 제어한 이유가 여기서 보였다.

## 두 제어루프를 나눈 이유 {#loops}

바깥쪽 speed PI는 속도 오차를 전류 명령으로 바꾸고, 안쪽 current PI는 그 전류를 빠르게 추종하도록 전압 명령을 만든다. 전류루프의 대역폭을 속도루프보다 높게 잡으면 바깥쪽에서는 안쪽 루프를 거의 즉시 반응하는 토크원처럼 볼 수 있다.

<figure><img src="{{ '/assets/images/coursework/dc-motor-cascaded-control.svg' | relative_url }}" alt="속도 PI, 전류 제한기, 전류 PI, H-bridge와 DC motor의 이중루프" width="1200" height="630"><figcaption>과제 보고서의 블록도를 공개용으로 다시 그렸다. 수치는 당시 보고서에 적힌 설정이며 이번에 다시 실행한 값은 아니다.</figcaption></figure>

처음에는 두 PI가 같은 오차를 줄이는 것으로 혼동했다. 다시 보니 speed PI의 출력은 전류 기준값이고, current PI의 출력은 전압 또는 duty 기준값이었다. 각 loop의 입력·출력 단위를 적어 두자 역할이 분명해졌다.

## 보고서의 PI 설정 읽기 {#gains}

남아 있던 보고서에는 speed PI가 `Kp = 24.8`, `Ki ≈ 3898`, current PI가 `Kp = 62.832`, `Ki = 314.16`으로 기록돼 있었다. 이 값 자체를 보편적인 최적 gain으로 보지 않고, 보고서에서 사용한 motor parameter와 목표 대역폭에 종속된 설정으로 읽었다.

코드나 block parameter를 다시 확인할 때는 다음 순서가 안전하다.

```text
1. motor parameter와 단위를 확인한다.
2. current loop를 먼저 닫고 step response를 본다.
3. current limit가 동작하는지 확인한다.
4. 그 다음 speed loop를 닫는다.
5. saturation과 anti-windup 유무를 함께 기록한다.
```

## 포화와 Field Weakening {#weakening}

속도가 올라가면 역기전력 `K_e ω`도 커진다. DC bus가 만들 수 있는 전압을 다 써도 전류를 더 유지할 수 없는 영역에서는 전압 포화가 생긴다. 과제의 타여자 DC Motor에서는 계자회로 저항을 높여 계자전류와 자속 `Φ`를 줄이는 방식으로 field weakening을 구성했다.

<p class="study-equation"><code>Kₑ = kₑΦ, Kₜ = kₜΦ</code></p>

따라서 자속을 줄이면 같은 속도에서 역기전력은 낮아져 더 높은 속도로 갈 여지가 생기지만, 같은 토크를 내려면 전기자전류가 더 커져야 한다. 이 구간에서는 앞 절의 상수 `K_e`, `K_t` 가정을 그대로 쓸 수 없다. Altair의 PSIM 자료는 current·speed loop와 base-speed 이후 제어라는 일반 맥락만 비교하는 데 사용했고, 이 DC 계자회로 구현의 근거는 과제 보고서에서 읽었다.

## 스위칭 주파수 비교 {#ripple}

과제 보고서에는 10 kHz에서 2.28 N·m, 30 kHz에서 0.38 N·m의 torque ripple이 기록돼 있었다. 이 값은 저장된 PSIM 시뮬레이션 비교이며, 실제 모터 샤프트에서 측정한 값이 아니다.

<figure><img src="{{ '/assets/images/coursework/dc-motor-switching-ripple.svg' | relative_url }}" alt="10 kHz 2.28 뉴턴미터와 30 kHz 0.38 뉴턴미터의 저장된 torque ripple 비교" width="1200" height="630"><figcaption>보고서에 적힌 두 결과를 같은 축으로 다시 그렸다. 높은 스위칭 주파수의 ripple 감소만 읽을 수 있고 손실·온도·EMI까지 좋아졌다고 말할 수는 없다.</figcaption></figure>

주파수를 높이면 전류가 한 주기 동안 변할 시간이 짧아져 ripple이 줄 수 있다. 반면 switching loss와 EMI, 계산 부하는 커질 수 있다. 그래서 이번 비교는 ripple 하나의 시뮬레이션 결과로만 남겼다.

## 이번 기록의 범위 {#limits}

이 단계까지는 저장된 과제 보고서의 모델, gain과 그래프를 다시 읽고 블록도를 재작성했다. PSIM 원본 회로를 새 버전에서 재실행하거나 실제 모터를 연결해 확인하지는 않았다. 다음에는 current-loop step부터 분리해 실행하고 saturation과 anti-windup 동작을 같은 조건에서 비교할 예정이다.
