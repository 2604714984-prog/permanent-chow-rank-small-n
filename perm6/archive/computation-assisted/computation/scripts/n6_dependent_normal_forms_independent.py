#!/usr/bin/env python3
"""Independent exact derivative verification for the five dependent-factor perm_6 normal forms.

The program intentionally imports no project module and reads no frozen JSON.
It expands

    T_s = x1*x2*x3*x4*x5*(x1+...+x_s),  1 <= s <= 5,

in a sparse rational representation, constructs every third and fourth partial
derivative, and computes exact ranks by sparse Gaussian elimination over QQ.
It also records the formal pair/triple-product spans, including the negative
regression cases that motivated the repaired proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
from pathlib import Path
from typing import Iterable

NVAR = 5
Exponent = tuple[int, ...]
Polynomial = dict[Exponent, Fraction]


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        if not result[monomial]:
            del result[monomial]
    return result


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            result[monomial] = result.get(monomial, Fraction(0)) + lc * rc
    return {m: c for m, c in result.items() if c}


def variable(index: int) -> Polynomial:
    exponent = [0] * NVAR
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def differentiate(poly: Polynomial, index: int) -> Polynomial:
    result: Polynomial = {}
    for monomial, coefficient in poly.items():
        power = monomial[index]
        if power:
            derived = list(monomial)
            derived[index] -= 1
            result[tuple(derived)] = coefficient * power
    return result


def derivative(poly: Polynomial, indices: Iterable[int]) -> Polynomial:
    result = poly
    for index in indices:
        result = differentiate(result, index)
    return result


def exact_rank(columns: list[Polynomial]) -> int:
    pivots: dict[Exponent, Polynomial] = {}
    for raw in columns:
        column = dict(raw)
        while column:
            lead = min(column)
            if lead not in pivots:
                scale = column[lead]
                pivots[lead] = {m: c / scale for m, c in column.items()}
                break
            scale = column[lead]
            pivot = pivots[lead]
            column = add(column, {m: -scale * c for m, c in pivot.items()})
    return len(pivots)


def all_derivatives(poly: Polynomial, order: int) -> list[Polynomial]:
    return [
        derivative(poly, directions)
        for directions in combinations_with_replacement(range(NVAR), order)
    ]


def product_of(factors: list[Polynomial], indices: Iterable[int]) -> Polynomial:
    result: Polynomial = {(0,) * NVAR: Fraction(1)}
    for index in indices:
        result = multiply(result, factors[index])
    return result


def normal_form(support: int) -> tuple[Polynomial, list[Polynomial]]:
    factors = [variable(i) for i in range(NVAR)]
    dependent: Polynomial = {}
    for i in range(support):
        dependent = add(dependent, variable(i))
    factors.append(dependent)
    return product_of(factors, range(6)), factors


def profile(support: int) -> dict[str, object]:
    poly, factors = normal_form(support)
    actual_quadratic = exact_rank(all_derivatives(poly, 4))
    actual_cubic = exact_rank(all_derivatives(poly, 3))
    formal_pairs = exact_rank(
        [product_of(factors, subset) for subset in combinations(range(6), 2)]
    )
    formal_triples = exact_rank(
        [product_of(factors, subset) for subset in combinations(range(6), 3)]
    )
    return {
        "s": support,
        "normal_form": f"x1*x2*x3*x4*x5*(x1+...+x{support})",
        "actual_D2_dimension": actual_quadratic,
        "actual_D3_dimension": actual_cubic,
        "formal_pair_product_span_dimension": formal_pairs,
        "formal_triple_product_span_dimension": formal_triples,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    profiles = [profile(support) for support in range(1, 6)]
    actual = [
        (row["actual_D2_dimension"], row["actual_D3_dimension"])
        for row in profiles
    ]
    expected = [(11, 14), (11, 14), (13, 18), (14, 20), (15, 20)]
    if actual != expected:
        raise RuntimeError(("actual derivative profile mismatch", actual))

    expected_formal = [(11, 14), (12, 17), (13, 19), (14, 20), (15, 20)]
    formal = [
        (
            row["formal_pair_product_span_dimension"],
            row["formal_triple_product_span_dimension"],
        )
        for row in profiles
    ]
    if formal != expected_formal:
        raise RuntimeError(("formal span regression mismatch", formal))

    payload = {
        "status": "PASS",
        "claim_type": "independent exact QQ derivative verification",
        "imports_primary_module": False,
        "reads_frozen_json": False,
        "arithmetic": "fractions.Fraction; sparse exact Gaussian elimination",
        "profiles": profiles,
        "actual_dimension_pairs": [list(pair) for pair in actual],
        "negative_regressions": {
            "T2_formal_pair_vs_actual_D2": [12, 11],
            "T2_formal_triple_vs_actual_D3": [17, 14],
            "T3_formal_triple_vs_actual_D3": [19, 18],
        },
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "actual_dimension_pairs": payload["actual_dimension_pairs"],
        "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest().upper(),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
