#!/usr/bin/env python3
"""Recheck published arXiv ZIPs in a fresh native environment, without writes to evidence."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
WORK = ROOT.parent / "fresh extracted submissions"
LOGS = AUDIT / "logs"
LOGS.mkdir(exist_ok=True)
RESULTS = {"baseline_commit": "ff27dd3377e341ae89e4fd9017cf3d174f51d7c8", "environment": {"python": sys.version, "platform": platform.platform()}, "commands": [], "packages": {}}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(directory: Path) -> dict[str, str]:
    return {p.relative_to(directory).as_posix(): sha(p) for p in sorted(directory.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def save() -> None:
    (AUDIT / "acceptance.json").write_bytes((json.dumps(RESULTS, indent=2, sort_keys=True) + "\n").encode())


def run(label: str, argv: list[str], cwd: Path, optimize: int = 0, timeout: int = 1800) -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONOPTIMIZE=str(optimize), PYTHONUTF8="1")
    log = LOGS / (label + ".log")
    start = time.monotonic()
    print("RUN", label, flush=True)
    with log.open("wb") as stream:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout, check=False)
    item = {"label": label, "command": argv, "cwd_relative_to_repository": os.path.relpath(cwd, ROOT), "PYTHONOPTIMIZE": optimize, "exit_code": proc.returncode, "seconds": round(time.monotonic() - start, 3), "log": log.relative_to(AUDIT).as_posix(), "log_sha256": sha(log)}
    RESULTS["commands"].append(item)
    save()
    print("RESULT", label, proc.returncode, item["seconds"], flush=True)
    if proc.returncode:
        print(log.read_text(encoding="utf-8", errors="replace")[-6000:], flush=True)
        raise RuntimeError("command failed: " + label)


def main() -> None:
    baseline = {str(n): snapshot(ROOT / f"perm{n}") for n in (5, 6)}
    if WORK.exists():
        raise RuntimeError("Refusing to reuse extraction directory")
    WORK.mkdir()
    for n in (5, 6):
        run(f"perm{n}_public", [sys.executable, "-B", f"perm{n}/verify_all.py"], ROOT)
        archive = ROOT / "dist" / f"perm{n}_arxiv_20261016.zip"
        dest = WORK / f"perm{n}"
        dest.mkdir()
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            if len(names) != len(set(names)) or "main.tex" not in names:
                raise RuntimeError("invalid ZIP inventory")
            for member in names:
                p = Path(member)
                if p.is_absolute() or ".." in p.parts or any(part.startswith(".") for part in p.parts):
                    raise RuntimeError("unsafe or hidden member")
                if member != "main.tex" and not member.startswith("anc/"):
                    raise RuntimeError("unexpected top-level member")
            if z.testzip() is not None:
                raise RuntimeError("ZIP CRC failure")
            z.extractall(dest)
        RESULTS["packages"][str(n)] = {"archive_sha256": sha(archive), "members": len(names)}
        frozen_before = snapshot(dest / "anc" / "original")
        for opt in (0, 1, 2):
            run(f"perm{n}_submission_O{opt}", [sys.executable, "-B", "anc/verify_submission.py"], dest, optimize=opt)
        # Check arbitrary CWD and spaces in the extracted absolute path.
        run(f"perm{n}_foreign_cwd_inventory", [sys.executable, "-B", str(dest / "anc" / "verify_submission.py"), "--inventory-only"], ROOT.parent)
        engine = "pdflatex"
        for passno in (1, 2):
            run(f"perm{n}_pdflatex_pass{passno}", [engine, "--disable-installer", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-recorder", "main.tex"], dest, timeout=180)
        log = (dest / "main.log").read_text(encoding="utf-8", errors="replace")
        warnings = [line for line in log.splitlines() if re.search(r"Warning|Overfull|Underfull|undefined|Rerun to", line)]
        RESULTS["packages"][str(n)].update({"final_tex_warnings": warnings, "compiled_pdf_sha256": sha(dest / "main.pdf"), "frozen_ancillary_bytes_unchanged": frozen_before == snapshot(dest / "anc" / "original")})
        (LOGS / f"perm{n}_final_tex.log").write_bytes((dest / "main.log").read_bytes())
        (LOGS / f"perm{n}_recorder.fls").write_bytes((dest / "main.fls").read_bytes())
        if not RESULTS["packages"][str(n)]["frozen_ancillary_bytes_unchanged"]:
            raise RuntimeError("frozen ancillary input was modified")
        save()
    RESULTS["public_original_bytes_unchanged"] = all(baseline[str(n)] == snapshot(ROOT / f"perm{n}") for n in (5, 6))
    RESULTS["status"] = "PASS" if RESULTS["public_original_bytes_unchanged"] else "FAIL"
    save()
    print(RESULTS["status"], flush=True)


if __name__ == "__main__":
    main()
