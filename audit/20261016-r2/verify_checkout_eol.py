#!/usr/bin/env python3
"""Test a real local Git clone with core.autocrlf=true. No network or CI."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination', type=Path, default=ROOT.parent/'accepted-autocrlf-checkout')
    args = parser.parse_args()
    checkout = args.destination.resolve()
    if checkout.exists():
        raise RuntimeError('refusing to reuse a checkout')
    subprocess.run(['git','-c','core.autocrlf=true','clone','--quiet','--no-local','--no-hardlinks',str(ROOT),str(checkout)],check=True)
    subprocess.run(['git','config','core.autocrlf','true'],cwd=checkout,check=True)
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()
    result = {'tested_commit':head,'core_autocrlf':'true','commands':[],'artifact_hashes':{},
              'scope':'real native Windows clone with byte-preserving repository attributes'}
    env = dict(os.environ,PYTHONOPTIMIZE='2',PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
    logs = AUDIT/'checkout_logs'
    logs.mkdir(exist_ok=True)
    for release in ('20261016','20261016-r2'):
        for n in (5,6):
            command = [sys.executable,'-B',f'submissions/{release}/perm{n}/anc/verify_submission.py']
            if release=='20261016':
                command.append('--inventory-only')
            label = f'perm{n}_{release}'
            log = logs/(label+'.log')
            start = time.monotonic()
            with log.open('wb') as stream:
                proc = subprocess.run(command,cwd=checkout,env=env,stdout=stream,stderr=subprocess.STDOUT)
            record = {'label':label,'exit_code':proc.returncode,'PYTHONOPTIMIZE':2,
                      'seconds':round(time.monotonic()-start,3),'log':log.relative_to(AUDIT).as_posix(),
                      'log_sha256':sha(log)}
            result['commands'].append(record)
            print(label,record['exit_code'],record['seconds'],flush=True)
            if proc.returncode:
                raise RuntimeError('checkout inventory/replay failed: '+label)
    rebuilt = checkout.parent/(checkout.name+'-rebuilt')
    subprocess.run([sys.executable,'-B','scripts/build_arxiv_submissions.py','--output-dir',str(rebuilt)],cwd=checkout,env=env,check=True)
    for n in (5,6):
        name = f'perm{n}_arxiv_20261016-r2.zip'
        actual = sha(rebuilt/name)
        expected = sha(ROOT/'dist'/name)
        if actual!=expected or sha(checkout/'dist'/name)!=expected:
            raise RuntimeError('fresh clone archive bytes differ')
        result['artifact_hashes'][name] = actual
    protected = ('perm3/','perm4/','perm5/','perm6/','submissions/','audit/')
    tree = subprocess.check_output(['git','ls-tree','-r','HEAD'],cwd=checkout,text=True).splitlines()
    checked = 0
    mismatches = []
    for line in tree:
        info,name = line.split('\t',1)
        if not name.startswith(protected):
            continue
        expected = info.split()[2]
        data = (checkout/name).read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        checked += 1
        if actual!=expected:
            mismatches.append(name)
    if mismatches:
        raise RuntimeError('byte-protected files changed during checkout: '+repr(mismatches))
    result['protected_tracked_files_checked'] = checked
    result['checkout_byte_mismatches'] = mismatches
    result['working_tree_clean'] = not subprocess.check_output(['git','status','--porcelain'],cwd=checkout,text=True).strip()
    if not result['working_tree_clean']:
        raise RuntimeError('checkout replay modified tracked files')
    result['status'] = 'PASS'
    (AUDIT/'checkout_eol_after.json').write_bytes((json.dumps(result,indent=2,sort_keys=True)+'\n').encode())
    print('AUTOC RLF CHECKOUT PASS'.replace('AUTOC RLF','AUTOCRLF'),checked,flush=True)


if __name__=='__main__':
    main()
