#!/usr/bin/env python3
"""Exact audit of the layer-defect reduction for shifted size profiles.

The proof used in the paper is the identity

    B(k) - Phi(sort(k))
      = sum_j Delta_n(j) (|d H_j| - n(|H_j|)),

where H_j={R:k_R>=j}.  This script reconstructs the ten-element
componentwise poset, its sixteen ideals, the fourteen low Ferrers
partitions, and every equality/stability datum using exact integers only.

The final traversal of all 1405 order-reversing profiles is an independent
diagnostic of the written identity.  It is not an active proof dependency.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_shifted_profile_layer_defect_exact.json"

TRIPLES = tuple(combinations(range(5), 3))
PAIRS = tuple(combinations(range(5), 2))
PAIR_INDEX = {value: index for index, value in enumerate(PAIRS)}
INITIAL_ORDER = (0, 1, 3, 6, 2, 4, 7, 5, 8, 9)


def positions(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


PREDECESSOR_MASKS = tuple(
    sum(
        1 << other_index
        for other_index, other in enumerate(TRIPLES)
        if other_index != index
        and all(first <= second for first, second in zip(other, triple))
    )
    for index, triple in enumerate(TRIPLES)
)

ONE_SHADOW_MASKS = tuple(
    sum(1 << PAIR_INDEX[pair] for pair in combinations(triple, 2))
    for triple in TRIPLES
)


def is_ideal(mask: int) -> bool:
    return all(
        not ((mask >> index) & 1) or not (PREDECESSOR_MASKS[index] & ~mask)
        for index in range(10)
    )


IDEALS = tuple(mask for mask in range(1 << 10) if is_ideal(mask))
assert len(IDEALS) == 16
IDEALS_BY_SIZE = {
    size: tuple(mask for mask in IDEALS if mask.bit_count() == size)
    for size in range(11)
}


def one_shadow_mask(ideal: int) -> int:
    result = 0
    for index in positions(ideal):
        result |= ONE_SHADOW_MASKS[index]
    return result


SHADOW_SIZE = {ideal: one_shadow_mask(ideal).bit_count() for ideal in IDEALS}
N_PROFILE = tuple(
    min(SHADOW_SIZE[ideal] for ideal in IDEALS_BY_SIZE[size])
    for size in range(11)
)
assert N_PROFILE == (0, 3, 5, 6, 6, 8, 9, 9, 10, 10, 10)
DELTA = tuple(
    N_PROFILE[index] - N_PROFILE[index - 1] for index in range(1, 11)
)
assert DELTA == (3, 2, 1, 0, 2, 1, 0, 1, 0, 0)

CANONICAL_IDEAL = {}
for size in range(11):
    minimizers = [
        ideal
        for ideal in IDEALS_BY_SIZE[size]
        if SHADOW_SIZE[ideal] == N_PROFILE[size]
    ]
    assert len(minimizers) == 1
    CANONICAL_IDEAL[size] = minimizers[0]

NONCANONICAL_IDEALS = tuple(
    ideal
    for ideal in IDEALS
    if SHADOW_SIZE[ideal] > N_PROFILE[ideal.bit_count()]
)
assert tuple(ideal.bit_count() for ideal in NONCANONICAL_IDEALS) == (3, 4, 5, 6, 7)
assert tuple(
    SHADOW_SIZE[ideal] - N_PROFILE[ideal.bit_count()]
    for ideal in NONCANONICAL_IDEALS
) == (1, 2, 1, 1, 1)


def new_shadow_coefficients() -> tuple[int, ...]:
    seen = 0
    answer = []
    for index in INITIAL_ORDER:
        shadow = ONE_SHADOW_MASKS[index]
        answer.append((shadow & ~seen).bit_count())
        seen |= shadow
    return tuple(answer)


COEFFICIENTS = new_shadow_coefficients()
assert COEFFICIENTS == (3, 2, 1, 0, 2, 1, 0, 1, 0, 0)


def partitions(total: int, length: int, upper: int):
    if length == 0:
        if total == 0:
            yield ()
        return
    for value in range(min(upper, total), -1, -1):
        for tail in partitions(total - value, length - 1, value):
            yield (value,) + tail


def ferrers_shadow(partition: tuple[int, ...]) -> int:
    return sum(
        coefficient * N_PROFILE[value]
        for coefficient, value in zip(COEFFICIENTS, partition)
    )


def conjugate(partition: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(value >= level for value in partition) for level in range(1, 11))


def profile_bound(profile: tuple[int, ...]) -> int:
    return sum(
        N_PROFILE[
            max(
                profile[index]
                for index, triple in enumerate(TRIPLES)
                if set(pair) <= set(triple)
            )
        ]
        for pair in PAIRS
    )


def level_ideals(profile: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(1 << index for index, value in enumerate(profile) if value >= level)
        for level in range(1, 11)
    )


def layer_defect(levels: tuple[int, ...]) -> int:
    return sum(
        DELTA[level - 1]
        * (SHADOW_SIZE[ideal] - N_PROFILE[ideal.bit_count()])
        for level, ideal in enumerate(levels, 1)
    )


def profile_from_levels(levels: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum((ideal >> index) & 1 for ideal in levels)
        for index in range(10)
    )


def chains_with_layer_sizes(sizes: tuple[int, ...]):
    answer = []

    def visit(level: int, previous: int, chosen: list[int]) -> None:
        if level == 10:
            answer.append(tuple(chosen))
            return
        for ideal in IDEALS_BY_SIZE[sizes[level]]:
            if not (ideal & ~previous):
                visit(level + 1, ideal, chosen + [ideal])

    visit(0, (1 << 10) - 1, [])
    return tuple(answer)


def nested_fibre_chains(partition: tuple[int, ...]):
    lengths = tuple(value for value in partition if value)
    answer = []

    def visit(index: int, previous: int, chosen: list[int]) -> None:
        if index == len(lengths):
            answer.append(tuple(chosen))
            return
        for ideal in IDEALS_BY_SIZE[lengths[index]]:
            if not (ideal & ~previous):
                visit(index + 1, ideal, chosen + [ideal])

    visit(0, (1 << 10) - 1, [])
    return tuple(answer)


def ideal_record(ideal: int) -> dict:
    size = ideal.bit_count()
    return {
        "vertices": list(positions(ideal)),
        "size": size,
        "shadow_size": SHADOW_SIZE[ideal],
        "defect": SHADOW_SIZE[ideal] - N_PROFILE[size],
    }


def main() -> None:
    low_partitions = tuple(
        partition
        for partition in partitions(20, 10, 10)
        if ferrers_shadow(partition) <= 50
    )
    assert len(low_partitions) == 14

    partition_records = []
    canonical_low_profiles = set()
    for partition in low_partitions:
        phi = ferrers_shadow(partition)
        sizes = conjugate(partition)
        chains = chains_with_layer_sizes(sizes)
        chain_records = []
        for chain in chains:
            profile = profile_from_levels(chain)
            defect = layer_defect(chain)
            bound = profile_bound(profile)
            assert tuple(sorted(profile, reverse=True)) == partition
            assert bound == phi + defect
            canonical = all(
                ideal == CANONICAL_IDEAL[size]
                for ideal, size in zip(chain, sizes)
            )
            if bound <= 50:
                assert canonical
                canonical_low_profiles.add(profile)
            chain_records.append({
                "defect": defect,
                "bound": bound,
                "canonical": canonical,
                "profile": list(profile),
            })
        noncanonical_defects = [
            record["defect"] for record in chain_records if not record["canonical"]
        ]
        partition_records.append({
            "partition": list(partition),
            "conjugate_layer_sizes": list(sizes),
            "ferrers_shadow": phi,
            "available_slack_to_50": 50 - phi,
            "compatible_ideal_chain_count": len(chains),
            "minimum_noncanonical_defect": (
                min(noncanonical_defects) if noncanonical_defects else None
            ),
            "chain_records": chain_records,
        })

    assert len(canonical_low_profiles) == 14

    primary_fibre_records = []
    primary_partitions = tuple(
        partition for partition in low_partitions if sum(bool(x) for x in partition) <= 4
    )
    assert len(primary_partitions) == 7
    for partition in primary_partitions:
        phi = ferrers_shadow(partition)
        chains = nested_fibre_chains(partition)
        records = []
        for chain in chains:
            defect = sum(
                COEFFICIENTS[index]
                * (
                    SHADOW_SIZE[ideal]
                    - N_PROFILE[ideal.bit_count()]
                )
                for index, ideal in enumerate(chain)
            )
            canonical = all(
                ideal == CANONICAL_IDEAL[length]
                for ideal, length in zip(chain, (x for x in partition if x))
            )
            records.append({
                "defect": defect,
                "shadow_size": phi + defect,
                "canonical": canonical,
                "fibres": [list(positions(ideal)) for ideal in chain],
            })
        good = [record for record in records if record["shadow_size"] <= 50]
        assert len(good) == 1 and good[0]["canonical"]
        noncanonical = [record["defect"] for record in records if not record["canonical"]]
        primary_fibre_records.append({
            "partition": list(partition),
            "ferrers_shadow": phi,
            "available_slack_to_50": 50 - phi,
            "compatible_fibre_chain_count": len(chains),
            "minimum_noncanonical_fibre_defect": (
                min(noncanonical) if noncanonical else None
            ),
            "chain_records": records,
        })

    row_predecessors = tuple(
        tuple(
            other_index
            for other_index, other in enumerate(TRIPLES[:index])
            if all(first <= second for first, second in zip(other, triple))
        )
        for index, triple in enumerate(TRIPLES)
    )
    profile_count = 0
    identity_count = 0
    low_profiles = set()
    defect_histogram = defaultdict(int)

    def visit_profile(index: int, values: list[int], remaining: int) -> None:
        nonlocal profile_count, identity_count
        if index == 10:
            if remaining:
                return
            profile = tuple(values)
            profile_count += 1
            levels = level_ideals(profile)
            assert all(is_ideal(ideal) for ideal in levels)
            phi = ferrers_shadow(tuple(sorted(profile, reverse=True)))
            defect = layer_defect(levels)
            bound = profile_bound(profile)
            assert bound == phi + defect
            identity_count += 1
            defect_histogram[defect] += 1
            if bound <= 50:
                low_profiles.add(profile)
            return
        upper = min(
            [values[parent] for parent in row_predecessors[index]] or [10]
        )
        upper = min(upper, remaining)
        for value in range(upper, -1, -1):
            visit_profile(index + 1, values + [value], remaining - value)

    visit_profile(0, [], 20)
    assert profile_count == 1405
    assert identity_count == profile_count
    assert low_profiles == canonical_low_profiles

    result = {
        "status": "PASS_EXACT_INTEGER_LAYER_DEFECT_REDUCTION_AUDIT",
        "evidence_role": (
            "exact diagnostic for a written layer-defect identity; the final "
            "1405-profile traversal is not an active proof dependency"
        ),
        "one_dimensional_ideal_count": len(IDEALS),
        "neighbourhood_profile": list(N_PROFILE),
        "increments": list(DELTA),
        "new_shadow_coefficients": list(COEFFICIENTS),
        "noncanonical_ideal_records": [
            ideal_record(ideal) for ideal in NONCANONICAL_IDEALS
        ],
        "low_partition_records": partition_records,
        "primary_fibre_chain_records": primary_fibre_records,
        "diagnostic": {
            "order_reversing_profiles_checked": profile_count,
            "layer_defect_identities_checked": identity_count,
            "low_ferrers_partition_count": len(low_partitions),
            "low_profile_count": len(low_profiles),
            "noncanonical_low_profile_count": 0,
            "defect_histogram": {
                str(value): count for value, count in sorted(defect_histogram.items())
            },
        },
        "proof_dependency": {
            "active_1405_profile_enumeration_required": False,
            "active_ideal_data_rows": 16,
            "active_low_partition_pairs": 7,
            "maximum_chains_per_low_partition": max(
                record["compatible_ideal_chain_count"]
                for record in partition_records
            ),
            "maximum_fibre_chains_per_primary_partition": max(
                record["compatible_fibre_chain_count"]
                for record in primary_fibre_records
            ),
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
        "order_reversing_profiles_checked": profile_count,
        "low_ferrers_partition_count": len(low_partitions),
        "low_profile_count": len(low_profiles),
        "maximum_chains_per_low_partition": result["proof_dependency"][
            "maximum_chains_per_low_partition"
        ],
        "maximum_fibre_chains_per_primary_partition": result[
            "proof_dependency"
        ]["maximum_fibre_chains_per_primary_partition"],
        "active_1405_profile_enumeration_required": False,
    }, indent=2))


if __name__ == "__main__":
    main()
