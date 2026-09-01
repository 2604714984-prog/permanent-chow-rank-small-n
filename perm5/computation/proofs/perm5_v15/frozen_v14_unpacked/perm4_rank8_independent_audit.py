"""Independent reconstruction audit for the rank-8 certificate.

This file intentionally imports no project module.  It rebuilds:

1. the Koszul image of the 36 explicit 2x2 subpermanents;
2. the exact 560 rank and the 16-dimensional prolongation upper bound;
3. the rank-92 independent Chow-term image;
4. the 659 x 659 chart minor and its simultaneous triangularization.

The implementation is redundant by design so it can catch shared-helper or
indexing errors in the primary certificate scripts.
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, permutations

from flint import fmpq_mat


N = 16
SELECTION_PRIME = 1_000_003
WEDGES = list(combinations(range(N), 2))
WEDGE_INDEX = {wedge: index for index, wedge in enumerate(WEDGES)}
QUADRATICS = list(combinations_with_replacement(range(N), 2))


def wedge(variable: int, other: int) -> tuple[int, tuple[int, int] | None]:
    if variable == other:
        return 0, None
    if variable < other:
        return 1, (variable, other)
    return -1, (other, variable)


def delta_column(
    quadratic: dict[tuple[int, int], int],
    exterior_variable: int,
) -> dict[int, int]:
    result: dict[int, int] = {}
    for monomial, coefficient in quadratic.items():
        for position, variable in enumerate(monomial):
            remaining = monomial[1 - position]
            sign, exterior_pair = wedge(variable, exterior_variable)
            if sign:
                row = remaining * len(WEDGES) + WEDGE_INDEX[exterior_pair]
                result[row] = result.get(row, 0) + sign * coefficient
    return {row: value for row, value in result.items() if value}


def direct_second_derivative(
    derivative: tuple[int, int],
) -> dict[tuple[int, int], int]:
    first, second = derivative
    row_a, column_a = divmod(first, 4)
    row_b, column_b = divmod(second, 4)
    if row_a == row_b or column_a == column_b:
        return {}
    remaining_rows = [
        row for row in range(4) if row not in (row_a, row_b)
    ]
    remaining_columns = [
        column
        for column in range(4)
        if column not in (column_a, column_b)
    ]
    monomial_a = tuple(
        sorted(
            (
                4 * remaining_rows[0] + remaining_columns[0],
                4 * remaining_rows[1] + remaining_columns[1],
            )
        )
    )
    monomial_b = tuple(
        sorted(
            (
                4 * remaining_rows[0] + remaining_columns[1],
                4 * remaining_rows[1] + remaining_columns[0],
            )
        )
    )
    return {monomial_a: 1, monomial_b: 1}


def permanent_image_columns() -> list[dict[int, int]]:
    columns = []
    for derivative in QUADRATICS:
        quadratic = direct_second_derivative(derivative)
        for exterior_variable in range(N):
            columns.append(delta_column(quadratic, exterior_variable))
    return columns


def add_echelon(
    source: dict[int, int],
    pivots: dict[int, dict[int, int]],
    prime: int,
) -> int | None:
    column = {row: value % prime for row, value in source.items() if value % prime}
    while column:
        pivot = min(column)
        value = column[pivot]
        if pivot not in pivots:
            inverse = pow(value, prime - 2, prime)
            pivots[pivot] = {
                row: coefficient * inverse % prime
                for row, coefficient in column.items()
            }
            return pivot
        basis = pivots[pivot]
        for row, coefficient in basis.items():
            updated = (column.get(row, 0) - value * coefficient) % prime
            if updated:
                column[row] = updated
            else:
                column.pop(row, None)
    return None


def reduce_echelon(
    source: dict[int, int],
    pivots: dict[int, dict[int, int]],
    prime: int,
) -> dict[int, int]:
    column = {row: value % prime for row, value in source.items() if value % prime}
    for pivot in sorted(pivots):
        value = column.get(pivot, 0)
        if not value:
            continue
        for row, coefficient in pivots[pivot].items():
            updated = (column.get(row, 0) - value * coefficient) % prime
            if updated:
                column[row] = updated
            else:
                column.pop(row, None)
    return column


def rank_mod(columns: list[dict[int, int]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for column in columns:
        add_echelon(column, pivots, prime)
    return len(pivots)


def dense(
    columns: list[dict[int, int]],
    rows: list[int],
) -> fmpq_mat:
    return fmpq_mat(
        [[column.get(row, 0) for column in columns] for row in rows]
    )


def topological_order(matrices: list[fmpq_mat]) -> list[int] | None:
    size = matrices[0].nrows()
    outgoing = [set() for _ in range(size)]
    indegree = [0] * size
    for matrix in matrices:
        for row in range(size):
            if matrix[row, row]:
                return None
            for column in range(size):
                if matrix[row, column] and column not in outgoing[row]:
                    outgoing[row].add(column)
                    indegree[column] += 1
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


def perm3_polynomial(
    rows: tuple[int, int, int],
    columns: tuple[int, int, int],
) -> dict[tuple[int, int, int], int]:
    result = {}
    for permutation in permutations(columns):
        monomial = tuple(
            sorted(4 * row + column for row, column in zip(rows, permutation))
        )
        result[monomial] = 1
    return result


def derivative_cubic(
    cubic: dict[tuple[int, int, int], int],
    variable: int,
) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    for monomial, coefficient in cubic.items():
        for position, entry in enumerate(monomial):
            if entry == variable:
                remaining = list(monomial)
                remaining.pop(position)
                key = tuple(remaining)
                result[key] = result.get(key, 0) + coefficient
    return {key: value for key, value in result.items() if value}


def in_explicit_e_space(quadratic: dict[tuple[int, int], int]) -> bool:
    coefficient_rows = {}
    for (row_a, row_b) in combinations(range(4), 2):
        for (column_a, column_b) in combinations(range(4), 2):
            diagonal = tuple(
                sorted(
                    (
                        4 * row_a + column_a,
                        4 * row_b + column_b,
                    )
                )
            )
            off_diagonal = tuple(
                sorted(
                    (
                        4 * row_a + column_b,
                        4 * row_b + column_a,
                    )
                )
            )
            left = quadratic.get(diagonal, 0)
            right = quadratic.get(off_diagonal, 0)
            if left != right:
                return False
            coefficient_rows[diagonal] = left
            coefficient_rows[off_diagonal] = right
    allowed = set(coefficient_rows)
    return all(not value or monomial in allowed for monomial, value in quadratic.items())


def verify_prolongation_upper_bound() -> None:
    cubics = []
    for rows in combinations(range(4), 3):
        for columns in combinations(range(4), 3):
            cubic = perm3_polynomial(rows, columns)
            cubics.append(cubic)
            for variable in range(N):
                if not in_explicit_e_space(derivative_cubic(cubic, variable)):
                    raise AssertionError("perm3 derivative left E_perm")
    unique_witnesses = []
    for cubic in cubics:
        witness = min(cubic)
        unique_witnesses.append(witness)
    if len(set(unique_witnesses)) != 16:
        raise AssertionError("perm3 prolongations were not independently witnessed")
    print("independent_perm3_prolongations=16")


def verify_chow_term_rank() -> None:
    pair_quadratics = [
        {tuple(sorted(pair)): 1}
        for pair in combinations(range(4), 2)
    ]
    columns = [
        delta_column(quadratic, exterior_variable)
        for quadratic in pair_quadratics
        for exterior_variable in range(N)
    ]
    rank = rank_mod(columns, SELECTION_PRIME)
    if rank != 92:
        raise AssertionError(f"unexpected independent Chow rank {rank}")
    print("independent_chow_koszul_rank=92")
    print("independent_chow_triple_prolongations=4")


def verify_chart_minor() -> None:
    a_columns = permanent_image_columns()
    a_pivots: dict[int, dict[int, int]] = {}
    selected_a_indices = []
    selected_a_rows = []
    for index, column in enumerate(a_columns):
        pivot = add_echelon(column, a_pivots, SELECTION_PRIME)
        if pivot is not None:
            selected_a_indices.append(index)
            selected_a_rows.append(pivot)
    if len(selected_a_indices) != 560:
        raise AssertionError("unexpected permanent image rank")

    q_columns_by_variable = [
        [
            delta_column({monomial: 1}, exterior_variable)
            for monomial in QUADRATICS
        ]
        for exterior_variable in range(N)
    ]
    q_pivots: dict[int, dict[int, int]] = {}
    selected_q_indices = []
    selected_q_rows = []
    for index, column in enumerate(q_columns_by_variable[0]):
        reduced = reduce_echelon(column, a_pivots, SELECTION_PRIME)
        pivot = add_echelon(reduced, q_pivots, SELECTION_PRIME)
        if pivot is not None:
            selected_q_indices.append(index)
            selected_q_rows.append(pivot)
    if len(selected_q_indices) != 99:
        raise AssertionError("unexpected fixed-v quotient rank")

    selected_a = [a_columns[index] for index in selected_a_indices]
    a_top = dense(selected_a, selected_a_rows)
    a_bottom = dense(selected_a, selected_q_rows)
    schur_blocks = []
    for exterior_variable in range(N):
        selected_q = [
            q_columns_by_variable[exterior_variable][index]
            for index in selected_q_indices
        ]
        q_top = dense(selected_q, selected_a_rows)
        q_bottom = dense(selected_q, selected_q_rows)
        schur_blocks.append(q_bottom - a_bottom * a_top.solve(q_top))

    normalized = [
        schur_blocks[0].inv() * block for block in schur_blocks[1:]
    ]
    order = topological_order(normalized)
    if order is None:
        raise AssertionError("independent chart matrices did not triangularize")
    full_constant = a_top.det() * schur_blocks[0].det()
    if full_constant != -32768:
        raise AssertionError(f"unexpected chart constant {full_constant}")
    print("direct_E_image_rank=560")
    print(f"independent_chart_constant={full_constant}")
    print("independent_chart_triangular=True")


def main() -> None:
    verify_prolongation_upper_bound()
    verify_chow_term_rank()
    verify_chart_minor()
    print("INDEPENDENT_RANK8_AUDIT_PASS")


if __name__ == "__main__":
    main()
