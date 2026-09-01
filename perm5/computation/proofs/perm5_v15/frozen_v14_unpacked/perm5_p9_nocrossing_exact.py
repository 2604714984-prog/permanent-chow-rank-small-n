"""Independent exact check of the no-crossing p_9 graph inequality.

This script uses only integer arithmetic.  It does not import the large
local-block/SAT certificates.  Formula (9) in perm5_pure_route_20260803.md
reduces the calculation to simple graphs on five vertices.

The output is diagnostic support for the handwritten graph lemma; it is not
used as a substitute for that lemma.
"""

from collections import defaultdict
from itertools import combinations, permutations


EDGES = list(combinations(range(5), 2))


def graph_states():
    out = []
    for mask in range(1 << len(EDGES)):
        adjacency = [[0] * 5 for _ in range(5)]
        degrees = [0] * 5
        edge_count = 0
        for bit, (u, v) in enumerate(EDGES):
            if mask >> bit & 1:
                adjacency[u][v] = adjacency[v][u] = 1
                degrees[u] += 1
                degrees[v] += 1
                edge_count += 1
        triangles = sum(
            adjacency[u][v] * adjacency[u][w] * adjacency[v][w]
            for u, v, w in combinations(range(5), 3)
        )
        out.append((edge_count, triangles, tuple(degrees)))
    return out


STATES = graph_states()


def triangle_envelope(max_edges=10, component_count=5):
    envelope = [-10**9] * (max_edges + 1)
    envelope[0] = 0
    for _ in range(component_count):
        updated = envelope[:]
        for old_edges, old_triangles in enumerate(envelope):
            if old_triangles < 0:
                continue
            for edges, triangles, _ in STATES:
                if old_edges + edges <= max_edges:
                    updated[old_edges + edges] = max(
                        updated[old_edges + edges], old_triangles + triangles
                    )
        envelope = updated
    return envelope


TAU = triangle_envelope(11)


def line_options(marked_vertices):
    best = {}
    for edges, triangles, degrees in STATES:
        key = (edges, tuple(degrees[v] for v in marked_vertices))
        best[key] = max(best.get(key, -1), triangles)
    return [(edges, degrees, triangles) for (edges, degrees), triangles in best.items()]


def side_options(square_cells, row_side, max_edges=10):
    groups = defaultdict(list)
    for row, column in square_cells:
        line = row if row_side else column
        marked = column if row_side else row
        groups[line].append(marked)

    current = [(0, {}, 0)]
    for line, marked in groups.items():
        marked = sorted(set(marked))
        updated = []
        for old_edges, old_degrees, old_triangles in current:
            for edges, degrees, triangles in line_options(marked):
                if old_edges + edges > max_edges:
                    continue
                new_degrees = dict(old_degrees)
                for vertex, degree in zip(marked, degrees):
                    new_degrees[(line, vertex)] = degree
                updated.append(
                    (old_edges + edges, new_degrees, old_triangles + triangles)
                )
        current = updated

    compressed = {}
    for edges, degree_map, triangles in current:
        degrees = tuple(
            degree_map[(row, column)]
            if row_side
            else degree_map[(column, row)]
            for row, column in square_cells
        )
        key = (edges, degrees)
        compressed[key] = max(compressed.get(key, -1), triangles)

    # Unmarked line graphs only affect the triangle count.  With at most nine
    # edges, the envelope TAU is already attainable in one unmarked K_5.
    augmented = {}
    for (edges, degrees), triangles in compressed.items():
        for extra in range(max_edges + 1 - edges):
            key = (edges + extra, degrees)
            value = triangles + TAU[extra]
            augmented[key] = max(augmented.get(key, -1), value)
    return [
        (edges, degrees, triangles)
        for (edges, degrees), triangles in augmented.items()
    ]


