---
layout: default
title: 포트폴리오 원본 자료 지도
seo_title: 포트폴리오 원본 자료 지도 | 류형록
description: 반도체 회로설계, 방산, 학부 과제·프로젝트 압축자료를 프로젝트·전공과제·블로그 페이지에 연결한 Source Collection Map
lang: ko
permalink: /source-collections/
alternate_url: /en/source-collections/
alternate_lang: en
---
<main id="main" class="page page-shell source-collection-page">
  <header class="page-heading">
    <p class="eyebrow">Source Collection Map</p>
    <h1>업로드한 과제·프로젝트 자료를 어디에 반영하는지</h1>
    <p class="page-heading__lead">압축파일을 통째로 공개하지 않고, 내부 보고서·코드·계산기·시뮬레이션 화면을 해당 프로젝트와 공부글에 연결합니다.</p>
  </header>
  <nav class="research-jump-nav" aria-label="자료 묶음 이동">
    <span class="research-jump-nav__label">바로가기</span>
    <div class="research-jump-nav__links">
      {% for collection in site.data.source_collections %}<a href="#{{ collection.id }}">{{ collection.title_ko }}</a>{% endfor %}
    </div>
  </nav>
  {% for collection in site.data.source_collections %}
  <section id="{{ collection.id }}" class="source-collection-card research-section">
    <div class="source-collection-card__heading">
      <div>
        <p class="eyebrow">{{ collection.source_file }}</p>
        <h2>{{ collection.title_ko }}</h2>
        <p>{{ collection.summary_ko }}</p>
      </div>
      <div class="source-collection-card__count"><strong>{{ collection.item_count }}</strong><span>파일·항목</span></div>
    </div>
    <div class="source-stat-grid">
      {% for stat in collection.stats %}<article><strong>{{ stat.value }}</strong><span>{{ stat.label }}</span></article>{% endfor %}
    </div>
    {% if collection.topics %}
    <h3>페이지에 반영할 핵심 주제</h3>
    <ul class="source-topic-list">{% for topic in collection.topics %}<li>{{ topic }}</li>{% endfor %}</ul>
    {% endif %}
    {% if collection.topic_groups %}
    <h3>과목·프로젝트별 자료량</h3>
    <div class="source-topic-grid">{% for group in collection.topic_groups %}<article><strong>{{ group.title_ko }}</strong><span>{{ group.item_count }}개 항목</span></article>{% endfor %}</div>
    {% endif %}
    <div class="paper-case-card__links">
      {% for destination in collection.destinations %}<a href="{{ destination | relative_url }}">관련 페이지 열기</a>{% endfor %}
    </div>
  </section>
  {% endfor %}
  <section class="paper-section paper-section--tinted">
    <p class="eyebrow">Publication rule</p>
    <h2>공개 방식</h2>
    <p>사용자가 작성한 코드·보고서·계산 결과와 직접 생성한 그림은 관련 페이지에 사용합니다. 강의교안, 기업분석집, 수료증, 라이선스와 재배포권이 불명확한 원문은 공개 저장소에 그대로 올리지 않고 내용 확인과 출처 대조에만 사용합니다.</p>
  </section>
</main>
