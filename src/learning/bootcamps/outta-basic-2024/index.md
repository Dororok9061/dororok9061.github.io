---
layout: learning
mode: program
program_id: outta-basic-2024
title: 2024 OUTTA AI 부트캠프 딥러닝반 Basic
lead: 강의자료와 내가 저장한 Notebook 사본을 다시 열어 데이터 처리부터 CNN·RNN·BERT까지 학습 흐름을 정리했다.
description: OUTTA Basic 강의자료, Notebook 출력, P1·P2·P3 재실행을 연결한 학습 기록.
permalink: /learning/bootcamps/outta-basic-2024/
lang: ko
alternate_url: /en/learning/bootcamps/outta-basic-2024/
alternate_lang: en
---

## 강의자료를 다시 분류한 방법

압축파일 안의 PDF 16개는 모두 열어 보았다. 전체 530쪽에는 데이터 전처리, Dataset과 DataLoader, 선형회귀와 경사하강법, 신경망, CNN, 언어모델, Word Embedding, RNN, BERT, GPT, 전이학습, 프로젝트 안내가 이어진다. 나는 파일 번호와 개념의 선후관계를 기준으로 다섯 묶음으로 다시 정리했다.

1. 데이터와 회귀: 데이터 분포를 보고 Tensor로 바꾸는 과정
2. 신경망과 CNN: forward, loss, backpropagation, image classification
3. 언어 표현: language model, embedding, autoencoder
4. 순차 모델: RNN, seq2seq, BERT와 Hugging Face
5. 프로젝트: P1 수어, P2 구인공고, P3 음악 장르 분류

## Notebook에서 확인한 출력

내가 저장한 Notebook 사본 15개에는 48개의 그림 출력이 남아 있었다. 일부 사본에는 내가 고친 코드가 있지만 모두 수정본인 것은 아니다. 모든 Cell의 실행 순서를 현재 환경에서 다시 재현한 것은 아니므로, 아래 그림은 당시 저장된 출력으로 설명한다.

<figure>
  <img src="{{ '/assets/images/learning/outta/notebook-23.webp' | relative_url }}" alt="Universal Approximator 실습에서 서로 다른 sigmoid 함수 열 개를 그린 결과" width="1198" height="790" loading="lazy">
  <figcaption>여러 sigmoid basis를 조합하기 전, 위치와 기울기가 다른 함수의 모양을 비교했다.</figcaption>
</figure>

Universal Approximator 실습에서는 같은 sigmoid라도 bias와 weight에 따라 전이 위치와 기울기가 달라졌다. 이 출력을 보고 은닉층의 여러 unit이 단순한 함수를 합쳐 복잡한 곡선을 만들 수 있다는 설명을 다시 연결했다.

<figure>
  <img src="{{ '/assets/images/learning/outta/notebook-39.webp' | relative_url }}" alt="CNN Notebook이 손글씨 숫자를 잘못 분류한 예시 스물다섯 개" width="794" height="812" loading="lazy">
  <figcaption>CNN 결과에서 예측과 정답이 다른 표본을 모아 본 화면이다.</figcaption>
</figure>

CNN 결과는 정확도 숫자만 보지 않고 틀린 표본의 모양부터 확인했다. 흐릿하거나 획이 붙은 숫자에서 오류가 몰렸고, 전처리와 augmentation을 바꾸기 전에 실패 표본을 먼저 보는 습관이 필요했다.

<figure>
  <img src="{{ '/assets/images/learning/outta/notebook-44.webp' | relative_url }}" alt="RNN 학습 정확도는 상승하지만 시험 정확도는 0.5 부근에 머문 그래프" width="846" height="470" loading="lazy">
  <figcaption>학습 정확도만 계속 오르고 시험 정확도는 개선되지 않은 RNN 실행 결과다.</figcaption>
</figure>

RNN Notebook에서는 train accuracy가 거의 1.0까지 오르는 동안 test accuracy가 0.5 부근에 머물렀다. 이 결과를 보고 epoch을 늘리는 것만으로 일반화가 좋아지지 않으며, 데이터 분할과 sequence length, regularization을 함께 확인해야 한다고 정리했다.

## 세 프로젝트를 다시 실행한 이유

P1·P2·P3의 과거 Notebook에는 낮은 학습 정확도와 중간에 멈춘 실행이 남아 있었다. 그래서 원본은 보존하고 별도 코드에서 전처리와 검증 분할을 다시 구성했다.

- [P1 Sign Language Classification]({{ '/learning/competitions/outta-basic-p1/' | relative_url }})에서는 HOG와 RBF-SVM을 비교했다. 무작위 행 분할의 1.0 정확도는 유사 이미지 누수 가능성이 있어 일반화 성능으로 해석하지 않았다.
- [P2 Real and Fake Job Postings]({{ '/learning/competitions/outta-basic-p2/' | relative_url }})에서는 중복 description이 서로 다른 분할에 섞이지 않게 묶고 TF-IDF와 LinearSVC를 사용했다.
- [P3 Music Genre Classification]({{ '/learning/competitions/outta-basic-p3/' | relative_url }})에서는 MFCC·chroma·spectral summary를 만들고 RBF-SVM을 교차검증했다.

## 공개용 코드에서 바꾼 점

예전 실습 Notebook 하나에는 API Key가 평문으로 남아 있었다. 그 파일은 저장소에 넣지 않았고, 공개용 코드는 환경변수에서 값을 읽도록 바꿨다. 강의 PDF와 데이터셋도 재배포하지 않고 내가 작성한 설명, 안전하게 정제한 코드, 직접 생성한 결과 그림만 연결했다.
