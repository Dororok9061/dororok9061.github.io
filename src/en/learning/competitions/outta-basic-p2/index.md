---
layout: learning
mode: competition
competition_id: outta-basic-p2
title: "[2024][Basic][P2] Real and Fake Job Postings"
lead: I revisited the interrupted BERT run and built a duplicate-aware TF-IDF and LinearSVC baseline.
description: OUTTA Basic P2 notes on grouped text splitting, local metrics, and a secret-free rerun.
permalink: /en/learning/competitions/outta-basic-p2/
lang: en
alternate_url: /learning/competitions/outta-basic-p2/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/kaggle/p2-competition.webp' | relative_url }}" alt="Kaggle P2 Real and Fake Job Postings overview" width="1290" height="811"><figcaption>The saved screen confirms the BERT-only rule and Accuracy metric.</figcaption></figure>

## Where the earlier run stopped

The notebook loaded 12,516 training rows and 5,364 test rows, but training stopped at step 51 of 352. I treated the preprocessing and partial output as a historical run, not a completed BERT result.

## Duplicate-aware split

Exact duplicate descriptions stay in one group before the train, calibration, and holdout split. This prevents a model from seeing the same job description on both sides.

## Local baseline

Word and character TF-IDF with a class-weighted LinearSVC reached 0.9896 accuracy, 0.9307 balanced accuracy, 0.8879 F1, and 0.9187 average precision on the holdout. I reported minority-class precision and recall alongside accuracy.

The old notebook contained a plaintext API key. I excluded it, moved credential access to an environment variable, and left revocation and replacement to the credential owner. These numbers are local holdout results, not Kaggle leaderboard results.
