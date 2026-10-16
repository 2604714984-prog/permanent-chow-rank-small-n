#!/usr/bin/env python3
"""Local acceptance for release 20261016-r2; never rewrites a frozen manifest.

Use a fresh --work directory. PDFLaTeX must already be installed. No network,
package installer, shell escape, scheduled job, or CI runner is needed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import subprocess
import sys
import tempfile
import time
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
RELEASE = "20261016-r2"
LOGS = AUDIT / "release_logs"
RESULT = {"release": RELEASE, "baseline_commit": "ff27dd3377e341ae89e4fd9017cf3d174f51d7c8",
          "environment": {"python": sys.version, "platform": platform.platform(),
                          "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION},
          "commands": [], "packages": {}, "negative_tests": []}


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def snapshot(directory: Path) -> dict[str, str]:
    return {p.relative_to(directory).as_posix(): sha(p) for p in sorted(directory.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def save() -> None:
    (AUDIT / "release_acceptance.json").write_bytes((json.dumps(RESULT, indent=2, sort_keys=True)+"\n").encode())


def run(label: str, argv: list[str], cwd: Path, optimize: int = 0,
        expect_success: bool = True, timeout: int = 1200) -> dict:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONOPTIMIZE=str(optimize), PYTHONUTF8="1")
    LOGS.mkdir(exist_ok=True)
    log = LOGS / (label+".log")
    start = time.monotonic()
    print("RUN", label, flush=True)
    with log.open("wb") as stream:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=stream,
                              stderr=subprocess.STDOUT, timeout=timeout, check=False)
    try:
        recorded_cwd = os.path.relpath(cwd, ROOT)
    except ValueError:
        recorded_cwd = "<system-temp>/"+cwd.name
    record = {"label": label, "arguments": [x.replace(str(ROOT.parent), "<audit-workspace>") for x in argv],
              "cwd": recorded_cwd, "PYTHONOPTIMIZE": optimize,
              "exit_code": proc.returncode, "expected_success": expect_success,
              "seconds": round(time.monotonic()-start, 3), "log": log.relative_to(AUDIT).as_posix(),
              "log_sha256": sha(log)}
    RESULT["commands"].append(record)
    save()
    require((proc.returncode == 0) == expect_success, "unexpected exit status: "+label)
    print("RESULT", label, proc.returncode, record["seconds"], flush=True)
    return record


def extract(archive: Path, destination: Path) -> dict:
    destination.mkdir()
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate ZIP member")
        require("main.tex" in names, "missing main.tex")
        for info in z.infolist():
            p = PurePosixPath(info.filename)
            require(not p.is_absolute() and ".." not in p.parts and "\\" not in info.filename, "unsafe member")
            require(info.filename == "main.tex" or info.filename.startswith("anc/"), "extra root member")
            require(not info.filename.lower().endswith(".tex") or info.filename == "main.tex", "ancillary TeX")
            require(info.compress_type == zipfile.ZIP_STORED, "backend-dependent compressed member")
            require(info.create_system == 3 and info.date_time == (2026, 10, 16, 0, 0, 0), "variable ZIP metadata")
        require(z.testzip() is None, "ZIP CRC failure")
        z.extractall(destination)
    source = ROOT / "submissions" / RELEASE / destination.name
    require(all((source / name).read_bytes() == (destination / name).read_bytes() for name in names),
            "source ZIP payload differs from frozen source tree")
    return {"zip_sha256": sha(archive), "zip_bytes": archive.stat().st_size,
            "zip_members": len(names), "source_manifest_sha256": sha(destination / "anc/SOURCE_MANIFEST.sha256"),
            "all_zip_members_stored": True, "all_member_bytes_match_source": True,
            "nested_tex_files": [], "external_figure_files": []}


def negatives(n: int, archive: Path) -> None:
    for kind in ("alter_certificate", "missing_certificate", "duplicate_manifest_entry", "unlisted_ancillary"):
        with tempfile.TemporaryDirectory(prefix=f"perm{n}_{kind}_") as temporary:
            root = Path(temporary)
            with zipfile.ZipFile(archive) as z:
                z.extractall(root)
            original_manifest = sha(root / "anc/original/MANIFEST.sha256")
            source_manifest = root / "anc/SOURCE_MANIFEST.sha256"
            if kind in ("alter_certificate", "missing_certificate"):
                certificate = next((root / "anc/original/computation").rglob("*.json"))
                if kind == "alter_certificate":
                    data = certificate.read_bytes()
                    certificate.write_bytes(data+b"\n")
                else:
                    certificate.unlink()
            elif kind == "duplicate_manifest_entry":
                first = source_manifest.read_bytes().splitlines(keepends=True)[0]
                source_manifest.write_bytes(source_manifest.read_bytes()+first)
            else:
                (root / "anc/unlisted_probe.txt").write_text("negative-test fixture only", encoding="utf-8")
            record = run(f"perm{n}_{kind}_O2", [sys.executable, "-B", "anc/verify_submission.py", "--inventory-only"],
                         root, optimize=2, expect_success=False, timeout=30)
            require(sha(root / "anc/original/MANIFEST.sha256") == original_manifest,
                    "negative fixture changed an original expected certificate hash")
            RESULT["negative_tests"].append({"n": n, "case": kind, "exit_code": record["exit_code"],
                                             "original_expected_hashes_unchanged": True})
            save()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, default=ROOT.parent / "r2 final extracted submissions")
    args = parser.parse_args()
    work = args.work.resolve()
    require(not work.exists(), "refusing to reuse an extraction directory")
    work.mkdir(parents=True)
    protected = [ROOT / "perm5", ROOT / "perm6", ROOT / "submissions/20261016"]
    before = {p.as_posix(): snapshot(p) for p in protected}
    legacy_dist = {p.name: sha(p) for p in (ROOT / "dist").iterdir() if p.is_file() and "-r2" not in p.name}
    run("pdflatex_version", ["pdflatex", "--version"], ROOT, timeout=30)
    for n in (5, 6):
        archive = ROOT / "dist" / f"perm{n}_arxiv_{RELEASE}.zip"
        dest = work / f"perm{n}"
        RESULT["packages"][str(n)] = extract(archive, dest)
        ancillary_before = snapshot(dest / "anc")
        for opt in (0, 1, 2):
            run(f"perm{n}_r2_O{opt}", [sys.executable, "-B", "anc/verify_submission.py"], dest, optimize=opt)
        run(f"perm{n}_r2_foreign_cwd", [sys.executable, "-B", str(dest / "anc/verify_submission.py")], work,
            optimize=2)
        for passno in (1, 2):
            run(f"perm{n}_r2_tex{passno}", ["pdflatex", "--disable-installer", "-no-shell-escape",
                "-interaction=nonstopmode", "-halt-on-error", "-recorder", "main.tex"], dest, timeout=120)
        log = (dest / "main.log").read_text(encoding="utf-8", errors="replace")
        warnings = [line for line in log.splitlines() if re.search(r"Warning|Overfull|Underfull|undefined|Rerun to", line)]
        bad = [line for line in warnings if line != "Package epstopdf Warning: Shell escape feature is not enabled."]
        require(not bad, "unresolved final TeX warning: "+repr(bad))
        require(not re.search(r"\\(?:input|include|includegraphics|bibliography|write18)\b", (dest / "main.tex").read_text()),
                "unexpected non-package TeX dependency")
        package = RESULT["packages"][str(n)]
        package.update({"final_tex_warnings": warnings, "unexpected_tex_warnings": bad,
                        "preview_pdf_sha256": sha(dest / "main.pdf"), "preview_pdf_bytes": (dest / "main.pdf").stat().st_size,
                        "ancillary_bytes_unchanged_after_replay_and_compile": ancillary_before == snapshot(dest / "anc")})
        require(package["ancillary_bytes_unchanged_after_replay_and_compile"], "ancillary inputs were modified")
        (LOGS / f"perm{n}_final.log").write_bytes((dest / "main.log").read_bytes())
        (LOGS / f"perm{n}_recorder.fls").write_bytes((dest / "main.fls").read_bytes())
        negatives(n, archive)
        save()
    RESULT["protected_original_trees_unchanged"] = all(snapshot(p) == before[p.as_posix()] for p in protected)
    RESULT["legacy_dist_unchanged"] = all(sha(ROOT / "dist" / name) == digest for name, digest in legacy_dist.items())
    require(RESULT["protected_original_trees_unchanged"] and RESULT["legacy_dist_unchanged"], "historical file mutation")
    RESULT["status"] = "PASS"
    RESULT["scope"] = "Exact finite replay and local technical acceptance; not external peer review or arXiv processor approval."
    save()
    print("RELEASE_ACCEPTANCE_PASS", flush=True)


if __name__ == "__main__":
    main()
