#!/usr/bin/env python3
"""Validate exact inventories and run computational premises, not a peer review."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

N = 6
ANC = Path(__file__).resolve().parent
ROOT = ANC.parent


def parse_manifest(manifest: Path) -> dict[str, str]:
    entries = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](.+)", line)
        if not match:
            raise RuntimeError("invalid SHA-256 manifest line")
        digest, name = match.groups()
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or "\\" in name or ":" in name or relative.as_posix() != name:
            raise RuntimeError("noncanonical inventory path")
        if name in entries:
            raise RuntimeError("duplicate inventory path")
        entries[name] = digest.lower()
    if not entries:
        raise RuntimeError("empty inventory")
    return entries


def inventory(base: Path, manifest: Path) -> dict[str, str]:
    entries = parse_manifest(manifest)
    for name, expected in entries.items():
        path = (base / name).resolve()
        if not path.is_relative_to(base.resolve()):
            raise RuntimeError("inventory path escapes package")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError("SHA-256 mismatch: " + name)
    return entries


def computational(name: str) -> bool:
    return name == "verify_all.py" or (name.startswith("computation/") and PurePosixPath(name).suffix in {".py", ".json", ".csv"})


def frozen_inventory() -> tuple[int, int]:
    full = parse_manifest(ANC / "original" / "MANIFEST.sha256")
    selected = inventory(ANC / "original", ANC / "COMPUTATION_INPUTS.sha256")
    if selected != {name: digest for name, digest in full.items() if computational(name)}:
        raise RuntimeError("computational subset does not match original expected hashes")
    return len(selected), len(full)


def run(path: Path, *args: object) -> None:
    subprocess.run([sys.executable, "-B", str(path), *map(str, args)], cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()
    current = inventory(ROOT, ANC / "SOURCE_MANIFEST.sha256")
    listed = set(current) | {"anc/SOURCE_MANIFEST.sha256"}
    actual_anc = {p.relative_to(ROOT).as_posix() for p in ANC.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    if actual_anc != {name for name in listed if name.startswith("anc/")}:
        raise RuntimeError("unlisted or missing ancillary file")
    if any(name.lower().endswith(".tex") and name != "main.tex" for name in listed):
        raise RuntimeError("TeX source is not permitted inside ancillary files")
    frozen, historical = frozen_inventory()
    print(f"INVENTORY_PASS submission_files={len(current)} frozen_computation_files={frozen} historical_manifest_entries={historical}", flush=True)
    if args.inventory_only:
        return
    if N == 5:
        with tempfile.TemporaryDirectory(prefix="perm5_short_proof_") as temporary:
            observed = Path(temporary) / "observed.json"
            run(ANC / "verify_short_proof.py", "--output", observed)
            if json.loads(observed.read_text()) != json.loads((ANC / "short_proof_exact.json").read_text()):
                raise RuntimeError("short-proof finite payload mismatch")
        run(ANC / "verify_short_proof_independent.py")
    run(ANC / "verify_prolongation_independent.py", "--n", N)
    run(ANC / "verify_glynn.py", N)
    run(ANC / "original" / "verify_all.py")
    frozen_inventory()
    print(f"PERM{N}_SUBMISSION_COMPUTATION_PASS written_proof_requires_mathematical_review")


if __name__ == "__main__":
    main()
