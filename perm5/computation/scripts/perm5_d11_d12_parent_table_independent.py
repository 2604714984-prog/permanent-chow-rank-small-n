#!/usr/bin/env python3
"""Independent exact audit of the finite parent table in the perm5 d=11,12 route.

The program reconstructs the four coordinate cubic flags from three-subsets,
differentiates them combinatorially, and streams all C(25,5) coordinate
five-planes.  It imports no project generator and reads no frozen certificate.
It checks only the finite table, not the relative-Grassmannian bridge.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


Triple = tuple[int, int, int]
Cubic = tuple[Triple, Triple]
Child = tuple[tuple[int, int], tuple[int, int]]
Variable = tuple[int, int]


def require_equal(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise RuntimeError(
            f"{label} mismatch: expected {expected!r}, observed {actual!r}"
        )


def triples(values: range | tuple[int, ...]) -> tuple[Triple, ...]:
    return tuple(combinations(values, 3))


ALL_TRIPLES = triples(range(5))
CORE_COLUMNS = triples((0, 1, 2, 3))
CORE_ROW: Triple = (0, 1, 2)
SIDE_ROWS: tuple[Triple, ...] = ((0, 1, 3), (0, 2, 3), (1, 2, 3))


def build_s22() -> frozenset[Cubic]:
    family = {(CORE_ROW, column_triple) for column_triple in ALL_TRIPLES}
    family.update(
        (row_triple, column_triple)
        for row_triple in SIDE_ROWS
        for column_triple in CORE_COLUMNS
    )
    require_equal("S22 cubic family size", len(family), 22)
    return frozenset(family)


S22 = build_s22()
FLAGS: dict[str, frozenset[Cubic]] = {
    "S22": S22,
    "delete_core_inner": S22 - {(CORE_ROW, (0, 1, 2))},
    "delete_core_with_4": S22 - {(CORE_ROW, (0, 1, 4))},
    "delete_side": S22 - {((0, 1, 3), (0, 1, 2))},
}


def derivative_parent_sets(family: frozenset[Cubic]) -> dict[Child, frozenset[Variable]]:
    parents: dict[Child, set[Variable]] = defaultdict(set)
    for row_triple, column_triple in family:
        for row in row_triple:
            child_rows = tuple(value for value in row_triple if value != row)
            for column in column_triple:
                child_columns = tuple(value for value in column_triple if value != column)
                parents[(child_rows, child_columns)].add((row, column))
    frozen = {child: frozenset(values) for child, values in parents.items()}
    require_equal("quadratic derivative shadow size", len(frozen), 48)
    return frozen


PARENTS = {name: derivative_parent_sets(family) for name, family in FLAGS.items()}


def row_partition(plane: tuple[int, ...]) -> str:
    counts = Counter(index // 5 for index in plane)
    return "+".join(str(value) for value in sorted(counts.values(), reverse=True))


EXPECTED = {
    "5": {"S22": 4, "delete_core_inner": 4, "delete_core_with_4": 4, "delete_side": 4},
    "4+1": {"S22": 4, "delete_core_inner": 4, "delete_core_with_4": 4, "delete_side": 7},
    "3+2": {"S22": 2, "delete_core_inner": 2, "delete_core_with_4": 5, "delete_side": 3},
    "3+1+1": {"S22": 1, "delete_core_inner": 1, "delete_core_with_4": 2, "delete_side": 5},
    "2+2+1": {"S22": 1, "delete_core_inner": 1, "delete_core_with_4": 5, "delete_side": 2},
    "2+1+1+1": {"S22": 0, "delete_core_inner": 0, "delete_core_with_4": 2, "delete_side": 2},
    "1+1+1+1+1": {"S22": 0, "delete_core_inner": 0, "delete_core_with_4": 0, "delete_side": 0},
}


def build_result() -> dict[str, object]:
    candidate_count = math.comb(25, 5)
    require_equal("coordinate five-plane candidate count", candidate_count, 53_130)
    maxima = {partition: {name: -1 for name in FLAGS} for partition in EXPECTED}
    witnesses = {partition: {name: [] for name in FLAGS} for partition in EXPECTED}

    checked = 0
    for plane in combinations(range(25), 5):
        checked += 1
        partition = row_partition(plane)
        selected = frozenset(divmod(index, 5) for index in plane)
        for name, parent_sets in PARENTS.items():
            codimension = sum(parent_set <= selected for parent_set in parent_sets.values())
            if codimension > maxima[partition][name]:
                maxima[partition][name] = codimension
                witnesses[partition][name] = list(plane)

    require_equal("coordinate five-planes checked", checked, candidate_count)
    require_equal("parent table", maxima, EXPECTED)
    return {
        "status": "PASS",
        "claim_type": "independent exact integer audit of finite parent table only",
        "imports_project_generator": False,
        "reads_frozen_result": False,
        "coordinate_five_planes_checked": checked,
        "cubic_flag_sizes": {name: len(family) for name, family in FLAGS.items()},
        "quadratic_shadow_sizes": {name: len(parent_sets) for name, parent_sets in PARENTS.items()},
        "maximum_killed_parent_points_by_row_partition": maxima,
        "first_maximizing_plane_by_row_partition": witnesses,
        "global_maxima": {name: max(rows[name] for rows in maxima.values()) for name in FLAGS},
        "strict_scope": (
            "This verifies the finite coordinate parent table. It does not prove "
            "the torus fixed-point reduction, DVR extension, or relative "
            "Grassmannian argument."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    print("PERM5_D11_D12_PARENT_TABLE_INDEPENDENT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
