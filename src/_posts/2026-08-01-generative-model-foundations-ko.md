---
title: 생성모델과 데이터 분포부터 시작하기
title_en: Starting with Generative Models and Data Distributions
description: 판별모델과 생성모델을 비교하고 Tensor shape와 데이터 시각화를 먼저 확인한 기록.
date: 2026-08-01 09:01:00 +0900
updated: 2026-08-01 09:01:00 +0900
study_date: 2025-07-07
lang: ko
translation_key: generative-model-foundations
permalink: /blog/2026/08/01/generative-model-foundations/
alternate_url: /en/blog/2026/08/01/generative-model-foundations/
alternate_lang: en
primary_category: ai-deep-learning
subcategory: generative-ai
series: 2025-generative-models
series_order: 1
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_PRIMARY_SOURCE
tools: [Python, PyTorch, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: PyTorch Learn the Basics, type: official-documentation, public_url: https://docs.pytorch.org/tutorials/beginner/basics/intro.html, file_reference: official tutorial, pages: "", used_for: tensor and training workflow }
prerequisites: [probability, python]
learning_objectives: [판별과 생성 구분, tensor shape 확인, 데이터 분할 전 시각화]
related_projects: []
related_posts: []
tags: [generative-ai, pytorch, tensor, data-visualization]
cover_image: /assets/images/learning/generative/overview.svg
thumbnail: /assets/images/learning/generative/overview.svg
image_alt: 관측 데이터에서 분포를 학습하고 새로운 샘플을 만드는 생성모델 흐름
draft: false
revision_history:
  - { date: 2026-08-01, change: 과정 노트와 공식 문서를 바탕으로 작성 }
toc:
  - { id: question, title: 처음 던진 질문 }
  - { id: distribution, title: 분포를 배운다는 뜻 }
  - { id: shape, title: Tensor shape 확인 }
  - { id: data, title: 데이터부터 그리기 }
  - { id: next, title: 다음 연결 }
---

## 처음 던진 질문 {#question}

먼저 “생성한다”는 말을 이미지 합성으로만 보지 않았다. 관측한 (x)의 분포를 근사하고 그 분포에서 새 표본을 뽑는 문제로 바꿔 적었다.

<figure><img src="{{ '/assets/images/learning/generative/overview.svg' | relative_url }}" alt="데이터, 분포 학습, 모델과 샘플을 연결한 생성모델 흐름" width="1200" height="630"><figcaption>데이터를 외우는 표가 아니라 확률분포를 근사하는 흐름으로 다시 그렸다.</figcaption></figure>

## 분포를 배운다는 뜻 {#distribution}

분류는 (p(y|x))를, 생성은 (p(x)) 또는 (p(x,y))를 주로 본다. 이 관점을 잡고 나니 Autoregressive Model은 조건부확률의 곱, VAE는 latent variable, GAN은 두 네트워크의 게임, Diffusion은 noise를 거꾸로 지우는 과정으로 비교할 수 있었다.

## Tensor shape 확인 {#shape}

Notebook을 실행했을 때 입력 Tensor가 `(N, C, H, W)`인지 먼저 출력했다. flatten 뒤 feature 수가 Linear layer의 입력과 맞지 않으면 바로 수정했다. broadcast가 조용히 적용되는 연산은 loss가 계산돼도 의미가 틀릴 수 있었다.

## 데이터부터 그리기 {#data}

class balance, 값의 범위, 결측치, 중복 표본을 train 전에 살폈다. normalization 통계는 split 뒤 training set에서만 계산했다. 모델 선택보다 데이터 누수 방지가 먼저라는 점은 P1 수어 분류를 다시 해석할 때 특히 중요했다.

## 다음 연결 {#next}

고차원 (p(x))를 직접 쓰기 어렵다는 문제가 남았다. 다음 글에서는 joint probability를 조건부확률의 곱으로 나누고 Maximum Likelihood를 loss로 바꾸는 과정을 이어서 정리한다.
