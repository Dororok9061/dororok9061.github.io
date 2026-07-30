# Attack Surface Register

## 상태 기준

- `PASS`: 현재 증거로 통제가 적용되고 검증됨
- `BLOCKED`: 저장소·배포·계정 설정 또는 승인 자료가 없어 검증/적용 불가
- `PLATFORM LIMITATION`: GitHub Pages나 외부 서비스가 필요한 통제를 제공하지 않음
- `ACCEPTED`: 기능 제거 또는 명시적 판단으로 남은 위험을 수용

2026-07-31 Simplex/Jekyll 재구축 산출물의 로컬 검증을 완료했다. 계정·로컬
기기·비공개 원본처럼 이 작업의 검증 범위를 벗어난 항목은 `BLOCKED`로 유지한다.

| ID | Attack surface | Entry point / data flow | 주요 Asset | 주요 공격 | 필수 통제 | Owner | 검증 | Status |
|---|---|---|---|---|---|---|---|---|
| AS-01 | 방문자 Browser | HTML/CSS/JS, URL fragment/query, 외부 링크 | 방문자 세션·표시 무결성·사이트 신뢰 | XSS, DOM injection, open redirect, mixed content, clickjacking | 사용자 입력 없음, DOM sink 금지, CSP, HTTPS-only, 외부 링크 검토 | 사이트 소유자/Browser vendor | 정적 scan, CSP console, 링크 crawl | PASS — source/build/browser 검사 |
| AS-02 | GitHub Pages Hosting | GitHub CDN/Fastly가 정적 파일 제공 | 가용성·전송 무결성 | HTTP downgrade, DDoS, stale deployment, 임의 header 부재 | Enforce HTTPS, 플랫폼 상태 모니터링, 최소 asset, no-cache 의존 금지 | GitHub/사이트 소유자 | curl, TLS, 공개 URL | PASS — HTTP 301, HTTPS 200, TLS 1.3 |
| AS-03 | GitHub Repository | commit, PR, branch, release, tag | 소스·history·Pages 설정 | 계정 탈취, workflow 변조, secret commit, branch 삭제 | 2FA/passkey, ruleset, 최소 collaborator, secret scanning, signed/tag review | 사이트 소유자/GitHub | repo settings, security log, history scan | PASS — public repo, ruleset, 보안 정책 |
| AS-04 | GitHub Actions Runner | workflow event, checkout, build command, artifact | `GITHUB_TOKEN`, 배포권한, 산출물 | script injection, malicious Action, poisoned artifact/cache | hosted runner, 최소 permissions, SHA pin, untrusted context를 env로 전달, secret 없음 | 사이트 소유자/GitHub | workflow review, run log | PASS — 최소 권한·5개 Action full SHA; 새 run은 PR/main에서 재검증 |
| AS-05 | Ruby/Jekyll/Node Dependency | Gemfile/package manifest, lockfile, install hook | build integrity | typosquat, compromised package, transitive malware | 필요한 의존성만, lockfile, trusted registry, Dependabot, license review | 사이트 소유자/upstream | manifest/lock diff, advisory scan | PASS — 7개 direct·41개 total Gem 고정, npm 0개 |
| AS-06 | 사용자 지정 Domain 및 DNS | registrar, DNS records, CNAME/A/AAAA | 이름·TLS·브랜드 신뢰 | DNS spoofing, dangling record, domain takeover, expiry | domain verification, registrar MFA/lock, 최소 records, DNSSEC 가능성 검토, 해제 시 record 먼저 제거 | 사용자/registrar/GitHub | DNS 조회, Pages domain check, expiry alert | ACCEPTED — 현재 `github.io`만 사용 |
| AS-07 | Public Notion | 외부 HTTPS hyperlink/embed | 설명 신뢰·방문자 이동 | 공개범위 오설정, 계정 탈취, 악성 redirect/콘텐츠 변경 | embed script 금지, 링크 allowlist, 정기 공개범위 검토, 외부임을 표시 | Notion 계정 owner | 익명 브라우저, URL inventory | PLATFORM LIMITATION |
| AS-08 | 외부 GitHub Project Pages | 외부 HTTPS hyperlink | 프로젝트 근거·브랜드 신뢰 | 외부 repo takeover, 오래된 Pages, mixed content | 소유 repo만 우선, HTTPS, 정기 link/status 검사, 실행 코드 import 금지 | 각 repo owner | link crawl, repo owner 확인 | PLATFORM LIMITATION |
| AS-09 | Local Development PC | editor, browser, Git credential, removable media | token·source·archive·계정 | malware, theft, session hijack, accidental push | OS update, disk encryption, auto-lock, EDR/AV, least privilege, encrypted backup, credential manager | 사용자 | 로컬 보안 설정 점검 | BLOCKED — 원격 검증 불가 |
| AS-10 | Private Source Archive | archive 열기·선별·복사 | 미공개 IP·개인정보·원본 | archive slip, malware, bulk accidental publish | 원본 read-only 백업, 격리 해제, AV scan, 파일별 allowlist, public 파생본만 복사 | 사용자/자료 owner | hash inventory, manual approval | BLOCKED — archive 미검토 |
| AS-11 | Quartus·EDA License Storage | license manager, license file, 환경변수·log | license credential·계약정보 | commit/log/screenshot 유출, malware 탈취 | workspace/repo와 분리, 최소 ACL, 암호화 저장, screenshot redaction, secret scan | 사용자/발급기관 | 경로/ACL 및 history 검사 | BLOCKED — 내용 미열람·보관 통제 미검증 |
| AS-12 | Third-Party Theme·Template Source | download, copy, package install | site source·visitor browser | backdoor, license violation, dependency confusion | LICENSE/commit/source 검토, 무출처 복사 금지, 필요한 아이디어만 재구현, hash/버전 기록 | 사이트 소유자/upstream | theme audit, diff, license notice | PASS — MIT Simplex 0.9.8.15 실제 Gem·SHA·commit 감사, 불명확 소스 제외 |

## 노출 파일 금지 목록

다음 파일은 확장자만 바꾸거나 링크를 숨기는 방식으로 공개하지 않는다.

- `.env*`, private key, SSH key, credential, recovery code
- `*.dat`, `*.lic` 등 EDA/license 파일
- Quartus/EDA 원본·archive·programming output
- `*.map` source map, debug dump, coverage raw data
- private archive와 원본 연구데이터
- 원본 profile/health/biometric data
- 절대 로컬 경로와 사용자 계정명이 포함된 log·screenshot

## 변경 규칙

다음 변경은 이 register와 Threat Model을 같은 PR에서 갱신해야 한다.

- 외부 script/font/form/analytics 추가
- 사용자 입력, 저장, 로그인, API, Service Worker 추가
- custom domain 또는 DNS 변경
- Actions permission·trigger·runner·third-party action 변경
- 새 dependency/theme/template 추가
- 새로운 데이터 유형 또는 직접 다운로드 asset 공개
