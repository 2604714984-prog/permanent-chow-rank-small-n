"""Exact structural diagnostic for the one-step equality witness graphs.

This script asks whether the 342 printed spanning-forest edges conceal only a
few abstract graph shapes.  It reconstructs the full pairwise-equality graph
from the local Boolean shadow formula, computes elementary graph invariants,
and groups directions by those invariants.  The result is a research
diagnostic, not a proof of graph isomorphism or of the witness implications.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import perm5_flag_shifted_stability_verify as base


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "n5_witness_graph_structure_exact.json"


def full_candidate_graph(
    family: int,
    plane: int,
    axis: int,
    low: int,
    high: int,
    fixed_family: int,
    movable_family: tuple[tuple[int, int], ...],
    fixed_plane: int,
    movable_plane: tuple[tuple[int, int], ...],
):
    variable_count = len(movable_family) + len(movable_plane)
    target_visible = base.visible_mask(family, plane)
    child_pairs = base.shadow_reflection_pairs(axis, low, high)
    high_of_low = dict(child_pairs)
    low_of_high = {
        high_child: low_child for low_child, high_child in child_pairs
    }
    witnesses_by_edge = defaultdict(set)

    for witness in range(100):
        if (target_visible >> witness) & 1:
            continue
        if witness in high_of_low:
            children = (witness, high_of_low[witness])
            operation = "or"
        elif witness in low_of_high:
            children = (low_of_high[witness], witness)
            operation = "and"
        else:
            children = (witness,)
            operation = "identity"

        support = sorted(set().union(*(
            base.visible_child_support(
                child,
                fixed_family,
                movable_family,
                fixed_plane,
                movable_plane,
            )
            for child in children
        )))
        zero_assignments = []
        for local_assignment in range(1 << len(support)):
            assignment = sum(
                ((local_assignment >> local_index) & 1) << global_index
                for local_index, global_index in enumerate(support)
            )
            values = tuple(
                base.visible_child_value(
                    child,
                    assignment,
                    fixed_family,
                    movable_family,
                    fixed_plane,
                    movable_plane,
                )
                for child in children
            )
            extra = (
                any(values)
                if operation == "or"
                else all(values)
                if operation == "and"
                else values[0]
            )
            if not extra:
                zero_assignments.append(assignment)

        for right_index, right in enumerate(support):
            for left in support[:right_index]:
                if all(
                    not ((assignment >> left) ^ (assignment >> right)) & 1
                    for assignment in zero_assignments
                ):
                    witnesses_by_edge[(left, right)].add(witness)

    return variable_count, witnesses_by_edge


def graph_components(vertex_count: int, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    components = []
    unseen = set(range(vertex_count))
    while unseen:
        start = min(unseen)
        component = {start}
        queue = [start]
        unseen.remove(start)
        while queue:
            vertex = queue.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(tuple(sorted(component)))
    return adjacency, tuple(components)


def component_diameter(adjacency, component):
    maximum = 0
    for start in component:
        distance = {start: 0}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor in component and neighbor not in distance:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        assert len(distance) == len(component)
        maximum = max(maximum, max(distance.values(), default=0))
    return maximum


def component_count_without(adjacency, removed):
    vertices = set(range(len(adjacency))) - {removed}
    count = 0
    while vertices:
        count += 1
        stack = [vertices.pop()]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in vertices:
                    vertices.remove(neighbor)
                    stack.append(neighbor)
    return count


def graph_record(vertex_count, witnesses_by_edge, family_variable_count):
    edges = tuple(sorted(witnesses_by_edge))
    adjacency, components = graph_components(vertex_count, edges)
    degrees = tuple(sorted(len(neighbors) for neighbors in adjacency))
    component_sizes = tuple(sorted(map(len, components)))
    diameters = tuple(sorted(
        component_diameter(adjacency, set(component)) for component in components
    ))
    articulation_count = sum(
        component_count_without(adjacency, vertex)
        > len(components)
        for vertex in range(vertex_count)
    )
    component_type_counts = tuple(sorted(
        (
            sum(vertex < family_variable_count for vertex in component),
            sum(vertex >= family_variable_count for vertex in component),
        )
        for component in components
    ))
    witness_multiplicities = Counter(
        witness
        for witnesses in witnesses_by_edge.values()
        for witness in witnesses
    )
    signature = (
        vertex_count,
        len(edges),
        degrees,
        component_sizes,
        diameters,
        articulation_count,
        component_type_counts,
        tuple(sorted(witness_multiplicities.values())),
    )
    return {
        "vertex_count": vertex_count,
        "family_vertex_count": family_variable_count,
        "plane_vertex_count": vertex_count - family_variable_count,
        "edge_count": len(edges),
        "degree_sequence": list(degrees),
        "component_sizes": list(component_sizes),
        "component_diameters": list(diameters),
        "articulation_vertex_count": articulation_count,
        "component_family_plane_counts": [
            list(value) for value in component_type_counts
        ],
        "distinct_witness_count": len(witness_multiplicities),
        "witness_edge_multiplicities": list(sorted(
            witness_multiplicities.values()
        )),
        "signature": repr(signature),
    }


def direction_records(name, shape, l_partition, use_full_shadow=False):
    family = base.family_from_shape(shape)
    plane = base.plane_from_partition(l_partition)
    records = []
    for axis in (0, 1):
        for low in range(5):
            for high in range(5):
                if low == high:
                    continue
                family_pairs, plane_pairs = base.reflection_pairs(
                    axis, low, high
                )
                family_data = base.preimage_data(family, family_pairs)
                plane_data = base.preimage_data(plane, plane_pairs)
                if family_data is None or plane_data is None:
                    continue
                fixed_family, movable_family = family_data
                fixed_plane, movable_plane = plane_data
                if use_full_shadow:
                    analysis_plane = 0
                    analysis_fixed_plane = 0
                    analysis_movable_plane = ()
                else:
                    analysis_plane = plane
                    analysis_fixed_plane = fixed_plane
                    analysis_movable_plane = movable_plane
                width, graph = full_candidate_graph(
                    family,
                    analysis_plane,
                    axis,
                    low,
                    high,
                    fixed_family,
                    movable_family,
                    analysis_fixed_plane,
                    analysis_movable_plane,
                )
                if width <= 1:
                    continue
                record = graph_record(
                    width, graph, len(movable_family)
                )
                record["direction"] = (
                    f"{'row' if axis == 0 else 'column'}:{low}<-{high}"
                )
                records.append(record)
    return records


def summarize(records):
    groups = defaultdict(list)
    for record in records:
        groups[record["signature"]].append(record["direction"])
    return {
        "nontrivial_direction_count": len(records),
        "coarse_signature_count": len(groups),
        "groups": [
            {
                "size": len(directions),
                "directions": directions,
                "representative_record": next(
                    record for record in records
                    if record["direction"] == directions[0]
                ),
            }
            for _signature, directions in sorted(
                groups.items(), key=lambda item: (len(item[1]), item[1])
            )
        ],
    }


def main():
    orbit0 = direction_records("orbit0", (10, 10), (5,), True)
    orbit1 = direction_records("orbit1", (10, 4, 4, 2), (4, 1))
    orbit13 = direction_records("orbit13", (7, 5, 4, 4), (3, 2))
    result = {
        "status": "PASS_EXACT_INTEGER_WITNESS_GRAPH_STRUCTURE_DIAGNOSTIC",
        "evidence_role": (
            "research diagnostic only; coarse graph signatures neither prove "
            "isomorphism nor replace the printed witness implications"
        ),
        "orbits": {
            "orbit0": summarize(orbit0),
            "orbit1": summarize(orbit1),
            "orbit13": summarize(orbit13),
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "summary": {
            name: {
                "directions": data["nontrivial_direction_count"],
                "coarse_signatures": data["coarse_signature_count"],
            }
            for name, data in result["orbits"].items()
        },
    }, indent=2))


if __name__ == "__main__":
    main()
