r"""Complete exact classification of S20 low-shadow families and L5 defects.

Every 20-element subset of the 10x10 product layer with lower shadow at most
50 is compressed to a shifted order ideal without increasing its shadow.
This script enumerates the shifted terminals, closes under row/column
symmetry, transpose, and inverse elementary shifts that preserve the bound,
then forms full symmetry orbits.  For one representative of each orbit it
also enumerates all 53130 coordinate five-planes and computes

    max_L codim_{partial S} W_L.

All operations are deterministic integer/bitset operations.  The output is
an exact finite classification and diagnostic; the paper must separately
prove the compression and Borel implications used in a case-free argument.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = (
    ROOT
    / "n5_fixed_five_shadow_s20_le50_annihilator_classification_exact.json"
)
SIZE = 20
SHADOW_BOUND = 50


def positions(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def main():
    triples = list(combinations(range(5), 3))
    triple_index = {triple: index for index, triple in enumerate(triples)}
    pairs = list(combinations(range(5), 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}

    predecessor_masks = []
    shadow_masks = []
    derivative_records = []
    for row_index, rows in enumerate(triples):
        for column_index, columns in enumerate(triples):
            predecessors = 0
            for first_index, first in enumerate(triples):
                if not all(a <= b for a, b in zip(first, rows)):
                    continue
                for second_index, second in enumerate(triples):
                    if (first_index, second_index) == (
                        row_index, column_index
                    ):
                        continue
                    if all(a <= b for a, b in zip(second, columns)):
                        predecessors |= 1 << (
                            10 * first_index + second_index
                        )
            predecessor_masks.append(predecessors)

            monomial_shadow = 0
            derivatives = []
            for row_pair in combinations(rows, 2):
                missing_row = next(row for row in rows if row not in row_pair)
                for column_pair in combinations(columns, 2):
                    missing_column = next(
                        column for column in columns
                        if column not in column_pair
                    )
                    child = (
                        10 * pair_index[row_pair]
                        + pair_index[column_pair]
                    )
                    monomial_shadow |= 1 << child
                    derivatives.append(
                        (child, 5 * missing_row + missing_column)
                    )
            assert monomial_shadow.bit_count() == 9
            shadow_masks.append(monomial_shadow)
            derivative_records.append(tuple(derivatives))

    def shadow(family):
        result = 0
        for position in positions(family):
            result |= shadow_masks[position]
        return result

    ideals = {0}
    level_counts = []
    for _level in range(1, SIZE + 1):
        next_ideals = set()
        for ideal in ideals:
            for position in range(100):
                bit = 1 << position
                if (
                    not ideal & bit
                    and not predecessor_masks[position] & ~ideal
                ):
                    next_ideals.add(ideal | bit)
        ideals = next_ideals
        level_counts.append(len(ideals))
    assert len(ideals) == 5209
    shifted_histogram = Counter(
        shadow(ideal).bit_count() for ideal in ideals
    )
    terminals = {
        ideal for ideal in ideals
        if shadow(ideal).bit_count() <= SHADOW_BOUND
    }
    assert len(terminals) == 14

    identity = tuple(range(5))
    generator_maps = []
    for coordinate in ("row", "column"):
        for first in range(4):
            permutation = list(identity)
            permutation[first], permutation[first + 1] = (
                permutation[first + 1], permutation[first]
            )
            row_permutation = (
                tuple(permutation) if coordinate == "row" else identity
            )
            column_permutation = (
                tuple(permutation) if coordinate == "column" else identity
            )
            mapping = []
            for rows in triples:
                for columns in triples:
                    image_rows = tuple(sorted(
                        row_permutation[value] for value in rows
                    ))
                    image_columns = tuple(sorted(
                        column_permutation[value] for value in columns
                    ))
                    mapping.append(
                        10 * triple_index[image_rows]
                        + triple_index[image_columns]
                    )
            generator_maps.append(tuple(mapping))
    generator_maps.append(tuple(
        10 * (position % 10) + position // 10
        for position in range(100)
    ))
    assert len(generator_maps) == 9

    shift_pairs = []
    for high_triple in triples:
        if 1 not in high_triple or 0 in high_triple:
            continue
        low_triple = tuple(sorted(
            (set(high_triple) - {1}) | {0}
        ))
        for column_index in range(10):
            shift_pairs.append((
                10 * triple_index[low_triple] + column_index,
                10 * triple_index[high_triple] + column_index,
            ))
    assert len(shift_pairs) == 30

    families = set(terminals)
    queue = deque(sorted(terminals))
    processed = set()
    search_nodes = 0
    accepted_preimage_leaves = 0
    while queue:
        target = queue.popleft()
        if target in processed:
            continue
        processed.add(target)

        for mapping in generator_maps:
            image = sum(
                1 << mapping[position] for position in positions(target)
            )
            assert image.bit_count() == SIZE
            assert shadow(image).bit_count() <= SHADOW_BOUND
            if image not in families:
                families.add(image)
                queue.append(image)

        if any(
            target >> high & 1 and not target >> low & 1
            for low, high in shift_pairs
        ):
            continue
        low_only = [
            (low, high) for low, high in shift_pairs
            if target >> low & 1 and not target >> high & 1
        ]
        fixed = target & ~sum(1 << low for low, _high in low_only)
        ordered = sorted(
            low_only,
            key=lambda item: -(
                (
                    shadow(fixed) | shadow_masks[item[0]]
                ).bit_count()
                + (
                    shadow(fixed) | shadow_masks[item[1]]
                ).bit_count()
            ),
        )

        def visit(index, family, family_shadow):
            nonlocal search_nodes, accepted_preimage_leaves
            search_nodes += 1
            if family_shadow.bit_count() > SHADOW_BOUND:
                return
            if index == len(ordered):
                accepted_preimage_leaves += 1
                assert family.bit_count() == SIZE
                if family not in families:
                    families.add(family)
                    queue.append(family)
                return
            low, high = ordered[index]
            visit(
                index + 1,
                family | (1 << low),
                family_shadow | shadow_masks[low],
            )
            visit(
                index + 1,
                family | (1 << high),
                family_shadow | shadow_masks[high],
            )

        visit(0, fixed, shadow(fixed))

    assert processed == families
    family_shadow_histogram = Counter(
        shadow(family).bit_count() for family in families
    )
    assert set(family_shadow_histogram) <= {48, 49, 50}

    unassigned = set(families)
    orbit_records = []
    while unassigned:
        seed = min(unassigned)
        orbit = {seed}
        orbit_queue = deque([seed])
        while orbit_queue:
            family = orbit_queue.popleft()
            for mapping in generator_maps:
                image = sum(
                    1 << mapping[position]
                    for position in positions(family)
                )
                assert image in families
                if image not in orbit:
                    orbit.add(image)
                    orbit_queue.append(image)
        unassigned.difference_update(orbit)
        representative = min(orbit)
        representative_shadow = shadow(representative)
        orbit_records.append({
            "orbit_index": len(orbit_records),
            "orbit_size": len(orbit),
            "shadow_size": representative_shadow.bit_count(),
            "representative_family_positions": list(
                positions(representative)
            ),
            "representative_shadow_positions": list(
                positions(representative_shadow)
            ),
            "_representative": representative,
        })

    coordinate_planes = tuple(combinations(range(25), 5))
    coordinate_plane_masks = tuple(
        sum(1 << variable for variable in plane)
        for plane in coordinate_planes
    )
    assert len(coordinate_planes) == 53130
    for record in orbit_records:
        family = record.pop("_representative")
        parent_masks = {}
        for position in positions(family):
            for child, variable in derivative_records[position]:
                parent_masks[child] = (
                    parent_masks.get(child, 0) | (1 << variable)
                )
        assert len(parent_masks) == record["shadow_size"]
        maximum = -1
        witnesses = []
        histogram = Counter()
        for plane, plane_mask in zip(
            coordinate_planes, coordinate_plane_masks
        ):
            codimension = sum(
                parent_mask & ~plane_mask == 0
                for parent_mask in parent_masks.values()
            )
            histogram[codimension] += 1
            if codimension > maximum:
                maximum = codimension
                witnesses = [plane]
            elif codimension == maximum and len(witnesses) < 20:
                witnesses.append(plane)
        record["maximum_coordinate_L5_codimension_in_shadow"] = maximum
        record["minimum_visible_shadow"] = (
            record["shadow_size"] - maximum
        )
        record["maximum_witnesses_first_20"] = [
            list(witness) for witness in witnesses
        ]
        record["codimension_histogram_over_53130_L5"] = dict(
            sorted(histogram.items())
        )

    result = {
        "status": (
            "PASS_EXACT_INTEGER_S20_LE50_CLASSIFICATION_AND_ANNIHILATOR"
        ),
        "claim_type": (
            "complete exact integer compression closure and symmetry "
            "classification of 20-element product-layer families with "
            "shadow at most 50, plus coordinate L5 annihilator maxima"
        ),
        "shifted_order_ideal_count": len(ideals),
        "shifted_shadow_histogram_le55": {
            str(size): shifted_histogram[size]
            for size in range(48, 56)
        },
        "shifted_terminal_count_le50": len(terminals),
        "complete_family_count": len(families),
        "family_shadow_size_histogram": dict(sorted(
            family_shadow_histogram.items()
        )),
        "symmetry_orbit_count": len(orbit_records),
        "symmetry_orbit_size_histogram": dict(sorted(Counter(
            record["orbit_size"] for record in orbit_records
        ).items())),
        "symmetry_orbit_shadow_histogram": dict(sorted(Counter(
            record["shadow_size"] for record in orbit_records
        ).items())),
        "minimum_visible_shadow_over_all_orbits": min(
            record["minimum_visible_shadow"] for record in orbit_records
        ),
        "maximum_coordinate_L5_codimension_by_shadow": {
            str(shadow_size): max(
                record[
                    "maximum_coordinate_L5_codimension_in_shadow"
                ]
                for record in orbit_records
                if record["shadow_size"] == shadow_size
            )
            for shadow_size in sorted(family_shadow_histogram)
        },
        "orbit_records": orbit_records,
        "closure_search_nodes": search_nodes,
        "accepted_preimage_leaves": accepted_preimage_leaves,
        "level_counts_1_through_20": level_counts,
        "strict_scope": (
            "Exact finite integer classification.  The general torus "
            "specialization and a case-free Petersen proof remain separate "
            "mathematical obligations."
        ),
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUTPUT.write_bytes((json.dumps(result, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({
        "status": result["status"],
        "complete_family_count": result["complete_family_count"],
        "symmetry_orbit_count": result["symmetry_orbit_count"],
        "shadow_histogram": result["family_shadow_size_histogram"],
        "codimension_maxima_by_shadow": result[
            "maximum_coordinate_L5_codimension_by_shadow"
        ],
        "minimum_visible_shadow": result[
            "minimum_visible_shadow_over_all_orbits"
        ],
        "output": OUTPUT.name,
    }, indent=2))


if __name__ == "__main__":
    main()
