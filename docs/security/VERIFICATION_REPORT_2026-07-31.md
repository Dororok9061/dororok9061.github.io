# Simplex Deployment Verification Report — 2026-07-31

## Release identity

- Public site: <https://tontonjeong.github.io/>
- Release pull request: [#3](https://github.com/Tontonjeong/Tontonjeong.github.io/pull/3)
- Main merge commit: `234ac48a4ce39acb56dbfe411b7cc353c9ec4110`
- Main validation and deployment run:
  [30561360113](https://github.com/Tontonjeong/Tontonjeong.github.io/actions/runs/30561360113)
- Theme: `jekyll-theme-simplex 0.9.8.15` (MIT), used as the actual Gem Theme
- Downloaded theme Gem SHA-256:
  `850ab718db1bd59d34612c8ed348577f8684e1aafd1bdccaa7f08ae3a17023a9`

## Verified controls

| Area | Verification evidence | Status |
|---|---|---|
| Jekyll build | Production build completed with 95 public files totaling 2,279,719 bytes | PASS |
| Theme use | `theme: jekyll-theme-simplex`; theme SCSS and WOFF2 assets resolve from the Gem | PASS |
| Minimum runtime | Static HTML/CSS plus one small first-party Vanilla JavaScript navigation file; no database, API, authentication, analytics, service worker, or runtime framework | PASS |
| Dependency scope | 7 direct and 41 total locked Gems; npm dependency count is zero | PASS |
| Dependency advisories | Bundler Audit database commit `99b6a95eafdbe9763c8f12aa2dc9017bdec27ab1`; no known vulnerabilities reported | PASS |
| GitHub Actions | Five third-party/official Actions pinned to full commit SHAs; minimum job permissions; hosted runner | PASS |
| CI/CD | PR validation and main validation/deployment completed successfully | PASS |
| HTTPS | HTTP redirects to the identical HTTPS host with 301; HTTPS returns 200 | PASS |
| TLS | TLS 1.3; certificate hostname matches `*.github.io`; certificate valid through 2026-09-03 KST at verification time | PASS |
| Mixed content | Source, built output, online security scan, and public browser console showed no mixed-content finding | PASS |
| Browser security | CSP present; no user HTML input, DOM HTML sink, `eval`, open redirect, form backend, or state-changing request | PASS |
| Localization | Korean and English root, project, blog, publication, and security routes return public pages with matching language metadata and canonicals | PASS |
| Project media | All ten retained project JPEG/WebP public asset URLs returned 200; lazy-loaded images completed when brought into view | PASS |
| Accessibility | Skip link, landmarks, labelled mobile navigation, keyboard Escape close/focus return, visible focus, reduced-motion rule, and no horizontal overflow verified | PASS |
| SEO | Per-page titles/descriptions, canonical links, Open Graph image, `robots.txt`, sitemap, and feed generated | PASS |

## Blocked, accepted, and platform-limited controls

These items are deliberately not recorded as PASS.

| Control | Status | Reason / owner boundary |
|---|---|---|
| Clickjacking response headers (`frame-ancestors` or `X-Frame-Options`) | PLATFORM LIMITATION | GitHub Pages does not provide repository-controlled arbitrary response headers. Meta CSP cannot replace this control. |
| Complete DDoS or bot-abuse blocking | PLATFORM LIMITATION | Availability and edge mitigation remain primarily GitHub/Fastly responsibilities; no claim of complete blocking is made. |
| Recall of historical deployments, crawled copies, and direct asset URLs | PLATFORM LIMITATION | Public caches and copies cannot be guaranteed to be recalled after publication. |
| GitHub account 2FA/passkeys and recovery-code custody | BLOCKED | Account settings and physical custody were outside repository verification. Site owner action is required. |
| Local PC encryption, EDR/AV, auto-lock, backup, and physical custody | BLOCKED | Device controls could not be remotely verified. Site owner/OS boundary. |
| Private source archive | BLOCKED | The supplied ZIP was not opened, extracted, copied, or published. |
| Quartus/EDA license storage | BLOCKED | The license file was not opened, copied, or published; storage ACL and issuer controls remain outside the site build. |
| Public Notion and external GitHub Project Pages | PLATFORM LIMITATION | Their accounts, availability, redirects, and future content are controlled by their respective service/project owners. |

## Data-protection record

- The approved profile photograph was processed only into metadata-free,
  resized public derivatives for Hero/About use.
- The OneDrive original was not modified, moved, renamed, or deleted.
- Existing public project visuals were retained as public derivatives.
- The private source archive and EDA license were excluded from source,
  generated output, Git history, and deployment.
- Evidence labels remain distinct: missing execution or measurement evidence is
  not presented as verified.
