# Threat Model

## 범위와 평가 방법

대상은 공개 정적 Engineering Portfolio의 source, build, GitHub Pages 배포,
외부 링크, DNS, 개발 PC와 비공개 원본이다. 서버 인증·DB·결제·업로드·상태 변경
기능은 아키텍처에서 제외한다.

Likelihood와 Impact는 `Low / Medium / High / Critical`로 기록한다. Risk는 둘을
보수적으로 결합한 `Critical / High / Medium / Low / Accepted`다.

Status:

- `PASS`: 실제 적용과 검증 증거가 있음
- `BLOCKED`: 적용 대상이나 필요한 권한·저장소·배포·자료가 없음
- `PLATFORM LIMITATION`: GitHub Pages/외부 플랫폼 제약으로 통제를 직접 적용할 수 없음
- `ACCEPTED`: 기능 제거 또는 명시적 판단으로 남은 위험을 수용

2026-07-30 현재 루트 repository와 Pages 배포가 없어 PASS 항목은 없다.

## Threat Register

| ID | Threat | Asset | Threat Actor | Attack Vector | Likelihood | Impact | Risk | Existing Control | Required Control | Residual Risk | Owner | Verification Method | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T-01 | HTTP 평문·Mixed Content | 방문자 통신, 페이지 무결성 | 동일 네트워크 공격자, 악성 ISP/프록시 | HTTP 접속, `http://` asset, downgrade | Medium | High | High | `github.io` wildcard TLS 인증서가 검사 시 유효 | Pages 생성, Enforce HTTPS, HTTP→동일 host HTTPS redirect, source와 `_site`의 HTTP resource 0건 | Low — TLS/브라우저/플랫폼 의존 | 사이트 소유자/GitHub | `curl -I`, 인증서 hostname/기간, browser console, 보안 script | BLOCKED — HTTP/HTTPS 모두 404, redirect 없음 |
| T-02 | XSS | 방문자 DOM·브랜드 신뢰 | 콘텐츠 공급망 공격자, repo 침입자 | 악성 script, inline handler, 외부 script | Low | High | Medium | 정적·무입력 아키텍처 원칙 | 외부 script 기본 금지, strict CSP, inline handler 금지, code review | Low — repository compromise 시 가능 | 사이트 소유자 | source/build scan, CSP console, 수동 DOM review | BLOCKED — 소스 없음 |
| T-03 | HTML Injection | 표시 콘텐츠·외부 링크 | 악성 데이터 제공자, repo 침입자 | Markdown/템플릿에서 raw HTML 삽입 | Low | High | Medium | 사용자 입력·동적 CMS 없음 | 데이터는 text escape, raw HTML allowlist 금지, 외부 콘텐츠 build-time 검토 | Low | 사이트 소유자 | 생성 HTML diff, raw HTML pattern review | BLOCKED |
| T-04 | DOM Injection | 방문자 DOM | 악성 URL 작성자, 외부 링크 공격자 | query/hash를 `innerHTML`, `document.write`, `insertAdjacentHTML`에 연결 | Low | High | Medium | 최소 Vanilla JS, 동적 기능 없음 | `textContent`/안전 DOM API만 사용, DOM sink와 `eval` 검사 | Low | 사이트 소유자 | JS 정적 scan, crafted query/hash test | BLOCKED |
| T-05 | Clickjacking | 사이트 신뢰, 외부 링크 유도 | 피싱 운영자 | 사이트를 공격자 iframe에 삽입 | Medium | Medium | Medium | 상태 변경·로그인 없음으로 직접 피해 제한 | CSP `frame-ancestors 'none'` 또는 `X-Frame-Options: DENY` 응답 헤더 | Medium — meta CSP는 `frame-ancestors` 미지원 | GitHub/사이트 소유자 | response header, iframe 재현 | PLATFORM LIMITATION — 임의 Pages 응답 헤더 불가 |
| T-06 | Open Redirect | 도메인 신뢰·방문자 | 피싱 공격자 | query/hash 기반 `location` 이동, 미검증 redirect URL | Low | Medium | Low | redirect 기능 요구 없음 | redirect helper를 만들지 않음, `location.assign/replace/href` 입력 흐름 검사 | Low | 사이트 소유자 | JS scan, malicious URL test | BLOCKED — 소스 없음 |
| T-07 | CSRF | 상태 변경·credential | 외부 사이트 | 방문자 권한으로 state-changing request 유도 | Low | Low | Accepted | 서버·로그인·form backend·상태 변경 없음 | 해당 구조 유지; 상태 변경 기능 추가 시 token/SameSite/origin 검증과 모델 갱신 | Accepted while architecture holds | 사이트 소유자 | architecture/repository review | ACCEPTED — N/A by architecture |
| T-08 | DNS Spoofing·Domain Takeover | 도메인·브랜드·TLS | DNS 공격자, 만료 domain 인수자 | registrar 탈취, dangling CNAME, 미검증 custom domain | Low | High | Medium | 현재 custom domain 없이 `github.io` 사용 | custom domain 추가 전 verification, registrar MFA/lock, 최소 record, 해제 시 DNS 먼저 제거 | Low/Medium — registrar·DNS 의존 | 사용자/registrar/GitHub | DNS 조회, GitHub Pages domain check, expiry alert | ACCEPTED — 현재 custom domain 없음 |
| T-09 | 피싱·사칭 사이트 | 사용자 신원·채용 신뢰 | 사칭자 | 유사 domain/account, 복제 콘텐츠, 변조 외부 링크 | Medium | High | High | 공식 GitHub 계정 존재 | canonical URL, 공식 profile 역링크, 일관된 identity, 신고/증거 절차 | Medium — 공개 콘텐츠는 복제 가능 | 사용자/GitHub/외부 플랫폼 | canonical/OG 확인, 계정 링크 교차검증, 정기 검색 | BLOCKED — 루트 사이트 없음 |
| T-10 | DDoS·Bot Abuse | 가용성·대역폭·사용자 경험 | botnet, scraper | 대량 GET, asset hotlink, link crawler | Medium | Medium | Medium | 정적 사이트이며 origin DB/API 없음 | 작은 asset, 불필요 endpoint/검색/API 제거, GitHub 상태 모니터링 | Medium — 완전 차단 불가, edge는 GitHub 책임 | GitHub/사이트 소유자 | asset 크기, request pattern, GitHub Status | PLATFORM LIMITATION |
| T-11 | GitHub 계정 탈취 | repo·Pages·workflow·브랜드 | credential thief, session hijacker | phishing, token theft, 약한 복구 절차 | Medium | Critical | Critical | CLI 로그인 계정만 확인; 보안 설정은 미검증 | passkey/2FA, 복구 코드 오프라인 보관, session/token 정기 검토, 최소 PAT, security log alert | Medium — 계정 플랫폼 의존 | 사용자/GitHub | account security settings, security log, token inventory | BLOCKED — 계정 설정 원격 검증 불가 |
| T-12 | GitHub Actions Workflow 변조 | 배포 무결성·`GITHUB_TOKEN` | repo writer, 공급망 공격자 | workflow commit, `pull_request_target`, 과도한 permissions | Medium | Critical | Critical | 제공 workflow는 contents read만 사용 | branch/ruleset, workflow diff review, untrusted privileged checkout 금지, hosted runner만 | Low/Medium | 사이트 소유자/GitHub | YAML review, permissions, event, Actions log | BLOCKED — repo 없음 |
| T-13 | 악성 Dependency | build·배포 산출물·runner | package maintainer 공격자, typosquatter | compromised gem/npm/action, install script | Medium | High | High | 새 runtime dependency를 추가하지 않는 기준 | manifest 최소화, lockfile, trusted registry, advisory/Dependabot, install script 검토 | Medium — upstream compromise 가능 | 사이트 소유자/upstream | lock diff, dependency review, advisory scan | BLOCKED — manifest 없음 |
| T-14 | 공급망 공격 | source부터 배포까지의 무결성 | upstream/CI/account 공격자 | movable Action tag, poisoned cache/artifact/theme | Medium | Critical | Critical | checkout Action을 full SHA로 고정한 workflow template | 모든 Action full SHA, provenance/source 검토, cache 최소화, artifact를 신뢰 경계로 취급 | Medium | 사이트 소유자/GitHub/upstream | workflow SHA, dependency graph, build 재현 비교 | BLOCKED |
| T-15 | 악성코드·바이러스 | 로컬 PC·archive·repo | malware operator | archive/실행파일, 문서 macro, 감염된 개발기기 | Medium | High | High | 원본 archive와 OneDrive 자료를 이 작업에서 열지 않음 | 격리된 복사본, AV/EDR scan, 실행파일·macro public build 제외, OS patch | Medium | 사용자/OS vendor | AV 상태, hash inventory, file-type review | BLOCKED — 기기/자료 미검증 |
| T-16 | Backdoor | site JS·workflow·dependency | 악성 contributor/upstream | 난독화 코드, 외부 beacon, postinstall, 숨은 workflow | Low | Critical | High | 최소 코드·의존성 원칙 | 난독화/minified third-party 금지, 외부 network call 0개, diff/source review | Low/Medium | 사이트 소유자/upstream | grep/network inventory, dependency source audit | BLOCKED |
| T-17 | 시스템·네트워크 침해 | 개발 PC·Git credential·private data | 원격 공격자, 로컬 관리자 | OS exploit, rogue Wi-Fi, credential dump | Low | Critical | High | 미검증 | OS 업데이트, disk encryption, firewall, auto-lock, non-admin 개발, credential manager, 안전한 backup | Medium | 사용자/OS·network provider | 로컬 설정·보안 log 점검 | BLOCKED — 원격 검증 불가 |
| T-18 | 리버싱·역공학에 따른 민감정보 노출 | JS/config/asset에 포함된 내부정보 | 방문자, 경쟁자, scraper | 정적 bundle·이미지·metadata 분석 | High | High | High | secret이 필요 없는 정적 구조 | client에 공개 가능 정보만 포함, security by obscurity 금지, build 산출물 직접 검사 | Low if allowlist enforced | 사이트 소유자 | unpack/search, metadata scan, direct asset review | BLOCKED |
| T-19 | Source Map·Build Artifact 노출 | 원본 source·경로·debug 정보 | 방문자, scraper | `*.map`, debug dump, coverage, CI artifact URL | Medium | High | High | source map이 필요 없는 정적 구조 | production map 제외, `_site` allowlist, artifact 보존 최소화, 절대 경로 scan | Low | 사이트 소유자/GitHub | file inventory, direct URL, Actions artifact list | BLOCKED |
| T-20 | API Key·Token·License 유출 | GitHub/외부 계정·EDA license | credential harvester | commit/history/log/screenshot/asset에 평문 포함 | High | Critical | Critical | 별도 license 자료는 열거나 복사하지 않음 | RESTRICTED 분리 보관, pre-publish/history/secret scan, 노출 시 즉시 폐기·회전 | Medium — 탐지 pattern 한계 | 사용자/발급기관/GitHub | secret scanning, history scan, build scan, screenshot review | BLOCKED — repo/history·보관 설정 미검증 |
| T-21 | 개인정보·생체정보·연구데이터 유출 | 사용자·연구 참가자·원본 사진 | scraper, 침입자, 실수한 contributor | raw photo/EXIF, health data, participant ID, 문서 metadata | Medium | Critical | Critical | 공개용 파생본만 허용하는 분류 정책 | 명시적 승인, 최소화·비식별화, EXIF/XMP 제거, raw data·주소·연락처 금지 | Medium — 재식별 가능성 | 사용자/연구 data owner | metadata scan, data inventory, anonymous review | BLOCKED — 공개 asset inventory 없음 |
| T-22 | 로컬 개발 PC·물리 장비 탈취 | source·token·private archive·license | 절도범, 무단 사용자 | 잠금 해제 기기·디스크·removable media 탈취 | Low | Critical | High | 미검증 | full-disk encryption, auto-lock, biometric/PIN, 원격 세션 해지, encrypted backup, 장비 inventory | Medium | 사용자/기관 | device encryption/lock/recovery 점검 | BLOCKED |
| T-23 | 과거 배포·Preview·직접 Asset URL 우회 | 삭제된 콘텐츠·비공개로 전환한 asset | 이전 URL 보유자, crawler, cache | Git history, Pages CDN, release/artifact, guessed direct URL | Medium | High | High | 메뉴 비노출을 통제로 인정하지 않음 | 공개 전 allowlist, old branch/release/artifact 정리, 민감정보는 회전, cache/검색엔진 제거 요청 | Medium — 복제본·cache 완전 회수 불가 | 사이트 소유자/GitHub/검색엔진 | old URL inventory, history/tag/release/artifact 확인 | PLATFORM LIMITATION |
| T-24 | 비공개 Notion·GitHub·EDA 파일 실수 공개 | 비공개 문서·IP·license·연구데이터 | 실수한 maintainer, 공격자 | 잘못된 share 설정, bulk copy, archive commit, build glob | Medium | Critical | Critical | Public/Private 경계를 별도 정의 | explicit public allowlist, anonymous link test, glob 금지, build 후 재검사, 2인 검토가 가능하면 적용 | Low/Medium | 사용자/각 자료 owner | anonymous access, source/build/history scan, manual approval | BLOCKED |
| T-25 | 외부 Notion·Project Pages 변조 | 근거 링크·방문자 신뢰 | 외부 계정 공격자 | 링크 대상 변경, 계정 takeover, 악성 redirect | Medium | High | High | 외부 링크는 본 origin에서 실행하지 않음 | HTTPS allowlist, owner 확인, 정기 link check, embed/script 금지, 외부 링크 표기 | Medium — 외부 owner 책임 | 외부 owner/사이트 소유자 | status/redirect chain, owner 검토 | PLATFORM LIMITATION |
| T-26 | Third-Party Theme·Template 변조·라이선스 문제 | source 무결성·법적 적합성 | upstream 공격자, 무권리 배포자 | 악성 ZIP, 불명확 LICENSE, asset hotlink | Medium | High | High | 시각 참고와 코드 복사를 분리 | LICENSE·commit·hash 기록, 불명확 소스 복사 금지, 필요한 패턴을 최소 재구현 | Low/Medium | 사이트 소유자/upstream | theme audit, license notice, diff | BLOCKED |

## 현재 최우선 조치

1. 루트 repository를 생성하기 전 RESTRICTED/CONFIDENTIAL 파일이 작업 트리에
   들어오지 않도록 공개 allowlist를 확정한다.
2. repository 생성 후 branch/ruleset, account 2FA/passkey, secret scanning,
   Actions 권한을 실제 설정하고 증거를 남긴다.
3. 소스와 `_site` 검사 통과 후 Pages를 배포하고 Enforce HTTPS를 켠다.
4. HTTP redirect, HTTPS 2xx, 인증서, Mixed Content, 직접 asset URL을 공개
   환경에서 다시 검증한다.

