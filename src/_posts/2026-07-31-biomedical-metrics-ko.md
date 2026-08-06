---
title: PPG-HRV 분류에서 AUC·F1의 평가 조건을 보존한 이유
title_en: Preserving evaluation conditions for AUC and F1 in PPG-HRV classification
description: Subject split, fold, preprocessing, confusion matrix와 paper-reported metric을 하나의 성능값으로 합치지 않는 기록.
date: 2026-07-31 00:50:00 +0900
updated: 2026-08-01 18:40:00 +0900
study_date: 2026-07-31
lang: ko
translation_key: biomedical-metric-conditions
permalink: /blog/2026/07/31/biomedical-metric-conditions/
alternate_url: /en/blog/2026/07/31/biomedical-metric-conditions/
alternate_lang: en
primary_category: ai-deep-learning
subcategory: model-evaluation
series: cnn-discriminative-ai
series_order: 3
post_type: study-note
difficulty: intermediate
study_status: published
evidence_status: PAPER_AND_CODE_SEPARATE
tools: [Python, CNN, HRV]
hardware: [PPG AFE, STM32]
software_versions: [not fully preserved]
source_materials:
  - { title: PPG-HRV Cognitive Load CNN, type: public-repository, public_url: https://github.com/Dororok9061/PPG-HRV-Cognitive-Load-CNN, file_reference: source and public paper, pages: "", used_for: pipeline and metric conditions }
  - { title: PPG-HRV project page, type: portfolio-page, public_url: /projects/ppg-hrv/, file_reference: public project data, pages: "", used_for: published result boundary }
prerequisites: [classification, confusion-matrix, cross-validation]
learning_objectives: [subject split 확인, fold aggregation 조건 기록, AUC와 F1 출처 분리]
related_projects: [ppg-hrv]
related_posts: []
tags: [cnn, hrv, model-evaluation, data-leakage]
cover_image: /assets/images/projects/ppg-pipeline.webp
thumbnail: /assets/images/projects/ppg-pipeline.webp
image_alt: PPG AFE와 STM32 취득에서 IBI HRV 전처리와 CNN 평가까지 연결한 pipeline
draft: false
revision_history:
  - { date: 2026-07-31, change: 최초 공개 }
  - { date: 2026-08-01, change: "split, fold, preprocessing, confusion matrix와 실제 pipeline 추가" }
toc:
  - { id: question, title: 먼저 확인할 질문 }
  - { id: pipeline, title: PPG에서 분류까지의 Pipeline }
  - { id: split, title: Subject Split과 Fold }
  - { id: metrics, title: AUC·F1·Confusion Matrix }
  - { id: results, title: Paper Result와 Code Archive }
  - { id: limits, title: 확인하지 못한 내용 }
---

## 먼저 확인할 질문 {#question}

모델 이름과 metric 이름이 같아도 수치를 바로 비교할 수는 없다. PPG-HRV 분류에서는 다음 조건이 결과를 바꾼다.

- 같은 피험자의 segment가 train과 test에 동시에 들어갔는가?
- split이 sample, recording, session, subject 중 어느 단위인가?
- preprocessing과 peak rejection을 fold 밖에서 미리 수행했는가?
- AUC가 fold별 값의 평균인지, 모든 prediction을 합친 값인지?
- F1이 binary, macro, weighted 중 무엇인지?

값 옆에 이 조건이 없으면 `0.85`가 무엇을 의미하는지 다시 계산할 수 없다.

## PPG에서 분류까지의 Pipeline {#pipeline}

<figure><picture><source srcset="/assets/images/projects/ppg-pipeline.webp" type="image/webp"><img src="/assets/images/projects/ppg-pipeline.jpg" alt="Earlobe PPG sensor, STM32 acquisition, IBI HRV preprocessing, CNN Transformer evaluation pipeline" width="1200" height="750" loading="lazy"></picture><figcaption>PPG sample timing에서 peak·IBI·HRV feature·model evaluation까지의 처리 순서다.</figcaption></figure>

Earlobe PPG sensor와 analog front-end의 sample이 STM32를 거쳐 저장된다. Peak 위치에서 inter-beat interval을 만들고 time-domain·frequency-domain HRV feature를 구성한다. 그 뒤 CNN 계열 분류와 평가로 넘어간다.

어느 단계에서 sample을 제거하거나 보간했는지 기록하지 않으면 원 PPG와 model input의 대응이 끊긴다. 특히 peak rejection threshold와 IBI correction은 label을 보기 전에 정해야 data leakage를 줄일 수 있다.

## Subject Split과 Fold {#split}

Biomedical signal은 한 사람의 여러 segment가 서로 비슷하다. Segment 단위 random split은 같은 subject의 패턴을 train과 test에 흘릴 수 있다. 일반화 대상을 “새로운 사람”으로 정의한다면 subject ID를 기준으로 group split해야 한다.

Cross validation에서는 각 fold의 train subject, validation subject, test subject 목록과 seed를 보존한다. Scaling, feature selection, missing-value 처리도 train fold에서 fit한 뒤 validation/test에 적용해야 한다. 전체 dataset으로 먼저 normalize하면 test 정보가 preprocessing parameter에 들어간다.

## AUC·F1·Confusion Matrix {#metrics}

**AUC**는 threshold를 바꾸며 true-positive rate와 false-positive rate의 관계를 본다. Class imbalance가 크면 ROC-AUC만으로 positive class의 실제 precision을 읽기 어렵기 때문에 PR curve도 함께 확인할 필요가 있다.

**F1**은 precision과 recall의 조화평균이다. Threshold, positive label, averaging 방식이 바뀌면 값이 달라진다. **Confusion matrix**는 TP, FP, FN, TN의 개수를 보여주므로 false alarm과 miss의 방향을 확인할 수 있다. Subject별 sample 수가 다르면 sample-level matrix와 subject-level summary도 구분한다.

<figure><picture><source srcset="/assets/images/projects/ppg-architecture.webp" type="image/webp"><img src="/assets/images/projects/ppg-architecture.jpg" alt="PPG acquisition, HRV preprocessing과 CNN model evaluation architecture" width="878" height="363" loading="lazy"></picture><figcaption>Metric은 pipeline 끝의 숫자가 아니라 split·preprocessing·aggregation 조건에 연결된 결과다.</figcaption></figure>

## Paper Result와 Code Archive {#results}

논문 Abstract가 보고한 평균 AUC는 **0.85**, F1-Score는 **0.82**다. 별도 code archive의 5-fold CSV는 dataset scope, fold 구성, aggregation 방식이 논문과 같은지 먼저 확인한 뒤 비교해야 한다. 그래서 현재는 두 값을 평균하거나 한 표의 동일 실험으로 합치지 않았다.

각 결과 묶음에는 최소한 source 파일, dataset 범위, exclusion, split 단위, fold 수, preprocessing version, model checkpoint, metric code를 연결해야 한다. 공개할 수 없는 피험자 raw signal은 넣지 않고 group-level aggregate와 재현 절차만 공개한다.

## 확인하지 못한 내용 {#limits}

당시 저장한 파일만으로는 모든 fold의 subject split과 preprocessing version을 다시 맞춰 돌릴 수 없었다. 그래서 논문 표의 수치와 별도 코드 실행 수치를 각각 적었다. 다음에는 subject-group split 목록과 fold별 prediction을 다시 만든 뒤 metric 계산을 비교할 예정이다.
