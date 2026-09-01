#!/usr/bin/env python3
"""Exact diagnostic for the closed crossing-marginal density lemma.

The proof replaces the old twelve-entry marginal table by

    F(q) <= floor(3q/4),  0 <= q <= 11,
    F(4) <= 2,

and hence mu(N) <= N for N <= 4 and ceil(3N/4) for 5 <= N <= 11.
This program checks the three cut-cost regimes using exact integers.  It is
diagnostic only; the algebraic regime proof is written separately.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_crossing_marginal_density_exact.json"
G = (0, 0, 1, 2, 4)


def diagonal_cost(matching: int, zero_cost: int, one_cost: int) -> int:
    if matching <= zero_cost:
        return 0
    if matching <= one_cost:
        return matching - zero_cost
    return 2 * matching - one_cost - zero_cost


def main() -> None:
    evaluations = 0
    feasible = []
    regime_counts = {"m_le_z": 0, "z_lt_m_le_o": 0, "o_lt_m": 0}

    for h2 in range(4):
        for h1 in range(4 - h2):
            for v2 in range(4):
                for v1 in range(4 - v2):
                    horizontal = h2 + h1
                    vertical = v2 + v1
                    group_count = horizontal + vertical
                    side_cost = group_count + h2 + v2
                    zero_cost = h2 * v2
                    one_cost = horizontal * vertical
                    for repeat in range(13):
                        if repeat > 2 * group_count:
                            continue
                        for matching in range(10):
                            evaluations += 1
                            diagonal = diagonal_cost(
                                matching, zero_cost, one_cost
                            )
                            cost = repeat + side_cost + diagonal
                            if cost > 11:
                                continue
                            if matching <= zero_cost:
                                regime = "m_le_z"
                            elif matching <= one_cost:
                                regime = "z_lt_m_le_o"
                            else:
                                regime = "o_lt_m"
                            regime_counts[regime] += 1
                            activated = repeat + matching
                            assert 4 * activated <= 3 * cost
                            if cost <= 4:
                                assert activated <= 2
                            feasible.append((cost, activated))

    exact_noncorner = []
    for budget in range(12):
        exact_noncorner.append(max(
            activated
            for cost, activated in feasible
            if cost <= budget
        ))
    assert exact_noncorner == [0, 0, 1, 2, 2, 3, 4, 5, 5, 6, 7, 8]

    density_bound = [3 * budget // 4 for budget in range(12)]
    density_bound[4] = 2
    assert all(
        actual <= bound
        for actual, bound in zip(exact_noncorner, density_bound)
    )

    corner_exceptions = []
    for squares in range(5):
        for boundary in range(5):
            occupied = squares + boundary
            corners = min(4, squares + G[boundary])
            ceiling = (3 * occupied + 3) // 4
            if corners > ceiling:
                corner_exceptions.append((squares, boundary))
    assert corner_exceptions == [(0, 4), (4, 0)]

    exact_marginal = []
    density_derived_marginal = []
    structural_marginal_bound = []
    for existing in range(12):
        values = []
        for squares in range(5):
            for boundary in range(5):
                if squares + boundary > existing:
                    continue
                remaining = existing - squares - boundary
                corners = min(4, squares + G[boundary])
                values.append(corners + exact_noncorner[remaining])
        exact_marginal.append(max(values))
        density_derived_marginal.append(max(
            min(4, squares + G[boundary])
            + density_bound[existing - squares - boundary]
            for squares in range(5)
            for boundary in range(5)
            if squares + boundary <= existing
        ))
        structural_marginal_bound.append(
            existing if existing <= 4 else (3 * existing + 3) // 4
        )

    expected = [0, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9]
    assert exact_marginal == expected
    assert all(
        derived <= bound
        for derived, bound in zip(
            density_derived_marginal, structural_marginal_bound
        )
    )
    assert structural_marginal_bound == expected

    result = {
        "status": "PASS_EXACT_INTEGER_CROSSING_MARGINAL_DENSITY_AUDIT",
        "evidence_role": (
            "diagnostic for the written three-regime density proof; the old "
            "twelve-entry marginal table is not an active proof dependency"
        ),
        "cut_cost_regimes": 3,
        "diagnostic_parameter_evaluations": evaluations,
        "diagnostic_feasible_cost_at_most_11": len(feasible),
        "diagnostic_regime_counts": regime_counts,
        "exact_noncorner_F_0_through_11": exact_noncorner,
        "density_upper_0_through_11": density_bound,
        "corner_exception_patterns": [
            {"squares": 4, "boundary_edges": 0},
            {"squares": 0, "boundary_edges": 4},
        ],
        "exact_marginal_0_through_11": exact_marginal,
        "density_derived_marginal_0_through_11": density_derived_marginal,
        "closed_marginal_upper": {
            "N_0_through_4": "N",
            "N_5_through_11": "ceil(3N/4)",
        },
        "active_12_value_marginal_table_required": False,
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": result["status"],
        "cut_cost_regimes": result["cut_cost_regimes"],
        "diagnostic_parameter_evaluations": evaluations,
        "exact_noncorner_F_0_through_11": exact_noncorner,
        "exact_marginal_0_through_11": exact_marginal,
        "active_12_value_marginal_table_required": False,
    }, indent=2))


if __name__ == "__main__":
    main()
