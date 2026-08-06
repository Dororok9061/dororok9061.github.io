---
layout: page
title: 전공과목 포트폴리오
eyebrow: Electrical Engineering Coursework
lead: 학부 과제와 실습을 전공 분야별로 모으고, 직접 한 설계·실행·측정을 구분해 설명합니다.
description: VHDL, 전력, 제어, RF, 센서 분야의 전자전기공학 학부 과제 포트폴리오.
permalink: /coursework/
lang: ko
alternate_url: /en/coursework/
alternate_lang: en
---

과목을 큰 묶음 하나로 합치지 않고 각각 독립된 허브로 나눴다. 저장된 과제와 결과가 있는 과목은 그 화면과 계산에서 시작하고, 개념 순서를 다시 세운 과목은 실제 수업 주차처럼 쓰지 않았다. 임베디드시스템은 대학 수업 원본과 개인·연구 프로젝트를 섞지 않기 위해 각각의 기록으로 바로 이어진다.

<div class="course-hub-grid">
{% assign courses = site.data.coursework_courses | sort: 'order' %}
{% for course in courses %}
<article><a class="course-hub-card__media" href="{{ '/coursework/' | append: course.id | append: '/' | relative_url }}"><img src="{{ course.thumbnail | relative_url }}" alt="{{ course.title_ko }} 대표 이미지" width="640" height="360" loading="lazy"></a><div><p class="post-card__meta">{% if course.units.size > 0 %}{{ course.units.size }}개 학습 단위{% else %}분리된 기록 3개{% endif %}</p><h2><a href="{{ '/coursework/' | append: course.id | append: '/' | relative_url }}">{{ course.title_ko }}</a></h2><p>{{ course.summary_ko }}</p></div></article>
{% endfor %}
</div>

## 별도 실습 트랙

PADS, STM32, mmWave는 과목 목록과 섞지 않고 실제 화면·보드·신호 자료를 중심으로 별도 하위 페이지를 만들었다.

- [PADS · PCB 설계](/study/pads/)
- [STM32 · Embedded](/study/stm32/)
- [mmWave · FMCW Radar](/study/mmwave/)

[전공 프로젝트 페이지](/projects/coursework/)와 [공개 coursework 저장소](https://github.com/Dororok9061/electrical-engineering-coursework-portfolio)도 함께 볼 수 있다.
