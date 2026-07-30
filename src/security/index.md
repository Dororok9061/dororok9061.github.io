---
layout: page
title: 보안·데이터 보호
eyebrow: Security
lead: 정적 사이트의 책임 범위, 적용된 통제와 플랫폼 제한을 공개합니다.
description: Engineering Portfolio의 위협 모델, 데이터 분류, 공급망 및 배포 보안 요약.
permalink: /security/
lang: ko
alternate_url: /en/security/
alternate_lang: en
---

## 적용된 구조

- Jekyll 4가 build하는 정적 HTML·CSS와 최소 Vanilla JavaScript
- 서버 DB, 로그인, 결제, 업로드, 댓글, 자체 Contact backend 없음
- `jekyll-theme-simplex 0.9.8.15`와 build dependency를 `Gemfile.lock`으로 고정
- GitHub-maintained Action을 full commit SHA로 고정
- source와 build에 대한 credential·license·개인정보·source map 검사

## 남는 제한

- GitHub Pages에서 임의의 `X-Frame-Options` 또는 CSP `frame-ancestors` 응답 헤더를 설정할 수 없어 Clickjacking header 통제는 **PLATFORM LIMITATION**입니다.
- GitHub 계정의 2FA/passkey와 로컬 PC의 디스크 암호화·자동 잠금은 사이트 build가 검증할 수 없어 **BLOCKED**입니다.
- DDoS edge 방어는 GitHub의 책임 범위이며 완전 차단을 보장하지 않습니다.

상세 문서는 [repository security directory](https://github.com/Tontonjeong/Tontonjeong.github.io/tree/main/docs/security)에서 확인할 수 있습니다.
