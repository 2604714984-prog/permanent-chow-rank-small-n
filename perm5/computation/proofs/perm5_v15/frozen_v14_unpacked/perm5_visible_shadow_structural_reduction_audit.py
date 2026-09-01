#!/usr/bin/env python3
"""Exact audit for replacing the 7x7 visible-shadow table.

The written proof uses a two-row parent function g_{p,q}(u,v), four short
one-variable sequences, and separate equality descriptions for the three
surviving flags.  The 49 table entries and all 5-subsets of the 25-variable
plane are traversed only as independent integer diagnostics.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_visible_shadow_structural_reduction_exact.json"

TRIPLES = tuple(combinations(range(5), 3))
TRIPLE_INDEX = {value: index for index, value in enumerate(TRIPLES)}
PAIRS = tuple(combinations(range(5), 2))
PAIR_INDEX = {value: index for index, value in enumerate(PAIRS)}
INITIAL_ORDER = (0, 1, 3, 6, 2, 4, 7, 5, 8, 9)
ROW_CHAIN = tuple(TRIPLES[index] for index in INITIAL_ORDER[:4])

FAMILY_PROFILES = (
    (10, 10, 0, 0),
    (10, 4, 4, 2),
    (10, 4, 3, 3),
    (9, 4, 4, 3),
    (8, 4, 4, 4),
    (7, 5, 4, 4),
    (5, 5, 5, 5),
)
PLANE_PARTITIONS = (
    (5, 0, 0, 0, 0),
    (4, 1, 0, 0, 0),
    (3, 2, 0, 0, 0),
    (3, 1, 1, 0, 0),
    (2, 2, 1, 0, 0),
    (2, 1, 1, 1, 0),
    (1, 1, 1, 1, 1),
)


def positions(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


J_MASKS = tuple(sum(1 << index for index in INITIAL_ORDER[:size]) for size in range(11))


def family_from_profile(profile: tuple[int, ...]) -> int:
    result = 0
    for row_index, length in zip(INITIAL_ORDER[:4], profile):
        for column_index in INITIAL_ORDER[:length]:
            result |= 1 << (10 * row_index + column_index)
    return result


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
assert all(len(value) == 9 for value in PARENTS_BY_CHILD)


def parent_masks(family: int) -> tuple[int, ...]:
    result = []
    for records in PARENTS_BY_CHILD:
        mask = 0
        for parent, variable in records:
            if (family >> parent) & 1:
                mask |= 1 << variable
        if mask:
            result.append(mask)
    return tuple(result)


def plane_from_partition(partition: tuple[int, ...]) -> int:
    return sum(
        1 << (5 * row + column)
        for row, length in enumerate(partition)
        for column in range(length)
    )


def killed_count(parents: tuple[int, ...], plane: int) -> int:
    return sum(not (mask & ~plane) for mask in parents)


def missing_columns(size: int, pair: tuple[int, int]) -> frozenset[int]:
    answer = set()
    for column in range(5):
        if column in pair:
            continue
        triple = tuple(sorted(pair + (column,)))
        if (J_MASKS[size] >> TRIPLE_INDEX[triple]) & 1:
            answer.add(column)
    return frozenset(answer)


def contained_in_prefix(values: frozenset[int], length: int) -> bool:
    return not values or max(values) < length


def g(first: int, second: int, first_length: int, second_length: int) -> int:
    result = 0
    for pair in PAIRS:
        first_parents = missing_columns(first, pair)
        second_parents = missing_columns(second, pair)
        if not (first_parents or second_parents):
            continue
        if contained_in_prefix(first_parents, first_length) and contained_in_prefix(
            second_parents, second_length
        ):
            result += 1
    return result


def six_edge_formula(profile: tuple[int, ...], plane: tuple[int, ...]) -> int:
    a, b, c, d = profile
    u0, u1, u2, u3, _u4 = plane
    return (
        g(a, b, u2, u3)
        + g(a, c, u1, u3)
        + g(b, c, u1, u2)
        + g(a, d, u0, u3)
        + g(b, d, u0, u2)
        + g(c, d, u0, u1)
    )


def alpha(size: int) -> tuple[int, ...]:
    return tuple(g(size, size, length, length) for length in range(6))


def structural_closed_form(profile: tuple[int, ...], plane: tuple[int, ...]) -> int:
    u0, u1, u2, u3, _u4 = plane
    if profile == (10, 10, 0, 0):
        return 2 * alpha(10)[u0] + 2 * alpha(10)[u1] + alpha(10)[u3]
    if profile == (10, 4, 3, 3):
        a = (0, 0, 0, 1, 4, 4)
        rho = (0, 0, 1, 2, 3, 3)
        return (
            a[u0]
            + alpha(3)[u1]
            + (rho[u0] if u2 == 1 else 0)
            + int(u1 == 2 and u2 == 1)
        )
    if profile == (9, 4, 4, 3):
        rho = (0, 0, 1, 2, 3, 3)
        sigma = (
            (0, 0, 2, 2, 4, 4)[u0]
            if u3 == 0
            else (3 if u0 == 2 else 0)
        )
        return (
            2 * int(u1 == 2)
            + sigma
            + (rho[u0] if u2 == 1 else 0)
            + (rho[u0] if u1 >= 1 else 0)
        )
    if profile == (8, 4, 4, 4):
        beta = (0, 1, 2, 3, 4, 4)
        return (
            beta[u0]
            + beta[u1]
            + beta[u2]
            + alpha(4)[u1]
            + 2 * alpha(4)[u2]
        )
    if profile == (5, 5, 5, 5):
        return alpha(5)[u1] + 2 * alpha(5)[u2] + 3 * alpha(5)[u3]
    raise ValueError("the surviving type-1/type-13 profiles use parent-set equality lemmas")


def main() -> None:
    assert alpha(3) == (0, 3, 3, 4, 6, 6)
    assert alpha(4) == (0, 0, 1, 3, 6, 6)
    assert alpha(5) == (0, 1, 3, 5, 7, 8)
    assert alpha(10) == (0, 0, 0, 1, 4, 10)

    family_records = []
    visible_table = []
    structural_profiles = {
        (10, 10, 0, 0),
        (10, 4, 3, 3),
        (9, 4, 4, 3),
        (8, 4, 4, 4),
        (5, 5, 5, 5),
    }
    expected_maximum_killed = (20, 8, 7, 7, 6, 9, 6)
    expected_global_maximizer_count = (2, 4, 4, 2, 18, 2, 42)

    for profile, expected_max, expected_count in zip(
        FAMILY_PROFILES, expected_maximum_killed, expected_global_maximizer_count
    ):
        family = family_from_profile(profile)
        parents = parent_masks(family)
        values = []
        for plane_partition in PLANE_PARTITIONS:
            plane = plane_from_partition(plane_partition)
            direct = killed_count(parents, plane)
            edge = six_edge_formula(profile, plane_partition)
            assert direct == edge
            if profile in structural_profiles:
                assert direct == structural_closed_form(profile, plane_partition)
            values.append({
                "plane_partition": list(plane_partition),
                "killed": direct,
                "visible": len(parents) - direct,
            })
        visible_table.append([record["visible"] for record in values])

        global_maximum = -1
        global_count = 0
        examples = []
        for cells in combinations(range(25), 5):
            plane = sum(1 << value for value in cells)
            value = killed_count(parents, plane)
            if value > global_maximum:
                global_maximum = value
                global_count = 1
                examples = [cells]
            elif value == global_maximum:
                global_count += 1
                if len(examples) < 8:
                    examples.append(cells)
        assert global_maximum == expected_max
        assert global_count == expected_count
        family_records.append({
            "profile": list(profile),
            "shadow_size": len(parents),
            "ferrers_plane_values": values,
            "maximum_killed_over_all_five_planes": global_maximum,
            "minimum_visible_over_all_five_planes": len(parents) - global_maximum,
            "global_maximizer_count": global_count,
            "global_maximizer_examples": [list(value) for value in examples],
            "parent_mask_size_histogram": {
                str(size): count
                for size, count in sorted(Counter(mask.bit_count() for mask in parents).items())
            },
        })

    assert visible_table == [
        [30, 42, 48, 48, 50, 50, 50],
        [41, 40, 43, 43, 46, 46, 48],
        [44, 41, 44, 42, 43, 44, 45],
        [44, 41, 42, 42, 42, 43, 48],
        [44, 43, 42, 43, 42, 44, 45],
        [44, 43, 40, 43, 42, 45, 47],
        [48, 47, 45, 45, 43, 42, 42],
    ]
    ferrers_survivors = [
        (family_index, plane_index)
        for family_index, row in enumerate(visible_table)
        for plane_index, value in enumerate(row)
        if value <= 40
    ]
    assert ferrers_survivors == [(0, 0), (1, 1), (5, 2)]

    result = {
        "status": "PASS_EXACT_INTEGER_VISIBLE_SHADOW_STRUCTURAL_REDUCTION_AUDIT",
        "evidence_role": (
            "exact diagnostic for the written six-edge parent formula and "
            "closed structural bounds; the 49 values are not an active proof dependency"
        ),
        "alpha_sequences": {
            str(size): list(alpha(size)) for size in (3, 4, 5, 10)
        },
        "family_records": family_records,
        "diagnostic_visible_table": visible_table,
        "ferrers_survivors": [list(value) for value in ferrers_survivors],
        "summary": {
            "family_profiles": 7,
            "plane_partitions": 7,
            "diagnostic_pair_values_checked": 49,
            "five_planes_checked_per_family": 53130,
            "shifted_survivor_count": 3,
            "active_49_value_table_required": False,
            "non_survivor_uniform_visible_lower_bounds": [41, 41, 42, 42],
        },
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": result["status"],
        **result["summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
