"""Independent exact audit for the case-free s19d9 counting proof.

This file is deliberately not a proof dependency.  It checks, using only
integer set combinatorics, the small tables and flag formulas appearing in
the pure proof:

* the Petersen-product lower bound at sizes 19 through 29;
* the two equality layer profiles at size 19;
* the 800 explicit flag families and their 45-element shadows;
* uniqueness of the 19-element preimage over every such shadow;
* the 100 ordinary plus 35 mixed first-prolongation lines;
* the special e=0 mixed-block formula for every flag position; and
* the final nine-direction bound for e=0,...,9.

No old orbit table, finite-field file, SAT certificate, LP solution, random
sample, or owner/matching witness is imported.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_s19d9_pure_count_audit_exact.json"
VERTICES = tuple(range(5))
EDGES = tuple(itertools.combinations(VERTICES, 2))
TRIPLES = tuple(itertools.combinations(VERTICES, 3))
G = (3, 4)  # the one missing W-edge
W = frozenset(set(EDGES) - {G})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def edge(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def petersen_neighborhood(vertices) -> frozenset[tuple[int, int]]:
    vertices = set(vertices)
    return frozenset(e for e in EDGES if any(set(e).isdisjoint(v) for v in vertices))


def product_shadow(family) -> frozenset[tuple[tuple[int, int], tuple[int, int]]]:
    out = set()
    for a, b in family:
        out.update(itertools.product(petersen_neighborhood({a}), petersen_neighborhood({b})))
    return frozenset(out)


def h_table() -> tuple[int, ...]:
    answer = []
    for size in range(11):
        minimum = min(
            len(petersen_neighborhood(subset))
            for subset in itertools.combinations(EDGES, size)
        )
        answer.append(10 - minimum)
    return tuple(answer)


def layer_dp(h):
    d = (0,) + tuple(h[t - 1] - h[t] for t in range(1, 11))
    cache = {}

    def solve(j: int, remaining: int, ceiling: int):
        key = (j, remaining, ceiling)
        if key in cache:
            return cache[key]
        if j == 11:
            answer = (0, ((),)) if remaining == 0 else (-10**9, ())
            cache[key] = answer
            return answer
        best = -10**9
        profiles = []
        for value in range(min(ceiling, remaining) + 1):
            tail_value, tails = solve(j + 1, remaining - value, value)
            candidate = d[j] * h[value] + tail_value
            if candidate > best:
                best = candidate
                profiles = [(value,) + tail for tail in tails]
            elif candidate == best:
                profiles.extend((value,) + tail for tail in tails)
        answer = (best, tuple(profiles))
        cache[key] = answer
        return answer

    return d, solve


def flag_family(p: int, z: int, q: int, y: int, transpose: bool):
    e = edge(p, z)
    f = edge(q, y)
    row_star = frozenset(edge(p, v) for v in VERTICES if v != p)
    col_star = frozenset(edge(q, v) for v in VERTICES if v != q)
    meet_f = frozenset(v for v in EDGES if set(v) & set(f))
    family = {(e, v) for v in meet_f}
    family.update((u, v) for u in row_star - {e} for v in col_star)
    if transpose:
        family = {(v, u) for u, v in family}
    return frozenset(family), e, f


def expected_shadow(p: int, z: int, q: int, y: int, transpose: bool):
    e = edge(p, z)
    f = edge(q, y)
    r0 = petersen_neighborhood({e})
    r1 = frozenset(v for v in EDGES if p not in v)
    c0 = frozenset(set(EDGES) - {f})
    c1 = frozenset(v for v in EDGES if q not in v)
    shadow = set(itertools.product(r0, c0)) | set(itertools.product(r1, c1))
    if transpose:
        shadow = {(v, u) for u, v in shadow}
    return frozenset(shadow)


def full_preimage(shadow):
    return frozenset(
        (u, v)
        for u in EDGES
        for v in EDGES
        if set(itertools.product(petersen_neighborhood({u}), petersen_neighborhood({v})))
        <= set(shadow)
    )


def triangle_set(graph_edges):
    graph_edges = set(graph_edges)
    return frozenset(
        triple
        for triple in TRIPLES
        if set(itertools.combinations(triple, 2)) <= graph_edges
    )


def mixed_w_only_count(shadow):
    triangles = triangle_set(W)
    total = len(triangles)  # r=0
    for r in range(1, 5):
        row_pair = edge(0, r)
        fibre = {col_pair for rp, col_pair in shadow if rp == row_pair}
        total += sum(set(itertools.combinations(c, 2)) <= fibre for c in triangles)
    return total


def alpha(f):
    """Number of W-triangles contained after deleting the edge f."""
    return sum(f not in set(itertools.combinations(c, 2)) for c in triangle_set(W))


def beta(v):
    """Number of W-triangles contained after deleting the vertex v."""
    return sum(v not in c for c in triangle_set(W))


def gamma(e):
    """Whether N_P(e), itself a triangle, avoids the missing W-edge."""
    return int(G not in petersen_neighborhood({e}))


def mixed_w_only_formula(p: int, z: int, q: int, y: int, transpose: bool):
    e = edge(p, z)
    f = edge(q, y)
    star0 = {edge(0, r) for r in range(1, 5)}
    r0 = set(petersen_neighborhood({e}))
    r1 = {v for v in EDGES if p not in v}
    c0 = set(EDGES) - {f}
    c1 = {v for v in EDGES if q not in v}
    if not transpose:
        a = len(star0 & r0)
        b = len(star0 & (r1 - r0))
        return 7 + a * alpha(f) + b * beta(q)
    a = len(star0 & c1)
    b = len(star0 & (c0 - c1))
    return 7 + a * beta(p) + b * gamma(e)


def monomial(*variables: int):
    return tuple(sorted(variables))


def derivative(poly, variable: int):
    out = Counter()
    for term, coefficient in poly.items():
        multiplicity = term.count(variable)
        if multiplicity:
            remaining = list(term)
            remaining.remove(variable)
            out[tuple(remaining)] += coefficient * multiplicity
    return {term: value for term, value in out.items() if value}


def normalized(poly):
    if not poly:
        return ()
    items = sorted(poly.items())
    first = items[0][1]
    return tuple((term, value // first) for term, value in items)


def ordinary_cubic(rows, cols):
    out = Counter()
    for permutation in itertools.permutations(cols):
        out[monomial(*(5 * row + col for row, col in zip(rows, permutation)))] += 1
    return dict(out)


def mixed_cubic(r: int, cols):
    if r == 0:
        return {monomial(*(5 * 0 + col for col in cols)): 1}
    out = {}
    for special in cols:
        variables = [5 * r + special]
        variables.extend(5 * 0 + col for col in cols if col != special)
        out[monomial(*variables)] = 1
    return out


def prolongation_line_audit():
    h_quadrics = []
    for rows in itertools.combinations(VERTICES, 2):
        for cols in itertools.combinations(VERTICES, 2):
            i, j = rows
            a, b = cols
            h_quadrics.append(
                {
                    monomial(5 * i + a, 5 * j + b): 1,
                    monomial(5 * i + b, 5 * j + a): 1,
                }
            )
    for a, b in W:
        h_quadrics.append({monomial(a, b): 1})
    h_lines = {normalized(q) for q in h_quadrics}
    assert len(h_lines) == 109

    cubics = []
    for rows in TRIPLES:
        for cols in TRIPLES:
            cubics.append(("ordinary", rows, cols, ordinary_cubic(rows, cols)))
    for r in VERTICES:
        for cols in TRIPLES:
            if G not in set(itertools.combinations(cols, 2)):
                cubics.append(("mixed", r, cols, mixed_cubic(r, cols)))
    assert Counter(kind for kind, *_ in cubics) == {"ordinary": 100, "mixed": 35}

    weights = set()
    for kind, rows_or_r, cols, poly in cubics:
        row_weight = [0] * 5
        col_weight = [0] * 5
        sample = next(iter(poly))
        for variable in sample:
            row, col = divmod(variable, 5)
            row_weight[row] += 1
            col_weight[col] += 1
        weight = (tuple(row_weight), tuple(col_weight))
        assert weight not in weights
        weights.add(weight)
        for variable in range(25):
            value = derivative(poly, variable)
            if value:
                assert normalized(value) in h_lines, (kind, rows_or_r, cols, variable, value)
    return {"ordinary_lines": 100, "mixed_lines": 35, "distinct_torus_weights": len(weights)}


def main() -> None:
    h = h_table()
    assert h == (10, 7, 5, 4, 4, 2, 1, 1, 0, 0, 0)
    d, solve = layer_dp(h)
    assert d == (0, 3, 2, 1, 0, 2, 1, 0, 1, 0, 0)
    product_lower_bounds = {}
    for size in range(19, 101):
        maximum_complement, profiles = solve(1, size, 10)
        product_lower_bounds[size] = 100 - maximum_complement
    assert all(
        product_lower_bounds[size] <= product_lower_bounds[size + 1]
        for size in range(19, 100)
    )
    assert {size: product_lower_bounds[size] for size in range(19, 30)} == {
        19: 45,
        20: 48,
        21: 48,
        22: 48,
        23: 52,
        24: 53,
        25: 54,
        26: 54,
        27: 54,
        28: 54,
        29: 57,
    }
    _value_19, profiles_19 = solve(1, 19, 10)
    assert set(profiles_19) == {
        (4, 4, 4, 4, 1, 1, 1, 0, 0, 0),
        (7, 4, 4, 4, 0, 0, 0, 0, 0, 0),
    }

    families = set()
    shadows = set()
    e0_histogram = Counter()
    e0_by_type = {False: Counter(), True: Counter()}
    for transpose in (False, True):
        for p in VERTICES:
            for z in VERTICES:
                if z == p:
                    continue
                for q in VERTICES:
                    for y in VERTICES:
                        if y == q:
                            continue
                        family, _e, _f = flag_family(p, z, q, y, transpose)
                        shadow = product_shadow(family)
                        assert len(family) == 19
                        assert len(shadow) == 45
                        assert shadow == expected_shadow(p, z, q, y, transpose)
                        assert full_preimage(shadow) == family
                        actual = mixed_w_only_count(shadow)
                        formula = mixed_w_only_formula(p, z, q, y, transpose)
                        assert actual == formula
                        assert actual <= 25
                        families.add(family)
                        shadows.add(shadow)
                        e0_histogram[actual] += 1
                        e0_by_type[transpose][actual] += 1
    assert len(families) == len(shadows) == 800
    assert max(e0_histogram) == 25

    triangle_maximum = []
    for size in range(11):
        triangle_maximum.append(
            max(
                len(triangle_set(subset))
                for subset in itertools.combinations(EDGES, size)
            )
        )
    assert tuple(triangle_maximum) == (0, 0, 0, 1, 1, 2, 4, 4, 5, 7, 10)

    completed_ordinary_bound = []
    for e_count in range(10):
        shadow_budget = 45 + e_count
        maximum = max(
            count
            for count in range(82)
            if product_lower_bounds[19 + count] <= shadow_budget
        )
        completed_ordinary_bound.append(maximum)
    assert completed_ordinary_bound == [0, 0, 0, 3, 3, 3, 3, 4, 5, 9]

    final_table = []
    for e_count in range(10):
        w_count = 9 - e_count
        ordinary = completed_ordinary_bound[e_count]
        if e_count == 0:
            mixed = max(e0_histogram)
        else:
            mixed = 5 * triangle_maximum[w_count]
        total = ordinary + mixed
        assert total <= 25
        final_table.append(
            {
                "E_directions_e": e_count,
                "W_directions_9_minus_e": w_count,
                "ordinary_completed_bound": ordinary,
                "mixed_completed_bound": mixed,
                "total_completed_bound": total,
            }
        )

    result = {
        "status": "PASS",
        "claim_type": "independent exact integer audit of the case-free s19d9 pure counting proof",
        "evidence_class": "exact_integer_audit_only_not_a_proof_dependency",
        "imports_old_certificate_data": False,
        "petersen_h_table": list(h),
        "product_shadow_lower_bounds_19_through_29": {
            str(size): product_lower_bounds[size] for size in range(19, 30)
        },
        "size_19_equality_layer_profiles": [list(p) for p in sorted(profiles_19)],
        "explicit_flag_families": len(families),
        "distinct_flag_shadows": len(shadows),
        "all_flag_shadows_have_unique_19_element_full_preimage": True,
        "e0_mixed_count_histogram": {
            str(value): count for value, count in sorted(e0_histogram.items())
        },
        "e0_histogram_untransposed": {
            str(value): count for value, count in sorted(e0_by_type[False].items())
        },
        "e0_histogram_transposed": {
            str(value): count for value, count in sorted(e0_by_type[True].items())
        },
        "five_vertex_triangle_maximum_by_edge_count": triangle_maximum,
        "completed_ordinary_bound_by_e": completed_ordinary_bound,
        "first_prolongation_lines": prolongation_line_audit(),
        "final_nine_direction_table": final_table,
        "uniform_completed_nonbaseline_bound": max(row["total_completed_bound"] for row in final_table),
        "uniform_first_prolongation_bound": 19
        + max(row["total_completed_bound"] for row in final_table),
        "strict_scope": (
            "The script audits the finite arithmetic and explicit flag formulas. "
            "The proof is the written Petersen layer inequality, equality recovery, "
            "torus-weight classification, and the two-table count."
        ),
    }
    assert result["uniform_completed_nonbaseline_bound"] == 25
    assert result["uniform_first_prolongation_bound"] == 44
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": result["status"],
                "flags": len(families),
                "prolongation_lines": result["first_prolongation_lines"],
                "completed_bound": result["uniform_completed_nonbaseline_bound"],
                "prolongation_bound": result["uniform_first_prolongation_bound"],
                "output": OUTPUT.name,
                "sha256": sha256(OUTPUT),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
