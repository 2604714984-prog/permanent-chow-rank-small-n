#!/usr/bin/env python3
"""Definition-level exact expansion of Glynn's 16-term formula for perm_5.

The implementation uses only integer coefficient accumulation.  It does not
import a project decomposition generator or read a frozen result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from pathlib import Path


N = 5


def require_equal(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise RuntimeError(
            f"{label} mismatch: expected {expected!r}, observed {actual!r}"
        )


def build_certificate() -> dict[str, object]:
    numerator_coefficients = {columns: 0 for columns in product(range(N), repeat=N)}
    signs = [(1, *tail) for tail in product((-1, 1), repeat=N - 1)]
    require_equal("normalized sign terms", len(signs), 16)

    column_choices = 0
    for delta in signs:
        outer_sign = product_value(delta)
        for columns in product(range(N), repeat=N):
            coefficient = outer_sign
            for column in columns:
                coefficient *= delta[column]
            numerator_coefficients[columns] += coefficient
            column_choices += 1

    require_equal("expanded column choices", column_choices, 50_000)
    require_equal("row-choice monomials", len(numerator_coefficients), 3_125)
    permutation_coefficients = {
        columns: value // 16
        for columns, value in numerator_coefficients.items()
        if len(set(columns)) == N
    }
    nonpermutation_coefficients = {
        columns: value // 16
        for columns, value in numerator_coefficients.items()
        if len(set(columns)) != N
    }
    require_equal("permutation monomials", len(permutation_coefficients), 120)
    require_equal("nonpermutation monomials", len(nonpermutation_coefficients), 3_005)
    require_equal("permutation coefficient set", set(permutation_coefficients.values()), {1})
    require_equal(
        "nonpermutation coefficient set",
        set(nonpermutation_coefficients.values()),
        {0},
    )

    support_text = "\n".join(
        ",".join(map(str, columns))
        for columns in sorted(permutation_coefficients)
    ) + "\n"
    return {
        "status": "PASS",
        "claim_type": "independent exact expansion of the Glynn upper bound",
        "imports_project_generator": False,
        "reads_frozen_result": False,
        "normalized_sign_terms": len(signs),
        "expanded_column_choices": column_choices,
        "row_choice_monomials": len(numerator_coefficients),
        "permutation_monomials": len(permutation_coefficients),
        "permutation_coefficient": 1,
        "nonpermutation_monomials": len(nonpermutation_coefficients),
        "nonpermutation_coefficient": 0,
        "permutation_support_sha256": hashlib.sha256(
            support_text.encode("ascii")
        ).hexdigest().upper(),
        "conclusion": "ChowRank(perm_5) <= 16 over characteristic zero.",
    }


def product_value(values: tuple[int, ...]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
    print("PERM5_GLYNN_UPPER_BOUND_INDEPENDENT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
