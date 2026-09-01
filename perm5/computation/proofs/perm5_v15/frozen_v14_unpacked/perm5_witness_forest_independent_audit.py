"""Independent exact audit of the printed one-step witness forests.

This file deliberately does not import ``perm5_flag_shifted_stability_verify``.
It treats the two Markdown appendices as the certificate, reconstructs every
parent relation from the definitions, and checks each printed edge directly.
All calculations are Boolean/integer calculations over the sets of triples and
pairs on {0,1,2,3,4}; no finite-field or floating-point rank is used.
"""

from __future__ import annotations

import hashlib
import json
import re
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCAL_CERT = ROOT / "n5_flag_local_witness_forests_20260810.md"
ORBIT0_CERT = ROOT / "n5_flag_orbit0_full_shadow_witness_forests_20260810.md"
OUTPUT = ROOT / "n5_witness_forest_independent_audit_exact.json"

TRIPLES = tuple(combinations(range(5), 3))
PAIRS = tuple(combinations(range(5), 2))
TI = {value: index for index, value in enumerate(TRIPLES)}
PI = {value: index for index, value in enumerate(PAIRS)}
INITIAL_ORDER = (0, 1, 3, 6, 2, 4, 7, 5, 8, 9)


def bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


# A parent position is (row triple, column triple), encoded in 0,...,99.
# Differentiating by its missing matrix variable gives a child position
# (row pair, column pair), again encoded in 0,...,99.
PARENTS: list[list[tuple[int, int]]] = [[] for _ in range(100)]
PARENT_SHADOW: list[int] = [0] * 100
for ri, rows in enumerate(TRIPLES):
    for ci, columns in enumerate(TRIPLES):
        parent = 10 * ri + ci
        for row_pair in combinations(rows, 2):
            missing_row = next(x for x in rows if x not in row_pair)
            for column_pair in combinations(columns, 2):
                missing_column = next(x for x in columns if x not in column_pair)
                child = 10 * PI[row_pair] + PI[column_pair]
                variable = 5 * missing_row + missing_column
                PARENTS[child].append((parent, variable))
                PARENT_SHADOW[parent] |= 1 << child
assert all(len(values) == 9 for values in PARENTS)
assert all(value.bit_count() == 9 for value in PARENT_SHADOW)


def family_from_shape(shape: tuple[int, ...]) -> int:
    result = 0
    for row_index, length in zip(INITIAL_ORDER, shape):
        for column_index in INITIAL_ORDER[:length]:
            result |= 1 << (10 * row_index + column_index)
    return result


def plane_from_partition(partition: tuple[int, ...]) -> int:
    result = 0
    for row, length in enumerate(partition):
        for column in range(length):
            result |= 1 << (5 * row + column)
    return result


TARGETS = {
    "orbit0": (family_from_shape((10, 10)), 0),
    "orbit1": (family_from_shape((10, 4, 4, 2)), plane_from_partition((4, 1))),
    "orbit13": (family_from_shape((7, 5, 4, 4)), plane_from_partition((3, 2))),
}


def reflection_pairs(kind: str, low: int, high: int, degree: int):
    """Pairs (low position, high position) for a ground-set shift."""
    base = TRIPLES if degree == 3 else PAIRS if degree == 2 else range(5)
    index = TI if degree == 3 else PI if degree == 2 else {i: i for i in range(5)}
    width = 10 if degree in (2, 3) else 5
    result = []
    if degree in (2, 3):
        for high_set in base:
            if high not in high_set or low in high_set:
                continue
            low_set = tuple(sorted((set(high_set) - {high}) | {low}))
            for other in range(width):
                if kind == "row":
                    result.append((width * index[low_set] + other,
                                   width * index[high_set] + other))
                else:
                    result.append((width * other + index[low_set],
                                   width * other + index[high_set]))
    else:
        for other in range(5):
            result.append((5 * low + other, 5 * high + other) if kind == "row"
                          else (5 * other + low, 5 * other + high))
    return tuple(result)


