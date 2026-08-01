---
title: OUTTA Basic — 기본 언어모델, Embedding과 Autoencoder 연결하기
title_en: OUTTA Basic — Connecting Language Models, Embeddings, and Autoencoders
description: TF-IDF cosine similarity에서 dense embedding과 autoencoder latent까지 표현 학습의 흐름을 정리했다.
date: 2026-08-01 10:04:00 +0900
updated: 2026-08-01 10:04:00 +0900
study_date: 2024-08-31
lang: ko
translation_key: outta-language-model-embedding
permalink: /blog/2026/08/01/outta-language-model-embedding/
alternate_url: /en/blog/2026/08/01/outta-language-model-embedding/
alternate_lang: en
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
  - { title: 기본 언어모델, type: course-pdf, pages: "49", used_for: tokenization과 next-token prediction }
  - { title: Word Embedding과 Autoencoder, type: course-pdf, pages: "28", used_for: dense representation과 reconstruction }
prerequisites: [linear-algebra, neural-network]
learning_objectives: [sparse와 dense 표현 비교하기, cosine similarity 해석하기, latent와 reconstruction 연결하기]
related_projects: []
related_posts: [outta-cnn-pytorch]
tags: [outta, language-model, tf-idf, embedding, autoencoder]
cover_image: /assets/images/learning/outta/notebook-40.webp
thumbnail: /assets/images/learning/outta/notebook-40.webp
image_alt: TF-IDF로 표현한 문서 사이 cosine similarity heatmap
draft: false
revision_history:
  - { date: 2026-08-01, change: 언어 표현과 autoencoder 모듈을 Notebook 그림과 연결 }
toc:
  - { id: tokens, title: Token에서 확률로 }
  - { id: sparse, title: TF-IDF와 cosine similarity }
  - { id: dense, title: Dense embedding }
  - { id: autoencoder, title: Autoencoder latent }
  - { id: code, title: Shape를 확인하는 코드 }
  - { id: compare, title: 표현을 비교한 기준 }
  - { id: navigation, title: 이전·다음 글 }
---

## Token에서 확률로 {#tokens}

먼저 언어모델이 무엇인지 문장을 통째로 외우는 장치가 아니라 앞의 token으로 다음 token의 분포를 계산하는 모델로 정리했다. 49쪽 기본 언어모델 모듈을 보면서 vocabulary, integer index, context window, target shift 순서로 Notebook shape를 확인했다.

<p class="study-equation"><code>p(w₁…wₜ) = ∏ₜ p(wₜ | w before t)</code></p>

같은 문장도 tokenizer와 vocabulary가 달라지면 index sequence가 바뀐다. 그래서 padding index와 unknown token을 먼저 정하고, embedding 입력 dtype이 `long`인지 확인했다.

## TF-IDF와 cosine similarity {#sparse}

Dense embedding에 들어가기 전 TF-IDF로 문서를 표현했다. 두 vector의 cosine similarity는 길이보다 방향을 비교한다. heatmap에서 밝은 쌍은 같은 단어를 많이 공유했고, 어두운 쌍은 vocabulary overlap이 적었다.

<p class="study-equation"><code>cos(a, b) = aᵀb / (‖a‖₂‖b‖₂)</code></p>

<figure><img src="{{ '/assets/images/learning/outta/notebook-40.webp' | relative_url }}" alt="일곱 문서 사이 TF-IDF cosine similarity heatmap" width="408" height="456" loading="lazy"><figcaption>밝은 대칭 cell을 따라 가까운 문서 쌍을 확인했다.</figcaption></figure>

## Dense embedding {#dense}

28쪽 Word Embedding·Autoencoder 모듈에서는 one-hot vector 대신 학습 가능한 dense row를 사용했다. `Embedding(vocab_size, embedding_dim)`의 출력은 입력 sequence 뒤에 embedding 축 하나가 붙는다. 단어 사이 관계를 확인할 때도 cosine similarity를 사용하지만, 이번에는 count가 아니라 학습된 좌표를 비교한다.

<figure><img src="{{ '/assets/images/learning/outta/notebook-41.webp' | relative_url }}" alt="반복 횟수가 늘면서 빠르게 감소한 embedding 실습 loss" width="567" height="432" loading="lazy"><figcaption>저장된 curve는 초기에 크게 감소한 뒤 낮은 값에서 안정됐다.</figcaption></figure>

## Autoencoder latent {#autoencoder}

Autoencoder에서는 입력을 작은 latent로 압축하고 다시 복원한다. 이 부분은 처음에 PCA와 혼동했다. PCA는 선형 축을 찾지만, encoder와 decoder 사이에 비선형 activation을 넣으면 곡선형 표현도 학습할 수 있다.

<p class="study-equation"><code>z = fθ(x), x̂ = gφ(z), L = ‖x − x̂‖₂²</code></p>

<section class="project-gallery" aria-label="Autoencoder latent와 reconstruction loss"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-42.webp' | relative_url }}" alt="두 차원 latent 공간에서 세 Iris 품종이 색으로 나뉜 산점도" width="559" height="413" loading="lazy"><figcaption>압축 좌표에서도 class가 어느 정도 분리되는지 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-43.webp' | relative_url }}" alt="약 180 iteration 동안 감소한 autoencoder reconstruction loss" width="576" height="432" loading="lazy"><figcaption>초기 급감 뒤 완만해지는 reconstruction loss를 읽었다.</figcaption></figure>
</div></section>

## Shape를 확인하는 코드 {#code}

```python
token_ids = tokenizer(batch_text)          # (batch, time)
vectors = embedding(token_ids)             # (batch, time, dim)

latent = encoder(features)                 # (batch, latent_dim)
reconstruction = decoder(latent)           # (batch, feature_dim)

assert vectors.shape[:2] == token_ids.shape
assert reconstruction.shape == features.shape
```

## 표현을 비교한 기준 {#compare}

TF-IDF는 어떤 단어가 겹쳤는지 설명하기 쉽고, embedding은 비슷한 문맥을 더 작은 dense vector에 담을 수 있다. Autoencoder latent는 입력 복원에 필요한 정보를 압축한다. 나는 세 표현을 서로 대체하는 답으로 보지 않고 목적·학습 신호·해석 방법이 다른 도구로 정리했다.

## 이전·다음 글 {#navigation}

- 이전: [PyTorch CNN과 손글씨 분류 오류]({{ '/blog/2026/08/01/outta-cnn-pytorch/' | relative_url }})
- 다음: [RNN과 Seq2Seq의 시간축]({{ '/blog/2026/08/01/outta-rnn-seq2seq/' | relative_url }})
