"""Exact diagnostic for the no-crossing compression programme for perm_5.

This file is deliberately independent of the large prolongation certificates.
It has two purposes only:

1. exhaustively check the local 0/1 inequalities used in the proposed
   row/column compression lemma;
2. enumerate fully shifted no-crossing families of size at most 12 and report
   their exact integer extrema.

The output is diagnostic support.  The compression lemma and the terminal
shifted-family estimates must still be proved in prose.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import product


N = 5
EDGES = tuple((i, j) for i in range(N) for j in range(i + 1, N))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def popcount(mask: int) -> int:
    return mask.bit_count()


def has_edge(mask: int, i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    return (mask >> EDGE_INDEX[(i, j)]) & 1


@lru_cache(maxsize=None)
def triangle_count(mask: int) -> int:
    return sum(
        has_edge(mask, i, j)
        * has_edge(mask, i, k)
        * has_edge(mask, j, k)
        for i in range(N)
        for j in range(i + 1, N)
        for k in range(j + 1, N)
    )


@lru_cache(maxsize=None)
def degree(mask: int, vertex: int) -> int:
    return sum(has_edge(mask, vertex, other) for other in range(N) if other != vertex)


def graph_shift(mask: int, low: int, high: int) -> int:
    """Standard (low, high)-shift on a simple graph."""
    assert low < high
    out = mask
    for k in range(N):
        if k in (low, high):
            continue
        high_bit = EDGE_INDEX[tuple(sorted((high, k)))]
        low_bit = EDGE_INDEX[tuple(sorted((low, k)))]
        if (out >> high_bit) & 1 and not ((out >> low_bit) & 1):
            out ^= 1 << high_bit
            out |= 1 << low_bit
    return out


def set_shift(mask: int, low: int, high: int) -> int:
    assert low < high
    if (mask >> high) & 1 and not ((mask >> low) & 1):
        return (mask ^ (1 << high)) | (1 << low)
    return mask


def incidence(vertex_mask: int, graph_mask: int) -> int:
    return sum(
        ((vertex_mask >> i) & 1) * degree(graph_mask, i)
        for i in range(N)
    )


def audit_local_compression_inequalities() -> None:
    # Binary rearrangement used for a square and a row edge in two rows.
    for x, y, a, b in product((0, 1), repeat=4):
        lhs = (x | y) * (a | b) + (x & y) * (a & b)
        rhs = x * a + y * b
        assert lhs >= rhs

    # Triangle count is supermodular under union/intersection of graph layers.
    for first in range(1 << len(EDGES)):
        for second in range(1 << len(EDGES)):
            assert (
                triangle_count(first | second) + triangle_count(first & second)
                >= triangle_count(first) + triangle_count(second)
            )

    # Simultaneous vertex-set/graph shifting does not lower incidence.
    for low in range(N):
        for high in range(low + 1, N):
            for vertices in range(1 << N):
                for graph in range(1 << len(EDGES)):
                    assert incidence(
                        set_shift(vertices, low, high),
                        graph_shift(graph, low, high),
                    ) >= incidence(vertices, graph)

    # Standard graph shifting does not lower the number of triangles.
    for low in range(N):
        for high in range(low + 1, N):
            for graph in range(1 << len(EDGES)):
                assert triangle_count(graph_shift(graph, low, high)) >= triangle_count(graph)


def triangle_envelope(max_total: int = 12) -> tuple[int, ...]:
    """Maximum total triangle count in five simple graphs with a total edge budget."""
    states = tuple((popcount(mask), triangle_count(mask)) for mask in range(1 << len(EDGES)))
    envelope = [-10**9] * (max_total + 1)
    envelope[0] = 0
    for _ in range(N):
        updated = envelope[:]
        for old_edges, old_triangles in enumerate(envelope):
            if old_triangles < 0:
                continue
            for edges, triangles in states:
                if old_edges + edges <= max_total:
                    updated[old_edges + edges] = max(
                        updated[old_edges + edges], old_triangles + triangles
                    )
        envelope = updated
    return tuple(envelope)


TAU = triangle_envelope()


def universal_square_bound(square_count: int, row_edges: int, column_edges: int) -> int:
    """The bound s+G+H+C with G<=min(4s,2r), H<=min(4s,2c), C<=rc."""
    row_incidence = min(4 * square_count, 2 * row_edges)
    column_incidence = min(4 * square_count, 2 * column_edges)
    corner = min(
        row_edges * column_edges,
        4 * row_incidence,
        4 * column_incidence,
    )
    return square_count + row_incidence + column_incidence + corner


def one_square_bound(row_edges: int, column_edges: int) -> int:
    return (min(4, row_edges) + 1) * (min(4, column_edges) + 1)


def row_domino_bound(row_edges: int, column_edges: int) -> int:
    # The two row-side marks lie in one graph; only their mutual edge can be
    # counted twice.  The two column-side marks lie in two graph layers.
    row_incidence = min(8, row_edges + (1 if row_edges else 0))
    column_incidence = min(8, column_edges)
    corner = min(
        row_edges * column_edges,
        4 * row_incidence,
        4 * column_incidence,
    )
    return 2 + row_incidence + column_incidence + corner


def row_triple_bound(row_edges: int, column_edges: int) -> int:
    row_incidence = min(12, row_edges + min(row_edges, 3))
    column_incidence = min(12, column_edges)
    return 3 + row_incidence + column_incidence + row_edges * column_edges


def ell_triple_bound(row_edges: int, column_edges: int) -> int:
    row_incidence = min(12, row_edges + (1 if row_edges else 0))
    column_incidence = min(12, column_edges + (1 if column_edges else 0))
    return 3 + row_incidence + column_incidence + row_edges * column_edges


def audit_closed_terminal_bounds() -> None:
    assert TAU == (0, 0, 0, 1, 1, 2, 4, 4, 5, 7, 10, 10, 10)
    targets = {9: 35, 10: 50, 11: 55, 12: 60}
    expected_exceptions = {
        9: {(1, 2, 6), (1, 3, 5), (2, 1, 6), (2, 3, 4)},
        10: set(),
        11: {(2, 3, 6)},
        12: {
            (1, 1, 10),
            (2, 3, 7),
            (2, 4, 6),
            (2, 5, 5),
            (3, 3, 6),
        },
    }
    actual_exceptions: dict[int, set[tuple[int, int, int]]] = {}
    for dimension, target in targets.items():
        exceptional: set[tuple[int, int, int]] = set()
        for square_count in range(dimension + 1):
            edge_count = dimension - square_count
            for row_edges in range(edge_count + 1):
                column_edges = edge_count - row_edges
                bound = 5 * (TAU[row_edges] + TAU[column_edges]) + universal_square_bound(
                    square_count, row_edges, column_edges
                )
                if bound > target:
                    exceptional.add(
                        (square_count, min(row_edges, column_edges), max(row_edges, column_edges))
                    )
        actual_exceptions[dimension] = exceptional
    assert actual_exceptions == expected_exceptions

    # Every one-square exception closes with the exact product bound.
    for dimension, row_edges, column_edges in ((9, 2, 6), (9, 3, 5), (12, 1, 10)):
        assert 5 * (TAU[row_edges] + TAU[column_edges]) + one_square_bound(
            row_edges, column_edges
        ) <= targets[dimension]

    # After transpose, a two-cell Ferrers ideal is a row domino.  The closed
    # domino bound closes all orientations except (d,r,c)=(9,1,6).
    domino_leftovers = []
    for dimension in (9, 11, 12):
        edge_count = dimension - 2
        for row_edges in range(edge_count + 1):
            column_edges = edge_count - row_edges
            bound = 5 * (TAU[row_edges] + TAU[column_edges]) + row_domino_bound(
                row_edges, column_edges
            )
            if bound > targets[dimension]:
                domino_leftovers.append((dimension, row_edges, column_edges, bound))
    assert domino_leftovers == [(9, 1, 6, 36)]
    # In the leftover, the single row edge is {0,1}.  If the six-edge side
    # has four triangles it is one K4, giving square term 10; otherwise its
    # triangle count is at most three and the closed domino bound is 16.
    assert 5 * 4 + 10 <= targets[9]
    assert 5 * 3 + row_domino_bound(1, 6) <= targets[9]

    # A three-cell Ferrers ideal is, up to transpose, a row triple or an L.
    for row_edges, column_edges in ((3, 6), (6, 3)):
        triangle_part = 5 * (TAU[row_edges] + TAU[column_edges])
        assert triangle_part + row_triple_bound(row_edges, column_edges) <= targets[12]
        assert triangle_part + ell_triple_bound(row_edges, column_edges) <= targets[12]

    print("triangle_envelope_0_through_12=" + ",".join(map(str, TAU)))
    print("universal_bound_exception_types_up_to_transpose=10")
    print("one_square_closed_cases=3")
    print("row_domino_unresolved_numeric_cases_after_closed_bound=1")
    print("three_square_Ferrers_shapes_up_to_transpose=2")
    print("PASS_CLOSED_NO_CROSSING_TERMINAL_BOUND_AUDIT")


def is_shifted_graph(mask: int) -> bool:
    return all(
        graph_shift(mask, low, high) == mask
        for low in range(N)
        for high in range(low + 1, N)
    )


SHIFTED_GRAPHS = tuple(mask for mask in range(1 << len(EDGES)) if is_shifted_graph(mask))


def nested_graph_families(max_total: int) -> tuple[tuple[int, ...], ...]:
    out: list[tuple[int, ...]] = []

    def visit(prefix: tuple[int, ...], allowed: tuple[int, ...], total: int) -> None:
        if len(prefix) == N:
            out.append(prefix)
            return
        for graph in allowed:
            size = popcount(graph)
            if total + size > max_total:
                continue
            visit(
                prefix + (graph,),
                tuple(candidate for candidate in allowed if candidate & ~graph == 0),
                total + size,
            )

    visit((), SHIFTED_GRAPHS, 0)
    return tuple(out)


def ferrers_square_masks(max_total: int) -> tuple[int, ...]:
    out: list[int] = []
    # A Ferrers ideal is uniquely encoded by nonincreasing row lengths.
    for lengths in product(range(N + 1), repeat=N):
        if any(lengths[i] < lengths[i + 1] for i in range(N - 1)):
            continue
        if sum(lengths) > max_total:
            continue
        mask = 0
        for i, length in enumerate(lengths):
            for a in range(length):
                mask |= 1 << (N * i + a)
        out.append(mask)
    return tuple(out)


def no_crossing_p(
    squares: int,
    row_graphs: tuple[int, ...],
    column_graphs: tuple[int, ...],
) -> tuple[int, int, int]:
    triangles = sum(map(triangle_count, row_graphs)) + sum(map(triangle_count, column_graphs))
    square_term = 0
    for i in range(N):
        for a in range(N):
            if (squares >> (N * i + a)) & 1:
                square_term += (degree(row_graphs[i], a) + 1) * (
                    degree(column_graphs[a], i) + 1
                )
    return 5 * triangles + square_term, triangles, square_term


def family_descriptor(
    squares: int,
    row_graphs: tuple[int, ...],
    column_graphs: tuple[int, ...],
) -> dict[str, object]:
    p_value, triangles, square_term = no_crossing_p(squares, row_graphs, column_graphs)
    row_sizes = tuple(map(popcount, row_graphs))
    column_sizes = tuple(map(popcount, column_graphs))
    return {
        "dimension": popcount(squares) + sum(row_sizes) + sum(column_sizes),
        "p": p_value,
        "triangles": triangles,
        "square_term": square_term,
        "square_count": popcount(squares),
        "row_sizes": row_sizes,
        "column_sizes": column_sizes,
        "square_rows": tuple(
            sum((squares >> (N * i + a)) & 1 for a in range(N))
            for i in range(N)
        ),
    }


def enumerate_shifted(max_total: int = 12) -> None:
    graph_families = nested_graph_families(max_total)
    squares = ferrers_square_masks(max_total)
    graphs_by_size: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    squares_by_size: dict[int, list[int]] = defaultdict(list)
    for family in graph_families:
        graphs_by_size[sum(map(popcount, family))].append(family)
    for mask in squares:
        squares_by_size[popcount(mask)].append(mask)

    maxima: dict[int, int] = defaultdict(lambda: -1)
    witnesses: dict[int, list[dict[str, object]]] = defaultdict(list)
    subcritical: dict[int, int] = defaultdict(lambda: -1)
    square_envelope: dict[tuple[int, int, int], int] = defaultdict(lambda: -1)
    state_count: dict[int, int] = defaultdict(int)

    for dimension in range(9, max_total + 1):
        for square_count, square_masks in squares_by_size.items():
            if square_count > dimension:
                continue
            for row_edges, rows_list in graphs_by_size.items():
                column_edges = dimension - square_count - row_edges
                if column_edges < 0:
                    continue
                for columns in graphs_by_size.get(column_edges, ()):
                    for rows in rows_list:
                        for square_mask in square_masks:
                            state_count[dimension] += 1
                            p_value, _triangles, square_term = no_crossing_p(
                                square_mask, rows, columns
                            )
                            key = (square_count, row_edges, column_edges)
                            square_envelope[key] = max(square_envelope[key], square_term)
                            if p_value > maxima[dimension]:
                                maxima[dimension] = p_value
                                witnesses[dimension] = [
                                    family_descriptor(square_mask, rows, columns)
                                ]
                            elif p_value == maxima[dimension]:
                                witnesses[dimension].append(
                                    family_descriptor(square_mask, rows, columns)
                                )
                            if max(map(popcount, rows + columns), default=0) <= 8:
                                subcritical[dimension] = max(subcritical[dimension], p_value)

    print(f"shifted_graph_ideals={len(SHIFTED_GRAPHS)}")
    print(f"nested_graph_families_total_le_{max_total}={len(graph_families)}")
    print(f"ferrers_square_ideals_total_le_{max_total}={len(squares)}")
    for dimension in range(9, max_total + 1):
        print(
            f"d={dimension} states={state_count[dimension]} "
            f"max={maxima[dimension]} subcritical_max={subcritical[dimension]} "
            f"witnesses={len(witnesses[dimension])}"
        )
        for witness in witnesses[dimension]:
            print("  ", witness)

    assert len(SHIFTED_GRAPHS) == 16
    assert len(graph_families) == 426
    assert len(squares) == 126
    assert [state_count[d] for d in range(9, 13)] == [2206, 4057, 7247, 12612]
    assert [maxima[d] for d in range(9, 13)] == [35, 50, 55, 60]
    assert [subcritical[d] for d in range(9, 13)] == [32, 37, 41, 46]


def main() -> None:
    audit_local_compression_inequalities()
    print("PASS_LOCAL_0_1_COMPRESSION_INEQUALITIES")
    audit_closed_terminal_bounds()
    enumerate_shifted()
    print("STATUS=EXACT_INTEGER_DIAGNOSTIC_PASS")


if __name__ == "__main__":
    main()
