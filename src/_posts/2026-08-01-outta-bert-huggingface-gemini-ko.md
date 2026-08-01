---
title: OUTTA Basic — BERT·Hugging Face·Gemini를 안전하게 정리하기
title_en: OUTTA Basic — Organizing BERT, Hugging Face, and Gemini Safely
description: Tokenization, attention mask, BERT output shape와 환경변수를 이용한 Gemini credential 처리를 코드 중심으로 정리했다.
date: 2026-08-01 10:06:00 +0900
updated: 2026-08-01 10:06:00 +0900
study_date: 2024-08-31
lang: ko
translation_key: outta-bert-huggingface-gemini
permalink: /blog/2026/08/01/outta-bert-huggingface-gemini/
alternate_url: /en/blog/2026/08/01/outta-bert-huggingface-gemini/
alternate_lang: en
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
  - { title: BERT, type: course-pdf, pages: "40", used_for: bidirectional attention과 fine-tuning }
  - { title: GPT, type: course-pdf, pages: "28", used_for: causal language modeling }
  - { title: CV와 NLP 연구동향, type: course-pdf, pages: "22", used_for: pretrained model 활용 흐름 }
  - { title: Gemini API Key 발급 방법, type: course-pdf, pages: "3", used_for: credential을 코드와 분리하는 계기 }
prerequisites: [language-model, embedding, rnn]
learning_objectives: [BERT 입력 shape 확인하기, attention mask 이해하기, credential을 환경변수로 분리하기]
related_projects: []
related_posts: [outta-rnn-seq2seq]
tags: [outta, bert, hugging-face, transformer, gemini, api-security]
cover_image: /assets/images/learning/outta/bert-input-credential-boundary.svg
thumbnail: /assets/images/learning/outta/bert-input-credential-boundary.svg
image_alt: BERT의 세 embedding 입력과 실행환경 API credential 경계를 함께 그린 구조도
draft: false
revision_history:
  - { date: 2026-08-01, change: Transformer 실습과 안전한 credential 사용법을 코드 중심으로 정리 }
toc:
  - { id: bert, title: BERT 입력을 세 부분으로 보기 }
  - { id: attention, title: Attention mask와 shape }
  - { id: huggingface, title: Hugging Face 흐름 }
  - { id: outputs, title: 당시 Notebook에 남은 출력 }
  - { id: gemini, title: Gemini credential 분리 }
  - { id: compare, title: BERT와 GPT 비교 }
  - { id: navigation, title: 이전·다음 글 }
---

## BERT 입력을 세 부분으로 보기 {#bert}

먼저 BERT가 무엇인지 양방향 Transformer encoder라는 문장만 외우지 않고 입력 embedding을 token·position·segment 세 항의 합으로 정리했다. 40쪽 BERT 모듈을 보면서 `[CLS]`, `[SEP]`, padding이 sequence에 들어가는 위치도 확인했다.

<p class="study-equation"><code>Eᵢ = E(token, i) + E(position, i) + E(segment, i)</code></p>

문장 분류에서는 `[CLS]` 위치의 representation을 classifier에 넣지만, token classification은 각 timestep 출력을 사용한다. 같은 BERT라도 output shape를 먼저 보지 않으면 task head를 잘못 연결하기 쉽다.

<figure><img src="{{ '/assets/images/learning/outta/bert-input-credential-boundary.svg' | relative_url }}" alt="Token, position, segment embedding을 더해 BERT encoder로 보내고 공개용 교체 코드는 credential을 실행환경에서 읽는 구조" width="1200" height="630"><figcaption>강의 주제에서 공부한 BERT 입력과 공개용 credential 처리 형태를 다시 그렸다. 오른쪽은 옛 Notebook의 동작을 묘사한 화면이 아니라 평문 값을 제거한 교체 패턴이다.</figcaption></figure>

## Attention mask와 shape {#attention}

Self-attention의 핵심은 query와 key의 유사도로 value를 섞는 과정이다.

<p class="study-equation"><code>Attention(Q, K, V) = softmax(QKᵀ / √dₖ + M)V</code></p>

여기서 mask (M)은 padding 위치가 attention에 들어가지 않게 만든다. Notebook에서 `input_ids.shape == attention_mask.shape`인지, 둘 다 `(batch, length)`인지 먼저 확인했다. 분류 logit은 `(batch, classes)`가 되어야 한다.

## Hugging Face 흐름 {#huggingface}

Hugging Face 실습은 tokenizer와 model checkpoint를 같은 이름으로 맞추는 순서로 정리했다. tokenizer가 만든 dictionary를 그대로 model에 넘기고, 출력 object에서 필요한 `logits`나 `last_hidden_state`를 명시적으로 선택했다.

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

## 당시 Notebook에 남은 출력 {#outputs}

Hugging Face 사본에는 39개 cell, 25개 code cell과 125개의 text·table output object가 남아 있었다. code source는 기본본과 같았고 출력만 보존돼 있었다. BERT 사본은 72개 cell과 31개 output object가 있었으며, 32개 code cell 중 17개가 기본본과 달랐다. Gemini 사본에는 33개 cell, 24개 code cell, 10개 output object가 남아 있었다.

이 세 Notebook은 저장된 image output 대신 text와 table 위주라서, 이번 글에서는 tokenization·mask·shape와 코드 흐름을 중심으로 다시 적었다. 당시 결과를 새 실행 결과처럼 바꾸어 쓰지 않았다.

## Gemini credential 분리 {#gemini}

옛 Gemini Notebook에는 평문 API Key가 남아 있었다. 그 원본은 공개하지 않았다. 기존 키는 소유자 계정에서 폐기·교체해야 하며, 공개 예제는 새 값을 코드에 적지 않고 환경변수에서 읽도록 바꿨다. 실제 값이나 당시 cell 내용은 글에 옮기지 않았다.

```python
import os

api_key = os.environ["GEMINI_API_KEY"]
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is empty")

# SDK client를 만들 때 api_key를 전달하고 출력하거나 저장하지 않는다.
```

환경변수 이름만 코드에 남고 값은 shell·Colab secret·CI secret 같은 실행 환경이 제공한다. Notebook을 공유하기 전에는 output과 metadata에도 credential이 남지 않았는지 확인해야 한다.

## BERT와 GPT 비교 {#compare}

28쪽 GPT 모듈에서는 미래 token을 가리는 causal mask를 사용한다. BERT는 양쪽 문맥을 보며 masked token이나 downstream task representation을 학습하고, GPT 계열은 왼쪽 문맥에서 다음 token을 예측한다. 22쪽 CV·NLP 동향 모듈까지 읽고 나니 pretrained backbone을 가져와 tokenizer·head·loss를 task에 맞추는 공통 흐름이 보였다.

## 이전·다음 글 {#navigation}

- 이전: [RNN과 Seq2Seq에서 시간축 따라가기]({{ '/blog/2026/08/01/outta-rnn-seq2seq/' | relative_url }})
- 다음: [2024 OUTTA AI 부트캠프 Basic 과정과 프로젝트]({{ '/learning/bootcamps/outta-basic-2024/' | relative_url }})
