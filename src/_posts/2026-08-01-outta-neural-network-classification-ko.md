---
title: OUTTA Basic — 함수 근사와 비선형 분류를 신경망으로 이해하기
title_en: OUTTA Basic — Neural Networks for Function Approximation and Nonlinear Classification
description: Sigmoid basis로 함수를 근사하고 spiral data의 decision boundary를 학습하면서 신경망의 깊이와 학습 실패를 비교했다.
date: 2026-08-01 10:02:00 +0900
updated: 2026-08-01 10:02:00 +0900
study_date: 2024-08-31
lang: ko
translation_key: outta-neural-network-classification
permalink: /blog/2026/08/01/outta-neural-network-classification/
alternate_url: /en/blog/2026/08/01/outta-neural-network-classification/
alternate_lang: en
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
  - { title: 인공신경망, type: course-pdf, pages: "71", used_for: "perceptron, activation, backpropagation" }
prerequisites: [linear-regression, gradient-descent]
learning_objectives: [basis function으로 근사하기, spiral data 분류하기, 실패 곡선과 경계 읽기]
related_projects: []
related_posts: [outta-data-autodiff-regression]
tags: [outta, neural-network, universal-approximation, classification, decision-boundary]
cover_image: /assets/images/learning/outta/notebook-30.webp
thumbnail: /assets/images/learning/outta/notebook-30.webp
image_alt: 신경망이 학습한 세 class spiral data의 비선형 decision boundary
draft: false
revision_history:
  - { date: 2026-08-01, change: 인공신경망 강의와 수정 Notebook 출력을 연결해 작성 }
toc:
  - { id: approximation, title: Sigmoid를 basis로 보기 }
  - { id: backprop, title: Loss와 backpropagation }
  - { id: spiral, title: Spiral data 분류 }
  - { id: failure, title: 실패한 학습 읽기 }
  - { id: code, title: 최소 분류 모델 }
  - { id: takeaway, title: 이번에 정리한 기준 }
  - { id: navigation, title: 이전·다음 글 }
---

## Sigmoid를 basis로 보기 {#approximation}

먼저 신경망이 무엇인지 neuron 개수로만 생각하지 않고, 입력을 여러 함수로 바꾼 다음 가중합하는 구조로 정리했다. 71쪽 인공신경망 모듈의 activation 설명을 보면서 sigmoid의 기울기와 위치를 weight·bias가 어떻게 바꾸는지 Notebook에서 비교했다.

<section class="project-gallery" aria-label="Sigmoid basis를 이용한 함수 근사"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-20.webp' | relative_url }}" alt="Cosine 형태의 실제 함수와 학습 초기 근사함수 비교" width="559" height="413" loading="lazy"><figcaption>basis가 충분히 조정되기 전에는 근사함수가 목표의 굴곡을 따라가지 못했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-21.webp' | relative_url }}" alt="학습 뒤 실제 주기함수와 거의 겹친 근사함수" width="559" height="413" loading="lazy"><figcaption>여러 sigmoid의 가중합이 목표 함수의 굴곡을 재구성했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-23.webp' | relative_url }}" alt="서로 다른 위치와 기울기를 가진 sigmoid basis 열 개" width="1198" height="790" loading="lazy"><figcaption>각 unit은 단순하지만 위치와 방향이 달라지면 조합할 재료가 늘어난다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-24.webp' | relative_url }}" alt="여러 sigmoid 곡선과 굵은 점선으로 표시한 전체 모델 출력" width="546" height="436" loading="lazy"><figcaption>얇은 basis들의 가중합이 굵은 최종 출력이 되는 과정을 확인했다.</figcaption></figure>
</div></section>

한 hidden layer의 출력을 다음처럼 적어 보니 그림과 식이 연결됐다.

<p class="study-equation"><code>ŷ(x) = Σⱼ vⱼσ(wⱼx + bⱼ) + c</code></p>

## Loss와 backpropagation {#backprop}

근사함수와 목표함수의 차이를 평균제곱오차로 두고 모든 parameter에 gradient를 전달했다. 당시 저장된 loss 곡선은 2,000 epoch 부근까지 감소했지만, epoch 수 자체보다 curve가 진동하면서도 내려가는지 확인하는 데 사용했다.

