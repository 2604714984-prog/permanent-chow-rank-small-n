#!/usr/bin/env python3
"""Exact audit of the shifted-terminal stability gap fix.

This verifier is deliberately self-contained.  It constructs the ten
3-subsets, the sixteen one-dimensional componentwise ideals, all
order-reversing size profiles of total area 20, the lower bound B(k), and the
compatible nested fibre ideals for the fourteen surviving profiles.

It is an exact integer/bitset diagnostic, not a proof dependency.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_shifted_terminal_stability_gap_verify_exact.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def positions(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def main() -> None:
    triples = list(combinations(range(5), 3))
    pairs = list(combinations(range(5), 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}

    predecessor_masks: list[int] = []
    one_shadow_masks: list[int] = []
    for index, triple in enumerate(triples):
        predecessor_masks.append(sum(
            1 << other_index
            for other_index, other in enumerate(triples)
            if other_index != index
            and all(first <= second for first, second in zip(other, triple))
        ))
        one_shadow_masks.append(sum(
            1 << pair_index[pair] for pair in combinations(triple, 2)
        ))

    def is_ideal(mask: int) -> bool:
        return all(
            not (mask >> index & 1)
            or not (predecessor_masks[index] & ~mask)
            for index in range(10)
        )

    ideals = [mask for mask in range(1 << 10) if is_ideal(mask)]
    assert len(ideals) == 16
    ideals_by_size = {
        size: [mask for mask in ideals if mask.bit_count() == size]
        for size in range(11)
    }

    def one_shadow(mask: int) -> int:
        result = 0
        for index in positions(mask):
            result |= one_shadow_masks[index]
        return result

    n = [
        min(one_shadow(mask).bit_count() for mask in ideals_by_size[size])
        for size in range(11)
    ]
    assert n == [0, 3, 5, 6, 6, 8, 9, 9, 10, 10, 10]

    row_predecessors = [
        [
            other_index
            for other_index, other in enumerate(triples[:index])
            if all(first <= second for first, second in zip(other, triple))
        ]
        for index, triple in enumerate(triples)
    ]

    profiles: list[tuple[int, tuple[int, ...]]] = []

    def profile_lower_bound(profile: tuple[int, ...]) -> int:
        result = 0
        for pair in pairs:
            maximum = max(
                profile[index]
                for index, triple in enumerate(triples)
                if set(pair) <= set(triple)
            )
            result += n[maximum]
        return result

    profile_count = 0

    def visit_profile(index: int, values: list[int], remaining: int) -> None:
        nonlocal profile_count
        if index == 10:
            if remaining == 0:
                profile_count += 1
                profile = tuple(values)
                lower_bound = profile_lower_bound(profile)
                if lower_bound <= 50:
                    profiles.append((lower_bound, profile))
            return
        upper = min(
            min(
                [values[parent] for parent in row_predecessors[index]]
                or [10]
            ),
            remaining,
        )
        for value in range(upper, -1, -1):
            visit_profile(index + 1, values + [value], remaining - value)

    visit_profile(0, [], 20)
    assert profile_count == 1405

    expected_profiles = {
        (48, (4, 4, 1, 3, 1, 1, 3, 1, 1, 1)),
        (48, (4, 4, 1, 4, 1, 1, 2, 1, 1, 1)),
        (48, (4, 4, 1, 4, 1, 1, 3, 1, 1, 0)),
        (48, (4, 4, 1, 4, 1, 1, 4, 1, 0, 0)),
        (48, (4, 4, 4, 4, 0, 0, 4, 0, 0, 0)),
        (48, (5, 5, 0, 5, 0, 0, 5, 0, 0, 0)),
        (48, (8, 4, 0, 4, 0, 0, 4, 0, 0, 0)),
        (48, (9, 4, 0, 4, 0, 0, 3, 0, 0, 0)),
        (48, (10, 4, 0, 3, 0, 0, 3, 0, 0, 0)),
        (48, (10, 4, 0, 4, 0, 0, 2, 0, 0, 0)),
        (49, (4, 4, 2, 4, 1, 0, 4, 1, 0, 0)),
        (49, (7, 5, 0, 4, 0, 0, 4, 0, 0, 0)),
        (50, (2, 2, 2, 2, 2, 2, 2, 2, 2, 2)),
        (50, (10, 10, 0, 0, 0, 0, 0, 0, 0, 0)),
    }
    assert set(profiles) == expected_profiles

    def exact_product_shadow(fibres: tuple[int, ...]) -> int:
        result = 0
        for pair in pairs:
            column_shadow = 0
            for index, triple in enumerate(triples):
                if set(pair) <= set(triple):
                    column_shadow |= one_shadow(fibres[index])
            result += column_shadow.bit_count()
        return result

    stability_records = []
    for lower_bound, profile in sorted(profiles):
        assignments: list[tuple[int, tuple[int, ...]]] = []

        def visit_fibres(index: int, fibres: list[int]) -> None:
            if index == 10:
                fibre_tuple = tuple(fibres)
                assignments.append((
                    exact_product_shadow(fibre_tuple),
                    fibre_tuple,
                ))
                return
            for ideal in ideals_by_size[profile[index]]:
                if all(
                    not (ideal & ~fibres[parent])
                    for parent in row_predecessors[index]
                ):
                    visit_fibres(index + 1, fibres + [ideal])

        visit_fibres(0, [])
        good = [record for record in assignments if record[0] <= 50]
        bad = [record[0] for record in assignments if record[0] > 50]
        assert len(good) == 1
        stability_records.append({
            "lower_bound": lower_bound,
            "profile": list(profile),
            "compatible_fibre_assignment_count": len(assignments),
            "good_assignment_count": len(good),
            "good_shadow": good[0][0],
            "good_fibres": [
                list(positions(mask)) for mask in good[0][1]
            ],
            "minimum_noncanonical_shadow": min(bad) if bad else None,
        })

    expected_assignment_histogram = {
        1: 2,
        2: 7,
        3: 4,
        6: 1,
    }
    assignment_histogram: dict[int, int] = {}
    for record in stability_records:
        count = record["compatible_fibre_assignment_count"]
        assignment_histogram[count] = assignment_histogram.get(count, 0) + 1
    assert assignment_histogram == expected_assignment_histogram

    result = {
        "status": "PASS_EXACT_INTEGER_SHIFTED_TERMINAL_STABILITY_GAP_FIX",
        "claim_type": (
            "self-contained exact audit of the 16-ideal size-profile lower "
            "bound and the unique good fibre assignment in each terminal"
        ),
        "one_dimensional_ideal_count": len(ideals),
        "one_dimensional_shadow_minima": n,
        "order_reversing_area20_profile_count": profile_count,
        "low_lower_bound_profile_count": len(profiles),
        "stability_records": stability_records,
        "compatible_assignment_count_histogram": {
            str(key): value
            for key, value in sorted(assignment_histogram.items())
        },
        "all_fourteen_profiles_have_exactly_one_good_assignment": True,
        "evidence_class": "exact integer audit only; not a proof dependency",
        "script_sha256_before_output": sha256(Path(__file__)),
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": result["status"],
        "profile_count": profile_count,
        "low_profile_count": len(profiles),
        "assignment_count_histogram": assignment_histogram,
        "output": OUTPUT.name,
    }, indent=2))


if __name__ == "__main__":
    main()

