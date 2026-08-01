---
layout: page
title: 전공과목 포트폴리오
eyebrow: Electrical Engineering Coursework
lead: 학부 과제와 실습을 전공 분야별로 모으고, 직접 한 설계·실행·측정을 구분해 설명합니다.
description: VHDL, 전력, 제어, RF, 센서 분야의 전자전기공학 학부 과제 포트폴리오.
permalink: /coursework/
lang: ko
alternate_url: /en/coursework/
alternate_lang: en
---

## 디지털논리와 FPGA

컨트롤로직설계 과제에서 작성한 VHDL을 다시 읽었다. `101`을 겹쳐 검출하는 Mealy FSM과 decoder 기반 8-to-1 MUX의 입력 흐름을 소스 단위로 따라갔다. MUX가 참조하는 `dec_3to8` 파일은 저장본에서 찾지 못해 컴파일 성공으로 적지 않았다.

- [Mealy 101 검출기와 8-to-1 MUX 소스 다시 읽기](/blog/2026/08/01/controller-logic-mealy-mux/)
- [SystemVerilog delay logic 구조 비교](/blog/2026/07/31/fpga-architecture-equivalence/)

## 제어와 전동기

전동기제어 보고서의 DC Motor, H-bridge, 전류·속도 이중 PI loop를 한 흐름으로 다시 그렸다. 10 kHz와 30 kHz의 torque ripple 비교는 당시 PSIM 시뮬레이션에 저장된 값으로 설명하고 실제 모터 측정값으로 바꾸어 쓰지 않았다.

- [PSIM에서 DC Motor 이중 PI 제어와 Field Weakening 정리](/blog/2026/08/01/dc-motor-cascaded-pi-field-weakening/)

## RF·Microwave

3.5 GHz alumina microstrip 계산에서 시작해 Wilkinson divider와 branch-line hybrid의 저장된 Cadence 화면을 회로 구조와 S-parameter로 연결했다. 화면 속 로컬 경로 대신 공개용 회로도를 새로 그렸다.

- [3.5 GHz Microstrip에서 Wilkinson·Branch-Line까지](/blog/2026/08/01/rf-passive-microstrip-divider-hybrid/)

## PADS와 PCB

Decal Wizard에 남은 6-pin SOIC 치수와 별도의 PPG 회로 화면을 두 사례로 정리했다. 두 화면의 부품 관계는 확인되지 않았으므로 하나의 artifact처럼 합치지 않았다.

- [PADS의 SOIC Footprint와 PPG 회로를 별도 사례로 다시 읽기](/blog/2026/08/01/pads-footprint-ppg-schematic/)

## 이어서 정리할 과목

변압기 계산, 자동제어 문제풀이, 센서공학의 AESA·SAR 제안서는 식과 계산표를 다시 대조한 뒤 이어서 정리한다. 저장된 보고서의 숫자는 그대로 옮기기 전에 단위와 입력조건부터 다시 계산한다.

- [Coursework project page](/projects/coursework/)
- [Full coursework repository](https://github.com/Tontonjeong/electrical-engineering-coursework-portfolio)
