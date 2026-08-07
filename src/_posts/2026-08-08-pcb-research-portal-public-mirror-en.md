---
title: PCB Research Publication Workbench public mirror
title_en: PCB Research Publication Workbench public mirror
description: The PCB inspection figure atlas and lightbox flow verified on the local 8765 portal are now linked from GitHub Pages, the project hub, and the blog.
date: 2026-08-07 23:56:00 +0900
updated: 2026-08-07 23:56:00 +0900
study_date: 2026-08-07
lang: en
translation_key: pcb-research-portal-public-mirror
permalink: /en/blog/2026/08/08/pcb-research-portal-public-mirror/
alternate_url: /blog/2026/08/08/pcb-research-portal-public-mirror/
alternate_lang: ko
primary_category: research-project-log
subcategory: project-log
series: engineering-record-provenance
series_order: 3
post_type: project-log
difficulty: intermediate
study_status: published
evidence_status: SOURCE_AVAILABLE
tools: [Jekyll, GitHub Pages, Material Icons, PaperBanana]
hardware: [STM32F411, camera]
software_versions: []
source_materials:
  - { title: PCB Research Publication Workbench, type: public-page, public_url: /projects/pcb-visual-inspection/research-portal/?fresh=20260808-public-mirror-v1#methodology, file_reference: src/projects/pcb-visual-inspection/research-portal, pages: "", used_for: public mirror }
  - { title: PCB Visual Inspection Studio project page, type: project-page, public_url: /en/projects/pcb-visual-inspection/, file_reference: src/en/projects/pcb-visual-inspection/index.md, pages: "", used_for: project hub link }
prerequisites: [PCB inspection, figure provenance, GitHub Pages]
learning_objectives: [sync local portal and public site, link individual figure atlas, verify click-to-enlarge publication flow]
related_projects: [pcb-visual-inspection]
related_posts: [evidence-status]
tags: [pcb-inspection, github-pages, paperbanana, figure-atlas, lightbox]
cover_image: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp
thumbnail: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp
image_alt: PCB capture, ROI, and quality gate arranged as a separated paper figure card
draft: false
published: true
revision_history:
  - { date: 2026-08-07, change: Mirrored the local 8765 portal into a public GitHub Pages route }
toc:
  - { id: mirror, title: Public mirror route }
  - { id: figures, title: Figure structure }
  - { id: boundary, title: Validation boundary }
---

## Public mirror route {#mirror}

The `127.0.0.1:8765` portal that was checked locally is now mirrored into the static GitHub Pages source.

[Open the full Research Publication Workbench](/projects/pcb-visual-inspection/research-portal/?fresh=20260808-public-mirror-v1#methodology)

The route includes `index.html`, `portal-data.js`, `style.css`, `script.js`, and the optimized `AssetsWeb` directory. It is no longer only a compact project-gallery summary; the full figure/table atlas is available as a standalone workbench.

## Figure structure {#figures}

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp" data-lightbox-alt="PCB capture and quality gate figure" data-lightbox-caption="fig31a. capture and quality gate">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp" alt="PCB capture and quality gate figure" width="900" height="900" loading="lazy">
  </button>
  <figcaption>Separated figure cards stay independent from contact sheets and open in the site lightbox.</figcaption>
</figure>

The portal contains PCB inspection assets from `fig01` through `fig44`, tables from `table01` through `table09`, and the separated `fig31a` through `fig31j` methodology cards. The project page keeps the compact gallery while the full Workbench carries the detailed publication view.

## Validation boundary {#boundary}

The public page documents the paper-style figure structure, label alignment, separated cards, and lightbox behavior. It does not make production-yield, manufacturing-defect, or gold-label quantitative claims beyond the evidence stated in the project boundary.
