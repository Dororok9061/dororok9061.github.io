---
title: OUTTA Basic — Neural Networks for Function Approximation and Nonlinear Classification
title_en: OUTTA Basic — Neural Networks for Function Approximation and Nonlinear Classification
description: I compared sigmoid-basis function approximation, spiral decision boundaries, and a stalled classifier to understand network capacity and training failure.
date: 2026-08-01 10:02:00 +0900
updated: 2026-08-01 10:02:00 +0900
study_date: 2024-08-31
lang: en
translation_key: outta-neural-network-classification
permalink: /en/blog/2026/08/01/outta-neural-network-classification/
alternate_url: /blog/2026/08/01/outta-neural-network-classification/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: discriminative-models
series: outta-basic-2024
series_order: 2
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_NOTEBOOK_OUTPUTS
tools: [Python, PyTorch, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: Artificial Neural Networks, type: course-pdf, pages: "71", used_for: "perceptrons, activations, and backpropagation" }
prerequisites: [linear-regression, gradient-descent]
learning_objectives: [approximate with basis functions, classify spiral data, read failed learning curves]
related_projects: []
related_posts: [outta-data-autodiff-regression]
tags: [outta, neural-network, universal-approximation, classification, decision-boundary]
cover_image: /assets/images/learning/outta/notebook-30.webp
thumbnail: /assets/images/learning/outta/notebook-30.webp
image_alt: Nonlinear decision boundary learned for three spiral classes
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected the neural-network module to retained notebook outputs }
toc:
  - { id: approximation, title: Sigmoid as a basis }
  - { id: backprop, title: Loss and backpropagation }
  - { id: spiral, title: Classifying spiral data }
  - { id: failure, title: Reading a failed run }
  - { id: code, title: Minimal classifier }
  - { id: takeaway, title: Checks I kept }
  - { id: navigation, title: Previous and next }
---

## Sigmoid as a basis {#approximation}

I stopped thinking of a network only as a neuron count and rewrote it as transformations followed by a weighted sum. The activation section in the 71-page neural-network module led me to compare how weights and biases shift the slope and position of each sigmoid.

<section class="project-gallery" aria-label="Function approximation with sigmoid basis functions"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-20.webp' | relative_url }}" alt="Target cosine-like function and a poor initial approximation" width="559" height="413" loading="lazy"><figcaption>Before the basis functions were adjusted, the approximation missed the target curvature.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-21.webp' | relative_url }}" alt="Target periodic function and a closely matching learned approximation" width="559" height="413" loading="lazy"><figcaption>The weighted sigmoid combination reconstructed the target bends.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-23.webp' | relative_url }}" alt="Ten sigmoid basis functions with different positions and slopes" width="1198" height="790" loading="lazy"><figcaption>Simple units become a useful basis when their locations and directions differ.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-24.webp' | relative_url }}" alt="Several sigmoid curves and the full model output as a thick dashed line" width="546" height="436" loading="lazy"><figcaption>The thin basis curves combine into the dashed model output.</figcaption></figure>
</div></section>

The hidden-layer output became easier to connect to the figures when I wrote

<p class="study-equation"><code>ŷ(x) = Σⱼ vⱼσ(wⱼx + bⱼ) + c</code></p>

## Loss and backpropagation {#backprop}

I measured the distance between the approximation and target with mean squared error and propagated it to every parameter. The stored curve approaches zero near 2,000 epochs; I used the trend and oscillation rather than the epoch count alone.

<figure><img src="{{ '/assets/images/learning/outta/notebook-22.webp' | relative_url }}" alt="Training loss decreasing over two thousand function-approximation epochs" width="567" height="432" loading="lazy"><figcaption>The loss retained some early noise while its overall trend fell toward zero.</figcaption></figure>

## Classifying spiral data {#spiral}

The three-class spiral made the need for hidden nonlinear layers visible. I passed logits, not softmax probabilities, to `CrossEntropyLoss` and printed the `(batch, 3)` output shape first. As training progressed, the boundary bent between the intertwined classes.

<section class="project-gallery" aria-label="Spiral training curves and decision boundary"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-25.webp' | relative_url }}" alt="Three colored classes intertwined in a spiral dataset" width="583" height="435" loading="lazy"><figcaption>No single straight line can separate these classes.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-26.webp' | relative_url }}" alt="Spiral-classification loss decreasing over one thousand epochs" width="567" height="432" loading="lazy"><figcaption>Batch noise remained, but the loss trend moved downward.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-27.webp' | relative_url }}" alt="Spiral-classification accuracy increasing over one thousand epochs" width="567" height="432" loading="lazy"><figcaption>Accuracy improved with substantial per-step variation.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-28.webp' | relative_url }}" alt="Longer spiral-classification loss curve through six thousand epochs" width="567" height="436" loading="lazy"><figcaption>Extending training did not remove the small oscillations.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-29.webp' | relative_url }}" alt="Noisy spiral-classification accuracy through six thousand epochs" width="567" height="432" loading="lazy"><figcaption>The width of the curve mattered alongside its peak value.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-30.webp' | relative_url }}" alt="A neural-network boundary following the three spiral classes" width="559" height="435" loading="lazy"><figcaption>The nonlinear boundary follows the inner and outer turns of the spiral.</figcaption></figure>
</div></section>

## Reading a failed run {#failure}

A second spiral experiment stayed near loss 1.10 and accuracy 1/3, the random level for three classes. I checked whether an activation was missing, whether labels used `long`, and whether the optimizer held the current model parameters.

<section class="project-gallery" aria-label="Stalled training and an unsuitable decision boundary"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-31.webp' | relative_url }}" alt="A second three-class spiral dataset" width="583" height="435" loading="lazy"><figcaption>Similar-looking inputs still require an independent training check.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-32.webp' | relative_url }}" alt="Training loss oscillating near 1.10 without improving" width="585" height="438" loading="lazy"><figcaption>The loss stalled near the three-class random baseline.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-33.webp' | relative_url }}" alt="Accuracy fixed at 0.333 for one thousand epochs" width="584" height="432" loading="lazy"><figcaption>The flat line shows that useful learning never began.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-34.webp' | relative_url }}" alt="Coarse decision regions that do not follow the spiral geometry" width="559" height="435" loading="lazy"><figcaption>The learned regions fail to represent the intertwined structure.</figcaption></figure>
</div></section>

## Minimal classifier {#code}

```python
model = torch.nn.Sequential(
    torch.nn.Linear(2, 32),
    torch.nn.Tanh(),
    torch.nn.Linear(32, 32),
    torch.nn.Tanh(),
    torch.nn.Linear(32, 3),
)

logits = model(features)
assert logits.shape == (features.shape[0], 3)
loss = torch.nn.functional.cross_entropy(logits, labels.long())
```

## Checks I kept {#takeaway}

I read loss, accuracy, and the decision boundary together. If only one looked good, I returned to the model, labels, and split. The retained outputs cover both a useful nonlinear boundary and a stalled network, which made the contrast more instructive than a success-only summary.

## Previous and next {#navigation}

- Previous: [Data exploration, autodiff, and regression]({{ '/en/blog/2026/08/01/outta-data-autodiff-regression/' | relative_url }})
- Next: [Building a CNN in PyTorch and reading error samples]({{ '/en/blog/2026/08/01/outta-cnn-pytorch/' | relative_url }})
