---
title: Interpretation boundary for radar AO/AC candidates after ECG-anchored beat alignment
title_en: Interpretation boundary for radar AO/AC candidates after ECG-anchored beat alignment
description: ECG R-peaks, SCG references, FMCW phase morphology, and the distinction between candidate timing and direct valve measurement.
date: 2026-07-31 00:31:00 +0900
updated: 2026-08-01 18:51:00 +0900
study_date: 2026-07-31
lang: en
translation_key: radar-candidate-timing
permalink: /en/blog/2026/07/31/radar-candidate-timing/
alternate_url: /blog/2026/07/31/radar-candidate-timing/
alternate_lang: ko
primary_category: rf-radar-signal
subcategory: ecg-scg-radar
series: fmcw-radar-signal-processing
series_order: 4
post_type: paper-review
difficulty: advanced
study_status: published
evidence_status: SOURCE_HARDWARE_AND_PAPER_REPORTED
tools: [Python, NumPy, SciPy]
hardware: [BGT60TR13C, STM32F411, ESP-32S, MPU6050]
software_versions: [not fully preserved]
source_materials:
  - { title: FMCW Radar AOAC Cardiac Analysis, type: public-repository, public_url: https://github.com/Tontonjeong/fmcw-radar-aoac-cardiac-analysis, file_reference: analysis source and firmware, pages: "", used_for: signal flow and candidate timing boundary }
  - { title: FMCW Radar Cardiac Timing project, type: portfolio-page, public_url: /en/projects/fmcw-radar/, file_reference: public project data, pages: "", used_for: hardware and reported acquisition summary }
prerequisites: [fmcw-radar, phase-processing, ecg-r-peak]
learning_objectives: [align multimodal beats to ECG anchors, separate SCG references from radar morphology, record candidate-timing limits]
related_projects: [fmcw-radar]
related_posts: []
tags: [fmcw-radar, beat-alignment, phase-processing, biomedical-signal]
cover_image: /assets/images/projects/radar-hardware.webp
thumbnail: /assets/images/projects/radar-hardware.webp
image_alt: Physical setup for concurrent ECG, SCG, and BGT60TR13C FMCW radar acquisition
draft: false
revision_history:
  - { date: 2026-07-31, change: Initial publication }
  - { date: 2026-08-01, change: Added acquisition architecture, phase and beat flow, hardware, and waveform evidence }
toc:
  - { id: setup, title: Concurrent acquisition system }
  - { id: phase, title: From radar phase to beats }
  - { id: alignment, title: ECG R-peak alignment }
  - { id: candidates, title: AO/AC candidate timing }
  - { id: evidence, title: Supported results and limits }
  - { id: next, title: Next validation }
---

## Concurrent acquisition system {#setup}

ECG, SCG, and FMCW radar are acquired over the same interval, with ECG R-peaks serving as common anchors. The radar is a BGT60TR13C, with STM32F411, ESP-32S, and MPU6050 devices in the acquisition and reference paths.

<figure><picture><source srcset="/assets/images/projects/radar-hardware.webp" type="image/webp"><img src="/assets/images/projects/radar-hardware.jpg" alt="Physical setup containing ECG electrodes, an SCG sensor, BGT60TR13C radar, and acquisition boards" width="1200" height="800" loading="lazy"></picture><figcaption>Privacy-reviewed concurrent ECG, SCG, and radar hardware. It proves the setup existed, not a performance value.</figcaption></figure>

The streams cannot be compared beat by beat until timestamps, sample rates, start offsets, and missing-sample handling are understood.

## From radar phase to beats {#phase}

The processing path calculates a range FFT from FMCW chirps and selects a range bin or ROI containing chest reflections. The phase of the selected complex sample is unwrapped and converted using wavelength-related scaling to obtain a displacement-related waveform.

ROI movement and respiration can alter cardiac morphology. ROI selection, unwrap discontinuities, filtering, and motion rejection are therefore part of the candidate-timing input conditions. One visual peak is not enough to declare a valve event.

## ECG R-peak alignment {#alignment}

<figure><picture><source srcset="/assets/images/projects/fmcw-waveform.webp" type="image/webp"><img src="/assets/images/projects/fmcw-waveform.jpg" alt="ECG, SCG, and FMCW radar cardiac waveforms aligned on a common time axis" width="1011" height="642" loading="lazy"></picture><figcaption>SCG and radar waveforms placed on a beat-relative axis anchored to ECG R-peaks.</figcaption></figure>

Each R-peak defines a window around one beat. SCG reference timing and radar morphology are compared within that beat. Resampling or length normalization can change timing, so original sample indices and transformed beat coordinates should both be retained.

The paper-reported scope is **600 seconds of concurrent acquisition** and **848 corresponding beats analyzed**. These remain paper-reported values rather than a new rerun.

## AO/AC candidate timing {#candidates}

AO/AC-related SCG reference points are constructed, then temporally corresponding radar peaks, slope changes, or detector-fusion outputs are selected. Low-SQI or detector-disagreement beats need separate handling. Candidate Timing Interval summaries describe the selected-point distribution.

The AO and AC labels mean **morphology-based candidate timing**. Radar did not image the aortic valve, and valve opening or closure was not independently observed by Doppler echo. The claim is limited to temporal candidates relative to ECG and SCG references.

## Supported results and limits {#evidence}

<figure><picture><source srcset="/assets/images/projects/fmcw-experiment.webp" type="image/webp"><img src="/assets/images/projects/fmcw-experiment.jpg" alt="Concurrent acquisition setup with an STM32 board, ECG electrodes, and FMCW radar" width="1000" height="1000" loading="lazy"></picture><figcaption>Hardware evidence for the experiment and acquisition path.</figcaption></figure>

Public evidence supports analysis source, firmware, configuration/export documentation, hardware photographs, 600-second acquisition, and 848 corresponding beats. It does not support clinical sensitivity, specificity, direct valve detection, or medical-device performance. Participant raw biosignals and identifying information are not published.

## Next validation {#next}

Validation closer to an anatomical event requires a synchronized independent reference such as echocardiography, ICG, or PCG. The protocol should quantify clock error, annotation rules, beat exclusion, inter-rater agreement, and timing error or Bland–Altman behavior. Until then, candidate terminology remains necessary.
