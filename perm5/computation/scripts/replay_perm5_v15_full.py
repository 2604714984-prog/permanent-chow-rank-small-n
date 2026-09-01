#!/usr/bin/env python3
"""Fail-closed full replay for the perm5 v15 author-reviewed proof package.

The frozen v14 ZIP remains the immutable authority.  This entry verifies its
identity and the ordinary-file mirror, runs every active perm5 producer from
that mirror, checks its manifest hashes before and after replay, and then runs
three definition-level independent audits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "evidence" / "small_n" / "v14_repaired"
FROZEN_ZIP = ASSET_DIR / "perm345_reviewer_submission_v14_repaired_20260812.zip"
ASSET_VERIFIER = ASSET_DIR / "verify_assets.py"
EXPECTED_ZIP_SHA256 = "CE8F639C532B754B4E0A8EEC959D97E461426C9F9402B923D6A13056F46DFF33"
UNPACKED_SOURCE = ROOT / "proofs" / "perm5_v15" / "frozen_v14_unpacked"

ACTIVE_PERM5_SCRIPTS = (
    "perm5_one_intersection_flag_standalone_exact.py",
    "perm5_fixed_six_pure_universe_audit.py",
    "perm5_s19d9_pure_count_audit.py",
    "perm5_p9_nocrossing_exact.py",
    "perm5_nocrossing_compression_diagnostic.py",
    "perm5_crossing_integer_tables_exact.py",
    "perm5_crossing_marginal_density_audit.py",
    "perm5_coordinate_prolongation_hypergraph.py",
    "perm5_p11_global_graph_bound_exact.py",
    "perm5_p12_global_graph_bound_exact.py",
    "perm5_shifted_profile_layer_defect_audit.py",
    "perm5_visible_shadow_structural_reduction_audit.py",
    "perm5_shifted_terminal_stability_gap_verify.py",
    "perm5_flag_shifted_stability_verify.py",
    "perm5_inverse_shift_layer_orbit_reduction_audit.py",
    "perm5_exceptional_visible_parent_reduction_audit.py",
    "perm5_flag_fibre_profile_reduction_audit.py",
    "perm5_orbit0_inverse_shift_petersen_audit.py",
    "perm5_orbit13_four_row_QQ_audit.py",
    "perm5_orbit13_structural36_audit.py",
    "perm5_fixed_five_shadow_s20_le50_annihilator_classify_exact.py",
    "perm5_s20_orbit1_fixed_flag_P3_graph_exact.py",
    "perm5_orbit1_length2_standalone_exact.py",
    "perm5_orbit1_terminal_pure_formula_audit.py",
    "perm5_orbit1_missing_WM_exact.py",
    "perm5_orbit1_WM_same_row_valuative_small_lemmas_QQ_exact.py",
    "perm5_s20_orbit0_fullflag_tangent_graph_exact.py",
    "perm5_orbit0_fourier_rigidity_verify.py",
)

INDEPENDENT_SCRIPTS = (
    ROOT / "scripts" / "perm5_glynn_upper_bound_independent.py",
    ROOT / "scripts" / "perm5_one_intersection_independent_multifield.py",
    ROOT / "scripts" / "perm5_d11_d12_parent_table_independent.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def require_equal(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise RuntimeError(
            f"{label} mismatch: expected {expected!r}, observed {actual!r}"
        )


def verify_unpacked_mirror() -> dict[str, object]:
    manifest_path = UNPACKED_SOURCE / "PACKAGE_MANIFEST.json"
    with zipfile.ZipFile(FROZEN_ZIP) as archive:
        archived_manifest = archive.read("PACKAGE_MANIFEST.json")
    require_equal("unpacked manifest bytes", manifest_path.read_bytes(), archived_manifest)
    manifest = json.loads(archived_manifest)
    expected = {entry["path"]: entry for entry in manifest["files"]}
    verified = []
    for path in sorted(UNPACKED_SOURCE.rglob("*")):
        if not path.is_file() or path == manifest_path:
            continue
        relative = path.relative_to(UNPACKED_SOURCE).as_posix()
        if relative == "README.md":
            continue
        entry = expected.get(relative)
        if entry is None:
            raise RuntimeError(f"untracked unpacked proof file: {relative}")
        require_equal(f"unpacked bytes {relative}", path.stat().st_size, entry["bytes"])
        require_equal(f"unpacked SHA-256 {relative}", sha256(path), entry["sha256"])
        verified.append(relative)
    require_equal("active unpacked scripts present", [
        name for name in ACTIVE_PERM5_SCRIPTS
        if (UNPACKED_SOURCE / name).is_file()
    ], list(ACTIVE_PERM5_SCRIPTS))
    return {
        "status": "PASS",
        "files_verified": len(verified),
        "manifest_sha256": sha256(manifest_path),
    }


def run_checked(command: list[str], cwd: Path, env: dict[str, str]) -> dict[str, object]:
    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    duration = time.perf_counter() - started
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    nonempty = [line for line in completed.stdout.splitlines() if line.strip()]

    def public_argument(argument: str) -> str:
        """Keep receipts reproducible without recording a reviewer's local paths."""
        if argument == sys.executable:
            return "python"
        candidate = Path(argument)
        if not candidate.is_absolute():
            return argument
        try:
            return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            pass
        try:
            candidate.resolve().relative_to(Path(tempfile.gettempdir()).resolve())
            return f"<temporary>/{candidate.name}"
        except ValueError:
            return candidate.name

    return {
        "command": [public_argument(argument) for argument in command],
        "duration_seconds": round(duration, 6),
        "last_stdout_line": nonempty[-1] if nonempty else "",
        "stdout_sha256": hashlib.sha256(
            completed.stdout.encode("utf-8")
        ).hexdigest().upper(),
        "stderr": completed.stderr,
    }


