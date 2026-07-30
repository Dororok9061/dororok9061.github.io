# Data Classification

## 기본 원칙

- 기본 분류는 `CONFIDENTIAL`이다. 공개 승인과 sanitation이 끝난 파생본만
  `PUBLIC`으로 내린다.
- GitHub Pages, public repository, release, Actions artifact, workflow log,
  Preview URL, 직접 asset URL은 모두 공개 채널로 본다.
- 파일명 변경, robots.txt, 메뉴에서 링크 제거, 난해한 URL은 접근통제가 아니다.
- `RESTRICTED` 자료는 repository, build input, CI runner, Pages에 절대 넣지 않는다.
- 비밀이 한 번 공개되면 삭제만으로 해결하지 않고 즉시 폐기·회전하고 history,
  cache, artifact, fork 범위를 조사한다.

## 분류

| 등급 | 정의 | 예시 | 공개 저장소 | Pages 산출물 | 보관·전송 |
|---|---|---|---|---|---|
| PUBLIC | 소유권과 공개 승인이 확인된 정보 | 승인된 소개, 프로젝트 요약, 공개 repo/Notion URL, sanitized profile 파생본 | 허용 | 허용 | HTTPS, 무결성 검토 |
| INTERNAL | 공개할 필요가 없지만 유출 영향이 제한적인 운영 정보 | 체크리스트, 미완료 초안, 비민감 QA 로그 | 원칙적 금지 | 금지 | 접근 제한된 작업 폴더 |
| CONFIDENTIAL | 유출 시 개인·연구·계약·지식재산 피해 가능 | private archive, 미공개 논문/연구데이터, 원본 EDA 파일, 미승인 screenshot, 원본 사진 | 금지 | 금지 | 암호화 저장, 최소 접근, 승인된 파생본만 이동 |
| RESTRICTED | credential·license·고위험 개인정보 | API key, GitHub token, SSH/private key, 복구 코드, Quartus/EDA license, 주민정보, 원본 생체/건강 데이터 | 절대 금지 | 절대 금지 | 별도 암호화 저장, 로그 금지, 필요 시 회전·폐기 |

## 제공 자료의 분류 결정

원본의 정확한 로컬 경로·식별자는 공개 문서에 기록하지 않는다.

| 자료 유형 | 초기 분류 | 공개 가능 조건 | 현재 결정 |
|---|---|---|---|
| EDA license data | RESTRICTED | 공개 불가 | 열람·복사·commit·CI upload 금지 |
| 학부 과제·프로젝트 archive | CONFIDENTIAL | 파일별 소유권·license·개인정보 검토 후 필요한 파생본만 | 원 archive 공개 금지 |
| 공식 프로필 사진 원본 | CONFIDENTIAL | EXIF 전부 제거, 승인된 crop/resize 파생본, 얼굴 생성·변형 금지 | 파생본만 PUBLIC 가능 |
| EDA/시뮬레이션 screenshot | CONFIDENTIAL | 로컬 경로, license ID, 계정명, 비공개 값 redaction 및 공개 승인 | 검토된 이미지 파생본만 PUBLIC |
| 공개 GitHub/Notion 콘텐츠 | PUBLIC 후보 | 실제 공개 상태, 소유권, 링크 대상, 민감 데이터 재검토 | 자동 PUBLIC 간주 금지 |
| Build log·source map·artifact | INTERNAL 또는 CONFIDENTIAL | 민감정보가 없고 공개 필요가 명확한 최소 산출물만 | Pages에서 제외 |

## 저장 위치 정책

| 위치 | 허용 최고 등급 | 규칙 |
|---|---|---|
| GitHub public repository | PUBLIC | allowlist 기반, history 포함 검사 |
| GitHub Pages `_site` | PUBLIC | build 후 재검사, directory listing 여부와 무관 |
| GitHub Actions log/artifact/cache | INTERNAL | RESTRICTED 금지, artifact 보존 최소화 |
| Local 작업 사본 | CONFIDENTIAL | 디스크 암호화·자동 잠금·OS 보호·백업 |
| Private source archive | CONFIDENTIAL | public repo와 분리, read-only 원본 유지 |
| License storage | RESTRICTED | repo/workspace와 분리, 최소 권한, 발급기관 조건 준수 |

## 공개 전 Declassification

다음 조건이 모두 확인된 경우에만 `PUBLIC`으로 분류한다.

- [ ] 작성자·소유자·라이선스와 공개 권한이 확인됨
- [ ] 개인정보·건강/생체정보·연구 참가자 정보가 없음
- [ ] API key, token, password, license 문자열, 내부 URL이 없음
- [ ] 로컬 절대 경로, 사용자명, 장비 serial, 계정 ID가 없음
- [ ] 이미지 EXIF·XMP·thumbnail·편집 이력이 제거됨
- [ ] screenshot의 창 제목·최근 파일·license 정보가 검토됨
- [ ] source map, debug file, 원본 archive가 빌드에 포함되지 않음
- [ ] 직접 asset URL로 열어도 공개해도 되는 내용임
- [ ] 영문·국문 설명이 과장 없이 공개 근거와 일치함
- [ ] `scripts/security/verify-site-security.ps1` 소스·빌드 검사가 통과함

확인할 수 없는 항목은 PASS가 아니라 `BLOCKED`로 기록한다.

## 사고 대응

1. 해당 Pages 배포와 공개 링크를 중단하되 증거를 보존한다.
2. credential/license라면 먼저 발급기관 절차에 따라 폐기·회전한다.
3. default branch뿐 아니라 Git history, tag, release, artifact, cache, fork,
   Preview와 CDN cache 범위를 조사한다.
4. 공개된 개인정보·연구데이터의 owner와 필요한 당사자에게 통지한다.
5. 원인과 통제 실패를 Threat Model과 Attack Surface Register에 반영한다.

