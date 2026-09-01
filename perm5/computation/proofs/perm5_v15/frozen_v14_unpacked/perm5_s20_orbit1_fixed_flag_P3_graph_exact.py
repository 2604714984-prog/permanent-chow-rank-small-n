r"""Unit-coefficient graph proof of the hard fixed-flag P3 tangent lemma.

For each of the four maximal coordinate L5 witnesses, the linearized
equations for

    A_Z(S0) contained in L

have at most two nonzero coefficients, all equal to +/-1.  Regard a
two-term equation as an edge between parameter vertices and a one-term
equation as an anchor forcing its vertex to zero.  The kernel dimension is
then the number of connected components containing no anchor.

This script performs only exact integer bookkeeping.  It proves that there
are precisely three unanchored components, lists them, and thereby replaces
the 417-rank statement by a transparent graph-elimination certificate.
"""

from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "n5_fixed_five_shadow_s20_le50_annihilator_classification_exact.json"
OUTPUT = ROOT / "n5_s20_orbit1_fixed_flag_P3_graph_integer_exact.json"


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, first: int, second: int) -> None:
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root != second_root:
            self.parent[second_root] = first_root


def parameter_record(parameter: tuple[str, int, int]) -> dict[str, object]:
    kind, source, target = parameter
    if kind == "L":
        return {
            "kind": "L_graph",
            "source_variable": source,
            "target_variable": target,
        }
    return {
        "kind": "Z_graph",
        "source_annihilator": source,
        "target_shadow_coordinate": target,
    }


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    orbit = next(
        record for record in source["orbit_records"]
        if record["orbit_index"] == 1
    )
    family = orbit["representative_family_positions"]
    shadow = orbit["representative_shadow_positions"]
    witnesses = orbit["maximum_witnesses_first_20"]

    triples = list(combinations(range(5), 3))
    pairs = list(combinations(range(5), 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    derivative: dict[int, dict[int, int]] = {}
    for position in family:
        rows = triples[position // 10]
        columns = triples[position % 10]
        record = {}
        for row_pair in combinations(rows, 2):
            missing_row = next(row for row in rows if row not in row_pair)
            for column_pair in combinations(columns, 2):
                missing_column = next(
                    column for column in columns if column not in column_pair
                )
                child = 10 * pair_index[row_pair] + pair_index[column_pair]
                record[child] = 5 * missing_row + missing_column
        assert len(record) == 9
        derivative[position] = record

    records = []
    for witness_index, plane in enumerate(witnesses):
        plane_set = set(plane)
        outside = [variable for variable in range(25) if variable not in plane_set]
        z_basis = [
            child
            for child in shadow
            if all(
                derivative[position].get(child) in plane_set
                for position in family
                if child in derivative[position]
            )
        ]
        assert len(z_basis) == 8
        z_complement = [child for child in shadow if child not in z_basis]

        parameters = (
            [("L", source_variable, target_variable)
             for source_variable in plane for target_variable in outside]
            + [("Z", alpha, beta)
               for alpha in z_basis for beta in z_complement]
        )
        assert len(parameters) == 420
        parameter_index = {
            parameter: index for index, parameter in enumerate(parameters)
        }
        graph = UnionFind(len(parameters))
        anchored_vertices: set[int] = set()
        one_term_equations = 0
        two_term_equations = 0

        for alpha in z_basis:
            for position in family:
                base_variable = derivative[position].get(alpha)
                for target_variable in outside:
                    support = []
                    if base_variable is not None:
                        support.append(parameter_index[
                            ("L", base_variable, target_variable)
                        ])
                    for beta in z_complement:
                        if derivative[position].get(beta) == target_variable:
                            support.append(parameter_index[("Z", alpha, beta)])
                    support = list(dict.fromkeys(support))
                    assert len(support) <= 2
                    if len(support) == 1:
                        one_term_equations += 1
                        anchored_vertices.add(support[0])
                    elif len(support) == 2:
                        two_term_equations += 1
                        graph.union(support[0], support[1])

        components: dict[int, list[int]] = {}
        for vertex in range(len(parameters)):
            components.setdefault(graph.find(vertex), []).append(vertex)
        anchored_roots = {graph.find(vertex) for vertex in anchored_vertices}
        unanchored_components = [
            components[root]
            for root in components
            if root not in anchored_roots
        ]
        unanchored_parameter_components = [
            [parameter_record(parameters[vertex]) for vertex in component]
            for component in unanchored_components
        ]

        expected_targets = sorted(
            set().union(*(set(other) for other in witnesses)) - plane_set
        )
        assert len(expected_targets) == 3
        assert len(unanchored_components) == 3
        assert sorted(
            next(
                item["target_variable"]
                for item in component
                if item["kind"] == "L_graph"
            )
            for component in unanchored_parameter_components
        ) == expected_targets
        assert all(len(component) == 3 for component in unanchored_components)
        assert all(
            sum(item["kind"] == "L_graph" for item in component) == 1
            and sum(item["kind"] == "Z_graph" for item in component) == 2
            for component in unanchored_parameter_components
        )

        records.append({
            "witness_index": witness_index,
            "coordinate_plane": plane,
            "annihilator_basis": z_basis,
            "parameter_vertices": len(parameters),
            "one_term_anchor_equations": one_term_equations,
            "distinct_anchored_vertices": len(anchored_vertices),
            "two_term_edge_equations": two_term_equations,
            "graph_connected_components": len(components),
            "unanchored_component_count": len(unanchored_components),
            "kernel_dimension_over_every_field": len(unanchored_components),
            "unanchored_parameter_components": unanchored_parameter_components,
        })

    result = {
        "status": "PASS_EXACT_INTEGER_FIXED_FLAG_P3_GRAPH",
        "claim_type": (
            "unit-coefficient graph elimination for the fixed hard-flag "
            "annihilator tangent equations"
        ),
        "orbit_index": 1,
        "records": records,
        "all_four_kernel_dimensions_equal_three_over_every_field": True,
        "all_four_kernels_are_exactly_the_P3_line_motions": True,
        "proof_rule": (
            "two-term equations identify graph vertices up to sign; one-term "
            "equations anchor a component to zero; each unanchored component "
            "contributes one kernel parameter"
        ),
        "strict_scope": (
            "This is the exact tangent-space upper bound. The separate explicit "
            "P3 family supplies the matching smooth three-dimensional lower "
            "bound needed to identify the local incidence germ."
        ),
        "input_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper(),
        "script_sha256_before_output": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest().upper(),
    }
    OUTPUT.write_bytes((json.dumps(result, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({
        "status": result["status"],
        "kernel_dimensions": [
            record["kernel_dimension_over_every_field"] for record in records
        ],
        "unanchored_components_witness_0": (
            records[0]["unanchored_parameter_components"]
        ),
        "output": OUTPUT.name,
    }, indent=2))


if __name__ == "__main__":
    main()
