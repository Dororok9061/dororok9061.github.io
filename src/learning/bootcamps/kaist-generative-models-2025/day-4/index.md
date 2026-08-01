---
layout: course-day
course_id: 2025-generative-models
day: 4
title: 2025 생성모델 집중과정 Day 4
description: GAN의 두 목적함수와 Pix2Pix의 conditional adversarial loss·L1 loss를 정리한 기록.
permalink: /learning/bootcamps/kaist-generative-models-2025/day-4/
lang: ko
alternate_url: /en/learning/bootcamps/kaist-generative-models-2025/day-4/
alternate_lang: en
---

<figure><img src="{{ '/assets/images/learning/generative/gan-pix2pix.svg' | relative_url }}" alt="입력, 생성기, 생성 결과, 판별기와 Pix2Pix loss를 연결한 그림" width="1200" height="630"><figcaption>GAN의 경쟁 구조에 입력 조건과 L1 reconstruction을 더하면 Pix2Pix 흐름이 된다.</figcaption></figure>

## 두 모델을 번갈아 학습하기

[GAN 원 논문](https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html)의 minimax 식을 Generator와 Discriminator 단계로 나눠 적었다. D를 학습할 때는 생성 결과를 detach하고, G를 학습할 때는 D의 parameter를 바꾸지 않으면서 D를 통과한 gradient를 G까지 전달해야 한다.

## Loss 숫자를 읽는 법

D loss가 작다고 전체 모델이 잘 학습된 것은 아니다. D가 너무 쉽게 이기면 G로 전달되는 gradient가 약해질 수 있고, 반대로 D가 무너지면 사실감을 구분하는 신호가 사라진다. 생성 표본, loss curve, diversity를 함께 봐야 했다.

## Pix2Pix에서 조건을 넣는 위치

[Pix2Pix 논문](https://openaccess.thecvf.com/content_cvpr_2017/html/Isola_Image-To-Image_Translation_With_CVPR_2017_paper.html)은 입력 영상 (x)를 G와 D 양쪽에 조건으로 준다. adversarial loss는 그럴듯한 고주파 구조를, L1 loss는 입력과 짝을 이루는 전체 형상을 유지하도록 돕는다. U-Net skip connection은 입력의 공간 정보를 출력으로 전달한다.

## 직접 비교하고 싶은 항목

같은 paired dataset에서 L1만 쓴 결과와 adversarial loss를 함께 쓴 결과를 나란히 비교할 예정이다. 당시 결과 화면이 남아 있지 않아 새 이미지를 과거 실습처럼 넣지는 않았다.
