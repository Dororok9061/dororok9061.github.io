---
layout: course-day
course_id: 2025-generative-models
day: 5
title: 2025 생성모델 집중과정 Day 5
description: DDPM의 forward·reverse process, latent diffusion, Stable Diffusion과 DiT를 연결한 기록.
permalink: /learning/bootcamps/kaist-generative-models-2025/day-5/
lang: ko
alternate_url: /en/learning/bootcamps/kaist-generative-models-2025/day-5/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/generative/diffusion.svg' | relative_url }}" alt="데이터에 잡음을 더하는 forward process와 잡음을 제거하는 reverse process, latent diffusion 흐름" width="1200" height="630"><figcaption>Diffusion의 두 process와 latent space에서 계산하는 흐름을 한 장에 다시 그렸다.</figcaption></figure>

## Forward process

깨끗한 (x_0)에 작은 Gaussian noise를 여러 번 더해 (x_T)를 표준정규분포에 가깝게 만든다. 중요한 점은 (x_t)를 만들기 위해 1단계부터 모두 반복하지 않고, 누적 계수 (\bar\alpha_t)를 사용해 임의 timestep의 noisy sample을 바로 만들 수 있다는 점이었다.

## Reverse process와 noise prediction

[DDPM 논문](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)의 구현에서는 U-Net이 (x_t)와 (t)를 받아 추가된 noise를 예측한다. 학습 때는 무작위 timestep 하나를 고를 수 있지만 sampling 때는 (T)에서 0까지 순서대로 denoise해야 하므로 느리다.

## Latent Diffusion

[Latent Diffusion 논문](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html)은 이미지를 Autoencoder의 latent로 압축한 뒤 그 공간에서 diffusion을 수행한다. pixel space보다 차원이 작아 계산량을 줄이면서 decoder가 이미지로 복원한다. text condition은 cross-attention을 통해 U-Net에 들어간다.

## Stable Diffusion과 DiT로 이어 보기

Stable Diffusion은 latent diffusion 계열의 text-to-image pipeline으로 이해했다. [DiT 논문](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html)은 latent patch를 다루는 Transformer로 U-Net backbone을 바꾼다. Diffusion의 확률 과정과 denoising objective는 유지되고, noise predictor의 구조가 달라진다.

## 다음 실행

Diffusion Notebook은 코드 구조까지만 남아 있고 출력 Cell은 비어 있었다. 먼저 작은 FashionMNIST DDPM에서 tensor shape와 sampling loop를 다시 확인한 뒤, latent diffusion의 encoder·decoder 경계를 같은 방식으로 기록할 예정이다.
