#!/usr/bin/env python3
import math

def close(actual, expected, tolerance=1e-3):
    if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
        raise AssertionError(f"{actual} != {expected}")

close(10 ** ((20 - 30) / 10), 0.1)
gamma = abs((100 - 50) / (100 + 50))
close(gamma, 1 / 3)
close((1 + gamma) / (1 - gamma), 2)
close(-20 * math.log10(gamma), 9.542425)
close(math.sqrt(50 * 100), 70.710678)
f1, f2, g1 = 10 ** (2 / 10), 10 ** (8 / 10), 10 ** (15 / 10)
close(10 * math.log10(f1 + (f2 - 1) / g1), 2.437315)
close(10 * math.log10(2), 3.0103)
k = math.sqrt(1)
close(50 * math.sqrt(k * (1 + k * k)), 70.710678)
close(50 * (k + 1 / k), 100)
print("RF formula tests: PASS (dBm, reflection, transformer, NF, split, Wilkinson)")
