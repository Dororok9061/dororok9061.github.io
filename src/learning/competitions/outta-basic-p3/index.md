---
layout: learning
mode: competition
competition_id: outta-basic-p3
title: "[2024][Basic][P3] Music Genre Classification"
lead: 10-epoch 음악 장르 분류 결과를 다시 읽고, 리듬·스펙트럼 특징과 RBF-SVM으로 로컬 기준선을 개선했다.
description: OUTTA Basic P3 음악 장르 분류의 MFCC·chroma·spectral summary와 로컬 재실행 기록.
permalink: /learning/competitions/outta-basic-p3/
lang: ko
alternate_url: /en/learning/competitions/outta-basic-p3/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/kaggle/p3-competition.webp' | relative_url }}" alt="Kaggle P3 Music Genre Classification 대회 개요 화면" width="1180" height="797"><figcaption>정해진 사전학습 모델 없이 직접 모델을 설계하는 과제였다.</figcaption></figure>

## 당시 학습 결과

Notebook에는 10 epoch 뒤 train loss 1.4228, train accuracy 0.5088이 남아 있었다. 음악 장르는 시간축 신호이므로 raw waveform만 넣기보다 어떤 음향 특징이 장르 차이를 드러내는지 먼저 비교했다.

## 특징을 다시 구성했다

MFCC와 delta는 음색의 시간 변화를, chroma는 pitch-class 에너지를, spectral centroid·bandwidth·rolloff는 주파수 분포를 요약한다. 각 통계량을 표준화한 뒤 RBF-SVM의 C를 training fold 안에서만 선택했다.

## 로컬 결과

80/20 stratified holdout에서 accuracy 0.8142, balanced accuracy 0.8120, macro-F1 0.8108을 얻었다. 단순 기준선의 macro-F1 0.0188과 비교하면 모든 class를 거의 한쪽으로 보내던 문제가 줄었다.

## 남은 한계

파일에는 track이나 artist group metadata가 없었다. 같은 artist의 유사한 녹음이 양쪽 분할에 있을 가능성을 배제하지 못하므로, 이 수치는 무작위 층화 분할의 로컬 결과다. Kaggle 제출 점수나 순위로 바꾸어 쓰지 않았다.