def preimage(target: int, pairs_: tuple[tuple[int, int], ...]):
    # A shifted target cannot contain high without low.
    if any((target >> high) & 1 and not ((target >> low) & 1)
           for low, high in pairs_):
        return None
    movable = tuple((low, high) for low, high in pairs_
                    if (target >> low) & 1 and not ((target >> high) & 1))
    fixed = target
    for low, _ in movable:
        fixed &= ~(1 << low)
    return fixed, movable


def oriented(fixed: int, movable: tuple[tuple[int, int], ...], assignment: int):
    result = fixed
    for i, (low, high) in enumerate(movable):
        result |= 1 << (high if (assignment >> i) & 1 else low)
    return result


def full_shadow(family: int) -> int:
    result = 0
    for parent in bits(family):
        result |= PARENT_SHADOW[parent]
    return result


def visible(child: int, family: int, plane: int) -> bool:
    return any((family >> parent) & 1 and not ((plane >> variable) & 1)
               for parent, variable in PARENTS[child])


def visible_mask(family: int, plane: int) -> int:
    return sum((1 << child) for child in range(100)
               if visible(child, family, plane))


def parse_variables(line: str, letter: str):
    if line.endswith("none"):
        return ()
    entries = re.findall(rf"{letter} (\d+)=\[(\d+),(\d+)\]", line)
    assert entries
    parsed = tuple((int(i), int(low), int(high)) for i, low, high in entries)
    assert tuple(i for i, _, _ in parsed) == tuple(range(parsed[0][0], parsed[0][0] + len(parsed)))
    return parsed


def parse_components(line: str):
    result = []
    for body in re.findall(r"\[([^]]*)\]", line):
        if body.strip():
            result.append(tuple(int(value) for value in body.split(",")))
    return tuple(result)


def parse_records(path: Path, orbit0: bool = False):
    text = path.read_text(encoding="utf-8")
    records = []
    if orbit0:
        orbit_chunks = [("orbit0", text)]
    else:
        matches = list(re.finditer(r"^## (orbit(?:1|13))\s*$", text, re.M))
        orbit_chunks = []
        for i, match in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            orbit_chunks.append((match.group(1), text[match.end():end]))
    for orbit, orbit_text in orbit_chunks:
        headings = list(re.finditer(r"^#{2,3} (row|column):(\d)<-(\d)\s*$", orbit_text, re.M))
        for i, heading in enumerate(headings):
            end = headings[i + 1].start() if i + 1 < len(headings) else len(orbit_text)
            body = orbit_text[heading.end():end]
            s_line = re.search(r"^S-vars:.*$", body, re.M).group(0)
            l_match = re.search(r"^L-vars:.*$", body, re.M)
            c_line = re.search(r"^Components:.*$", body, re.M).group(0)
            forest_body = re.search(r"Witness forest:\s*```text\s*(.*?)```", body, re.S).group(1)
            edges = []
            for line in forest_body.splitlines():
                if not line.strip():
                    continue
                match = re.fullmatch(r"(\d+) (\d+) (\d+)=\((\d)(\d);(\d)(\d)\)", line.strip())
                assert match, (path.name, line)
                edges.append(tuple(map(int, match.groups())))
            records.append({
                "orbit": orbit,
                "kind": heading.group(1),
                "low": int(heading.group(2)),
                "high": int(heading.group(3)),
                "s": parse_variables(s_line, "S"),
                "l": parse_variables(l_match.group(0), "L") if l_match else (),
                "components": parse_components(c_line),
                "edges": tuple(edges),
            })
    return records


def literal_variable(position: int, fixed: int,
                     movable: tuple[tuple[int, int], ...], offset: int):
    if (fixed >> position) & 1:
        return None
    for i, (low, high) in enumerate(movable):
        if position == low or position == high:
            return offset + i
    return None


def local_support(children: tuple[int, ...], fixed_family: int,
                  movable_family: tuple[tuple[int, int], ...], fixed_plane: int,
                  movable_plane: tuple[tuple[int, int], ...]):
    result = set()
    for child in children:
        for parent, variable in PARENTS[child]:
            a = literal_variable(parent, fixed_family, movable_family, 0)
            b = literal_variable(variable, fixed_plane, movable_plane,
                                 len(movable_family))
            if a is not None:
                result.add(a)
            if b is not None:
                result.add(b)
    return tuple(sorted(result))


