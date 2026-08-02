(() => {
  "use strict";

  const finite = (form, name, min = -Infinity, max = Infinity) => {
    const value = Number(form.elements[name].value);
    if (!Number.isFinite(value) || value < min || value > max) {
      throw new Error(`${name}: 범위 안의 숫자를 입력하세요.`);
    }
    return value;
  };
  const fixed = (value, digits = 4) => Number(value).toLocaleString("ko-KR", { maximumFractionDigits: digits });
  const dbToLinear = (value) => 10 ** (value / 10);
  const linearToDb = (value) => 10 * Math.log10(value);

  const calculators = {
    "dbm-watt": (form) => {
      const dbm = finite(form, "dbm", -300, 300);
      const watt = finite(form, "watt", Number.MIN_VALUE, 1e24);
      const fromDbm = 10 ** ((dbm - 30) / 10);
      const fromWatt = 10 * Math.log10(watt * 1000);
      return `${fixed(dbm)} dBm = ${fixed(fromDbm, 9)} W\n${fixed(watt, 9)} W = ${fixed(fromWatt)} dBm`;
    },
    "reflection-vswr": (form) => {
      const z0 = finite(form, "z0", Number.MIN_VALUE, 1e9);
      const r = finite(form, "rl", -1e9, 1e9);
      const x = finite(form, "xl", -1e9, 1e9);
      const denominator = (r + z0) ** 2 + x ** 2;
      if (denominator === 0) throw new Error("ZL + Z0가 0이 될 수 없습니다.");
      const gr = (r * r + x * x - z0 * z0) / denominator;
      const gi = (2 * z0 * x) / denominator;
      const magnitude = Math.hypot(gr, gi);
      const phase = Math.atan2(gi, gr) * 180 / Math.PI;
      const rl = magnitude === 0 ? Infinity : -20 * Math.log10(magnitude);
      const vswr = magnitude >= 1 ? Infinity : (1 + magnitude) / (1 - magnitude);
      const mismatch = magnitude >= 1 ? NaN : -10 * Math.log10(1 - magnitude ** 2);
      return `Γ = ${fixed(gr)} ${gi < 0 ? "−" : "+"} j${fixed(Math.abs(gi))}\n|Γ| = ${fixed(magnitude)}, ∠Γ = ${fixed(phase, 2)}°\nReturn loss = ${Number.isFinite(rl) ? fixed(rl) + " dB" : "∞ dB"}\nVSWR = ${Number.isFinite(vswr) ? fixed(vswr) : "∞"}\nMismatch loss = ${Number.isFinite(mismatch) ? fixed(mismatch) + " dB" : "정의 범위 밖"}`;
    },
    "quarter-wave-transformer": (form) => {
      const z0 = finite(form, "z0", Number.MIN_VALUE, 1e9);
      const zl = finite(form, "zl", Number.MIN_VALUE, 1e9);
      const freq = finite(form, "freq", Number.MIN_VALUE, 1e6) * 1e9;
      const eeff = finite(form, "eeff", 1, 1e6);
      const zt = Math.sqrt(z0 * zl);
      const lambdaG = 299792458 / (freq * Math.sqrt(eeff));
      return `Transformer Zt = ${fixed(zt)} Ω\nGuided wavelength = ${fixed(lambdaG * 1000)} mm\nQuarter-wave length = ${fixed(lambdaG * 250)} mm`;
    },
    "cascade-noise-figure": (form) => {
      const gains = [1, 2, 3].map((n) => dbToLinear(finite(form, `g${n}`, -200, 200)));
      const factors = [1, 2, 3].map((n) => dbToLinear(finite(form, `nf${n}`, 0, 200)));
      const total = factors[0] + (factors[1] - 1) / gains[0] + (factors[2] - 1) / (gains[0] * gains[1]);
      return `Total noise factor = ${fixed(total, 6)}\nTotal noise figure = ${fixed(linearToDb(total))} dB\nTotal gain = ${fixed(linearToDb(gains[0] * gains[1] * gains[2]))} dB`;
    },
    "microstrip": (form) => {
      const er = finite(form, "er", 1.000001, 1000);
      const h = finite(form, "h", Number.MIN_VALUE, 1e6);
      const w = finite(form, "w", Number.MIN_VALUE, 1e6);
      const freq = finite(form, "freq", Number.MIN_VALUE, 1e6) * 1e9;
      const u = w / h;
      const correction = u < 1 ? 0.04 * (1 - u) ** 2 : 0;
      const eeff = (er + 1) / 2 + (er - 1) / 2 * (1 / Math.sqrt(1 + 12 / u) + correction);
      const z0 = u <= 1
        ? 60 / Math.sqrt(eeff) * Math.log(8 / u + u / 4)
        : 120 * Math.PI / (Math.sqrt(eeff) * (u + 1.393 + 0.667 * Math.log(u + 1.444)));
      const lambdaG = 299792458 / (freq * Math.sqrt(eeff));
      return `W/h = ${fixed(u)}\nEffective εr ≈ ${fixed(eeff)}\nCharacteristic impedance ≈ ${fixed(z0)} Ω\nGuided wavelength ≈ ${fixed(lambdaG * 1000)} mm\n90° length ≈ ${fixed(lambdaG * 250)} mm`;
    },
    "equal-split": (form) => {
      const pin = finite(form, "pin", -300, 300);
      const outputs = finite(form, "outputs", 2, 64);
      if (!Number.isInteger(outputs)) throw new Error("outputs는 정수여야 합니다.");
      const extraLoss = finite(form, "loss", 0, 300);
      const idealLoss = 10 * Math.log10(outputs);
      const pout = pin - idealLoss - extraLoss;
      return `Ideal split loss/output = ${fixed(idealLoss)} dB\nOutput power/output = ${fixed(pout)} dBm\nOutput power/output = ${fixed(10 ** ((pout - 30) / 10), 9)} W`;
    },
    "unequal-wilkinson": (form) => {
      const z0 = finite(form, "z0", Number.MIN_VALUE, 1e9);
      const powerRatio = finite(form, "ratio", Number.MIN_VALUE, 1e9);
      const k = Math.sqrt(powerRatio);
      const z2 = z0 * Math.sqrt(k * (1 + k * k));
      const z3 = z0 * Math.sqrt((1 + k * k) / (k ** 3));
      const resistor = z0 * (k + 1 / k);
      const p2Fraction = powerRatio / (1 + powerRatio);
      return `K = sqrt(P2/P3) = ${fixed(k)}\nPort-2 arm Z02 = ${fixed(z2)} Ω\nPort-3 arm Z03 = ${fixed(z3)} Ω\nIsolation resistor R = ${fixed(resistor)} Ω\nIdeal power fractions: P2=${fixed(100 * p2Fraction, 2)}%, P3=${fixed(100 * (1 - p2Fraction), 2)}%`;
    }
  };

  document.querySelectorAll("[data-rf-calculator]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const output = form.querySelector("output");
      try {
        output.textContent = calculators[form.dataset.rfCalculator](form);
        output.dataset.state = "ok";
      } catch (error) {
        output.textContent = error.message;
        output.dataset.state = "error";
      }
    });
  });
})();
