---
layout: learning
mode: competition
competition_id: outta-basic-p3
title: "[2024][Basic][P3] Music Genre Classification"
lead: I revisited the ten-epoch run and improved a local baseline with rhythmic and spectral features.
description: OUTTA Basic P3 notes on MFCC, chroma, spectral summaries, and a local RBF-SVM rerun.
permalink: /en/learning/competitions/outta-basic-p3/
lang: en
alternate_url: /learning/competitions/outta-basic-p3/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/kaggle/p3-competition.webp' | relative_url }}" alt="Kaggle P3 Music Genre Classification overview" width="1180" height="797"><figcaption>The project required participants to design their own model.</figcaption></figure>

## Earlier result

The notebook retained ten epochs with a final train loss of 1.4228 and train accuracy of 0.5088. I compared acoustic summaries before committing to another end-to-end neural model.

## Feature set

MFCC and delta features describe timbral change, chroma summarizes pitch-class energy, and centroid, bandwidth, and rolloff summarize the spectrum. I standardized the features and selected the RBF-SVM C value only inside training folds.

## Local result

The 80/20 stratified holdout produced 0.8142 accuracy, 0.8120 balanced accuracy, and 0.8108 macro-F1. The simple baseline macro-F1 was 0.0188.

Track and artist group metadata was unavailable, so artist-conditioned separation was not possible. These are local split metrics rather than a Kaggle score or rank.
