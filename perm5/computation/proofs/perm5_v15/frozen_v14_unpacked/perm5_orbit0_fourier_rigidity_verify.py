#!/usr/bin/env python3
"""Independent exact check for the pure orbit-0 Fourier rigidity lemma.

This script is diagnostic only.  The proof is in
``n5_orbit0_fourier_rigidity_pure_20260810.md`` and does not depend on this
enumeration.  All ranks below use exact rational Gaussian elimination.
"""

from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


OMEGA = [(1,) + z for z in product((-1, 1), repeat=4)]


def rank_q(columns):
    if not columns:
        return 0
    rows = len(columns[0])
    matrix = [
        [Fraction(columns[j][i]) for j in range(len(columns))]
        for i in range(rows)
    ]
    rank = 0
    for col in range(len(columns)):
        pivot = next(
            (i for i in range(rank, rows) if matrix[i][col] != 0), None
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][col]
        matrix[rank] = [x / value for x in matrix[rank]]
        for i in range(rows):
            if i == rank or matrix[i][col] == 0:
                continue
            value = matrix[i][col]
            matrix[i] = [
                x - value * y for x, y in zip(matrix[i], matrix[rank])
            ]
        rank += 1
    return rank


def nullspace_q(columns):
    """Right nullspace of a matrix specified by columns."""
    if not columns:
        return []
    rows = len(columns[0])
    cols = len(columns)
    matrix = [
        [Fraction(columns[j][i]) for j in range(cols)]
        for i in range(rows)
    ]
    pivot_columns = []
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (i for i in range(pivot_row, rows) if matrix[i][col] != 0),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        value = matrix[pivot_row][col]
        matrix[pivot_row] = [x / value for x in matrix[pivot_row]]
        for i in range(rows):
            if i == pivot_row or matrix[i][col] == 0:
                continue
            value = matrix[i][col]
            matrix[i] = [
                x - value * y
                for x, y in zip(matrix[i], matrix[pivot_row])
            ]
        pivot_columns.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    free_columns = [i for i in range(cols) if i not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(cols)]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -matrix[row][free]
        basis.append(vector)
    return basis


def character(z, subset):
    value = 1
    for i in subset:
        value *= z[i + 1]
    return value


SUBSETS_LE2 = [
    subset
    for size in range(3)
    for subset in combinations(range(4), size)
]
SUBSETS_LE3 = [
    subset
    for size in range(4)
    for subset in combinations(range(4), size)
]


def fourier_catalecticant_rank(weights):
    # Rows are cubic characters and columns are quadratic characters.
    columns = []
    for b in SUBSETS_LE2:
        column = []
        for a in SUBSETS_LE3:
            total = 0
            for z, h in zip(OMEGA, weights):
                total += (
                    character(z, (0, 1, 2, 3))
                    * h
                    * character(z, a)
                    * character(z, b)
                )
            column.append(total)
        columns.append(tuple(column))
    return rank_q(columns)


rank_four_sixes = []
proper_shortening_max = 0
standard_rank_histogram = {}
predicted_r4_dimension_histogram = {}
baseline_rank = fourier_catalecticant_rank([1] * 16)

for labels in combinations(range(16), 6):
    columns = [OMEGA[i] for i in labels]
    if rank_q(columns) != 4:
        continue
    rank_four_sixes.append(labels)

    full_nullity = 6 - rank_q(columns)
    assert full_nullity == 2
    for size in range(6):
        for subset in combinations(labels, size):
            nullity = size - rank_q([OMEGA[i] for i in subset])
            proper_shortening_max = max(proper_shortening_max, nullity)
            assert nullity <= 1

    weights = [1] * 16
    for i in labels:
        weights[i] = 0
    rank = fourier_catalecticant_rank(weights)
    standard_rank_histogram[rank] = standard_rank_histogram.get(rank, 0) + 1
    assert rank == 9

    complement = [i for i in range(16) if i not in labels]
    square_columns = [
        tuple(character(OMEGA[i], subset) for subset in SUBSETS_LE2)
        for i in complement
    ]
    relation_basis = nullspace_q(square_columns)
    assert len(relation_basis) == 1
    support = [
        complement[j]
        for j, value in enumerate(relation_basis[0])
        if value != 0
    ]
    support_rank = rank_q([OMEGA[i] for i in support])
    assert support_rank >= 3
    predicted_r4_dimension = 10 - support_rank
    assert predicted_r4_dimension <= 7
    predicted_r4_dimension_histogram[predicted_r4_dimension] = (
        predicted_r4_dimension_histogram.get(predicted_r4_dimension, 0) + 1
    )

assert baseline_rank == 10
assert len(rank_four_sixes) == 600

payload = {
    "status": "PASS_EXACT_QQ_FOURIER_RIGIDITY_DIAGNOSTIC",
    "evidence_role": "independent diagnostic; not used by the pure proof",
    "field": "QQ",
    "omega_size": 16,
    "rm_le2_dimension": len(SUBSETS_LE2),
    "rm_le3_dimension": len(SUBSETS_LE3),
    "baseline_permanent_catalecticant_rank": baseline_rank,
    "rank_four_six_subsets": len(rank_four_sixes),
    "maximum_proper_shortening_nullity": proper_shortening_max,
    "standard_point_rank_histogram": standard_rank_histogram,
    "predicted_R4_dimension_histogram": predicted_r4_dimension_histogram,
    "pure_universal_R4_upper_bound": 7,
    "pure_global_K1_lower_bound": 25 * 90 - 5 * 7,
    "nine_chow_term_K1_upper_bound": 9 * 245,
}

assert payload["pure_global_K1_lower_bound"] > payload["nine_chow_term_K1_upper_bound"]

output = Path("n5_orbit0_fourier_rigidity_verify_exact.json")
output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(payload, sort_keys=True))
print("output", output)
