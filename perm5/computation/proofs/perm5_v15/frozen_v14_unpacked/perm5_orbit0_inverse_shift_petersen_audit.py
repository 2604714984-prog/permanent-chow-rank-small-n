"""Exact diagnostic for the witness-free orbit-0 inverse-shift proof.

The mathematical proof is the Petersen even-walk lemma plus the five-slice
formula.  This script independently checks all Petersen subsets, all valid
one-step directions and every two-row five-cell plane.  It never constructs
or reads the former 92-edge witness forests.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import perm5_flag_shifted_stability_verify as base


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_orbit0_inverse_shift_petersen_exact.json"


def petersen_neighbors():
    result = []
    for first in base.PAIRS:
        mask = 0
        for index, second in enumerate(base.PAIRS):
            if set(first).isdisjoint(second):
                mask |= 1 << index
        result.append(mask)
    assert all(mask.bit_count() == 3 for mask in result)
    return tuple(result)


def neighborhood(mask: int, neighbors):
    result = 0
    for vertex in base.positions(mask):
        result |= neighbors[vertex]
    return result


def plane_split(second_row: int, moved_columns):
    moved = set(moved_columns)
    return sum(
        1 << (5 * (second_row if column in moved else 0) + column)
        for column in range(5)
    )


def main():
    neighbors = petersen_neighbors()
    all_vertices = (1 << 10) - 1
    petersen_slack = Counter()
    for subset in range(1, all_vertices):
        overlap = (
            neighborhood(subset, neighbors)
            & neighborhood(all_vertices ^ subset, neighbors)
        ).bit_count()
        assert overlap >= 1
        petersen_slack[overlap] += 1

    family = base.family_from_shape((10, 10))
    plane = base.plane_from_partition((5,))
    assert base.shadow_mask(family).bit_count() == 50
    assert base.visible_size(family, plane) == 30

    valid_count = 0
    nontrivial_family_count = 0
    direction_records = []
    for axis in (0, 1):
        for low in range(5):
            for high in range(5):
                if low == high:
                    continue
                family_pairs, plane_pairs = base.reflection_pairs(
                    axis, low, high
                )
                family_data = base.preimage_data(family, family_pairs)
                plane_data = base.preimage_data(plane, plane_pairs)
                if family_data is None or plane_data is None:
                    continue
                valid_count += 1
                fixed_family, movable_family = family_data
                fixed_plane, movable_plane = plane_data

                family_pass = []
                for assignment in range(1 << len(movable_family)):
                    source = base.oriented_mask(
                        fixed_family, movable_family, assignment
                    )
                    if base.shadow_mask(source).bit_count() <= 50:
                        family_pass.append(assignment)
                expected_family_pass = (
                    [0]
                    if not movable_family
                    else [0, (1 << len(movable_family)) - 1]
                )
                assert family_pass == expected_family_pass
                if movable_family:
                    nontrivial_family_count += 1

                flag_pass = []
                for family_assignment in family_pass:
                    source_family = base.oriented_mask(
                        fixed_family, movable_family, family_assignment
                    )
                    for plane_assignment in range(1 << len(movable_plane)):
                        source_plane = base.oriented_mask(
                            fixed_plane, movable_plane, plane_assignment
                        )
                        visible = base.visible_size(source_family, source_plane)
                        if visible <= 40:
                            flag_pass.append((family_assignment, plane_assignment))
                expected_flag_count = (
                    1 if not movable_family and not movable_plane else 2
                )
                assert len(flag_pass) == expected_flag_count
                direction_records.append({
                    "direction": (
                        f"{'row' if axis == 0 else 'column'}:{low}<-{high}"
                    ),
                    "family_variable_count": len(movable_family),
                    "plane_variable_count": len(movable_plane),
                    "family_pass_count": len(family_pass),
                    "flag_pass_count": len(flag_pass),
                })

    assert valid_count == 31
    assert nontrivial_family_count == 8

    slice_formula = {}
    for second_row in range(1, 5):
        by_size = {}
        for size in range(6):
            values = set()
            for moved_columns in combinations(range(5), size):
                value = base.visible_size(
                    family, plane_split(second_row, moved_columns)
                )
                values.add(value)
            assert len(values) == 1
            value = values.pop()
            expected = (
                50
                - 2 * (size * (size - 1) * (size - 2) // 6)
                - 2 * ((5 - size) * (4 - size) * (3 - size) // 6)
                if second_row == 1
                else 50
                - 2 * ((5 - size) * (4 - size) * (3 - size) // 6)
            )
            assert value == expected
            by_size[str(size)] = value
        slice_formula[str(second_row)] = by_size

    result = {
        "status": "PASS_EXACT_INTEGER_ORBIT0_PETERSEN_INVERSE_DIAGNOSTIC",
        "evidence_role": (
            "counterexample and arithmetic diagnostic only; the proof is the "
            "Petersen even-walk lemma and the five-slice formula"
        ),
        "petersen_nontrivial_subsets_checked": 1022,
        "petersen_overlap_histogram": dict(sorted(petersen_slack.items())),
        "valid_direction_count": valid_count,
        "nontrivial_family_direction_count": nontrivial_family_count,
        "direction_records": direction_records,
        "normalized_plane_slice_formula": slice_formula,
        "former_witness_edges_required": 0,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "petersen_subsets": result["petersen_nontrivial_subsets_checked"],
        "valid_directions": valid_count,
        "nontrivial_family_directions": nontrivial_family_count,
        "former_witness_edges_required": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
