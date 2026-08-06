---
title: Shift Register와 Circular Queue의 cycle-delay 동등성을 검증한 방법
title_en: Verifying cycle-delay equivalence between shift-register and circular-queue designs
description: 동일 interface contract, 독립 reference model, expected cycle과 26개 regression check로 RTL architecture를 비교한 기록.
date: 2026-07-31 00:20:00 +0900
updated: 2026-08-01 18:20:00 +0900
study_date: 2026-07-31
lang: ko
translation_key: fpga-architecture-equivalence
permalink: /blog/2026/07/31/fpga-architecture-equivalence/
alternate_url: /en/blog/2026/07/31/fpga-architecture-equivalence/
alternate_lang: en
primary_category: fpga-rtl-dv
subcategory: reference-model
series: systemverilog-delay-dv
series_order: 5
post_type: project-log
difficulty: intermediate
study_status: verified
evidence_status: EXECUTED_FUNCTIONAL_SIMULATION
tools: [SystemVerilog, Icarus Verilog, VCD]
hardware: []
software_versions: [Icarus Verilog version recorded in public CI logs]
source_materials:
  - { title: FPGA Delay Logic Design Verification, type: public-repository, public_url: https://github.com/Dororok9061/fpga-delay-logic-design-verification, file_reference: RTL testbench and logs, pages: "", used_for: architecture contract and regression evidence }
  - { title: FPGA project detail, type: portfolio-page, public_url: /projects/fpga-delay-logic/, file_reference: public project data, pages: "", used_for: result and boundary summary }
prerequisites: [systemverilog, sequential-logic, testbench]
learning_objectives: [외부 contract로 architecture 비교, 독립 reference model 구성, cycle-aligned checker 해석]
related_projects: [fpga-delay-logic]
related_posts: []
tags: [systemverilog, reference-model, icarus-verilog, fpga]
cover_image: /assets/images/projects/fpga-architecture.webp
thumbnail: /assets/images/projects/fpga-architecture.webp
image_alt: Shift Register, Circular Queue, Memory-Based 구조로 발전하는 FPGA delay logic architecture
draft: false
revision_history:
  - { date: 2026-07-31, change: 최초 공개 }
  - { date: 2026-08-01, change: "interface contract, checker 절차, waveform과 26개 동등성 결과 추가" }
toc:
  - { id: problem, title: 비교한 문제 }
  - { id: contract, title: 동일 Interface Contract }
  - { id: reference, title: 독립 Reference Model }
  - { id: regression, title: 26개 Equivalence Test }
  - { id: waveform, title: Waveform 읽기 }
  - { id: quartus-next, title: Quartus에서 이어서 할 일 }
---

## 비교한 문제 {#problem}

Programmable delay logic은 입력 transaction을 설정한 cycle만큼 늦춰 내보낸다. 단순 Shift Register는 동작을 읽기 쉽지만 delay depth가 커질수록 register 수가 증가한다. Circular Queue는 read/write pointer로 같은 contract를 구현하지만 wrap-around, occupancy, dynamic delay 변경에서 off-by-one 오류가 생기기 쉽다.

비교 대상은 내부 배열이나 pointer가 아니다. 동일한 `data_i`, `valid_i`, reset, delay 설정을 넣었을 때 `data_o`, `valid_o`, 출력 cycle이 같아야 한다.

<figure><picture><source srcset="/assets/images/projects/fpga-architecture.webp" type="image/webp"><img src="/assets/images/projects/fpga-architecture.jpg" alt="Shift Register에서 Circular Queue와 Memory-Based Driver Checker로 확장되는 delay logic architecture" width="1200" height="517" loading="lazy"></picture><figcaption>구현 자료구조는 바뀌지만 외부 cycle-delay contract는 유지한다.</figcaption></figure>

## 동일 Interface Contract {#contract}

Checker가 보는 transaction은 다음 네 값으로 충분하다.

```systemverilog
typedef struct packed {
  logic [DATA_W-1:0] data;
  logic              valid;
  int unsigned       accepted_cycle;
  int unsigned       expected_cycle;
} expected_txn_t;
```

`valid_i`가 1인 cycle에 입력을 accept하고 `expected_cycle = accepted_cycle + delay`를 계산한다. 출력 cycle에서 valid와 data를 함께 비교한다. reset 중에는 queue를 비우고 `valid_o`가 내려가는지도 같은 contract에 포함한다.

Dynamic delay를 지원할 때 “현재 설정”을 나중에 다시 읽으면 안 된다. transaction을 accept한 시점의 delay를 함께 기록해야 설정 변경 전후의 packet이 섞이지 않는다.

## 독립 Reference Model {#reference}

Reference model이 DUT의 shift register나 circular buffer 코드를 복사하면 같은 설계 오류를 재현할 수 있다. 그래서 model은 입력 transaction과 예상 출력 cycle만 queue에 저장한다. DUT가 어떤 pointer 계산을 쓰는지는 알지 못한다.

Driver는 reset, 연속 valid, valid gap, delay 변경, buffer wrap 조건을 만든다. Checker는 expected queue의 head와 두 DUT의 출력을 같은 cycle에서 비교한다. mismatch에는 입력 tag, accept cycle, expected cycle, observed data를 남겨 어느 경계가 틀렸는지 찾을 수 있게 한다.

## 26개 Equivalence Test {#regression}

공개 regression log가 지원하는 Project 2 결과는 **26 architecture-equivalence checks PASS**다. DEPTH 10과 100을 포함해 서로 다른 parameter와 sequence에서 Shift Register와 Circular Queue 출력을 reference model에 대조했다.

이 수치는 assertion 수나 전체 simulation cycle 수가 아니다. testbench가 명시적으로 기록한 비교 check 수다. Project 1의 20 checks와 Project 3의 3 file-driven scenarios도 별도 결과이며 합쳐서 하나의 PPA 수치처럼 표시하지 않는다.

## Waveform 읽기 {#waveform}

<figure><picture><source srcset="/assets/images/projects/fpga-waveform.webp" type="image/webp"><img src="/assets/images/projects/fpga-waveform.jpg" alt="Programmable delay logic의 입력 valid, delay 설정, 출력 valid와 data를 표시한 verification waveform" width="1200" height="578" loading="lazy"></picture><figcaption>입력 accept cycle과 설정 delay를 기준으로 출력 valid와 data가 expected cycle에 나타나는지 확인한다.</figcaption></figure>

파형에서는 data만 맞는지 보지 않는다. `valid_o`가 한 cycle 먼저 올라가거나 reset 직후 오래된 data가 valid와 함께 나오는 것도 contract 위반이다. File-driven scenario는 입력 vector와 delay 변경을 외부 파일로 고정해 같은 regression을 반복할 수 있게 한다.

## Quartus에서 이어서 할 일 {#quartus-next}

Functional simulation은 직접 실행했다. 아직 Quartus synthesis report, timing analyzer, resource utilization, power, Fmax, numerical PPA report는 찾지 못했다. 그래서 Circular Queue가 실제 FPGA에서 더 적은 register 또는 memory resource를 쓴다는 수치는 적지 않았다. 다음에는 같은 constraint와 device 설정으로 두 architecture를 합성하고 report 원본과 명령을 함께 보존할 예정이다.
