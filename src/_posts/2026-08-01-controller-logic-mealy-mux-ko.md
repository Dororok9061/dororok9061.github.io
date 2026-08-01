---
title: Mealy 101 검출기와 8-to-1 MUX 소스 다시 읽기
title_en: Reading the Mealy 101 Detector and 8-to-1 MUX Sources
description: 저장된 VHDL에서 overlapping 101 상태전이와 decoder 기반 MUX 구조를 다시 따라간 기록.
date: 2026-08-01 11:01:00 +0900
updated: 2026-08-01 11:01:00 +0900
study_date: 2024-11-22
lang: ko
translation_key: controller-logic-mealy-mux
permalink: /blog/2026/08/01/controller-logic-mealy-mux/
alternate_url: /en/blog/2026/08/01/controller-logic-mealy-mux/
alternate_lang: en
primary_category: major-foundations
subcategory: controller-logic
series: vhdl-foundations
series_order: 7
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: SOURCE_REVIEWED_NOT_RERUN
tools: [VHDL, Vivado]
hardware: []
software_versions: []
source_materials:
  - { title: Controller Logic coursework VHDL source, type: local-coursework, public_url: "", file_reference: mealy.vhd and mux_8to1.vhd, pages: "", used_for: state transitions and source structure }
prerequisites: [digital-logic, vhdl]
learning_objectives: [Mealy state transition, overlapping sequence detection, multiplexer selection]
related_projects: [fpga-delay-logic]
related_posts: [fpga-architecture-equivalence]
tags: [vhdl, mealy-fsm, sequence-detector, multiplexer]
cover_image: /assets/images/study/coursework/controller-logic-waveform.webp
thumbnail: /assets/images/study/coursework/controller-logic-waveform.webp
image_alt: 01010101 입력에서 Mealy 101 검출기의 상태와 출력이 바뀌는 Vivado 파형
draft: false
revision_history:
  - { date: 2026-08-01, change: 저장된 VHDL과 testbench 입력을 바탕으로 작성 }
toc:
  - { id: source, title: 소스에서 다시 시작 }
  - { id: states, title: 세 상태로 101 찾기 }
  - { id: stimulus, title: 01010101 따라가기 }
  - { id: mux, title: MUX를 독립형으로 쓰기 }
  - { id: rerun, title: 다시 실행할 때 볼 것 }
  - { id: navigation, title: 이전 글과 다음 글 }
---

## 소스에서 다시 시작 {#source}

이번에는 2024년에 저장한 <code>mealy.vhd</code>, <code>mealy_tb.vhd</code>, <code>mux_8to1.vhd</code>를 차례로 읽었다. Vivado가 만든 cache와 실행 파일보다 직접 작성한 entity, architecture, testbench 입력을 먼저 봤다.

<figure>
  <img src="{{ '/assets/images/learning/coursework/controller-logic-mealy-mux.svg' | relative_url }}" alt="왼쪽은 st0, st1, st2로 구성한 Mealy 101 검출기이고 오른쪽은 3-bit 선택값에 따른 8-to-1 MUX 입력표" width="1200" height="630">
  <figcaption>왼쪽 패널은 overlapping 101 검출기, 오른쪽 패널은 같은 선택 논리를 독립형 MUX로 다시 적은 모습이다.</figcaption>
</figure>

## 세 상태로 101 찾기 {#states}

상태 이름은 단순했다. <code>st0</code>는 아직 유효한 앞부분이 없고, <code>st1</code>은 마지막 입력이 1이며, <code>st2</code>는 마지막 두 입력이 10인 상태다. <code>st2</code>에서 1을 받으면 101이 완성되어 <code>dout</code>이 1이 된다. 동시에 <code>st1</code>로 돌아가므로 마지막 1을 다음 패턴의 첫 1로 다시 쓸 수 있다.

<figure>
  <table>
    <thead><tr><th>현재 상태</th><th>입력 0</th><th>입력 1</th><th>출력 1 조건</th></tr></thead>
    <tbody>
      <tr><td>st0</td><td>st0</td><td>st1</td><td>-</td></tr>
      <tr><td>st1</td><td>st2</td><td>st1</td><td>-</td></tr>
      <tr><td>st2</td><td>st2</td><td>st1</td><td>입력 1</td></tr>
    </tbody>
  </table>
  <figcaption>상태표를 만들자 overlap 처리가 <code>st2 → st1</code> 전이에 들어 있다는 점이 보였다.</figcaption>
</figure>

## 01010101 따라가기 {#stimulus}

저장된 testbench는 reset을 내린 뒤 <code>01010101</code>을 20 ns 간격으로 넣는다. 상태표대로 종이에 따라가면 네 번째, 여섯 번째, 여덟 번째 입력에서 101이 완성된다. 이 계산은 코드의 전이 규칙을 손으로 확인한 것이며, 이번 정리에서 GHDL이나 Vivado simulation을 다시 돌리지는 않았다.

<figure><img src="{{ '/assets/images/study/coursework/controller-logic-waveform.webp' | relative_url }}" alt="01010101 입력과 st0, st1, st2 상태, dout pulse가 표시된 저장 파형" width="1200" height="514"><figcaption>당시 저장한 파형에서 입력과 상태 전이를 함께 따라갔다.</figcaption></figure>

## MUX를 독립형으로 쓰기 {#mux}

원래 <code>mux_8to1.vhd</code>는 <code>dec_3to8</code> component와 AND/OR 조합으로 8개 입력을 선택한다. 저장 묶음에서는 decoder의 VHDL 원본을 찾지 못했다. 그래서 같은 진리표를 공부할 때는 의존성이 없는 <code>with select</code> 형태로 다시 적어봤다.

<figure>
  <pre><code class="language-vhdl">with sel select
  y &lt;= a when "000",
       b when "001",
       c when "010",
       d when "011",
       e when "100",
       f when "101",
       g when "110",
       h when others;</code></pre>
  <figcaption>이 예시는 원래 archive를 고쳤다는 뜻이 아니라, 같은 선택 함수를 독립된 VHDL로 표현한 학습용 코드다.</figcaption>
</figure>

## 다시 실행할 때 볼 것 {#rerun}

다음 실행에서는 clock edge 직후의 <code>present_state</code>, 조합논리의 <code>next_state</code>, <code>dout</code>을 한 파형에 놓을 생각이다. MUX는 먼저 독립형 예제를 모든 선택값으로 확인한 뒤, decoder 원본을 다시 찾으면 구조형 구현과 출력을 비교할 예정이다.

## 이전 글과 다음 글 {#navigation}

- [이전: 전공과목 전체 보기]({{ '/coursework/' | relative_url }})
- [시리즈: VHDL 디지털논리 기초]({{ '/blog/series/vhdl-foundations/' | relative_url }})
- [다음: Shift Register와 Circular Queue 검증 글]({{ '/blog/2026/07/31/fpga-architecture-equivalence/' | relative_url }})
