---
layout: course-day
course_id: 2025-generative-models
day: 1
title: 2025 생성모델 집중과정 Day 1
description: 생성모델 개요, 딥러닝 기초, 데이터셋 시각화를 다시 정리한 첫날 기록.
permalink: /learning/bootcamps/kaist-generative-models-2025/day-1/
lang: ko
alternate_url: /en/learning/bootcamps/kaist-generative-models-2025/day-1/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/generative/overview.svg' | relative_url }}" alt="관측 데이터에서 분포를 학습하고 새로운 샘플을 만드는 생성모델 흐름" width="1200" height="630"><figcaption>생성모델을 데이터 복사기가 아니라 분포를 학습하는 모델로 정리했다.</figcaption></figure>

## 판별과 생성의 차이

분류기는 입력 (x)가 주어졌을 때 (p(y|x))를 구하는 쪽에 가깝다. 생성모델은 (p(x)) 또는 (p(x,y))를 다루고, 학습한 분포에서 새 (x)를 뽑는다. 처음에는 “이미지를 만드는 신경망”이라고만 생각했지만, 확률분포와 sampling 관점으로 바꾸니 Autoregressive Model, VAE, GAN, Diffusion의 차이가 보였다.

## Tensor shape부터 다시 확인

Notebook을 실행할 때 가장 먼저 확인할 값은 batch, channel, height, width 순서였다. 이미지 batch가 `(N, C, H, W)`인지, flatten 뒤 feature 수가 Linear layer 입력과 맞는지 출력 Shape를 찍어 봤다. loss가 계산돼도 잘못된 축으로 normalize하면 학습 의미가 달라질 수 있었다.

## 데이터부터 그려 본 이유

모델을 만들기 전에 class balance, pixel range, 결측치, 중복 표본을 먼저 봤다. train과 validation을 나눈 뒤에 전처리 통계를 계산해야 정보가 섞이지 않는다. 이 순서는 나중에 OUTTA P1의 유사 이미지 누수 가능성을 해석할 때도 그대로 적용했다.

## 다음 날로 이어진 질문

복잡한 이미지를 한 번에 확률로 나타내기 어렵다면, 여러 조건부확률의 곱으로 나눌 수 있는지가 다음 질문이었다. 그 답을 Autoregressive factorization과 MLE에서 이어서 정리했다.
