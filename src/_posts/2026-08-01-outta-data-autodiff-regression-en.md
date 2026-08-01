---
title: OUTTA Basic — From Data Exploration to Autodiff and Linear Regression
title_en: OUTTA Basic — From Data Exploration to Autodiff and Linear Regression
description: I revisited scatter plots, loss surfaces, gradient descent, and normalization using the linear-regression outputs retained in my notebook.
date: 2026-08-01 10:01:00 +0900
updated: 2026-08-01 10:01:00 +0900
study_date: 2024-08-31
lang: en
translation_key: outta-data-autodiff-regression
permalink: /en/blog/2026/08/01/outta-data-autodiff-regression/
alternate_url: /blog/2026/08/01/outta-data-autodiff-regression/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: machine-learning-basics
series: outta-basic-2024
series_order: 1
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_NOTEBOOK_OUTPUTS
tools: [Python, NumPy, PyTorch, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: Machine Learning Basics and Linear Regression, type: course-pdf, pages: "39", used_for: regression and loss functions }
  - { title: Gradient Descent, type: course-pdf, pages: "25", used_for: autodiff and parameter updates }
prerequisites: [python, algebra]
learning_objectives: [plot relationships first, understand autodiff, connect regression loss and normalization]
related_projects: []
related_posts: []
tags: [outta, linear-regression, gradient-descent, autodiff, normalization]
cover_image: /assets/images/learning/outta/notebook-12.webp
thumbnail: /assets/images/learning/outta/notebook-12.webp
image_alt: Learned and reference regression lines over NBA body measurements
draft: false
revision_history:
  - { date: 2026-08-01, change: Written from course modules and retained notebook outputs }
toc:
  - { id: inspect, title: Why I plotted first }
  - { id: relation, title: Reading relationships }
  - { id: surface, title: Loss surfaces and autodiff }
  - { id: normalize, title: Normalization and convergence }
  - { id: errors, title: What stored errors taught me }
  - { id: code, title: Minimal regression loop }
  - { id: navigation, title: Previous and next }
---

## Why I plotted first {#inspect}

I began by plotting the inputs instead of memorizing a regression formula. After reading the 39-page regression module, I compared hand length, hand width, height, weight, and wingspan in the NBA draft measurements notebook. I checked the direction of each point cloud and noticed that a categorical axis such as position needs different handling from a continuous input.

<section class="project-gallery" aria-label="NBA measurement exploration plots"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-01.webp' | relative_url }}" alt="Scatter plot of hand length and hand width for 2019 NBA draftees" width="576" height="455" loading="lazy"><figcaption>Hand width generally increases with hand length.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-02.webp' | relative_url }}" alt="Two scatter plots of height and weight grouped by player position" width="571" height="455" loading="lazy"><figcaption>The crowded categorical labels exposed a plotting problem before modeling began.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-03.webp' | relative_url }}" alt="A second hand-length and hand-width scatter plot with a simplified layout" width="556" height="435" loading="lazy"><figcaption>I redrew the same relationship to check titles, axes, and ranges.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-04.webp' | relative_url }}" alt="The squared function from minus ten to ten" width="552" height="439" loading="lazy"><figcaption>I inspected the curvature and minimum of (x^2) before the differentiation exercise.</figcaption></figure>
</div></section>

## Reading relationships {#relation}

Height and wingspan showed a roughly linear relationship. I first predicted the direction from the scatter alone, then overlaid a line and repeated the plot through a second implementation. Matching axes and units mattered more than making the plot decorative.

<section class="project-gallery" aria-label="Height, wingspan, and fitted-line plots"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-05.webp' | relative_url }}" alt="Positive relationship between NBA player height and wingspan" width="553" height="435" loading="lazy"><figcaption>I inspected direction and outliers before adding a fitted line.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-06.webp' | relative_url }}" alt="First linear fit over the height and wingspan scatter" width="543" height="435" loading="lazy"><figcaption>The slope and intercept place the line through the center of the point cloud.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-07.webp' | relative_url }}" alt="Wingspan versus height scatter plot with explicit axis labels" width="572" height="455" loading="lazy"><figcaption>The labels make the input and target roles explicit.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-08.webp' | relative_url }}" alt="A second implementation of the height and wingspan regression line" width="543" height="435" loading="lazy"><figcaption>Reproducing the same line cross-checked the selected columns and formula.</figcaption></figure>
</div></section>

