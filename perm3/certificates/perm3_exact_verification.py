"""Independent exact verification for the 3 by 3 permanent Chow rank.

The program is self-contained. All matrix ranks are computed over the prime
field F_p. A rank r over F_p proves that the corresponding integer matrix has
an r by r minor not divisible by p. Upper bounds used below come from the
explicit prolongation bases described in the accompanying report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb
from pathlib import Path


PRIME = 1_000_003


def add_column(
    source: dict[int, int],
    pivots: dict[int, dict[int, int]],
    prime: int,
) -> int | None:
    column = {r: v % prime for r, v in source.items() if v % prime}
    while column:
        pivot = min(column)
        value = column[pivot]
        basis = pivots.get(pivot)
        if basis is None:
            inverse = pow(value, prime - 2, prime)
            normalized = {r: v * inverse % prime for r, v in column.items()}
            pivots[pivot] = normalized
            return pivot
        for row, coefficient in basis.items():
            updated = (column.get(row, 0) - value * coefficient) % prime
            if updated:
                column[row] = updated
            else:
                column.pop(row, None)
    return None


def reduce_column(
    source: dict[int, int],
    pivots: dict[int, dict[int, int]],
    prime: int,
) -> dict[int, int]:
    column = {r: v % prime for r, v in source.items() if v % prime}
    for pivot in sorted(pivots):
        value = column.get(pivot, 0)
        if not value:
            continue
        basis = pivots[pivot]
        for row, coefficient in basis.items():
            updated = (column.get(row, 0) - value * coefficient) % prime
            if updated:
                column[row] = updated
            else:
                column.pop(row, None)
    return column


def wedge(a: int, b: int) -> tuple[int, tuple[int, int] | None]:
    if a == b:
        return 0, None
    return (1, (a, b)) if a < b else (-1, (b, a))


class KoszulData:
    def __init__(self, n: int):
        self.n = n
        self.N = n * n
        self.wedges = list(combinations(range(self.N), 2))
        self.wedge_index = {w: i for i, w in enumerate(self.wedges)}
        self.row_count = self.N * len(self.wedges)

    def delta(
        self,
        quadratic: dict[tuple[int, int], int],
        exterior: dict[int, int],
    ) -> dict[int, int]:
        result: dict[int, int] = {}
        for monomial, qcoefficient in quadratic.items():
            a, b = monomial
            entries = ((a, b), (b, a))
            for differentiated, remaining in entries:
                for v, vcoefficient in exterior.items():
                    sign, pair = wedge(differentiated, v)
                    if sign:
                        row = remaining * len(self.wedges) + self.wedge_index[pair]
                        result[row] = (
                            result.get(row, 0)
                            + sign * qcoefficient * vcoefficient
                        )
        return {r: v for r, v in result.items() if v}

    def permanent_quadrics(self) -> list[dict[tuple[int, int], int]]:
        result = []
        for rows in combinations(range(self.n), 2):
            for columns in combinations(range(self.n), 2):
                i, j = rows
                a, b = columns
                result.append(
                    {
                        tuple(sorted((self.n * i + a, self.n * j + b))): 1,
                        tuple(sorted((self.n * i + b, self.n * j + a))): 1,
                    }
                )
        return result

    def chow_quadrics(self) -> list[dict[tuple[int, int], int]]:
        # Coordinate model for n independent factors.
        return [{(i, j): 1} for i, j in combinations(range(self.n), 2)]

    def image_pivots(
        self,
        quadrics: list[dict[tuple[int, int], int]],
        prime: int,
    ) -> tuple[dict[int, dict[int, int]], list[tuple[int, int]]]:
        pivots: dict[int, dict[int, int]] = {}
        witnesses = []
        for q_index, quadratic in enumerate(quadrics):
            for variable in range(self.N):
                column = self.delta(quadratic, {variable: 1})
                pivot = add_column(column, pivots, prime)
                if pivot is not None:
                    witnesses.append((q_index * self.N + variable, pivot))
        return pivots, witnesses

    def psi_rank(
        self,
        base_pivots: dict[int, dict[int, int]],
        vector: dict[int, int],
        prime: int,
    ) -> tuple[int, list[tuple[int, int]]]:
        quotient_pivots: dict[int, dict[int, int]] = {}
        witnesses = []
        for q_index, pair in enumerate(
            combinations_with_replacement(range(self.N), 2)
        ):
            reduced = reduce_column(
                self.delta({pair: 1}, vector), base_pivots, prime
            )
            reduced = reduce_column(reduced, quotient_pivots, prime)
            pivot = add_column(reduced, quotient_pivots, prime)
            if pivot is not None:
                witnesses.append((q_index, pivot))
        return len(quotient_pivots), witnesses


def glynn_coefficients(n: int) -> dict[tuple[int, ...], int]:
    """Return coefficients after multiplying Glynn's identity by 2^(n-1)."""
    coefficients: dict[tuple[int, ...], int] = {}
    for tail in product((-1, 1), repeat=n - 1):
        delta = (1,) + tail
        outer = 1
        for value in delta:
            outer *= value
        for row_choice in product(range(n), repeat=n):
            coefficient = outer
            for row in row_choice:
                coefficient *= delta[row]
            monomial = tuple(sorted(n * row_choice[column] + column for column in range(n)))
            coefficients[monomial] = coefficients.get(monomial, 0) + coefficient
    return {m: c for m, c in coefficients.items() if c}


