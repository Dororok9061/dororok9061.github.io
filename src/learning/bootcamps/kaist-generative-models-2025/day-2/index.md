---
layout: course-day
course_id: 2025-generative-models
day: 2
title: 2025 생성모델 집중과정 Day 2
description: Autoregressive factorization, teacher forcing, Maximum Likelihood와 NLL을 연결한 기록.
permalink: /learning/bootcamps/kaist-generative-models-2025/day-2/
lang: ko
alternate_url: /en/learning/bootcamps/kaist-generative-models-2025/day-2/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/generative/autoregressive-mle.svg' | relative_url }}" alt="이전 값을 조건으로 다음 값을 예측하고 로그확률을 합하는 자가회귀 학습 흐름" width="1200" height="630"><figcaption>결합확률의 factorization과 Negative Log-Likelihood를 한 흐름으로 묶었다.</figcaption></figure>

## 결합확률을 순서대로 풀기

(p(x_1, ldots, x_T)=\prod_t p(x_t|x_{&lt;t}))로 쓰면 고차원 분포를 다음 token 또는 pixel의 조건부확률 문제로 바꿀 수 있다. [PixelRNN 논문](https://proceedings.mlr.press/v48/oord16.html)은 이 관점을 이미지의 두 공간축에 적용한다.

## Teacher forcing과 생성의 차이

학습 때는 정답 prefix를 다음 예측의 입력으로 넣을 수 있지만 생성 때는 방금 모델이 뽑은 값을 다시 입력해야 한다. 이 차이 때문에 초반 오류가 뒤로 전파될 수 있다. 병렬 학습이 가능한 Transformer라도 causal mask로 미래 token을 보지 못하게 하는 이유는 같다.

## MLE에서 loss로

확률의 곱은 값이 작아지고 미분도 다루기 어렵다. log를 취하면 곱이 합으로 바뀌며, 최대화 대신 음수를 붙여 최소화하면 Negative Log-Likelihood가 된다. 분류에서는 정답 class의 log probability를 고르는 cross entropy와 같은 계산으로 만난다.

## 내가 헷갈렸던 부분

MLE는 모델이 정답을 “외운다”는 뜻이 아니라, 관측 데이터가 모델 아래에서 높은 확률을 갖도록 parameter를 조정하는 원리다. 다음에는 latent variable을 직접 관측할 수 없을 때 likelihood를 어떻게 다루는지 VAE로 넘어갔다.
