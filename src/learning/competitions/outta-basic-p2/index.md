---
layout: learning
mode: competition
competition_id: outta-basic-p2
title: "[2024][Basic][P2] Real and Fake Job Postings"
lead: 중간에 멈춘 BERT 실행을 다시 읽고, 중복 description을 묶은 분할에서 TF-IDF·LinearSVC 기준선을 만들었다.
description: OUTTA Basic P2 구인공고 진위 분류의 중복 그룹 분할과 비밀정보를 제거한 로컬 재실행 기록.
permalink: /learning/competitions/outta-basic-p2/
lang: ko
alternate_url: /en/learning/competitions/outta-basic-p2/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/kaggle/p2-competition.webp' | relative_url }}" alt="Kaggle P2 Real and Fake Job Postings 대회 개요 화면" width="1290" height="811"><figcaption>당시 화면에서 BERT 사용 조건과 Accuracy 평가 방식을 다시 확인했다.</figcaption></figure>

## 남아 있던 실행 위치

Notebook에는 train 12,516개, test 5,364개를 읽은 기록이 있었지만 학습은 352 step 중 51 step에서 멈춰 있었다. 완성된 BERT 결과처럼 쓰지 않고, 실제로 남은 전처리와 중간 학습 출력까지만 과거 기록으로 봤다.

## 중복 문장을 먼저 묶었다

같은 `description`이 train과 validation에 동시에 들어가면 모델이 문장을 외워도 높은 점수를 받을 수 있다. exact duplicate description을 하나의 group으로 묶은 뒤 train, calibration, holdout으로 나눴다.

## 새 기준선

word·character TF-IDF와 class-weighted LinearSVC를 사용하고 calibration split에서 F1 threshold를 골랐다. holdout accuracy 0.9896, balanced accuracy 0.9307, F1 0.8879, average precision 0.9187이 나왔다. 불균형 데이터라 accuracy 하나보다 fake class의 precision과 recall을 함께 봤다.

## API Key 처리

예전 Notebook에는 평문 API Key가 들어 있었다. 원본 파일은 올리지 않았고 공개용 코드는 환경변수에서 값을 읽도록 바꿨다. 기존 키는 소유자 계정에서 폐기하고 다시 발급해야 한다. 위 숫자는 로컬 holdout 결과이며 Kaggle leaderboard 점수가 아니다.
