"""Build the exact local-weight model for coordinate relative prolongations.

For a coordinate weight set W in Q=Sym^2(V)/E_5, the relative first
prolongation decomposes over cubic row/column torus weights.  Each local
block involves only a small subset of the 225 quadratic quotient weights.
This script enumerates the local block functions exactly over F_3 and emits
a compact truth-table model for later exact optimization.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations_with_replacement
from pathlib import Path

from perm5_coordinate_d3_orbit_scan import (
    CLASSES,
    CLASS_INDEX,
    representative_monomial,
)


PRIME = 3
OUTPUT = Path(__file__).with_name(
    "n5_coordinate_prolongation_hypergraph_F3_exact.json"
)


def torus_weight(monomial: tuple[int, ...]) -> tuple[int, ...]:
    rows = [0] * 5
    columns = [0] * 5
    for variable in monomial:
        row, column = divmod(variable, 5)
        rows[row] += 1
        columns[column] += 1
    return tuple(rows + columns)


def quadratic_class(monomial: tuple[int, int]) -> tuple[int, int]:
    first, second = sorted(monomial)
    r1, c1 = divmod(first, 5)
    r2, c2 = divmod(second, 5)
    if first == second:
        descriptor = ("S", r1, c1)
        return CLASS_INDEX[descriptor], 1
    if r1 == r2:
        descriptor = ("R", r1, min(c1, c2), max(c1, c2))
        return CLASS_INDEX[descriptor], 1
    if c1 == c2:
        descriptor = ("C", min(r1, r2), max(r1, r2), c1)
        return CLASS_INDEX[descriptor], 1
    descriptor = (
        "X", min(r1, r2), max(r1, r2), min(c1, c2), max(c1, c2)
    )
    index = CLASS_INDEX[descriptor]
    representative = representative_monomial(descriptor)
    sign = 1 if (first, second) == representative else -1
    return index, sign % PRIME


def rank_mod3(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    matrix = [row[:] for row in rows if any(row)]
    rank = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next(
            (i for i in range(rank, len(matrix)) if matrix[i][column] % 3),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = 1 if matrix[rank][column] % 3 == 1 else 2
        matrix[rank] = [(inverse * value) % 3 for value in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank or not matrix[i][column] % 3:
                continue
            factor = matrix[i][column] % 3
            matrix[i] = [
                (a - factor * b) % 3
                for a, b in zip(matrix[i], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def main() -> None:
    cubic_groups: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for monomial in combinations_with_replacement(range(25), 3):
        cubic_groups[torus_weight(monomial)].append(monomial)

    local_blocks = []
    involved_histogram = Counter()
    truth_table_size = 0
    for weight, monomials in sorted(cubic_groups.items()):
        row_coefficients: dict[tuple[int, int], list[int]] = {}
        involved = set()
        for column, monomial in enumerate(monomials):
            # Use divided-power polarization coordinates.  The Koszul
            # kernel computed by the exact flattening is characteristic
            # independent in these coordinates; ordinary polynomial
            # derivative multiplicities would introduce spurious
            # Frobenius kernels in characteristic three.
            for variable in set(monomial):
                remaining = list(monomial)
                remaining.remove(variable)
                q_index, q_sign = quadratic_class(tuple(remaining))
                involved.add(q_index)
                row = row_coefficients.setdefault(
                    (variable, q_index), [0] * len(monomials)
                )
                row[column] = (
                    row[column] + q_sign
                ) % PRIME

        involved = sorted(involved)
        involved_histogram[len(involved)] += 1
        full_rows = list(row_coefficients.values())
        base_kernel = len(monomials) - rank_mod3(full_rows)
        table = {}
        for mask in range(1 << len(involved)):
            allowed = {
                involved[position]
                for position in range(len(involved))
                if mask >> position & 1
            }
            constrained_rows = [
                row for (variable, q_index), row in row_coefficients.items()
                if q_index not in allowed
            ]
            kernel = len(monomials) - rank_mod3(constrained_rows)
            relative = kernel - base_kernel
            if relative:
                table[str(mask)] = relative
        truth_table_size += len(table)
        if table:
            local_blocks.append(
                {
                    "cubic_weight": list(weight),
                    "cubic_monomial_count": len(monomials),
                    "base_kernel_dimension": base_kernel,
                    "involved_quadratic_weights": involved,
                    "nonzero_relative_truth_table": table,
                }
            )

    # Exact calibration on the known extremal coordinate sets.
    def evaluate(selected: set[int]) -> int:
        total = 0
        for block in local_blocks:
            mask = 0
            for position, index in enumerate(
                block["involved_quadratic_weights"]
            ):
                if index in selected:
                    mask |= 1 << position
            total += block["nonzero_relative_truth_table"].get(str(mask), 0)
        return total

    calibrations = {
        "d4_extremal": {
            "set": [0, 25, 26, 29],
            "relative_prolongation": 8,
        },
        "d5_extremal": {
            "set": [0, 1, 25, 26, 29],
            "relative_prolongation": 11,
        },
        "d6_structured": {
            "set": [0, 1, 2, 25, 26, 29],
            "relative_prolongation": 14,
        },
    }
    for calibration in calibrations.values():
        actual = evaluate(set(calibration["set"]))
        assert actual == calibration["relative_prolongation"], (
            calibration,
            actual,
        )

    result = {
        "claim_type": (
            "exact exhaustive F3 local torus-weight truth tables for "
            "coordinate relative first prolongation"
        ),
        "prime": PRIME,
        "cubic_monomials": 2925,
        "cubic_weight_spaces": len(cubic_groups),
        "quadratic_quotient_weights": len(CLASSES),
        "involved_weight_count_histogram": {
            str(key): value for key, value in sorted(involved_histogram.items())
        },
        "nonzero_local_blocks": len(local_blocks),
        "nonzero_truth_table_entries": truth_table_size,
        "calibrations": calibrations,
        "local_blocks": local_blocks,
        "status": "PASS",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key != "local_blocks"
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
