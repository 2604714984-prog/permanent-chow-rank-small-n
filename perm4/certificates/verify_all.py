"""Replay every exact certificate accompanying the perm4 manuscript."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(script: str) -> None:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)


def main() -> None:
    run("perm4_rank8_independent_audit.py")
    run("perm4_rank8_verify_all.py")
    print("PERM4_ACTIVE_PROOF_REPLAY_PASS")


if __name__ == "__main__":
    main()
