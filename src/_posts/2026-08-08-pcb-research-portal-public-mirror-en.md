---
title: PCB Research Publication Workbench public mirror
title_en: PCB Research Publication Workbench public mirror
description: The PCB inspection figure atlas and lightbox flow verified on the local 8765 portal are now reflected in the GitHub Pages blog and project hub.
date: 2026-08-07 23:56:00 +0900
updated: 2026-08-10 00:00:00 +0900
study_date: 2026-08-07
lang: en
translation_key: pcb-research-portal-public-mirror
permalink: /en/blog/2026/08/08/pcb-research-portal-public-mirror/
alternate_url: /blog/2026/08/08/pcb-research-portal-public-mirror/
alternate_lang: ko
primary_category: research-project-log
subcategory: project-log
series: engineering-record-lineage
series_order: 3
post_type: project-log
difficulty: intermediate
study_status: published
evidence_status: SOURCE_AVAILABLE
tools: [Jekyll, GitHub Pages, Material Icons, PaperBanana]
hardware: [STM32F411, camera]
software_versions: []
source_materials:
  - { title: PCB Research Publication Workbench, type: public-page, public_url: /projects/pcb-visual-inspection/research-portal/?fresh=20260810-main-republish#methodology, file_reference: src/projects/pcb-visual-inspection/research-portal, pages: "", used_for: public mirror }
  - { title: PCB Visual Inspection Studio repository paper package, type: github-repository, public_url: https://github.com/Dororok9061/PCB-Visual-Inspection-Studio/tree/main/docs/paper, file_reference: docs/paper, pages: "", used_for: paper package }
prerequisites: [PCB inspection, figure source mapping, GitHub Pages]
learning_objectives: [sync local portal and public site, publish individual figure atlas, verify click-to-enlarge review flow]
related_projects: [pcb-visual-inspection]
related_posts: [evidence-status]
tags: [pcb-inspection, github-pages, paperbanana, figure-atlas, lightbox]
cover_image: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp
thumbnail: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp
image_alt: PCB inspection pipeline and paper-style figure atlas
draft: false
published: true
revision_history:
  - date: 2026-08-07
    change: Mirrored the local portal into a public GitHub Pages route
  - date: 2026-08-10
    change: Added primary pipeline and architecture figures to the blog article
toc:
  - { id: mirror, title: Public mirror route }
  - { id: key-figures, title: Key figures }
  - { id: pipeline, title: Pipeline and architecture }
  - { id: results, title: Tables and claim boundary }
  - { id: links, title: Links }
---

## Public mirror route {#mirror}

The PCB inspection publication workbench that was checked on `127.0.0.1:8765` is now connected to the public GitHub Pages route again.

[Open the full Research Publication Workbench](/projects/pcb-visual-inspection/research-portal/?fresh=20260810-main-republish#methodology)

The important change is that readers do not have to inspect one bundled contact sheet. The blog now exposes primary paper figures directly, while each card remains clickable through the site lightbox.

## Key figures {#key-figures}

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

## Pipeline and architecture {#pipeline}

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp" data-lightbox-alt="FR-PatchCore style PCB registration and memory-bank pipeline" data-lightbox-caption="FR-PatchCore style PCB registration and memory-bank pipeline">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig09_frpatchcore_pipeline.webp" alt="FR-PatchCore style PCB registration and memory-bank pipeline" width="900" height="900" loading="lazy">
  </button>
  <figcaption>The pipeline reconstructs registration, feature encoding, coreset memory bank, and kNN scoring for the PCB inspection setting.</figcaption>
</figure>

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig20_vit_model_overview.webp" data-lightbox-alt="ViT style PCB patch-token architecture" data-lightbox-caption="ViT style PCB patch-token architecture">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig20_vit_model_overview.webp" alt="ViT style PCB patch-token architecture" width="900" height="900" loading="lazy">
  </button>
  <figcaption>The architecture figure shows a PCB ROI converted into patch tokens and routed through a transformer encoder plus MLP head.</figcaption>
</figure>

## Tables and claim boundary {#results}

The public tables are registry-backed publication artifacts and research pilot evidence. They are not production acceptance claims. Live camera frame acquisition and gold-label production metrics remain gated until the supporting dataset is approved.

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_table02_result_tables.webp" data-lightbox-alt="PCB result tables" data-lightbox-caption="PCB result tables">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_table02_result_tables.webp" alt="PCB result tables" width="900" height="900" loading="lazy">
  </button>
  <figcaption>The result table keeps the FR-PatchCore/PatchCore-style table layout while separating PCB inspection values from claim boundaries.</figcaption>
</figure>

## Links {#links}

- GitHub repository: <https://github.com/Dororok9061/PCB-Visual-Inspection-Studio>
- Camera validation report: <https://github.com/Dororok9061/PCB-Visual-Inspection-Studio/blob/main/docs/camera_validation_report.md>
- Public research portal: <https://dororok9061.github.io/projects/pcb-visual-inspection/research-portal/?fresh=20260810-main-republish#methodology>
- Korean version: [PCB Research Publication Workbench 공개 미러](/blog/2026/08/08/pcb-research-portal-public-mirror/?fresh=20260810-main-republish)
