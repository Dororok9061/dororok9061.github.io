---
layout: default
title: ViScan 스마트미러
description: Radar·Vision AI·Sensor Fusion·초음파 측정을 통합한 ViScan과 CES 2027 제출·국내 특허출원 현황.
permalink: /projects/viscan/
lang: ko
alternate_url: /en/projects/viscan/
alternate_lang: en
---

<main id="main" class="page page-shell research-case-page">
  <nav class="breadcrumbs" aria-label="현재 위치"><a href="/">홈</a><span aria-hidden="true">/</span><a href="/projects/">프로젝트</a></nav>

  <header id="overview" class="project-heading research-section">
    <div>
      <p class="eyebrow">Radar · Vision AI · Sensor Fusion · Digital Health</p>
      <h1>ViScan 스마트미러</h1>
      <p class="page-heading__lead">Radar Presence부터 Face Session, AR Guide, 초음파 측정, rPPG와 Report까지 하나의 상태 기반 파이프라인으로 통합한 스마트미러 프로젝트입니다.</p>
      <div class="research-resource-strip" aria-label="프로젝트 현황">
        <span>CES 2027 Innovation Awards 제출 완료</span>
        <span>국내 특허 출원 완료</span>
        <span>CES 2027 부스 운영·시연 예정</span>
      </div>
    </div>
    <div class="project-heading__diagram" role="img" aria-label="ViScan 처리 흐름">
      <span>Radar Presence</span><span>Vision AI · Sensor Fusion</span><span>Ultrasound · Report</span>
    </div>
  </header>

  <nav class="research-jump-nav" aria-label="이 페이지">
    <span class="research-jump-nav__label">이 페이지</span>
    <div class="research-jump-nav__links">
      <a href="#problem">문제 정의</a><a href="#architecture">구조</a><a href="#methodology">구현</a><a href="#results">성과</a><a href="#patent">특허</a>
    </div>
  </nav>

  <div class="project-narrative">
    <section id="problem" class="research-section">
      <p class="eyebrow">01</p><h2>문제 정의</h2>
      <p>카메라·FMCW Radar·초음파·rPPG처럼 갱신주기와 실패 양상이 다른 모듈을 단순히 연결하면 오래된 Frame, 저조도, 다중인원, Radar 타깃 모호성이나 Calibration 불일치가 다음 측정 단계로 전파될 수 있습니다. ViScan은 각 센서의 책임과 다음 상태로 넘어갈 조건을 먼저 정의하는 방식으로 설계했습니다.</p>
    </section>
    <section id="architecture" class="research-section">
      <p class="eyebrow">02</p><h2>시스템 구조</h2>
      <p>Radar Presence → Face Session → AR Guide → Ultrasound Measurement → rPPG → Report → Session Reset 순서로 동작합니다. BGT60TR13C는 존재·거리·안정도 정보를 제공하고, 카메라는 얼굴 세션·Pose·노출·가림·다중인원 상태를 판단합니다.</p>
    </section>
    <section id="methodology" class="research-section">
      <p class="eyebrow">03</p><h2>내가 구현한 부분</h2>
      <ul>
        <li>C# WPF와 Python 기반 상태 파이프라인 통합</li>
        <li>YuNet·SFace 기반 얼굴 세션과 MediaPipe Pose 기반 복부 AR Guide</li>
        <li>저조도·저프레임률·가림·다중인원·오래된 Frame 판정</li>
        <li>BGT60TR13C 존재·거리 정보와 Camera 판단을 결합한 Sensor Fusion</li>
        <li>Timestamp·Projection·Calibration 불일치 시 측정을 중지하는 Fail-safe 조건</li>
      </ul>
    </section>
    <section id="results" class="research-section">
      <p class="eyebrow">04</p><h2>현재 공개 가능한 성과</h2>
      <ul>
        <li>CES 2027 Innovation Awards 신청·제출 완료</li>
        <li>CES 2027 ViScan 부스 운영 및 제품 시연 예정</li>
        <li>통합시험에서 Radar 20.017 Hz, Camera 14.696 fps, Pose 14.650 Hz 기록</li>
        <li>기술보고서·발표자료·기업 미팅·선행특허 조사와 사업화 전략 수행</li>
      </ul>
    </section>
  </div>

  <figure class="research-flow-figure" aria-labelledby="viscan-flow-caption">
    <div class="research-flow-figure__grid">
      <div class="research-flow-step"><span class="research-flow-step__index">01</span><strong>Presence</strong><p>BGT60TR13C 존재·거리·안정도</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">02</span><strong>Session</strong><p>YuNet·SFace 얼굴 세션</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">03</span><strong>Guidance</strong><p>MediaPipe Pose와 Camera–Radar Fusion</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">04</span><strong>Measurement</strong><p>초음파·rPPG·Report·Reset</p></div>
    </div>
    <figcaption id="viscan-flow-caption">ViScan의 공개 가능한 상태 기반 처리 흐름입니다.</figcaption>
  </figure>

  <section id="patent" class="research-section boundary-panel">
    <h2>국내 특허 출원</h2>
    <dl class="profile-facts">
      <div><dt>발명의 명칭</dt><dd>초음파 기반 스마트미러 체성분 분석 시스템</dd></div>
      <div><dt>출원번호</dt><dd><strong>10-2026-0154726</strong></dd></div>
      <div><dt>출원일</dt><dd>2026년 8월 18일</dd></div>
      <div><dt>출원인</dt><dd>단국대학교 천안캠퍼스 산학협력단·주식회사 한소노 공동출원</dd></div>
      <div><dt>역할</dt><dd>공동발명자</dd></div>
      <div><dt>법적 상태</dt><dd>특허출원 완료. 등록 특허 또는 권리 확정 상태를 의미하지 않습니다.</dd></div>
    </dl>
  </section>
</main>
