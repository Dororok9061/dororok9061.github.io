---
layout: default
title: Portfolio Source Collection Map
seo_title: Portfolio Source Collection Map | Hyeongrok Ryu
description: Source map connecting the uploaded semiconductor, defense, and undergraduate coursework archives to project, coursework, and study pages
lang: en
permalink: /en/source-collections/
alternate_url: /source-collections/
alternate_lang: ko
---
<main id="main" class="page page-shell source-collection-page">
  <header class="page-heading">
    <p class="eyebrow">Source Collection Map</p>
    <h1>How the uploaded coursework and project archives are used</h1>
    <p class="page-heading__lead">The archives are not published as raw ZIP files. Reports, source code, calculators, and simulation screens are mapped to the relevant project, coursework, and study pages.</p>
  </header>
  <nav class="research-jump-nav" aria-label="Source collection navigation">
    <span class="research-jump-nav__label">Collections</span>
    <div class="research-jump-nav__links">
      {% for collection in site.data.source_collections %}<a href="#{{ collection.id }}">{{ collection.title_en }}</a>{% endfor %}
    </div>
  </nav>
  {% for collection in site.data.source_collections %}
  <section id="{{ collection.id }}" class="source-collection-card research-section">
    <div class="source-collection-card__heading">
      <div>
        <p class="eyebrow">{{ collection.source_file }}</p>
        <h2>{{ collection.title_en }}</h2>
        <p>{{ collection.summary_en }}</p>
      </div>
      <div class="source-collection-card__count"><strong>{{ collection.item_count }}</strong><span>files / items</span></div>
    </div>
    <div class="source-stat-grid">
      {% for stat in collection.stats %}<article><strong>{{ stat.value }}</strong><span>{{ stat.label }}</span></article>{% endfor %}
    </div>
    {% if collection.topics %}
    <h3>Topics mapped to public pages</h3>
    <ul class="source-topic-list">{% for topic in collection.topics %}<li>{{ topic }}</li>{% endfor %}</ul>
    {% endif %}
    {% if collection.topic_groups %}
    <h3>Course and project groups</h3>
    <div class="source-topic-grid">{% for group in collection.topic_groups %}<article><strong>{{ group.title_en }}</strong><span>{{ group.item_count }} items</span></article>{% endfor %}</div>
    {% endif %}
    <div class="paper-case-card__links">
      {% for destination in collection.destinations %}<a href="{% if destination == '/defense/' %}{{ '/en/defense/' | relative_url }}{% elsif destination == '/coursework/' %}{{ '/en/coursework/' | relative_url }}{% elsif destination contains '/projects/' %}{{ '/en' | append: destination | relative_url }}{% else %}{{ destination | relative_url }}{% endif %}">Open related page</a>{% endfor %}
    </div>
  </section>
  {% endfor %}
  <section class="paper-section paper-section--tinted">
    <p class="eyebrow">Publication rule</p>
    <h2>How source material is published</h2>
    <p>User-authored code, reports, calculations, and figures are used on the relevant pages. Course handouts, company-analysis books, certificates, licenses, and source material with unclear redistribution rights are retained for review and attribution rather than uploaded unchanged.</p>
  </section>
</main>
