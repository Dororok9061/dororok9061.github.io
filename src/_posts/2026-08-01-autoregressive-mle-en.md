---
title: Autoregressive Factorization and MLE
title_en: Autoregressive Factorization and MLE
description: Notes connecting joint-probability factorization, teacher forcing, log-likelihood, and cross entropy.
date: 2026-08-01 09:02:00 +0900
updated: 2026-08-01 09:02:00 +0900
study_date: 2025-07-08
lang: en
translation_key: autoregressive-mle
permalink: /en/blog/2026/08/01/autoregressive-mle/
alternate_url: /blog/2026/08/01/autoregressive-mle/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: generative-ai
series: 2025-generative-models
series_order: 2
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_PRIMARY_SOURCE
tools: [Python, PyTorch]
hardware: []
software_versions: []
source_materials:
  - { title: Pixel Recurrent Neural Networks, type: paper, public_url: https://proceedings.mlr.press/v48/oord16.html, file_reference: PMLR paper, pages: 1747-1756, used_for: autoregressive image factorization }
prerequisites: [conditional-probability, logarithms]
learning_objectives: [joint factorization, teacher forcing, negative log-likelihood]
related_projects: []
related_posts: [generative-model-foundations]
tags: [autoregressive, mle, nll, teacher-forcing]
cover_image: /assets/images/learning/generative/autoregressive-mle.svg
thumbnail: /assets/images/learning/generative/autoregressive-mle.svg
image_alt: Sequential conditional prediction and summed log probabilities
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected course notes with the PixelRNN paper }
toc:
  - { id: factorization, title: Factorizing the joint }
  - { id: train, title: Training versus generation }
  - { id: mle, title: MLE as a loss }
  - { id: code, title: Code checks }
  - { id: limit, title: Sequential cost }
---

## Factorizing the joint {#factorization}

(p(x_1,ldots,x_T)=\prod_t p(x_t|x_{&lt;t})) reduces a joint model to repeated next-value prediction.

<figure><img src="{{ '/assets/images/learning/generative/autoregressive-mle.svg' | relative_url }}" alt="Conditional sequence and negative log-likelihood" width="1200" height="630"><figcaption>The probability chain rule and the training loss describe the same path.</figcaption></figure>

## Training versus generation {#train}

Teacher forcing provides the true prefix during training. Generation must reuse model samples, so early errors can propagate. A causal mask prevents access to future tokens.

## MLE as a loss {#mle}

Logs convert products to sums. Negating the maximization objective produces NLL, and cross entropy selects the target class log probability.

## Code checks {#code}

I shifted inputs and targets by one step, checked the vocabulary axis, and masked padding tokens out of the loss.

## Sequential cost {#limit}

Sampling remains sequential over long outputs, motivating comparisons with latent-variable and diffusion approaches.
