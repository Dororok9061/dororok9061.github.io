---
layout: course-day
course_id: 2025-generative-models
day: 3
title: 2025 생성모델 집중과정 Day 3
description: VAE의 encoder, reparameterization, reconstruction loss와 KL divergence를 연결한 기록.
permalink: /learning/bootcamps/kaist-generative-models-2025/day-3/
lang: ko
alternate_url: /en/learning/bootcamps/kaist-generative-models-2025/day-3/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/generative/vae.svg' | relative_url }}" alt="입력에서 평균과 분산을 예측하고 잠재변수를 거쳐 입력을 복원하는 VAE 구조" width="1200" height="630"><figcaption>Encoder가 하나의 좌표 대신 latent distribution의 parameter를 예측한다.</figcaption></figure>

## Autoencoder와 달라진 점

일반 Autoencoder는 입력을 하나의 latent vector로 압축한다. VAE는 (q_\phi(z|x))의 평균과 분산을 예측하고 그 분포에서 (z)를 뽑는다. [VAE 원 논문](https://arxiv.org/abs/1312.6114)을 다시 읽으면서 approximate posterior와 prior가 왜 함께 나오는지 확인했다.

## Reparameterization trick

코드를 실행했을 때 `z = mu + std * eps` 한 줄이 sampling을 없애는 것으로 오해했다. 실제로는 무작위성 (ε)을 parameter 밖으로 분리해 (\mu)와 (\sigma)까지 gradient가 흐르게 만드는 표현이었다.

## 두 loss의 역할

Reconstruction loss는 입력 정보를 복원하도록 만들고, KL divergence는 (q_\phi(z|x))가 prior에서 지나치게 멀어지지 않게 한다. KL 항을 너무 강하게 주면 decoder가 (z)를 거의 쓰지 않는 posterior collapse도 생길 수 있다.

## 다시 실행할 항목

당시 latent interpolation 출력은 남아 있지 않았다. 현재 글에는 구조와 loss 계산까지만 정리했고, 다음 실행에서는 (β) 값을 바꾸며 reconstruction과 latent continuity를 함께 비교할 예정이다.
