---
layout: learning
mode: program
program_id: kaist-generative-models-2025
title: Generative Models A to Z — From VAE to Stable Diffusion
lead: I reorganized the 20-hour course held from July 7 to 11, 2025 into a five-day study sequence.
description: Study notes on generative-model foundations, autoregressive models, VAE, GAN, Pix2Pix, diffusion, and Stable Diffusion.
permalink: /en/learning/bootcamps/kaist-generative-models-2025/
lang: en
alternate_url: /learning/bootcamps/kaist-generative-models-2025/
alternate_lang: ko
---

## The sequence I used

I started with learning a data distribution, moved through autoregressive factorization and maximum likelihood, and then connected VAE, GAN, Pix2Pix, and diffusion. The source page exposed only one explicit day heading, so these pages follow my study sequence rather than claiming an official day-by-day timetable.

## Original papers I revisited

I checked [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114), [Generative Adversarial Nets](https://papers.nips.cc/paper_files/paper/2014/hash/f033ed80deb0234979a61f95710dbe25-Abstract.html), [Pix2Pix](https://openaccess.thecvf.com/content_cvpr_2017/html/Isola_Image-To-Image_Translation_With_CVPR_2017_paper.html), [DDPM](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html), [Latent Diffusion](https://openaccess.thecvf.com/content/CVPR2022/html/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.html), and [DiT](https://openaccess.thecvf.com/content/ICCV2023/html/Peebles_Scalable_Diffusion_Models_with_Transformers_ICCV_2023_paper.html). The diagrams are my own redraws rather than copied paper figures.

Some Colab outputs were not saved. For those topics I stopped at the equations and code path, and I did not invent images that looked like historical runs.
