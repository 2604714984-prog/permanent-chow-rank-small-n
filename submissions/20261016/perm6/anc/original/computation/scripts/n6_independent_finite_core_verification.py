#!/usr/bin/env python3
"""Independent finite-core verification for the ordinary Chow-rank-32 proof.

This program intentionally does not import the primary replay or read its
frozen JSON.  It recomputes two load-bearing finite tables from their
definitions by algorithms different from those in the primary replay:

* all labelled subsets of at most six edges of the 6-by-6 bipartite graph;
* all coordinate kernel/killed-edge specializations of the squarefree symbol.

Only Python's standard library and exact integer arithmetic are used.
"""

from __future__ import annotations

from itertools import combinations
from math import comb


VERTICES = tuple(range(6))
GRAPH_EDGES = tuple((row, column) for row in VERTICES for column in VERTICES)
K6_EDGES = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))


def verification_four_cycle_maxima() -> tuple[list[int], list[int]]:
    """Enumerate labelled edge subsets, without row-orbit reduction."""

    maxima: list[int] = []
    candidate_counts: list[int] = []
    for edge_count in range(7):
        best = 0
        seen = 0
        for chosen in combinations(GRAPH_EDGES, edge_count):
            seen += 1
            chosen_set = set(chosen)
            cycles = 0
            for row_a, row_b in combinations(VERTICES, 2):
                common = sum(
                    (row_a, column) in chosen_set
                    and (row_b, column) in chosen_set
                    for column in VERTICES
                )
                cycles += comb(common, 2)
            best = max(best, cycles)
        maxima.append(best)
        candidate_counts.append(seen)
    return maxima, candidate_counts


def direct_symbol_rank(
    kernel_vertices: frozenset[int], killed_edges: frozenset[tuple[int, int]]
) -> int:
    """Count surviving squarefree cubic coordinates directly."""

    surviving = 0
    for triple in TRIPLES:
        for output_vertex in triple:
            input_edge = tuple(v for v in triple if v != output_vertex)
            if output_vertex not in kernel_vertices and input_edge not in killed_edges:
                surviving += 1
                break
    return surviving


def verification_squarefree_symbol_table() -> tuple[list[list[int]], int]:
    """Exhaust the 45,696 coordinate specializations from scratch."""

    table: list[list[int]] = []
    candidate_count = 0
    for relation_bound in range(4):
        allowed_edge_sets = tuple(
            edge_set
            for size in range(relation_bound + 1)
            for edge_set in combinations(K6_EDGES, size)
        )
        row: list[int] = []
        for quotient_dimension in range(7):
            best = len(TRIPLES) + 1
            for kernel_tuple in combinations(VERTICES, 6 - quotient_dimension):
                kernel = frozenset(kernel_tuple)
                for edge_tuple in allowed_edge_sets:
                    candidate_count += 1
                    rank = direct_symbol_rank(kernel, frozenset(edge_tuple))
                    best = min(best, rank)
            row.append(best)
        table.append(row)
    return table, candidate_count


def main() -> None:
    expected_cycles = [0, 0, 0, 0, 1, 1, 3]
    expected_graph_counts = [comb(36, edge_count) for edge_count in range(7)]
    expected_symbol = [
        [0, 10, 16, 19, 20, 20, 20],
        [0, 9, 14, 16, 16, 20, 20],
        [0, 8, 12, 13, 16, 19, 20],
        [0, 7, 10, 10, 15, 17, 19],
    ]

    cycles, graph_counts = verification_four_cycle_maxima()
    symbol, symbol_count = verification_squarefree_symbol_table()

    if cycles != expected_cycles:
        raise SystemExit(f"FAIL: four-cycle maxima {cycles!r}")
    if graph_counts != expected_graph_counts:
        raise SystemExit(f"FAIL: graph candidate counts {graph_counts!r}")
    if symbol != expected_symbol:
        raise SystemExit(f"FAIL: squarefree symbol table {symbol!r}")
    if symbol_count != 45_696:
        raise SystemExit(f"FAIL: symbol candidate count {symbol_count}")

    print("PASS: independent n=6 finite-core verification")
    print(f"labelled bipartite graphs checked: {sum(graph_counts):,}")
    print(f"coordinate symbol cases checked: {symbol_count:,}")


if __name__ == "__main__":
    main()
