#!/usr/bin/env python3
"""Second exact implementation of the perm5 one-intersection endpoint bound.

Differences from the frozen verifier:

* cubic divided-power monomials are exponent vectors, not sorted tuples;
* local integer matrices are constructed explicitly before any field choice;
* the complete 886,464 flag set is evaluated independently over F_3, F_5,
  and F_7;
* row/column permutations and transpose explicitly generate the two five-plane
  orbits from their representatives;
* every maximal attached flag is identified and rechecked over QQ.

The program imports no project generator and reads no frozen certificate.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations
from pathlib import Path


N = 5
VARIABLE_COUNT = N * N
PRIMES = (3, 5, 7)
Descriptor = tuple[object, ...]
Exponent = tuple[int, ...]


def require_equal(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise RuntimeError(
            f"{label} mismatch: expected {expected!r}, observed {actual!r}"
        )


def descriptor_key(descriptor: Descriptor) -> str:
    return ":".join(str(value) for value in descriptor)


def build_quotient_basis() -> tuple[list[Descriptor], dict[Descriptor, int]]:
    basis: list[Descriptor] = []
    for row in range(N):
        for column in range(N):
            basis.append(("square", row, column))
    for row in range(N):
        for first, second in combinations(range(N), 2):
            basis.append(("row", row, first, second))
    for column in range(N):
        for first, second in combinations(range(N), 2):
            basis.append(("column", first, second, column))
    for first_row, second_row in combinations(range(N), 2):
        for first_column, second_column in combinations(range(N), 2):
            basis.append(
                ("cross", first_row, second_row, first_column, second_column)
            )
    require_equal("quadratic quotient dimension", len(basis), 225)
    return basis, {descriptor: index for index, descriptor in enumerate(basis)}


QUOTIENT_BASIS, QUOTIENT_INDEX = build_quotient_basis()


def exponent_from_variables(variables: tuple[int, ...]) -> Exponent:
    values = [0] * VARIABLE_COUNT
    for variable in variables:
        values[variable] += 1
    return tuple(values)


def quotient_coordinate(exponent: Exponent) -> tuple[int, int]:
    variables = [
        variable
        for variable, multiplicity in enumerate(exponent)
        for _ in range(multiplicity)
    ]
    require_equal("quadratic total degree", len(variables), 2)
    first, second = variables
    first_row, first_column = divmod(first, N)
    second_row, second_column = divmod(second, N)
    if first == second:
        descriptor = ("square", first_row, first_column)
        return QUOTIENT_INDEX[descriptor], 1
    if first_row == second_row:
        descriptor = (
            "row",
            first_row,
            min(first_column, second_column),
            max(first_column, second_column),
        )
        return QUOTIENT_INDEX[descriptor], 1
    if first_column == second_column:
        descriptor = (
            "column",
            min(first_row, second_row),
            max(first_row, second_row),
            first_column,
        )
        return QUOTIENT_INDEX[descriptor], 1
    low_row, high_row = sorted((first_row, second_row))
    low_column, high_column = sorted((first_column, second_column))
    descriptor = ("cross", low_row, high_row, low_column, high_column)
    canonical = {
        N * low_row + low_column,
        N * high_row + high_column,
    }
    sign = 1 if {first, second} == canonical else -1
    return QUOTIENT_INDEX[descriptor], sign


def torus_weight(exponent: Exponent) -> tuple[int, ...]:
    rows = [0] * N
    columns = [0] * N
    for variable, multiplicity in enumerate(exponent):
        row, column = divmod(variable, N)
        rows[row] += multiplicity
        columns[column] += multiplicity
    return tuple(rows + columns)


def cubic_exponents() -> list[Exponent]:
    result = [
        exponent_from_variables(variables)
        for variables in combinations_with_replacement(range(VARIABLE_COUNT), 3)
    ]
    require_equal("cubic divided-power monomial count", len(result), 2925)
    return result


def integer_blocks() -> list[tuple[list[int], list[tuple[int, list[int]]]]]:
    grouped: dict[tuple[int, ...], list[Exponent]] = defaultdict(list)
    for exponent in cubic_exponents():
        grouped[torus_weight(exponent)].append(exponent)
    require_equal("cubic torus-weight block count", len(grouped), 1225)

    result: list[tuple[list[int], list[tuple[int, list[int]]]]] = []
    for monomials in grouped.values():
        rows: dict[tuple[int, int], list[int]] = {}
        involved: set[int] = set()
        for column_index, exponent in enumerate(monomials):
            for variable, multiplicity in enumerate(exponent):
                if multiplicity == 0:
                    continue
                derivative = list(exponent)
                derivative[variable] -= 1
                quotient, sign = quotient_coordinate(tuple(derivative))
                involved.add(quotient)
                row = rows.setdefault(
                    (variable, quotient), [0] * len(monomials)
                )
                row[column_index] += sign
        ordered = sorted(involved)
        ordered_rows = [
            (quotient, row)
            for (_variable, quotient), row in sorted(rows.items())
        ]
        result.append((ordered, ordered_rows))
    require_equal("integer block count", len(result), 1225)
    return result


def rank_mod(rows: list[list[int]], prime: int) -> int:
    matrix = [
        [value % prime for value in row]
        for row in rows
        if any(value % prime for value in row)
    ]
    if not matrix:
        return 0
    row_index = 0
    column_count = len(matrix[0])
    for column in range(column_count):
        pivot = next(
            (
                candidate
                for candidate in range(row_index, len(matrix))
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[row_index], matrix[pivot] = matrix[pivot], matrix[row_index]
        inverse = pow(matrix[row_index][column], -1, prime)
        matrix[row_index] = [
            inverse * value % prime for value in matrix[row_index]
        ]
        for target in range(len(matrix)):
            if target == row_index:
                continue
            factor = matrix[target][column]
            if not factor:
                continue
            matrix[target] = [
                (left - factor * right) % prime
                for left, right in zip(matrix[target], matrix[row_index])
            ]
        row_index += 1
        if row_index == len(matrix):
            break
    return row_index


def rank_qq(rows: list[list[int]]) -> int:
    matrix = [
        [Fraction(value) for value in row]
        for row in rows
        if any(value for value in row)
    ]
    if not matrix:
        return 0
    row_index = 0
    column_count = len(matrix[0])
    for column in range(column_count):
        pivot = next(
            (
                candidate
                for candidate in range(row_index, len(matrix))
                if matrix[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[row_index], matrix[pivot] = matrix[pivot], matrix[row_index]
        value = matrix[row_index][column]
        matrix[row_index] = [entry / value for entry in matrix[row_index]]
        for target in range(len(matrix)):
            if target == row_index:
                continue
            factor = matrix[target][column]
            if not factor:
                continue
            matrix[target] = [
                left - factor * right
                for left, right in zip(matrix[target], matrix[row_index])
            ]
        row_index += 1
        if row_index == len(matrix):
            break
    return row_index


def quotient_of_cells(cells: tuple[int, ...] | list[int]) -> list[int]:
    return sorted(
        {
            quotient_coordinate(exponent_from_variables(pair))[0]
            for pair in combinations_with_replacement(cells, 2)
        }
    )


def rectangles() -> list[tuple[int, ...]]:
    return [
        tuple(N * row + column for row in rows for column in columns)
        for rows in combinations(range(N), 2)
        for columns in combinations(range(N), 2)
    ]


def transform_cells(
    cells: tuple[int, ...],
    row_permutation: tuple[int, ...],
    column_permutation: tuple[int, ...],
    transpose: bool,
) -> tuple[int, ...]:
    transformed = []
    for cell in cells:
        row, column = divmod(cell, N)
        row = row_permutation[row]
        column = column_permutation[column]
        if transpose:
            row, column = column, row
        transformed.append(N * row + column)
    return tuple(sorted(transformed))


def explicit_five_plane_orbits() -> dict[str, set[tuple[int, ...]]]:
    representatives = {
        "attached": (0, 1, 2, 5, 6),
        "external": (0, 1, 5, 6, 12),
    }
    permutations5 = tuple(permutations(range(N)))
    orbits: dict[str, set[tuple[int, ...]]] = {}
    for name, representative in representatives.items():
        orbit = {
            transform_cells(representative, row_perm, column_perm, transpose)
            for row_perm in permutations5
            for column_perm in permutations5
            for transpose in (False, True)
        }
        orbits[name] = orbit
    require_equal("attached orbit size", len(orbits["attached"]), 1200)
    require_equal("external orbit size", len(orbits["external"]), 900)
    require_equal(
        "five-plane orbit disjointness",
        len(orbits["attached"] & orbits["external"]),
        0,
    )
    return orbits


def prepare_prime_tables(
    blocks: list[tuple[list[int], list[tuple[int, list[int]]]]], prime: int
) -> tuple[list[tuple[list[int], dict[int, int]]], int]:
    tables: list[tuple[list[int], dict[int, int]]] = []
    base_kernel_total = 0
    for involved, labelled_rows in blocks:
        rows = [row for _quotient, row in labelled_rows]
        column_count = len(rows[0]) if rows else 0
        base_kernel = column_count - rank_mod(rows, prime)
        base_kernel_total += base_kernel
        table: dict[int, int] = {}
        positions = {weight: index for index, weight in enumerate(involved)}
        for mask in range(1 << len(involved)):
            constrained = [
                row
                for quotient, row in labelled_rows
                if not (mask >> positions[quotient]) & 1
            ]
            relative_kernel = (
                column_count - rank_mod(constrained, prime) - base_kernel
            )
            if relative_kernel:
                table[mask] = relative_kernel
        tables.append((involved, table))
    return tables, base_kernel_total


def index_prime_tables(
    tables: list[tuple[list[int], dict[int, int]]]
) -> list[list[tuple[int, int]]]:
    by_weight: list[list[tuple[int, int]]] = [
        [] for _ in range(len(QUOTIENT_BASIS))
    ]
    for block_index, (involved, _table) in enumerate(tables):
        for position, weight in enumerate(involved):
            by_weight[weight].append((block_index, 1 << position))
    return by_weight


def masks_and_value(
    selected: frozenset[int],
    tables: list[tuple[list[int], dict[int, int]]],
    by_weight: list[list[tuple[int, int]]],
) -> tuple[list[int], int]:
    masks = [0] * len(tables)
    for weight in selected:
        for block_index, bit in by_weight[weight]:
            masks[block_index] |= bit
    value = sum(
        table.get(mask, 0)
        for mask, (_involved, table) in zip(masks, tables)
    )
    return masks, value


def extension_delta(
    masks: list[int],
    extra_weight: int,
    tables: list[tuple[list[int], dict[int, int]]],
    by_weight: list[list[tuple[int, int]]],
) -> int:
    value = 0
    for block_index, bit in by_weight[extra_weight]:
        table = tables[block_index][1]
        old_mask = masks[block_index]
        value += table.get(old_mask | bit, 0) - table.get(old_mask, 0)
    return value


def serialize_flag(nine: tuple[int, ...], extra: int) -> dict[str, object]:
    return {
        "nine_weights": [descriptor_key(QUOTIENT_BASIS[index]) for index in nine],
        "extra_weight": descriptor_key(QUOTIENT_BASIS[extra]),
        "ten_weight_set": [
            descriptor_key(QUOTIENT_BASIS[index])
            for index in sorted((*nine, extra))
        ],
    }


def evaluate_prime(
    prime: int,
    blocks: list[tuple[list[int], list[tuple[int, list[int]]]]],
) -> tuple[dict[str, object], list[tuple[tuple[int, ...], int]]]:
    tables, base_kernel = prepare_prime_tables(blocks, prime)
    require_equal(f"base kernel over F_{prime}", base_kernel, 100)
    by_weight = index_prime_tables(tables)

    four_histogram: Counter[int] = Counter()
    four_checked = 0
    for rectangle in rectangles():
        nine = tuple(quotient_of_cells(rectangle))
        require_equal("rectangle quotient size", len(nine), 9)
        selected = frozenset(nine)
        masks, base_value = masks_and_value(selected, tables, by_weight)
        for extra in range(len(QUOTIENT_BASIS)):
            if extra in selected:
                continue
            value = base_value + extension_delta(
                masks, extra, tables, by_weight
            )
            four_histogram[value] += 1
            four_checked += 1
    require_equal("four-dimensional flag count", four_checked, 21_600)
    require_equal("four-dimensional maximum", max(four_histogram), 22)

    representatives = {
        "attached": (0, 1, 2, 5, 6),
        "external": (0, 1, 5, 6, 12),
    }
    orbit_results: dict[str, object] = {}
    attached_max_flags: list[tuple[tuple[int, ...], int]] = []
    for orbit, cells in representatives.items():
        universe = quotient_of_cells(cells)
        require_equal(f"{orbit} quotient universe size", len(universe), 14)
        histogram: Counter[int] = Counter()
        maximum = -1
        maximum_flags: list[tuple[tuple[int, ...], int]] = []
        checked = 0
        for nine in combinations(universe, 9):
            selected = frozenset(nine)
            masks, base_value = masks_and_value(selected, tables, by_weight)
            for extra in range(len(QUOTIENT_BASIS)):
                if extra in selected:
                    continue
                value = base_value + extension_delta(
                    masks, extra, tables, by_weight
                )
                histogram[value] += 1
                checked += 1
                if value > maximum:
                    maximum = value
                    maximum_flags = [(nine, extra)]
                elif value == maximum:
                    maximum_flags.append((nine, extra))
        require_equal(f"{orbit} flag count", checked, 432_432)
        expected_maximum = 26 if orbit == "attached" else 22
        require_equal(f"{orbit} maximum", maximum, expected_maximum)
        if orbit == "attached":
            require_equal("attached maximum flag count", len(maximum_flags), 20)
            attached_max_flags = maximum_flags
        orbit_results[orbit] = {
            "flags_checked": checked,
            "histogram": dict(sorted(histogram.items())),
            "maximum": maximum,
            "maximum_flag_count": len(maximum_flags),
        }

    result = {
        "prime": prime,
        "base_kernel_dimension": base_kernel,
        "dimension_four": {
            "flags_checked": four_checked,
            "histogram": dict(sorted(four_histogram.items())),
            "maximum": max(four_histogram),
        },
        "dimension_five": orbit_results,
        "total_flags_checked": four_checked + 2 * 432_432,
    }
    require_equal("total flag count", result["total_flags_checked"], 886_464)
    return result, attached_max_flags


def relative_kernel_qq(
    blocks: list[tuple[list[int], list[tuple[int, list[int]]]]],
    selected: frozenset[int],
) -> tuple[int, int]:
    base_total = 0
    relative_total = 0
    for _involved, labelled_rows in blocks:
        rows = [row for _quotient, row in labelled_rows]
        column_count = len(rows[0]) if rows else 0
        base_kernel = column_count - rank_qq(rows)
        constrained = [
            row for quotient, row in labelled_rows if quotient not in selected
        ]
        kernel = column_count - rank_qq(constrained)
        base_total += base_kernel
        relative_total += kernel - base_kernel
    return base_total, relative_total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    blocks = integer_blocks()
    orbits = explicit_five_plane_orbits()
    require_equal(
        "five-plane orbit total",
        len(orbits["attached"]) + len(orbits["external"]),
        2100,
    )

    prime_results: dict[str, object] = {}
    maximal_flags_by_prime: dict[int, list[tuple[tuple[int, ...], int]]] = {}
    for prime in PRIMES:
        result, maximal_flags = evaluate_prime(prime, blocks)
        prime_results[str(prime)] = result
        maximal_flags_by_prime[prime] = maximal_flags

    canonical = sorted(maximal_flags_by_prime[PRIMES[0]])
    for prime in PRIMES[1:]:
        require_equal(
            f"F{PRIMES[0]}/F{prime} maximal attached flags",
            canonical,
            sorted(maximal_flags_by_prime[prime]),
        )

    qq_records = []
    for nine, extra in canonical:
        base_kernel, relative_kernel = relative_kernel_qq(
            blocks, frozenset((*nine, extra))
        )
        require_equal("QQ base kernel", base_kernel, 100)
        require_equal("QQ maximal relative kernel", relative_kernel, 26)
        qq_records.append(
            {
                **serialize_flag(nine, extra),
                "base_kernel_QQ": base_kernel,
                "relative_kernel_QQ": relative_kernel,
            }
        )

    certificate = {
        "status": "PASS",
        "claim_type": "independent multifield exact endpoint certificate",
        "imports_project_generator": False,
        "reads_frozen_result": False,
        "monomial_encoding": "25-entry divided-power exponent vectors",
        "primes": list(PRIMES),
        "quadratic_quotient_weights": len(QUOTIENT_BASIS),
        "cubic_torus_blocks": len(blocks),
        "five_plane_orbit_sizes": {
            name: len(orbit) for name, orbit in orbits.items()
        },
        "prime_results": prime_results,
        "maximal_attached_flags_QQ": qq_records,
        "characteristic_zero_conclusion": (
            "Every one-intersection endpoint has relative prolongation kernel "
            "at most 26 over characteristic zero."
        ),
    }
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    print("PERM5_ONE_INTERSECTION_INDEPENDENT_MULTIFIELD_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
