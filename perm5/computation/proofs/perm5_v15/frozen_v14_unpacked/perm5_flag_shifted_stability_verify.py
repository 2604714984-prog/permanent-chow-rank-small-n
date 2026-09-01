"""Independent exact audit for the pure S20 flag-stability note.

This script reads no project certificate and uses only Python integer bitsets.
It verifies:

* the 16 one-dimensional shifted ideals and the nested shadow profile n(k);
* the 14 Ferrers partitions of area 20 with product shadow at most 50;
* the 7 by 7 visible-shadow table;
* every valid one-step inverse ground-set compression of the three special
  flags, including the four visible-equality exceptions and their full
  shadow sizes.

The output is a diagnostic, not a premise of the mathematical proof.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_flag_shifted_stability_verify_exact.json"

TRIPLES = list(combinations(range(5), 3))
TRIPLE_INDEX = {triple: index for index, triple in enumerate(TRIPLES)}
PAIRS = list(combinations(range(5), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}

# The nested one-dimensional minimizers J_k.
INITIAL_ORDER = (0, 1, 3, 6, 2, 4, 7, 5, 8, 9)
N_PROFILE = (0, 3, 5, 6, 6, 8, 9, 9, 10, 10, 10)
ROW_INCREMENT = (3, 2, 1, 0, 2, 1, 0, 1, 0, 0)

BASE_SHAPES = (
    (10, 10, 0, 0),
    (10, 4, 4, 2),
    (10, 4, 3, 3),
    (9, 4, 4, 3),
    (8, 4, 4, 4),
    (7, 5, 4, 4),
    (5, 5, 5, 5),
)
L_PARTITIONS = (
    (5,),
    (4, 1),
    (3, 2),
    (3, 1, 1),
    (2, 2, 1),
    (2, 1, 1, 1),
    (1, 1, 1, 1, 1),
)
EXPECTED_VISIBLE_TABLE = (
    (30, 42, 48, 48, 50, 50, 50),
    (41, 40, 43, 43, 46, 46, 48),
    (44, 41, 44, 42, 43, 44, 45),
    (44, 41, 42, 42, 42, 43, 48),
    (44, 43, 42, 43, 42, 44, 45),
    (44, 43, 40, 43, 42, 45, 47),
    (48, 47, 45, 45, 43, 42, 42),
)


def positions(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


MONOMIAL_SHADOWS: list[int] = []
DERIVATIVE_RECORDS: list[tuple[tuple[int, int], ...]] = []
for rows in TRIPLES:
    for columns in TRIPLES:
        monomial_shadow = 0
        records = []
        for row_pair in combinations(rows, 2):
            missing_row = next(row for row in rows if row not in row_pair)
            for column_pair in combinations(columns, 2):
                missing_column = next(
                    column for column in columns if column not in column_pair
                )
                child = 10 * PAIR_INDEX[row_pair] + PAIR_INDEX[column_pair]
                variable = 5 * missing_row + missing_column
                monomial_shadow |= 1 << child
                records.append((child, variable))
        assert monomial_shadow.bit_count() == 9
        MONOMIAL_SHADOWS.append(monomial_shadow)
        DERIVATIVE_RECORDS.append(tuple(records))

PARENTS_BY_CHILD: list[list[tuple[int, int]]] = [
    [] for _ in range(100)
]
for parent_position, records in enumerate(DERIVATIVE_RECORDS):
    for child, variable in records:
        PARENTS_BY_CHILD[child].append((parent_position, variable))
assert all(len(records) == 9 for records in PARENTS_BY_CHILD)


def shadow_mask(family: int) -> int:
    result = 0
    for position in positions(family):
        result |= MONOMIAL_SHADOWS[position]
    return result


def parent_masks(family: int) -> tuple[int, ...]:
    result: dict[int, int] = {}
    for position in positions(family):
        for child, variable in DERIVATIVE_RECORDS[position]:
            result[child] = result.get(child, 0) | (1 << variable)
    return tuple(result.values())


def visible_size_from_parents(parents: tuple[int, ...], plane: int) -> int:
    return sum(bool(mask & ~plane) for mask in parents)


def visible_size(family: int, plane: int) -> int:
    return visible_size_from_parents(parent_masks(family), plane)


def visible_mask(family: int, plane: int) -> int:
    result = 0
    for child, records in enumerate(PARENTS_BY_CHILD):
        if any(
            family >> parent & 1 and not plane >> variable & 1
            for parent, variable in records
        ):
            result |= 1 << child
    return result


def ideal_mask(indices) -> int:
    return sum(1 << index for index in indices)


def direct_one_dimensional_shadow(mask: int) -> int:
    result = 0
    for index in positions(mask):
        for pair in combinations(TRIPLES[index], 2):
            result |= 1 << PAIR_INDEX[pair]
    return result


def is_order_ideal(mask: int) -> bool:
    for high_index, high in enumerate(TRIPLES):
        if not mask >> high_index & 1:
            continue
        for low_index, low in enumerate(TRIPLES):
            if all(a <= b for a, b in zip(low, high)):
                if not mask >> low_index & 1:
                    return False
    return True


def conjugate_partition(partition: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(value >= column for value in partition)
        for column in range(1, partition[0] + 1)
    )


def partitions(total: int, maximum: int = 10, length: int = 10):
    def visit(remaining: int, previous: int, current: list[int]):
        if remaining == 0:
            yield tuple(current)
            return
        if len(current) == length:
            return
        for value in range(min(previous, remaining), 0, -1):
            yield from visit(
                remaining - value, value, current + [value]
            )

    yield from visit(total, maximum, [])


def phi(partition: tuple[int, ...]) -> int:
    padded = partition + (0,) * (10 - len(partition))
    return sum(
        ROW_INCREMENT[index] * N_PROFILE[padded[index]]
        for index in range(10)
    )


def family_from_shape(shape: tuple[int, ...]) -> int:
    family = 0
    for row_index, length in zip(INITIAL_ORDER, shape):
        for column_index in INITIAL_ORDER[:length]:
            family |= 1 << (10 * row_index + column_index)
    return family


def plane_from_partition(partition: tuple[int, ...]) -> int:
    plane = 0
    for row, length in enumerate(partition):
        for column in range(length):
            plane |= 1 << (5 * row + column)
    return plane


def reflection_pairs(axis: int, low: int, high: int):
    family_pairs = []
    for triple in TRIPLES:
        if high not in triple or low in triple:
            continue
        low_triple = tuple(sorted((set(triple) - {high}) | {low}))
        low_index = TRIPLE_INDEX[low_triple]
        high_index = TRIPLE_INDEX[triple]
        for other in range(10):
            if axis == 0:
                family_pairs.append(
                    (10 * low_index + other, 10 * high_index + other)
                )
            else:
                family_pairs.append(
                    (10 * other + low_index, 10 * other + high_index)
                )
    plane_pairs = []
    for other in range(5):
        if axis == 0:
            plane_pairs.append((5 * low + other, 5 * high + other))
        else:
            plane_pairs.append((5 * other + low, 5 * other + high))
    return tuple(family_pairs), tuple(plane_pairs)


def shadow_reflection_pairs(axis: int, low: int, high: int):
    result = []
    for pair in PAIRS:
        if high not in pair or low in pair:
            continue
        low_pair = tuple(sorted((set(pair) - {high}) | {low}))
        low_index = PAIR_INDEX[low_pair]
        high_index = PAIR_INDEX[pair]
        for other in range(10):
            if axis == 0:
                result.append(
                    (10 * low_index + other, 10 * high_index + other)
                )
            else:
                result.append(
                    (10 * other + low_index, 10 * other + high_index)
                )
    return tuple(result)


def preimage_data(mask: int, pairs: tuple[tuple[int, int], ...]):
    if any(
        mask >> high & 1 and not mask >> low & 1
        for low, high in pairs
    ):
        return None
    movable = tuple(
        (low, high)
        for low, high in pairs
        if mask >> low & 1 and not mask >> high & 1
    )
    fixed = mask
    for low, _high in movable:
        fixed &= ~(1 << low)
    return fixed, movable


def oriented_mask(
    fixed: int, movable: tuple[tuple[int, int], ...], assignment: int
) -> int:
    return fixed | sum(
        1 << (high if assignment >> index & 1 else low)
        for index, (low, high) in enumerate(movable)
    )


def uniform_assignment(assignment: int, width: int) -> bool:
    return assignment in (0, (1 << width) - 1)


def literal_data(
    position: int,
    fixed: int,
    movable: tuple[tuple[int, int], ...],
    offset: int,
    complement: bool,
):
    """Return a constant, or (variable, value making the literal true)."""
    if fixed >> position & 1:
        return (not complement, None)
    for index, (low, high) in enumerate(movable):
        if position == low:
            return (None, (offset + index, complement))
        if position == high:
            return (None, (offset + index, not complement))
    return (complement, None)


def visible_child_support(
    child: int,
    fixed_family: int,
    movable_family: tuple[tuple[int, int], ...],
    fixed_plane: int,
    movable_plane: tuple[tuple[int, int], ...],
):
    support = set()
    for parent, variable in PARENTS_BY_CHILD[child]:
        for _constant, literal in (
            literal_data(
                parent, fixed_family, movable_family, 0, False
            ),
            literal_data(
                variable,
                fixed_plane,
                movable_plane,
                len(movable_family),
                True,
            ),
        ):
            if literal is not None:
                support.add(literal[0])
    return support


def visible_child_value(
    child: int,
    assignment: int,
    fixed_family: int,
    movable_family: tuple[tuple[int, int], ...],
    fixed_plane: int,
    movable_plane: tuple[tuple[int, int], ...],
):
    for parent, variable in PARENTS_BY_CHILD[child]:
        family_constant, family_literal = literal_data(
            parent, fixed_family, movable_family, 0, False
        )
        plane_constant, plane_literal = literal_data(
            variable,
            fixed_plane,
            movable_plane,
            len(movable_family),
            True,
        )
        family_true = (
            family_constant
            if family_literal is None
            else bool(assignment >> family_literal[0] & 1)
            == family_literal[1]
        )
        plane_true = (
            plane_constant
            if plane_literal is None
            else bool(assignment >> plane_literal[0] & 1)
            == plane_literal[1]
        )
        if family_true and plane_true:
            return True
    return False


def local_witness_forest(
    family: int,
    plane: int,
    axis: int,
    low: int,
    high: int,
    fixed_family: int,
    movable_family: tuple[tuple[int, int], ...],
    fixed_plane: int,
    movable_plane: tuple[tuple[int, int], ...],
):
    """Build a spanning forest of pairwise equality witnesses.

    An edge (i,j,w) means: whenever orientation bits i,j differ, the
    compressed source visible shadow contains the target-absent child w.
    The implication is checked from the local Boolean formula for w only.
    """
    variable_count = len(movable_family) + len(movable_plane)
    target_visible = visible_mask(family, plane)
    child_pairs = shadow_reflection_pairs(axis, low, high)
    high_of_low = dict(child_pairs)
    low_of_high = {high_child: low_child for low_child, high_child in child_pairs}
    candidate_edges = []

    for witness in range(100):
        if target_visible >> witness & 1:
            continue
        if witness in high_of_low:
            children = (witness, high_of_low[witness])
            operation = "or"
        elif witness in low_of_high:
            children = (low_of_high[witness], witness)
            operation = "and"
        else:
            children = (witness,)
            operation = "identity"

        support = sorted(set().union(*(
            visible_child_support(
                child,
                fixed_family,
                movable_family,
                fixed_plane,
                movable_plane,
            )
            for child in children
        )))
        zero_assignments = []
        for local_assignment in range(1 << len(support)):
            assignment = sum(
                ((local_assignment >> local_index) & 1) << global_index
                for local_index, global_index in enumerate(support)
            )
            values = tuple(
                visible_child_value(
                    child,
                    assignment,
                    fixed_family,
                    movable_family,
                    fixed_plane,
                    movable_plane,
                )
                for child in children
            )
            extra = (
                any(values)
                if operation == "or"
                else all(values)
                if operation == "and"
                else values[0]
            )
            if not extra:
                zero_assignments.append(assignment)

        for right_index, right in enumerate(support):
            for left in support[:right_index]:
                if all(
                    not ((assignment >> left) ^ (assignment >> right)) & 1
                    for assignment in zero_assignments
                ):
                    candidate_edges.append((left, right, witness))

    parent = list(range(variable_count))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    forest = []
    for left, right, witness in candidate_edges:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            continue
        parent[right_root] = left_root
        forest.append((left, right, witness))
    components = {}
    for vertex in range(variable_count):
        components.setdefault(find(vertex), []).append(vertex)
    return tuple(forest), tuple(sorted(
        (tuple(component) for component in components.values()),
        key=lambda component: component[0],
    ))


def main():
    ideals = [mask for mask in range(1 << 10) if is_order_ideal(mask)]
    assert len(ideals) == 16
    ideal_records = []
    for mask in ideals:
        ideal_records.append({
            "indices": list(positions(mask)),
            "size": mask.bit_count(),
            "shadow_size": direct_one_dimensional_shadow(mask).bit_count(),
        })
    nested = tuple(
        ideal_mask(INITIAL_ORDER[:size]) for size in range(11)
    )
    assert all(is_order_ideal(mask) for mask in nested)
    assert tuple(
        direct_one_dimensional_shadow(mask).bit_count() for mask in nested
    ) == N_PROFILE
    for size in range(11):
        assert N_PROFILE[size] == min(
            record["shadow_size"]
            for record in ideal_records
            if record["size"] == size
        )

    all_partitions = tuple(partitions(20))
    low_shadow_partitions = tuple(
        sorted(partition for partition in all_partitions if phi(partition) <= 50)
    )
    normalized_base_shapes = tuple(
        tuple(value for value in partition if value)
        for partition in BASE_SHAPES
    )
    expected_partitions = tuple(sorted(set(
        normalized_base_shapes
        + tuple(
            conjugate_partition(partition)
            for partition in normalized_base_shapes
        )
    )))
    assert low_shadow_partitions == expected_partitions
    both_sides_at_least_five = tuple(
        partition
        for partition in all_partitions
        if len(partition) >= 5 and partition[0] >= 5
    )
    assert min(map(phi, both_sides_at_least_five)) == 51
    assert all(
        shadow_mask(family_from_shape(partition)).bit_count()
        == phi(partition)
        for partition in all_partitions
    )

    visible_table = tuple(
        tuple(
            visible_size(
                family_from_shape(shape), plane_from_partition(partition)
            )
            for partition in L_PARTITIONS
        )
        for shape in BASE_SHAPES
    )
    assert visible_table == EXPECTED_VISIBLE_TABLE

    special = (
        ("orbit0", (10, 10), (5,), 50, 30),
        ("orbit1", (10, 4, 4, 2), (4, 1), 48, 40),
        ("orbit13", (7, 5, 4, 4), (3, 2), 49, 40),
    )
    inverse_records = {}
    visible_exceptions = {}
    expected_valid = {"orbit0": 31, "orbit1": 21, "orbit13": 21}
    expected_exception_values = {
        "orbit1:row:2<-3": (54, 54),
        "orbit1:row:3<-4": (58, 58),
        "orbit13:row:2<-3": (51, 51),
        "orbit13:column:3<-4": (53, 53),
    }

    for name, shape, l_partition, base_shadow, base_visible in special:
        family = family_from_shape(shape)
        plane = plane_from_partition(l_partition)
        assert shadow_mask(family).bit_count() == base_shadow
        assert visible_size(family, plane) == base_visible
        records = []
        exceptions = {}
        for axis in (0, 1):
            for low in range(5):
                for high in range(5):
                    if low == high:
                        continue
                    family_pairs, plane_pairs = reflection_pairs(
                        axis, low, high
                    )
                    family_data = preimage_data(family, family_pairs)
                    plane_data = preimage_data(plane, plane_pairs)
                    if family_data is None or plane_data is None:
                        continue
                    fixed_family, movable_family = family_data
                    fixed_plane, movable_plane = plane_data
                    direction = (
                        f"{'row' if axis == 0 else 'column'}:"
                        f"{low}<-{high}"
                    )
                    if name in ("orbit1", "orbit13"):
                        witness_forest, witness_components = (
                            local_witness_forest(
                                family,
                                plane,
                                axis,
                                low,
                                high,
                                fixed_family,
                                movable_family,
                                fixed_plane,
                                movable_plane,
                            )
                        )
                        exception_key = f"{name}:{direction}"
                        expected_components = (
                            0
                            if not movable_family and not movable_plane
                            else 2
                            if exception_key in expected_exception_values
                            else 1
                        )
                        assert len(witness_components) == expected_components
                        assert len(witness_forest) == (
                            len(movable_family)
                            + len(movable_plane)
                            - expected_components
                        )
                    else:
                        witness_forest = ()
                        witness_components = ()
                    if name == "orbit0":
                        full_witness_forest, full_witness_components = (
                            local_witness_forest(
                                family,
                                0,
                                axis,
                                low,
                                high,
                                fixed_family,
                                movable_family,
                                0,
                                (),
                            )
                        )
                        expected_full_components = (
                            0 if not movable_family else 1
                        )
                        assert (
                            len(full_witness_components)
                            == expected_full_components
                        )
                        assert len(full_witness_forest) == (
                            len(movable_family) - expected_full_components
                        )
                    else:
                        full_witness_forest = ()
                        full_witness_components = ()
                    planes = tuple(
                        oriented_mask(fixed_plane, movable_plane, assignment)
                        for assignment in range(1 << len(movable_plane))
                    )
                    visible_pass = []
                    flag_pass = []
                    for family_assignment in range(
                        1 << len(movable_family)
                    ):
                        source_family = oriented_mask(
                            fixed_family,
                            movable_family,
                            family_assignment,
                        )
                        source_shadow = shadow_mask(source_family).bit_count()
                        # The orbit-0 proof uses its saturated full-shadow
                        # bound first.  Do not scan the irrelevant 2^5 plane
                        # choices for a family already above 50.
                        if name == "orbit0" and source_shadow > 50:
                            continue
                        parents = parent_masks(source_family)
                        for plane_assignment, source_plane in enumerate(planes):
                            source_visible = visible_size_from_parents(
                                parents, source_plane
                            )
                            if source_visible <= 40:
                                visible_pass.append((
                                    family_assignment,
                                    plane_assignment,
                                    source_shadow,
                                    source_visible,
                                ))
                            if source_shadow <= 50 and source_visible <= 40:
                                flag_pass.append((
                                    family_assignment,
                                    plane_assignment,
                                    source_shadow,
                                    source_visible,
                                ))

                    variable_count = len(movable_family) + len(movable_plane)
                    expected_flag_count = 1 if variable_count == 0 else 2
                    assert len(flag_pass) == expected_flag_count
                    assert all(
                        uniform_assignment(row[0], len(movable_family))
                        and uniform_assignment(row[1], len(movable_plane))
                        for row in flag_pass
                    )
                    nonuniform_visible = [
                        row for row in visible_pass
                        if not (
                            uniform_assignment(row[0], len(movable_family))
                            and uniform_assignment(row[1], len(movable_plane))
                        )
                    ]
                    if nonuniform_visible:
                        exceptions[direction] = {
                            "count": len(nonuniform_visible),
                            "full_shadow_sizes": [
                                row[2] for row in nonuniform_visible
                            ],
                            "family_assignments": [
                                format(row[0], f"0{len(movable_family)}b")
                                for row in nonuniform_visible
                            ],
                            "plane_assignments": [
                                format(row[1], f"0{len(movable_plane)}b")
                                for row in nonuniform_visible
                            ],
                        }
                    records.append({
                        "direction": direction,
                        "family_variables": len(movable_family),
                        "plane_variables": len(movable_plane),
                        "family_movable_pairs": [
                            [low_position, high_position]
                            for low_position, high_position in movable_family
                        ],
                        "plane_movable_pairs": [
                            [low_position, high_position]
                            for low_position, high_position in movable_plane
                        ],
                        "local_witness_components": [
                            list(component) for component in witness_components
                        ],
                        "local_witness_spanning_forest": [
                            {
                                "left_variable": left,
                                "right_variable": right,
                                "witness_child_position": witness,
                                "witness_child": [
                                    list(PAIRS[witness // 10]),
                                    list(PAIRS[witness % 10]),
                                ],
                            }
                            for left, right, witness in witness_forest
                        ],
                        "full_shadow_witness_components": [
                            list(component)
                            for component in full_witness_components
                        ],
                        "full_shadow_witness_spanning_forest": [
                            {
                                "left_variable": left,
                                "right_variable": right,
                                "witness_child_position": witness,
                                "witness_child": [
                                    list(PAIRS[witness // 10]),
                                    list(PAIRS[witness % 10]),
                                ],
                            }
                            for left, right, witness in full_witness_forest
                        ],
                        "visible_pass_count": len(visible_pass),
                        "full_flag_pass_count": len(flag_pass),
                    })
        assert len(records) == expected_valid[name]
        inverse_records[name] = records
        visible_exceptions[name] = exceptions

    actual_exception_values = {}
    for name, exceptions in visible_exceptions.items():
        for direction, record in exceptions.items():
            actual_exception_values[f"{name}:{direction}"] = tuple(
                record["full_shadow_sizes"]
            )
    assert actual_exception_values == expected_exception_values

    result = {
        "status": "PASS_EXACT_INTEGER_FLAG_SHIFTED_STABILITY_DIAGNOSTIC",
        "proof_dependency": False,
        "one_dimensional_ideal_count": len(ideals),
        "one_dimensional_ideals": ideal_records,
        "nested_profile": list(N_PROFILE),
        "area_20_partition_count": len(all_partitions),
        "minimum_shadow_when_both_sides_at_least_five": 51,
        "low_shadow_partition_count": len(low_shadow_partitions),
        "low_shadow_partitions": [
            {"partition": list(partition), "shadow": phi(partition)}
            for partition in low_shadow_partitions
        ],
        "visible_table": [list(row) for row in visible_table],
        "inverse_valid_direction_counts": {
            name: len(records) for name, records in inverse_records.items()
        },
        "inverse_records": inverse_records,
        "visible_equality_exceptions": visible_exceptions,
        "all_full_flag_preimages_are_uniform_endpoints": True,
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "ideal_count": result["one_dimensional_ideal_count"],
        "low_shadow_partition_count": result["low_shadow_partition_count"],
        "visible_table": result["visible_table"],
        "valid_directions": result["inverse_valid_direction_counts"],
        "exceptions": result["visible_equality_exceptions"],
    }, indent=2))


if __name__ == "__main__":
    main()
