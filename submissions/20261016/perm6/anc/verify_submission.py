#!/usr/bin/env python3
"""Check inventories, replay finite premises, and preserve frozen evidence."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

N = 6
ANC = Path(__file__).resolve().parent
ROOT = ANC.parent


def inventory(base, manifest):
    count = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, name = line.split(maxsplit=1)
        path = (base / name.removeprefix("*")).resolve()
        if not path.is_relative_to(base.resolve()):
            raise RuntimeError("inventory path escapes package")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual.lower() != expected.lower():
            raise RuntimeError(f"SHA-256 mismatch: {path.relative_to(ROOT)}")
        count += 1
    if not count:
        raise RuntimeError("empty inventory")
    return count


def run(path, *args):
    subprocess.run([sys.executable, "-B", str(path), *map(str,args)], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()
    current = inventory(ROOT, ANC / "SOURCE_MANIFEST.sha256")
    frozen = inventory(ANC / "original", ANC / "original" / "MANIFEST.sha256")
    print(f"INVENTORY_PASS submission_files={current} frozen_files={frozen}", flush=True)
    if args.inventory_only:
        return
    run(ANC / "verify_glynn.py", N)
    run(ANC / "original" / "verify_all.py")
    inventory(ANC / "original", ANC / "original" / "MANIFEST.sha256")
    print(f"PERM{N}_SUBMISSION_COMPUTATION_PASS written_proof_requires_mathematical_review")


if __name__ == "__main__":
    main()
