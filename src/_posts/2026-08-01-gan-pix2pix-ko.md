---
title: GAN에서 Pix2Pix까지
title_en: From GANs to Pix2Pix
description: Generator·Discriminator의 교대학습과 Pix2Pix의 조건·L1 loss를 연결한 기록.
date: 2026-08-01 09:04:00 +0900
updated: 2026-08-01 09:04:00 +0900
study_date: 2025-07-10
lang: ko
translation_key: gan-pix2pix
permalink: /blog/2026/08/01/gan-pix2pix/
alternate_url: /en/blog/2026/08/01/gan-pix2pix/
alternate_lang: en
primary_category: ai-deep-learning
subcategory: generative-ai
series: 2025-generative-models
series_order: 4
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_PRIMARY_SOURCE
tools: [Python, PyTorch]
hardware: []
software_versions: []
source_materials:
  - { title: Generative Adversarial Nets, type: paper, public_url: https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html, file_reference: NeurIPS 2014, pages: 2672-2680, used_for: minimax objective }
  - { title: Image-to-Image Translation with Conditional Adversarial Networks, type: paper, public_url: https://openaccess.thecvf.com/content_cvpr_2017/html/Isola_Image-To-Image_Translation_With_CVPR_2017_paper.html, file_reference: CVPR 2017, pages: 1125-1134, used_for: Pix2Pix architecture }
prerequisites: [cnn, backpropagation]
learning_objectives: [alternating optimization, detach and gradient flow, conditional GAN and L1]
related_projects: []
related_posts: [vae-elbo]
tags: [gan, pix2pix, conditional-gan, unet]
cover_image: /assets/images/learning/generative/gan-pix2pix.svg
thumbnail: /assets/images/learning/generative/gan-pix2pix.svg
image_alt: 입력에서 Generator와 Discriminator를 거쳐 Pix2Pix loss를 계산하는 구조
draft: false
revision_history:
  - { date: 2026-08-01, change: GAN과 Pix2Pix 원 논문을 연결 }
toc:
  - { id: game, title: 두 모델의 게임 }
  - { id: gradient, title: Gradient 경로 }
  - { id: loss, title: Loss 읽기 }
  - { id: pix2pix, title: Pix2Pix }
  - { id: rerun, title: 비교할 실험 }
---

## 두 모델의 게임 {#game}

Generator는 가짜 표본을 만들고 Discriminator는 real과 fake를 구분한다. 두 optimizer가 서로 다른 목적을 갖기 때문에 한 번의 backward로 끝나지 않는다.

<figure><img src="{{ '/assets/images/learning/generative/gan-pix2pix.svg' | relative_url }}" alt="Generator, 생성 결과, Discriminator와 Pix2Pix loss 흐름" width="1200" height="630"><figcaption>입력 조건과 L1 항이 GAN을 paired image translation으로 확장한다.</figcaption></figure>

## Gradient 경로 {#gradient}

D를 학습할 때 생성 결과를 detach하고, G를 학습할 때는 D를 통과한 gradient가 G까지 가도록 했다. 두 단계의 `zero_grad`, `backward`, `step` 순서를 따로 적어 보니 parameter가 어디서 바뀌는지 명확해졌다.

## Loss 읽기 {#loss}

D loss 하나만 작아지는 것은 좋은 신호가 아닐 수 있다. 생성 표본의 다양성과 품질, G·D loss를 같이 봐야 mode collapse나 지나치게 강한 D를 찾을 수 있다.

## Pix2Pix {#pix2pix}

Pix2Pix는 입력 영상을 G와 D 양쪽에 조건으로 준다. adversarial loss는 사실감을, L1은 paired target과의 전체 형상 일치를 돕는다. U-Net skip은 공간 정보를 출력 쪽으로 넘긴다.

## 비교할 실험 {#rerun}

당시 결과 이미지는 찾지 못했다. 같은 paired dataset에서 L1-only와 adversarial+L1 결과를 현재 환경에서 나란히 그리는 것이 다음 단계다.
