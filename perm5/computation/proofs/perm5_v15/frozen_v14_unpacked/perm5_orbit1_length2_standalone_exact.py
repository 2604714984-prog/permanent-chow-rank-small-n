"""Standalone exact-QQ verification of the orbit--1 length-two fibre.

The script uses only the defining rectangle relation of

    Q = Sym^2(A tensor B) / E_5,

namely q(x_ia x_jb) = -q(x_ib x_ja) for i != j and a != b.
No project module, finite field, random sample, or precomputed table is used.

For

    M = <x00,x01,x02,x03>,
    y = x10 + B*x11 + C*x20 + D*x21,
    L = M + <y>,

and

    W0 = <S00,S01,S02,R0;01,R0;02,R0;03,
          R0;12,R0;13,R0;23,C01;0>,

the condition W0 subset q(Sym^2 L) reduces to asking whether C01;0 has a
preimage.  Exact lexicographic elimination gives (B^2,C,D), so the local
fibre is Spec QQ[B]/(B^2), of length two.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from sympy import Poly, groebner, symbols


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_orbit1_length2_standalone_exact.json"


Cell = tuple[int, int]
Descriptor = tuple[object, ...]


def quotient_class(first: Cell, second: Cell) -> tuple[Descriptor, int]:
    """Return a canonical quotient-weight descriptor and its sign over QQ."""

    (i, a), (j, b) = sorted((first, second))
    if (i, a) == (j, b):
        return ("S", i, a), 1
    if i == j:
        return ("R", i, min(a, b), max(a, b)), 1
    if a == b:
        return ("C", min(i, j), max(i, j), a), 1

    low_row, high_row = min(i, j), max(i, j)
    low_col, high_col = min(a, b), max(a, b)
    descriptor = ("X", low_row, high_row, low_col, high_col)
    main_diagonal = {(low_row, low_col), (high_row, high_col)}
    sign = 1 if {(i, a), (j, b)} == main_diagonal else -1
    return descriptor, sign


def add_term(
    vector: dict[Descriptor, object],
    descriptor: Descriptor,
    coefficient: object,
) -> None:
    value = vector.get(descriptor, 0) + coefficient
    if value:
        vector[descriptor] = value
    else:
        vector.pop(descriptor, None)


def product_vector(
    first_terms: tuple[tuple[Cell, object], ...],
    second_terms: tuple[tuple[Cell, object], ...],
) -> dict[Descriptor, object]:
    vector: dict[Descriptor, object] = {}
    for first, first_coefficient in first_terms:
        for second, second_coefficient in second_terms:
            descriptor, sign = quotient_class(first, second)
            add_term(
                vector,
                descriptor,
                sign * first_coefficient * second_coefficient,
            )
    return vector


def descriptor_text(descriptor: Descriptor) -> str:
    return "_".join(str(entry) for entry in descriptor)


def main() -> None:
    B, C, D = symbols("B C D")
    coefficient_symbols = symbols("c0:15")

    m_cells = tuple((0, column) for column in range(4))
    y_terms = (
        ((1, 0), 1),
        ((1, 1), B),
        ((2, 0), C),
        ((2, 1), D),
    )

    vectors: list[dict[Descriptor, object]] = []
    basis_names: list[str] = []

    for first_index, first in enumerate(m_cells):
        for second in m_cells[first_index:]:
            vectors.append(product_vector(((first, 1),), ((second, 1),)))
            basis_names.append(
                f"x{first[0]}{first[1]}*x{second[0]}{second[1]}"
            )

    for first in m_cells:
        vectors.append(product_vector(((first, 1),), y_terms))
        basis_names.append(f"x{first[0]}{first[1]}*y")

    vectors.append(product_vector(y_terms, y_terms))
    basis_names.append("y^2")
    assert len(vectors) == len(basis_names) == 15

    origin_pivots: list[Descriptor] = []
    for vector in vectors:
        nonzero_at_origin = []
        for descriptor, coefficient in vector.items():
            value = Poly(coefficient, B, C, D).eval({B: 0, C: 0, D: 0})
            if value:
                nonzero_at_origin.append((descriptor, value))
        assert len(nonzero_at_origin) == 1
        descriptor, value = nonzero_at_origin[0]
        assert value in (1, -1)
        origin_pivots.append(descriptor)
    assert len(set(origin_pivots)) == 15

    w0 = (
        ("S", 0, 0),
        ("S", 0, 1),
        ("S", 0, 2),
        ("R", 0, 0, 1),
        ("R", 0, 0, 2),
        ("R", 0, 0, 3),
        ("R", 0, 1, 2),
        ("R", 0, 1, 3),
        ("R", 0, 2, 3),
        ("C", 0, 1, 0),
    )
    sym2m_descriptors = set().union(*(set(vector) for vector in vectors[:10]))
    assert set(w0[:-1]).issubset(sym2m_descriptors)
    target = w0[-1]
    assert target not in sym2m_descriptors

    all_descriptors = sorted(
        {target}.union(*(set(vector) for vector in vectors)),
        key=repr,
    )
    equations = []
    for descriptor in all_descriptors:
        equation = sum(
            coefficient_symbols[index] * vectors[index].get(descriptor, 0)
            for index in range(15)
        ) - (1 if descriptor == target else 0)
        if equation != 0:
            equations.append(equation)

    basis = groebner(
        equations,
        *coefficient_symbols,
        B,
        C,
        D,
        order="lex",
    )
    full_basis = [polynomial.as_expr() for polynomial in basis.polys]
    elimination_basis = [
        polynomial
        for polynomial in full_basis
        if not any(polynomial.has(symbol) for symbol in coefficient_symbols)
    ]
    assert elimination_basis == [B**2, C, D]

    expected_full_basis = (
        list(coefficient_symbols[:10])
        + [coefficient_symbols[10] - 1, -B + coefficient_symbols[11]]
        + list(coefficient_symbols[12:])
        + [B**2, C, D]
    )
    assert full_basis == expected_full_basis

    moving_vectors = {
        basis_names[index]: {
            descriptor_text(descriptor): str(coefficient)
            for descriptor, coefficient in vectors[index].items()
        }
        for index in range(10, 15)
    }
    result = {
        "status": "PASS_STANDALONE_EXACT_QQ_ORBIT1_LENGTH_TWO",
        "field": "QQ",
        "project_imports": 0,
        "quotient_relation": (
            "q(x_ia*x_jb)=-q(x_ib*x_ja) for i!=j and a!=b"
        ),
        "moving_line": "x10+B*x11+C*x20+D*x21",
        "W0": [descriptor_text(descriptor) for descriptor in w0],
        "sym2L_basis": basis_names,
        "origin_unit_pivots": [
            descriptor_text(descriptor) for descriptor in origin_pivots
        ],
        "moving_basis_quotient_expansions": moving_vectors,
        "coefficient_equation_count": len(equations),
        "full_lex_groebner_basis": [str(polynomial) for polynomial in full_basis],
        "elimination_ideal_in_QQ_B_C_D": ["B^2", "C", "D"],
        "fibre_ring": "QQ[B]/(B^2)",
        "fibre_length": 2,
        "manual_reverse_witness": "x00*y+B*x01*y modulo (B^2,C,D)",
        "evidence_role": (
            "standalone exact diagnostic for the coefficient comparison; "
            "the paper gives the same comparison as a pure proof"
        ),
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUTPUT.write_bytes((json.dumps(result, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({
        "status": result["status"],
        "project_imports": result["project_imports"],
        "elimination_ideal": result["elimination_ideal_in_QQ_B_C_D"],
        "fibre_ring": result["fibre_ring"],
        "fibre_length": result["fibre_length"],
        "output": OUTPUT.name,
    }, indent=2))


if __name__ == "__main__":
    main()
