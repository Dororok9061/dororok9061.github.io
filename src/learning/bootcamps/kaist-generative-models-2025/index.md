---
layout: learning
mode: program
program_id: kaist-generative-models-2025
title: VAE부터 Stable Diffusion까지, 생성모델의 AtoZ
lead: 2025년 7월 7일부터 11일까지 들은 20시간 과정을 다섯 날의 공부 흐름으로 다시 정리했다.
description: 생성모델 기초, Autoregressive Model, VAE, GAN, Pix2Pix, Diffusion, Stable Diffusion 학습 기록.
permalink: /learning/bootcamps/kaist-generative-models-2025/
lang: ko
alternate_url: /en/learning/bootcamps/kaist-generative-models-2025/
alternate_lang: en
---

## 내가 다시 잡은 학습 순서

먼저 생성모델이 관측한 데이터의 분포를 배운다는 뜻을 정리했다. 그다음 결합확률을 순서대로 푸는 Autoregressive Model과 Maximum Likelihood를 거쳐 VAE, GAN, Pix2Pix, Diffusion으로 넘어갔다. 강의자료의 파일 번호가 실제 날짜와 일대일로 대응한다고 단정하지 않고, 다섯 날 동안 이해한 개념의 선후관계로 묶었다.

## 읽은 원 논문

강의 노트를 다시 쓰면서 [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114), [Generative Adversarial Nets](https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html), [Pix2Pix](https://openaccess.thecvf.com/content_cvpr_2017/html/Isola_Image-To-Image_Translation_With_CVPR_2017_paper.html), [DDPM](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html), [Latent Diffusion](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html), [DiT](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html)을 함께 확인했다. 블로그 그림은 논문 이미지를 복사하지 않고 학습 흐름을 직접 다시 그렸다.

## 아직 이어서 할 실습

당시 저장한 Colab 출력이 모든 주제에 남아 있지는 않았다. 그래서 실행 화면이 없는 부분은 수식과 코드 흐름까지만 적었고, 새로운 결과 이미지를 만들어 과거 실행처럼 넣지 않았다. 다음에는 VAE latent interpolation과 DDPM sampling loop를 현재 환경에서 다시 실행해 비교할 예정이다.
