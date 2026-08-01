---
title: Preserving evaluation conditions for AUC and F1 in PPG-HRV classification
title_en: Preserving evaluation conditions for AUC and F1 in PPG-HRV classification
description: Why subject splits, folds, preprocessing, confusion matrices, and paper-reported metrics are not merged into one performance value.
date: 2026-07-31 00:51:00 +0900
updated: 2026-08-01 18:41:00 +0900
study_date: 2026-07-31
lang: en
translation_key: biomedical-metric-provenance
permalink: /en/blog/2026/07/31/biomedical-metric-provenance/
alternate_url: /blog/2026/07/31/biomedical-metric-provenance/
alternate_lang: ko
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
  - { title: PPG-HRV Cognitive Load CNN, type: public-repository, public_url: https://github.com/Tontonjeong/PPG-HRV-Cognitive-Load-CNN, file_reference: source and public paper, pages: "", used_for: pipeline and metric provenance }
  - { title: PPG-HRV project page, type: portfolio-page, public_url: /en/projects/ppg-hrv/, file_reference: public project data, pages: "", used_for: published result boundary }
prerequisites: [classification, confusion-matrix, cross-validation]
learning_objectives: [inspect subject splits, record fold aggregation, separate AUC and F1 sources]
related_projects: [ppg-hrv]
related_posts: []
tags: [cnn, hrv, model-evaluation, data-leakage]
cover_image: /assets/images/projects/ppg-pipeline.webp
thumbnail: /assets/images/projects/ppg-pipeline.webp
image_alt: Pipeline from PPG AFE and STM32 acquisition through IBI HRV preprocessing and CNN evaluation
draft: false
revision_history:
  - { date: 2026-07-31, change: Initial publication }
  - { date: 2026-08-01, change: "Added split, fold, preprocessing, confusion-matrix, and pipeline detail" }
toc:
  - { id: question, title: Questions before comparing values }
  - { id: pipeline, title: PPG-to-classification pipeline }
  - { id: split, title: Subject splits and folds }
  - { id: metrics, title: "AUC, F1, and confusion matrices" }
  - { id: provenance, title: Paper result and code archive }
  - { id: limits, title: Unverified items }
---

## Questions before comparing values {#question}

Matching model and metric names do not make two values comparable. In PPG-HRV classification, the result changes with these decisions:

- Can segments from one participant enter both train and test sets?
- Is the split made by sample, recording, session, or subject?
- Was preprocessing or peak rejection fitted before the folds were formed?
- Is AUC the mean of fold values or a pooled prediction result?
- Is F1 binary, macro, or weighted?

Without those conditions, a number such as `0.85` cannot be reproduced or interpreted correctly.

## PPG-to-classification pipeline {#pipeline}

<figure><picture><source srcset="/assets/images/projects/ppg-pipeline.webp" type="image/webp"><img src="/assets/images/projects/ppg-pipeline.jpg" alt="Pipeline connecting an earlobe PPG sensor, STM32 acquisition, IBI HRV preprocessing, and CNN Transformer evaluation" width="1200" height="750" loading="lazy"></picture><figcaption>Provenance is maintained from sample timing through peaks, IBIs, HRV features, and model evaluation.</figcaption></figure>

An earlobe PPG sensor and analog front-end feed samples to STM32 acquisition. Peak locations produce inter-beat intervals, followed by time- and frequency-domain HRV features and CNN-family classification.

Sample rejection and interpolation must be recorded. Peak-rejection thresholds and IBI correction should be fixed without using test labels; otherwise preprocessing can leak information.

## Subject splits and folds {#split}

Segments from one participant are correlated. A random segment split can place one person's patterns in both training and testing. When the target is generalization to unseen people, the split should group by subject.

Each cross-validation fold needs preserved train, validation, and test subject lists plus a seed. Scaling, feature selection, and missing-value processing must be fitted on the training fold and then applied to validation and test data. Dataset-wide normalization before splitting leaks test information into preprocessing parameters.

## AUC, F1, and confusion matrices {#metrics}

**AUC** summarizes the tradeoff between true-positive and false-positive rates across thresholds. With strong class imbalance, ROC-AUC alone may hide poor positive-class precision, so a precision-recall curve is useful.

**F1** is the harmonic mean of precision and recall. Threshold, positive label, and averaging method all change it. A **confusion matrix** exposes TP, FP, FN, and TN counts, making false alarms and misses visible. Sample-level and subject-level summaries should remain separate when subject sample counts differ.

<figure><picture><source srcset="/assets/images/projects/ppg-architecture.webp" type="image/webp"><img src="/assets/images/projects/ppg-architecture.jpg" alt="Architecture connecting PPG acquisition, HRV preprocessing, and CNN evaluation" width="878" height="363" loading="lazy"></picture><figcaption>A metric is tied to split, preprocessing, and aggregation conditions rather than presented as an isolated endpoint.</figcaption></figure>

## Paper result and code archive {#provenance}

The public paper abstract reports average AUC **0.85** and F1-score **0.82**. These values are labeled `PAPER_REPORTED`. A separate five-fold CSV archive is not averaged with them or placed in the same experiment row unless dataset scope, folds, and aggregation are shown to match.

Each result bundle should retain its source file, dataset scope, exclusions, split unit, fold count, preprocessing version, model checkpoint, and metric code. Participant raw signals remain private; only group-level aggregates and a reproducible procedure are public.

## Unverified items {#limits}

The public evidence does not provide a fresh run proving that every fold used the same subject split and preprocessing version. The paper values are not claimed as reproduced in the current environment. The next verification step is an anonymized group-split manifest plus fold-level predictions linked back to metric calculation.
