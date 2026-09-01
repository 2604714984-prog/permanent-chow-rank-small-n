"""Exact characteristic-zero audit for the orbit-13 fourteen-weight table.

The calculation is intentionally small and self-contained.  It reconstructs
the quotient weights of Sym^2(K^5) modulo E_5, decomposes the first
prolongation by row/column torus weight, and performs every local rank over Q.
It then checks all C(14,10)=1001 ten-weight subsets of the adjacent 3+2
five-coordinate support used by orbit 13.

The resulting JSON is an independent exact diagnostic for the finite cut
table.  The paper proof should cite the graph-cut rule, not this program, as
the mathematical reason for the local ranks.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_orbit13_four_row_QQ_audit_exact.json"
N = 5


def build_classes():
    result = []
    for row in range(N):
        for column in range(N):
            result.append(("S", row, column))
    for row in range(N):
        for first, second in combinations(range(N), 2):
            result.append(("R", row, first, second))
    for column in range(N):
        for first, second in combinations(range(N), 2):
            result.append(("C", first, second, column))
    for r1, r2 in combinations(range(N), 2):
        for c1, c2 in combinations(range(N), 2):
            result.append(("X", r1, r2, c1, c2))
    assert len(result) == 225
    return tuple(result)


CLASSES = build_classes()
CLASS_INDEX = {descriptor: i for i, descriptor in enumerate(CLASSES)}


UA_DESCRIPTORS = (
    ("S", 0, 0), ("S", 0, 1), ("S", 0, 2),
    ("S", 1, 0), ("S", 1, 1),
    ("R", 0, 0, 1), ("R", 0, 0, 2), ("R", 0, 1, 2),
    ("R", 1, 0, 1),
    ("C", 0, 1, 0), ("C", 0, 1, 1),
    ("X", 0, 1, 0, 1), ("X", 0, 1, 0, 2),
    ("X", 0, 1, 1, 2),
)
UA = tuple(CLASS_INDEX[value] for value in UA_DESCRIPTORS)
UA_POSITION = {value: i for i, value in enumerate(UA)}
CROSSING_POSITIONS = (11, 12, 13)
NONCROSSING_POSITIONS = tuple(range(11))


def torus_weight(monomial: tuple[int, ...]):
    rows = [0] * N
    columns = [0] * N
    for variable in monomial:
        row, column = divmod(variable, N)
        rows[row] += 1
        columns[column] += 1
    return tuple(rows + columns)


def quadratic_class(monomial: tuple[int, int]):
    first, second = sorted(monomial)
    r1, c1 = divmod(first, N)
    r2, c2 = divmod(second, N)
    if first == second:
        return CLASS_INDEX[("S", r1, c1)], 1
    if r1 == r2:
        return CLASS_INDEX[("R", r1, min(c1, c2), max(c1, c2))], 1
    if c1 == c2:
        return CLASS_INDEX[("C", min(r1, r2), max(r1, r2), c1)], 1
    descriptor = ("X", min(r1, r2), max(r1, r2),
                  min(c1, c2), max(c1, c2))
    representative = (N * descriptor[1] + descriptor[3],
                      N * descriptor[2] + descriptor[4])
    return CLASS_INDEX[descriptor], 1 if (first, second) == representative else -1


def rank_q(rows: list[list[int]]):
    matrix = [[Fraction(value) for value in row] for row in rows if any(row)]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for i in range(len(matrix)):
            if i == rank or not matrix[i][column]:
                continue
            factor = matrix[i][column]
            matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def graph_kernel_dimension(rows, monomial_count: int, selected: set[int]):
    """Kernel dimension from the signed coefficient-relation graph.

    A constrained row has one nonzero entry (an anchor to zero) or two
    nonzero entries (a signed equality edge).  Thus every local kernel is a
    connected-component count; this is the graph-cut formulation used in the
    pure proof.
    """
    adjacency = [[] for _ in range(monomial_count)]
    anchored = [False] * monomial_count
    for (_variable, q_index), row in rows.items():
        if q_index in selected:
            continue
        support = [(i, value) for i, value in enumerate(row) if value]
        assert 1 <= len(support) <= 2
        if len(support) == 1:
            anchored[support[0][0]] = True
        else:
            (u, a), (v, b) = support
            ratio = Fraction(-a, b)  # coefficient(v) = ratio * coefficient(u)
            adjacency[u].append((v, ratio))
            adjacency[v].append((u, 1 / ratio))

    seen = {}
    dimension = 0
    for start in range(monomial_count):
        if start in seen:
            continue
        seen[start] = Fraction(1)
        stack = [start]
        component_anchored = False
        consistent = True
        while stack:
            u = stack.pop()
            component_anchored |= anchored[u]
            for v, ratio in adjacency[u]:
                value = ratio * seen[u]
                if v in seen:
                    consistent &= seen[v] == value
                else:
                    seen[v] = value
                    stack.append(v)
        if consistent and not component_anchored:
            dimension += 1
    return dimension


def build_local_tables():
    cubic_groups = defaultdict(list)
    for monomial in combinations_with_replacement(range(25), 3):
        cubic_groups[torus_weight(monomial)].append(monomial)

    tables = []
    local_sizes = Counter()
    for monomials in cubic_groups.values():
        rows = {}
        involved = set()
        for column, monomial in enumerate(monomials):
            # Divided-power coordinates: one derivative incidence per
            # distinct variable.  This is Q-linearly equivalent to ordinary
            # derivatives and keeps all entries integral in {-1,0,1}.
            for variable in set(monomial):
                remaining = list(monomial)
                remaining.remove(variable)
                q_index, sign = quadratic_class(tuple(remaining))
                involved.add(q_index)
                row = rows.setdefault((variable, q_index), [0] * len(monomials))
                row[column] += sign
        relevant = tuple(sorted(value for value in involved if value in UA_POSITION))
        if not relevant:
            continue
        full_rows = list(rows.values())
        base_kernel = len(monomials) - rank_q(full_rows)
        values = {}
        graph_base_kernel = graph_kernel_dimension(rows, len(monomials), set())
        assert graph_base_kernel == base_kernel
        for local_mask in range(1 << len(relevant)):
            selected = {relevant[i] for i in range(len(relevant))
                        if (local_mask >> i) & 1}
            constrained = [row for (_variable, q_index), row in rows.items()
                           if q_index not in selected]
            relative = len(monomials) - rank_q(constrained) - base_kernel
            graph_relative = (
                graph_kernel_dimension(rows, len(monomials), selected)
                - graph_base_kernel
            )
            assert graph_relative == relative
            if relative:
                values[local_mask] = relative
        tables.append((tuple(UA_POSITION[value] for value in relevant), values))
        local_sizes[len(relevant)] += 1
    return tables, local_sizes


def evaluator(tables):
    def evaluate(selected_positions):
        selected = set(selected_positions)
        total = 0
        for relevant, values in tables:
            mask = sum(1 << i for i, position in enumerate(relevant)
                       if position in selected)
            total += values.get(mask, 0)
        return total
    return evaluate


def descriptor_name(position: int):
    descriptor = UA_DESCRIPTORS[position]
    return "".join(map(str, descriptor))


def crossing_pattern_name(pattern):
    if not pattern:
        return "none"
    return "+".join(descriptor_name(position) for position in pattern)


def bin_name(value: int):
    if 12 <= value <= 16:
        return "12-16"
    if 17 <= value <= 18:
        return "17-18"
    return str(value)


def main():
    tables, local_sizes = build_local_tables()
    p = evaluator(tables)
    assert p(()) == 0
    # The evaluator takes positions 0,...,13 in the displayed universe.
    full_value = p(range(14))
    assert full_value == 41

    records = []
    pattern_summary = {}
    t_summary = {}
    conditional_t = defaultdict(lambda: {"subset_count": 0,
                                         "max_crossing_increment": 0,
                                         "max_p_total": 0})
    p10_histogram = Counter()
    for selected in combinations(range(14), 10):
        selected = tuple(selected)
        crossing_pattern = tuple(x for x in selected if x in CROSSING_POSITIONS)
        core = tuple(x for x in selected if x in NONCROSSING_POSITIONS)
        p_core = p(core)
        p_total = p(selected)
        increment = p_total - p_core
        assert increment >= 0
        p10_histogram[p_total] += 1
        record = {
            "selected": selected,
            "crossing_pattern": crossing_pattern,
            "p_core": p_core,
            "crossing_increment": increment,
            "p_total": p_total,
        }
        records.append(record)
        pattern_key = crossing_pattern_name(crossing_pattern)
        item = pattern_summary.setdefault(pattern_key, {
            "crossing_count": len(crossing_pattern), "subset_count": 0,
            "max_p_core": 0, "max_crossing_increment": 0, "max_p_total": 0})
        item["subset_count"] += 1
        item["max_p_core"] = max(item["max_p_core"], p_core)
        item["max_crossing_increment"] = max(item["max_crossing_increment"], increment)
        item["max_p_total"] = max(item["max_p_total"], p_total)
        t_item = t_summary.setdefault(str(len(crossing_pattern)), {
            "subset_count": 0, "max_p_core": 0,
            "max_crossing_increment": 0, "max_p_total": 0})
        t_item["subset_count"] += 1
        t_item["max_p_core"] = max(t_item["max_p_core"], p_core)
        t_item["max_crossing_increment"] = max(t_item["max_crossing_increment"], increment)
        t_item["max_p_total"] = max(t_item["max_p_total"], p_total)
        conditional = conditional_t[(len(crossing_pattern), p_core)]
        conditional["subset_count"] += 1
        conditional["max_crossing_increment"] = max(
            conditional["max_crossing_increment"], increment)
        conditional["max_p_total"] = max(conditional["max_p_total"], p_total)

    assert len(records) == 1001
    assert max(record["p_total"] for record in records) == 26

    # Ten-line hand table: ranges are chosen so the displayed independent
    # maxima already imply p(W)<=26 in every row.
    hand_ranges = (
        (0, 0, 25),
        (1, 0, 21), (1, 22, 22),
        (2, 0, 16), (2, 17, 19), (2, 20, 20),
        (3, 0, 13), (3, 14, 14), (3, 15, 15), (3, 16, 17),
    )
    hand_table = []
    for crossing_count, lower, upper in hand_ranges:
        items = [value for (t, core_value), value in conditional_t.items()
                 if t == crossing_count and lower <= core_value <= upper]
        assert items
        row = {
            "crossing_count": crossing_count,
            "p_core_range": [lower, upper],
            "subset_count": sum(item["subset_count"] for item in items),
            "max_crossing_increment": max(
                item["max_crossing_increment"] for item in items),
            "max_p_total": max(item["max_p_total"] for item in items),
        }
        row["independent_sum_bound"] = upper + row["max_crossing_increment"]
        assert row["independent_sum_bound"] <= 26
        hand_table.append(row)
    assert sum(row["subset_count"] for row in hand_table) == 1001
    assert [(row["subset_count"], row["max_crossing_increment"],
             row["max_p_total"]) for row in hand_table] == [
        (11, 0, 25), (159, 4, 25), (6, 3, 25),
        (435, 8, 24), (57, 7, 26), (3, 5, 25),
        (306, 12, 23), (9, 9, 23), (8, 10, 25), (7, 8, 25),
    ]
    maximizers = [
        [descriptor_name(position) for position in record["selected"]]
        for record in records if record["p_total"] == 26
    ]
    assert len(maximizers) == 2

    marginal = {}
    for nine in combinations(range(14), 9):
        p9 = p(nine)
        for y in range(14):
            if y in nine:
                continue
            p10 = p(tuple(sorted(nine + (y,))))
            delta = p10 - p9
            kind = UA_DESCRIPTORS[y][0]
            key = (bin_name(p9), kind)
            item = marginal.setdefault(key, {
                "pair_count": 0, "max_delta": 0, "max_p10": 0})
            item["pair_count"] += 1
            item["max_delta"] = max(item["max_delta"], delta)
            item["max_p10"] = max(item["max_p10"], p10)

    ordered_bins = ("12-16", "17-18", "19", "20", "21", "22")
    ordered_types = ("S", "R", "C", "X")
    marginal_table = []
    for value_bin in ordered_bins:
        for kind in ordered_types:
            item = marginal.get((value_bin, kind))
            if item:
                marginal_table.append({"p9_bin": value_bin, "added_type": kind, **item})
    coarse = {}
    for value_bin in ordered_bins:
        items = [item for (key_bin, _), item in marginal.items() if key_bin == value_bin]
        if items:
            coarse[value_bin] = {
                "pair_count": sum(item["pair_count"] for item in items),
                "max_delta": max(item["max_delta"] for item in items),
                "max_p10": max(item["max_p10"] for item in items),
            }
    assert [coarse[value]["max_delta"] for value in ordered_bins] == [9, 8, 7, 6, 4, 4]
    assert max(item["max_p10"] for item in coarse.values()) == 26

    result = {
        "status": "PASS_EXACT_RATIONAL_ORBIT13_FOUR_ROW_AUDIT",
        "proof_dependency": False,
        "field": "Q",
        "uses_finite_field": False,
        "uses_floating_point": False,
        "all_local_Q_kernels_equal_signed_graph_component_counts": True,
        "fourteen_weight_universe": [list(value) for value in UA_DESCRIPTORS],
        "local_relevant_block_count": len(tables),
        "local_relevant_size_histogram": dict(sorted(local_sizes.items())),
        "full_universe_p": full_value,
        "ten_subset_count": len(records),
        "p10_histogram": dict(sorted(p10_histogram.items())),
        "max_p10": max(p10_histogram),
        "p10_maximizers": maximizers,
        "by_crossing_count": t_summary,
        "by_crossing_pattern": pattern_summary,
        "ten_line_hand_table": hand_table,
        "marginal_coarse_table": coarse,
        "marginal_by_added_weight_type": marginal_table,
        "script_sha256_before_output": hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper(),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "status", "field", "ten_subset_count", "p10_histogram", "max_p10",
        "by_crossing_count", "ten_line_hand_table", "by_crossing_pattern",
        "marginal_coarse_table")}, indent=2))


if __name__ == "__main__":
    main()
