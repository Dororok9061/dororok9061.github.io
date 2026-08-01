---
title: OUTTA Basic — Organizing BERT, Hugging Face, and Gemini Safely
title_en: OUTTA Basic — Organizing BERT, Hugging Face, and Gemini Safely
description: I focused on tokenization, attention masks, BERT output shapes, and environment-based credential handling for Gemini.
date: 2026-08-01 10:06:00 +0900
updated: 2026-08-01 10:06:00 +0900
study_date: 2024-08-31
lang: en
translation_key: outta-bert-huggingface-gemini
permalink: /en/blog/2026/08/01/outta-bert-huggingface-gemini/
alternate_url: /blog/2026/08/01/outta-bert-huggingface-gemini/
alternate_lang: ko
primary_category: ai-deep-learning
subcategory: transformer
series: outta-basic-2024
series_order: 6
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_NOTEBOOK_OUTPUTS
tools: [Python, PyTorch, Transformers]
hardware: []
software_versions: []
source_materials:
  - { title: BERT, type: course-pdf, pages: "40", used_for: bidirectional attention and fine-tuning }
  - { title: GPT, type: course-pdf, pages: "28", used_for: causal language modeling }
  - { title: CV and NLP Research Trends, type: course-pdf, pages: "22", used_for: pretrained-model workflows }
  - { title: Issuing a Gemini API Key, type: course-pdf, pages: "3", used_for: separating credentials from code }
prerequisites: [language-model, embedding, rnn]
learning_objectives: [check BERT input shapes, understand attention masks, keep credentials in environment variables]
related_projects: []
related_posts: [outta-rnn-seq2seq]
tags: [outta, bert, hugging-face, transformer, gemini, api-security]
cover_image: /assets/images/learning/outta/bert-input-credential-boundary.svg
thumbnail: /assets/images/learning/outta/bert-input-credential-boundary.svg
image_alt: BERT's three input embeddings beside a safe runtime credential boundary
draft: false
revision_history:
  - { date: 2026-08-01, change: Organized transformer exercises and safe credential handling around small code examples }
toc:
  - { id: bert, title: Three parts of a BERT input }
  - { id: attention, title: Attention masks and shapes }
  - { id: huggingface, title: Hugging Face workflow }
  - { id: outputs, title: Outputs retained in the notebooks }
  - { id: gemini, title: Separating Gemini credentials }
  - { id: compare, title: Comparing BERT and GPT }
  - { id: navigation, title: Previous and next }
---

## Three parts of a BERT input {#bert}

I went beyond the phrase “bidirectional Transformer encoder” and wrote the BERT input as the sum of token, position, and segment embeddings. The 40-page BERT module also helped me locate `[CLS]`, `[SEP]`, and padding in the sequence.

<p class="study-equation"><code>Eᵢ = E(token, i) + E(position, i) + E(segment, i)</code></p>

Sequence classification uses the `[CLS]` representation, while token classification uses every timestep. Checking the output shape first prevents connecting the wrong task head.

<figure><img src="{{ '/assets/images/learning/outta/bert-input-credential-boundary.svg' | relative_url }}" alt="Token, position, and segment embeddings feed a BERT encoder while the sanitized public replacement reads a credential from the runtime environment" width="1200" height="630"><figcaption>I redrew BERT input and the sanitized public credential pattern. The right side is a replacement pattern after excluding the raw notebook, not a record of its original code.</figcaption></figure>

## Attention masks and shapes {#attention}

Self-attention mixes values according to query-key similarity.

<p class="study-equation"><code>Attention(Q, K, V) = softmax(QKᵀ / √dₖ + M)V</code></p>

The mask (M) prevents padding positions from contributing. I checked that `input_ids.shape == attention_mask.shape`, both with `(batch, length)`, and expected classification logits to have `(batch, classes)`.

## Hugging Face workflow {#huggingface}

I matched the tokenizer and model checkpoint names, passed the tokenizer dictionary directly into the model, and selected the required field such as `logits` or `last_hidden_state` from the output object.

```python
encoded = tokenizer(
    texts,
    padding=True,
    truncation=True,
    return_tensors="pt",
)

assert encoded["input_ids"].shape == encoded["attention_mask"].shape
result = model(**encoded)
assert result.logits.shape[0] == len(texts)
```

## Outputs retained in the notebooks {#outputs}

The Hugging Face copy retained 39 cells, 25 code cells, and 125 text or table output objects. Its code source matched the base notebook; the outputs were the difference. The BERT copy had 72 cells and 31 output objects, with 17 of 32 code cells differing from the base. The Gemini copy retained 33 cells, 24 code cells, and 10 output objects.

These notebooks contained text and table outputs rather than saved image outputs, so I centered this note on tokenization, masks, shapes, and code flow. I did not describe the stored material as a fresh execution.

## Separating Gemini credentials {#gemini}

The old Gemini notebook contained a plaintext API key. I excluded that raw notebook and rewrote the public example to use an environment variable after the owner revokes and replaces the old key. No value or original credential cell is reproduced here.

```python
import os

api_key = os.environ["GEMINI_API_KEY"]
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is empty")

# Pass api_key to the SDK client without printing or saving it.
```

Only the environment-variable name remains in source. The value belongs in a shell, Colab secret, or CI secret. Before sharing a notebook, I also check outputs and metadata for accidental credential retention.

## Comparing BERT and GPT {#compare}

The 28-page GPT module uses a causal mask that hides future tokens. BERT reads context on both sides for masked-token learning and downstream representations; GPT-style models predict the next token from left context. The 22-page CV and NLP trends module tied both to the shared workflow of selecting a pretrained backbone, tokenizer, task head, and loss.

## Previous and next {#navigation}

- Previous: [Following the time axis in RNNs and Seq2Seq]({{ '/en/blog/2026/08/01/outta-rnn-seq2seq/' | relative_url }})
- Next: [2024 OUTTA AI Bootcamp Basic and its projects]({{ '/en/learning/bootcamps/outta-basic-2024/' | relative_url }})
