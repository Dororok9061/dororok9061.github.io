---
layout: default
title: ViScan Smart Mirror
description: ViScan integrates radar, vision AI, sensor fusion, ultrasound measurement, with CES 2027 submission and Korean patent-application milestones.
permalink: /en/projects/viscan/
lang: en
alternate_url: /projects/viscan/
alternate_lang: ko
---

<main id="main" class="page page-shell research-case-page">
  <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/en/">Home</a><span aria-hidden="true">/</span><a href="/en/projects/">Projects</a></nav>

  <header id="overview" class="project-heading research-section">
    <div>
      <p class="eyebrow">Radar · Vision AI · Sensor Fusion · Digital Health</p>
      <h1>ViScan Smart Mirror</h1>
      <p class="page-heading__lead">A state-driven smart-mirror system that connects Radar Presence, Face Session, AR Guide, ultrasound measurement, rPPG, and report delivery.</p>
      <div class="research-resource-strip" aria-label="Project milestones">
        <span>CES 2027 Innovation Awards application submitted</span>
        <span>Korean patent application filed</span>
        <span>CES 2027 booth operation and demonstration planned</span>
      </div>
    </div>
    <div class="project-heading__diagram" role="img" aria-label="ViScan processing flow">
      <span>Radar Presence</span><span>Vision AI · Sensor Fusion</span><span>Ultrasound · Report</span>
    </div>
  </header>

  <nav class="research-jump-nav" aria-label="On this page">
    <span class="research-jump-nav__label">On this page</span>
    <div class="research-jump-nav__links">
      <a href="#problem">Problem</a><a href="#architecture">Architecture</a><a href="#methodology">Implementation</a><a href="#results">Milestones</a><a href="#patent">Patent filing</a>
    </div>
  </nav>

  <div class="project-narrative">
    <section id="problem" class="research-section">
      <p class="eyebrow">01</p><h2>Problem</h2>
      <p>Camera, FMCW radar, ultrasound, and rPPG modules have different update rates and failure modes. Without explicit gates, stale frames, low light, multiple people, ambiguous radar targets, or calibration mismatch can propagate into the next measurement stage. ViScan therefore defines sensor responsibilities and state-transition conditions before combining outputs.</p>
    </section>
    <section id="architecture" class="research-section">
      <p class="eyebrow">02</p><h2>Architecture</h2>
      <p>The public system flow is Radar Presence → Face Session → AR Guide → Ultrasound Measurement → rPPG → Report → Session Reset. The BGT60TR13C supplies presence, distance, and stability information, while the camera handles face sessions, pose, exposure, occlusion, and multiple-person conditions.</p>
    </section>
    <section id="methodology" class="research-section">
      <p class="eyebrow">03</p><h2>My engineering contribution</h2>
      <ul>
        <li>C# WPF and Python integration for the state-driven sensing pipeline</li>
        <li>YuNet/SFace face-session handling and MediaPipe Pose abdominal AR guidance</li>
        <li>Low-light, low-frame-rate, occlusion, multiple-person, and stale-frame checks</li>
        <li>Sensor fusion between BGT60TR13C presence/distance data and camera-side decisions</li>
        <li>Fail-safe transitions for timestamp, projection, and calibration mismatches</li>
      </ul>
    </section>
    <section id="results" class="research-section">
      <p class="eyebrow">04</p><h2>Public milestones</h2>
      <ul>
        <li>CES 2027 Innovation Awards application submitted</li>
        <li>ViScan booth operation and live product demonstration planned for CES 2027</li>
        <li>Integrated test rates: radar 20.017 Hz, camera 14.696 fps, pose 14.650 Hz</li>
        <li>Technical reports, presentations, company meetings, prior-art review, and commercialization planning completed</li>
      </ul>
    </section>
  </div>

  <figure class="research-flow-figure" aria-labelledby="viscan-flow-caption">
    <div class="research-flow-figure__grid">
      <div class="research-flow-step"><span class="research-flow-step__index">01</span><strong>Presence</strong><p>BGT60TR13C presence, distance, and stability</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">02</span><strong>Session</strong><p>YuNet/SFace face session</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">03</span><strong>Guidance</strong><p>MediaPipe Pose and camera–radar fusion</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">04</span><strong>Measurement</strong><p>Ultrasound, rPPG, report, and reset</p></div>
    </div>
    <figcaption id="viscan-flow-caption">Disclosure-safe state flow for the ViScan system.</figcaption>
  </figure>

  <section id="patent" class="research-section boundary-panel">
    <h2>Korean patent application</h2>
    <dl class="profile-facts">
      <div><dt>Title</dt><dd>“Ultrasound-Based Smart Mirror Body Composition Analysis System” — portfolio translation of the Korean filing title</dd></div>
      <div><dt>Application No.</dt><dd><strong>10-2026-0154726</strong></dd></div>
      <div><dt>Filing date</dt><dd>August 18, 2026</dd></div>
      <div><dt>Applicants</dt><dd>Dankook University Cheonan Campus Industry-Academic Cooperation Foundation and Hansono Co., Ltd.</dd></div>
      <div><dt>Role</dt><dd>Co-inventor</dd></div>
      <div><dt>Legal status</dt><dd>Patent application filed. This does not mean that a patent has been granted or that rights have been finally established.</dd></div>
    </dl>
  </section>
</main>
