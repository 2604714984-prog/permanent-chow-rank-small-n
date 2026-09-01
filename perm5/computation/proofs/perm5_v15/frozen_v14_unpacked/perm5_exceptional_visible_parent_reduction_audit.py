#!/usr/bin/env python3
"""Exact audit for replacing the fourteen exceptional visible-shadow rows.

The written proof uses three parent-set formulas: a three-bit polynomial for
the type-1 (4,2) transfer, a seven-element potential-parent set for the
type-1 (10,2) transfer, and a two-bit polynomial for the type-13 column
transfer.  This script rebuilds every parent set from the coordinate
definitions using exact integer bit masks.  The final 160 compatible
family/plane evaluations are diagnostic only.
"""

from __future__ import annotations

from itertools import combinations, product
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_exceptional_visible_parent_reduction_exact.json"

TRIPLES = tuple(combinations(range(5), 3))
PAIRS = tuple(combinations(range(5), 2))
TRIPLE_INDEX = {value: index for index, value in enumerate(TRIPLES)}
PAIR_INDEX = {value: index for index, value in enumerate(PAIRS)}
INITIAL_ORDER = (0, 1, 3, 6, 2, 4, 7, 5, 8, 9)


def positions(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def family_from_shape(shape: tuple[int, ...]) -> int:
    answer = 0
    for row_index, row_length in zip(INITIAL_ORDER[:4], shape):
        for column_index in INITIAL_ORDER[:row_length]:
            answer |= 1 << (10 * row_index + column_index)
    return answer


def plane_from_partition(partition: tuple[int, ...]) -> int:
    return sum(
        1 << (5 * row + column)
        for row, length in enumerate(partition)
        for column in range(length)
    )


def reflection_pairs(axis: int, low: int, high: int, size: int):
    pairs = []
    if size == 100:
        # Preserve the intrinsic triple-first ordering used in the proof:
        # each high-containing triple is lowered once, followed by the ten
        # choices in the transverse coordinate.  The order matters only for
        # naming the Boolean orientation variables.
        for high_triple in TRIPLES:
            if high not in high_triple or low in high_triple:
                continue
            low_triple = tuple(
                sorted((set(high_triple) - {high}) | {low})
            )
            low_index = TRIPLE_INDEX[low_triple]
            high_index = TRIPLE_INDEX[high_triple]
            for other in range(10):
                pairs.append(
                    (10 * low_index + other, 10 * high_index + other)
                    if axis == 0
                    else (10 * other + low_index, 10 * other + high_index)
                )
    else:
        if axis == 0:
            pairs.extend((5 * low + column, 5 * high + column) for column in range(5))
        else:
            pairs.extend((5 * row + low, 5 * row + high) for row in range(5))
    # Each two-orbit appears once; source is the compressed low position.
    return tuple(pairs)


def compressed_preimage_data(mask: int, pairs):
    fixed = mask
    movable = []
    for first, second in pairs:
        first_in = bool((mask >> first) & 1)
        second_in = bool((mask >> second) & 1)
        if second_in and not first_in:
            return None
        if first_in and not second_in:
            fixed &= ~(1 << first)
            movable.append((first, second))
    return fixed, tuple(movable)


def oriented_mask(fixed: int, movable, assignment: int) -> int:
    answer = fixed
    for index, (first, second) in enumerate(movable):
        answer |= 1 << (second if (assignment >> index) & 1 else first)
    return answer


PARENTS_BY_CHILD = [[] for _ in range(100)]
for row_index, row_triple in enumerate(TRIPLES):
    for column_index, column_triple in enumerate(TRIPLES):
        parent = 10 * row_index + column_index
        for row_pair in combinations(row_triple, 2):
            missing_row = next(value for value in row_triple if value not in row_pair)
            for column_pair in combinations(column_triple, 2):
                missing_column = next(
                    value for value in column_triple if value not in column_pair
                )
                child = 10 * PAIR_INDEX[row_pair] + PAIR_INDEX[column_pair]
                variable = 5 * missing_row + missing_column
                PARENTS_BY_CHILD[child].append((parent, variable))
assert all(len(records) == 9 for records in PARENTS_BY_CHILD)


def child_name(child: int) -> str:
    row_pair = "".join(str(value) for value in PAIRS[child // 10])
    column_pair = "".join(str(value) for value in PAIRS[child % 10])
    return f"{row_pair},{column_pair}"


def parent_records(family: int):
    answer = []
    for child, records in enumerate(PARENTS_BY_CHILD):
        parent_mask = 0
        for parent, variable in records:
            if (family >> parent) & 1:
                parent_mask |= 1 << variable
        if parent_mask:
            answer.append((child_name(child), parent_mask))
    return tuple(answer)


def killed_count(family: int, plane: int) -> int:
    return sum(
        not (parent_mask & ~plane)
        for _name, parent_mask in parent_records(family)
    )


def compatible_case(shape, plane_partition, axis, low, high):
    family = family_from_shape(shape)
    plane = plane_from_partition(plane_partition)
    family_pairs = reflection_pairs(axis, low, high, 100)
    plane_pairs = reflection_pairs(axis, low, high, 25)
    family_data = compressed_preimage_data(family, family_pairs)
    plane_data = compressed_preimage_data(plane, plane_pairs)
    assert family_data is not None and plane_data is not None
    return family_data, plane_data


def potential_children(family: int, planes) -> tuple[str, ...]:
    answer = []
    for name, parent_mask in parent_records(family):
        if any(not (parent_mask & ~plane) for plane in planes):
            answer.append(name)
    return tuple(answer)


def type1_small_polynomial(bits: tuple[int, int, int]) -> int:
    z0, z1, z2 = bits
    positive = z0 * z1 + z0 * z2 + z1 * z2 + z0 * z1 * z2
    y0, y1, y2 = 1 - z0, 1 - z1, 1 - z2
    negative = y0 * y1 + y0 * y2 + y1 * y2 + y0 * y1 * y2
    crossing = y0 + y1 + y2
    return positive + negative + crossing


def type1_four_polynomial(bits: tuple[int, int, int, int]) -> int:
    z0, z1, z2, z3 = bits
    values = (z0, z1, z2, z3)
    complements = tuple(1 - value for value in values)
    positive = sum(
        values[i] * values[j] * values[k]
        for i, j, k in combinations(range(4), 3)
    )
    negative = sum(
        complements[i] * complements[j] * complements[k]
        for i, j, k in combinations(range(4), 3)
    )
    crossing = z0 * (1 - z1) + (1 - z0) * (
        (1 - z1) + (1 - z2) + (1 - z3)
    )
    return positive + negative + crossing


def type13_polynomial(bits: tuple[int, int]) -> int:
    z0, z1 = bits
    return 7 - 2 * z0 - z1 + 2 * z0 * z1


def main() -> None:
    diagnostic_assignments = 0
    records = []

    # Type 1, (4,2): row 0<-1 and its stabilizer mate row 0<-2.
    for low, high in ((0, 1), (0, 2)):
        family_data, plane_data = compatible_case(
            (10, 4, 4, 2), (4, 1), 0, low, high
        )
        family_fixed, family_movable = family_data
        plane_fixed, plane_movable = plane_data
        assert len(family_movable) == 2
        assert len(plane_movable) == (3 if high == 1 else 4)
        for family_assignment in (1, 2):
            family = oriented_mask(
                family_fixed, family_movable, family_assignment
            )
            assert len(parent_records(family)) == 48
            values = []
            for plane_assignment in range(1 << len(plane_movable)):
                plane = oriented_mask(plane_fixed, plane_movable, plane_assignment)
                bits = tuple(
                    (plane_assignment >> index) & 1
                    for index in range(len(plane_movable))
                )
                polynomial = (
                    type1_small_polynomial
                    if low == 0 and high == 1
                    else type1_four_polynomial
                )
                expected = polynomial(
                    bits
                    if family_assignment == 1
                    else tuple(1 - bit for bit in bits)
                )
                actual = killed_count(family, plane)
                assert actual == expected
                values.append(actual)
                diagnostic_assignments += 1
            assert max(values) == 7
        records.append({
            "case": f"type1_row_{low}<-{high}_pair_4_2",
            "family_states": 2,
            "plane_assignments_per_state": 1 << len(plane_movable),
            "maximum_killed": 7,
            "minimum_visible": 41,
        })

    # Type 1, (10,2): six exact-shadow states after the union bound.
    family_data, plane_data = compatible_case(
        (10, 4, 4, 2), (4, 1), 0, 0, 3
    )
    family_fixed, family_movable = family_data
    plane_fixed, plane_movable = plane_data
    assert len(family_movable) == 8 and len(plane_movable) == 4
    named_assignments = {
        "{3}": 2,
        "{6}": 16,
        "{3,6}": 18,
        "K": 237,
        "K+{3}": 239,
        "K+{6}": 253,
    }
    common = ("12,04", "12,14", "12,24", "12,34")
    expected_potential = {
        "{3}": common + ("23,12", "23,13", "23,23"),
        "{6}": common,
        "{3,6}": common,
        "K": common,
        "K+{3}": common,
        "K+{6}": ("02,12", "02,13", "02,23") + common,
    }
    planes = tuple(
        oriented_mask(plane_fixed, plane_movable, assignment)
        for assignment in range(1 << len(plane_movable))
    )
    for name, family_assignment in named_assignments.items():
        family = oriented_mask(family_fixed, family_movable, family_assignment)
        assert len(parent_records(family)) == 48
        potential = potential_children(family, planes)
        assert set(potential) == set(expected_potential[name])
        assert len(potential) <= 7
        for plane in planes:
            assert killed_count(family, plane) <= len(potential)
            diagnostic_assignments += 1
    records.append({
        "case": "type1_row_0<-3_pair_10_2",
        "family_states": 6,
        "plane_assignments_per_state": len(planes),
        "maximum_potential_children": 7,
        "minimum_visible": 41,
    })

    # Type 13 column exceptions; the second direction is a stabilizer mate.
    for low, high in ((0, 3), (1, 3)):
        family_data, plane_data = compatible_case(
            (7, 5, 4, 4), (3, 2), 1, low, high
        )
        family_fixed, family_movable = family_data
        plane_fixed, plane_movable = plane_data
        assert len(family_movable) == 3 and len(plane_movable) == 2
        for family_assignment in (2, 5):
            family = oriented_mask(
                family_fixed, family_movable, family_assignment
            )
            assert len(parent_records(family)) == 50
            values = []
            for plane_assignment in range(1 << len(plane_movable)):
                plane = oriented_mask(plane_fixed, plane_movable, plane_assignment)
                bits = tuple(
                    (plane_assignment >> index) & 1
                    for index in range(len(plane_movable))
                )
                expected = (
                    type13_polynomial(bits)
                    if family_assignment == 2
                    else type13_polynomial(tuple(1 - bit for bit in bits))
                )
                actual = killed_count(family, plane)
                assert actual == expected
                values.append(actual)
                diagnostic_assignments += 1
            assert max(values) == 7
        records.append({
            "case": f"type13_column_{low}<-{high}",
            "family_states": 2,
            "plane_assignments_per_state": 1 << len(plane_movable),
            "maximum_killed": 7,
            "minimum_visible": 43,
        })

    assert diagnostic_assignments == 160
    assert sum(record["family_states"] for record in records) == 14

    result = {
        "status": "PASS_EXACT_INTEGER_EXCEPTIONAL_VISIBLE_PARENT_REDUCTION_AUDIT",
        "evidence_role": (
            "diagnostic for three written parent-set formulas; the fourteen-row "
            "visible-minimum table is not an active proof dependency"
        ),
        "records": records,
        "summary": {
            "structural_parent_cases": 3,
            "exceptional_directions": 5,
            "nonuniform_family_states": 14,
            "diagnostic_compatible_family_plane_assignments": diagnostic_assignments,
            "maximum_killed_parent_points": 7,
            "uniform_minimum_visible": 41,
            "active_14_state_visible_table_required": False,
        },
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": result["status"], **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