def small_square_table(square_cells, total_dimension=9):
    square_count = len(square_cells)
    edge_budget = total_dimension - square_count
    row_options = side_options(square_cells, True, edge_budget)
    column_options = side_options(square_cells, False, edge_budget)
    by_split = {}
    for row_edges, row_degrees, row_triangles in row_options:
        for column_edges, column_degrees, column_triangles in column_options:
            if row_edges + column_edges != edge_budget:
                continue
            value = 5 * (row_triangles + column_triangles) + sum(
                (row_degree + 1) * (column_degree + 1)
                for row_degree, column_degree in zip(row_degrees, column_degrees)
            )
            key = (row_edges, column_edges)
            by_split[key] = max(by_split.get(key, -1), value)
    return by_split


def relaxed_square_term(square_count, row_edges, column_edges):
    """Upper-bound the square term from degree sums and individual caps."""
    row_sum_cap = 2 * row_edges
    column_sum_cap = 2 * column_edges
    states = {(0, 0): 0}
    for _ in range(square_count):
        updated = {}
        for (row_sum, column_sum), value in states.items():
            for row_degree in range(min(4, row_edges) + 1):
                for column_degree in range(min(4, column_edges) + 1):
                    new_row_sum = row_sum + row_degree
                    new_column_sum = column_sum + column_degree
                    if new_row_sum > row_sum_cap or new_column_sum > column_sum_cap:
                        continue
                    key = (new_row_sum, new_column_sum)
                    new_value = value + (row_degree + 1) * (column_degree + 1)
                    updated[key] = max(updated.get(key, -1), new_value)
        states = updated
    return max(states.values())


def square_pattern_canonical(cells):
    """Canonical small bipartite graph, allowing row/column transpose."""
    active_rows = sorted({row for row, _column in cells})
    active_columns = sorted({column for _row, column in cells})
    edges = {
        (active_rows.index(row), active_columns.index(column))
        for row, column in cells
    }
    row_count = len(active_rows)
    column_count = len(active_columns)
    images = []
    for row_perm in permutations(range(row_count)):
        for column_perm in permutations(range(column_count)):
            images.append(
                tuple(sorted((row_perm[row], column_perm[column]) for row, column in edges))
            )
    for row_perm in permutations(range(column_count)):
        for column_perm in permutations(range(row_count)):
            images.append(
                tuple(sorted((row_perm[column], column_perm[row]) for row, column in edges))
            )
    return min(images)


