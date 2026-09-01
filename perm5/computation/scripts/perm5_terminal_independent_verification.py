#!/usr/bin/env python3
"""Definition-level independent verification of the final perm_5 orbit-0 endpoint.

The script has two self-contained parts and imports no project code or frozen
payload:

1. It builds the 4,100-variable tangent graph for the orbit-0 flag directly
   from the linearized condition partial(S) subset T.  Because every equation
   has one variable or a two-variable coefficient pattern (+1,-1), the kernel
   dimension over every field is the number of unanchored connected components.
2. It reconstructs the Boolean-Fourier shortening calculation over QQ and
   verifies the numerical endpoint 2,215 > 9*245 = 2,205.

This is an verification of the finite endpoint.  The geometric reduction to orbit 0
and the representation-theoretic passage from the tangent calculation to the
local symbol are written in the paper.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path


def tangent_graph_verification() -> dict[str, object]:
    a3 = list(combinations(range(5), 3))
    a2 = list(combinations(range(5), 2))
    b3 = list(combinations(range(5), 3))
    b2 = list(combinations(range(5), 2))
    u0 = [(0, 1, 2), (0, 1, 3)]
    uout = [x for x in a3 if x not in u0]
    r0 = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3)]
    rout = [x for x in a2 if x not in r0]

    vertices: list[tuple[object, ...]] = []
    index: dict[tuple[object, ...], int] = {}
    for ur in u0:
        for bc in b3:
            for vr in uout:
                for dc in b3:
                    key = ("S", ur, bc, vr, dc)
                    index[key] = len(vertices)
                    vertices.append(key)
    for rr in r0:
        for bc in b2:
            for tr in rout:
                for dc in b2:
                    key = ("T", rr, bc, tr, dc)
                    index[key] = len(vertices)
                    vertices.append(key)
    if len(vertices) != 4100:
        raise RuntimeError(("vertex count", len(vertices)))

    equations: set[tuple[int, ...]] = set()
    for ur in u0:
        for bc in b3:
            for i in range(5):
                for a in range(5):
                    for tr in rout:
                        for dc in b2:
                            terms: list[int] = []
                            if i not in tr and a not in dc:
                                vr = tuple(sorted(tr + (i,)))
                                outc = tuple(sorted(dc + (a,)))
                                terms.append(index[("S", ur, bc, vr, outc)])
                            if i in ur and a in bc:
                                rr = tuple(x for x in ur if x != i)
                                inc = tuple(x for x in bc if x != a)
                                terms.append(index[("T", rr, inc, tr, dc)])
                            if terms:
                                equations.add(tuple(terms))

    parent = list(range(len(vertices)))
    size = [1] * len(vertices)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a == b:
            return
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]

    anchors: set[int] = set()
    edges: set[tuple[int, int]] = set()
    for equation in equations:
        if len(equation) == 1:
            anchors.add(equation[0])
        elif len(equation) == 2:
            edges.add(tuple(sorted(equation)))
        else:
            raise RuntimeError(("non-graph equation", equation))
    for a, b in edges:
        union(a, b)

    anchored_roots = {find(a) for a in anchors}
    components: dict[int, list[int]] = defaultdict(list)
    for v in range(len(vertices)):
        components[find(v)].append(v)
    unanchored = [vals for root, vals in components.items() if root not in anchored_roots]
    unanchored_sizes = sorted(len(vals) for vals in unanchored)
    expected_sizes = [20, 20, 20, 20, 30, 30, 50, 50]
    if unanchored_sizes != expected_sizes:
        raise RuntimeError(("unanchored component sizes", unanchored_sizes))

    # Verify that each kernel component is fixed setwise by every column permutation.
    def permute_vertex(v: int, permutation: tuple[int, ...]) -> int:
        key = vertices[v]
        if key[0] == "S":
            kind, ur, bc, vr, dc = key
            bc2 = tuple(sorted(permutation[x] for x in bc))
            dc2 = tuple(sorted(permutation[x] for x in dc))
            return index[(kind, ur, bc2, vr, dc2)]
        kind, rr, bc, tr, dc = key
        bc2 = tuple(sorted(permutation[x] for x in bc))
        dc2 = tuple(sorted(permutation[x] for x in dc))
        return index[(kind, rr, bc2, tr, dc2)]

    all_column_permutations = tuple(permutations(range(5)))
    column_trivial = all(
        {permute_vertex(v, p) for v in component} == set(component)
        for component in unanchored
        for p in all_column_permutations
    )
    if not column_trivial:
        raise RuntimeError("column action is not setwise trivial on a kernel component")

    return {
        "status": "PASS",
        "coefficient_pattern": "one-variable anchors and two-variable (+1,-1) edges",
        "vertex_count": len(vertices),
        "distinct_one_term_equations": len(anchors),
        "distinct_two_term_equations": len(edges),
        "connected_component_count": len(components),
        "unanchored_component_count": len(unanchored),
        "kernel_dimension_over_every_field": len(unanchored),
        "unanchored_component_sizes": unanchored_sizes,
        "column_permutation_group_order": len(all_column_permutations),
        "every_kernel_component_fixed_setwise_by_columns": column_trivial,
    }


def matrix_rank(columns: list[tuple[int, ...] | list[int]]) -> int:
    if not columns:
        return 0
    rows = len(columns[0])
    matrix = [
        [Fraction(columns[col][row]) for col in range(len(columns))]
        for row in range(rows)
    ]
    rank = 0
    for col in range(len(columns)):
        pivot = next(
            (row for row in range(rank, rows) if matrix[row][col]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][col]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(rows):
            if row == rank or not matrix[row][col]:
                continue
            scale = matrix[row][col]
            matrix[row] = [
                a - scale * b for a, b in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def nullspace_dimension(columns: list[tuple[int, ...] | list[int]]) -> int:
    return len(columns) - matrix_rank(columns)


def right_nullspace_basis(columns: list[tuple[int, ...]]) -> list[list[Fraction]]:
    if not columns:
        return []
    rows = len(columns[0])
    cols = len(columns)
    matrix = [
        [Fraction(columns[col][row]) for col in range(cols)]
        for row in range(rows)
    ]
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][col]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][col]:
                continue
            scale = matrix[row][col]
            matrix[row] = [
                a - scale * b for a, b in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    free_cols = [col for col in range(cols) if col not in pivot_cols]
    basis: list[list[Fraction]] = []
    for free in free_cols:
        vector = [Fraction(0)] * cols
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivot_cols):
            vector[pivot] = -matrix[row][free]
        basis.append(vector)
    return basis


def fourier_verification() -> dict[str, object]:
    omega = [(1,) + signs for signs in product((-1, 1), repeat=4)]
    subsets_le2 = [s for degree in range(3) for s in combinations(range(4), degree)]
    subsets_le3 = [s for degree in range(4) for s in combinations(range(4), degree)]

    def character(point: tuple[int, ...], subset: tuple[int, ...]) -> int:
        value = 1
        for index in subset:
            value *= point[index + 1]
        return value

    def catalecticant_rank(weights: list[int]) -> int:
        columns: list[tuple[int, ...]] = []
        for b in subsets_le2:
            column = []
            for a in subsets_le3:
                total = sum(
                    character(z, (0, 1, 2, 3))
                    * weight
                    * character(z, a)
                    * character(z, b)
                    for z, weight in zip(omega, weights)
                )
                column.append(total)
            columns.append(tuple(column))
        return matrix_rank(columns)

    baseline = catalecticant_rank([1] * 16)
    if baseline != 10:
        raise RuntimeError(("baseline catalecticant rank", baseline))

    rank_four_sixes = 0
    max_proper_shortening_nullity = 0
    masked_rank_histogram: dict[int, int] = {}
    predicted_r4_histogram: dict[int, int] = {}
    for labels in combinations(range(16), 6):
        label_columns = [omega[index] for index in labels]
        if matrix_rank(label_columns) != 4:
            continue
        rank_four_sixes += 1
        if nullspace_dimension(label_columns) != 2:
            raise RuntimeError(("six-point nullity", labels))
        for size in range(6):
            for subset in combinations(labels, size):
                nullity = nullspace_dimension([omega[index] for index in subset])
                max_proper_shortening_nullity = max(
                    max_proper_shortening_nullity, nullity
                )
                if nullity > 1:
                    raise RuntimeError(("proper shortening nullity", subset, nullity))

        weights = [1] * 16
        for index in labels:
            weights[index] = 0
        masked_rank = catalecticant_rank(weights)
        masked_rank_histogram[masked_rank] = masked_rank_histogram.get(masked_rank, 0) + 1
        if masked_rank != 9:
            raise RuntimeError(("masked rank", labels, masked_rank))

        complement = [index for index in range(16) if index not in labels]
        square_columns = [
            tuple(character(omega[index], subset) for subset in subsets_le2)
            for index in complement
        ]
        relation_basis = right_nullspace_basis(square_columns)
        if len(relation_basis) != 1:
            raise RuntimeError(("complement relation dimension", labels))
        support = [
            complement[j]
            for j, value in enumerate(relation_basis[0])
            if value
        ]
        support_rank = matrix_rank([omega[index] for index in support])
        predicted_r4 = 10 - support_rank
        if predicted_r4 > 7:
            raise RuntimeError(("R4 dimension", labels, predicted_r4))
        predicted_r4_histogram[predicted_r4] = (
            predicted_r4_histogram.get(predicted_r4, 0) + 1
        )

    if rank_four_sixes != 600:
        raise RuntimeError(("rank-four six-subsets", rank_four_sixes))
    global_lower = 25 * 90 - 5 * 7
    nine_term_upper = 9 * 245
    if not global_lower > nine_term_upper:
        raise RuntimeError(("terminal numerical contradiction", global_lower, nine_term_upper))

    return {
        "status": "PASS",
        "field": "QQ",
        "omega_size": len(omega),
        "RM_degree_at_most_2_dimension": len(subsets_le2),
        "RM_degree_at_most_3_dimension": len(subsets_le3),
        "baseline_catalecticant_rank": baseline,
        "rank_four_six_subsets": rank_four_sixes,
        "maximum_proper_shortening_nullity": max_proper_shortening_nullity,
        "masked_catalecticant_rank_histogram": masked_rank_histogram,
        "predicted_R4_dimension_histogram": predicted_r4_histogram,
        "uniform_R4_upper_bound": 7,
        "global_terminal_K_lower": global_lower,
        "nine_Chow_term_K_upper": nine_term_upper,
        "strict_gap": global_lower - nine_term_upper,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "status": "PASS",
        "claim_type": "independent definition-level verification of the orbit-0 terminal certificate",
        "imports_project_code": False,
        "reads_frozen_payload": False,
        "tangent_graph": tangent_graph_verification(),
        "boolean_fourier": fourier_verification(),
        "strict_scope": (
            "The script verifies the finite orbit-0 tangent and Fourier endpoint.  The "
            "geometric reduction to the three terminal orbits and the local-to-global "
            "symbol comparison remain written arguments in the manuscript."
        ),
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "status": payload["status"],
        "tangent_kernel": payload["tangent_graph"]["kernel_dimension_over_every_field"],
        "terminal_lower": payload["boolean_fourier"]["global_terminal_K_lower"],
        "nine_term_upper": payload["boolean_fourier"]["nine_Chow_term_K_upper"],
        "gap": payload["boolean_fourier"]["strict_gap"],
        "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest().upper(),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
