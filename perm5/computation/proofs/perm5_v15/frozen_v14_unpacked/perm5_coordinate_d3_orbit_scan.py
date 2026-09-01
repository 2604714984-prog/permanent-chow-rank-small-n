"""Exhaustive orbit scan of coordinate three-direction quotient spaces.

The 325 quadratic monomials give 225 projectively distinct classes modulo
E_5: 25 squares, 50 same-row edges, 50 same-column edges, and 100 rectangle
matching classes.  This script enumerates all C(225,3)=1,873,200 triples,
reduces them under S_5 x S_5 and transpose, and computes the exact F_3
Koszul rank for every orbit representative.

The family scan is exhaustive and every modular rank is exact.  Its scope is
still the coordinate quotient family, not arbitrary three-dimensional W.
"""

from __future__ import annotations

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

from perm35_exact_verification import KoszulData, add_column


PRIME = 3
OUTPUT = Path(__file__).with_name(
    "n5_coordinate_d3_orbits_F3_exact.json"
)
N = 5


def build_classes() -> list[tuple]:
    classes = []
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
    assert len(classes) == 225
    return classes


CLASSES = build_classes()
CLASS_INDEX = {descriptor: index for index, descriptor in enumerate(CLASSES)}


def swap(value: int, first: int, second: int) -> int:
    if value == first:
        return second
    if value == second:
        return first
    return value


def act(
    descriptor: tuple,
    row_swap: tuple[int, int] | None = None,
    column_swap: tuple[int, int] | None = None,
    transpose: bool = False,
) -> tuple:
    kind = descriptor[0]
    if kind == "S":
        _, row, column = descriptor
        if row_swap:
            row = swap(row, *row_swap)
        if column_swap:
            column = swap(column, *column_swap)
        result = ("S", row, column)
    elif kind == "R":
        _, row, first, second = descriptor
        if row_swap:
            row = swap(row, *row_swap)
        if column_swap:
            first = swap(first, *column_swap)
            second = swap(second, *column_swap)
        first, second = sorted((first, second))
        result = ("R", row, first, second)
    elif kind == "C":
        _, first, second, column = descriptor
        if row_swap:
            first = swap(first, *row_swap)
            second = swap(second, *row_swap)
        if column_swap:
            column = swap(column, *column_swap)
        first, second = sorted((first, second))
        result = ("C", first, second, column)
    else:
        _, r1, r2, c1, c2 = descriptor
        if row_swap:
            r1 = swap(r1, *row_swap)
            r2 = swap(r2, *row_swap)
        if column_swap:
            c1 = swap(c1, *column_swap)
            c2 = swap(c2, *column_swap)
        r1, r2 = sorted((r1, r2))
        c1, c2 = sorted((c1, c2))
        result = ("X", r1, r2, c1, c2)

    if not transpose:
        return result
    kind = result[0]
    if kind == "S":
        _, row, column = result
        return ("S", column, row)
    if kind == "R":
        _, row, first, second = result
        return ("C", first, second, row)
    if kind == "C":
        _, first, second, column = result
        return ("R", column, first, second)
    _, r1, r2, c1, c2 = result
    return ("X", c1, c2, r1, r2)


def generator_permutations() -> list[list[int]]:
    generators = []
    for first in range(4):
        generators.append(
            [
                CLASS_INDEX[
                    act(descriptor, row_swap=(first, first + 1))
                ]
                for descriptor in CLASSES
            ]
        )
    for first in range(4):
        generators.append(
            [
                CLASS_INDEX[
                    act(descriptor, column_swap=(first, first + 1))
                ]
                for descriptor in CLASSES
            ]
        )
    generators.append(
        [CLASS_INDEX[act(descriptor, transpose=True)] for descriptor in CLASSES]
    )
    return generators


def encoded(triple: tuple[int, int, int]) -> int:
    first, second, third = triple
    return (first * 225 + second) * 225 + third


