---
title: DDPM에서 Latent Diffusion과 DiT까지
title_en: From DDPM to Latent Diffusion and DiT
description: Forward noise, reverse denoising, latent space와 Transformer backbone을 한 흐름으로 정리한 기록.
date: 2026-08-01 09:05:00 +0900
updated: 2026-08-01 09:05:00 +0900
study_date: 2025-07-11
lang: ko
translation_key: diffusion-latent-dit
permalink: /blog/2026/08/01/diffusion-latent-dit/
alternate_url: /en/blog/2026/08/01/diffusion-latent-dit/
alternate_lang: en
primary_category: ai-deep-learning
subcategory: generative-ai
series: 2025-generative-models
series_order: 5
post_type: study-note
difficulty: advanced
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_PRIMARY_SOURCE
tools: [Python, PyTorch]
hardware: []
software_versions: []
source_materials:
  - { title: Denoising Diffusion Probabilistic Models, type: paper, public_url: https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html, file_reference: NeurIPS 2020, pages: 6840-6851, used_for: DDPM objective }
  - { title: High-Resolution Image Synthesis with Latent Diffusion Models, type: paper, public_url: https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html, file_reference: CVPR 2022, pages: 10684-10695, used_for: latent diffusion }
  - { title: Scalable Diffusion Models with Transformers, type: paper, public_url: https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html, file_reference: ICCV 2023, pages: 4195-4205, used_for: DiT }
prerequisites: [vae, probability, unet, transformer]
learning_objectives: [forward process, noise prediction, latent diffusion, DiT backbone]
related_projects: []
related_posts: [gan-pix2pix]
tags: [ddpm, latent-diffusion, stable-diffusion, dit]
cover_image: /assets/images/learning/generative/diffusion.svg
thumbnail: /assets/images/learning/generative/diffusion.svg
image_alt: Diffusion forward noise와 reverse denoising, latent diffusion 흐름
draft: false
revision_history:
  - { date: 2026-08-01, change: "DDPM, LDM, DiT 원 논문을 한 흐름으로 연결" }
toc:
  - { id: forward, title: Forward process }
  - { id: reverse, title: Reverse process }
  - { id: training, title: Noise prediction 학습 }
  - { id: latent, title: Latent Diffusion과 DiT }
  - { id: rerun, title: 다시 실행할 순서 }
---

## Forward process {#forward}

깨끗한 (x_0)에 작은 Gaussian noise를 반복해 (x_T)를 단순한 분포에 가깝게 만든다.

<figure><img src="{{ '/assets/images/learning/generative/diffusion.svg' | relative_url }}" alt="Gaussian noise를 더하는 forward 과정과 학습한 reverse denoising 과정" width="1200" height="630"><figcaption>pixel space와 latent space에서 같은 denoising 아이디어가 어떻게 쓰이는지 비교했다.</figcaption></figure>

## Reverse process {#reverse}

생성은 noise에서 시작해 (T)에서 0까지 이동한다. 각 단계에서 모델이 분포의 mean이나 noise를 예측해 조금 더 깨끗한 sample을 만든다.

## Noise prediction 학습 {#training}

학습 때는 무작위 timestep을 고르고, 누적 계수로 (x_t)를 바로 만든 뒤 실제로 더한 ε과 모델 예측을 비교한다. sampling은 모든 timestep을 순서대로 거치므로 학습 한 step보다 오래 걸린다.

## Latent Diffusion과 DiT {#latent}

Latent Diffusion은 Autoencoder로 이미지를 압축한 공간에서 denoise하고 decoder로 복원한다. DiT는 같은 latent diffusion 문제에서 U-Net 대신 latent patch를 처리하는 Transformer를 쓴다.

## 다시 실행할 순서 {#rerun}

강의 Notebook에는 코드만 있고 출력 Cell은 비어 있었다. 먼저 FashionMNIST DDPM의 Tensor shape와 sampling loop를 확인하고, 그다음 encoder·decoder가 추가되는 latent diffusion으로 확장할 예정이다.
