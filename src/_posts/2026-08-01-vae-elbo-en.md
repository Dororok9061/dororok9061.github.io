---
title: VAE ELBO and Reparameterization
title_en: VAE ELBO and Reparameterization
description: Notes on why the encoder predicts a mean and variance and how reconstruction and KL losses interact.
date: 2026-08-01 09:03:00 +0900
updated: 2026-08-01 09:03:00 +0900
study_date: 2025-07-09
lang: en
translation_key: vae-elbo
permalink: /en/blog/2026/08/01/vae-elbo/
alternate_url: /blog/2026/08/01/vae-elbo/
alternate_lang: ko
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
image_alt: VAE encoder predicting a mean and variance before decoding a latent sample
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected course notes with the original VAE paper }
toc:
  - { id: latent, title: From a point to a distribution }
  - { id: trick, title: Reparameterization }
  - { id: loss, title: Two loss terms }
  - { id: shape, title: Shape checks }
  - { id: rerun, title: Next rerun }
---

## From a point to a distribution {#latent}

The VAE encoder predicts the mean and log variance of (q_\phi(z|x)), not one fixed latent code.

<figure><img src="{{ '/assets/images/learning/generative/vae.svg' | relative_url }}" alt="VAE input, encoder, mean, variance, latent code, and decoder" width="1200" height="630"><figcaption>I separated learned parameters from the random sample.</figcaption></figure>

## Reparameterization {#trick}

`z = mu + std * eps` moves randomness outside the learned parameters so gradients can reach `mu` and `std`.

## Two loss terms {#loss}

Reconstruction preserves input information; KL divergence keeps the posterior near the prior. Poor weighting can produce weak reconstructions or posterior collapse.

## Shape checks {#shape}

I verified that `mu`, `logvar`, `eps`, and `z` all use `(batch, latent_dim)` and made the KL reductions explicit.

## Next rerun {#rerun}

The latent-interpolation output was not saved. I will vary β and plot reconstruction against latent continuity in a new run.
