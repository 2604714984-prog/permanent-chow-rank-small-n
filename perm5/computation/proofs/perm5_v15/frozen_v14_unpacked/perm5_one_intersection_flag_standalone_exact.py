#!/usr/bin/env python3
"""Standalone exact verifier for the one-intersection flag bound at n=5.

The verifier reconstructs the 225 quadratic quotient weights and all local
relative-prolongation matrices directly from definitions.  It does not import
any project generator and does not read a frozen result.  All matrix arithmetic
is exact over F_3.  Because the integral divided-power matrices have rank over
F_3 at most their rank over Q, and the reduced base matrix has kernel dimension
100, equal to the characteristic-zero base kernel, the computed relative kernel
dimensions are rigorous upper bounds in characteristic zero.  No identification
of the divided-power lattice with the usual symmetric power in characteristic
three is used.

The finite statement checked is the coordinate endpoint of the geometric
degeneration theorem:

* a four-dimensional factor span limits to a 2-by-2 rectangle;
* a five-dimensional factor span limits to a rectangle plus one cell, with
  the fifth cell either attached to the rectangle or external to it;
* every coordinate nine-plane in the resulting quotient universe and every
  possible tenth quotient weight are checked.

The script is compare-only by default.  Pass ``--output PATH`` to write the
compact machine-readable certificate.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement
from pathlib import Path


N = 5
VARIABLES = N * N
PRIME = 3
Descriptor = tuple[str, ...]
Pair = tuple[int, int]


def require_equal(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise RuntimeError(
            f"{label} mismatch: expected {expected!r}, observed {actual!r}"
        )


def build_classes() -> list[tuple]:
    classes: list[tuple] = []
    for row in range(N):
        for column in range(N):
            classes.append(("S", row, column))
    for row in range(N):
        for first, second in combinations(range(N), 2):
            classes.append(("R", row, first, second))
    for column in range(N):
        for first, second in combinations(range(N), 2):
            classes.append(("C", first, second, column))
    for first_row, second_row in combinations(range(N), 2):
        for first_column, second_column in combinations(range(N), 2):
            classes.append(
                (
                    "X",
                    first_row,
                    second_row,
                    first_column,
                    second_column,
                )
            )
    require_equal("quadratic quotient weight count", len(classes), 225)
    return classes


CLASSES = build_classes()
CLASS_INDEX = {descriptor: index for index, descriptor in enumerate(CLASSES)}


def representative_monomial(descriptor: tuple) -> Pair:
    kind = descriptor[0]
    if kind == "S":
        _, row, column = descriptor
        variable = N * row + column
        return variable, variable
    if kind == "R":
        _, row, first, second = descriptor
        return N * row + first, N * row + second
    if kind == "C":
        _, first, second, column = descriptor
        return N * first + column, N * second + column
    _, first_row, second_row, first_column, second_column = descriptor
    return N * first_row + first_column, N * second_row + second_column


def quadratic_class(monomial: Pair) -> tuple[int, int]:
    first, second = sorted(monomial)
    first_row, first_column = divmod(first, N)
    second_row, second_column = divmod(second, N)
    if first == second:
        descriptor = ("S", first_row, first_column)
        return CLASS_INDEX[descriptor], 1
    if first_row == second_row:
        descriptor = (
            "R",
            first_row,
            min(first_column, second_column),
            max(first_column, second_column),
        )
        return CLASS_INDEX[descriptor], 1
    if first_column == second_column:
        descriptor = (
            "C",
            min(first_row, second_row),
            max(first_row, second_row),
            first_column,
        )
        return CLASS_INDEX[descriptor], 1
    descriptor = (
        "X",
        min(first_row, second_row),
        max(first_row, second_row),
        min(first_column, second_column),
        max(first_column, second_column),
    )
    representative = representative_monomial(descriptor)
    sign = 1 if (first, second) == representative else -1
    return CLASS_INDEX[descriptor], sign % PRIME


def torus_weight(monomial: tuple[int, ...]) -> tuple[int, ...]:
    rows = [0] * N
    columns = [0] * N
    for variable in monomial:
        row, column = divmod(variable, N)
        rows[row] += 1
        columns[column] += 1
    return tuple(rows + columns)


def rank_mod3(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    matrix = [row[:] for row in rows if any(value % PRIME for value in row)]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next(
            (
                index
                for index in range(rank, len(matrix))
                if matrix[index][column] % PRIME
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = 1 if matrix[rank][column] % PRIME == 1 else 2
        matrix[rank] = [
            inverse * value % PRIME for value in matrix[rank]
        ]
        for row_index in range(len(matrix)):
            if row_index == rank or not matrix[row_index][column] % PRIME:
                continue
            factor = matrix[row_index][column] % PRIME
            matrix[row_index] = [
                (left - factor * right) % PRIME
                for left, right in zip(matrix[row_index], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def build_local_blocks() -> list[tuple[list[int], dict[int, int]]]:
    cubic_groups: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    cubic_count = 0
    for monomial in combinations_with_replacement(range(VARIABLES), 3):
        cubic_groups[torus_weight(monomial)].append(monomial)
        cubic_count += 1
    require_equal("cubic monomial count", cubic_count, 2925)
    require_equal("cubic torus-weight count", len(cubic_groups), 1225)

    blocks: list[tuple[list[int], dict[int, int]]] = []
    involved_histogram: Counter[int] = Counter()
    truth_table_entries = 0
    base_kernel_sum = 0
    for monomials in cubic_groups.values():
        row_coefficients: dict[tuple[int, int], list[int]] = {}
        involved: set[int] = set()
        for column, monomial in enumerate(monomials):
            for variable in set(monomial):
                remaining = list(monomial)
                remaining.remove(variable)
                quotient_weight, sign = quadratic_class(tuple(remaining))
                involved.add(quotient_weight)
                row = row_coefficients.setdefault(
                    (variable, quotient_weight), [0] * len(monomials)
                )
                row[column] = (row[column] + sign) % PRIME

        ordered_weights = sorted(involved)
        involved_histogram[len(ordered_weights)] += 1
        full_rows = list(row_coefficients.values())
        base_kernel = len(monomials) - rank_mod3(full_rows)
        base_kernel_sum += base_kernel
        table: dict[int, int] = {}
        for mask in range(1 << len(ordered_weights)):
            allowed = {
                ordered_weights[position]
                for position in range(len(ordered_weights))
                if mask >> position & 1
            }
            constrained_rows = [
                row
                for (_, quotient_weight), row in row_coefficients.items()
                if quotient_weight not in allowed
            ]
            kernel = len(monomials) - rank_mod3(constrained_rows)
            relative = kernel - base_kernel
            if relative:
                table[mask] = relative
        truth_table_entries += len(table)
        blocks.append((ordered_weights, table))

    require_equal("nonzero local block count", len(blocks), 1225)
    require_equal("local truth-table entries", truth_table_entries, 43825)
    require_equal(
        "involved-weight histogram",
        dict(sorted(involved_histogram.items())),
        {1: 25, 2: 200, 3: 100, 4: 400, 6: 400, 9: 100},
    )
    require_equal("base permanent prolongation dimension", base_kernel_sum, 100)
    return blocks


def index_blocks(
    blocks: list[tuple[list[int], dict[int, int]]],
) -> list[list[tuple[int, int]]]:
    by_weight: list[list[tuple[int, int]]] = [[] for _ in range(225)]
    for block_index, (weights, _) in enumerate(blocks):
        for position, weight in enumerate(weights):
            by_weight[weight].append((block_index, 1 << position))
    return by_weight


def masks_and_value(
    selected: set[int],
    blocks: list[tuple[list[int], dict[int, int]]],
    by_weight: list[list[tuple[int, int]]],
) -> tuple[list[int], int]:
    masks = [0] * len(blocks)
    for weight in selected:
        for block_index, bit in by_weight[weight]:
            masks[block_index] |= bit
    value = sum(
        table.get(mask, 0)
        for mask, (_, table) in zip(masks, blocks)
    )
    return masks, value


def extension_delta(
    masks: list[int],
    extra_weight: int,
    blocks: list[tuple[list[int], dict[int, int]]],
    by_weight: list[list[tuple[int, int]]],
) -> int:
    delta = 0
    for block_index, bit in by_weight[extra_weight]:
        old_mask = masks[block_index]
        table = blocks[block_index][1]
        delta += table.get(old_mask | bit, 0) - table.get(old_mask, 0)
    return delta


def quotient_universe(cells: tuple[int, ...] | list[int]) -> list[int]:
    return sorted(
        {
            quadratic_class(tuple(sorted(pair)))[0]
            for pair in combinations_with_replacement(cells, 2)
        }
    )


def rectangle_sets() -> list[frozenset[int]]:
    return [
        frozenset(N * row + column for row in rows for column in columns)
        for rows in combinations(range(N), 2)
        for columns in combinations(range(N), 2)
    ]


def classify_coordinate_five_planes() -> dict[str, int]:
    rectangles = rectangle_sets()
    counts = Counter()
    for cells in combinations(range(VARIABLES), 5):
        cell_set = frozenset(cells)
        contained = [rectangle for rectangle in rectangles if rectangle < cell_set]
        if not contained:
            continue
        require_equal("unique rectangle in a five-cell set", len(contained), 1)
        rectangle = contained[0]
        fifth = next(iter(cell_set - rectangle))
        rows = {cell // N for cell in rectangle}
        columns = {cell % N for cell in rectangle}
        fifth_row, fifth_column = divmod(fifth, N)
        orbit = (
            "attached"
            if fifth_row in rows or fifth_column in columns
            else "external"
        )
        counts[orbit] += 1
    require_equal("attached coordinate five-planes", counts["attached"], 1200)
    require_equal("external coordinate five-planes", counts["external"], 900)
    require_equal("all coordinate five-planes with a rectangle", sum(counts.values()), 2100)
    return dict(sorted(counts.items()))


def verify_dimension_four_flags(
    blocks: list[tuple[list[int], dict[int, int]]],
    by_weight: list[list[tuple[int, int]]],
) -> dict[str, object]:
    histogram: Counter[int] = Counter()
    checked = 0
    for rectangle in rectangle_sets():
        nine_weights = quotient_universe(sorted(rectangle))
        require_equal("rectangle quotient dimension", len(nine_weights), 9)
        selected = set(nine_weights)
        masks, base_value = masks_and_value(selected, blocks, by_weight)
        for extra_weight in range(225):
            if extra_weight in selected:
                continue
            value = base_value + extension_delta(
                masks, extra_weight, blocks, by_weight
            )
            histogram[value] += 1
            checked += 1
    expected_histogram = {20: 12300, 21: 5700, 22: 3600}
    require_equal("four-dimensional flag count", checked, 21600)
    require_equal(
        "four-dimensional flag histogram",
        dict(sorted(histogram.items())),
        expected_histogram,
    )
    return {
        "factor_span_dimension": 4,
        "flags_checked": checked,
        "histogram": {str(key): value for key, value in expected_histogram.items()},
        "maximum": max(histogram),
    }


def verify_dimension_five_flags(
    blocks: list[tuple[list[int], dict[int, int]]],
    by_weight: list[list[tuple[int, int]]],
) -> dict[str, object]:
    representatives = {
        "attached": [0, 1, 2, 5, 6],
        "external": [0, 1, 5, 6, 12],
    }
    histogram: Counter[int] = Counter()
    orbit_maxima: dict[str, int] = {}
    checked = 0
    for orbit, cells in representatives.items():
        universe = quotient_universe(cells)
        require_equal(f"{orbit} quotient universe size", len(universe), 14)
        orbit_maximum = -1
        orbit_checked = 0
        for nine_tuple in combinations(universe, 9):
            selected = set(nine_tuple)
            masks, base_value = masks_and_value(selected, blocks, by_weight)
            for extra_weight in range(225):
                if extra_weight in selected:
                    continue
                value = base_value + extension_delta(
                    masks, extra_weight, blocks, by_weight
                )
                histogram[value] += 1
                orbit_maximum = max(orbit_maximum, value)
                checked += 1
                orbit_checked += 1
        require_equal(f"{orbit} flag count", orbit_checked, 2002 * 216)
        orbit_maxima[orbit] = orbit_maximum

    expected_histogram = {
        10: 2238,
        11: 10854,
        12: 44407,
        13: 88827,
        14: 143962,
        15: 166486,
        16: 149800,
        17: 110299,
        18: 67615,
        19: 37787,
        20: 19798,
        21: 11214,
        22: 7394,
        23: 2768,
        24: 944,
        25: 451,
        26: 20,
    }
    require_equal("five-dimensional flag count", checked, 864864)
    require_equal("orbit maxima", orbit_maxima, {"attached": 26, "external": 22})
    require_equal(
        "five-dimensional flag histogram",
        dict(sorted(histogram.items())),
        expected_histogram,
    )
    return {
        "factor_span_dimension": 5,
        "flags_checked": checked,
        "orbit_maxima": orbit_maxima,
        "histogram": {
            str(key): value for key, value in expected_histogram.items()
        },
        "maximum": max(histogram),
    }


def build_certificate() -> dict[str, object]:
    blocks = build_local_blocks()
    by_weight = index_blocks(blocks)
    five_plane_counts = classify_coordinate_five_planes()
    dimension_four = verify_dimension_four_flags(blocks, by_weight)
    dimension_five = verify_dimension_five_flags(blocks, by_weight)
    require_equal(
        "global one-intersection flag maximum",
        max(dimension_four["maximum"], dimension_five["maximum"]),
        26,
    )
    return {
        "status": "PASS",
        "claim_type": "standalone exact finite certificate",
        "field": "F_3 reduction of integral divided-power coordinate matrices",
        "quadratic_quotient_weights": 225,
        "reduced_base_matrix_kernel_dimension": 100,
        "coordinate_five_plane_orbits": five_plane_counts,
        "dimension_four": dimension_four,
        "dimension_five": dimension_five,
        "characteristic_zero_conclusion": (
            "For every one-intersection Chow flag covered by the geometric "
            "degeneration theorem, p(W_10) <= 26."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    print("PERM5_ONE_INTERSECTION_FLAG_STANDALONE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
