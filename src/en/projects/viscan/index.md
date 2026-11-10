---
layout: default
title: ViScan Smart Mirror
description: VISCAN engineering case study: CES 2027 Honoree in Digital Health and Sports & Fitness, with system integration and a Korean patent filing.
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
        <span>CES 2027 Honoree · Digital Health &amp; Sports &amp; Fitness</span>
        <span>Korean patent application filed</span>
        <span>CES 2027 booth operation and demonstration planned</span>
      </div>
    </div>
    <div class="project-heading__diagram" role="img" aria-label="ViScan processing flow">
      <span>Radar Presence</span><span>Vision AI · Sensor Fusion</span><span>Ultrasound · Report</span>
    </div>
  </header>

  {% include project-shortcuts.html project_id='viscan' id='project-files' %}

  <nav class="research-jump-nav" aria-label="On this page">
    <span class="research-jump-nav__label">On this page</span>
    <div class="research-jump-nav__links">
      <a href="#problem">Problem</a><a href="#architecture">Architecture</a><a href="#methodology">Implementation</a><a href="#results">Milestones</a><a href="#ces-award">CES 2027</a><a href="#patent">Patent filing</a>
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
        <li><strong>CES 2027 Innovation Awards Honoree in Digital Health and Sports &amp; Fitness.</strong> <a href="https://www.ces.tech/ces-innovation-awards/2027/viscan-ai-guided-ultrasound-mirror-for-muscle-and-fat-tracking/" target="_blank" rel="noopener noreferrer">Official CES listing</a></li>
        <li>ViScan booth operation and live product demonstration planned for CES 2027</li>
        <li>Integrated test rates: radar 20.017 Hz, camera 14.696 fps, pose 14.650 Hz</li>
        <li>Technical reports, presentations, company meetings, prior-art review, and commercialization planning completed</li>
      </ul>
    </section>
  </div>

  <section id="ces-award" class="research-section boundary-panel" aria-labelledby="viscan-ces-award-title">
    <p class="eyebrow">CES 2027 · Innovation Awards</p>
    <h2 id="viscan-ces-award-title">Honoree in Digital Health and Sports &amp; Fitness</h2>
    <p><strong>Official product:</strong> VISCAN: AI Guided Ultrasound Mirror for Muscle and Fat Tracking</p>
    <p>VISCAN combines AI-assisted probe placement with ultrasound measurement of regional skin, subcutaneous-fat and muscle thickness. The product received Honoree designations in two CES 2027 categories, announced on November 9, 2026.</p>
    <p><strong>My contributions:</strong> C# WPF smart-mirror application integration; camera and MediaPipe Pose AI Guide; ultrasound SDK/B-mode connection; measurement state handling; user profiles, result visualization and reporting; troubleshooting for system responsiveness and reliability.</p>
    <p><strong>Collaboration:</strong> Developed under the WE-Meet project within Next-Generation Display COSS, with students from Dankook, Hoseo and Hanseo Universities. Hansono provided ultrasound technology support; Dankook University's Future Imaging Research Lab led integrated system and software development.</p>
    <p><a class="text-link" href="https://www.ces.tech/ces-innovation-awards/2027/viscan-ai-guided-ultrasound-mirror-for-muscle-and-fat-tracking/" target="_blank" rel="noopener noreferrer">View the official CES VISCAN Honoree page →</a></p>
    <p class="small-note">The Honoree recognition applies to the product, not an individual; it is not a medical-performance certification.</p>
  </section>

  <figure class="research-flow-figure" aria-labelledby="viscan-flow-caption">
    <div class="research-flow-figure__grid">
      <div class="research-flow-step"><span class="research-flow-step__index">01</span><strong>Presence</strong><p>BGT60TR13C presence, distance, and stability</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">02</span><strong>Session</strong><p>YuNet/SFace face session</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">03</span><strong>Guidance</strong><p>MediaPipe Pose and camera–radar fusion</p></div>
      <div class="research-flow-step"><span class="research-flow-step__index">04</span><strong>Measurement</strong><p>Ultrasound, rPPG, report, and reset</p></div>
    </div>
    <figcaption id="viscan-flow-caption">ViScan state-based processing flow.</figcaption>
  </figure>

  <section id="patent" class="research-section boundary-panel">
    <h2>Korean patent application</h2>
    <dl class="profile-facts">
      <div><dt>Title</dt><dd>“Ultrasound-Based Smart Mirror Body Composition Analysis System” — portfolio translation of the Korean filing title</dd></div>
      <div><dt>Application No.</dt><dd><strong>10-2026-0154726</strong></dd></div>
      <div><dt>Filing date</dt><dd>August 18, 2026</dd></div>
      <div><dt>Applicants</dt><dd>Dankook University Cheonan Campus Industry-Academic Cooperation Foundation and Hansono Co., Ltd.</dd></div>
      <div><dt>Role</dt><dd>Co-inventor</dd></div>
      <div><dt>Legal status</dt><dd>Patent application filed.</dd></div>
    </dl>
  </section>
</main>
