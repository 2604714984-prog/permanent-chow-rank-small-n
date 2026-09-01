"""Exact QQ diagnostic for the missing orbit--1 common-envelope branch.

This script deliberately tests only the fifteen quotient weights in

    L_0 = <x_00,x_01,x_02,x_03,x_10>.

It reconstructs the characteristic-zero signed-graph prolongation evaluator
from ``perm5_orbit13_four_row_QQ_audit.py`` and checks all C(15,10)=3003
coordinate ten-planes.  The calculation is a diagnostic for the global
degeneration interface; it is not used as a substitute for a proof that an
arbitrary non-coordinate family has one of these limits.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations, combinations_with_replacement
from pathlib import Path

import perm5_orbit13_four_row_QQ_audit as engine


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_orbit1_missing_WM_exact.json"
ENGINE = ROOT / "perm5_orbit13_four_row_QQ_audit.py"

M_CELLS = (0, 1, 2, 3)
N_CELLS = (5, 6, 10, 11)
L0_CELLS = M_CELLS + (5,)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def quotient_descriptors(cells: tuple[int, ...]):
    result = []
    for first, second in combinations_with_replacement(cells, 2):
        q_index, _sign = engine.quadratic_class((first, second))
        result.append(engine.CLASSES[q_index])
    return tuple(result)


def descriptor_json(descriptor):
    return list(descriptor)


def main() -> None:
    universe = quotient_descriptors(L0_CELLS)
    assert len(universe) == 15
    assert len(set(universe)) == 15  # q|Sym^2(L_0) is injective.

    # The imported engine reads these globals when it constructs its exact
    # local signed graphs.  No numerical or finite-field rank is used.
    engine.UA_DESCRIPTORS = universe
    engine.UA = tuple(engine.CLASS_INDEX[value] for value in universe)
    engine.UA_POSITION = {value: i for i, value in enumerate(engine.UA)}
    tables, local_sizes = engine.build_local_tables()
    p_value = engine.evaluator(tables)

    records = []
    histogram = Counter()
    for chosen in combinations(range(15), 10):
        value = p_value(chosen)
        histogram[value] += 1
        if value >= 36:
            records.append(
                {
                    "p_exact_QQ": value,
                    "positions": list(chosen),
                    "descriptors": [descriptor_json(universe[i]) for i in chosen],
                }
            )

    wm_descriptors = quotient_descriptors(M_CELLS)
    wm_positions = tuple(universe.index(value) for value in wm_descriptors)
    assert len(wm_positions) == 10
    assert p_value(wm_positions) == 36

    c010 = ("C", 0, 1, 0)
    o1_descriptors = (
        ("S", 0, 0),
        ("S", 0, 1),
        ("S", 0, 2),
        ("R", 0, 0, 1),
        ("R", 0, 0, 2),
        ("R", 0, 0, 3),
        ("R", 0, 1, 2),
        ("R", 0, 1, 3),
        ("R", 0, 2, 3),
        c010,
    )
    o1_positions = tuple(universe.index(value) for value in o1_descriptors)
    assert p_value(o1_positions) == 36

    candidate_envelopes = [set(quotient_descriptors(M_CELLS + (cell,))) for cell in N_CELLS]
    common_envelope = set.intersection(*candidate_envelopes)
    assert common_envelope == set(wm_descriptors)

    high_descriptor_sets = {
        frozenset(tuple(value) for value in record["descriptors"])
        for record in records
    }
    assert len(records) == 4
    assert max(histogram) == 36
    assert frozenset(wm_descriptors) in high_descriptor_sets
    assert frozenset(o1_descriptors) in high_descriptor_sets

    result = {
        "status": "PASS_EXACT_QQ_DIAGNOSTIC_FOUND_MISSING_WM_BRANCH",
        "evidence_class": "exact characteristic-zero signed-graph diagnostic",
        "logical_scope": (
            "All 3003 coordinate ten-planes inside q(Sym^2 L0) are checked. "
            "This does not prove the global degeneration or exclude the WM branch."
        ),
        "engine_sha256": sha256(ENGINE),
        "ambient_cells": list(L0_CELLS),
        "quotient_universe": [descriptor_json(value) for value in universe],
        "coordinate_ten_planes_checked": 3003,
        "local_weight_block_size_histogram": {
            str(key): value for key, value in sorted(local_sizes.items())
        },
        "p_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "maximum_p_exact_QQ": 36,
        "p_at_least_36_count": len(records),
        "p_at_least_36_records": records,
        "paper_length_two_plane": {
            "p_exact_QQ": p_value(o1_positions),
            "descriptors": [descriptor_json(value) for value in o1_descriptors],
        },
        "missing_common_envelope_plane_WM": {
            "definition": "q(Sym^2 <x_00,x_01,x_02,x_03>)",
            "p_exact_QQ": p_value(wm_positions),
            "descriptors": [descriptor_json(value) for value in wm_descriptors],
            "contained_in_all_four_candidate_L_envelopes": True,
        },
        "four_candidate_extra_cells": list(N_CELLS),
        "intersection_of_four_candidate_envelopes": [
            descriptor_json(value) for value in universe if value in common_envelope
        ],
        "conclusion": (
            "The length-two W0 fibre is not the only p=36 coordinate endpoint. "
            "WM is the common ten-dimensional intersection of all four candidate "
            "five-plane envelopes, so it requires a separate relative rigidity proof."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS_EXACT_QQ_DIAGNOSTIC_FOUND_MISSING_WM_BRANCH")
    print("coordinate_ten_planes_checked=3003")
    print("maximum_p_exact_QQ=36")
    print("p_at_least_36_count=4")
    print("p_WM_exact_QQ=36")
    print("common_four_envelope_dimension=10")


if __name__ == "__main__":
    main()