def verify_glynn(n: int) -> dict[str, int]:
    coefficients = glynn_coefficients(n)
    expected = {
        tuple(sorted(n * row + sigma[row] for row in range(n))): 2 ** (n - 1)
        for sigma in permutations(range(n))
    }
    if coefficients != expected:
        raise AssertionError(f"Glynn identity failed for n={n}")
    return {
        "term_count": 2 ** (n - 1),
        "nonzero_monomials": len(coefficients),
        "scaled_coefficient": 2 ** (n - 1),
    }


def witness_digest(witnesses: list[tuple[int, int]]) -> str:
    payload = json.dumps(witnesses, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def run(n: int, psi: bool) -> dict:
    data = KoszulData(n)
    permanent_quadrics = data.permanent_quadrics()
    chow_quadrics = data.chow_quadrics()

    base_pivots, base_witnesses = data.image_pivots(permanent_quadrics, PRIME)
    chow_pivots, chow_witnesses = data.image_pivots(chow_quadrics, PRIME)

    expected_E_dim = comb(n, 2) ** 2
    expected_prolongation = comb(n, 3) ** 2
    expected_base_rank = n * n * expected_E_dim - expected_prolongation
    expected_chow_rank = n * n * comb(n, 2) - comb(n, 3)
    if len(base_pivots) != expected_base_rank:
        raise AssertionError((n, "base", len(base_pivots), expected_base_rank))
    if len(chow_pivots) != expected_chow_rank:
        raise AssertionError((n, "chow", len(chow_pivots), expected_chow_rank))

    result = {
        "n": n,
        "prime": PRIME,
        "ambient_variables": data.N,
        "C_nminus2_2_rank": expected_E_dim,
        "E_dimension": expected_E_dim,
        "E_first_prolongation_dimension": expected_prolongation,
        "base_koszul_rank_mod_p": len(base_pivots),
        "base_rank_formula_upper_bound": expected_base_rank,
        "base_minor_witness_count": len(base_witnesses),
        "base_minor_witness_sha256": witness_digest(base_witnesses),
        "independent_chow_E_dimension": comb(n, 2),
        "independent_chow_prolongation_dimension": comb(n, 3),
        "independent_chow_koszul_rank_mod_p": len(chow_pivots),
        "independent_chow_rank_formula_upper_bound": expected_chow_rank,
        "chow_minor_witness_count": len(chow_witnesses),
        "chow_minor_witness_sha256": witness_digest(chow_witnesses),
        "basic_flattening_lower_bound": (
            len(base_pivots) + expected_chow_rank - 1
        )
        // expected_chow_rank,
        "glynn": verify_glynn(n),
    }

    if psi:
        coordinate_rank, coordinate_witnesses = data.psi_rank(
            base_pivots, {0: 1}, PRIME
        )
        deterministic_vector = {
            index: (index * index + 3 * index + 1) % PRIME
            for index in range(data.N)
        }
        random_rank, random_witnesses = data.psi_rank(
            base_pivots, deterministic_vector, PRIME
        )
        theoretical_max = comb(data.N + 1, 2) - expected_E_dim - 1
        result["psi"] = {
            "source_dimension": comb(data.N + 1, 2) - expected_E_dim,
            "theoretical_max_from_v_square_kernel": theoretical_max,
            "coordinate_v_rank_mod_p": coordinate_rank,
            "coordinate_witness_sha256": witness_digest(coordinate_witnesses),
            "deterministic_dense_v_rank_mod_p": random_rank,
            "deterministic_dense_witness_sha256": witness_digest(random_witnesses),
            "dense_vector_rule": "v_i=i^2+3i+1 mod p",
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(3, True)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
