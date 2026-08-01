---
title: Starting with Generative Models and Data Distributions
title_en: Starting with Generative Models and Data Distributions
description: My notes comparing discriminative and generative models before checking tensor shapes and visualizing data.
date: 2026-08-01 09:01:00 +0900
updated: 2026-08-01 09:01:00 +0900
study_date: 2025-07-07
lang: en
translation_key: generative-model-foundations
permalink: /en/blog/2026/08/01/generative-model-foundations/
alternate_url: /blog/2026/08/01/generative-model-foundations/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: generative-ai
series: 2025-generative-models
series_order: 1
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_PRIMARY_SOURCE
tools: [Python, PyTorch, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: PyTorch Learn the Basics, type: official-documentation, public_url: https://docs.pytorch.org/tutorials/beginner/basics/intro.html, file_reference: official tutorial, pages: "", used_for: tensor and training workflow }
prerequisites: [probability, python]
learning_objectives: [generation versus discrimination, tensor shapes, visualization before modeling]
related_projects: []
related_posts: []
tags: [generative-ai, pytorch, tensor, data-visualization]
cover_image: /assets/images/learning/generative/overview.svg
thumbnail: /assets/images/learning/generative/overview.svg
image_alt: Flow from observed data through distribution learning to new samples
draft: false
revision_history:
  - { date: 2026-08-01, change: Written from course notes and official documentation }
toc:
  - { id: question, title: First question }
  - { id: distribution, title: Learning a distribution }
  - { id: shape, title: Tensor shapes }
  - { id: data, title: Plotting the data }
  - { id: next, title: Next connection }
---

## First question {#question}

I reframed generation as approximating the distribution of observed (x) and sampling from it, rather than simply producing an image.

<figure><img src="{{ '/assets/images/learning/generative/overview.svg' | relative_url }}" alt="Data, distribution learning, model, and sample flow" width="1200" height="630"><figcaption>The model approximates a distribution rather than storing a lookup table.</figcaption></figure>

## Learning a distribution {#distribution}

Classification focuses on a conditional such as (p(y|x)); generation works with (p(x)) or a joint distribution. This made autoregressive models, VAEs, GANs, and diffusion comparable under one question.

## Tensor shapes {#shape}

I printed `(N, C, H, W)` before building the model and checked the feature count after flattening. Silent broadcasting can produce a numeric loss with the wrong meaning.

## Plotting the data {#data}

I inspected class balance, ranges, missing values, and duplicates. Normalization statistics came only from the training split to avoid leakage.

## Next connection {#next}

The next note factorizes a difficult joint distribution and converts maximum likelihood into a trainable loss.
