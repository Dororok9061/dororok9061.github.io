---
layout: learning
mode: competition
competition_id: outta-basic-p1
title: "[2024][Basic][P1] Sign Language Classification"
lead: VGG16 조건의 수어 이미지 분류 과제를 다시 보고, 낮은 1-epoch 결과와 새 로컬 분할 실험을 비교했다.
description: OUTTA Basic P1 수어 이미지 분류의 과거 Notebook과 HOG·RBF-SVM 로컬 재실행 기록.
permalink: /learning/competitions/outta-basic-p1/
lang: ko
alternate_url: /en/learning/competitions/outta-basic-p1/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/kaggle/p1-competition.webp' | relative_url }}" alt="Kaggle P1 Sign Language Classification 대회 개요 화면" width="992" height="740"><figcaption>당시 화면에서 대회 제목, 진행 기간, VGG16 사용 조건을 다시 확인했다.</figcaption></figure>

## 처음 Notebook의 결과

당시 코드는 28×28 grayscale 이미지를 VGG16 입력으로 바꿔 한 epoch을 학습했다. 저장된 출력은 train loss 2.5738, train accuracy 0.2781이었다. epoch을 늘리기 전에 입력 크기 변환, channel 복제, class balance가 실제로 의도한 흐름인지부터 다시 살폈다.

## 가벼운 기준선을 만든 이유

GPU 학습만 반복하면 데이터 문제가 모델에 가려질 수 있어 HOG 특징과 RBF-SVM으로 별도 기준선을 만들었다. 80/20 stratified random-row split에서 accuracy와 macro-F1이 모두 1.0으로 나왔다.

## 1.0을 그대로 성능이라고 쓰지 않은 이유

원 데이터에는 촬영자나 원본 이미지 group ID가 없었다. 증강본이나 거의 같은 이미지가 train과 validation에 나뉘면 과도하게 높은 수치가 나올 수 있다. 그래서 이 값은 현재 분할에서 코드가 동작한 결과로만 남기고, 새로운 사람의 수어를 분류하는 일반화 성능으로 해석하지 않았다.

## 다음 비교

다음 실행에서는 perceptual hash로 유사 이미지를 묶은 group split을 만들고, 같은 분할에서 VGG16과 HOG 기준선을 비교할 예정이다. Kaggle에 로그인해 제출한 점수나 순위를 재현한 실험은 아니다.