def main():
    assert TAU == [0, 0, 0, 1, 1, 2, 4, 4, 5, 7, 10, 10]
    patterns = {
        "s1": [(0, 0)],
        "s2_adjacent": [(0, 0), (0, 1)],
        "s2_matching": [(0, 0), (1, 1)],
        "s3_star": [(0, 0), (0, 1), (0, 2)],
        "s3_path": [(0, 0), (0, 1), (1, 1)],
        "s3_matching": [(0, 0), (1, 1), (2, 2)],
        "s3_adjacent_plus_isolated": [(0, 0), (0, 1), (1, 2)],
    }
    expected_maxima = {
        "s1": 32,
        "s2_adjacent": 32,
        "s2_matching": 29,
        "s3_star": 32,
        "s3_path": 29,
        "s3_matching": 26,
        "s3_adjacent_plus_isolated": 29,
    }
    print("tau =", TAU)
    for name, cells in patterns.items():
        table = small_square_table(cells)
        maximum = max(table.values())
        assert maximum == expected_maxima[name]
        print(name, "max =", maximum, "splits =", sorted(table.items()))

    relaxed_maxima = {}
    for square_count in range(4, 10):
        bounds = []
        for row_edges in range(10 - square_count):
            column_edges = 9 - square_count - row_edges
            square_bound = relaxed_square_term(
                square_count, row_edges, column_edges
            )
            total_bound = (
                5 * (TAU[row_edges] + TAU[column_edges]) + square_bound
            )
            bounds.append(((row_edges, column_edges), total_bound))
        relaxed_maxima[square_count] = max(value for _, value in bounds)
        print("s =", square_count, "bounds =", bounds)
    assert relaxed_maxima == {4: 31, 5: 24, 6: 17, 7: 13, 8: 10, 9: 9}

    expected_ten_dimensional = {
        "s1": 40,
        "s2_adjacent": 36,
        "s2_matching": 33,
        "s3_star": 36,
        "s3_path": 34,
        "s3_matching": 30,
        "s3_adjacent_plus_isolated": 33,
    }
    ten_dimensional_small = {
        name: max(small_square_table(cells, total_dimension=10).values())
        for name, cells in patterns.items()
    }
    assert ten_dimensional_small == expected_ten_dimensional

    ten_dimensional_relaxed = {}
    for square_count in range(4, 11):
        bounds = []
        for row_edges in range(11 - square_count):
            column_edges = 10 - square_count - row_edges
            square_bound = relaxed_square_term(
                square_count, row_edges, column_edges
            )
            bounds.append(
                5 * (TAU[row_edges] + TAU[column_edges]) + square_bound
            )
        ten_dimensional_relaxed[square_count] = max(bounds)
    assert ten_dimensional_relaxed == {
        4: 44,
        5: 32,
        6: 25,
        7: 18,
        8: 14,
        9: 11,
        10: 10,
    }

    eleven_dimensional_small = {
        name: max(small_square_table(cells, total_dimension=11).values())
        for name, cells in patterns.items()
    }
    assert eleven_dimensional_small == {
        "s1": 55,
        "s2_adjacent": 45,
        "s2_matching": 41,
        "s3_star": 40,
        "s3_path": 38,
        "s3_matching": 34,
        "s3_adjacent_plus_isolated": 37,
    }
    eleven_dimensional_relaxed = {}
    for square_count in range(4, 12):
        bounds = []
        for row_edges in range(12 - square_count):
            column_edges = 11 - square_count - row_edges
            square_bound = relaxed_square_term(
                square_count, row_edges, column_edges
            )
            bounds.append(
                5 * (TAU[row_edges] + TAU[column_edges]) + square_bound
            )
        eleven_dimensional_relaxed[square_count] = max(bounds)
    assert eleven_dimensional_relaxed == {
        4: 52,
        5: 45,
        6: 33,
        7: 26,
        8: 19,
        9: 15,
        10: 12,
        11: 11,
    }

    # At d=12 the relaxed four-square degree bound 62 is spurious.  There
    # are only ten row/column/transpose isomorphism types of four cells, and
    # their exact maxima are all at most 44.
    four_square_orbits = {}
    for cells in combinations(
        [(row, column) for row in range(5) for column in range(5)], 4
    ):
        four_square_orbits.setdefault(square_pattern_canonical(cells), cells)
    assert len(four_square_orbits) == 10
    four_square_maxima = sorted(
        max(small_square_table(cells, total_dimension=12).values())
        for cells in four_square_orbits.values()
    )
    assert four_square_maxima == [35, 38, 38, 38, 39, 40, 40, 41, 42, 44]

    twelve_dimensional_small = {
        name: max(small_square_table(cells, total_dimension=12).values())
        for name, cells in patterns.items()
    }
    assert twelve_dimensional_small == {
        "s1": 60,
        "s2_adjacent": 60,
        "s2_matching": 56,
        "s3_star": 50,
        "s3_path": 46,
        "s3_matching": 42,
        "s3_adjacent_plus_isolated": 46,
    }
    twelve_dimensional_relaxed_s5_plus = {}
    for square_count in range(5, 13):
        bounds = []
        for row_edges in range(13 - square_count):
            column_edges = 12 - square_count - row_edges
            bounds.append(
                5 * (TAU[row_edges] + TAU[column_edges])
                + relaxed_square_term(square_count, row_edges, column_edges)
            )
        twelve_dimensional_relaxed_s5_plus[square_count] = max(bounds)
    assert twelve_dimensional_relaxed_s5_plus == {
        5: 53,
        6: 46,
        7: 34,
        8: 27,
        9: 20,
        10: 16,
        11: 13,
        12: 12,
    }
    print("NO_CROSSING_P9_UPPER = 35")
    print("NO_CROSSING_EQUALITY_COUNT = 100")
    print("NO_CROSSING_P10_UPPER = 50")
    print("NO_CROSSING_P10_EQUALITY_COUNT = 10")
    print("NO_CROSSING_P11_UPPER = 55")
    print("NO_CROSSING_P12_UPPER = 60")
    print("STATUS = PASS")


if __name__ == "__main__":
    main()
