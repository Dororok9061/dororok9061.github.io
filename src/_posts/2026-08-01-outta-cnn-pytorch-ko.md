---
title: OUTTA Basic — PyTorch CNN과 손글씨 분류 오류 읽기
title_en: OUTTA Basic — PyTorch CNN and Handwritten-Digit Error Analysis
description: Convolution과 pooling의 shape를 따라가고, 저장된 loss·accuracy·오분류 이미지를 함께 읽은 CNN 공부 기록이다.
date: 2026-08-01 10:03:00 +0900
updated: 2026-08-01 10:03:00 +0900
study_date: 2024-08-31
lang: ko
translation_key: outta-cnn-pytorch
permalink: /blog/2026/08/01/outta-cnn-pytorch/
alternate_url: /en/blog/2026/08/01/outta-cnn-pytorch/
alternate_lang: en
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
  - { title: CNN, type: course-pdf, pages: "92", used_for: "convolution, pooling, image classification" }
  - { title: Dataset과 DataLoader, type: course-pdf, pages: "14", used_for: batch와 split 구성 }
  - { title: 전이학습, type: course-pdf, pages: "26", used_for: feature extractor와 fine-tuning 구분 }
prerequisites: [neural-network, pytorch]
learning_objectives: [convolution output shape 계산하기, loss와 accuracy 함께 읽기, 오분류 이미지를 원인별로 보기]
related_projects: []
related_posts: [outta-neural-network-classification]
tags: [outta, cnn, pytorch, image-classification, error-analysis]
cover_image: /assets/images/learning/outta/notebook-39.webp
thumbnail: /assets/images/learning/outta/notebook-39.webp
image_alt: 예측값과 정답이 다른 손글씨 숫자 스물다섯 개
draft: false
revision_history:
  - { date: 2026-08-01, change: CNN 강의와 저장된 분류 출력으로 작성 }
toc:
  - { id: shape, title: Convolution shape부터 확인 }
  - { id: samples, title: 입력 이미지를 먼저 보기 }
  - { id: curves, title: Loss와 accuracy 같이 보기 }
  - { id: errors, title: 맞힌 예와 틀린 예 }
  - { id: code, title: 최소 CNN forward }
  - { id: transfer, title: 전이학습과 연결 }
  - { id: navigation, title: 이전·다음 글 }
---

## Convolution shape부터 확인 {#shape}

먼저 CNN이 무엇인지 filter 그림만 외우지 않고 입력과 출력 shape로 정리했다. 92쪽 CNN 모듈에서 kernel, stride, padding을 확인한 뒤 다음 식으로 한 축의 크기를 계산했다.

<p class="study-equation"><code>H(out) = floor((H(in) + 2P − K) / S) + 1</code></p>

Notebook을 실행했을 때 flatten 뒤 feature 수가 `Linear` 입력과 맞지 않는 부분을 먼저 확인했다. `forward` 중간에 shape를 출력해 convolution과 pooling이 공간 크기를 어떻게 줄이는지 따라갔다.

## 입력 이미지를 먼저 보기 {#samples}

14쪽 Dataset·DataLoader 모듈을 보면서 batch를 만들기 전에 sample과 label을 함께 그렸다. 손글씨는 같은 숫자라도 굵기·기울기·위치가 크게 달랐다. 이 차이를 보지 않고 accuracy만 읽으면 모델이 어떤 변형을 어려워하는지 알 수 없었다.

<figure><img src="{{ '/assets/images/learning/outta/notebook-35.webp' | relative_url }}" alt="Label과 함께 배열한 손글씨 숫자 열여섯 개" width="639" height="658" loading="lazy"><figcaption>기울기와 획 모양이 다른 입력을 batch 단위로 먼저 살펴봤다.</figcaption></figure>

## Loss와 accuracy 같이 보기 {#curves}

내가 수정한 CNN Notebook은 28개 code cell 중 2개가 기본본과 달랐고, 17개의 output object와 5개의 그림이 남아 있었다. 당시 저장된 curve에서는 loss가 전체적으로 줄고 accuracy가 높은 구간에 도달했지만 작은 validation set에서는 한두 sample만 바뀌어도 값이 크게 흔들릴 수 있다.

<section class="project-gallery" aria-label="CNN loss와 accuracy 곡선"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-36.webp' | relative_url }}" alt="15 epoch 동안 전반적으로 감소한 CNN training loss" width="576" height="432" loading="lazy"><figcaption>loss는 감소했지만 중간 epoch의 상승도 함께 남아 있다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-37.webp' | relative_url }}" alt="15 epoch 동안 0.9 이상에서 변동한 CNN accuracy" width="576" height="432" loading="lazy"><figcaption>높은 accuracy만 보지 않고 표본 수와 변동 폭을 함께 읽었다.</figcaption></figure>
</div></section>

## 맞힌 예와 틀린 예 {#errors}

정답을 맞힌 `1`은 세로획이 뚜렷했다. 반대로 오분류 모음에서는 열린 고리, 붙은 획, 기울어진 선 때문에 `5→3`, `4→9`, `7→9`처럼 모양이 가까운 class로 이동했다. 다음 실험을 생각할 때는 무작정 layer를 늘리기보다 normalization, crop, augmentation 순서로 확인하는 편이 낫다고 정리했다.

<section class="project-gallery" aria-label="CNN 정답과 오분류 예시"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-38.webp' | relative_url }}" alt="CNN이 숫자 1로 정확히 분류한 손글씨 한 장" width="416" height="456" loading="lazy"><figcaption>예측과 정답이 모두 1인 단순한 세로획 sample.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-39.webp' | relative_url }}" alt="예측값과 정답을 제목에 표시한 CNN 오분류 손글씨 스물다섯 개" width="794" height="812" loading="lazy"><figcaption>정확도 숫자 뒤에 숨어 있던 실패 모양을 한 화면에서 비교했다.</figcaption></figure>
</div></section>

## 최소 CNN forward {#code}

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

## 전이학습과 연결 {#transfer}

26쪽 전이학습 모듈에서는 작은 CNN을 처음부터 학습하는 경우와 pretrained feature extractor를 쓰는 경우를 구분했다. 입력 channel·resize·normalization을 backbone이 기대하는 형식에 맞추고, 먼저 classifier만 학습한 뒤 필요할 때 일부 block을 푸는 순서로 정리했다.

## 이전·다음 글 {#navigation}

- 이전: [함수 근사와 비선형 분류]({{ '/blog/2026/08/01/outta-neural-network-classification/' | relative_url }})
- 다음: [언어모델·Embedding·Autoencoder]({{ '/blog/2026/08/01/outta-language-model-embedding/' | relative_url }})
