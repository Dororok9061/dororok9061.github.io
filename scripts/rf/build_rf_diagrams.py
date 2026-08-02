#!/usr/bin/env python3
"""Build small, original SVG study diagrams used by the RF article pages."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "src" / "assets" / "images" / "study" / "rf-rfdh"

DIAGRAMS = {
    "foundations/distributed-wave.svg": ("전기적 길이", "회로 크기와 파장이 가까워지면 전압과 전류를 위치 함수로 본다.", ["Source", "Forward wave", "Load", "Reflected wave"]),
    "impedance/impedance-chain.svg": ("50 Ω 신호 경로", "source, line, port, load의 기준 임피던스를 한 줄로 비교한다.", ["50 Ω source", "50 Ω port", "Z₀ line", "ZL load"]),
    "impedance/reflection-relations.svg": ("반사 관계", "부하 mismatch에서 반사계수, return loss, VSWR로 이어지는 관계.", ["ZL and Z₀", "Γ", "Return loss", "VSWR"]),
    "sparameters/s-matrix.svg": ("S-parameter 행렬", "입사파 a와 반사파 b를 다중 포트 산란행렬로 연결한다.", ["Incident a₁,a₂", "S matrix", "Reflected b₁,b₂", "S11 · S21"]),
    "power-db/db-power-scale.svg": ("dBm 전력 눈금", "전력이 열 배가 될 때 dBm이 10 dB씩 증가한다.", ["1 mW\n0 dBm", "10 mW\n10 dBm", "100 mW\n20 dBm", "1 W\n30 dBm"]),
    "smith-chart/smith-coordinates.svg": ("Smith chart 좌표", "정규화 임피던스와 반사계수 평면을 같은 원 안에서 읽는다.", ["Normalize z", "Map to Γ", "r/x circles", "Read magnitude"]),
    "smith-chart/smith-movement.svg": ("Smith chart 이동", "series, shunt, transmission-line 이동을 서로 다른 단계로 표시한다.", ["Load zL", "Series reactance", "Admittance y", "Line rotation"]),
    "matching/quarter-wave.svg": ("Quarter-wave transformer", "두 실수 임피던스 사이에 √(Z₀ZL) 선로를 λg/4만큼 둔다.", ["Z₀", "Zt=√Z₀ZL", "λg/4", "ZL"]),
    "linearity/p1db-ip3.svg": ("P1dB와 IP3", "fundamental 출력의 compression과 IM3 외삽 교점을 분리해서 읽는다.", ["Small signal", "1 dB compression", "Fundamental", "IM3 extrapolation"]),
    "circuit-blocks/noise-cascade.svg": ("Cascaded noise figure", "첫 단의 gain이 뒤 단 noise contribution을 나누는 흐름.", ["F₁,G₁", "F₂/G₁", "F₃/(G₁G₂)", "Ftotal"]),
    "circuit-blocks/rf-block-chain.svg": ("RF 송수신 block", "baseband에서 antenna까지 주파수와 신호 수준이 바뀌는 경로.", ["Baseband", "Mixer + LO", "PA / LNA", "Antenna"]),
    "circuit-blocks/pll-loop.svg": ("PLL feedback loop", "reference와 divided VCO phase를 비교해 VCO를 제어한다.", ["Reference", "Phase detector", "Loop filter", "VCO ÷N"]),
    "circuit-blocks/mixer-spectrum.svg": ("Mixer frequency translation", "RF와 LO 곱에서 sum과 difference 성분이 생긴다.", ["RF fRF", "LO fLO", "Nonlinear product", "fRF±fLO"]),
    "circuit-blocks/coupler-divider.svg": ("Coupler와 divider", "through, coupled, isolated port와 equal split을 구분한다.", ["Input", "Through", "Coupled / split", "Isolated"]),
    "circuit-blocks/isolator-circulator.svg": ("Isolator와 circulator", "비가역 port 흐름을 화살표 방향으로 읽는다.", ["Port 1", "Port 2", "Port 3", "Termination"]),
    "instrumentation/vna-reference-plane.svg": ("VNA reference plane", "calibration plane부터 DUT port까지 남는 fixture 영향을 표시한다.", ["VNA", "Calibration plane", "Fixture", "DUT"]),
    "wireless-communications/tx-rx-chain.svg": ("통신 link", "source coding부터 channel과 receiver decision까지 이어지는 기본 경로.", ["Bits / I-Q", "Modulator", "Channel + noise", "Demod + BER"]),
}


def diagram(title: str, description: str, labels: list[str]) -> str:
    boxes = []
    arrows = []
    for index, label in enumerate(labels):
        x = 70 + index * 280
        lines = label.split("\n")
        text = "".join(
            f'<tspan x="{x + 110}" dy="{0 if line_index == 0 else 28}">{escape(line)}</tspan>'
            for line_index, line in enumerate(lines)
        )
        boxes.append(
            f'<rect x="{x}" y="245" width="220" height="140" rx="18" class="box"/>'
            f'<text x="{x + 110}" y="{310 - 14 * (len(lines) - 1)}" class="label">{text}</text>'
        )
        if index < len(labels) - 1:
            x1, x2 = x + 220, x + 280
            arrows.append(f'<path d="M{x1} 315 H{x2}" class="arrow" marker-end="url(#arrow)"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="#1d6fa5"/></marker></defs>
  <style>.bg{{fill:#f7fafc}}.box{{fill:#fff;stroke:#1d6fa5;stroke-width:3}}.arrow{{stroke:#1d6fa5;stroke-width:4;fill:none}}.label{{font:700 22px system-ui,sans-serif;text-anchor:middle;fill:#13293d}}.heading{{font:700 34px system-ui,sans-serif;fill:#13293d}}.caption{{font:20px system-ui,sans-serif;fill:#334e68}}</style>
  <rect width="1200" height="630" rx="24" class="bg"/>
  <text x="70" y="88" class="heading">{escape(title)}</text>
  <text x="70" y="130" class="caption">{escape(description)}</text>
  {''.join(arrows)}
  {''.join(boxes)}
</svg>'''


def main() -> None:
    for relative, values in DIAGRAMS.items():
        path = OUT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(diagram(*values), encoding="utf-8")
    print(f"wrote {len(DIAGRAMS)} RF study diagrams under {OUT}")


if __name__ == "__main__":
    main()
