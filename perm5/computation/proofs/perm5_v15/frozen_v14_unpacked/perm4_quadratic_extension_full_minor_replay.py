"""Direct modular replay of the concrete 659 x 659 chart minor.

Unlike the exact Schur/triangular verifier, this script assembles the full
minor and asks FLINT for its determinant at independent random parameter
points and primes.  It checks

    det = -32768 * v_00^99.

This is a cross-check of the implementation path, not a replacement for the
exact rational proof.
"""

from __future__ import annotations

import argparse
import random

from flint import nmod_mat

import perm4_chow_experiments as exp
from perm4_quadratic_extension_chart_certificate import (
    QUADRATIC_BASIS,
    delta_one,
    echelon_add,
    reduce_column,
)


def select_indices(prime: int) -> tuple[list[int], list[int], list[int], list[int]]:
    exp.MOD = prime
    all_a = list(exp.koszul_columns(exp.perm4_poly(), 2, 1))
    a_pivots: dict[int, dict[int, int]] = {}
    a_indices = []
    a_rows = []
    for index, column in enumerate(all_a):
        pivot = echelon_add(column, a_pivots, prime)
        if pivot is not None:
            a_indices.append(index)
            a_rows.append(pivot)

    reduced_q = [
        reduce_column(
            delta_one(monomial, 0, prime),
            a_pivots,
            prime,
        )
        for monomial in QUADRATIC_BASIS
    ]
    q_pivots: dict[int, dict[int, int]] = {}
    q_indices = []
    q_rows = []
    for index, column in enumerate(reduced_q):
        pivot = echelon_add(column, q_pivots, prime)
        if pivot is not None:
            q_indices.append(index)
            q_rows.append(pivot)
    return a_indices, a_rows, q_indices, q_rows


def full_determinant(
    prime: int,
    vector: list[int],
    selection: tuple[list[int], list[int], list[int], list[int]],
) -> int:
    a_indices, a_rows, q_indices, q_rows = selection
    exp.MOD = prime
    all_a = list(exp.koszul_columns(exp.perm4_poly(), 2, 1))
    a_columns = [all_a[index] for index in a_indices]
    q_columns = []
    for q_index in q_indices:
        monomial = QUADRATIC_BASIS[q_index]
        column: dict[int, int] = {}
        for variable, coefficient in enumerate(vector):
            if not coefficient:
                continue
            for row, value in delta_one(
                monomial,
                variable,
                prime,
            ).items():
                column[row] = (
                    column.get(row, 0) + coefficient * value
                ) % prime
        q_columns.append(column)

    rows = a_rows + q_rows
    columns = a_columns + q_columns
    matrix = nmod_mat(len(rows), len(columns), prime)
    row_index = {row: index for index, row in enumerate(rows)}
    for column_index, column in enumerate(columns):
        for row, value in column.items():
            if row in row_index:
                matrix[row_index[row], column_index] = value % prime
    return int(matrix.det())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection-prime", type=int, default=1_000_003)
    parser.add_argument(
        "--primes",
        type=int,
        nargs="+",
        default=(1_000_033, 1_000_037),
    )
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260727)
    args = parser.parse_args()

    selection = select_indices(args.selection_prime)
    print(
        f"selected_A={len(selection[0])} "
        f"selected_Q={len(selection[2])}"
    )
    rng = random.Random(args.seed)
    failures = []
    for prime in args.primes:
        for sample in range(args.samples):
            vector = [rng.randrange(prime) for _ in range(exp.N)]
            if sample == 0:
                vector[0] = 1
            determinant = full_determinant(prime, vector, selection)
            expected = (
                -32768 * pow(vector[0], 99, prime)
            ) % prime
            match = determinant == expected
            print(
                f"prime={prime} sample={sample} v00={vector[0]} "
                f"det={determinant} expected={expected} match={match}"
            )
            if not match:
                failures.append((prime, sample))
    print(f"failures={failures}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
