---
layout: course-day
course_id: 2025-generative-models
day: 2
title: 2025 Generative Models Intensive Day 2
description: Notes connecting autoregressive factorization, teacher forcing, maximum likelihood, and NLL.
permalink: /en/learning/bootcamps/kaist-generative-models-2025/day-2/
lang: en
alternate_url: /learning/bootcamps/kaist-generative-models-2025/day-2/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/generative/autoregressive-mle.svg' | relative_url }}" alt="Autoregressive sequence and negative log-likelihood" width="1200" height="630"><figcaption>Joint-probability factorization and NLL are two views of the same training path.</figcaption></figure>

## Factorizing a joint distribution

(p(x_1, ldots, x_T)=\prod_t p(x_t|x_{&lt;t})) turns a high-dimensional problem into next-value prediction. [PixelRNN](https://proceedings.mlr.press/v48/oord16.html) applies this view over two image axes.

## Teacher forcing

Training can feed the true prefix, while generation must reuse model samples. Early mistakes can therefore propagate. A causal Transformer uses the same dependency rule even though its training operations are parallelized.

## From MLE to a loss

Taking logs turns products into sums. Negating the objective converts maximization into a negative log-likelihood loss; cross entropy selects the log probability assigned to the target class.

The next step was handling a latent variable whose posterior is not directly tractable.
