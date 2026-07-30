---
title: 포트폴리오에서 Evidence Status를 분리하는 이유
description: Source Available, Executed, Measured, BLOCKED를 하나의 PASS로 합치지 않는 기록 원칙.
date: 2026-07-31 00:10:00 +0900
categories: [systems-engineering]
lang: ko
permalink: /blog/2026/07/31/evidence-status/
alternate_url: /en/blog/2026/07/31/evidence-status/
alternate_lang: en
---

프로젝트에 source가 있다는 사실과 실제 도구에서 실행했다는 사실은 다릅니다.
실행과 synthesis, 수치 PPA, hardware measurement도 각각 다른 근거를 요구합니다.

이 포트폴리오는 다음 네 상태를 기본으로 사용합니다.

- **SOURCE AVAILABLE** — 공개 source와 문서가 존재합니다.
- **EXECUTED** — 명시한 환경에서 실행 결과를 확인했습니다.
- **MEASURED** — 측정 조건과 결과가 함께 공개되어 있습니다.
- **BLOCKED** — 필요한 도구, 원본 또는 보고서가 없어 확인할 수 없습니다.

이 구분은 미완료를 숨기기 위한 것이 아닙니다. 어떤 단계부터 재현할 수 있는지,
다음 검증에 무엇이 필요한지를 빠르게 판단하기 위한 engineering interface입니다.
