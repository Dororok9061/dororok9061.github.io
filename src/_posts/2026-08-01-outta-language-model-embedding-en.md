---
title: OUTTA Basic — Connecting Language Models, Embeddings, and Autoencoders
title_en: OUTTA Basic — Connecting Language Models, Embeddings, and Autoencoders
description: I connected TF-IDF cosine similarity, dense embeddings, and an autoencoder latent space as different representation-learning tools.
date: 2026-08-01 10:04:00 +0900
updated: 2026-08-01 10:04:00 +0900
study_date: 2024-08-31
lang: en
translation_key: outta-language-model-embedding
permalink: /en/blog/2026/08/01/outta-language-model-embedding/
alternate_url: /blog/2026/08/01/outta-language-model-embedding/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: autoencoder-vae
series: outta-basic-2024
series_order: 4
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_NOTEBOOK_OUTPUTS
tools: [Python, PyTorch, scikit-learn, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: Basic Language Models, type: course-pdf, pages: "49", used_for: tokenization and next-token prediction }
  - { title: Word Embeddings and Autoencoders, type: course-pdf, pages: "28", used_for: dense representations and reconstruction }
prerequisites: [linear-algebra, neural-network]
learning_objectives: [compare sparse and dense representations, interpret cosine similarity, connect latent codes and reconstruction]
related_projects: []
related_posts: [outta-cnn-pytorch]
tags: [outta, language-model, tf-idf, embedding, autoencoder]
cover_image: /assets/images/learning/outta/notebook-40.webp
thumbnail: /assets/images/learning/outta/notebook-40.webp
image_alt: Heatmap of cosine similarities between TF-IDF document vectors
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected language representations and autoencoders to notebook figures }
toc:
  - { id: tokens, title: From tokens to probability }
  - { id: sparse, title: TF-IDF and cosine similarity }
  - { id: dense, title: Dense embeddings }
  - { id: autoencoder, title: Autoencoder latent space }
  - { id: code, title: Shape-checking code }
  - { id: compare, title: How I compared representations }
  - { id: navigation, title: Previous and next }
---

## From tokens to probability {#tokens}

I defined a language model as a distribution over the next token given previous tokens, not a device that stores complete sentences. The 49-page language-model module led me through vocabulary construction, integer indices, context windows, and shifted targets.

<p class="study-equation"><code>p(w₁…wₜ) = ∏ₜ p(wₜ | w before t)</code></p>

The same sentence becomes a different index sequence when the tokenizer or vocabulary changes. I therefore fixed padding and unknown-token indices and checked that embedding inputs used the `long` dtype.

## TF-IDF and cosine similarity {#sparse}

Before dense embeddings, I represented documents with TF-IDF. Cosine similarity compares direction rather than vector length. Bright cells in the heatmap connect documents with stronger vocabulary overlap.

<p class="study-equation"><code>cos(a, b) = aᵀb / (‖a‖₂‖b‖₂)</code></p>

<figure><img src="{{ '/assets/images/learning/outta/notebook-40.webp' | relative_url }}" alt="TF-IDF cosine-similarity heatmap for seven documents" width="408" height="456" loading="lazy"><figcaption>The bright symmetric cells reveal the closest document pairs.</figcaption></figure>

## Dense embeddings {#dense}

The 28-page embedding and autoencoder module replaced one-hot vectors with learned dense rows. `Embedding(vocab_size, embedding_dim)` appends an embedding axis to the input sequence. Cosine similarity still applies, but it now compares learned coordinates instead of raw counts.

<figure><img src="{{ '/assets/images/learning/outta/notebook-41.webp' | relative_url }}" alt="Embedding exercise loss falling rapidly with iteration count" width="567" height="432" loading="lazy"><figcaption>The retained curve drops sharply before settling near a low value.</figcaption></figure>

## Autoencoder latent space {#autoencoder}

An autoencoder compresses an input into a smaller latent code and reconstructs it. I initially confused this with PCA. PCA learns linear axes; nonlinear activations between an encoder and decoder can learn a curved representation.

<p class="study-equation"><code>z = fθ(x), x̂ = gφ(z), L = ‖x − x̂‖₂²</code></p>

<section class="project-gallery" aria-label="Autoencoder latent coordinates and reconstruction loss"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-42.webp' | relative_url }}" alt="Three Iris species colored in a two-dimensional latent scatter plot" width="559" height="413" loading="lazy"><figcaption>I checked whether the classes remained distinguishable after compression.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-43.webp' | relative_url }}" alt="Autoencoder reconstruction loss decreasing across about 180 iterations" width="576" height="432" loading="lazy"><figcaption>The reconstruction curve falls quickly and then flattens.</figcaption></figure>
</div></section>

## Shape-checking code {#code}

```python
token_ids = tokenizer(batch_text)          # (batch, time)
vectors = embedding(token_ids)             # (batch, time, dim)

latent = encoder(features)                 # (batch, latent_dim)
reconstruction = decoder(latent)           # (batch, feature_dim)

assert vectors.shape[:2] == token_ids.shape
assert reconstruction.shape == features.shape
```

## How I compared representations {#compare}

TF-IDF is easy to connect to overlapping words. An embedding stores contextual similarity in a compact dense vector. An autoencoder latent code compresses information needed for reconstruction. I treated them as tools with different objectives and interpretation methods, not as interchangeable answers.

## Previous and next {#navigation}

- Previous: [PyTorch CNN and handwritten-digit errors]({{ '/en/blog/2026/08/01/outta-cnn-pytorch/' | relative_url }})
- Next: [Time axes in RNNs and Seq2Seq]({{ '/en/blog/2026/08/01/outta-rnn-seq2seq/' | relative_url }})
