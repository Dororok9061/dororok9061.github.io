---
title: From GANs to Pix2Pix
title_en: From GANs to Pix2Pix
description: Notes connecting alternating generator and discriminator updates with Pix2Pix conditioning and L1 loss.
date: 2026-08-01 09:04:00 +0900
updated: 2026-08-01 09:04:00 +0900
study_date: 2025-07-10
lang: en
translation_key: gan-pix2pix
permalink: /en/blog/2026/08/01/gan-pix2pix/
alternate_url: /blog/2026/08/01/gan-pix2pix/
alternate_lang: ko
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
learning_objectives: [alternating optimization, gradient flow, conditional GAN and L1]
related_projects: []
related_posts: [vae-elbo]
tags: [gan, pix2pix, conditional-gan, unet]
cover_image: /assets/images/learning/generative/gan-pix2pix.svg
thumbnail: /assets/images/learning/generative/gan-pix2pix.svg
image_alt: Input, generator, generated output, discriminator, and Pix2Pix losses
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected the GAN and Pix2Pix papers }
toc:
  - { id: game, title: Two-model game }
  - { id: gradient, title: Gradient path }
  - { id: loss, title: Reading losses }
  - { id: pix2pix, title: Pix2Pix }
  - { id: rerun, title: Planned comparison }
---

## Two-model game {#game}

The generator produces samples while the discriminator distinguishes real from fake. Their different objectives require separate optimizer steps.

<figure><img src="{{ '/assets/images/learning/generative/gan-pix2pix.svg' | relative_url }}" alt="Generator, output, discriminator, and Pix2Pix loss flow" width="1200" height="630"><figcaption>Conditioning and L1 extend the adversarial game to paired image translation.</figcaption></figure>

## Gradient path {#gradient}

I detached generated samples during the discriminator update. The generator update preserved the path through D without changing D's parameters.

## Reading losses {#loss}

A small discriminator loss alone can be misleading. Generated samples, diversity, and both curves are needed to identify imbalance or mode collapse.

## Pix2Pix {#pix2pix}

Pix2Pix conditions both networks on the input. Adversarial loss rewards realistic structure, L1 preserves the paired target, and U-Net skips carry spatial detail.

## Planned comparison {#rerun}

The course output image was not saved. I will compare L1-only with adversarial-plus-L1 on the same paired dataset in a new run.