def source_masks(assignment: int, fixed_family: int,
                 movable_family: tuple[tuple[int, int], ...], fixed_plane: int,
                 movable_plane: tuple[tuple[int, int], ...]):
    family_width = len(movable_family)
    family_assignment = assignment & ((1 << family_width) - 1)
    plane_assignment = assignment >> family_width
    return (oriented(fixed_family, movable_family, family_assignment),
            oriented(fixed_plane, movable_plane, plane_assignment))


def compressed_visible_at(child: int, family: int, plane: int, kind: str,
                          low: int, high: int):
    pairs_ = reflection_pairs(kind, low, high, 2)
    high_of_low = dict(pairs_)
    low_of_high = {b: a for a, b in pairs_}
    if child in high_of_low:
        return visible(child, family, plane) or visible(high_of_low[child], family, plane)
    if child in low_of_high:
        return visible(low_of_high[child], family, plane) and visible(child, family, plane)
    return visible(child, family, plane)


def forest_components(vertex_count: int, edges: tuple[tuple[int, int], ...]):
    parent = list(range(vertex_count))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "printed graph is not a forest"
        parent[rb] = ra
    groups: dict[int, list[int]] = {}
    for vertex in range(vertex_count):
        groups.setdefault(find(vertex), []).append(vertex)
    return tuple(sorted((tuple(group) for group in groups.values()), key=lambda x: x[0]))


def direction_key(record):
    return record["kind"], record["low"], record["high"]


def all_valid_directions(orbit: str, require_movable: bool):
    family, plane = TARGETS[orbit]
    result = set()
    for kind in ("row", "column"):
        for low in range(5):
            for high in range(5):
                if low == high:
                    continue
                f = preimage(family, reflection_pairs(kind, low, high, 3))
                p = preimage(plane, reflection_pairs(kind, low, high, 1))
                if f is None or p is None:
                    continue
                if require_movable and not f[1]:
                    continue
                result.add((kind, low, high))
    return result


def audit_record(record):
    orbit = record["orbit"]
    family, plane = TARGETS[orbit]
    kind, low, high = direction_key(record)
    family_data = preimage(family, reflection_pairs(kind, low, high, 3))
    plane_data = preimage(plane, reflection_pairs(kind, low, high, 1))
    assert family_data is not None and plane_data is not None
    fixed_family, movable_family = family_data
    fixed_plane, movable_plane = plane_data

    printed_s = tuple((low_, high_) for _, low_, high_ in record["s"])
    printed_l = tuple((low_, high_) for _, low_, high_ in record["l"])
    assert printed_s == movable_family
    if orbit == "orbit0":
        assert not printed_l
        fixed_plane, movable_plane = 0, ()
    else:
        assert printed_l == movable_plane
    width = len(movable_family) + len(movable_plane)
    assert tuple(i for i, _, _ in record["s"]) == tuple(range(len(movable_family)))
    assert tuple(i for i, _, _ in record["l"]) == tuple(range(len(movable_family), width))

    target_visible = visible_mask(family, plane if orbit != "orbit0" else 0)
    checked_assignments = 0
    simple_edges = []
    for a, b, child, r0, r1, c0, c1 in record["edges"]:
        assert 0 <= a < width and 0 <= b < width and a != b
        assert child == 10 * PI[(r0, r1)] + PI[(c0, c1)]
        assert not ((target_visible >> child) & 1)
        child_pairs = reflection_pairs(kind, low, high, 2)
        high_of_low = dict(child_pairs)
        low_of_high = {v: u for u, v in child_pairs}
        if child in high_of_low:
            children = (child, high_of_low[child])
        elif child in low_of_high:
            children = (low_of_high[child], child)
        else:
            children = (child,)
        support = set(local_support(children, fixed_family, movable_family,
                                    fixed_plane, movable_plane))
        support.update((a, b))
        support = tuple(sorted(support))
        other = tuple(v for v in support if v not in (a, b))
        for endpoint_a, endpoint_b in ((0, 1), (1, 0)):
            for local in range(1 << len(other)):
                assignment = (endpoint_a << a) | (endpoint_b << b)
                for i, variable in enumerate(other):
                    assignment |= ((local >> i) & 1) << variable
                source_family, source_plane = source_masks(
                    assignment, fixed_family, movable_family,
                    fixed_plane, movable_plane)
                assert compressed_visible_at(child, source_family, source_plane,
                                             kind, low, high)
                checked_assignments += 1
        simple_edges.append((a, b))

    actual_components = forest_components(width, tuple(simple_edges))
    assert actual_components == record["components"]
    return {
        "orbit": orbit,
        "direction": f"{kind}:{low}<-{high}",
        "variables": width,
        "edges": len(simple_edges),
        "local_boolean_assignments_checked": checked_assignments,
        "components": [list(component) for component in actual_components],
        "fixed_family": fixed_family,
        "movable_family": movable_family,
        "fixed_plane": fixed_plane,
        "movable_plane": movable_plane,
    }


