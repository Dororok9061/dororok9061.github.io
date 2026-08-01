---
title: PADS의 SOIC Footprint와 PPG 회로를 별도 사례로 다시 읽기
title_en: Reading an SOIC Footprint and a PPG Schematic as Separate PADS Examples
description: 6-pin SOIC decal 치수와 OPA2333·filter·logic PPG 화면을 서로 다른 PADS 학습 사례로 정리한 기록.
date: 2026-08-01 11:03:00 +0900
updated: 2026-08-01 11:03:00 +0900
study_date: 2026-02-12
lang: ko
translation_key: pads-footprint-ppg-schematic
permalink: /blog/2026/08/01/pads-footprint-ppg-schematic/
alternate_url: /en/blog/2026/08/01/pads-footprint-ppg-schematic/
alternate_lang: en
primary_category: pcb-pads
subcategory: decal-footprint
series: pads-pcb-design
series_order: 3
post_type: study-note
practical: true
difficulty: intermediate
study_status: published
evidence_status: ARCHIVED_DESIGN_SCREENSHOTS
tools: [PADS Logic, PADS Layout]
hardware: []
software_versions: []
source_materials:
  - { title: PADS footprint and PPG design screenshots, type: local-coursework, public_url: "", file_reference: 2026 PADS screenshots, pages: "", used_for: two separate examples of decal dimensions and schematic-to-layout flow }
prerequisites: [electronic-circuits, pcb-basics]
learning_objectives: [decal dimensions, pin numbering, schematic and layout connectivity, unrelated captures 구분]
related_projects: [ppg-hrv]
related_posts: [biomedical-metric-conditions]
tags: [pads, pcb-footprint, ppg, opa2333]
cover_image: /assets/images/study/pads/pads-ppg-layout.webp
thumbnail: /assets/images/study/pads/pads-ppg-layout.webp
image_alt: PADS Logic의 PPG 회로도와 Layout의 초기 부품 배치 화면
draft: false
revision_history:
  - { date: 2026-08-01, change: 저장된 Decal Wizard와 PPG 회로 화면을 바탕으로 작성 }
toc:
  - { id: start, title: 두 화면을 분리해서 본 이유 }
  - { id: footprint, title: 6-pin SOIC 치수 }
  - { id: numbering, title: Pin 번호와 방향 }
  - { id: schematic, title: PPG signal chain }
  - { id: layout, title: Layout 화면에서 본 것 }
  - { id: next, title: 다음에 확인할 순서 }
  - { id: navigation, title: 이전 글과 다음 글 }
---

## 두 화면을 분리해서 본 이유 {#start}

PADS를 처음 배울 때 저장한 Decal Wizard 화면과 PPG schematic·layout 화면을 다시 펼쳐 봤다. 두 화면은 같은 폴더에 남아 있지만, 6-pin SOIC decal이 PPG 설계에 사용됐다고 확인할 연결 정보는 없었다. 그래서 하나의 부품 흐름으로 합치지 않고 footprint 입력과 schematic-to-layout 읽기를 서로 다른 사례로 나란히 정리했다.

<figure>
  <img src="{{ '/assets/images/learning/coursework/pads-footprint-ppg-schematic.svg' | relative_url }}" alt="서로 독립된 사례로 배치한 여섯 pad SOIC decal과 OPA2333, filter, SN74LVC logic PPG 화면" width="1200" height="630">
  <figcaption>왼쪽과 오른쪽은 별도 저장 화면에서 읽은 두 학습 사례다. 두 artifact가 같은 package를 공유한다고 뜻하지 않는다.</figcaption>
</figure>

## 6-pin SOIC 치수 {#footprint}

Decal Wizard 화면에서 pin count를 6으로 두고 SMD pad 폭 0.6 mm, 길이 1.05 mm를 입력했다. 같은 줄의 pin pitch는 1.27 mm, 양쪽 row 중심 간격은 2.65 mm였다. 처음에는 lead span과 row pitch를 같은 값으로 읽었는데, pad 중심을 기준으로 다시 보니 서로 다른 치수였다.

