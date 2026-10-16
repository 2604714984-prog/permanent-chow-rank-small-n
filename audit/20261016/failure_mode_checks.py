#!/usr/bin/env python3
"""Prove inventory failures stay nonzero without changing expected hashes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def run(stage,optimized):
    env = dict(os.environ)
    env["PYTHONOPTIMIZE"] = "1" if optimized else "0"
    result = subprocess.run([sys.executable,"-B",str(stage/"anc/verify_submission.py"),
                             "--inventory-only"],cwd=stage.parent,env=env,
                            capture_output=True,text=True)
    return result.returncode


def main():
    records = []
    for n in (5,6):
        with tempfile.TemporaryDirectory(prefix=f"perm{n}_negative_checks_") as temporary:
            stage = Path(temporary)/"submission"
            with zipfile.ZipFile(ROOT/"dist"/f"perm{n}_arxiv_20261016.zip") as archive:
                archive.extractall(stage)
            original_manifest = (stage/"anc/original/MANIFEST.sha256").read_bytes()
            release_manifest = (stage/"anc/SOURCE_MANIFEST.sha256").read_bytes()
            for optimized in (False,True):
                if run(stage,optimized)!=0:
                    raise RuntimeError((n,"clean package rejected",optimized))
                records.append({"n":n,"case":"clean_inventory","optimized":optimized,"expected_exit":"zero","pass":True})
            targets = [("main.tex","altered_source"),
                       ("anc/original/verify_all.py","missing_frozen_verifier"),
                       ("anc/original/computation/evidence/"+
                        ("perm5_terminal_independent_verification.json" if n==5 else
                         "n6_dependent_normal_forms_independent.json"),"altered_frozen_evidence")]
            for relative,label in targets:
                path = stage/relative
                original = path.read_bytes()
                if label.startswith("missing"):
                    path.unlink()
                else:
                    path.write_bytes(original+b"\n")
                for optimized in (False,True):
                    if run(stage,optimized)==0:
                        raise RuntimeError((n,"tampering accepted",label,optimized))
                    records.append({"n":n,"case":label,"optimized":optimized,
                                    "expected_exit":"nonzero","pass":True})
                path.write_bytes(original)
            if (stage/"anc/original/MANIFEST.sha256").read_bytes()!=original_manifest:
                raise RuntimeError("original expected hashes changed during negative test")
            if (stage/"anc/SOURCE_MANIFEST.sha256").read_bytes()!=release_manifest:
                raise RuntimeError("release expected hashes changed during negative test")
    payload = {"status":"PASS","scope":"inventory guards, not a mathematical proof or full optimized replay",
               "cases":len(records),"expected_hashes_changed":False,"records":records}
    (ROOT/"audit/20261016/failure_mode_checks.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(f"FAIL_CLOSED_CHECKS_PASS cases={len(records)} expected_hashes_changed=False")


if __name__ == "__main__":
    main()
