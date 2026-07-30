---
title: Delay Logic에서 architecture equivalence를 확인하는 방법
description: Shift Register와 Circular Queue 구현을 같은 cycle-delay contract로 비교하는 검증 관점.
date: 2026-07-31 00:20:00 +0900
categories: [fpga]
lang: ko
permalink: /blog/2026/07/31/fpga-architecture-equivalence/
alternate_url: /en/blog/2026/07/31/fpga-architecture-equivalence/
alternate_lang: en
---

Delay logic 구현을 변경할 때 비교해야 하는 것은 내부 자료구조가 아니라 외부
contract입니다. 동일한 input data와 valid sequence에 대해 출력 data, valid,
reset 이후 상태와 정확한 cycle delay가 같아야 합니다.

독립 reference model은 DUT 구조를 그대로 복사하지 않습니다. 입력 transaction에
tag를 붙여 expected output cycle을 계산하고, 구현별 출력과 같은 기준으로
비교해야 동일한 설계 오류를 복제할 가능성을 줄일 수 있습니다.

[FPGA project page](/projects/fpga-delay-logic/)에는 공개 log가 지원하는 check
수와 Quartus 검증이 BLOCKED인 이유를 함께 기록합니다.
