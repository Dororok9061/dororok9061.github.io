---
layout: page
title: RF 계산기
description: dBm, reflection, quarter-wave, noise figure, microstrip, power split을 브라우저에서 다시 계산하는 학습 도구.
lang: ko
permalink: /tools/rf/
image: /assets/images/study/rf-rfdh/power-db/db-power-scale.svg
---

## 식을 먼저 확인하고 숫자를 넣는다

모든 계산은 브라우저 안에서만 실행된다. 입력값을 서버로 보내지 않는다. 결과는 공부와 초기 설계 비교용이며 simulation·제작·측정을 대신하지 않는다.

{% assign rf_tools = site.pages | where: 'layout', 'rf-calculator' | sort: 'tool_order' %}
<div class="track-card-grid">
{% for tool in rf_tools %}<article><div><p class="eyebrow">RF Calculator {{ tool.tool_order }}</p><h3><a href="{{ tool.url | relative_url }}">{{ tool.title }}</a></h3><p>{{ tool.description }}</p></div></article>{% endfor %}
</div>

## 공부글과 함께 보기

[RF·Microwave 공부 시작점]({{ '/blog/rf/start-here/' | relative_url }})에서 각 식의 가정, 자체 도식, 내 Cadence·FMCW 자료 연결을 함께 정리했다.
