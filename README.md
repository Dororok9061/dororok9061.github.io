# Hyeongrok Ryu Engineering Portfolio

[![GitHub Pages](https://img.shields.io/badge/Portfolio-dororok9061.github.io-2E86AB)](https://dororok9061.github.io/)
[![Start Here](https://img.shields.io/badge/Research%20Portal-Start%20Here-1565C0)](https://dororok9061.github.io/blog/start-here/)
[![Research Cases](https://img.shields.io/badge/View-Research%20Case%20Studies-111111)](https://dororok9061.github.io/projects/)
[![Source Map](https://img.shields.io/badge/Source-Collections-0F766E)](https://dororok9061.github.io/source-collections/)
[![Public Notion](https://img.shields.io/badge/Notion-Engineering%20Portfolio-000000)](https://fierce-rodent-308.notion.site/Engineering-Portfolio-FPGA-Radar-Embedded-Systems-Biomedical-AI-3ab518ac7a598121b666e4c7cce8324c)

The multilingual Jekyll portfolio for [dororok9061.github.io](https://dororok9061.github.io/) connects radar signal processing, Vision AI, sensor fusion, embedded systems, FPGA RTL/DV, biomedical AI, RF/microwave, PCB design, control, publications, coursework, and study notes.

## Dedicated research portal

The existing Jekyll 4 + Simplex visual theme remains in place. The generated `/blog/start-here/` route now uses a dedicated paper-style layout inspired by the iNdra research-page template:

```text
Abstract and author block
→ Material-icon resource buttons
→ Introduction and research domains
→ Methodology figure
→ Project results
→ Horizontal image gallery
→ Uploaded source collections
→ Resources and BibTeX
```

The previous full-width research takeover was removed from the homepage. The normal profile homepage remains the first screen, while the navigation exposes a direct **Research Hub** link.

## Representative case studies

| Domain | Website case study | Repository case study |
|---|---|---|
| FMCW Radar · ECG/SCG sensing | [FMCW Radar Cardiac Timing](https://dororok9061.github.io/projects/fmcw-radar/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/fmcw-radar-aoac-cardiac-analysis/blob/main/RESEARCH_CASE_STUDY.md) |
| PPG · HRV · Biomedical AI | [PPG–HRV Cognitive Load](https://dororok9061.github.io/projects/ppg-hrv/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/PPG-HRV-Cognitive-Load-CNN/blob/main/RESEARCH_CASE_STUDY.md) |
| FPGA RTL · Digital Verification | [FPGA Delay Logic](https://dororok9061.github.io/projects/fpga-delay-logic/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/fpga-delay-logic-design-verification/blob/main/RESEARCH_CASE_STUDY.md) |
| Vision · Embedded Systems | [Drowsiness Monitor](https://dororok9061.github.io/projects/drowsiness-monitor/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/Sleep-monitoring-and-prevention-device/blob/main/RESEARCH_CASE_STUDY.md) |
| Electrical Engineering Coursework | [Coursework hub](https://dororok9061.github.io/coursework/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/electrical-engineering-coursework-portfolio/blob/main/RESEARCH_CASE_STUDY.md) |

## Uploaded source collections

The public source map inventories three uploaded archives without publishing the raw ZIP files:

- **Low-Power Semiconductor Circuit Design** — 137 entries across shift-register, circular-queue, and memory-based delay-logic projects; SystemVerilog, ModelSim, Quartus, reference vectors, and regression files.
- **Defense Systems Engineering** — 28 entries covering Counter-UAS, EW jammer specification, KF-21 reliability, course materials, and screenshots.
- **Undergraduate Coursework and Projects** — 576 entries including 473 images and 28 PDFs across high-frequency engineering, controller logic, power systems, motor control, electrical machines, sensor applications, and VRET.

See [Portfolio Source Collection Map](https://dororok9061.github.io/source-collections/).

## Figure strategy and PaperBanana

Existing experiment photographs, source-derived plots, waveforms, circuit screens, and report figures remain the preferred assets. When an architecture or methodology figure is missing, the page first renders a source-based SVG/HTML figure.

- [PaperBanana workflow](docs/PAPERBANANA_FIGURE_WORKFLOW.md)
- [Figure backlog and prompts](docs/paperbanana_figures.yml)
- [Start Here methodology figure](src/assets/images/research/start-here-methodology.svg)
- [Start Here domain map](src/assets/images/research/start-here-domain-map.svg)

A PaperBanana output is not published as experimental evidence until every label, arrow, component, and numeric value has been checked against the linked source. Generated figures must not invent measurements, hardware, model scores, PPA, clinical claims, certifications, or CES award results.

## Material icons

The research portal uses local SVG assets based on Google's Material Icons under the Apache License 2.0. They are stored under `src/assets/icons/material/` and are loaded locally to preserve the site's strict Content Security Policy.

## Theme and architecture

- Jekyll `4.4.1`
- Gem theme: `jekyll-theme-simplex 0.9.8.15` (MIT)
- Korean and English routes for projects, publications, coursework, defense, roles, lab, blog, category, about, and source-collection pages
- static HTML/CSS output with small first-party Vanilla JavaScript files for navigation, lightbox, section tracking, gallery controls, theme switching, and BibTeX copy
- no database, authentication, form backend, analytics, ads, chat, or runtime framework
- GitHub Actions build and Pages deployment with pinned Actions

`src/` is the Jekyll source and `_site/` is the ignored generated output.

## Build and validate

```bash
bundle install
JEKYLL_ENV=production bundle exec jekyll build --source src --destination _site --trace
python3 scripts/check_site.py _site
pwsh scripts/security/verify-site-security.ps1 -SiteRoot .
pwsh scripts/security/verify-site-security.ps1 -SiteRoot _site -BuiltSite
```

## Documentation

- [Project inventory](docs/inventory/PROJECT_INVENTORY.md)
- [Notion inventory](docs/inventory/NOTION_INVENTORY.md)
- [PaperBanana workflow](docs/PAPERBANANA_FIGURE_WORKFLOW.md)
- [Threat model](docs/security/THREAT_MODEL.md)
- [Security architecture](docs/security/SECURITY_ARCHITECTURE.md)
- [Data classification](docs/security/DATA_CLASSIFICATION.md)

## Publication rule

User-authored code, reports, calculations, and figures are used on the relevant pages. Course handouts, company-analysis books, certificates, licenses, and material with unclear redistribution rights are retained for review and attribution rather than uploaded unchanged. Source files, rerun simulations, measured hardware results, generated illustrations, and proposed future work remain distinct.
