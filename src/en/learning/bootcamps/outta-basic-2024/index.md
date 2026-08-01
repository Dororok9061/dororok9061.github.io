---
layout: learning
mode: program
program_id: outta-basic-2024
title: 2024 OUTTA AI Bootcamp — Deep Learning Basic
lead: I revisited the lecture files and my modified notebooks, then connected data handling, CNNs, RNNs, BERT, and the three projects.
description: Study notes connecting OUTTA Basic materials, saved notebook outputs, and local P1-P3 reruns.
permalink: /en/learning/bootcamps/outta-basic-2024/
lang: en
alternate_url: /learning/bootcamps/outta-basic-2024/
alternate_lang: ko
---

## How I reorganized the course

I reviewed all 16 PDFs in the archive: 530 pages covering preprocessing, Dataset and DataLoader, regression, gradient descent, neural networks, CNNs, language models, embeddings, RNNs, BERT, GPT, transfer learning, and project guidance. I grouped the material into data and regression, neural networks and CNNs, language representation, sequence models, and the three projects.

## Saved notebook outputs

Fifteen modified notebooks retained 48 figures. I did not claim a fresh end-to-end run of every cell; the plots below are outputs saved in the notebooks.

<figure><img src="{{ '/assets/images/learning/outta/notebook-23.webp' | relative_url }}" alt="Ten sigmoid basis functions from the Universal Approximator notebook" width="1198" height="790" loading="lazy"><figcaption>Changing weights and biases shifts the position and slope of each sigmoid basis.</figcaption></figure>

<figure><img src="{{ '/assets/images/learning/outta/notebook-39.webp' | relative_url }}" alt="Twenty-five CNN misclassifications with predictions and true labels" width="794" height="812" loading="lazy"><figcaption>I inspected failure samples before changing preprocessing or augmentation.</figcaption></figure>

<figure><img src="{{ '/assets/images/learning/outta/notebook-44.webp' | relative_url }}" alt="RNN training accuracy rising while test accuracy stays near one half" width="846" height="470" loading="lazy"><figcaption>The curve shows memorization without a matching gain on the test split.</figcaption></figure>

## P1, P2, and P3

I kept the original notebooks and built separate reruns. P1 compares HOG with an RBF-SVM, P2 groups duplicate descriptions before TF-IDF and LinearSVC training, and P3 combines MFCC, chroma, and spectral summaries with an RBF-SVM. The result pages explain the split and its limitations.

- [P1 Sign Language Classification]({{ '/en/learning/competitions/outta-basic-p1/' | relative_url }})
- [P2 Real and Fake Job Postings]({{ '/en/learning/competitions/outta-basic-p2/' | relative_url }})
- [P3 Music Genre Classification]({{ '/en/learning/competitions/outta-basic-p3/' | relative_url }})

One old practice notebook contained a plaintext API key. I excluded it and changed the public example to read secrets from environment variables. Course PDFs and datasets are not redistributed.
