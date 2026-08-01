---
layout: course-day
course_id: 2025-generative-models
day: 5
title: 2025 Generative Models Intensive Day 5
description: Notes connecting DDPM forward and reverse processes, latent diffusion, Stable Diffusion, and DiT.
permalink: /en/learning/bootcamps/kaist-generative-models-2025/day-5/
lang: en
alternate_url: /learning/bootcamps/kaist-generative-models-2025/day-5/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/generative/diffusion.svg' | relative_url }}" alt="Forward noise, learned reverse denoising, and latent diffusion" width="1200" height="630"><figcaption>I redrew the two diffusion processes and the latent-space boundary in one diagram.</figcaption></figure>

## Forward process

Small Gaussian perturbations move (x_0) toward a standard normal sample. A cumulative coefficient produces an arbitrary (x_t) directly during training instead of replaying every earlier step.

## Reverse process

In [DDPM](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html), a U-Net receives (x_t) and (t) and predicts noise. Training samples one timestep, but generation walks from (T) back to zero and is therefore sequential.

## Latent diffusion and DiT

[Latent Diffusion](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html) performs denoising in an autoencoder's compressed space and uses cross-attention for conditions such as text. [DiT](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html) keeps the diffusion objective but replaces the U-Net backbone with a transformer over latent patches.

The course diffusion notebook retained code but no output cells. I will first rerun a small FashionMNIST DDPM and record tensor shapes and the sampling loop before moving to latent diffusion.
