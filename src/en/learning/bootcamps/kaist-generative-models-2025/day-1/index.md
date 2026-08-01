---
layout: course-day
course_id: 2025-generative-models
day: 1
title: 2025 Generative Models Intensive Day 1
description: My first-day notes on generative models, deep-learning foundations, and dataset visualization.
permalink: /en/learning/bootcamps/kaist-generative-models-2025/day-1/
lang: en
alternate_url: /learning/bootcamps/kaist-generative-models-2025/day-1/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/generative/overview.svg' | relative_url }}" alt="Flow from observed data through distribution learning to new samples" width="1200" height="630"><figcaption>I treated a generative model as a distribution learner, not an image lookup table.</figcaption></figure>

## Generation versus discrimination

A classifier focuses on a conditional such as (p(y|x)). A generative model works with (p(x)) or a joint distribution and samples a new (x). This view made the differences among autoregressive models, VAEs, GANs, and diffusion easier to compare.

## Tensor shapes first

I printed batch, channel, height, and width before constructing the network. A loss can still return a number when normalization or flattening uses the wrong axis, so shape checks came before tuning.

## Looking at the data

I inspected class balance, ranges, missing values, and duplicates before choosing a model. Preprocessing statistics belong to the training split; calculating them before the split leaks information.

## Next question

The next step was to ask whether a difficult joint distribution could be rewritten as a sequence of conditional probabilities.
