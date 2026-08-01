---
title: OUTTA Basic — PyTorch CNN and Handwritten-Digit Error Analysis
title_en: OUTTA Basic — PyTorch CNN and Handwritten-Digit Error Analysis
description: I traced convolution shapes and read retained loss, accuracy, correct-sample, and misclassification plots together.
date: 2026-08-01 10:03:00 +0900
updated: 2026-08-01 10:03:00 +0900
study_date: 2024-08-31
lang: en
translation_key: outta-cnn-pytorch
permalink: /en/blog/2026/08/01/outta-cnn-pytorch/
alternate_url: /blog/2026/08/01/outta-cnn-pytorch/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: cnn
series: outta-basic-2024
series_order: 3
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_NOTEBOOK_OUTPUTS
tools: [Python, PyTorch, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: CNN, type: course-pdf, pages: "92", used_for: "convolution, pooling, and image classification" }
  - { title: Dataset and DataLoader, type: course-pdf, pages: "14", used_for: batches and data splits }
  - { title: Transfer Learning, type: course-pdf, pages: "26", used_for: feature extraction and fine-tuning }
prerequisites: [neural-network, pytorch]
learning_objectives: [calculate convolution output shapes, read loss and accuracy together, inspect misclassified images]
related_projects: []
related_posts: [outta-neural-network-classification]
tags: [outta, cnn, pytorch, image-classification, error-analysis]
cover_image: /assets/images/learning/outta/notebook-39.webp
thumbnail: /assets/images/learning/outta/notebook-39.webp
image_alt: Twenty-five handwritten digits with different predicted and true labels
draft: false
revision_history:
  - { date: 2026-08-01, change: Written from the CNN module and retained classification outputs }
toc:
  - { id: shape, title: Start with convolution shapes }
  - { id: samples, title: Inspect inputs first }
  - { id: curves, title: Read loss and accuracy together }
  - { id: errors, title: Correct and incorrect examples }
  - { id: code, title: Minimal CNN forward pass }
  - { id: transfer, title: Connection to transfer learning }
  - { id: navigation, title: Previous and next }
---

## Start with convolution shapes {#shape}

I studied a CNN through input and output shapes instead of memorizing filter diagrams. After checking kernel, stride, and padding in the 92-page CNN module, I used

<p class="study-equation"><code>H(out) = floor((H(in) + 2P − K) / S) + 1</code></p>

When a notebook tensor did not match the `Linear` input after flattening, I printed intermediate shapes and followed how convolution and pooling reduced the spatial dimensions.

## Inspect inputs first {#samples}

The 14-page Dataset and DataLoader module reminded me to plot samples beside labels before batching. The same digit can vary greatly in stroke width, tilt, and position. Accuracy alone cannot explain which variations are difficult.

<figure><img src="{{ '/assets/images/learning/outta/notebook-35.webp' | relative_url }}" alt="Sixteen handwritten digits arranged with their labels" width="639" height="658" loading="lazy"><figcaption>I inspected stroke shape and tilt before interpreting the classifier.</figcaption></figure>

## Read loss and accuracy together {#curves}

My edited CNN notebook had two code cells that differed from the base, plus 17 retained output objects and five figures. Its stored curves show an overall loss decrease and high accuracy, but a small validation set can move sharply when only one or two samples change.

<section class="project-gallery" aria-label="CNN loss and accuracy curves"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-36.webp' | relative_url }}" alt="CNN training loss decreasing overall across fifteen epochs" width="576" height="432" loading="lazy"><figcaption>The curve falls overall while preserving several mid-training increases.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-37.webp' | relative_url }}" alt="CNN accuracy fluctuating above 0.9 across fifteen epochs" width="576" height="432" loading="lazy"><figcaption>I read the high values together with sample count and variation.</figcaption></figure>
</div></section>

## Correct and incorrect examples {#errors}

The correctly predicted `1` has a clear vertical stroke. In the error grid, open loops, connected strokes, and tilted lines lead to confusions such as `5→3`, `4→9`, and `7→9`. Before adding layers, I would check normalization, cropping, and augmentation in that order.

<section class="project-gallery" aria-label="A correct CNN prediction and misclassification examples"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-38.webp' | relative_url }}" alt="A handwritten one correctly predicted as class one" width="416" height="456" loading="lazy"><figcaption>A simple vertical-stroke sample with matching prediction and truth.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-39.webp' | relative_url }}" alt="Twenty-five CNN mistakes labeled with predicted and true digits" width="794" height="812" loading="lazy"><figcaption>The grid exposes failure shapes hidden behind aggregate accuracy.</figcaption></figure>
</div></section>

## Minimal CNN forward pass {#code}

```python
class SmallCNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.features = torch.nn.Sequential(
            torch.nn.Conv2d(1, 16, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
            torch.nn.Conv2d(16, 32, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),
        )
        self.classifier = torch.nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        features = self.features(x)
        return self.classifier(features.flatten(1))
```

## Connection to transfer learning {#transfer}

The 26-page transfer-learning module separated training a small CNN from scratch from using a pretrained feature extractor. I wrote down the order as matching channel count, resize, and normalization to the backbone, training the classifier first, and leaving partial unfreezing for a later step. I have not counted that sequence as a fresh run here.

## Previous and next {#navigation}

- Previous: [Function approximation and nonlinear classification]({{ '/en/blog/2026/08/01/outta-neural-network-classification/' | relative_url }})
- Next: [Language models, embeddings, and autoencoders]({{ '/en/blog/2026/08/01/outta-language-model-embedding/' | relative_url }})
