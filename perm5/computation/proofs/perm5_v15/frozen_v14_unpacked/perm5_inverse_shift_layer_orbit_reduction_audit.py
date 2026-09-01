#!/usr/bin/env python3
"""Exact audit for replacing the 42 inverse-shift direction records.

The written proof uses the layer-defect identity for an arbitrary Petersen
fibre-size profile, the fourteen low Ferrers partitions, and equality rigidity
for four- and seven-vertex Petersen neighbourhood minimizers.  This script
independently reconstructs those objects with exact integers.  Its traversal of
all ground-set transpositions is diagnostic, not an active proof dependency.
"""

from __future__ import annotations

from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_inverse_shift_layer_orbit_reduction_exact.json"

POINTS = tuple(range(5))
EDGES = tuple(combinations(POINTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRANSPOSITIONS = tuple(combinations(POINTS, 2))

NEIGHBOUR_MASKS = tuple(
    sum(
        1 << other_index
        for other_index, other in enumerate(EDGES)
        if set(edge).isdisjoint(other)
    )
    for edge in EDGES
)

N_PROFILE = (0, 3, 5, 6, 6, 8, 9, 9, 10, 10, 10)
DELTA = tuple(
    N_PROFILE[index] - N_PROFILE[index - 1]
    for index in range(1, 11)
)
assert DELTA == (3, 2, 1, 0, 2, 1, 0, 1, 0, 0)


def positions(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def neighbourhood_mask(mask: int) -> int:
    answer = 0
    for index in positions(mask):
        answer |= NEIGHBOUR_MASKS[index]
    return answer


def partitions(total: int, length: int, upper: int):
    if length == 0:
        if total == 0:
            yield ()
        return
    for value in range(min(total, upper), -1, -1):
        for tail in partitions(total - value, length - 1, value):
            yield (value,) + tail


def ferrers_shadow(partition: tuple[int, ...]) -> int:
    return sum(
        coefficient * N_PROFILE[value]
        for coefficient, value in zip(DELTA, partition)
    )


LOW_PARTITIONS = tuple(
    partition
    for partition in partitions(20, 10, 10)
    if ferrers_shadow(partition) <= 50
)
assert len(LOW_PARTITIONS) == 14


def profile_bound(profile: tuple[int, ...]) -> int:
    return sum(
        N_PROFILE[
            max(
                profile[other_index]
                for other_index, other in enumerate(EDGES)
                if set(edge).isdisjoint(other)
            )
        ]
        for edge in EDGES
    )


def layer_defect(profile: tuple[int, ...]) -> int:
    answer = 0
    for level, coefficient in enumerate(DELTA, 1):
        if coefficient == 0:
            continue
        level_mask = sum(
            1 << index
            for index, value in enumerate(profile)
            if value >= level
        )
        size = level_mask.bit_count()
        defect = neighbourhood_mask(level_mask).bit_count() - N_PROFILE[size]
        assert defect >= 0
        answer += coefficient * defect
    return answer


def profile_from_edge_values(values: dict[tuple[int, int], int]) -> tuple[int, ...]:
    return tuple(values.get(edge, 0) for edge in EDGES)


PROFILES = {
    "row_type1": profile_from_edge_values({
        (0, 4): 2,
        (1, 4): 4,
        (2, 4): 4,
        (3, 4): 10,
    }),
    "row_type13": profile_from_edge_values({
        (0, 4): 4,
        (1, 4): 4,
        (2, 4): 5,
        (3, 4): 7,
    }),
    "column_type1": profile_from_edge_values({
        (0, 1): 1,
        (0, 2): 1,
        (0, 3): 1,
        (0, 4): 3,
        (1, 2): 1,
        (1, 3): 1,
        (1, 4): 3,
        (2, 3): 1,
        (2, 4): 4,
        (3, 4): 4,
    }),
    "column_type13": profile_from_edge_values({
        (0, 3): 1,
        (0, 4): 4,
        (1, 3): 1,
        (1, 4): 4,
        (2, 3): 2,
        (2, 4): 4,
        (3, 4): 4,
    }),
}

assert tuple(sorted(PROFILES["row_type1"], reverse=True)) == (
    10, 4, 4, 2, 0, 0, 0, 0, 0, 0
)
assert tuple(sorted(PROFILES["row_type13"], reverse=True)) == (
    7, 5, 4, 4, 0, 0, 0, 0, 0, 0
)
assert tuple(sorted(PROFILES["column_type1"], reverse=True)) == (
    4, 4, 3, 3, 1, 1, 1, 1, 1, 1
)
assert tuple(sorted(PROFILES["column_type13"], reverse=True)) == (
    4, 4, 4, 4, 2, 1, 1, 0, 0, 0
)


def permuted_edge(edge: tuple[int, int], permutation: tuple[int, ...]):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def stabilizer(profile: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    answer = []
    for permutation in permutations(POINTS):
        moved = [0] * len(EDGES)
        for edge, value in zip(EDGES, profile):
            moved[EDGE_INDEX[permuted_edge(edge, permutation)]] = value
        if tuple(moved) == profile:
            answer.append(permutation)
    return tuple(answer)


def transposition_orbits(profile: tuple[int, ...]):
    group = stabilizer(profile)
    remaining = set(TRANSPOSITIONS)
    answer = []
    while remaining:
        representative = min(remaining)
        orbit = {
            tuple(sorted((permutation[representative[0]], permutation[representative[1]])))
            for permutation in group
        }
        remaining -= orbit
        answer.append(tuple(sorted(orbit)))
    return tuple(answer)


def transfer_pairs(profile: tuple[int, ...], transposition: tuple[int, int]):
    first, second = transposition
    answer = []
    for third in POINTS:
        if third in transposition:
            continue
        first_edge = tuple(sorted((first, third)))
        second_edge = tuple(sorted((second, third)))
        first_index = EDGE_INDEX[first_edge]
        second_index = EDGE_INDEX[second_edge]
        first_value = profile[first_index]
        second_value = profile[second_index]
        if first_value == second_value:
            continue
        if first_value > second_value:
            answer.append((first_index, second_index, first_value, second_value))
        else:
            answer.append((second_index, first_index, second_value, first_value))
    return tuple(sorted(answer, key=lambda item: (-item[2], -item[3], item[0], item[1])))


def moved_profile(profile, pairs, counts):
    answer = list(profile)
    for (large_index, small_index, large, small), moved in zip(pairs, counts):
        answer[large_index] = large - moved
        answer[small_index] = small + moved
    return tuple(answer)


def scheme(pairs):
    return tuple((large, small) for _li, _si, large, small in pairs)


def record_transposition(profile_name: str, transposition):
    profile = PROFILES[profile_name]
    pairs = transfer_pairs(profile, transposition)
    widths = tuple(large - small for _li, _si, large, small in pairs)
    good = []
    for counts in product(*(range(width + 1) for width in widths)):
        candidate = moved_profile(profile, pairs, counts)
        partition = tuple(sorted(candidate, reverse=True))
        phi = ferrers_shadow(partition)
        bound = profile_bound(candidate)
        defect = layer_defect(candidate)
        assert bound == phi + defect
        if bound <= 50:
            good.append({
                "counts": list(counts),
                "partition": list(partition),
                "ferrers_shadow": phi,
                "layer_defect": defect,
                "bound": bound,
            })
    endpoints = {tuple(0 for _ in widths), widths}
    noncoherent = [
        item for item in good if tuple(item["counts"]) not in endpoints
    ]
    return {
        "transposition": list(transposition),
        "scheme": [list(value) for value in scheme(pairs)],
        "widths": list(widths),
        "good_count_vectors": good,
        "noncoherent_good_count": len(noncoherent),
    }


def star_mask(center: int) -> int:
    return sum(
        1 << EDGE_INDEX[tuple(sorted((center, other)))]
        for other in POINTS
        if other != center
    )


def main() -> None:
    # Petersen isoperimetry used by the written equality-rigidity proof.
    size_four_minimizers = []
    size_seven_minimizers = []
    for cells in combinations(range(10), 4):
        mask = sum(1 << value for value in cells)
        if neighbourhood_mask(mask).bit_count() == N_PROFILE[4]:
            size_four_minimizers.append(mask)
    for cells in combinations(range(10), 7):
        mask = sum(1 << value for value in cells)
        if neighbourhood_mask(mask).bit_count() == N_PROFILE[7]:
            size_seven_minimizers.append(mask)
    assert set(size_four_minimizers) == {star_mask(center) for center in POINTS}
    expected_seven = {
        ((1 << 10) - 1) ^ NEIGHBOUR_MASKS[index]
        for index in range(10)
    }
    assert set(size_seven_minimizers) == expected_seven

    expected_stabilizers = {
        "row_type1": 2,
        "row_type13": 2,
        "column_type1": 4,
        "column_type13": 2,
    }
    expected_orbits = {
        "row_type1": 7,
        "row_type13": 7,
        "column_type1": 5,
        "column_type13": 7,
    }
    exceptional = {
        ("row_type1", (0, 1)),
        ("row_type1", (0, 2)),
        ("row_type1", (0, 3)),
        ("column_type13", (0, 3)),
        ("column_type13", (1, 3)),
    }

    profile_records = {}
    discovered_exceptional = set()
    for profile_name, profile in PROFILES.items():
        group = stabilizer(profile)
        orbits = transposition_orbits(profile)
        assert len(group) == expected_stabilizers[profile_name]
        assert len(orbits) == expected_orbits[profile_name]
        records = []
        for transposition in TRANSPOSITIONS:
            record = record_transposition(profile_name, transposition)
            if record["noncoherent_good_count"]:
                discovered_exceptional.add((profile_name, transposition))
            records.append(record)
        profile_records[profile_name] = {
            "profile": list(profile),
            "sorted_partition": list(sorted(profile, reverse=True)),
            "stabilizer_size": len(group),
            "transposition_orbit_count": len(orbits),
            "transposition_orbits": [
                [list(value) for value in orbit] for orbit in orbits
            ],
            "diagnostic_transposition_records": records,
        }

    assert discovered_exceptional == exceptional

    # Exact exceptional count-vector patterns used before the stronger union bound.
    def good_counts(profile_name, transposition):
        record = profile_records[profile_name]["diagnostic_transposition_records"]
        found = next(
            item for item in record
            if tuple(item["transposition"]) == transposition
        )
        return tuple(tuple(item["counts"]) for item in found["good_count_vectors"])

    assert good_counts("row_type1", (0, 1)) == ((0,), (1,), (2,))
    assert good_counts("row_type1", (0, 2)) == ((0,), (1,), (2,))
    assert good_counts("row_type1", (0, 3)) == (
        (0,), (1,), (2,), (3,), (5,), (6,), (7,), (8,)
    )
    assert good_counts("column_type13", (0, 3)) == (
        (0, 0), (1, 0), (1, 1), (2, 1)
    )
    assert good_counts("column_type13", (1, 3)) == (
        (0, 0), (1, 0), (1, 1), (2, 1)
    )

    result = {
        "status": "PASS_EXACT_INTEGER_INVERSE_SHIFT_LAYER_ORBIT_REDUCTION_AUDIT",
        "evidence_role": (
            "diagnostic for the arbitrary-profile layer identity, stabilizer orbit "
            "schemes, and Petersen equality cases; no 42-row direction table is "
            "an active proof dependency"
        ),
        "n_profile": list(N_PROFILE),
        "delta": list(DELTA),
        "low_partitions": [list(value) for value in LOW_PARTITIONS],
        "four_vertex_minimizer_count": len(size_four_minimizers),
        "seven_vertex_minimizer_count": len(size_seven_minimizers),
        "profiles": profile_records,
        "summary": {
            "base_profiles": 4,
            "diagnostic_unordered_transpositions": 40,
            "stabilizer_transposition_orbit_types": sum(expected_orbits.values()),
            "exceptional_movement_schemes": 3,
            "exceptional_transpositions": 5,
            "active_42_direction_table_required": False,
            "remaining_nonuniform_family_states_after_union_bounds": 14,
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
