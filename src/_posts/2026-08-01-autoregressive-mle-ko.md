---
title: Autoregressive Factorization과 MLE
title_en: Autoregressive Factorization and MLE
description: 결합확률을 순서대로 풀고 teacher forcing, log-likelihood, cross entropy를 연결한 기록.
date: 2026-08-01 09:02:00 +0900
updated: 2026-08-01 09:02:00 +0900
study_date: 2025-07-08
lang: ko
translation_key: autoregressive-mle
permalink: /blog/2026/08/01/autoregressive-mle/
alternate_url: /en/blog/2026/08/01/autoregressive-mle/
alternate_lang: en
primary_category: ai-deep-learning
subcategory: generative-ai
series: 2025-generative-models
series_order: 2
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_PRIMARY_SOURCE
tools: [Python, PyTorch]
hardware: []
software_versions: []
source_materials:
  - { title: Pixel Recurrent Neural Networks, type: paper, public_url: https://proceedings.mlr.press/v48/oord16.html, file_reference: PMLR paper, pages: 1747-1756, used_for: autoregressive image factorization }
prerequisites: [conditional-probability, logarithms]
learning_objectives: [joint factorization, teacher forcing, negative log-likelihood]
related_projects: []
related_posts: [generative-model-foundations]
tags: [autoregressive, mle, nll, teacher-forcing]
cover_image: /assets/images/learning/generative/autoregressive-mle.svg
thumbnail: /assets/images/learning/generative/autoregressive-mle.svg
image_alt: 이전 값을 조건으로 다음 값을 예측하고 로그확률을 합하는 흐름
draft: false
revision_history:
  - { date: 2026-08-01, change: 과정 노트와 PixelRNN 논문을 연결 }
toc:
  - { id: factorization, title: 결합확률 나누기 }
  - { id: train, title: 학습과 생성의 입력 }
  - { id: mle, title: MLE를 loss로 바꾸기 }
  - { id: code, title: 코드에서 확인 }
  - { id: limit, title: 남은 비용 }
---

## 결합확률 나누기 {#factorization}

(p(x_1,ldots,x_T)=\prod_t p(x_t|x_{&lt;t}))로 쓰면 다음 값 예측을 반복해 전체 표본을 만들 수 있다.

<figure><img src="{{ '/assets/images/learning/generative/autoregressive-mle.svg' | relative_url }}" alt="조건부확률을 순서대로 예측하고 Negative Log-Likelihood를 합하는 흐름" width="1200" height="630"><figcaption>확률의 chain rule과 실제 loss 계산을 한 줄로 연결했다.</figcaption></figure>

## 학습과 생성의 입력 {#train}

학습에서는 정답 prefix를 넣는 teacher forcing이 가능하다. 생성에서는 모델이 방금 뽑은 값을 다시 넣으므로 초기 오류가 누적될 수 있다. causal mask는 미래 token을 미리 보는 것을 막는다.

## MLE를 loss로 바꾸기 {#mle}

Likelihood의 곱에 log를 취하면 합이 된다. 최대화 식에 음수를 붙여 최소화하면 NLL이 된다. class index를 정답으로 쓰는 cross entropy는 정답 class의 log probability를 고르는 같은 계산이다.

## 코드에서 확인 {#code}

입력과 target을 한 칸 밀고, output logits의 마지막 축이 vocabulary인지 확인했다. padding token까지 loss에 들어가지 않도록 mask도 함께 봤다.

## 남은 비용 {#limit}

순차 sampling은 긴 sequence에서 느리다. 이 한계가 병렬 latent-variable 모델과 diffusion sampling을 비교하게 만든다.
