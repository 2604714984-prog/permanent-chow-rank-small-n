"""Integer audit of the handwritten characteristic-zero graph proof p12<=61.

The proof uses the no-crossing graph formula, the pure crossing marginal
sequence mu(N), and two small equality-gap lemmas.  This file checks only the
resulting integer case split.  The optional local-model comparison at the end
is diagnostic and is not needed for the graph argument.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from perm5_coordinate_d3_orbit_scan import CLASSES
from perm5_crossing_integer_tables_exact import marginal_cap


ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "n5_coordinate_prolongation_hypergraph_F3_exact.json"
OUTPUT = ROOT / "n5_p12_global_graph_bound_integer_exact.json"


def main() -> None:
    mu = [marginal_cap(n) for n in range(12)]
    assert mu == [0, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9]

    # Exact/upper no-crossing values, separated by square count.
    d11_by_squares = {
        0: 50, 1: 55, 2: 45, 3: 40, 4: 52, 5: 45,
        6: 33, 7: 26, 8: 19, 9: 15, 10: 12, 11: 11,
    }
    d10_by_squares = {
        0: 50, 1: 40, 2: 36, 3: 36, 4: 44, 5: 32,
        6: 25, 7: 18, 8: 14, 9: 11, 10: 10,
    }

    # One crossing.  The only coarse value above 61 is s=1.  In that case
    # the one-square no-crossing table has a gap: value 55 occurs only for a
    # full K5 in the marked row/column.  A full K5 on an unmarked line gives
    # 51, and every configuration with triangle total below ten is <=40.
    # A crossing adds at most one to the exceptional K5+square configuration.
    one_crossing = {}
    for squares, base in d11_by_squares.items():
        if squares == 1:
            bound = max(55 + 1, 51 + mu[11])
        else:
            bound = base + mu[11]
        one_crossing[squares] = bound
    assert max(one_crossing.values()) == 61

    # Two crossings.  With no squares, either the ten pure edges are one K5
    # (the first crossing has zero marginal and the second at most nine), or
    # their triangle total is at most seven, hence the base p is at most 35.
    # For positive square count the ordinary two marginal caps suffice.
    two_crossings = {}
    for squares, base in d10_by_squares.items():
        if squares == 0:
            bound = max(50 + 0 + mu[11], 35 + mu[10] + mu[11])
        else:
            bound = base + mu[10] + mu[11]
        two_crossings[squares] = bound
    assert max(two_crossings.values()) == 61

    no_crossing_by_dimension = {
        0: 0, 1: 1, 2: 2, 3: 5, 4: 8, 5: 11,
        6: 20, 7: 24, 8: 28, 9: 35, 10: 50,
        11: 55, 12: 60,
    }
    at_least_three = {
        crossings: no_crossing_by_dimension[12 - crossings]
        + sum(mu[12 - crossings:12])
        for crossings in range(3, 13)
    }
    assert at_least_three == {
        3: 59, 4: 58, 5: 60, 6: 61, 7: 56,
        8: 57, 9: 57, 10: 56, 11: 56, 12: 55,
    }
    global_bound = max(60, max(one_crossing.values()), max(two_crossings.values()), max(at_least_three.values()))
    assert global_bound == 61

    # Diagnostic only: exact local tables reproduce the exceptional
    # K5+square statement.  The paper proof obtains the same 0/1 marginal by
    # inspecting the four-corner, repeat, and K3,3 cuts.
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    full_row = {
        index for index, descriptor in enumerate(CLASSES)
        if descriptor[0] == "R" and descriptor[1] == 0
    }
    base = full_row | {0}

    def p(selected: set[int]) -> int:
        total = 0
        for block in model["local_blocks"]:
            mask = sum(
                1 << bit
                for bit, weight in enumerate(block["involved_quadratic_weights"])
                if weight in selected
            )
            total += block["nonzero_relative_truth_table"].get(str(mask), 0)
        return total

    assert p(base) == 55
    crossing_values = [
        p(base | {index})
        for index, descriptor in enumerate(CLASSES)
        if descriptor[0] == "X"
    ]
    assert Counter(crossing_values) == {55: 84, 56: 16}

    result = {
        "status": "PASS",
        "claim_type": "integer audit of the pure graph case split p12<=61",
        "mu_0_through_11": mu,
        "one_crossing_bounds_by_square_count": one_crossing,
        "two_crossing_bounds_by_square_count": two_crossings,
        "at_least_three_crossing_bounds": at_least_three,
        "global_p12_upper": global_bound,
        "exceptional_K5_plus_square_diagnostic_histogram": dict(Counter(crossing_values)),
        "strict_evidence_note": (
            "The global proof is the handwritten no-crossing formula plus cut marginal lemmas. "
            "The finite-field local-model comparison is diagnostic only."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
