"""Exact audit of the pure five-vertex orbit--1 terminal formula.

The proof is in n5_orbit1_terminal_pure_graph_classification_20260810.md.
This script is redundant: it compares that closed formula with the independent
QQ/signed-graph prolongation engine on all 2^15 subsets, then checks the
ten-weight extremum.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import perm5_orbit13_four_row_QQ_audit as engine
from perm5_orbit1_missing_WM_exact import L0_CELLS, quotient_descriptors


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_orbit1_terminal_pure_formula_audit_exact.json"

# Positions in quotient_descriptors(L0_CELLS).
S0, A1, A2, A3, C, S1, B12, B13, X1, S2, B23, X2, S3, X3, SZ = range(15)
A_POS = {1: A1, 2: A2, 3: A3}
S_POS = {0: S0, 1: S1, 2: S2, 3: S3, 4: SZ}
X_POS = {1: X1, 2: X2, 3: X3}
B_POS = {(1, 2): B12, (1, 3): B13, (2, 3): B23}


def indicator(selected: set[int], position: int) -> int:
    return int(position in selected)


def pure_formula(selected_positions) -> tuple[int, dict[str, int]]:
    selected = set(selected_positions)
    square = {v: indicator(selected, position) for v, position in S_POS.items()}
    a = {i: indicator(selected, position) for i, position in A_POS.items()}
    x = {i: indicator(selected, position) for i, position in X_POS.items()}
    b = {pair: indicator(selected, position) for pair, position in B_POS.items()}
    c = indicator(selected, C)

    degree = {
        0: c + sum(a.values()),
        1: a[1] + b[1, 2] + b[1, 3] + x[1],
        2: a[2] + b[1, 2] + b[2, 3] + x[2],
        3: a[3] + b[1, 3] + b[2, 3] + x[3],
        4: c + sum(x.values()),
    }
    base_triangles = (
        a[1] * a[2] * b[1, 2]
        + a[1] * a[3] * b[1, 3]
        + a[2] * a[3] * b[2, 3]
        + b[1, 2] * b[1, 3] * b[2, 3]
    )
    z_triangles = (
        sum(c * a[i] * x[i] for i in (1, 2, 3))
        + sum(x[i] * x[j] * b[i, j] for i, j in combinations((1, 2, 3), 2))
    )
    four_cycles = sum(
        a[i] * a[j] * x[i] * x[j] * (1 - b[i, j])
        for i, j in combinations((1, 2, 3), 2)
    )
    eta = sum(x.values()) + c * sum(a[i] * (1 - x[i]) for i in (1, 2, 3))
    square_part = square[0] * (1 + degree[0] + eta)
    square_part += sum(square[v] * (1 + degree[v]) for v in (1, 2, 3, 4))
    total = 5 * base_triangles + z_triangles + four_cycles + square_part
    return total, {
        "selected_edges": sum(a.values()) + sum(b.values()) + c + sum(x.values()),
        "selected_squares": sum(square.values()),
        "base_triangles": base_triangles,
        "z_triangles": z_triangles,
        "four_cycles": four_cycles,
        "eta": eta,
        "square_part": square_part,
    }


def main() -> None:
    universe = quotient_descriptors(L0_CELLS)
    assert len(universe) == len(set(universe)) == 15
    engine.UA_DESCRIPTORS = universe
    engine.UA = tuple(engine.CLASS_INDEX[value] for value in universe)
    engine.UA_POSITION = {value: i for i, value in enumerate(engine.UA)}
    tables, _local_sizes = engine.build_local_tables()
    exact_qq = engine.evaluator(tables)

    checked = 0
    for mask in range(1 << 15):
        selected = tuple(i for i in range(15) if (mask >> i) & 1)
        formula_value, _parts = pure_formula(selected)
        engine_value = exact_qq(selected)
        assert formula_value == engine_value, (selected, formula_value, engine_value)
        checked += 1

    histogram = Counter()
    maxima_by_edge_count: dict[int, int] = {}
    maximizers = []
    for selected in combinations(range(15), 10):
        value, parts = pure_formula(selected)
        histogram[value] += 1
        edge_count = parts["selected_edges"]
        maxima_by_edge_count[edge_count] = max(
            maxima_by_edge_count.get(edge_count, -1), value
        )
        if value == 36:
            maximizers.append(list(selected))

    expected_maxima = {5: 25, 6: 36, 7: 36, 8: 34, 9: 31, 10: 26}
    assert maxima_by_edge_count == expected_maxima
    assert len(maximizers) == 4
    assert max(histogram) == 36

    payload = {
        "status": "PASS_EXACT_QQ_REDUNDANT_AUDIT_OF_PURE_GRAPH_FORMULA",
        "evidence_class": "redundant exact audit; not a proof dependency",
        "all_subsets_formula_vs_QQ_checked": checked,
        "ten_weight_subsets_checked": sum(histogram.values()),
        "maximum_p": max(histogram),
        "maximum_count": len(maximizers),
        "maxima_by_selected_edge_count": {
            str(key): value for key, value in sorted(maxima_by_edge_count.items())
        },
        "maximizer_positions": maximizers,
        "p_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "pure_proof": "n5_orbit1_terminal_pure_graph_classification_20260810.md",
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("PASS_EXACT_QQ_REDUNDANT_AUDIT_OF_PURE_GRAPH_FORMULA")
    print(f"all_subsets_formula_vs_QQ_checked={checked}")
    print(f"ten_weight_subsets_checked={sum(histogram.values())}")
    print("maximum_p=36")
    print("maximum_count=4")


if __name__ == "__main__":
    main()
