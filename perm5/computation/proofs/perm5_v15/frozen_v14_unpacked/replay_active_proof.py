#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

try:
    import flint  # noqa: F401 -- required by the independent n=4 replay
except ModuleNotFoundError:
    raise SystemExit(
        "REPLAY_DEPENDENCY_MISSING: install python-flint==0.8.0 "
        "(python -m pip install -r requirements-replay.txt)"
    )


def run(command: list[str], cwd: Path) -> None:
    print("RUN", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


parser = argparse.ArgumentParser()
parser.add_argument("--with-pdf", action="store_true")
args = parser.parse_args()

run([sys.executable, "verify_manifest.py"], ROOT)
with tempfile.TemporaryDirectory(prefix="perm345_v14_replay_") as temporary:
    work = Path(temporary) / "packet"
    shutil.copytree(ROOT, work)
    commands = [
        [sys.executable, "perm35_exact_verification.py", "--n", "3", "--psi"],
        [sys.executable, "perm4_rank8_independent_audit.py"],
        [sys.executable, "perm4_rank8_verify_all.py"],
        [sys.executable, "-O", "perm5_one_intersection_flag_standalone_exact.py"],
    ]
    for command in commands:
        run(command, work)
    if args.with_pdf:
        run([sys.executable, "build_pdf.py"], work / "latex" / "perm345_v14_repaired")
run([sys.executable, "verify_manifest.py"], ROOT)
print("ACTIVE_PROOF_REPLAY_PASS")
