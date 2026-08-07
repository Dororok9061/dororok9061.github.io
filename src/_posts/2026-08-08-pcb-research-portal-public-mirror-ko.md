---
title: PCB Research Publication Workbench 공개 미러 반영
title_en: PCB Research Publication Workbench public mirror
description: 로컬 8765 포털에서 검증한 PCB inspection figure atlas와 lightbox 구성을 GitHub Pages 블로그와 프로젝트 허브에 연결했습니다.
date: 2026-08-07 23:55:00 +0900
updated: 2026-08-07 23:55:00 +0900
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
tools: [Jekyll, GitHub Pages, Material Icons, PaperBanana]
hardware: [STM32F411, camera]
software_versions: []
source_materials:
  - { title: PCB Research Publication Workbench, type: public-page, public_url: /projects/pcb-visual-inspection/research-portal/?fresh=20260808-public-mirror-v1#methodology, file_reference: src/projects/pcb-visual-inspection/research-portal, pages: "", used_for: public mirror }
  - { title: PCB Visual Inspection Studio project page, type: project-page, public_url: /projects/pcb-visual-inspection/, file_reference: src/projects/pcb-visual-inspection/index.md, pages: "", used_for: project hub link }
prerequisites: [PCB inspection, figure source mapping, GitHub Pages]
learning_objectives: [로컬 포털과 공개 사이트 동기화, 낱장 figure atlas 연결, click-to-enlarge 공개 검증]
related_projects: [pcb-visual-inspection]
related_posts: [evidence-status]
tags: [pcb-inspection, github-pages, paperbanana, figure-atlas, lightbox]
cover_image: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp
thumbnail: /projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp
image_alt: PCB capture, ROI, quality gate를 분리형 논문 figure 카드로 정리한 그림
draft: false
published: true
revision_history:
  - { date: 2026-08-07, change: 로컬 8765 포털을 GitHub Pages 공개 경로로 미러 }
toc:
  - { id: mirror, title: 공개 미러 경로 }
  - { id: hub, title: 허브 연결 }
  - { id: assets, title: 에셋 처리 }
  - { id: figures, title: 그림 구조 }
  - { id: boundary, title: 검증 범위 }
---

## 공개 미러 경로 {#mirror}

로컬에서 확인하던 `127.0.0.1:8765` 포털을 GitHub Pages 안의 정적 경로로 미러했습니다.

[전체 Research Publication Workbench 열기](/projects/pcb-visual-inspection/research-portal/?fresh=20260808-public-mirror-v1#methodology)

이 경로에는 `index.html`, `portal-data.js`, `style.css`, `script.js`, 그리고 최적화된 `AssetsWeb` 폴더가 함께 들어갑니다. 따라서 프로젝트 요약 페이지의 10장 갤러리만 보는 것이 아니라, PaperBanana reference-intake 방식으로 정리한 전체 figure/table atlas를 한 페이지에서 볼 수 있습니다.

## 허브 연결 {#hub}

PCB 프로젝트 페이지, repository README, KO/EN 프로젝트 메타데이터가 모두 같은 공개 Workbench 경로를 가리키도록 맞췄습니다. 그래서 로컬 8765 미리보기와 공개 GitHub Pages 사이에 내용 차이가 남지 않도록 연결했습니다.

## 에셋 처리 {#assets}

원본 고해상도 캡처는 로컬 프로젝트 기록 안에 그대로 두고, 공개 페이지에서는 최적화된 `AssetsWeb` 파일만 사용합니다. 큰 contact sheet를 독자용 기본 경로로 쓰지 않고, 개별 figure card를 하나씩 분리해 lightbox에서 각 PCB inspection diagram을 확대할 수 있게 했습니다.

## 그림 구조 {#figures}

<figure>
  <button type="button" data-lightbox="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp" data-lightbox-alt="PCB capture and quality gate figure" data-lightbox-caption="fig31a. capture and quality gate">
    <img src="/projects/pcb-visual-inspection/research-portal/AssetsWeb/paper_style/pcb_style_fig31a_capture_quality_gate.webp" alt="PCB capture and quality gate figure" width="900" height="900" loading="lazy">
  </button>
  <figcaption>분리형 figure card는 contact sheet로 뭉치지 않고, 클릭하면 lightbox에서 확대됩니다.</figcaption>
</figure>

포털에는 `fig01`부터 `fig44`, `table01`부터 `table09`, 그리고 `fig31a`부터 `fig31j`까지의 PCB inspection용 그림과 표 자산이 들어갑니다. 프로젝트 페이지에는 요약 gallery를 남기고, 상세 검토는 전체 Workbench 링크로 연결했습니다.

## 검증 범위 {#boundary}

공개 페이지는 논문형 그림 구조, label 정렬, figure card 분리, lightbox 동작을 보여주는 출판 허브입니다. 생산 수율, 제조 결함 판정, gold-label 기반 정량 성능은 데이터셋 공개 승인 이후 결과 요약에 반영합니다.