I wrote the model as <code>ŷ = mx + b</code> and the mean squared error as

<p class="study-equation"><code>L(m, b) = (1/N) Σᵢ(mxᵢ + b − yᵢ)²</code></p>

## Loss surfaces and autodiff {#surface}

While reading the 25-page gradient-descent module, I plotted loss against (m) and (b). The phrase “move downhill” initially felt separate from `loss.backward()`. Marking the current point and update path on the surface connected the gradient to a direction in parameter space.

<section class="project-gallery" aria-label="Loss surfaces and gradient paths"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-09.webp' | relative_url }}" alt="Linear-regression loss surface over slope and intercept with the current point marked" width="389" height="389" loading="lazy"><figcaption>The marker locates the current parameters on the loss surface.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-10.webp' | relative_url }}" alt="Loss, slope, and intercept across ten updates" width="990" height="1190" loading="lazy"><figcaption>A large first step reduced loss but made the parameters oscillate.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-11.webp' | relative_url }}" alt="Several gradient-descent points on a regression loss surface" width="389" height="389" loading="lazy"><figcaption>The updates move toward the low region of the surface.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-13.webp' | relative_url }}" alt="Multiple update paths descending the same regression surface" width="389" height="389" loading="lazy"><figcaption>Initialization and step size produce different paths on the same objective.</figcaption></figure>
</div></section>

## Normalization and convergence {#normalize}

The scale of height and wingspan also changed the gradient scale. I subtracted the mean and divided by the standard deviation, then studied the same model again. These figures are outputs retained in the notebook from that work; I did not present them as a fresh rerun.

<section class="project-gallery" aria-label="Regression comparisons and normalized training"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-12.webp' | relative_url }}" alt="Learned and reference fits over the height and wingspan scatter" width="572" height="432" loading="lazy"><figcaption>Overlaying the two lines made the slope difference visible.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-14.webp' | relative_url }}" alt="Several learned regression lines and a dashed reference line" width="572" height="432" loading="lazy"><figcaption>I compared whether different paths converged to similar fits.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-15.webp' | relative_url }}" alt="Scatter plot of normalized height and normalized wingspan" width="565" height="455" loading="lazy"><figcaption>Normalization changes coordinates without removing the relationship.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-16.webp' | relative_url }}" alt="Loss, slope, and intercept stabilizing over fifty updates" width="989" height="1190" loading="lazy"><figcaption>After normalization, loss and both parameters settle smoothly.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-17.webp' | relative_url }}" alt="Mean-squared-error surface for the normalized regression problem" width="392" height="389" loading="lazy"><figcaption>The update point is easier to read around the normalized minimum.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-18.webp' | relative_url }}" alt="Positive correlation between two normalized measurements" width="546" height="414" loading="lazy"><figcaption>The centered coordinates preserve the positive trend.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-19.webp' | relative_url }}" alt="Height and wingspan scatter restored to the original units" width="553" height="413" loading="lazy"><figcaption>I returned to physical units to interpret the fitted relationship.</figcaption></figure>
</div></section>

## What stored errors taught me {#errors}

My edited regression notebook retained 30 output objects, 13 figures, and three error outputs. I kept those failures in the study record and checked tensor dtype and shape, `requires_grad`, and the order of the update and gradient reset. Forgetting `zero_grad()` causes gradients to accumulate across iterations.

## Minimal regression loop {#code}

```python
m = torch.zeros((), requires_grad=True)
b = torch.zeros((), requires_grad=True)

for _ in range(50):
    prediction = m * x + b
    loss = ((prediction - y) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        m -= learning_rate * m.grad
        b -= learning_rate * b.grad
        m.grad.zero_()
        b.grad.zero_()
```

The loop stays short but preserves forward, loss, backward, update, and reset. The next note moves from a line to function approximation and nonlinear spiral classification.

## Previous and next {#navigation}

- Previous: [2024 OUTTA AI Bootcamp Basic]({{ '/en/learning/bootcamps/outta-basic-2024/' | relative_url }})
- Next: [Function approximation and nonlinear classification]({{ '/en/blog/2026/08/01/outta-neural-network-classification/' | relative_url }})