def exceptional_shadow_check(audited):
    expected = {
        ("orbit1", "row:2<-3"): 54,
        ("orbit1", "row:3<-4"): 58,
        ("orbit13", "row:2<-3"): 51,
        ("orbit13", "column:3<-4"): 53,
    }
    actual = {}
    for item in audited:
        if len(item["components"]) != 2:
            continue
        width = item["variables"]
        values = []
        visible_values = []
        for component_bits in ((0, 1), (1, 0)):
            assignment = 0
            for bit, component in zip(component_bits, item["components"]):
                for variable in component:
                    assignment |= bit << variable
            family, plane = source_masks(
                assignment, item["fixed_family"], item["movable_family"],
                item["fixed_plane"], item["movable_plane"])
            values.append(full_shadow(family).bit_count())
            visible_values.append(visible_mask(family, plane).bit_count())
        key = (item["orbit"], item["direction"])
        assert key in expected
        assert values == [expected[key], expected[key]]
        actual[f"{key[0]}:{key[1]}"] = {
            "mixed_component_full_shadows": values,
            "mixed_component_visible_shadows": visible_values,
            "uniform_endpoint_count": 2,
            "variable_count": width,
        }
    assert set(actual) == {f"{orbit}:{direction}" for orbit, direction in expected}
    return actual


def main():
    records = parse_records(LOCAL_CERT) + parse_records(ORBIT0_CERT, orbit0=True)
    by_orbit = {name: [record for record in records if record["orbit"] == name]
                for name in TARGETS}
    assert len(by_orbit["orbit1"]) == 21
    assert len(by_orbit["orbit13"]) == 21
    assert len(by_orbit["orbit0"]) == 8
    assert {direction_key(record) for record in by_orbit["orbit1"]} == all_valid_directions("orbit1", False)
    assert {direction_key(record) for record in by_orbit["orbit13"]} == all_valid_directions("orbit13", False)
    assert {direction_key(record) for record in by_orbit["orbit0"]} == all_valid_directions("orbit0", True)

    audited = [audit_record(record) for record in records]
    exceptions = exceptional_shadow_check(audited)
    compact = [{key: value for key, value in item.items()
                if key not in {"fixed_family", "movable_family", "fixed_plane", "movable_plane"}}
               for item in audited]
    result = {
        "status": "PASS_EXACT_INTEGER_INDEPENDENT_WITNESS_FOREST_AUDIT",
        "proof_dependency": False,
        "imports_original_generator": False,
        "certificate_files": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest().upper()
            for path in (LOCAL_CERT, ORBIT0_CERT)
        },
        "record_counts": {orbit: len(values) for orbit, values in by_orbit.items()},
        "edge_count": sum(item["edges"] for item in audited),
        "local_boolean_assignments_checked": sum(
            item["local_boolean_assignments_checked"] for item in audited),
        "exceptional_two_component_checks": exceptions,
        "records": compact,
        "script_sha256_before_output": hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper(),
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in (
        "status", "record_counts", "edge_count",
        "local_boolean_assignments_checked", "exceptional_two_component_checks")}, indent=2))


if __name__ == "__main__":
    main()