<figure><img src="{{ '/assets/images/learning/outta/notebook-22.webp' | relative_url }}" alt="함수 근사 학습에서 2천 epoch 동안 감소한 training loss" width="567" height="432" loading="lazy"><figcaption>초기 진동 뒤 loss가 점차 0에 가까워지는 저장 출력.</figcaption></figure>

## Spiral data 분류 {#spiral}

직선으로 나눌 수 없는 세 class spiral을 보면서 hidden layer가 왜 필요한지 확인했다. `CrossEntropyLoss`에는 softmax 전 logit을 넣고, 출력 shape가 `(batch, 3)`인지 먼저 출력했다. 학습이 진행되자 경계가 점 구름 사이를 휘어 지나갔다.

<section class="project-gallery" aria-label="Spiral dataset 학습곡선과 decision boundary"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-25.webp' | relative_url }}" alt="세 class가 서로 감긴 spiral dataset" width="583" height="435" loading="lazy"><figcaption>하나의 직선으로 분리할 수 없는 입력을 선택했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-26.webp' | relative_url }}" alt="천 epoch 동안 감소하는 spiral 분류 training loss" width="567" height="432" loading="lazy"><figcaption>noise가 있어도 전체 loss 추세는 아래로 향했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-27.webp' | relative_url }}" alt="천 epoch 동안 상승하는 spiral 분류 accuracy" width="567" height="432" loading="lazy"><figcaption>accuracy가 상승하면서도 batch별 변동이 크게 남았다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-28.webp' | relative_url }}" alt="6천 epoch까지 이어진 spiral 분류 loss 곡선" width="567" height="436" loading="lazy"><figcaption>더 오래 학습해도 작은 진동은 사라지지 않았다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-29.webp' | relative_url }}" alt="6천 epoch 학습에서 변동하며 상승한 spiral 분류 accuracy" width="567" height="432" loading="lazy"><figcaption>한 숫자보다 곡선 폭을 함께 읽어야 했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-30.webp' | relative_url }}" alt="세 spiral class 사이를 따라 휘어진 신경망 decision boundary" width="559" height="435" loading="lazy"><figcaption>비선형 경계가 spiral의 안쪽과 바깥쪽을 따라 형성됐다.</figcaption></figure>
</div></section>

## 실패한 학습 읽기 {#failure}

두 번째 spiral 실험에서는 loss가 약 1.10 근처에서 움직이고 accuracy가 1/3에 머물렀다. 세 class를 무작위로 고를 때의 수준이다. activation을 빠뜨렸는지, label dtype이 `long`인지, optimizer가 실제 model parameter를 받는지부터 순서대로 확인했다.

<section class="project-gallery" aria-label="학습 정체와 잘못된 분류경계"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-31.webp' | relative_url }}" alt="두 번째 세 class spiral dataset" width="583" height="435" loading="lazy"><figcaption>입력 모양은 첫 실험과 비슷해도 학습 설정은 별도로 확인해야 했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-32.webp' | relative_url }}" alt="1.10 부근에서 줄지 않는 training loss" width="585" height="438" loading="lazy"><figcaption>loss가 무작위 세 class 기준 근처에서 정체됐다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-33.webp' | relative_url }}" alt="천 epoch 내내 0.333에 머문 accuracy" width="584" height="432" loading="lazy"><figcaption>평평한 accuracy는 학습이 사실상 시작되지 않았다는 신호였다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-34.webp' | relative_url }}" alt="Spiral 구조를 따라가지 못하고 큰 조각으로 나뉜 decision boundary" width="559" height="435" loading="lazy"><figcaption>경계가 점의 spiral 구조를 표현하지 못했다.</figcaption></figure>
</div></section>

## 최소 분류 모델 {#code}

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

## 이번에 정리한 기준 {#takeaway}

나는 loss 감소, accuracy 상승, decision boundary 세 가지를 함께 봤다. 한 그래프만 좋아 보여도 다른 두 개가 맞지 않으면 model·label·split을 다시 확인했다. 저장된 Notebook 사본 15개 중 이 모듈과 연결된 출력은 basis, loss, spiral, 경계까지 이어져 있어 성공과 실패를 함께 공부하기 좋았다.

## 이전·다음 글 {#navigation}

- 이전: [데이터 탐색·자동미분·선형회귀]({{ '/blog/2026/08/01/outta-data-autodiff-regression/' | relative_url }})
- 다음: [CNN을 PyTorch로 구성하고 오류 샘플 읽기]({{ '/blog/2026/08/01/outta-cnn-pytorch/' | relative_url }})