def python_command(script: Path, optimized: bool, *arguments: str) -> list[str]:
    command = [sys.executable, "-B"]
    if optimized:
        command.append("-O")
    command.extend((str(script), *arguments))
    return command


def replay(mode: str) -> dict[str, object]:
    optimized = mode == "optimized"
    require_equal("frozen reviewer ZIP SHA-256", sha256(FROZEN_ZIP), EXPECTED_ZIP_SHA256)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.perf_counter()

    asset_receipt = run_checked(
        python_command(ASSET_VERIFIER, optimized), ASSET_DIR, env
    )
    pre_unpacked = verify_unpacked_mirror()
    with tempfile.TemporaryDirectory(prefix="perm5_v15_full_replay_") as temp_name:
        active_receipts = []
        for filename in ACTIVE_PERM5_SCRIPTS:
            script = UNPACKED_SOURCE / filename
            if not script.is_file():
                raise RuntimeError(f"active proof script missing: {filename}")
            receipt = run_checked(
                python_command(script, optimized), UNPACKED_SOURCE, env
            )
            receipt["script"] = filename
            active_receipts.append(receipt)

        independent_receipts = []
        independent_output_dir = Path(temp_name) / "independent"
        independent_output_dir.mkdir()
        for script in INDEPENDENT_SCRIPTS:
            if not script.is_file():
                raise RuntimeError(f"independent audit script missing: {script}")
            output_path = independent_output_dir / f"{script.stem}.json"
            receipt = run_checked(
                python_command(script, optimized, "--output", str(output_path)),
                ROOT,
                env,
            )
            receipt.update(
                {
                    "script": str(script.relative_to(ROOT)),
                    "script_sha256": sha256(script),
                    "output_sha256": sha256(output_path),
                }
            )
            independent_receipts.append(receipt)

        post_unpacked = verify_unpacked_mirror()
        bytecode_files = tuple(UNPACKED_SOURCE.rglob("*.pyc"))
        require_equal("bytecode files created", len(bytecode_files), 0)

    return {
        "status": "PASS",
        "claim_type": "full author-side exact replay; not independent human peer review",
        "mode": mode,
        "frozen_zip": str(FROZEN_ZIP.relative_to(ROOT)),
        "frozen_zip_sha256": EXPECTED_ZIP_SHA256,
        "asset_verifier": asset_receipt,
        "pre_replay_unpacked_manifest": pre_unpacked,
        "active_perm5_script_count": len(active_receipts),
        "active_perm5_scripts": active_receipts,
        "independent_audit_count": len(independent_receipts),
        "independent_audits": independent_receipts,
        "post_replay_unpacked_manifest": post_unpacked,
        "bytecode_files_created": 0,
        "duration_seconds": round(time.perf_counter() - started, 6),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("normal", "optimized"), required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = replay(args.mode)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(text, encoding="utf-8", newline="\n")
    print(
        "PERM5_V15_FULL_REPLAY_PASS "
        f"mode={args.mode} active={result['active_perm5_script_count']} "
        f"independent={result['independent_audit_count']} "
        f"seconds={result['duration_seconds']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
