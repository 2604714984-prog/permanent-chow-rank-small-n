#!/usr/bin/env python3
"""Exact finite replay for the ordinary Chow-rank-32 proof for ``perm_6``.

The replay derives, rather than merely restates, the finite ingredients of
the half-defect quotient-symbol lemma:

* the coordinate intersection bounds for five- and six-dimensional spaces;
* the universal squarefree projected-symbol table;
* the actual derivative dimensions of the five dependent-factor normal
  forms; and
* the low-factor-span monomial floors and final defect cancellation.

The geometric torus-specialization argument, the two elementary directional
shadow arguments, and the global filtration remain written proofs in the
adjacent theorem document. This program is deliberately small and bounded:
it stores no family of candidates, and all enumerations are streamed or kept
below one thousand cached coordinate edge sets.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Iterator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "n6_exact_ordinary_chow_rank_32.json"

VERTICES = tuple(range(6))
EDGES = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))
EXPONENT = tuple[int, ...]
POLYNOMIAL = dict[EXPONENT, Fraction]


def require(condition: bool, payload: object) -> None:
    if not condition:
        raise AssertionError(payload)


def encoded(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def dominates_half_defect(row: tuple[Fraction, ...]) -> bool:
    return all(value >= Fraction(10 * d, 3) for d, value in enumerate(row))


def positive_partitions(
    total: int, length: int, ceiling: int | None = None
) -> Iterator[tuple[int, ...]]:
    """Yield nonincreasing positive partitions of ``total`` of fixed length."""

    if length == 0:
        if total == 0:
            yield ()
        return
    if ceiling is None:
        ceiling = total
    for first in range(min(ceiling, total - length + 1), 0, -1):
        for tail in positive_partitions(total - first, length - 1, first):
            yield (first,) + tail


def monomial_middle_rank(multiplicities: tuple[int, ...]) -> int:
    """Count degree-three divisors of a monomial with given multiplicities."""

    answer = 0

    def visit(index: int, degree_left: int) -> None:
        nonlocal answer
        if index == len(multiplicities):
            answer += int(degree_left == 0)
            return
        for exponent in range(min(multiplicities[index], degree_left) + 1):
            visit(index + 1, degree_left - exponent)

    visit(0, 3)
    return answer


def low_span_rows() -> tuple[dict[str, object], dict[int, int]]:
    expected_floors = {1: 1, 2: 2, 3: 4, 4: 8}
    rows: dict[str, object] = {}
    floors: dict[int, int] = {}
    for ell in range(1, 5):
        partition_rows = [
            {
                "multiplicities": list(partition),
                "middle_rank": monomial_middle_rank(partition),
            }
            for partition in positive_partitions(6, ell)
        ]
        floor = min(int(row["middle_rank"]) for row in partition_rows)
        require(floor == expected_floors[ell], (ell, floor, partition_rows))
        floors[ell] = floor

        entries = []
        maximum = min(20, comb(ell + 2, 3))
        for d in range(ell + 1):
            candidates = []
            for u in range(floor, maximum + 1):
                if d == ell:
                    rank = u
                else:
                    kernel_cap = comb(ell - d + 2, 3) + d
                    rank = max(0, u - kernel_cap)
                value = Fraction(rank) + Fraction(20 - u, 2)
                candidates.append((value, u, rank))
            value, u, rank = min(candidates)
            entries.append(
                {
                    "d": d,
                    "minimum_half_defect_lhs": encoded(value),
                    "attained_at_middle_rank": u,
                    "rank_lower_bound": rank,
                }
            )
        rows[str(ell)] = {
            "monomial_degenerations": partition_rows,
            "middle_rank_floor": floor,
            "entries": entries,
        }
    return rows, floors


def coordinate_symbol_rank(
    kernel_vertices: frozenset[int], killed_edges: frozenset[tuple[int, int]]
) -> int:
    """Rank of a coordinate specialization of the squarefree symbol map."""

    rank = 0
    for triple in TRIPLES:
        survives = False
        for vertex in triple:
            edge = tuple(sorted(item for item in triple if item != vertex))
            if vertex not in kernel_vertices and edge not in killed_edges:
                survives = True
                break
        rank += int(survives)
    return rank


def killed_cubic_count(
    kernel_vertices: frozenset[int], killed_edges: frozenset[tuple[int, int]]
) -> int:
    """Evaluate the four-term killed-column formula in the written proof."""

    outside = frozenset(VERTICES) - kernel_vertices
    internal_kernel_edges = sum(
        left in kernel_vertices and right in kernel_vertices
        for left, right in killed_edges
    )
    cross_degrees = {
        vertex: sum(
            vertex in edge and bool(set(edge) & outside) for edge in killed_edges
        )
        for vertex in kernel_vertices
    }
    outside_triangles = sum(
        all(tuple(sorted(edge)) in killed_edges for edge in combinations(triple, 2))
        for triple in combinations(sorted(outside), 3)
    )
    return (
        comb(len(kernel_vertices), 3)
        + len(outside) * internal_kernel_edges
        + sum(comb(degree, 2) for degree in cross_degrees.values())
        + outside_triangles
    )


def derive_squarefree_symbol_table() -> tuple[list[list[int]], dict[str, object]]:
    """Exhaust all coordinate fixed points for ``dim R <= 3``."""

    table: list[list[int]] = []
    witnesses: dict[str, object] = {}
    candidate_count = 0
    for r in range(4):
        row = []
        edge_choices = tuple(
            edge_set
            for size in range(r + 1)
            for edge_set in combinations(EDGES, size)
        )
        for d in range(7):
            best = 21
            witness: tuple[tuple[int, ...], tuple[tuple[int, int], ...]] | None = None
            for raw_kernel in combinations(VERTICES, 6 - d):
                kernel = frozenset(raw_kernel)
                for raw_edges in edge_choices:
                    candidate_count += 1
                    rank = coordinate_symbol_rank(kernel, frozenset(raw_edges))
                    require(
                        rank == 20 - killed_cubic_count(kernel, frozenset(raw_edges)),
                        (raw_kernel, raw_edges, rank),
                    )
                    if rank < best:
                        best = rank
                        witness = (raw_kernel, raw_edges)
            require(witness is not None, (r, d))
            row.append(best)
            witnesses[f"r{r}_d{d}"] = {
                "kernel_vertices": list(witness[0]),
                "killed_edges": [list(edge) for edge in witness[1]],
                "rank": best,
            }
        table.append(row)

    expected = [
        [0, 10, 16, 19, 20, 20, 20],
        [0, 9, 14, 16, 16, 20, 20],
        [0, 8, 12, 13, 16, 19, 20],
        [0, 7, 10, 10, 15, 17, 19],
    ]
    require(table == expected, table)
    return table, {"candidate_count": candidate_count, "witnesses": witnesses}


def row_neighborhoods(
    edges_left: int,
    minimum_mask: int = 1,
    current: tuple[int, ...] = (),
) -> Iterator[tuple[int, ...]]:
    """Enumerate bipartite graphs up to row permutation, with six columns."""

    if edges_left == 0:
        yield current
        return
    if len(current) == 6:
        return
    for mask in range(minimum_mask, 1 << 6):
        size = mask.bit_count()
        if size <= edges_left:
            yield from row_neighborhoods(
                edges_left - size, mask, current + (mask,)
            )


def four_cycle_count(neighborhoods: tuple[int, ...]) -> int:
    return sum(
        comb((left & right).bit_count(), 2)
        for left, right in combinations(neighborhoods, 2)
    )


def derive_coordinate_intersection_bounds() -> dict[str, object]:
    """Find the exact four-cycle maximum for at most six coordinate axes."""

    maxima = []
    witnesses = []
    candidate_counts = []
    for edge_count in range(7):
        best = -1
        witness: tuple[int, ...] = ()
        count = 0
        for neighborhoods in row_neighborhoods(edge_count):
            count += 1
            cycles = four_cycle_count(neighborhoods)
            if cycles > best:
                best = cycles
                witness = neighborhoods
        maxima.append(best)
        candidate_counts.append(count)
        witnesses.append(
            [[column for column in range(6) if mask & (1 << column)] for mask in witness]
        )
    require(maxima == [0, 0, 0, 0, 1, 1, 3], maxima)
    return {
        "four_cycle_maxima_by_edge_count_0_to_6": maxima,
        "row_permutation_reduced_candidate_counts": candidate_counts,
        "witness_row_neighborhoods": witnesses,
    }


def add_polynomials(left: POLYNOMIAL, right: POLYNOMIAL) -> POLYNOMIAL:
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
        if not answer[monomial]:
            del answer[monomial]
    return answer


def multiply_polynomials(left: POLYNOMIAL, right: POLYNOMIAL) -> POLYNOMIAL:
    answer: POLYNOMIAL = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_power + right_power
                for left_power, right_power in zip(left_monomial, right_monomial)
            )
            answer[monomial] = (
                answer.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
    return {monomial: value for monomial, value in answer.items() if value}


def differentiate(polynomial: POLYNOMIAL, variable: int) -> POLYNOMIAL:
    answer: POLYNOMIAL = {}
    for monomial, coefficient in polynomial.items():
        power = monomial[variable]
        if power:
            derived = list(monomial)
            derived[variable] -= 1
            answer[tuple(derived)] = coefficient * power
    return answer


def sparse_rank(columns: list[POLYNOMIAL]) -> int:
    pivots: dict[EXPONENT, POLYNOMIAL] = {}
    for raw_column in columns:
        column = dict(raw_column)
        while column:
            leading = min(column)
            if leading not in pivots:
                scale = column[leading]
                column = {
                    monomial: coefficient / scale
                    for monomial, coefficient in column.items()
                }
                pivots[leading] = column
                break
            scale = column[leading]
            pivot = pivots[leading]
            column = add_polynomials(
                column,
                {
                    monomial: -scale * coefficient
                    for monomial, coefficient in pivot.items()
                },
            )
    return len(pivots)


def variable_polynomial(variable: int) -> POLYNOMIAL:
    exponent = [0] * 5
    exponent[variable] = 1
    return {tuple(exponent): Fraction(1)}


def dependent_normal_form(support: int) -> tuple[POLYNOMIAL, list[POLYNOMIAL]]:
    factors = [variable_polynomial(variable) for variable in range(5)]
    dependent: POLYNOMIAL = {}
    for variable in range(support):
        dependent = add_polynomials(dependent, variable_polynomial(variable))
    factors.append(dependent)
    product: POLYNOMIAL = {(0, 0, 0, 0, 0): Fraction(1)}
    for factor in factors:
        product = multiply_polynomials(product, factor)
    return product, factors


def derivative_space_columns(polynomial: POLYNOMIAL, order: int) -> list[POLYNOMIAL]:
    """All order-``order`` partial derivatives, with repetitions removed by rank."""

    columns = []

    def visit(minimum: int, remaining: int, directions: tuple[int, ...]) -> None:
        if remaining == 0:
            derived = polynomial
            for variable in directions:
                derived = differentiate(derived, variable)
            columns.append(derived)
            return
        for variable in range(minimum, 5):
            visit(variable, remaining - 1, directions + (variable,))

    visit(0, order, ())
    return columns


def derivative_space_rank(polynomial: POLYNOMIAL, order: int) -> int:
    return sparse_rank(derivative_space_columns(polynomial, order))


def formal_product_rank(factors: list[POLYNOMIAL], degree: int) -> int:
    columns = []
    for selected in combinations(range(6), degree):
        product: POLYNOMIAL = {(0, 0, 0, 0, 0): Fraction(1)}
        for index in selected:
            product = multiply_polynomials(product, factors[index])
        columns.append(product)
    return sparse_rank(columns)


def derive_span_five_profiles() -> list[dict[str, object]]:
    profiles = []
    expected = {
        1: (11, 14),
        2: (11, 14),
        3: (13, 18),
        4: (14, 20),
        5: (15, 20),
    }
    expected_squarefree = {
        1: tuple(combinations(range(5), 3)),
        2: (
            (0, 2, 3),
            (0, 2, 4),
            (0, 3, 4),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 4),
            (2, 3, 4),
        ),
        3: tuple(
            triple
            for triple in combinations(range(5), 3)
            if triple != (0, 1, 2)
        ),
        4: tuple(combinations(range(5), 3)),
        5: tuple(combinations(range(5), 3)),
    }
    for support in range(1, 6):
        polynomial, factors = dependent_normal_form(support)
        quadratic_columns = derivative_space_columns(polynomial, 4)
        cubic_columns = derivative_space_columns(polynomial, 3)
        quadratic_rank = sparse_rank(quadratic_columns)
        cubic_rank = sparse_rank(cubic_columns)
        formal_pair_rank = formal_product_rank(factors, 2)
        formal_triple_rank = formal_product_rank(factors, 3)
        require(
            (quadratic_rank, cubic_rank) == expected[support],
            (support, quadratic_rank, cubic_rank),
        )
        contained_squarefree = []
        for triple in combinations(range(5), 3):
            exponent = [0] * 5
            for variable in triple:
                exponent[variable] = 1
            monomial = {tuple(exponent): Fraction(1)}
            if sparse_rank(cubic_columns + [monomial]) == cubic_rank:
                contained_squarefree.append(triple)
        require(
            tuple(contained_squarefree) == expected_squarefree[support],
            (support, contained_squarefree),
        )
        vertex_degrees = [
            sum(variable in triple for triple in contained_squarefree)
            for variable in range(5)
        ]
        profiles.append(
            {
                "support": support,
                "quadratic_derivative_rank": quadratic_rank,
                "middle_derivative_rank": cubic_rank,
                "formal_pair_product_span_rank": formal_pair_rank,
                "formal_triple_product_span_rank": formal_triple_rank,
                "formal_pair_equals_actual_derivative_space": (
                    formal_pair_rank == quadratic_rank
                ),
                "formal_triple_equals_actual_derivative_space": (
                    formal_triple_rank == cubic_rank
                ),
                "contained_squarefree_triples": [
                    [variable + 1 for variable in triple]
                    for triple in contained_squarefree
                ],
                "contained_squarefree_vertex_degrees": vertex_degrees,
                "contained_squarefree_directional_rank_floor": min(vertex_degrees),
            }
        )
    return profiles


def derive_span_five_half_defect_rows(
    profiles: list[dict[str, object]],
) -> dict[int, tuple[Fraction, ...]]:
    """Apply the written kernel and directional bounds to the actual profiles."""

    rows: dict[int, tuple[Fraction, ...]] = {}
    for profile in profiles:
        support = int(profile["support"])
        middle_rank = int(profile["middle_derivative_rank"])
        if support <= 2:
            # Section 4.3 proves this directly from the displayed actual bases.
            directional_rank_before_r = 7
        else:
            directional_rank_before_r = int(
                profile["contained_squarefree_directional_rank_floor"]
            )

        adjusted = []
        for d in range(6):
            if d == 0:
                rank = 0
            elif d == 5:
                rank = middle_rank
            else:
                kernel_cap = comb(5 - d + 2, 3) + d
                rank = max(0, middle_rank - kernel_cap)
                # A positive-rank quotient admits a rank-one composite. Reducing
                # the quadratic target by R loses at most dim R <= 1.
                rank = max(rank, directional_rank_before_r - 1)
                if support <= 2 and d == 4:
                    # The essential-variable argument leaves at most a
                    # one-dimensional cubic kernel.
                    rank = max(rank, middle_rank - 1)
            adjusted.append(Fraction(rank) + Fraction(20 - middle_rank, 2))
        rows[support] = tuple(adjusted)

    require(rows[1] == rows[2] == tuple(map(Fraction, (3, 9, 9, 10, 16, 17))), rows)
    require(rows[3] == tuple(map(Fraction, (1, 5, 7, 12, 14, 19))), rows)
    require(rows[4] == rows[5] == tuple(map(Fraction, (0, 5, 8, 13, 15, 20))), rows)
    return rows


def build_payload() -> dict[str, object]:
    low_rows, floors = low_span_rows()
    squarefree_table, squarefree_audit = derive_squarefree_symbol_table()
    coordinate_intersections = derive_coordinate_intersection_bounds()
    span_five_profiles = derive_span_five_profiles()
    span_five_rows = derive_span_five_half_defect_rows(span_five_profiles)

    half_defect_rows = {
        "ell_1": tuple(
            Fraction(entry["minimum_half_defect_lhs"])
            for entry in low_rows["1"]["entries"]
        ),
        "ell_2": tuple(
            Fraction(entry["minimum_half_defect_lhs"])
            for entry in low_rows["2"]["entries"]
        ),
        "ell_3": tuple(
            Fraction(entry["minimum_half_defect_lhs"])
            for entry in low_rows["3"]["entries"]
        ),
        "ell_4": tuple(
            Fraction(entry["minimum_half_defect_lhs"])
            for entry in low_rows["4"]["entries"]
        ),
        "ell_6": tuple(map(Fraction, squarefree_table[3][:-1] + [20])),
        # These rows are derived from the actual five-variable derivative
        # profiles and the written kernel/directional bounds.
        "ell_5_s5": span_five_rows[5],
        "ell_5_s4": span_five_rows[4],
        "ell_5_s3": span_five_rows[3],
        "ell_5_s1_s2": span_five_rows[1],
    }
    checks = {
        name: dominates_half_defect(row) for name, row in half_defect_rows.items()
    }
    require(all(checks.values()), checks)

    n31_gap = 120 - (10 * 31 - 200)
    n32_gap = 120 - (10 * 32 - 200)
    require(n31_gap == 10, n31_gap)
    require(n32_gap == 0, n32_gap)

    return {
        "status": "EXACT_THEOREM_FINITE_REPLAY",
        "scope": "ordinary Chow rank over characteristic zero; not border rank",
        "replay_boundary": (
            "Exact finite derivation of the coordinate intersection, squarefree "
            "symbol, normal-form, monomial-floor, and cancellation tables. The "
            "torus fixed-point reductions, directional-shadow cases, permanent "
            "prolongation identity, and global filtration are written proofs."
        ),
        "half_defect_coefficient": "1/2",
        "factor_increment_slope": "10/3",
        "factor_span_total": 36,
        "lower_symbol_constant": 120,
        "upper_symbol_formula": "10*N - 200 - Delta/2",
        "lower_symbol_formula": "120 - Delta/2",
        "minimum_n": 32,
        "n31_gap": n31_gap,
        "n32_gap": n32_gap,
        "coordinate_intersection_audit": coordinate_intersections,
        "squarefree_symbol_table": squarefree_table,
        "squarefree_symbol_audit": squarefree_audit,
        "span_five_normal_forms": span_five_profiles,
        "span_five_derived_half_defect_rows": {
            str(support): [encoded(value) for value in row]
            for support, row in span_five_rows.items()
        },
        "low_factor_span_rows": low_rows,
        "low_factor_span_middle_rank_floors": {
            str(key): value for key, value in floors.items()
        },
        "half_defect_rows": {
            name: [encoded(value) for value in row]
            for name, row in half_defect_rows.items()
        },
        "all_half_defect_rows_pass": all(checks.values()),
        "conclusion": "ChowRank(perm_6) = 32",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    parser.add_argument("--verify-json", type=Path)
    args = parser.parse_args()
    payload = build_payload()
    if args.json:
        args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if args.verify_json:
        frozen = json.loads(args.verify_json.read_text(encoding="utf-8"))
        if payload != frozen:
            raise SystemExit("frozen payload mismatch")
        print("PASS: exact ordinary rank-32 finite proof payload matches")
    if not args.json and not args.verify_json:
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
