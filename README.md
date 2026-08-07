# Hyeongrok Ryu Engineering Portfolio

[![GitHub Pages](https://img.shields.io/badge/Portfolio-dororok9061.github.io-2E86AB)](https://dororok9061.github.io/)
[![Research Cases](https://img.shields.io/badge/View-Research%20Case%20Studies-111111)](https://dororok9061.github.io/projects/)
[![Public Notion](https://img.shields.io/badge/Notion-Engineering%20Portfolio-000000)](https://fierce-rodent-308.notion.site/Engineering-Portfolio-FPGA-Radar-Embedded-Systems-Biomedical-AI-3ab518ac7a598121b666e4c7cce8324c)

The multilingual, multi-page Jekyll source for
[dororok9061.github.io](https://dororok9061.github.io/). It connects public
evidence across radar signal processing, Vision AI, sensor fusion, embedded
systems, FPGA RTL/DV, biomedical AI, systems engineering, publications,
coursework, and engineering study notes.

## Research Case Study framework

The existing Jekyll 4 + Simplex visual theme is preserved. A shared research-page
structure is layered across projects, publications, coursework, technical blog
posts, STM32/PADS/mmWave study units, and external-learning notes.

Each detailed page is organized around the material that actually exists:

```text
Problem or research question
→ Architecture and data flow
→ Hardware / software / equations
→ Methodology and implementation
→ Results and figures
→ Contribution, resources, and next work
```

### Representative case studies

| Domain | Website case study | Repository case study |
|---|---|---|
| FMCW Radar · ECG/SCG sensing | [FMCW Radar Cardiac Timing](https://dororok9061.github.io/projects/fmcw-radar/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/fmcw-radar-aoac-cardiac-analysis/blob/main/RESEARCH_CASE_STUDY.md) |
| PPG · HRV · Biomedical AI | [PPG–HRV Cognitive Load](https://dororok9061.github.io/projects/ppg-hrv/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/PPG-HRV-Cognitive-Load-CNN/blob/main/RESEARCH_CASE_STUDY.md) |
| FPGA RTL · Digital Verification | [FPGA Delay Logic](https://dororok9061.github.io/projects/fpga-delay-logic/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/fpga-delay-logic-design-verification/blob/main/RESEARCH_CASE_STUDY.md) |
| Vision · Embedded Systems | [Drowsiness Monitor](https://dororok9061.github.io/projects/drowsiness-monitor/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/Sleep-monitoring-and-prevention-device/blob/main/RESEARCH_CASE_STUDY.md) |
| Electrical Engineering Coursework | [Coursework hub](https://dororok9061.github.io/coursework/) | [RESEARCH_CASE_STUDY.md](https://github.com/Dororok9061/electrical-engineering-coursework-portfolio/blob/main/RESEARCH_CASE_STUDY.md) |

The homepage now exposes the case-study hub before the original hero section so
visitors can immediately enter the technical evidence rather than searching for
the new structure at the bottom of the page.

## Figure strategy and PaperBanana

Existing experiment photographs, source-derived plots, waveforms, circuit
screens, and report figures remain the preferred assets. When a publishable
architecture or methodology figure is missing, the page first renders a
source-faithful HTML/CSS concept flow. PaperBanana is prepared as a second-stage
academic-figure workflow for high-resolution replacements.

- [PaperBanana workflow](docs/PAPERBANANA_FIGURE_WORKFLOW.md)
- [Figure backlog and prompts](docs/paperbanana_figures.yml)

Generated figures must not invent measurements, hardware, model scores, PPA,
clinical claims, certifications, or CES award results.

## Theme and architecture

- Jekyll `4.4.1`
- actual Gem Theme: `jekyll-theme-simplex 0.9.8.15` (MIT)
- Korean and English routes with independent project, publication, coursework,
  defense, role, lab, blog, category, about, and security pages
- static HTML/CSS output with small first-party Vanilla JavaScript files for
  accessible navigation, image lightbox, search, section tracking, and BibTeX copy
- no database, authentication, API, form backend, analytics, ads, chat,
  Service Worker, or runtime framework
- GitHub Actions build and Pages deployment with every Action pinned to a full
  commit SHA

`src/` is the Jekyll source and `_site/` is the generated, ignored output. The
previous hand-authored site remains in `site/` only as a recovery snapshot; the
deployment workflow does not publish it.

## Build and validate

```bash
bundle install
JEKYLL_ENV=production bundle exec jekyll build --source src --destination _site --trace
python3 scripts/check_site.py _site
pwsh scripts/security/verify-site-security.ps1 -SiteRoot .
pwsh scripts/security/verify-site-security.ps1 -SiteRoot _site -BuiltSite
```

Windows PowerShell can invoke the scanner with:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File scripts/security/verify-site-security.ps1 -SiteRoot _site -BuiltSite
```

After deployment:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File scripts/security/verify-site-security.ps1 `
  -SiteRoot _site -BuiltSite `
  -PublicUrl "https://dororok9061.github.io/" -Online
```

## Documentation

- [Project inventory](docs/inventory/PROJECT_INVENTORY.md)
- [Notion inventory](docs/inventory/NOTION_INVENTORY.md)
- [Theme audit](docs/design/THEME_AUDIT.md)
- [Theme decision](docs/design/THEME_DECISION.md)
- [Third-party notices](docs/design/THIRD_PARTY_NOTICES.md)
- [Profile asset status](docs/PROFILE_ASSET_STATUS.md)
- [Threat model](docs/security/THREAT_MODEL.md)
- [Security architecture](docs/security/SECURITY_ARCHITECTURE.md)
- [Data classification](docs/security/DATA_CLASSIFICATION.md)
- [Deployment verification report](docs/security/VERIFICATION_REPORT_2026-07-31.md)

## Public evidence rule

Source files, rerun simulations, measured hardware results, generated
illustrations, and proposed future work are kept distinct. Missing evidence is
not converted into a pass or a measured result.
