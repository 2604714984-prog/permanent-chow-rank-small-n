"""Exact audit of the handwritten global graph proof p_11 <= 55.

This script checks the finite arithmetic after the no-crossing formula and
the one-crossing marginal lemma have been proved.  It does not replace those
two graph lemmas.
"""

import json
from pathlib import Path

from perm5_coordinate_d3_orbit_scan import CLASSES
from perm5_crossing_integer_tables_exact import marginal_cap


ROOT = Path(__file__).resolve().parent
HYPERGRAPH = ROOT / "n5_coordinate_prolongation_hypergraph_F3_exact.json"


# Exact no-crossing maxima B_d for d=0,...,11, proved by the triangle/square
# inequalities and independently audited in perm5_p9_nocrossing_exact.py.
NO_CROSSING = [0, 1, 2, 5, 8, 11, 20, 24, 28, 35, 50, 55]


def main() -> None:
    mu = [marginal_cap(n) for n in range(11)]
    assert mu == [0, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8]

    # If there are c crossings, remove them all and add them back.  For
    # c>=2 the coarse marginal bounds already suffice.
    bounds = {
        c: NO_CROSSING[11 - c] + sum(mu[11 - c : 11])
        for c in range(2, 12)
    }
    assert bounds == {
        2: 50,
        3: 49,
        4: 51,
        5: 52,
        6: 47,
        7: 48,
        8: 48,
        9: 47,
        10: 47,
        11: 46,
    }

    # Direct exact audit of the only exceptional local lemma: adding any
    # crossing to all ten edge weights in one fixed row contributes zero.
    model = json.loads(HYPERGRAPH.read_text(encoding="utf-8"))
    full_row = {
        index
        for index, descriptor in enumerate(CLASSES)
        if descriptor[0] == "R" and descriptor[1] == 0
    }
    crossings = [
        index for index, descriptor in enumerate(CLASSES) if descriptor[0] == "X"
    ]
    assert len(full_row) == 10 and len(crossings) == 100

    def relative_prolongation(selected: set[int]) -> int:
        total = 0
        for block in model["local_blocks"]:
            mask = sum(
                1 << bit
                for bit, weight in enumerate(block["involved_quadratic_weights"])
                if weight in selected
            )
            total += block["nonzero_relative_truth_table"].get(str(mask), 0)
        return total

    assert relative_prolongation(full_row) == 50
    assert all(
        relative_prolongation(full_row | {crossing}) == 50
        for crossing in crossings
    )

    # For exactly one crossing, the ten-direction no-crossing base is split:
    # with a square its value is at most 44 and the crossing adds at most 8;
    # without squares a non-extreme row/column split is at most 35 and adds
    # at most 8; a complete K5 in one row/column has value 50 and the direct
    # local-block lemma says that a crossing has zero marginal.
    one_crossing = max(44 + 8, 35 + 8, 50 + 0)
    assert one_crossing == 52
    assert max(NO_CROSSING[11], one_crossing, max(bounds.values())) == 55

    print("NO_CROSSING_BOUND=55")
    print(f"ONE_CROSSING_BOUND={one_crossing}")
    print(f"AT_LEAST_TWO_CROSSINGS_BOUND={max(bounds.values())}")
    print("FULL_ROW_PLUS_ANY_CROSSING=50")
    print("GLOBAL_P11_UPPER=55")
    print("STATUS=PASS")


if __name__ == "__main__":
    main()
