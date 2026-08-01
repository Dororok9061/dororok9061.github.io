---
title: OUTTA Basic — 데이터 탐색에서 자동미분과 선형회귀까지
title_en: OUTTA Basic — From Data Exploration to Autodiff and Linear Regression
description: NBA 신체 측정값을 그려 보고, 손실곡면·경사하강법·정규화를 선형회귀 Notebook 출력과 함께 다시 정리했다.
date: 2026-08-01 10:01:00 +0900
updated: 2026-08-01 10:01:00 +0900
study_date: 2024-08-31
lang: ko
translation_key: outta-data-autodiff-regression
permalink: /blog/2026/08/01/outta-data-autodiff-regression/
alternate_url: /en/blog/2026/08/01/outta-data-autodiff-regression/
alternate_lang: en
primary_category: ai-deep-learning
subcategory: machine-learning-basics
series: outta-basic-2024
series_order: 1
post_type: study-note
difficulty: beginner
study_status: published
evidence_status: STUDIED_FROM_COURSE_AND_NOTEBOOK_OUTPUTS
tools: [Python, NumPy, PyTorch, Matplotlib]
hardware: []
software_versions: []
source_materials:
  - { title: 머신러닝 기초와 선형회귀, type: course-pdf, pages: "39", used_for: 회귀 문제와 손실함수 }
  - { title: 경사하강법, type: course-pdf, pages: "25", used_for: 자동미분과 parameter update }
prerequisites: [python, algebra]
learning_objectives: [관계를 먼저 시각화하기, 자동미분 흐름 이해하기, 선형회귀 손실과 정규화 연결하기]
related_projects: []
related_posts: []
tags: [outta, linear-regression, gradient-descent, autodiff, normalization]
cover_image: /assets/images/learning/outta/notebook-12.webp
thumbnail: /assets/images/learning/outta/notebook-12.webp
image_alt: NBA 신체 측정값 위에 표시한 학습 회귀선과 기준 회귀선
draft: false
revision_history:
  - { date: 2026-08-01, change: 강의 모듈과 당시 Notebook 출력을 바탕으로 작성 }
toc:
  - { id: inspect, title: 먼저 데이터를 그려 본 이유 }
  - { id: relation, title: 변수 관계 읽기 }
  - { id: surface, title: 손실곡면과 자동미분 }
  - { id: normalize, title: 정규화와 수렴 }
  - { id: errors, title: 저장된 오류에서 배운 점 }
  - { id: code, title: 최소 회귀 Loop }
  - { id: navigation, title: 이전·다음 글 }
---

## 먼저 데이터를 그려 본 이유 {#inspect}

먼저 선형회귀가 무엇인지 식부터 외우기보다 입력 두 개를 직접 그려 봤다. 강의의 39쪽짜리 회귀 모듈을 읽고 NBA draft 측정값 Notebook에서 손 길이·손 너비·키·체중·윙스팬을 산점도로 비교했다. 점이 한 방향으로 모이는지, position처럼 범주형인 축이 그대로 숫자 계산에 들어가지는 않는지부터 확인했다.

<section class="project-gallery" aria-label="NBA 측정값 탐색 그래프"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-01.webp' | relative_url }}" alt="2019 NBA 지명 선수의 손 길이와 손 너비 산점도" width="576" height="455" loading="lazy"><figcaption>손 길이가 늘수록 손 너비도 커지는 경향을 먼저 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-02.webp' | relative_url }}" alt="선수 position별 키와 체중을 나눠 그린 두 산점도" width="571" height="455" loading="lazy"><figcaption>범주형 position을 축으로 썼을 때 label이 겹치는 문제도 함께 보였다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-03.webp' | relative_url }}" alt="축 label을 단순화해 다시 그린 손 길이와 손 너비 산점도" width="556" height="435" loading="lazy"><figcaption>같은 데이터를 다시 그리며 title·axis·range가 해석에 미치는 영향을 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-04.webp' | relative_url }}" alt="마이너스 10부터 10까지 그린 x 제곱 함수" width="552" height="439" loading="lazy"><figcaption>미분 실습에 들어가기 전 (x^2)의 곡률과 최소점을 눈으로 확인했다.</figcaption></figure>
</div></section>

## 변수 관계 읽기 {#relation}

키와 윙스팬은 비교적 선형적인 관계를 보였다. 직선을 얹기 전 산점도만 보고 방향을 예상한 뒤, 같은 데이터를 서로 다른 코드로 다시 그려 결과가 일치하는지 확인했다. 이 과정에서 plot이 예쁘게 나오는 것보다 축 단위와 입력 순서를 맞추는 일이 먼저라는 점을 배웠다.

<section class="project-gallery" aria-label="키와 윙스팬 관계 및 회귀선"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-05.webp' | relative_url }}" alt="NBA 선수 키와 윙스팬의 양의 상관관계 산점도" width="553" height="435" loading="lazy"><figcaption>회귀선을 넣기 전 원자료의 방향과 이상치를 살펴봤다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-06.webp' | relative_url }}" alt="키와 윙스팬 산점도 위에 겹친 첫 선형 회귀선" width="543" height="435" loading="lazy"><figcaption>기울기와 절편이 점 구름의 중심을 통과하는지 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-07.webp' | relative_url }}" alt="x축 키와 y축 윙스팬을 명시한 산점도" width="572" height="455" loading="lazy"><figcaption>입력과 target의 역할을 축 이름으로 분명히 적었다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-08.webp' | relative_url }}" alt="두 번째 구현에서 다시 계산한 키와 윙스팬 회귀선" width="543" height="435" loading="lazy"><figcaption>같은 직선을 다시 얻어 데이터 선택과 식을 교차 확인했다.</figcaption></figure>
</div></section>

