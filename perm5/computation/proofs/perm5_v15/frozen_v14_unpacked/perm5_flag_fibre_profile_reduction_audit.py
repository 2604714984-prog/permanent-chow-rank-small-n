"""Exact audit for the fibre-profile replacement of the local witness forests.

The mathematical input is the Petersen fibre inequality

    |dS| = sum_A |N(union_{R superset A} S_R)|
          >= sum_A n(|union_{R superset A} S_R|)
          >= sum_A n(max_{R superset A} |S_R|).

This program does not read the old witness-forest certificate.  It checks how
far the two displayed lower bounds alone reduce every one-step inverse shift
of the two surviving S_20 flags.  It also records the remaining five family
directions and the global five-plane extremizers.  The output is an exact
integer diagnostic; the inequalities themselves are proved in the paper.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_flag_fibre_profile_reduction_exact.json"

TRIPLES = tuple(combinations(range(5), 3))
TRIPLE_INDEX = {value: index for index, value in enumerate(TRIPLES)}
PAIRS = tuple(combinations(range(5), 2))
PAIR_INDEX = {value: index for index, value in enumerate(PAIRS)}
INITIAL_ORDER = (0, 1, 3, 6, 2, 4, 7, 5, 8, 9)
N_PROFILE = (0, 3, 5, 6, 6, 8, 9, 9, 10, 10, 10)

ROW_PARENT_INDICES = tuple(
    tuple(
        row_index
        for row_index, row_triple in enumerate(TRIPLES)
        if set(row_pair) <= set(row_triple)
    )
    for row_pair in PAIRS
)
assert all(len(value) == 3 for value in ROW_PARENT_INDICES)

MONOMIAL_SHADOWS = []
PARENTS_BY_CHILD = [[] for _ in range(100)]
for row_index, rows in enumerate(TRIPLES):
    for column_index, columns in enumerate(TRIPLES):
        parent = 10 * row_index + column_index
        shadow = 0
        for row_pair in combinations(rows, 2):
            missing_row = next(value for value in rows if value not in row_pair)
            for column_pair in combinations(columns, 2):
                missing_column = next(
                    value for value in columns if value not in column_pair
                )
                child = 10 * PAIR_INDEX[row_pair] + PAIR_INDEX[column_pair]
                variable = 5 * missing_row + missing_column
                shadow |= 1 << child
                PARENTS_BY_CHILD[child].append((parent, variable))
        assert shadow.bit_count() == 9
        MONOMIAL_SHADOWS.append(shadow)
assert all(len(value) == 9 for value in PARENTS_BY_CHILD)


def positions(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def family_from_shape(shape: tuple[int, ...]) -> int:
    result = 0
    for row, length in zip(INITIAL_ORDER, shape):
        for column in INITIAL_ORDER[:length]:
            result |= 1 << (10 * row + column)
    return result


def plane_from_partition(partition: tuple[int, ...]) -> int:
    return sum(
        1 << (5 * row + column)
        for row, length in enumerate(partition)
        for column in range(length)
    )


def reflection_pairs(axis: int, low: int, high: int):
    family_pairs = []
    for triple in TRIPLES:
        if high not in triple or low in triple:
            continue
        low_triple = tuple(sorted((set(triple) - {high}) | {low}))
        low_index = TRIPLE_INDEX[low_triple]
        high_index = TRIPLE_INDEX[triple]
        for other in range(10):
            family_pairs.append(
                (10 * low_index + other, 10 * high_index + other)
                if axis == 0
                else (10 * other + low_index, 10 * other + high_index)
            )
    plane_pairs = tuple(
        (5 * low + other, 5 * high + other)
        if axis == 0
        else (5 * other + low, 5 * other + high)
        for other in range(5)
    )
    return tuple(family_pairs), plane_pairs


def preimage_data(mask: int, pairs):
    if any((mask >> high) & 1 and not (mask >> low) & 1 for low, high in pairs):
        return None
    movable = tuple(
        (low, high)
        for low, high in pairs
        if (mask >> low) & 1 and not (mask >> high) & 1
    )
    fixed = mask
    for low, _high in movable:
        fixed &= ~(1 << low)
    return fixed, movable


def oriented_mask(fixed: int, movable, assignment: int) -> int:
    return fixed | sum(
        1 << (high if (assignment >> index) & 1 else low)
        for index, (low, high) in enumerate(movable)
    )


def transpose_family(family: int) -> int:
    result = 0
    for position in positions(family):
        row, column = divmod(position, 10)
        result |= 1 << (10 * column + row)
    return result


def fibre_masks(family: int):
    return tuple((family >> (10 * row)) & 1023 for row in range(10))


def fibre_size_bound_from_sizes(sizes) -> int:
    return sum(
        N_PROFILE[max(sizes[index] for index in parents)]
        for parents in ROW_PARENT_INDICES
    )


def fibre_union_bound(family: int) -> int:
    fibres = fibre_masks(family)
    return sum(
        N_PROFILE[
            (fibres[parents[0]] | fibres[parents[1]] | fibres[parents[2]]).bit_count()
        ]
        for parents in ROW_PARENT_INDICES
    )


def shadow_mask(family: int) -> int:
    result = 0
    for position in positions(family):
        result |= MONOMIAL_SHADOWS[position]
    return result


def parent_masks(family: int):
    result = []
    for records in PARENTS_BY_CHILD:
        mask = 0
        for parent, variable in records:
            if (family >> parent) & 1:
                mask |= 1 << variable
        if mask:
            result.append(mask)
    return tuple(result)


def visible_size(family: int, plane: int) -> int:
    return sum(bool(mask & ~plane) for mask in parent_masks(family))


def analysed_fibre_sizes(family: int, axis: int):
    analysed = family if axis == 0 else transpose_family(family)
    return tuple(mask.bit_count() for mask in fibre_masks(analysed))


def transfer_groups(movable_family, axis: int):
    grouped = defaultdict(list)
    for variable, (low_position, high_position) in enumerate(movable_family):
        low_row, low_column = divmod(low_position, 10)
        high_row, high_column = divmod(high_position, 10)
        low = low_row if axis == 0 else low_column
        high = high_row if axis == 0 else high_column
        grouped[(low, high)].append(variable)
    return tuple(
        (low, high, tuple(indices))
        for (low, high), indices in sorted(grouped.items())
    )


def size_bound_for_assignment(base_sizes, groups, assignment: int) -> int:
    sizes = list(base_sizes)
    for low, high, indices in groups:
        moved = sum((assignment >> index) & 1 for index in indices)
        sizes[low] -= moved
        sizes[high] += moved
    return fibre_size_bound_from_sizes(sizes)


def plane_partition(plane: int):
    counts = tuple(
        sum((plane >> (5 * row + column)) & 1 for column in range(5))
        for row in range(5)
    )
    return tuple(sorted(counts, reverse=True))


def global_plane_record(family: int, threshold: int):
    parents = parent_masks(family)
    partition_data = defaultdict(lambda: {"maximum_invisible": -1, "count": 0})
    good = []
    for cells in combinations(range(25), 5):
        plane = sum(1 << value for value in cells)
        invisible = sum(not (mask & ~plane) for mask in parents)
        partition = plane_partition(plane)
        record = partition_data[partition]
        if invisible > record["maximum_invisible"]:
            record["maximum_invisible"] = invisible
            record["count"] = 1
            record["example"] = list(cells)
        elif invisible == record["maximum_invisible"]:
            record["count"] += 1
        if len(parents) - invisible <= threshold:
            good.append({"cells": list(cells), "visible": len(parents) - invisible})
    return {
        "shadow_size": len(parents),
        "good_plane_count": len(good),
        "good_planes": good,
        "row_partition_maxima": [
            {
                "partition": list(partition),
                **record,
            }
            for partition, record in sorted(partition_data.items(), reverse=True)
        ],
    }


def ordered_two_row_maxima(family: int, longer: int, shorter: int):
    parents = parent_masks(family)
    matrix = []
    equality_cells = []
    for long_row in range(5):
        row = []
        for short_row in range(5):
            if long_row == short_row:
                row.append(None)
                continue
            maximum = -1
            maximizers = []
            for long_columns in combinations(range(5), longer):
                for short_columns in combinations(range(5), shorter):
                    cells = tuple(
                        [5 * long_row + column for column in long_columns]
                        + [5 * short_row + column for column in short_columns]
                    )
                    plane = sum(1 << value for value in cells)
                    invisible = sum(not (mask & ~plane) for mask in parents)
                    if invisible > maximum:
                        maximum = invisible
                        maximizers = [cells]
                    elif invisible == maximum:
                        maximizers.append(cells)
            row.append(maximum)
            equality_cells.append({
                "long_row": long_row,
                "short_row": short_row,
                "maximum_invisible": maximum,
                "maximizer_count": len(maximizers),
                "maximizer_examples": [list(value) for value in maximizers[:4]],
            })
        matrix.append(row)
    return {"matrix": matrix, "records": equality_cells}


def direction_records(name: str, shape, plane_partition_value):
    family = family_from_shape(shape)
    plane = plane_from_partition(plane_partition_value)
    records = []
    for axis, low, high in product((0, 1), range(5), range(5)):
        if low == high:
            continue
        family_pairs, plane_pairs = reflection_pairs(axis, low, high)
        family_data = preimage_data(family, family_pairs)
        plane_data = preimage_data(plane, plane_pairs)
        if family_data is None or plane_data is None:
            continue
        fixed_family, movable_family = family_data
        fixed_plane, movable_plane = plane_data
        groups = transfer_groups(movable_family, axis)
        base_sizes = analysed_fibre_sizes(family, axis)
        width = len(movable_family)
        size_pass = []
        union_pass = []
        exact_pass = []
        full_flag_pass = []
        nonuniform_visible_minima = []
        count_vector_values = {}

        for counts in product(*(range(len(indices) + 1) for _lo, _hi, indices in groups)):
            sizes = list(base_sizes)
            for (low_row, high_row, _indices), moved in zip(groups, counts):
                sizes[low_row] -= moved
                sizes[high_row] += moved
            count_vector_values[counts] = fibre_size_bound_from_sizes(sizes)

        for assignment in range(1 << width):
            size_value = size_bound_for_assignment(base_sizes, groups, assignment)
            if size_value > 50:
                continue
            size_pass.append(assignment)
            source = oriented_mask(fixed_family, movable_family, assignment)
            analysed = source if axis == 0 else transpose_family(source)
            union_value = fibre_union_bound(analysed)
            exact_value = shadow_mask(source).bit_count()
            assert exact_value >= union_value >= size_value
            if union_value <= 50:
                union_pass.append(assignment)
            if exact_value <= 50:
                exact_pass.append(assignment)
            assert (union_value <= 50) == (exact_value <= 50)

        endpoints = {0, (1 << width) - 1} if width else {0}
        for assignment in exact_pass:
            source = oriented_mask(fixed_family, movable_family, assignment)
            for plane_assignment in range(1 << len(movable_plane)):
                source_plane = oriented_mask(
                    fixed_plane, movable_plane, plane_assignment
                )
                if visible_size(source, source_plane) <= 40:
                    full_flag_pass.append((assignment, plane_assignment))
        assert all(assignment in endpoints for assignment, _plane in full_flag_pass)

        for assignment in exact_pass:
            if assignment in endpoints:
                continue
            source = oriented_mask(fixed_family, movable_family, assignment)
            visible_values = []
            for plane_assignment in range(1 << len(movable_plane)):
                source_plane = oriented_mask(
                    fixed_plane, movable_plane, plane_assignment
                )
                visible_values.append((
                    visible_size(source, source_plane), plane_assignment
                ))
            minimum = min(value for value, _assignment in visible_values)
            nonuniform_visible_minima.append({
                "family_assignment": assignment,
                "family_support": [
                    index for index in range(width) if (assignment >> index) & 1
                ],
                "shadow_size": shadow_mask(source).bit_count(),
                "minimum_compatible_visible_size": minimum,
                "minimizing_plane_assignments": [
                    value
                    for visible, value in visible_values
                    if visible == minimum
                ],
            })

        record = {
            "direction": f"{'row' if axis == 0 else 'column'}:{low}<-{high}",
            "family_variable_count": width,
            "plane_variable_count": len(movable_plane),
            "transfer_blocks": [
                {"low_fibre": low_row, "high_fibre": high_row, "width": len(indices)}
                for low_row, high_row, indices in groups
            ],
            "size_bound_count_vectors_at_most_50": [
                {"counts": list(counts), "bound": value}
                for counts, value in sorted(count_vector_values.items())
                if value <= 50
            ],
            "size_bound_assignment_count": len(size_pass),
            "union_bound_assignment_count": len(union_pass),
            "exact_shadow_assignment_count": len(exact_pass),
            "full_flag_pass_count": len(full_flag_pass),
            "full_flag_pass_assignments": [
                {
                    "family_assignment": family_assignment,
                    "plane_assignment": plane_assignment,
                }
                for family_assignment, plane_assignment in full_flag_pass
            ],
            "exact_shadow_assignment_supports": [
                [index for index in range(width) if (assignment >> index) & 1]
                for assignment in exact_pass
            ],
            "nonuniform_visible_minima": nonuniform_visible_minima,
        }
        records.append(record)

    assert len(records) == 21
    exceptional = {
        record["direction"]
        for record in records
        if record["nonuniform_visible_minima"]
    }
    expected = (
        {"row:0<-1", "row:0<-2", "row:0<-3"}
        if name == "orbit1"
        else {"column:0<-3", "column:1<-3"}
    )
    assert exceptional == expected
    assert all(
        item["minimum_compatible_visible_size"] > 40
        for record in records
        for item in record["nonuniform_visible_minima"]
    )
    return records


def main():
    special = {
        "orbit1": ((10, 4, 4, 2), (4, 1)),
        "orbit13": ((7, 5, 4, 4), (3, 2)),
    }
    directions = {
        name: direction_records(name, shape, partition)
        for name, (shape, partition) in special.items()
    }
    global_planes = {
        name: global_plane_record(family_from_shape(shape), 40)
        for name, (shape, _partition) in special.items()
    }
    ordered_matrices = {
        "orbit1_4_plus_1": ordered_two_row_maxima(
            family_from_shape(special["orbit1"][0]), 4, 1
        ),
        "orbit13_3_plus_2": ordered_two_row_maxima(
            family_from_shape(special["orbit13"][0]), 3, 2
        ),
    }
    assert global_planes["orbit1"]["good_planes"] == [
        {"cells": [0, 1, 2, 3, value], "visible": 40}
        for value in (5, 6, 10, 11)
    ]
    assert global_planes["orbit13"]["good_planes"] == [
        {"cells": [0, 1, 2, 5, 6], "visible": 40},
        {"cells": [0, 1, 5, 6, 7], "visible": 40},
    ]
    assert ordered_matrices["orbit1_4_plus_1"]["matrix"] == [
        [None, 8, 8, 6, 6],
        [4, None, 4, 4, 4],
        [4, 4, None, 4, 4],
        [0, 0, 0, None, 0],
        [0, 0, 0, 0, None],
    ]
    assert ordered_matrices["orbit13_3_plus_2"]["matrix"] == [
        [None, 9, 7, 6, 5],
        [9, None, 7, 6, 5],
        [5, 5, None, 4, 1],
        [4, 4, 2, None, 0],
        [3, 3, 1, 0, None],
    ]

    result = {
        "status": "PASS_EXACT_INTEGER_FIBRE_PROFILE_REDUCTION_AUDIT",
        "evidence_role": (
            "exact diagnostic for a written Petersen fibre inequality; it "
            "does not by itself prove the remaining row-partition maxima"
        ),
        "petersen_neighbourhood_profile": list(N_PROFILE),
        "directions": directions,
        "global_five_plane_extremizers": global_planes,
        "ordered_two_row_maxima": ordered_matrices,
        "summary": {
            "old_visible_witness_edges": 250,
            "valid_direction_records": 42,
            "family_exceptional_directions": 5,
            "family_exceptional_nonuniform_states": sum(
                len(record["nonuniform_visible_minima"])
                for records in directions.values()
                for record in records
            ),
            "minimum_visible_over_all_exceptional_compatible_flags": min(
                item["minimum_compatible_visible_size"]
                for records in directions.values()
                for record in records
                for item in record["nonuniform_visible_minima"]
            ),
            "orbit1_global_good_planes": 4,
            "orbit13_global_good_planes": 2,
        },
    }
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper()
    result["script_sha256_before_output"] = source_hash
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], **result["summary"]}, indent=2))


if __name__ == "__main__":
    main()
