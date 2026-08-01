---
title: From DDPM to Latent Diffusion and DiT
title_en: From DDPM to Latent Diffusion and DiT
description: Notes connecting forward noise, reverse denoising, latent space, and a transformer backbone.
date: 2026-08-01 09:05:00 +0900
updated: 2026-08-01 09:05:00 +0900
study_date: 2025-07-11
lang: en
translation_key: diffusion-latent-dit
permalink: /en/blog/2026/08/01/diffusion-latent-dit/
alternate_url: /blog/2026/08/01/diffusion-latent-dit/
alternate_lang: ko
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
image_alt: Diffusion forward noise, reverse denoising, and latent-space flow
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected the DDPM, LDM, and DiT papers }
toc:
  - { id: forward, title: Forward process }
  - { id: reverse, title: Reverse process }
  - { id: training, title: Noise prediction }
  - { id: latent, title: Latent diffusion and DiT }
  - { id: rerun, title: Rerun order }
---

## Forward process {#forward}

Repeated Gaussian perturbations move clean (x_0) toward a simple (x_T) distribution.

<figure><img src="{{ '/assets/images/learning/generative/diffusion.svg' | relative_url }}" alt="Forward Gaussian noise, reverse denoising, and latent diffusion" width="1200" height="630"><figcaption>I compared the same denoising idea in pixel and latent spaces.</figcaption></figure>

## Reverse process {#reverse}

Generation starts from noise and moves from (T) toward zero. The model predicts a distribution parameter or the added noise at each step.

## Noise prediction {#training}

Training samples a timestep and constructs (x_t) directly with cumulative coefficients. Sampling remains sequential over all timesteps.

## Latent diffusion and DiT {#latent}

Latent diffusion denoises inside an autoencoder representation and decodes the image afterward. DiT replaces the U-Net noise predictor with a transformer over latent patches.

## Rerun order {#rerun}

The course notebook retained code but no outputs. I will first check tensor shapes and the sampling loop on FashionMNIST, then add the latent encoder and decoder boundary.