선형 모델은 <code>ŷ = mx + b</code>, 평균제곱오차는 다음처럼 적었다.

<p class="study-equation"><code>L(m, b) = (1/N) Σᵢ(mxᵢ + b − yᵢ)²</code></p>

## 손실곡면과 자동미분 {#surface}

강의의 25쪽 경사하강법 모듈을 보면서 (m)과 (b)를 축으로 둔 손실곡면을 다시 그려 봤다. 처음에는 그래프의 낮은 곳으로 이동한다는 설명과 `loss.backward()`가 따로 느껴졌다. 곡면 위 현재점과 update 궤적을 함께 보니 gradient가 parameter 공간에서 어느 방향을 가리키는지 연결됐다.

<section class="project-gallery" aria-label="손실곡면과 경사하강 궤적"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-09.webp' | relative_url }}" alt="기울기 m과 절편 b에 따른 선형회귀 손실곡면과 현재점" width="389" height="389" loading="lazy"><figcaption>현재 parameter가 손실곡면의 어느 위치에 있는지 표시했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-10.webp' | relative_url }}" alt="10회 update 동안의 loss와 m과 b 변화 그래프" width="990" height="1190" loading="lazy"><figcaption>큰 첫 update 뒤 loss는 줄었지만 parameter가 빠르게 흔들리는 모습이 남았다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-11.webp' | relative_url }}" alt="선형회귀 손실곡면 위 여러 경사하강 update 지점" width="389" height="389" loading="lazy"><figcaption>update가 최저점 주변으로 이동하는 경로를 곡면 위에서 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-13.webp' | relative_url }}" alt="서로 다른 시작점에서 손실곡면을 내려가는 여러 궤적" width="389" height="389" loading="lazy"><figcaption>초기값과 step 크기에 따라 같은 곡면에서도 경로가 달라졌다.</figcaption></figure>
</div></section>

## 정규화와 수렴 {#normalize}

키와 윙스팬의 단위가 크면 gradient 크기도 함께 달라졌다. 평균을 빼고 표준편차로 나눈 뒤 같은 구조를 학습하니 손실곡면과 update가 읽기 쉬워졌다. 당시 저장된 그래프는 재실행 결과가 아니라 Notebook에 남아 있던 출력이다.

<section class="project-gallery" aria-label="회귀선 비교와 정규화 후 수렴"><div>
<figure><img src="{{ '/assets/images/learning/outta/notebook-12.webp' | relative_url }}" alt="학습한 키 윙스팬 회귀선과 기준 회귀선 비교" width="572" height="432" loading="lazy"><figcaption>학습선과 기준선을 겹쳐 기울기 차이를 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-14.webp' | relative_url }}" alt="여러 학습 회귀선과 빨간 기준선을 겹친 산점도" width="572" height="432" loading="lazy"><figcaption>여러 실행 경로가 비슷한 직선으로 모이는지 비교했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-15.webp' | relative_url }}" alt="정규화한 키와 윙스팬의 산점도" width="565" height="455" loading="lazy"><figcaption>두 변수의 중심과 scale을 맞춘 뒤 선형 관계가 유지되는지 봤다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-16.webp' | relative_url }}" alt="50회 update 동안 감소하는 loss와 안정되는 m과 b" width="989" height="1190" loading="lazy"><figcaption>정규화 뒤 loss와 두 parameter가 부드럽게 안정됐다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-17.webp' | relative_url }}" alt="정규화한 회귀 문제의 평균제곱오차 곡면과 update 점" width="392" height="389" loading="lazy"><figcaption>좁아진 scale에서 최저점 주변 이동을 다시 확인했다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-18.webp' | relative_url }}" alt="정규화된 두 변수의 양의 상관 산점도" width="546" height="414" loading="lazy"><figcaption>정규화는 상관 구조를 없애지 않고 좌표계만 바꾼다.</figcaption></figure>
<figure><img src="{{ '/assets/images/learning/outta/notebook-19.webp' | relative_url }}" alt="원래 단위로 표시한 키와 윙스팬 산점도" width="553" height="413" loading="lazy"><figcaption>마지막에는 원래 단위로 돌아와 회귀 결과를 해석했다.</figcaption></figure>
</div></section>

## 저장된 오류에서 배운 점 {#errors}

내가 수정한 회귀 Notebook에는 30개의 output object와 13개의 그림이 남아 있었고, 그중 error output도 3개 있었다. 오류를 없었던 일처럼 지우지 않고 입력 Tensor의 dtype·shape, `requires_grad`, update 뒤 gradient 초기화 순서부터 확인했다. 특히 parameter를 갱신한 다음 `zero_grad()`를 빠뜨리면 gradient가 누적된다는 점을 다시 적어 뒀다.

## 최소 회귀 Loop {#code}

```python
m = torch.zeros((), requires_grad=True)
b = torch.zeros((), requires_grad=True)

for _ in range(50):
    prediction = m * x + b
    loss = ((prediction - y) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        m -= learning_rate * m.grad
        b -= learning_rate * b.grad
        m.grad.zero_()
        b.grad.zero_()
```

코드를 짧게 만들면서도 forward, loss, backward, update, gradient reset 순서는 남겼다. 다음 글에서는 직선 하나로 풀 수 없는 함수와 spiral data를 신경망으로 옮긴다.

## 이전·다음 글 {#navigation}

- 이전: [2024 OUTTA AI 부트캠프 Basic 과정]({{ '/learning/bootcamps/outta-basic-2024/' | relative_url }})
- 다음: [함수 근사와 비선형 분류]({{ '/blog/2026/08/01/outta-neural-network-classification/' | relative_url }})
