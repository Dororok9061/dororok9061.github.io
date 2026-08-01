---
layout: course-day
course_id: 2025-generative-models
day: 3
title: 2025 Generative Models Intensive Day 3
description: Notes on the VAE encoder, reparameterization, reconstruction, and KL divergence.
permalink: /en/learning/bootcamps/kaist-generative-models-2025/day-3/
lang: en
alternate_url: /learning/bootcamps/kaist-generative-models-2025/day-3/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/generative/vae.svg' | relative_url }}" alt="VAE encoder predicting mean and variance before sampling a latent code" width="1200" height="630"><figcaption>The encoder predicts a latent distribution rather than a single coordinate.</figcaption></figure>

## From an autoencoder to a VAE

A VAE predicts the mean and variance of (q_\phi(z|x)). I reread [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) to connect the approximate posterior, prior, and lower bound.

## Reparameterization

`z = mu + std * eps` does not remove randomness. It moves the random variable outside the learned parameters so gradients can reach both `mu` and `std`.

## Two loss terms

Reconstruction preserves information from the input; KL divergence discourages the posterior from drifting too far from the prior. Overweighting the KL term can lead the decoder to ignore the latent code.

The saved latent-interpolation output was unavailable, so I stopped at the architecture and loss path and will rerun that comparison separately.
