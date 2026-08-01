---
title: OUTTA Basic — Following the Time Axis in RNNs and Seq2Seq
title_en: OUTTA Basic — Following the Time Axis in RNNs and Seq2Seq
description: I revisited hidden states, sequence shapes, train-test divergence, and teacher forcing through retained RNN learning curves.
date: 2026-08-01 10:05:00 +0900
updated: 2026-08-01 10:05:00 +0900
study_date: 2024-08-31
lang: en
translation_key: outta-rnn-seq2seq
permalink: /en/blog/2026/08/01/outta-rnn-seq2seq/
alternate_url: /blog/2026/08/01/outta-rnn-seq2seq/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: discriminative-models
series: outta-basic-2024
series_order: 5
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_NOTEBOOK_OUTPUTS
tools: [Python, PyTorch, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: RNN, type: course-pdf, pages: "38", used_for: "recurrence, hidden states, and Seq2Seq" }
prerequisites: [language-model, embedding, neural-network]
learning_objectives: [separate batch and time axes, read train-test divergence, connect encoder and decoder shapes]
related_projects: []
related_posts: [outta-language-model-embedding]
tags: [outta, rnn, seq2seq, recurrent-neural-network, teacher-forcing]
cover_image: /assets/images/learning/outta/notebook-44.webp
thumbnail: /assets/images/learning/outta/notebook-44.webp
image_alt: RNN training accuracy rising while test accuracy stays near one half
draft: false
revision_history:
  - { date: 2026-08-01, change: Connected the RNN module to retained sequence-learning curves }
toc:
  - { id: recurrence, title: Start with the hidden-state equation }
  - { id: shapes, title: Batch and time axes }
  - { id: divergence, title: Train and test separate }
  - { id: dynamics, title: Reading different learning curves }
  - { id: seq2seq, title: Connecting encoder and decoder }
  - { id: code, title: Minimal unpacked example }
  - { id: navigation, title: Previous and next }
---

## Start with the hidden-state equation {#recurrence}

I described an RNN as a repeated transformation of the current input and previous hidden state, not as a model that remembers everything. The unrolled diagram in the 38-page RNN module helped me see that parameters are shared across timesteps.

<p class="study-equation"><code>hₜ = tanh(Wₓxₜ + Wₕhₜ₋₁ + b), oₜ = Wₒhₜ + c</code></p>

## Batch and time axes {#shapes}

The first notebook check was `(batch, time, feature)`. Without `batch_first=True`, the first two axes switch. A task may consume only the final timestep or pass all timestep outputs to a decoder.

Padded tokens need lengths or a mask so that they do not contribute to loss. I also checked the hidden-state shape `(layers * directions, batch, hidden)` when changing layer count or bidirectionality.

## Train and test separate {#divergence}

In the retained RNN figure, training accuracy approaches 1.0 while test accuracy stays near 0.5. More epochs do not close the gap; the pattern looks like memorization rather than improved generalization.

<figure><img src="{{ '/assets/images/learning/outta/notebook-44.webp' | relative_url }}" alt="RNN training accuracy rising for fifteen hundred epochs while test accuracy stays near one half" width="846" height="470" loading="lazy"><figcaption>The stored curve separates training progress from generalization.</figcaption></figure>

I returned to sequence length, splitting, class balance, hidden size, and dropout. Adjacent windows cut from the same source can also become overly similar when distributed across train and test.

## Reading different learning curves {#dynamics}

Other retained outputs showed loss decreasing while accuracy rose. A short series dipped, rebounded, and fell again; another loss curve decreased steadily. I learned to inspect the x-axis definition and sequence length before comparing plots directly.

<section class="project-gallery" aria-label="Several retained RNN learning curves"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-45.webp' | relative_url }}" alt="RNN loss decreasing and accuracy increasing across one hundred plotted intervals" width="855" height="470" loading="lazy"><figcaption>I checked that the two metrics moved consistently in opposite directions.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-46.webp' | relative_url }}" alt="A short sequence of values falling from one toward 0.85" width="556" height="413" loading="lazy"><figcaption>On a short axis, one rebound appears large, so the x-axis meaning matters.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-47.webp' | relative_url }}" alt="Sequence-model loss decreasing from 2.4 to below 0.8 over one hundred epochs" width="855" height="470" loading="lazy"><figcaption>The slope shows how the rate of improvement slows over time.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-48.webp' | relative_url }}" alt="A value near one that drops sharply toward zero after the tenth point" width="547" height="413" loading="lazy"><figcaption>The abrupt transition prompted checks of metric definition, masks, and length boundaries.</figcaption></figure>
</div></section>

## Connecting encoder and decoder {#seq2seq}

In Seq2Seq, an encoder reads the source and a decoder begins from `<bos>` to produce target tokens. I initially confused all encoder outputs with the final hidden state. Without attention, the final hidden state initializes the decoder; with teacher forcing, the target token becomes the next decoder input.

<p class="study-equation"><code>L = −Σₜ log p(yₜ | y before t, x)</code></p>

## Minimal unpacked example {#code}

```python
embedded = embedding(token_ids)             # (batch, time, dim)
encoder_output, hidden = encoder(embedded)

decoder_input = bos_tokens
logits = []
for target_step in range(target_length):
    step_vector = embedding(decoder_input).unsqueeze(1)
    step_output, hidden = decoder(step_vector, hidden)
    step_logits = projection(step_output[:, 0])
    logits.append(step_logits)
    decoder_input = target[:, target_step]  # teacher forcing

logits = torch.stack(logits, dim=1)         # (batch, time, vocab)
```

## Previous and next {#navigation}

- Previous: [Language models, embeddings, and autoencoders]({{ '/en/blog/2026/08/01/outta-language-model-embedding/' | relative_url }})
- Next: [Organizing BERT, Hugging Face, and Gemini safely]({{ '/en/blog/2026/08/01/outta-bert-huggingface-gemini/' | relative_url }})
