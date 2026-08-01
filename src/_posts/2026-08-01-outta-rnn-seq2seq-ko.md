---
title: OUTTA Basic — RNN과 Seq2Seq에서 시간축 따라가기
title_en: OUTTA Basic — Following the Time Axis in RNNs and Seq2Seq
description: Hidden state, sequence shape, train-test divergence와 Seq2Seq teacher forcing을 저장된 RNN 곡선으로 다시 정리했다.
date: 2026-08-01 10:05:00 +0900
updated: 2026-08-01 10:05:00 +0900
study_date: 2024-08-31
lang: ko
translation_key: outta-rnn-seq2seq
permalink: /blog/2026/08/01/outta-rnn-seq2seq/
alternate_url: /en/blog/2026/08/01/outta-rnn-seq2seq/
alternate_lang: en
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
  - { title: RNN, type: course-pdf, pages: "38", used_for: "recurrence, hidden state, Seq2Seq" }
prerequisites: [language-model, embedding, neural-network]
learning_objectives: [batch와 time 축 구분하기, train-test divergence 읽기, encoder-decoder shape 연결하기]
related_projects: []
related_posts: [outta-language-model-embedding]
tags: [outta, rnn, seq2seq, recurrent-neural-network, teacher-forcing]
cover_image: /assets/images/learning/outta/notebook-44.webp
thumbnail: /assets/images/learning/outta/notebook-44.webp
image_alt: RNN train accuracy는 상승하지만 test accuracy는 0.5에 머문 그래프
draft: false
revision_history:
  - { date: 2026-08-01, change: RNN 모듈과 저장된 sequence 학습곡선을 연결 }
toc:
  - { id: recurrence, title: Hidden state 식으로 시작 }
  - { id: shapes, title: Batch와 time 축 }
  - { id: divergence, title: Train과 test의 분리 }
  - { id: dynamics, title: 서로 다른 학습곡선 읽기 }
  - { id: seq2seq, title: Encoder와 decoder 연결 }
  - { id: code, title: Packed shape 없는 최소 예 }
  - { id: navigation, title: 이전·다음 글 }
---

## Hidden state 식으로 시작 {#recurrence}

먼저 RNN이 무엇인지 이전 정보를 무조건 기억하는 모델이라고 쓰지 않고, 직전 hidden state와 현재 입력을 같은 cell에 넣는 반복식으로 정리했다. 38쪽 RNN 모듈에서 펼친 시간축 그림을 보면서 parameter는 timestep마다 새로 생기는 것이 아니라 공유된다는 점을 다시 적었다.

<p class="study-equation"><code>hₜ = tanh(Wₓxₜ + Wₕhₜ₋₁ + b), oₜ = Wₒhₜ + c</code></p>

## Batch와 time 축 {#shapes}

Notebook에서 가장 먼저 확인한 것은 `(batch, time, feature)`였다. `batch_first=True`가 아니면 앞의 두 축 순서가 바뀐다. 마지막 timestep만 쓸지, 모든 timestep 출력을 decoder에 넘길지도 task에 따라 달라진다.

문장 분류라면 padding을 loss에 포함하지 않도록 length나 mask가 필요하다. hidden state shape도 layer 수와 양방향 여부를 포함해 `(layers * directions, batch, hidden)`으로 확인했다.

## Train과 test의 분리 {#divergence}

당시 RNN Notebook에 저장된 그래프에서는 train accuracy가 거의 1.0까지 올라가지만 test accuracy는 0.5 부근에 머문다. epoch를 더 돌리면 좋아질 것이라고 생각했지만, 두 곡선 간격이 계속 벌어지는 모습은 memorization에 가깝다.

<figure><img src="{{ '/assets/images/learning/outta/notebook-44.webp' | relative_url }}" alt="천오백 epoch 동안 RNN train accuracy는 상승하고 test accuracy는 0.5에 머문 곡선" width="846" height="470" loading="lazy"><figcaption>학습 곡선 상승과 일반화 개선이 같은 뜻이 아님을 보여 준 저장 출력.</figcaption></figure>

sequence length, split 방식, class balance, hidden size, dropout을 함께 확인해야 했다. 특히 같은 원문에서 잘라낸 인접 window가 train과 test에 나뉘면 비슷한 sequence가 양쪽에 들어갈 수 있다.

## 서로 다른 학습곡선 읽기 {#dynamics}

다른 Notebook 출력에서는 loss 감소와 accuracy 상승이 함께 나타났다. 또 짧은 series에서는 값이 한 번 반등한 뒤 감소했고, 다른 실험은 loss가 꾸준히 낮아졌다. 한 곡선의 축 범위나 timestep 수를 확인하지 않고 서로 직접 비교하면 안 된다는 점을 배웠다.

<section class="project-gallery" aria-label="여러 RNN 학습곡선"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-45.webp' | relative_url }}" alt="100개 구간에서 RNN loss는 감소하고 accuracy는 상승한 그래프" width="855" height="470" loading="lazy"><figcaption>두 metric이 반대 방향으로 꾸준히 움직이는지 함께 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-46.webp' | relative_url }}" alt="Sequence 길이 변화에 따라 1.0에서 0.85로 내려간 값" width="556" height="413" loading="lazy"><figcaption>짧은 축에서는 한 점의 반등도 크게 보이므로 x축 의미를 먼저 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-47.webp' | relative_url }}" alt="100 epoch 동안 2.4에서 0.8 아래로 감소한 sequence model loss" width="855" height="470" loading="lazy"><figcaption>완만하게 감소하는 loss에서 학습 속도의 변화를 읽었다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-48.webp' | relative_url }}" alt="초기에는 1에 가깝다가 10번째 이후 0으로 급락한 값" width="547" height="413" loading="lazy"><figcaption>급격한 변화는 metric 정의, mask, length 경계를 다시 보게 했다.</figcaption></figure>
</div></section>

## Encoder와 decoder 연결 {#seq2seq}

Seq2Seq에서는 encoder가 입력 sequence를 읽고 decoder가 `<bos>`부터 다음 token을 한 단계씩 만든다. 이 부분은 처음에 encoder의 모든 출력과 마지막 hidden state를 혼동했다. attention이 없는 기본 구조에서는 마지막 hidden state가 decoder 초기 상태로 전달되고, teacher forcing을 쓰면 정답 token을 다음 입력으로 넣는다.

<p class="study-equation"><code>L = −Σₜ log p(yₜ | y before t, x)</code></p>

## Packed shape 없는 최소 예 {#code}

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

## 이전·다음 글 {#navigation}

- 이전: [기본 언어모델·Embedding·Autoencoder]({{ '/blog/2026/08/01/outta-language-model-embedding/' | relative_url }})
- 다음: [BERT·Hugging Face·Gemini를 안전하게 정리하기]({{ '/blog/2026/08/01/outta-bert-huggingface-gemini/' | relative_url }})
