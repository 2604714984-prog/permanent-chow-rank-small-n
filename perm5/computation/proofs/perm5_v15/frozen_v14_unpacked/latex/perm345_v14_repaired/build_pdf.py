#!/usr/bin/env python3
"""Build the v14 AMS paper and embed the exact reviewer-reproduction sources."""

from pathlib import Path
import hashlib
import json
import subprocess

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
MAIN = "perm345_chow_rank_strict_proofs_zh_ams.tex"
PDF = ROOT / "perm345_chow_rank_strict_proofs_zh_ams.pdf"

for pass_number in (1, 2, 3):
    print(f"xelatex pass {pass_number}", flush=True)
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error", MAIN],
        cwd=ROOT,
        check=True,
    )

attachments = [
    ROOT / MAIN,
    ROOT / "n3_body.tex",
    ROOT / "n4_body.tex",
    ROOT / "n5_body.tex",
    ROOT / "formal_computation_spec.tex",
    ROOT / "build_pdf.py",
    PROJECT / "perm35_exact_verification.py",
    PROJECT / "n3_perm35_exact_verification_v11.json",
    PROJECT / "perm4_chow_experiments.py",
    PROJECT / "perm4_quadratic_extension_chart_certificate.py",
    PROJECT / "perm4_quadratic_extension_chart_exact_verify.py",
    PROJECT / "perm4_quadratic_extension_full_minor_replay.py",
    PROJECT / "perm4_rank8_independent_audit.py",
    PROJECT / "perm4_rank8_verify_all.py",
    PROJECT / "perm5_one_intersection_flag_standalone_exact.py",
    PROJECT / "n5_one_intersection_flag_standalone_exact.json",
    PROJECT / "perm5_v14_mathematical_repair.md",
    PROJECT / "n5_lower15_bypass_padding_lemma_20260810.md",
    PROJECT / "n5_v11_strict_self_audit_20260810.md",
    PROJECT / "n5_v12_structural_candidate_self_audit_20260810.md",
    PROJECT / "n5_flag_fibre_profile_structural_reduction_20260810.md",
    PROJECT / "n5_inverse_shift_layer_orbit_reduction_20260810.md",
    PROJECT / "n5_exceptional_visible_parent_reduction_20260810.md",
    PROJECT / "n5_crossing_marginal_density_reduction_20260810.md",
    PROJECT / "n5_nocrossing_compression_structural_reduction_20260810.md",
    PROJECT / "n5_fixed_six_58_routes_pure_arithmetic_20260810.md",
    PROJECT / "n5_d11_d12_pure_route_audit_20260810.md",
    PROJECT / "n5_flag_simultaneous_shift_lemma_20260810.md",
    PROJECT / "n5_flag_shifted_stability_pure_20260810.md",
    PROJECT / "n5_shifted_terminal_stability_gap_fix_20260810.md",
    PROJECT / "n5_shifted_profile_layer_defect_reduction_20260810.md",
    PROJECT / "n5_visible_shadow_structural_reduction_20260810.md",
    PROJECT / "n5_flag_local_witness_forests_20260810.md",
    PROJECT / "n5_flag_orbit0_full_shadow_witness_forests_20260810.md",
    PROJECT / "n5_orbit0_inverse_shift_petersen_pure_20260810.md",
    PROJECT / "n5_orbit13_ten_line_cut_table_pure_20260810.md",
    PROJECT / "n5_orbit13_pure_cut_reduction_20260810.md",
    PROJECT / "n5_orbit13_structural36_pure_20260810.md",
    PROJECT / "n5_orbit1_relative_length2_pure_audit_20260810.md",
    PROJECT / "n5_orbit1_terminal_pure_graph_classification_20260810.md",
    PROJECT / "n5_orbit1_WM_same_row_valuative_two_row_closure_20260810.md",
    PROJECT / "n5_lower16_route4_orbit1_WM_valuative_splice_20260810.md",
    PROJECT / "n5_lower16_pure_dependency_splice_audit_20260810.md",
    PROJECT / "n5_v13_pure_terminal_self_audit_20260810.md",
    PROJECT / "n5_orbit0_fullflag_column_rigidity_pure_20260810.md",
    PROJECT / "n5_orbit0_fourier_rigidity_pure_20260810.md",
    PROJECT / "perm5_shifted_terminal_stability_gap_verify.py",
    PROJECT / "n5_shifted_terminal_stability_gap_verify_exact.json",
    PROJECT / "perm5_shifted_profile_layer_defect_audit.py",
    PROJECT / "n5_shifted_profile_layer_defect_exact.json",
    PROJECT / "perm5_visible_shadow_structural_reduction_audit.py",
    PROJECT / "n5_visible_shadow_structural_reduction_exact.json",
    PROJECT / "perm5_flag_shifted_stability_verify.py",
    PROJECT / "n5_flag_shifted_stability_verify_exact.json",
    PROJECT / "perm5_flag_fibre_profile_reduction_audit.py",
    PROJECT / "n5_flag_fibre_profile_reduction_exact.json",
    PROJECT / "perm5_inverse_shift_layer_orbit_reduction_audit.py",
    PROJECT / "n5_inverse_shift_layer_orbit_reduction_exact.json",
    PROJECT / "perm5_exceptional_visible_parent_reduction_audit.py",
    PROJECT / "n5_exceptional_visible_parent_reduction_exact.json",
    PROJECT / "perm5_crossing_marginal_density_audit.py",
    PROJECT / "n5_crossing_marginal_density_exact.json",
    PROJECT / "perm5_flag_direction_symmetry_audit.py",
    PROJECT / "n5_flag_direction_symmetry_exact.json",
    PROJECT / "perm5_witness_graph_structure_audit.py",
    PROJECT / "n5_witness_graph_structure_exact.json",
    PROJECT / "perm5_fixed_six_pure_universe_audit.py",
    PROJECT / "n5_fixed_six_pure_universe_audit_exact.json",
    PROJECT / "perm5_s19d9_pure_count_audit.py",
    PROJECT / "n5_s19d9_pure_count_audit_exact.json",
    PROJECT / "perm5_p9_nocrossing_exact.py",
    PROJECT / "perm5_nocrossing_compression_diagnostic.py",
    PROJECT / "perm5_crossing_integer_tables_exact.py",
    PROJECT / "perm5_coordinate_d3_orbit_scan.py",
    PROJECT / "perm5_coordinate_prolongation_hypergraph.py",
    PROJECT / "n5_coordinate_prolongation_hypergraph_F3_exact.json",
    PROJECT / "perm5_p11_global_graph_bound_exact.py",
    PROJECT / "perm5_p12_global_graph_bound_exact.py",
    PROJECT / "n5_p12_global_graph_bound_integer_exact.json",
    PROJECT / "perm5_witness_forest_independent_audit.py",
    PROJECT / "n5_witness_forest_independent_audit_exact.json",
    PROJECT / "perm5_orbit0_inverse_shift_petersen_audit.py",
    PROJECT / "n5_orbit0_inverse_shift_petersen_exact.json",
    PROJECT / "perm5_orbit13_four_row_QQ_audit.py",
    PROJECT / "n5_orbit13_four_row_QQ_audit_exact.json",
    PROJECT / "perm5_orbit13_structural36_audit.py",
    PROJECT / "n5_orbit13_structural36_audit_exact.json",
    PROJECT / "perm5_fixed_five_shadow_s20_le50_annihilator_classify_exact.py",
    PROJECT / "n5_fixed_five_shadow_s20_le50_annihilator_classification_exact.json",
    PROJECT / "perm5_s20_orbit1_fixed_flag_P3_graph_exact.py",
    PROJECT / "n5_s20_orbit1_fixed_flag_P3_graph_integer_exact.json",
    PROJECT / "perm5_orbit1_length2_standalone_exact.py",
    PROJECT / "n5_orbit1_length2_standalone_exact.json",
    PROJECT / "perm5_orbit1_missing_WM_exact.py",
    PROJECT / "n5_orbit1_missing_WM_exact.json",
    PROJECT / "perm5_orbit1_terminal_pure_formula_audit.py",
    PROJECT / "n5_orbit1_terminal_pure_formula_audit_exact.json",
    PROJECT / "perm5_orbit1_WM_same_row_valuative_small_lemmas_QQ_exact.py",
    PROJECT / "n5_orbit1_WM_same_row_valuative_small_lemmas_QQ_exact.json",
    PROJECT / "perm5_s20_orbit0_fullflag_tangent_graph_exact.py",
    PROJECT / "n5_s20_orbit0_fullflag_tangent_graph_integer_exact.json",
    PROJECT / "perm5_orbit0_fourier_rigidity_verify.py",
    PROJECT / "n5_orbit0_fourier_rigidity_verify_exact.json",
]
missing = [str(path) for path in attachments if not path.is_file()]
if missing:
    raise FileNotFoundError("Missing PDF attachments: " + ", ".join(missing))

manifest = ROOT / "attachment_manifest.json"
manifest_payload = {
    "format": "perm345-v14-repaired-pdf-attachment-manifest-v1",
    "files": [
        {
            "name": path.name,
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper(),
        }
        for path in attachments
    ],
}
manifest.write_bytes(
    (json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
)
attachments.append(manifest)

if len({path.name for path in attachments}) != len(attachments):
    raise RuntimeError("Attachment basenames must be unique")

reader = PdfReader(PDF)
writer = PdfWriter()
writer.clone_document_from_reader(reader)
for path in attachments:
    writer.add_attachment(path.name, path.read_bytes())
temporary = PDF.with_suffix(".attached.tmp.pdf")
with temporary.open("wb") as stream:
    writer.write(stream)
temporary.replace(PDF)

check = PdfReader(PDF)
embedded = sorted(check.attachments)
expected = sorted(path.name for path in attachments)
if embedded != expected:
    raise RuntimeError(f"Attachment mismatch: {embedded!r} != {expected!r}")

print(
    f"PASS_AMS_PDF_BUILD pages={len(check.pages)} "
    f"attachments={len(embedded)}"
)