<figure><img src="{{ '/assets/images/study/pads/pads-soic-decal-a.webp' | relative_url }}" alt="6-pin SOIC 치수를 입력한 PADS Decal Wizard 작업 화면" width="1024" height="704"><figcaption>내가 저장한 Decal Wizard 화면을 메타데이터 없이 WebP로 변환했다.</figcaption></figure>

<figure>
  <table>
    <thead><tr><th>항목</th><th>입력값</th><th>내가 확인한 기준</th></tr></thead>
    <tbody>
      <tr><td>Pin count</td><td>6</td><td>양쪽에 3개씩</td></tr>
      <tr><td>Pad width</td><td>0.6 mm</td><td>Pad의 짧은 변</td></tr>
      <tr><td>Pad length</td><td>1.05 mm</td><td>Body 바깥 방향</td></tr>
      <tr><td>Pin pitch</td><td>1.27 mm</td><td>같은 row의 pad 간격</td></tr>
      <tr><td>Row pitch</td><td>2.65 mm</td><td>좌우 row 중심 간격</td></tr>
    </tbody>
  </table>
  <figcaption>숫자를 package drawing의 어느 선에 대응시키는지 함께 적어두니 입력 실수를 줄이기 쉬웠다.</figcaption>
</figure>

## Pin 번호와 방향 {#numbering}

저장된 화면은 counter-clockwise 번호 방향과 pin 1 표시를 사용했다. 나는 footprint를 만든 뒤 schematic symbol의 1번 pin, 전원 pin, 출력 pin이 같은 번호로 이어지는지 먼저 확인해야 한다고 정리했다. 모양이 맞아도 pin mapping이 틀리면 netlist가 다른 회로를 만들기 때문이다.

## PPG signal chain {#schematic}

별도의 PPG schematic 화면에는 OPA2333 증폭 단계와 RC filtering, 뒤쪽의 SN74LVC 계열 logic이 함께 보였다. 아날로그 입력을 바로 logic으로 보내는 구조가 아니라, 작은 신호를 증폭하고 대역을 제한한 다음 다음 단계로 넘기는 흐름이었다. 이 화면에 보이는 OPA2333 package를 앞의 6-pin SOIC decal과 같은 부품이라고 보지는 않았다.

<figure><img src="{{ '/assets/images/study/pads/pads-ppg-layout.webp' | relative_url }}" alt="OPA2333 증폭단과 SN74LVC logic, 초기 PADS Layout 배치가 함께 보이는 작업 화면" width="1904" height="1018"><figcaption>회로도와 초기 배치를 함께 저장한 실제 PADS 화면이다.</figcaption></figure>

<figure>
  <pre><code>PPG input
  → OPA2333 amplification
  → RC filtering and gain
  → OPA2333 output stage
  → SN74LVC logic interface
  → PPG capture의 placement view</code></pre>
  <figcaption>저장된 화면에서 보이는 기능 블록만 연결했다. 부품값이나 cutoff frequency를 새로 추정하지 않았다.</figcaption>
</figure>

## Layout 화면에서 본 것 {#layout}

같은 캡처에 PADS Logic schematic과 PADS Layout 배치 화면이 함께 있었다. 이 화면은 부품과 연결선이 layout으로 넘어간 설계 과정을 보여준다. 하지만 화면 한 장만으로 fabrication, DRC 완료, 실제 PPG 측정을 말할 수는 없다.

## 다음에 확인할 순서 {#next}

다음에는 6-pin 부품의 실제 package drawing을 찾아 decal의 pin 1, pad 크기, courtyard를 따로 확인할 생각이다. PPG 설계에서는 사용된 각 part와 footprint 연결표를 먼저 확보한 뒤 schematic-to-layout packaging, net 이름과 unrouted connection을 본다. 그 연결표가 생기기 전에는 두 저장 화면을 같은 artifact로 묶지 않는다.

## 이전 글과 다음 글 {#navigation}

- [이전: 전공과목 전체 보기]({{ '/coursework/' | relative_url }})
- [시리즈: PADS PCB 설계]({{ '/blog/series/pads-pcb-design/' | relative_url }})
- [다음: PPG-HRV 프로젝트]({{ '/projects/ppg-hrv/' | relative_url }})
