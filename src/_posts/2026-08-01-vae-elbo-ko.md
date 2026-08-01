---
title: VAE의 ELBO와 Reparameterization
title_en: VAE ELBO and Reparameterization
description: Encoder가 평균과 분산을 예측하는 이유와 reconstruction·KL loss를 코드 흐름으로 정리한 기록.
date: 2026-08-01 09:03:00 +0900
updated: 2026-08-01 09:03:00 +0900
study_date: 2025-07-09
lang: ko
translation_key: vae-elbo
permalink: /blog/2026/08/01/vae-elbo/
alternate_url: /en/blog/2026/08/01/vae-elbo/
alternate_lang: en
primary_category: ai-deep-learning
subcategory: generative-ai
series: 2025-generative-models
series_order: 3
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_PRIMARY_SOURCE
tools: [Python, PyTorch]
hardware: []
software_versions: []
source_materials:
  - { title: Auto-Encoding Variational Bayes, type: paper, public_url: https://arxiv.org/abs/1312.6114, file_reference: arXiv 1312.6114, pages: 1-14, used_for: ELBO and reparameterization }
prerequisites: [probability, autoencoder, backpropagation]
learning_objectives: [approximate posterior, reparameterization, reconstruction and KL balance]
related_projects: []
related_posts: [autoregressive-mle]
tags: [vae, elbo, latent-space, kl-divergence]
cover_image: /assets/images/learning/generative/vae.svg
thumbnail: /assets/images/learning/generative/vae.svg
image_alt: Encoder가 평균과 분산을 예측하고 latent를 거쳐 입력을 복원하는 VAE
draft: false
revision_history:
  - { date: 2026-08-01, change: 과정 노트와 VAE 원 논문을 연결 }
toc:
  - { id: latent, title: 하나의 좌표에서 분포로 }
  - { id: trick, title: Reparameterization }
  - { id: loss, title: 두 loss }
  - { id: shape, title: 코드 Shape }
  - { id: rerun, title: 다시 돌릴 실험 }
---

## 하나의 좌표에서 분포로 {#latent}

VAE Encoder는 (z) 하나를 내지 않고 (q_\phi(z|x))의 평균과 log variance를 예측한다.

<figure><img src="{{ '/assets/images/learning/generative/vae.svg' | relative_url }}" alt="VAE의 입력, encoder, 평균과 분산, latent, decoder 구조" width="1200" height="630"><figcaption>학습 가능한 parameter와 무작위 sampling의 위치를 나눠 그렸다.</figcaption></figure>

## Reparameterization {#trick}

처음에는 `z = mu + std * eps`가 sampling을 없앤다고 혼동했다. 실제로는 ε을 parameter 밖으로 분리해 μ와 σ까지 gradient가 흐르게 한다.

## 두 loss {#loss}

Reconstruction은 입력 정보를 유지하고 KL divergence는 posterior가 prior에서 지나치게 멀어지지 않게 한다. 둘의 비율이 맞지 않으면 흐릿한 복원이나 posterior collapse가 생길 수 있다.

## 코드 Shape {#shape}

`mu`, `logvar`, `eps`, `z`의 Shape가 모두 `(batch, latent_dim)`인지 출력했다. KL은 batch와 latent 축을 어디까지 합할지 명시해야 loss scale을 비교할 수 있었다.

## 다시 돌릴 실험 {#rerun}

당시 latent interpolation 그림은 남아 있지 않았다. β 값을 바꾸고 reconstruction과 latent continuity를 함께 그리는 실험을 다음에 추가할 예정이다.
