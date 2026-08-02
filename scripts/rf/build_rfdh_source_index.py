#!/usr/bin/env python3
"""Turn the private RFDH crawl inventory into source and coverage indexes."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "work" / "rfdh-study"
DATA = ROOT / "src" / "_data"
DOCS = ROOT / "docs" / "internal"

TOPICS = {
    "foundations": {
        "question": "RF 회로를 분포정수 관점으로 바꾸어 읽어야 하는 조건은 무엇인가?",
        "terms": ["RF", "electrical length", "Maxwell equations", "resonance"],
        "equations": ["lambda = v_p / f", "theta = beta l"],
        "coursework": ["high-frequency-engineering/distributed-circuits"],
        "blog": ["/blog/rf/foundations/"],
    },
    "impedance-matching": {
        "question": "기준 임피던스, 포트, 부하 정합은 전력 전달과 반사를 어떻게 연결하는가?",
        "terms": ["50 ohm", "port", "impedance", "matching"],
        "equations": ["Gamma = (Z_L - Z_0) / (Z_L + Z_0)", "Z_t = sqrt(Z_0 Z_L)"],
        "coursework": ["high-frequency-engineering/impedance-matching"],
        "blog": ["/blog/rf/impedance-port-matching/"],
    },
    "transmission-lines": {
        "question": "전송선 구조와 유효 유전율이 특성 임피던스와 전기적 길이를 어떻게 바꾸는가?",
        "terms": ["transmission line", "microstrip", "CPW", "waveguide"],
        "equations": ["Z_0 = sqrt(L prime / C prime)", "gamma = alpha + j beta"],
        "coursework": ["high-frequency-engineering/transmission-lines", "high-frequency-engineering/microstrip"],
        "blog": ["/blog/rf/transmission-lines/"],
    },
    "reflection-vswr": {
        "question": "반사계수, return loss, VSWR을 같은 mismatch에서 어떻게 변환하는가?",
        "terms": ["reflection coefficient", "return loss", "VSWR", "standing wave"],
        "equations": ["VSWR = (1 + abs(Gamma)) / (1 - abs(Gamma))", "RL = -20 log10(abs(Gamma))"],
        "coursework": ["high-frequency-engineering/reflection-vswr"],
        "blog": ["/blog/rf/reflection-vswr/"],
    },
    "s-parameters": {
        "question": "다중 포트에서 입사파와 반사파를 S-parameter로 어떻게 해석하는가?",
        "terms": ["S11", "S21", "S31", "reference impedance"],
        "equations": ["b = S a", "IL = -20 log10(abs(S21))"],
        "coursework": ["high-frequency-engineering/s-parameters", "high-frequency-engineering/cadence-workflow"],
        "blog": ["/blog/rf/s-parameters-vna/"],
    },
    "power-db": {
        "question": "dB의 비와 dBm의 절대 전력을 혼동하지 않고 계산하려면 무엇을 확인해야 하는가?",
        "terms": ["dB", "dBm", "watt", "power ratio"],
        "equations": ["P_dBm = 10 log10(P_mW)", "P_mW = 10^(P_dBm / 10)"],
        "coursework": ["high-frequency-engineering/s-parameters"],
        "blog": ["/blog/rf/db-dbm-power/"],
    },
    "smith-chart": {
        "question": "정규화 임피던스와 전송선 회전을 Smith chart에서 어떻게 추적하는가?",
        "terms": ["Smith chart", "normalized impedance", "admittance", "stub matching"],
        "equations": ["z = Z_L / Z_0", "Gamma = (z - 1) / (z + 1)"],
        "coursework": ["high-frequency-engineering/smith-chart", "high-frequency-engineering/l-network-stub"],
        "blog": ["/blog/rf/smith-chart/"],
    },
    "linearity": {
        "question": "P1dB, IMD, IP3가 대신호 비선형성을 각각 어떤 관점에서 나타내는가?",
        "terms": ["P1dB", "IP3", "IMD", "harmonic"],
        "equations": ["y = a1 x + a2 x^2 + a3 x^3", "OIP3 = P_out + Delta_IM3 / 2"],
        "coursework": ["electronic-circuits-2/frequency-response"],
        "blog": ["/blog/rf/linearity-p1db-ip3/"],
    },
    "circuit-blocks": {
        "question": "송수신 체인의 각 RF block은 주파수, 이득, 잡음, 격리를 어떻게 나누어 맡는가?",
        "terms": ["amplifier", "oscillator", "PLL", "mixer", "filter", "coupler"],
        "equations": ["f_IF = abs(f_RF - f_LO)", "G_total_dB = sum(G_i_dB)"],
        "coursework": ["high-frequency-engineering/wilkinson-divider", "high-frequency-engineering/branch-line-hybrid"],
        "blog": ["/blog/rf/circuit-blocks/"],
    },
    "instrumentation": {
        "question": "VNA calibration, reference plane, sweep 조건을 함께 기록해야 하는 이유는 무엇인가?",
        "terms": ["VNA", "calibration", "reference plane", "frequency sweep"],
        "equations": ["S11 = b1 / a1 at a2 = 0", "S21 = b2 / a1 at a2 = 0"],
        "coursework": ["high-frequency-engineering/cadence-workflow", "high-frequency-engineering/result-interpretation"],
        "blog": ["/blog/rf/measurement-vna/"],
    },
    "wireless-communications": {
        "question": "baseband 신호, 변조, 채널, 잡음, BER을 하나의 link로 어떻게 연결하는가?",
        "terms": ["I/Q", "modulation", "channel", "SNR", "BER"],
        "equations": ["SNR_dB = 10 log10(P_s / P_n)", "R_s = R_b / log2(M)"],
        "coursework": ["digital-communications"],
        "blog": ["/blog/rf/wireless-communications/"],
    },
    "rf-reference": {
        "question": "재료와 표준 치수를 설계 입력으로 사용할 때 어떤 조건과 출처를 함께 기록해야 하는가?",
        "terms": ["permittivity", "conductivity", "permeability", "standard dimensions"],
        "equations": ["v_p = c / sqrt(epsilon_r)", "delta = sqrt(2 / (omega mu sigma))"],
        "coursework": ["high-frequency-engineering/microstrip"],
        "blog": ["/blog/rf/transmission-lines/"],
    },
}


def clean_topic(row: dict[str, str]) -> str:
    url, title = row["url"].lower(), row["title"].lower()
    if any(part in url for part in ("50ohm", "whyport", "whymatch")):
        return "impedance-matching"
    if any(part in url for part in ("vswr",)):
        return "reflection-vswr"
    if any(part in url for part in ("ip3", "acpr", "uplin", "linear", "harmonic", "/im.htm")):
        return "linearity"
    if any(part in url for part in ("smith", "complex")):
        return "smith-chart"
    if any(part in url for part in ("amp.htm", "osc.htm", "pll", "mixer", "multiplier", "filter.php3", "duplexer", "coupler", "isolator", "antenna")):
        return "circuit-blocks"
    if "/bas_com/" in url:
        return "wireless-communications"
    if any(part in url for part in ("network.htm", "hpib")):
        return "instrumentation"
    if any(part in url for part in ("/s.htm", "whys")) or "s파라" in title:
        return "s-parameters"
    if any(part in url for part in ("whydb", "dbdbm", "dbmw", "pae", "largesmall")):
        return "power-db"
    if any(part in url for part in ("trans_", "microstrip", "msline", "sline", "coaxline", "slotline", "cpw", "cps", "/wg.htm", "skin", "mode.htm", "emwave", "ms_make")):
        return "transmission-lines"
    if any(part in url for part in ("whatisrf", "start.htm", "curi.htm", "maxwell", "act_pass", "/imp.htm", "reso")):
        return "foundations"
    if row["topic"] in TOPICS:
        return row["topic"]
    return "rf-reference"


def page_id(url: str) -> str:
    path = urlsplit(url).path.strip("/") or "home"
    value = re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")
    return value or "home"


def q(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def public_related(urls: list[str]) -> list[str]:
    denied = ("/admin", "/member", "/login", "/market", "/qna", "/board", "/bbs")
    return [url for url in urls if not any(part in url.lower() for part in denied)][:8]


def yaml_list(values: list[str], indent: int) -> list[str]:
    return [(" " * indent) + f"- {q(value)}" for value in values]


def main() -> int:
    with (WORK / "rfdh-pages.csv").open(encoding="utf-8-sig") as handle:
        pages = list(csv.DictReader(handle))
    edges = json.loads((WORK / "rfdh-link-graph.json").read_text(encoding="utf-8"))
    with (WORK / "rfdh-images.csv").open(encoding="utf-8-sig") as handle:
        images = list(csv.DictReader(handle))
    with (WORK / "rfdh-calculators.csv").open(encoding="utf-8-sig") as handle:
        calculators = list(csv.DictReader(handle))

    outgoing: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge["target"] not in outgoing[edge["source"]]:
            outgoing[edge["source"]].append(edge["target"])
    image_counts = Counter(item["page_url"] for item in images)
    calculator_urls = {item["page_url"] for item in calculators}
    seen_ids: set[str] = set()
    records: list[dict[str, object]] = []
    topic_members: dict[str, list[str]] = defaultdict(list)

    for order, row in enumerate(pages, 1):
        topic = clean_topic(row)
        meta = TOPICS[topic]
        identifier = page_id(row["url"])
        if identifier in seen_ids:
            identifier = f"{identifier}-{order}"
        seen_ids.add(identifier)
        record = {
            "id": identifier,
            "title": row["title"],
            "url": row["url"],
            "section": topic,
            "subsection": Path(urlsplit(row["url"]).path).stem,
            "order": order,
            "main_questions": [meta["question"]],
            "key_terms": meta["terms"],
            "equations": meta["equations"],
            "figures": int(image_counts[row["url"]]),
            "examples": ["interactive reference page"] if row["url"] in calculator_urls else ["worked explanation in source page"],
            "related_rfdh_pages": public_related(outgoing[row["url"]]),
            "related_coursework": meta["coursework"],
            "related_projects": ["fmcw-radar"] if topic in {"wireless-communications", "circuit-blocks", "s-parameters"} else [],
            "related_blog_ko": meta["blog"],
            "related_blog_en": [value.replace("/blog/", "/en/blog/") for value in meta["blog"]],
            "notion_page": "",
            "github_asset": "",
            "status": "indexed",
            "last_reviewed": str(date.today()),
        }
        records.append(record)
        topic_members[topic].append(identifier)

    DATA.mkdir(parents=True, exist_ok=True)
    lines = [
        f"source_name: {q('RFDH — RF Design House')}",
        f"source_url: {q('https://rfdh.com/')}",
        f"last_reviewed: {q(str(date.today()))}",
        "public_learning_pages_only: true",
        "pages:",
    ]
    for record in records:
        lines.extend([
            f"  - id: {q(record['id'])}",
            f"    title: {q(record['title'])}",
            f"    url: {q(record['url'])}",
            f"    section: {q(record['section'])}",
            f"    subsection: {q(record['subsection'])}",
            f"    order: {record['order']}",
            "    main_questions:",
            *yaml_list(record["main_questions"], 6),
            "    key_terms:",
            *yaml_list(record["key_terms"], 6),
            "    equations:",
            *yaml_list(record["equations"], 6),
            f"    figures: {record['figures']}",
            "    examples:",
            *yaml_list(record["examples"], 6),
            "    related_rfdh_pages:",
            *(yaml_list(record["related_rfdh_pages"], 6) or ["      []"]),
            "    related_coursework:",
            *yaml_list(record["related_coursework"], 6),
            "    related_projects:",
            *(yaml_list(record["related_projects"], 6) or ["      []"]),
            "    related_blog_ko:",
            *yaml_list(record["related_blog_ko"], 6),
            "    related_blog_en:",
            *yaml_list(record["related_blog_en"], 6),
            f"    notion_page: {q(record['notion_page'])}",
            f"    github_asset: {q(record['github_asset'])}",
            f"    status: {q(record['status'])}",
            f"    last_reviewed: {q(record['last_reviewed'])}",
        ])
    (DATA / "rfdh_source_index.yml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    topic_lines = ["topics:"]
    for topic, meta in TOPICS.items():
        topic_lines.extend([
            f"  - id: {q(topic)}",
            f"    source_count: {len(topic_members[topic])}",
            "    main_questions:",
            f"      - {q(meta['question'])}",
            "    source_ids:",
            *yaml_list(topic_members[topic], 6),
            "    blog_ko:",
            *yaml_list(meta["blog"], 6),
            "    blog_en:",
            *yaml_list([value.replace('/blog/', '/en/blog/') for value in meta["blog"]], 6),
        ])
    (WORK / "topic-map.yml").write_text("\n".join(topic_lines) + "\n", encoding="utf-8")

    DOCS.mkdir(parents=True, exist_ok=True)
    coverage_fields = ["id", "title", "url", "section", "status", "related_coursework", "related_blog_ko", "last_reviewed"]
    with (DOCS / "RFDH_TOPIC_COVERAGE.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=coverage_fields)
        writer.writeheader()
        for record in records:
            writer.writerow({
                **{key: record[key] for key in coverage_fields if key not in {"related_coursework", "related_blog_ko"}},
                "related_coursework": " | ".join(record["related_coursework"]),
                "related_blog_ko": " | ".join(record["related_blog_ko"]),
            })
    counts = Counter(record["section"] for record in records)
    report = [
        "# RFDH public RF-study source map",
        "",
        f"Reviewed {len(records)} public learning pages on {date.today()}. Raw legacy HTML stays in the D:-resident private cache.",
        "Account, community, market, Q&A, login, and administrative paths are outside the crawl scope.",
        "",
        "| Topic | Pages | Public study route |",
        "|---|---:|---|",
    ]
    for topic, meta in TOPICS.items():
        report.append(f"| {topic} | {counts[topic]} | {meta['blog'][0]} |")
    report.extend([
        "",
        "The public articles paraphrase concepts, recompute examples, and link the original source URL. RFDH images and prose are not republished in bulk.",
        "Interactive values from RFDH are treated as references, not as measurements from the author's hardware.",
    ])
    (DOCS / "RFDH_SOURCE_MAP.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(records), "topics": dict(counts)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
