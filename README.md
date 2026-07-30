# Hyeongrok Ryu Engineering Portfolio

The multilingual, multi-page Jekyll source for
[tontonjeong.github.io](https://tontonjeong.github.io/). It connects public
evidence across FPGA RTL/DV, FMCW radar, embedded systems, biomedical AI,
systems engineering, publications, role-oriented views, and electrical
engineering coursework.

## Theme and architecture

- Jekyll `4.4.1`
- actual Gem Theme: `jekyll-theme-simplex 0.9.8.15` (MIT)
- Korean and English routes with independent project, publication, coursework,
  defense, role, lab, blog, category, about, and security pages
- static HTML/CSS output and one small first-party Vanilla JavaScript file for
  the accessible mobile navigation
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
  -PublicUrl "https://tontonjeong.github.io/" -Online
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

## Public evidence rule

`SOURCE AVAILABLE`, `EXECUTED`, `MEASURED`, and `BLOCKED` are separate states.
Missing evidence is never relabeled as a pass.
