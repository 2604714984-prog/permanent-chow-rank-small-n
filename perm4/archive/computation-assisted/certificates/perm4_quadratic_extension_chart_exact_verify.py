"""Exact rational verification of the v_00 chart minor.

This reconstructs the 560 permanent columns and the 99 quotient columns
selected by `perm4_quadratic_extension_chart_certificate.py`, forms the
corresponding concrete 659 x 659 minor, and computes its Schur complement
over QQ with python-flint.  It then verifies that after normalizing the
v_00 coefficient to the identity, all other 15 coefficient matrices are
simultaneously strictly triangular.

That proves the determinant of this concrete minor is

    nonzero_rational_constant * v_00^99

over characteristic zero.
"""

from __future__ import annotations

import argparse

from flint import fmpq_mat

import perm4_chow_experiments as exp
from perm4_quadratic_extension_chart_certificate import (
    QUADRATIC_BASIS,
    delta_one,
    echelon_add,
    reduce_column,
    topological_order,
)


def lift(value: int, prime: int) -> int:
    value %= prime
    return value - prime if value > prime // 2 else value


def dense_submatrix(
    columns: list[dict[int, int]],
    rows: list[int],
    prime: int,
) -> fmpq_mat:
    return fmpq_mat(
        [
            [lift(column.get(row, 0), prime) for column in columns]
            for row in rows
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection-prime", type=int, default=1_000_003)
    args = parser.parse_args()
    prime = args.selection_prime
    exp.MOD = prime

    all_a_columns = list(exp.koszul_columns(exp.perm4_poly(), 2, 1))
    a_pivots: dict[int, dict[int, int]] = {}
    selected_a_indices = []
    selected_a_rows = []
    for index, column in enumerate(all_a_columns):
        pivot = echelon_add(column, a_pivots, prime)
        if pivot is not None:
            selected_a_indices.append(index)
            selected_a_rows.append(pivot)
    selected_a_columns = [
        all_a_columns[index] for index in selected_a_indices
    ]
    print(f"selected_A={len(selected_a_columns)}")

    reduced = []
    original_q = []
    for wedge_variable in range(exp.N):
        original_columns = [
            delta_one(monomial, wedge_variable, prime)
            for monomial in QUADRATIC_BASIS
        ]
        original_q.append(original_columns)
        reduced.append(
            [
                reduce_column(column, a_pivots, prime)
                for column in original_columns
            ]
        )

    quotient_pivots: dict[int, dict[int, int]] = {}
    selected_q_indices = []
    selected_q_rows = []
    for index, column in enumerate(reduced[0]):
        pivot = echelon_add(column, quotient_pivots, prime)
        if pivot is not None:
            selected_q_indices.append(index)
            selected_q_rows.append(pivot)
    print(f"selected_Q={len(selected_q_indices)}")

    a_top = dense_submatrix(
        selected_a_columns,
        selected_a_rows,
        prime,
    )
    a_bottom = dense_submatrix(
        selected_a_columns,
        selected_q_rows,
        prime,
    )

    q_top_blocks = []
    q_bottom_blocks = []
    for wedge_variable in range(exp.N):
        columns = [
            original_q[wedge_variable][index]
            for index in selected_q_indices
        ]
        q_top_blocks.append(
            dense_submatrix(columns, selected_a_rows, prime)
        )
        q_bottom_blocks.append(
            dense_submatrix(columns, selected_q_rows, prime)
        )

    q_top_all = fmpq_mat(
        [
            [
                block[row, column]
                for block in q_top_blocks
                for column in range(block.ncols())
            ]
            for row in range(q_top_blocks[0].nrows())
        ]
    )
    print(
        f"solving_A_top={a_top.nrows()}x{a_top.ncols()} "
        f"rhs={q_top_all.nrows()}x{q_top_all.ncols()}"
    )
    solved_all = a_top.solve(q_top_all)

    schur_blocks = []
    width = len(selected_q_indices)
    for index, q_bottom in enumerate(q_bottom_blocks):
        solved = fmpq_mat(
            [
                [
                    solved_all[row, index * width + column]
                    for column in range(width)
                ]
                for row in range(solved_all.nrows())
            ]
        )
        schur_blocks.append(q_bottom - a_bottom * solved)

    inverse_constant = schur_blocks[0].inv()
    normalized = [
        inverse_constant * block for block in schur_blocks[1:]
    ]

    normalized_lists = []
    nonzero_diagonals = 0
    support = set()
    for matrix in normalized:
        values = []
        for row in range(width):
            value_row = []
            for column in range(width):
                value = matrix[row, column]
                value_row.append(value)
                if value:
                    support.add((row, column))
                    if row == column:
                        nonzero_diagonals += 1
            values.append(value_row)
        normalized_lists.append(values)

    order = topological_order(normalized_lists)
    a_determinant = a_top.det()
    determinant = schur_blocks[0].det()
    full_minor_constant = a_determinant * determinant
    print(f"A_top_determinant={a_determinant}")
    print(f"constant_block_determinant={determinant}")
    print(f"full_minor_constant={full_minor_constant}")
    print(f"exact_nonzero_diagonals={nonzero_diagonals}")
    print(f"exact_union_support={len(support)}")
    print(f"exact_simultaneously_strict_triangular={order is not None}")
    if order is None:
        raise SystemExit("exact triangular certificate failed")
    print(f"topological_order={order}")
    print("exact_chart_minor=constant*v00^99")


if __name__ == "__main__":
    main()
