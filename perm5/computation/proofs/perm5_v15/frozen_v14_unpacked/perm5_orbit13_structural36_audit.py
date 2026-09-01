"""Exact diagnostic for a structural p(W) <= 36 orbit-13 proof.

The intended mathematical proof uses two inequalities:

    p(C) <= 3 |C|                                      (noncrossing core),
    p(C union X) - p(C) <= 5 |X|                       (crossings).

For a ten-weight set and at most three crossing weights this gives 36 < 39,
so the former 1001-case p <= 26 table is unnecessary.  This script searches
all 2^14 subsets for counterexamples using the exact characteristic-zero
signed-graph model.  It is a diagnostic, not the proof of the inequalities.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations_with_replacement
from pathlib import Path

from perm5_orbit13_four_row_QQ_audit import (
    CROSSING_POSITIONS,
    NONCROSSING_POSITIONS,
    UA,
    UA_DESCRIPTORS,
    UA_POSITION,
    build_local_tables,
    evaluator,
    quadratic_class,
    torus_weight,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_orbit13_structural36_audit_exact.json"
SUPPORT_VARIABLES = frozenset({0, 1, 2, 5, 6})


def selected(mask: int):
    return tuple(index for index in range(14) if (mask >> index) & 1)


def noncrossing_formula(indices: tuple[int, ...]):
    chosen = {UA_DESCRIPTORS[index] for index in indices}
    squares = [descriptor for descriptor in chosen if descriptor[0] == "S"]
    row_edges = [descriptor for descriptor in chosen if descriptor[0] == "R"]
    column_edges = [descriptor for descriptor in chosen if descriptor[0] == "C"]

    def row_degree(row: int, column: int):
        return sum(
            descriptor[1] == row
            and column in (descriptor[2], descriptor[3])
            for descriptor in row_edges
        )

    def column_degree(row: int, column: int):
        return sum(
            descriptor[3] == column
            and row in (descriptor[1], descriptor[2])
            for descriptor in column_edges
        )

    top_triangle = all(
        ("R", 0, first, second) in chosen
        for first, second in ((0, 1), (0, 2), (1, 2))
    )
    return 5 * int(top_triangle) + sum(
        (row_degree(row, column) + 1)
        * (column_degree(row, column) + 1)
        for _, row, column in squares
    )


def weighted_table_index(tables):
    cubic_groups = defaultdict(list)
    for monomial in combinations_with_replacement(range(25), 3):
        cubic_groups[torus_weight(monomial)].append(monomial)
    weights = []
    for weight, monomials in cubic_groups.items():
        involved = set()
        for monomial in monomials:
            for variable in set(monomial):
                remaining = list(monomial)
                remaining.remove(variable)
                q_index, _sign = quadratic_class(tuple(remaining))
                if q_index in UA_POSITION:
                    involved.add(q_index)
        if involved:
            weights.append(weight)
    assert len(weights) == len(tables)
    return dict(zip(weights, tables))


def add_weight(first, second):
    return tuple(a + b for a, b in zip(first, second))


def crossing_weight(position: int):
    _, first_row, second_row, first_column, second_column = UA_DESCRIPTORS[position]
    representative = (
        5 * first_row + first_column,
        5 * second_row + second_column,
    )
    return torus_weight(representative)


def local_marginal(table, crossing: int):
    relevant, values = table
    if crossing not in relevant:
        return 0
    bit = 1 << relevant.index(crossing)
    maximum = 0
    for mask in range(1 << len(relevant)):
        if mask & bit:
            continue
        delta = values.get(mask | bit, 0) - values.get(mask, 0)
        assert delta >= 0
        maximum = max(maximum, delta)
    return maximum


def cubic_block_details():
    groups = defaultdict(list)
    for monomial in combinations_with_replacement(range(25), 3):
        groups[torus_weight(monomial)].append(monomial)
    details = {}
    for weight, monomials in groups.items():
        rows = {}
        for column, monomial in enumerate(monomials):
            for variable in set(monomial):
                remaining = list(monomial)
                remaining.remove(variable)
                q_index, sign = quadratic_class(tuple(remaining))
                row = rows.setdefault(
                    (variable, q_index), [0] * len(monomials)
                )
                row[column] += sign
        details[weight] = (monomials, rows)
    return details


def support_of(row):
    return tuple(index for index, value in enumerate(row) if value)


def connected_vertex_count(vertex_count: int, rows):
    adjacency = [[] for _ in range(vertex_count)]
    for row in rows:
        support = support_of(row)
        assert len(support) == 2
        first, second = support
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return len(seen)


def structural_locality_shape_audit(blocks):
    """Check the two graph shapes used in the crossing-locality proof.

    Outside L_A, a repeated row/column block has both crossing endpoints
    anchored by quotient labels outside U_A.  A three-row/three-column block
    is K_{3,3}; all U_A-labelled edges form a matching, and deleting the whole
    matching leaves it connected.  These checks diagnose the stated proof
    shapes but are not invoked as a finite classification in the proof.
    """
    ua = set(UA)
    result = {}
    for crossing in CROSSING_POSITIONS:
        descriptor = UA_DESCRIPTORS[crossing]
        first_column, second_column = descriptor[3], descriptor[4]
        q_index = UA[crossing]
        q_weight = crossing_weight(crossing)
        counts = Counter()
        for variable in range(25):
            row_index, column_index = divmod(variable, 5)
            weight = add_weight(q_weight, torus_weight((variable,)))
            monomials, rows = blocks[weight]
            target = rows[(variable, q_index)]
            if variable in SUPPORT_VARIABLES:
                counts["support_rank_drop_at_most_one"] += 1
                continue

            if row_index in {0, 1} or column_index in {
                first_column, second_column
            }:
                target_vertices = support_of(target)
                assert len(target_vertices) == 2
                for vertex in target_vertices:
                    assert any(
                        other_q not in ua and support_of(row) == (vertex,)
                        for (_other_variable, other_q), row in rows.items()
                    )
                counts["external_repeated_row_or_column_anchored"] += 1
                continue

            assert len(monomials) == 6
            assert len(rows) == 9
            assert all(len(support_of(row)) == 2 for row in rows.values())
            degrees = Counter(
                vertex for row in rows.values() for vertex in support_of(row)
            )
            assert set(degrees.values()) == {3}
            assert all(
                row[first] == -row[second]
                for row in rows.values()
                for first, second in [support_of(row)]
            )
            ua_rows = [row for (_variable, q), row in rows.items() if q in ua]
            assert all(UA_POSITION[q] in CROSSING_POSITIONS
                       for (_variable, q), row in rows.items() if q in ua)
            matching_vertices = [
                vertex for row in ua_rows for vertex in support_of(row)
            ]
            assert len(matching_vertices) == len(set(matching_vertices))
            remaining_rows = [
                row for (_variable, q), row in rows.items() if q not in ua
            ]
            assert connected_vertex_count(6, remaining_rows) == 6
            counts["external_k33_minus_matching_connected"] += 1
        assert counts == {
            "support_rank_drop_at_most_one": 5,
            "external_repeated_row_or_column_anchored": 11,
            "external_k33_minus_matching_connected": 9,
        }
        result[str(crossing)] = dict(counts)
    return result


def main():
    tables, local_size_histogram = build_local_tables()
    evaluate = evaluator(tables)
    tables_by_weight = weighted_table_index(tables)
    locality_shape_counts = structural_locality_shape_audit(
        cubic_block_details()
    )
    values = [evaluate(selected(mask)) for mask in range(1 << 14)]

    noncrossing_slack = Counter()
    noncrossing_equality = []
    for mask in range(1 << 11):
        indices = selected(mask)
        value = values[mask]
        assert value == noncrossing_formula(indices)
        bound = 3 * len(indices)
        assert value <= bound
        noncrossing_slack[bound - value] += 1
        if value == bound:
            noncrossing_equality.append(indices)

    crossing_marginal_max = {}
    crossing_marginal_equality_count = {}
    crossing_locality = {}
    for crossing in CROSSING_POSITIONS:
        maximum = 0
        equality_count = 0
        for mask in range(1 << 14):
            if (mask >> crossing) & 1:
                continue
            delta = values[mask | (1 << crossing)] - values[mask]
            assert delta <= 5
            if delta > maximum:
                maximum = delta
                equality_count = 1
            elif delta == maximum:
                equality_count += 1
        crossing_marginal_max[str(crossing)] = maximum
        crossing_marginal_equality_count[str(crossing)] = equality_count
        per_variable = {}
        q_weight = crossing_weight(crossing)
        for variable in range(25):
            weight = add_weight(q_weight, torus_weight((variable,)))
            per_variable[str(variable)] = local_marginal(
                tables_by_weight[weight], crossing
            )
        assert max(
            value for variable, value in per_variable.items()
            if int(variable) not in SUPPORT_VARIABLES
        ) == 0
        assert max(per_variable.values()) <= 1
        crossing_locality[str(crossing)] = {
            "per_variable_local_marginal": per_variable,
            "support_variable_sum_bound": sum(
                value for variable, value in per_variable.items()
                if int(variable) in SUPPORT_VARIABLES
            ),
            "external_variable_max": max(
                value for variable, value in per_variable.items()
                if int(variable) not in SUPPORT_VARIABLES
            ),
        }

    global_slack = Counter()
    ten_weight_coarse_bounds = Counter()
    actual_ten_weight_max = 0
    for mask in range(1 << 14):
        core_size = sum((mask >> index) & 1 for index in NONCROSSING_POSITIONS)
        crossing_size = sum((mask >> index) & 1 for index in CROSSING_POSITIONS)
        bound = 3 * core_size + 5 * crossing_size
        assert values[mask] <= bound
        global_slack[bound - values[mask]] += 1
        if core_size + crossing_size == 10:
            ten_weight_coarse_bounds[crossing_size] = max(
                ten_weight_coarse_bounds[crossing_size], bound
            )
            actual_ten_weight_max = max(actual_ten_weight_max, values[mask])

    assert dict(ten_weight_coarse_bounds) == {0: 30, 1: 32, 2: 34, 3: 36}
    assert actual_ten_weight_max == 26
    result = {
        "status": "PASS_EXACT_QQ_ORBIT13_STRUCTURAL36_DIAGNOSTIC",
        "evidence_role": (
            "counterexample search and arithmetic check only; the proof is "
            "the noncrossing charging lemma plus crossing locality lemma"
        ),
        "field": "Q",
        "all_2pow14_subsets_checked": 1 << 14,
        "local_relevant_block_count": len(tables),
        "local_relevant_size_histogram": dict(local_size_histogram),
        "noncrossing_formula_checked_subsets": 1 << 11,
        "noncrossing_equality_count": len(noncrossing_equality),
        "noncrossing_slack_histogram": dict(sorted(noncrossing_slack.items())),
        "crossing_marginal_max": crossing_marginal_max,
        "crossing_marginal_equality_count": crossing_marginal_equality_count,
        "crossing_locality_by_weight_block": crossing_locality,
        "crossing_locality_shape_counts": locality_shape_counts,
        "global_weighted_bound_slack_histogram": dict(sorted(global_slack.items())),
        "ten_weight_coarse_bounds_by_crossing_count": dict(
            sorted(ten_weight_coarse_bounds.items())
        ),
        "structural_ten_weight_bound": 36,
        "actual_ten_weight_max_diagnostic": actual_ten_weight_max,
        "required_threshold": 39,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
