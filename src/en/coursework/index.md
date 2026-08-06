---
layout: page
title: Coursework Portfolio
eyebrow: Electrical Engineering Coursework
lead: Undergraduate assignments and laboratories organized by domain, with design, execution, and measurement described separately.
description: Electrical engineering coursework across VHDL, power, control, RF, and sensors.
permalink: /en/coursework/
lang: en
alternate_url: /coursework/
alternate_lang: ko
---

I separated every subject into its own hub instead of folding them into one large field. Subjects with saved assignments and results begin from those visuals and calculations; concept sequences are not presented as the original classroom calendar. Embedded Systems links to separate university, personal, and research records so their boards and results are not mixed together.

<div class="course-hub-grid">
{% assign courses = site.data.coursework_courses | sort: 'order' %}
{% for course in courses %}
<article><a class="course-hub-card__media" href="{{ '/en/coursework/' | append: course.id | append: '/' | relative_url }}"><img src="{{ course.thumbnail | relative_url }}" alt="{{ course.title_en }} course visual" width="640" height="360" loading="lazy"></a><div><p class="post-card__meta">{% if course.units.size > 0 %}{{ course.units.size }} study units{% else %}3 separate records{% endif %}</p><h2><a href="{{ '/en/coursework/' | append: course.id | append: '/' | relative_url }}">{{ course.title_en }}</a></h2><p>{{ course.summary_en }}</p></div></article>
{% endfor %}
</div>

## Separate lab tracks

PADS, STM32, and mmWave remain separate from the course list, with child pages centered on real screens, boards, and signals.

- [PADS · PCB Design](/en/study/pads/)
- [STM32 · Embedded](/en/study/stm32/)
- [mmWave · FMCW Radar](/en/study/mmwave/)

The [coursework project page](/en/projects/coursework/) and [public coursework repository](https://github.com/Dororok9061/electrical-engineering-coursework-portfolio) remain connected.
