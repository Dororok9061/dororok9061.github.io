---
layout: learning
mode: competition
competition_id: outta-basic-p1
title: "[2024][Basic][P1] Sign Language Classification"
lead: I revisited the VGG16 assignment and compared its one-epoch result with a lightweight local baseline.
description: OUTTA Basic P1 notes connecting the historical notebook with a HOG and RBF-SVM rerun.
permalink: /en/learning/competitions/outta-basic-p1/
lang: en
alternate_url: /learning/competitions/outta-basic-p1/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/kaggle/p1-competition.webp' | relative_url }}" alt="Kaggle P1 Sign Language Classification overview" width="992" height="740"><figcaption>The saved screen confirms the title, dates, and VGG16-only rule.</figcaption></figure>

## Earlier notebook

The notebook resized 28×28 grayscale images for VGG16 and retained one epoch: train loss 2.5738 and train accuracy 0.2781. I checked channel conversion, resizing, and class balance before extending training.

## Lightweight baseline

I used HOG features and an RBF-SVM on an 80/20 stratified random-row split. Accuracy and macro-F1 both reached 1.0.

## Why 1.0 is not a generalization claim

The data does not expose signer or source-image groups. Augmented or near-duplicate images may cross the split, so I treat this as a result for this local split rather than performance on unseen signers.

A future comparison will group perceptually similar images and evaluate VGG16 and HOG on the same split. No signed-in Kaggle score or rank was reproduced.
