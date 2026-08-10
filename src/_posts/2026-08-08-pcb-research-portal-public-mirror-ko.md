---
title: PCB Research Publication Workbench 공개 미러
title_en: PCB Research Publication Workbench public mirror
description: 로컬 8765 포털에서 검증한 PCB inspection figure atlas와 lightbox 구성을 GitHub Pages 블로그와 프로젝트 허브에 다시 반영했습니다.
date: 2026-08-07 23:55:00 +0900
updated: 2026-08-10 00:00:00 +0900
study_date: 2026-08-07
lang: ko
translation_key: pcb-research-portal-public-mirror
permalink: /blog/2026/08/08/pcb-research-portal-public-mirror/
alternate_url: /en/blog/2026/08/08/pcb-research-portal-public-mirror/
alternate_lang: en
primary_category: research-project-log
subcategory: project-log
series: engineering-record-lineage
series_order: 3
post_type: project-log
difficulty: intermediate
study_status: published
evidence_status: SOURCE_AVAILABLE
tools: [Jekyll, GitHub Pages, Material Icons]
hardware: [STM32F411, camera]
software_versions: []
source_materials:
  - { title: PCB Research Publication Workbench, type: public-page, public_url: /projects/pcb-visual-inspection/research-portal/?fresh=20260810-main-republish#methodology, file_reference: src/projects/pcb-visual-inspection/research-portal, pages: "", used_for: public mirror }
  - { title: PCB Visual Inspection Studio repository paper package, type: github-repository, public_url: https://github.com/Dororok9061/PCB-Visual-Inspection-Studio/tree/main/docs/paper, file_reference: docs/paper, pages: "", used_for: paper package }
prerequisites: [PCB inspection, figure source mapping, GitHub Pages]
learning_objectives: [local portal and public site sync, individual figure atlas publication, click-to-enlarge review flow]
related_projects: [pcb-visual-inspection]
related_posts: [evidence-status]
tags: [pcb-inspection, github-pages, figure-atlas, lightbox]
cover_image: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp
thumbnail: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp
image_alt: PCB inspection pipeline and paper-style figure atlas
draft: false
published: true
revision_history:
  - date: 2026-08-07
    change: Public mirror route wired from the local portal
  - date: 2026-08-10
    change: Added primary pipeline and architecture figures to the blog
toc:
  - { id: mirror, title: 공개 미러 경로 }
  - { id: key-figures, title: 주요 그림 }
  - { id: pipeline, title: 파이프라인과 아키텍처 }
  - { id: results, title: 결과표와 주장 경계 }
  - { id: links, title: 연결 경로 }
---

## 공개 미러 경로 {#mirror}

로컬 `127.0.0.1:8765` 포털에서 확인하던 PCB inspection publication workbench를 GitHub Pages 경로로 다시 연결했습니다.

[전체 Research Publication Workbench 열기](/projects/pcb-visual-inspection/research-portal/?fresh=20260810-main-republish#methodology)

이번 반영의 핵심은 contact sheet 하나로 뭉쳐 보이는 방식이 아니라, 논문 본문에서 바로 읽을 수 있는 대표 그림과 개별 확대 가능한 figure card를 함께 노출하는 것입니다. 각 그림은 `data-lightbox`를 통해 클릭하면 크게 볼 수 있습니다.

## 주요 그림 {#key-figures}

<div class="publication-figure-grid">
{% assign figure_cards = "/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp|Capture and quality gate;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31b_vit_dino_patch_path.webp|ViT DINO patch path;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31c_registration_memory_bank.webp|Registration and memory bank;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig13_heatmap_gt_mask.webp|Heatmap GT and mask;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig14_threshold_masks.webp|Threshold masks;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig15_dataset_examples.webp|Dataset examples;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig16_pro_line_chart.webp|Mean PRO line chart;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig18_loss_convergence.webp|Loss convergence;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig19_qualitative_grid.webp|Qualitative inspection grid;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig25_embedding_filters.webp|Embedding filters;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig29_layer_attention_maps.webp|Layer attention maps;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_table07_industrial_scores.webp|Industrial score tables;/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_table09_full_result.webp|Full result table" | split: ";" %}
{% for item in figure_cards %}
{% assign parts = item | split: "|" %}
<figure class="publication-figure-card">
  <button class="publication-figure-trigger" type="button" data-lightbox="{{ parts[0] }}" data-lightbox-alt="{{ parts[1] }}" data-lightbox-caption="{{ parts[1] }}">
    <img class="publication-figure-image" src="{{ parts[0] }}" alt="{{ parts[1] }}" width="900" height="900" loading="lazy">
  </button>
  <figcaption class="publication-figure-caption">{{ parts[1] }}</figcaption>
</figure>
{% endfor %}
</div>

## 파이프라인과 아키텍처 {#pipeline}

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp" data-lightbox-alt="FR-PatchCore style PCB registration and memory-bank pipeline" data-lightbox-caption="FR-PatchCore style PCB registration and memory-bank pipeline">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp" alt="FR-PatchCore style PCB registration and memory-bank pipeline" width="900" height="900" loading="lazy">
  </button>
  <figcaption>등록, feature encoding, coreset memory bank, kNN score 흐름을 PCB inspection 데이터에 맞춰 재구성한 파이프라인입니다.</figcaption>
</figure>

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig20_vit_model_overview.webp" data-lightbox-alt="ViT style PCB patch-token architecture" data-lightbox-caption="ViT style PCB patch-token architecture">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig20_vit_model_overview.webp" alt="ViT style PCB patch-token architecture" width="900" height="900" loading="lazy">
  </button>
  <figcaption>PCB ROI를 patch token으로 바꾸고, transformer encoder와 MLP head로 연결하는 논문형 아키텍처 그림입니다.</figcaption>
</figure>

## 결과표와 주장 경계 {#results}

공개 페이지의 표와 수치는 production acceptance가 아니라, 출판 패키지와 연구용 pilot evidence를 설명하기 위한 registry-backed 결과입니다. 실물 카메라 프레임 수신과 gold-label production 성능은 아직 별도 승인 전입니다.

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_table02_result_tables.webp" data-lightbox-alt="PCB result tables" data-lightbox-caption="PCB result tables">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_table02_result_tables.webp" alt="PCB result tables" width="900" height="900" loading="lazy">
  </button>
  <figcaption>FR-PatchCore/PatchCore-style table format을 유지하면서 PCB inspection 수치와 claim boundary를 분리한 결과표입니다.</figcaption>
</figure>

## 연결 경로 {#links}

- GitHub repository: <https://github.com/Dororok9061/PCB-Visual-Inspection-Studio>
- Camera validation report: <https://github.com/Dororok9061/PCB-Visual-Inspection-Studio/blob/main/docs/camera_validation_report.md>
- Public research portal: <https://dororok9061.github.io/projects/pcb-visual-inspection/research-portal/?fresh=20260810-main-republish#methodology>
- English version: [PCB Research Publication Workbench public mirror](/en/blog/2026/08/08/pcb-research-portal-public-mirror/?fresh=20260810-main-republish)
