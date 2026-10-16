#!/usr/bin/env python3
"""Fresh extraction, local compilation, and standalone computation acceptance."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

REPO = Path(__file__).resolve().parents[2]


def run(command,cwd,log):
    start = time.monotonic()
    with log.open("w") as output:
        result = subprocess.run(command,cwd=cwd,stdout=output,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {command}; see {log}")
    return {"command":command,"returncode":result.returncode,
            "elapsed_seconds":round(time.monotonic()-start,3),
            "log":log.name,"log_sha256":hashlib.sha256(log.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("n",type=int,choices=(5,6))
    parser.add_argument("--work-dir",type=Path,required=True)
    args = parser.parse_args()
    archive = REPO / "dist" / f"perm{args.n}_arxiv_20261016.zip"
    stage = Path(tempfile.mkdtemp(prefix=f"perm{args.n}_release_",dir=args.work_dir))
    logs = REPO / "audit" / "20261016" / "logs"
    logs.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise RuntimeError("corrupt archive")
        for info in z.infolist():
            path = Path(info.filename)
            if path.is_absolute() or ".." in path.parts or any(x.startswith('.') for x in path.parts):
                raise RuntimeError("unsafe or hidden archive member")
            if info.filename != "main.tex" and not info.filename.startswith("anc/"):
                raise RuntimeError("unexpected top-level source member")
        members = len(z.infolist())
        z.extractall(stage)
    record = {"n":args.n,"archive":archive.name,
              "archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
              "members":members,"python_version":sys.version.split()[0],"commands":[]}
    for iteration in range(1,4):
        entry = run(["pdflatex","-no-shell-escape","-recorder","-interaction=nonstopmode",
                     "-halt-on-error","main.tex"],stage,
                    logs/f"perm{args.n}_compile_pass{iteration}.log")
        record["commands"].append(entry)
        log = (stage/"main.log").read_text(errors="replace")
        if iteration>=2 and not any(x in log for x in ("Rerun to get", "Rerun to get outlines right")):
            break
    if any(x in log for x in ("Overfull", "Underfull", "undefined", "LaTeX Warning")):
        raise RuntimeError("final TeX warning or box defect")
    record["commands"].append(run([sys.executable,"-B",str(stage/"anc/verify_submission.py")],
                                  args.work_dir,logs/f"perm{args.n}_release_replay.log"))
    preview = REPO/"dist"/f"perm{args.n}_chow_rank_{16 if args.n==5 else 32}_20261016.pdf"
    shutil.copyfile(stage/"main.pdf",preview)
    record["commands"].append(run(["pdfinfo",str(preview)],stage,logs/f"perm{args.n}_pdfinfo.log"))
    record["commands"].append(run(["pdffonts",str(preview)],stage,logs/f"perm{args.n}_fonts.log"))
    info = (logs/f"perm{args.n}_pdfinfo.log").read_text()
    if "JavaScript:      no" not in info or "Encrypted:       no" not in info:
        raise RuntimeError("unexpected PDF property")
    font_lines = (logs/f"perm{args.n}_fonts.log").read_text().splitlines()[2:]
    if not font_lines or any(line.split()[-5] != "yes" for line in font_lines):
        raise RuntimeError("missing embedded font")
    record["preview_sha256"] = hashlib.sha256(preview.read_bytes()).hexdigest()
    record["stage_directory"] = str(stage)
    record["status"] = "PASS_LOCAL_SOURCE_AND_COMPUTATION"
    (REPO/"audit"/"20261016"/f"perm{args.n}_release_qa.json").write_text(
        json.dumps(record,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"n":args.n,"status":record["status"],"stage_directory":str(stage)},sort_keys=True))


if __name__ == "__main__":
    main()
