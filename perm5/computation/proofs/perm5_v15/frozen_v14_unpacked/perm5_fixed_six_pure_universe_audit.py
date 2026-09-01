#!/usr/bin/env python3
"""Independent integer audit for section 42.1 of the pure perm5 route.

The mathematical proof is the Petersen fibre recurrence and the two-sided
Koszul inequality written in the paper.  This script only checks the small
integer tables, the exclusion margins, and the resulting 58-state universe.
It reads no shifted-ideal, SAT/DRAT, frontier, or orbit certificate.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "n5_fixed_six_pure_universe_audit_exact.json"

H = (10, 7, 5, 4, 4, 2, 1, 1, 0, 0, 0)
D = tuple(H[t - 1] - H[t] for t in range(1, 11))
P_UPPER = (0, 1, 4, 5, 8, 11, 20, 24, 28)


@lru_cache(maxsize=None)
def tail(layer: int, remaining: int, cap: int) -> int:
    if layer == 10:
        return 0 if remaining == 0 else -10**9
    return max(
        D[layer] * H[value] + tail(layer + 1, remaining - value, value)
        for value in range(min(cap, remaining) + 1)
    )


def shadow_lower(size: int) -> int:
    if size == 0:
        return 0
    complement_upper = max(
        D[0] * H[first] + tail(1, size - first, first)
        for first in range(1, min(10, size) + 1)
    )
    return 100 - complement_upper


def main() -> None:
    minimum_shadow = [shadow_lower(size) for size in range(24)]
    expected = [
        0, 9, 15, 18, 18, 24, 27, 27, 30, 30, 30, 35,
        35, 36, 36, 36, 36, 42, 45, 45, 48, 48, 48, 52,
    ]
    assert minimum_shadow == expected

    # For d <= 7, either the transpose/prolongation lower bound already
    # fails, or the two-sided Koszul lower bound exceeds the nine-term cap.
    low_d_records = []
    for s in range(19):
        feasible = []
        for d in range(8):
            required_p = minimum_shadow[s] + d - s
            if required_p <= P_UPPER[d]:
                lower_rank = (
                    2400 + (25 * d - P_UPPER[d])
                    - (25 * s - minimum_shadow[s])
                )
                feasible.append({
                    "d": d,
                    "required_p": required_p,
                    "p_upper": P_UPPER[d],
                    "residual_K_lower": lower_rank,
                    "excess_over_nine_terms": lower_rank - 2160,
                })
                assert lower_rank > 2160
        low_d_records.append({
            "s": s,
            "not_already_transpose_excluded": feasible,
            "minimum_excess": min(
                (row["excess_over_nine_terms"] for row in feasible),
                default=None,
            ),
        })

    high_d_uniform_lower = 2400 + (25 * 8 - P_UPPER[8]) - (
        25 * 18 - minimum_shadow[18]
    )
    assert high_d_uniform_lower == 2167

    states = []
    for s in range(19, 23):
        m_s = minimum_shadow[s]
        for d in range(9, 61 - m_s):
            for t in range(m_s, 61 - d):
                states.append({
                    "s": s,
                    "d": d,
                    "t": t,
                    "h": t + d,
                    "H_equals_U_by_h_ge_57": t + d >= 57,
                })
    assert len(states) == 58
    histogram = {
        str(s): sum(row["s"] == s for row in states)
        for s in range(19, 23)
    }
    assert histogram == {"19": 28, "20": 10, "21": 10, "22": 10}
    assert sum(row["H_equals_U_by_h_ge_57"] for row in states) == 52

    result = {
        "status": "PASS",
        "claim_type": "independent exact integer audit of the pure fixed-six universe derivation",
        "evidence_class": "exact_integer_audit_only_not_a_proof_dependency",
        "imports_old_shifted_ideal_or_frontier_data": False,
        "petersen_h": list(H),
        "layer_differences": list(D),
        "minimum_product_shadow_0_through_23": minimum_shadow,
        "relative_prolongation_upper_0_through_8": list(P_UPPER),
        "s_0_through_18_low_d_checks": low_d_records,
        "d_at_least_8_uniform_residual_K_lower": high_d_uniform_lower,
        "fixed_six_state_count": len(states),
        "state_histogram_by_s": histogram,
        "h_at_least_57_state_count": 52,
        "states": states,
        "strict_scope": (
            "This audits only the finite arithmetic in section 42.1.  The "
            "proof dependencies are the written Petersen fibre inequality, "
            "torus semicontinuity, two-sided Koszul rank inequality, and "
            "coupling lemmas."
        ),
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUT.write_bytes((json.dumps(result, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({
        "status": result["status"],
        "shadow_table": minimum_shadow,
        "fixed_six_states": len(states),
        "histogram": histogram,
        "h_ge_57": 52,
    }, indent=2))
    print("output", OUT.name)
    print("sha256", hashlib.sha256(OUT.read_bytes()).hexdigest().upper())


if __name__ == "__main__":
    main()