def representative_monomial(descriptor: tuple) -> tuple[int, int]:
    kind = descriptor[0]
    if kind == "S":
        _, row, column = descriptor
        variable = 5 * row + column
        return (variable, variable)
    if kind == "R":
        _, row, first, second = descriptor
        return (5 * row + first, 5 * row + second)
    if kind == "C":
        _, first, second, column = descriptor
        return (5 * first + column, 5 * second + column)
    _, r1, r2, c1, c2 = descriptor
    return (5 * r1 + c1, 5 * r2 + c2)


def enumerate_orbits() -> list[dict]:
    generators = generator_permutations()
    visited = bytearray(225**3)
    orbits = []
    for triple in combinations(range(225), 3):
        code = encoded(triple)
        if visited[code]:
            continue
        visited[code] = 1
        queue = deque([triple])
        members = 0
        minimum = triple
        while queue:
            current = queue.popleft()
            members += 1
            if current < minimum:
                minimum = current
            for permutation in generators:
                image = tuple(
                    sorted(permutation[index] for index in current)
                )
                image_code = encoded(image)
                if not visited[image_code]:
                    visited[image_code] = 1
                    queue.append(image)
        orbits.append(
            {
                "representative": minimum,
                "orbit_size": members,
            }
        )
    assert sum(orbit["orbit_size"] for orbit in orbits) == 1_873_200
    return orbits


def rank_representatives(orbits: list[dict]) -> None:
    data = KoszulData(5)
    base_pivots, _ = data.image_pivots(
        data.permanent_quadrics(), PRIME
    )
    base_rank = len(base_pivots)
    assert base_rank == 2400
    delta_columns = {}
    for class_index, descriptor in enumerate(CLASSES):
        monomial = representative_monomial(descriptor)
        delta_columns[class_index] = [
            data.delta({monomial: 1}, {variable: 1})
            for variable in range(25)
        ]

    for orbit in orbits:
        pivots = {
            pivot: dict(vector)
            for pivot, vector in base_pivots.items()
        }
        for class_index in orbit["representative"]:
            for column in delta_columns[class_index]:
                add_column(column, pivots, PRIME)
        increment = len(pivots) - base_rank
        orbit["koszul_increment_F3"] = increment
        orbit["relative_prolongation_dimension_F3"] = 75 - increment
        orbit["representative_descriptors"] = [
            list(CLASSES[index])
            for index in orbit["representative"]
        ]
        orbit["representative_monomials"] = [
            list(representative_monomial(CLASSES[index]))
            for index in orbit["representative"]
        ]


def main() -> None:
    orbits = enumerate_orbits()
    rank_representatives(orbits)
    increment_histogram_by_triples: Counter[int] = Counter()
    increment_histogram_by_orbits: Counter[int] = Counter()
    for orbit in orbits:
        increment = orbit["koszul_increment_F3"]
        increment_histogram_by_orbits[increment] += 1
        increment_histogram_by_triples[increment] += orbit["orbit_size"]
    minimum = min(increment_histogram_by_triples)
    extremal_orbits = [
        orbit for orbit in orbits
        if orbit["koszul_increment_F3"] == minimum
    ]
    result = {
        "claim_type": (
            "exhaustive exact F_3 scan of the finite coordinate quotient "
            "family, reduced by exact symmetry orbits"
        ),
        "prime": PRIME,
        "coordinate_quotient_classes": len(CLASSES),
        "coordinate_three_spaces_checked": 1_873_200,
        "symmetry_orbits": len(orbits),
        "koszul_increment_histogram_by_three_spaces": {
            str(increment): count
            for increment, count in sorted(
                increment_histogram_by_triples.items()
            )
        },
        "koszul_increment_histogram_by_orbits": {
            str(increment): count
            for increment, count in sorted(
                increment_histogram_by_orbits.items()
            )
        },
        "minimum_koszul_increment_F3": minimum,
        "maximum_relative_prolongation_dimension_F3": 75 - minimum,
        "extremal_orbits": extremal_orbits,
        "all_orbits": orbits,
        "logical_scope": (
            "Every one of the 1,873,200 coordinate quotient three-spaces "
            "is covered and every displayed rank is exact over F_3.  A "
            "modular lower rank also lower-bounds the corresponding QQ "
            "rank, but this finite coordinate family does not cover "
            "arbitrary W."
        ),
        "status": "PASS",
    }
    OUTPUT.write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key != "all_orbits"
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
