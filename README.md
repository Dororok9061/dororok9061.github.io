# Hyeongrok Ryu Engineering Portfolio

Root GitHub Pages site for [tontonjeong.github.io](https://tontonjeong.github.io/).

The site connects public evidence across FPGA RTL/DV, FMCW radar, embedded
systems, biomedical AI, systems engineering, and electrical engineering
coursework.

## Architecture

- Static HTML and CSS
- One small Vanilla JavaScript file for theme preference
- No runtime package dependency
- No database, authentication, API, form backend, analytics, ads, chat, or Service Worker
- GitHub Actions Pages deployment with actions pinned to full commit SHAs

## Validate

```powershell
python scripts/check_site.py site
powershell -ExecutionPolicy Bypass -File scripts/security/verify-site-security.ps1 -SiteRoot .
powershell -ExecutionPolicy Bypass -File scripts/security/verify-site-security.ps1 -SiteRoot site -BuiltSite
```

After deployment:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/security/verify-site-security.ps1 `
  -SiteRoot site `
  -BuiltSite `
  -PublicUrl "https://tontonjeong.github.io/" `
  -Online
```

## Documentation

- [Project inventory](docs/inventory/PROJECT_INVENTORY.md)
- [Notion inventory](docs/inventory/NOTION_INVENTORY.md)
- [Theme audit](docs/design/THEME_AUDIT.md)
- [Theme decision](docs/design/THEME_DECISION.md)
- [Third-party notices](docs/design/THIRD_PARTY_NOTICES.md)
- [Threat model](docs/security/THREAT_MODEL.md)
- [Security architecture](docs/security/SECURITY_ARCHITECTURE.md)
- [Data classification](docs/security/DATA_CLASSIFICATION.md)

## Public evidence rule

`SOURCE AVAILABLE`, `EXECUTED`, `MEASURED`, and `BLOCKED` are separate states.
Missing evidence is never relabeled as a pass.

