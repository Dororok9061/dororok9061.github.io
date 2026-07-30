# Security Verification Report — 2026-07-30

## Scope

- Repository: `Tontonjeong/Tontonjeong.github.io`
- Public site: `https://tontonjeong.github.io/`
- Published artifact: the allowlisted `site/` directory only
- Architecture: static HTML/CSS, one first-party Vanilla JavaScript file, no
  server, database, authentication, form backend, analytics, or service worker

## Verified controls

| Control | Evidence | Status |
|---|---|---|
| HTTP upgrade | `http://tontonjeong.github.io/` returned `301` to the identical HTTPS host | PASS |
| HTTPS | Root URL returned `200`; GitHub Pages API reported `https_enforced: true` | PASS |
| TLS | TLS 1.3; certificate subject `CN=*.github.io`; valid through 2026-09-03 KST | PASS |
| Mixed Content | Static source/build scan and live DOM resource inventory found zero HTTP resources | PASS |
| Public file allowlist | 21 files, 1,353,854 bytes; forbidden archives, licenses, maps, executables, and secrets absent | PASS |
| Browser structure | Korean and English pages each have one H1, one main landmark, canonical and hreflang metadata | PASS |
| Responsive layout | Desktop 1280×720 and mobile 390×844 showed no horizontal overflow | PASS |
| Images | Five sanitized WebP project images and JPEG fallbacks passed local load and metadata review | PASS |
| CSP | Strict meta CSP present; no inline script, external script, DOM HTML sink, or `eval` | PASS |
| Supply chain | No runtime/build packages; four GitHub-maintained Actions pinned to full commit SHAs | PASS |
| Actions | Validate and deploy run `30553770411` completed successfully | PASS |
| Deployment scope | Workflow uploads `site/` only and deploy job has only `contents: read`, `pages: write`, `id-token: write` | PASS |
| Repository reporting | `SECURITY.md` and GitHub private vulnerability reporting are enabled | PASS |

## Residual and blocked controls

| Control | Reason | Status |
|---|---|---|
| Clickjacking response header | GitHub Pages does not allow repository-defined `X-Frame-Options` or CSP `frame-ancestors` response headers; meta CSP cannot replace them | PLATFORM LIMITATION |
| DDoS edge controls | CDN and edge mitigation are operated by GitHub; the site owner can minimize assets and monitor status but cannot guarantee complete blocking | PLATFORM LIMITATION |
| GitHub account hardening | 2FA/passkey, recovery-code storage, active sessions, and token inventory require the account owner to inspect settings | BLOCKED |
| Local PC hardening | Disk encryption, auto-lock, OS/AV status, physical security, and backup posture were not remotely verified | BLOCKED |
| Private archive | The archive was not opened or copied; malware and contents were intentionally not inspected in this release | BLOCKED |
| EDA license storage | The license file was not opened, copied, scanned, or committed; its local ACL/encryption posture was not verified | BLOCKED |
| Formal profile photo | The supplied original resides in OneDrive and was not touched; the public site uses a non-biometric HR identity graphic | BLOCKED |
| Custom domain and DNS | No custom domain is configured; registrar and DNS controls are not applicable to this deployment | ACCEPTED |

## Verification commands

```powershell
python scripts/check_site.py site
powershell -File scripts/security/verify-site-security.ps1 -SiteRoot .
powershell -File scripts/security/verify-site-security.ps1 -SiteRoot site -BuiltSite
powershell -File scripts/security/verify-site-security.ps1 `
  -SiteRoot site `
  -PublicUrl "https://tontonjeong.github.io/" `
  -BuiltSite `
  -Online
curl.exe -I "http://tontonjeong.github.io/"
curl.exe -I "https://tontonjeong.github.io/"
```

This report records a point-in-time verification. It does not claim complete
protection from intrusion, phishing, supply-chain compromise, or denial of
service.
