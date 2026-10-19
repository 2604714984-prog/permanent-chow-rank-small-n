"""Search for a triangular certificate on the chart v_00 != 0.

For fixed v, consider

    psi_v : S^2(V)/E_perm -> coker(delta(E_perm tensor V)),
    [q] |-> [delta(q tensor v)].

The expected kernel is the line [v^2], hence rank 99.  This script reduces
the map modulo delta(E_perm tensor V), chooses a 99 x 99 nonsingular block
at v=e_00, normalizes its constant matrix to the identity, and checks
whether all other coefficient matrices are simultaneously strictly
triangular.  If they are, the determinant of the block is identically
v_00^99 on this chart.
"""

from __future__ import annotations

import argparse
from itertools import combinations, combinations_with_replacement

import perm4_chow_experiments as exp


WEDGE_BASIS = list(combinations(range(exp.N), 2))
WEDGE_INDEX = {
    wedge: index for index, wedge in enumerate(WEDGE_BASIS)
}
QUADRATIC_BASIS = list(combinations_with_replacement(range(exp.N), 2))


def echelon_add(
    column: dict[int, int],
    pivots: dict[int, dict[int, int]],
    prime: int,
) -> int | None:
    column = dict(column)
    while column:
        pivot = min(column)
        value = column[pivot] % prime
        if not value:
            del column[pivot]
            continue
        if pivot not in pivots:
            inverse = pow(value, prime - 2, prime)
            normalized = {
                row: coefficient * inverse % prime
                for row, coefficient in column.items()
                if coefficient % prime
            }
            pivots[pivot] = normalized
            return pivot
        basis = pivots[pivot]
        for row, coefficient in basis.items():
            updated = (
                column.get(row, 0) - value * coefficient
            ) % prime
            if updated:
                column[row] = updated
            else:
                column.pop(row, None)
    return None


def reduce_column(
    column: dict[int, int],
    pivots: dict[int, dict[int, int]],
    prime: int,
) -> dict[int, int]:
    column = dict(column)
    while column:
        pivot = min(column)
        if pivot not in pivots:
            break
        value = column[pivot] % prime
        basis = pivots[pivot]
        for row, coefficient in basis.items():
            updated = (
                column.get(row, 0) - value * coefficient
            ) % prime
            if updated:
                column[row] = updated
            else:
                column.pop(row, None)
    # Remaining columns can still contain later A pivots.
    for pivot in sorted(pivots):
        value = column.get(pivot, 0) % prime
        if not value:
            continue
        basis = pivots[pivot]
        for row, coefficient in basis.items():
            updated = (
                column.get(row, 0) - value * coefficient
            ) % prime
            if updated:
                column[row] = updated
            else:
                column.pop(row, None)
    return column


def delta_one(
    monomial: tuple[int, int],
    wedge_variable: int,
    prime: int,
) -> dict[int, int]:
    column: dict[int, int] = {}
    for index, variable in enumerate(monomial):
        remaining = monomial[1 - index]
        sign, wedge = exp.wedge_add(variable, (wedge_variable,))
        if sign:
            row = remaining * len(WEDGE_BASIS) + WEDGE_INDEX[wedge]
            column[row] = (column.get(row, 0) + sign) % prime
    return {row: value for row, value in column.items() if value}


def invert_matrix(
    matrix: list[list[int]],
    prime: int,
) -> list[list[int]]:
    size = len(matrix)
    augmented = [
        [value % prime for value in row]
        + [int(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            row
            for row in range(column, size)
            if augmented[row][column]
        )
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        inverse = pow(augmented[column][column], prime - 2, prime)
        augmented[column] = [
            value * inverse % prime for value in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    (left - factor * right) % prime
                    for left, right in zip(
                        augmented[row],
                        augmented[column],
                    )
                ]
    return [row[size:] for row in augmented]


def multiply(
    left: list[list[int]],
    right: list[list[int]],
    prime: int,
) -> list[list[int]]:
    size = len(left)
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        for k, value in enumerate(left[i]):
            if not value:
                continue
            for j, other in enumerate(right[k]):
                if other:
                    result[i][j] = (
                        result[i][j] + value * other
                    ) % prime
    return result


def topological_order(
    matrices: list[list[list[int]]],
) -> list[int] | None:
    size = len(matrices[0])
    outgoing = [set() for _ in range(size)]
    indegree = [0] * size
    for matrix in matrices:
        for row in range(size):
            for column, value in enumerate(matrix[row]):
                if value and row != column and column not in outgoing[row]:
                    outgoing[row].add(column)
                    indegree[column] += 1
            if matrix[row][row]:
                return None
    ready = [index for index, degree in enumerate(indegree) if degree == 0]
    order = []
    while ready:
        node = ready.pop()
        order.append(node)
        for target in outgoing[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    return order if len(order) == size else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", type=int, default=1_000_003)
    args = parser.parse_args()
    exp.MOD = args.prime

    a_pivots: dict[int, dict[int, int]] = {}
    for column in exp.koszul_columns(exp.perm4_poly(), 2, 1):
        echelon_add(column, a_pivots, args.prime)
    print(f"rank_delta_E={len(a_pivots)}")

    reduced = []
    for wedge_variable in range(exp.N):
        reduced.append(
            [
                reduce_column(
                    delta_one(monomial, wedge_variable, args.prime),
                    a_pivots,
                    args.prime,
                )
                for monomial in QUADRATIC_BASIS
            ]
        )

    quotient_pivots: dict[int, dict[int, int]] = {}
    selected_columns = []
    selected_rows = []
    for column_index, column in enumerate(reduced[0]):
        pivot = echelon_add(column, quotient_pivots, args.prime)
        if pivot is not None:
            selected_columns.append(column_index)
            selected_rows.append(pivot)
    print(f"rank_psi_e00={len(selected_columns)}")
    if len(selected_columns) != 99:
        raise SystemExit("unexpected chart rank")

    coefficient_matrices = []
    for wedge_variable in range(exp.N):
        coefficient_matrices.append(
            [
                [
                    reduced[wedge_variable][column].get(row, 0)
                    for column in selected_columns
                ]
                for row in selected_rows
            ]
        )

    inverse_constant = invert_matrix(
        coefficient_matrices[0],
        args.prime,
    )
    normalized = [
        multiply(inverse_constant, matrix, args.prime)
        for matrix in coefficient_matrices[1:]
    ]
    order = topological_order(normalized)
    nonzero_diagonals = sum(
        bool(matrix[index][index])
        for matrix in normalized
        for index in range(99)
    )
    edge_count = len(
        {
            (row, column)
            for matrix in normalized
            for row in range(99)
            for column in range(99)
            if matrix[row][column]
        }
    )
    print(f"normalized_nonzero_diagonals={nonzero_diagonals}")
    print(f"normalized_union_support={edge_count}")
    print(f"simultaneously_strict_triangular={order is not None}")
    if order is not None:
        print(f"topological_order={order}")
        print("chart_minor=v00^99")


if __name__ == "__main__":
    main()
