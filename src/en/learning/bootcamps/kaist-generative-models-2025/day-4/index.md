---
layout: course-day
course_id: 2025-generative-models
day: 4
title: 2025 Generative Models Intensive Day 4
description: Notes on alternating GAN objectives and Pix2Pix conditional adversarial and L1 losses.
permalink: /en/learning/bootcamps/kaist-generative-models-2025/day-4/
lang: en
alternate_url: /learning/bootcamps/kaist-generative-models-2025/day-4/
alternate_lang: ko
---

<figure><img src="{{ '/assets/images/learning/generative/gan-pix2pix.svg' | relative_url }}" alt="Generator, generated result, discriminator, and Pix2Pix loss" width="1200" height="630"><figcaption>Pix2Pix adds an input condition and an L1 reconstruction term to the adversarial game.</figcaption></figure>

## Alternating two optimizers

I split the minimax objective from [Generative Adversarial Nets](https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html) into discriminator and generator updates. Generated samples are detached for the D update; the G update keeps the gradient path through D without updating D's parameters.

## Reading the loss curves

A small discriminator loss does not mean that generation is good. I need the two curves, generated samples, and diversity together to spot an overpowering discriminator or mode collapse.

## Pix2Pix

[Pix2Pix](https://openaccess.thecvf.com/content_cvpr_2017/html/Isola_Image-To-Image_Translation_With_CVPR_2017_paper.html) conditions both networks on the input image. Its adversarial term rewards realistic local structure, while L1 helps preserve the paired target and U-Net skip connections carry spatial detail.

I did not retain a paired-image output from the course run, so a direct L1-only comparison remains a future rerun.
