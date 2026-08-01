---
title: Raspberry Pi 두 대로 구성한 졸음 모니터의 sensor-to-alarm data path
title_en: Sensor-to-alarm data path in a two-node Raspberry Pi drowsiness monitor
description: PPG sensing node, Camera/EAR analysis node, TCP/IP, file IPC, GPIO, I2C LCD와 alarm 경계를 실제 prototype으로 정리한 기록.
date: 2026-07-31 00:40:00 +0900
updated: 2026-08-01 18:30:00 +0900
study_date: 2026-07-31
lang: ko
translation_key: embedded-data-path
permalink: /blog/2026/07/31/embedded-data-path/
alternate_url: /en/blog/2026/07/31/embedded-data-path/
alternate_lang: en
primary_category: major-foundations
subcategory: embedded-systems
series: embedded-integration
series_order: 1
post_type: project-log
difficulty: intermediate
study_status: published
evidence_status: SOURCE_AND_PROTOTYPE
tools: [C, C++, OpenCV, TCP/IP, GPIO, I2C]
hardware: [Raspberry Pi, PPG sensor, camera, LCD, LED, buzzer]
software_versions: [not fully preserved]
source_materials:
  - { title: Sleep Monitoring and Prevention Device, type: public-repository, public_url: https://github.com/Tontonjeong/Sleep-monitoring-and-prevention-device, file_reference: C and C++ source, pages: "", used_for: module and data-path inventory }
  - { title: Drowsiness Monitor project page, type: portfolio-page, public_url: /projects/drowsiness-monitor/, file_reference: project photographs and source, pages: "", used_for: architecture and next tests }
prerequisites: [tcp-ip, gpio, i2c, basic image processing]
learning_objectives: [두 node의 역할 분리, packet과 file IPC 경계 기록, 사진 근거와 성능 측정 구분]
related_projects: [drowsiness-monitor]
related_posts: []
tags: [embedded-systems, tcp-ip, raspberry-pi, i2c]
cover_image: /assets/images/projects/embedded-prototype.webp
thumbnail: /assets/images/projects/embedded-prototype.webp
image_alt: Raspberry Pi, LCD와 sensor wiring으로 구성한 졸음 모니터링 prototype
draft: false
revision_history:
  - { date: 2026-07-31, change: 최초 공개 }
  - { date: 2026-08-01, change: "node 역할, data path, failure boundary와 prototype 사진 추가" }
toc:
  - { id: goal, title: 두 Node로 나눈 이유 }
  - { id: nodes, title: PPG Node와 Camera Node }
  - { id: path, title: Packet·File·GPIO·I2C 경로 }
  - { id: prototype, title: 실제 Prototype에서 확인한 것 }
  - { id: failures, title: 실패처리와 미측정 항목 }
  - { id: next, title: 다음 검증 }
---

## 두 Node로 나눈 이유 {#goal}

PPG 신호 취득과 camera 기반 EAR 계산은 입력 주기와 처리 부하가 다르다. 한 Raspberry Pi에서 모두 처리하면 camera frame 처리 지연이 PPG 읽기와 alarm timing에 영향을 줄 수 있다. 이 prototype은 sensing과 analysis를 두 node로 나누고 네트워크와 file IPC로 상태를 전달한다.

이 분리는 성능 향상을 자동으로 보장하지 않는다. 대신 각 node가 맡은 입력, 저장 파일, packet, output을 따로 추적할 수 있게 한다.

## PPG Node와 Camera Node {#nodes}

**PPG sensing node**는 sensor sample을 읽고 heart-related 값과 상태를 만든다. **Camera/EAR node**는 frame에서 눈 영역을 처리하고 EAR 기반 상태를 계산한다. 공개 C/C++ source와 architecture 문서가 두 경로의 존재를 지원한다.

통합 판단은 PPG 값과 vision 상태가 전달된 뒤 alarm 조건을 조합하는 단계에서 이뤄진다. 사진만으로 알고리즘 threshold나 정확도를 복원할 수 없으므로 source에서 확인되는 모듈 경계와 prototype 배선 근거를 분리한다.

<figure><picture><source srcset="/assets/images/projects/embedded-prototype.webp" type="image/webp"><img src="/assets/images/projects/embedded-prototype.jpg" alt="Raspberry Pi 두 대, LCD, sensor wiring으로 조립된 졸음 모니터 prototype" width="984" height="560" loading="lazy"></picture><figcaption>실제 조립과 LCD·sensor 연결은 확인되지만 latency나 detection accuracy 측정은 아니다.</figcaption></figure>

## Packet·File·GPIO·I2C 경로 {#path}

```text
PPG sensor → sensing process → TCP/IP or shared file state
camera → frame processing → EAR state
PPG state + EAR state → decision path
decision → GPIO LED/buzzer + I2C LCD
```

TCP/IP 경계에는 sender/receiver address, message length, reconnect 정책이 필요하다. File IPC는 producer가 쓰는 중 consumer가 읽지 않도록 임시 파일과 atomic rename 또는 명시적 ready flag가 필요하다. GPIO는 LED·buzzer의 active level, I2C는 LCD address와 update 실패 처리까지 기록해야 재현할 수 있다.

공개 자료는 network, file IPC, GPIO, I2C라는 경로를 확인시켜 주지만 모든 packet schema와 timeout 값을 완전하게 보존하지는 않는다. 그래서 packet loss 복구나 stale file 제거가 구현됐다고 추가로 주장하지 않는다.

## 실제 Prototype에서 확인한 것 {#prototype}

<figure><picture><source srcset="/assets/images/projects/drowsiness-contact-sheet.webp" type="image/webp"><img src="/assets/images/projects/drowsiness-contact-sheet.jpg" alt="졸음 모니터의 Raspberry Pi, LCD, sensor wiring과 공개 source 화면을 모은 contact sheet" width="780" height="1100" loading="lazy"></picture><figcaption>공개 source와 실제 prototype 사진을 한 화면에서 비교한 contact sheet.</figcaption></figure>

사진에서 Raspberry Pi, LCD, sensor 배선과 조립 상태를 확인했다. Repository의 PPG server와 image/EAR processing module을 함께 읽으니 두 node의 data path가 실제 prototype에서 어떻게 이어지는지 보였다. 화면에 보이는 값은 calibration 조건을 알 수 없어 정량 성능표에는 넣지 않았다.

## 실패처리와 미측정 항목 {#failures}

분산된 두 node에서 필요한 실패처리는 camera frame 누락, TCP 연결 끊김, 오래된 file state, I2C write 실패, sensor read timeout이다. 현재 공개 자료만으로 각 실패가 어떤 retry와 fallback을 거치는지 모두 검증할 수 없다.

end-to-end latency, sensitivity, specificity, false-alarm rate와 장시간 안정성의 저장된 측정값은 찾지 못했다. 그래서 이 수치들은 실제 성능 결과처럼 쓰지 않았다.

## 다음 검증 {#next}

다음 단계는 message schema와 monotonic timestamp를 고정하고, 각 node에서 동일 event ID를 log하는 것이다. 의도적으로 network를 끊거나 camera 입력을 중단해 alarm path가 안전한 상태로 이동하는지도 확인해야 한다. 그 전까지 prototype 존재와 성능 주장을 분리한다.
