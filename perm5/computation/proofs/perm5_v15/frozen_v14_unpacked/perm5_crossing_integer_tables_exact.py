"""Exact integer audit for the pure crossing inequalities.

This script checks only the small arithmetic minimizations in equations
(21)--(29) of perm5_pure_route_20260803.md.  It is not a substitute for the
graph-cut proof that reduces the prolongation problem to those inequalities.
All arithmetic is over the integers and every search range is explicit.
"""

from __future__ import annotations

import json


def diagonal_cost(m: int, z: int, o: int) -> int:
    assert 0 <= z <= o
    if m <= z:
        return 0
    if m <= o:
        return m - z
    return 2 * m - o - z


def minimum_q(r: int, m: int) -> int:
    values: list[int] = []
    for h2 in range(4):
        for h1 in range(4 - h2):
            for v2 in range(4):
                for v1 in range(4 - v2):
                    groups = h2 + h1 + v2 + v1
                    if 2 * groups < r:
                        continue
                    side_cost = 2 * (h2 + v2) + h1 + v1
                    z = h2 * v2
                    o = (h2 + h1) * (v2 + v1)
                    values.append(r + side_cost + diagonal_cost(m, z, o))
    assert values
    return min(values)


def noncorner_cap(q: int) -> int:
    best = 0
    for r in range(13):
        for m in range(10):
            if minimum_q(r, m) <= q:
                best = max(best, r + m)
    return best


def corner_cap(s: int, b: int) -> int:
    g = (0, 0, 1, 2, 4)
    return min(4, s + g[b])


def marginal_cap(n: int) -> int:
    return max(
        corner_cap(s, b) + noncorner_cap(n - s - b)
        for s in range(5)
        for b in range(5)
        if s + b <= n
    )


def main() -> None:
    expected_rows = {
        3: [6, 6, 5, 5],
        4: [8, 8, 7, 6, 6],
        5: [10, 9, 9, 8, 7, 8],
        6: [10, 11, 10, 10, 9, 9, 9],
    }
    actual_rows = {
        k: [minimum_q(r, k - r) for r in range(k + 1)]
        for k in expected_rows
    }
    assert actual_rows == expected_rows

    f_values = [noncorner_cap(q) for q in range(11)]
    assert f_values == [0, 0, 1, 2, 2, 3, 4, 5, 5, 6, 7]

    mu_values = [marginal_cap(n) for n in range(11)]
    assert mu_values == [0, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8]

    result = {
        "status": "PASS",
        "proof_role": "integer-table audit only; graph-cut reduction required",
        "equation_26_rows": actual_rows,
        "F_q": f_values,
        "mu_N": mu_values,
        "endpoint_only_warning": {
            "p_h": 3,
            "p_v": 3,
            "m": 6,
            "interior_minimizers": [[2, 3], [3, 2]],
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
