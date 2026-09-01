# Reproducing the four proof packages

Each package is independent. Run its entry point from the repository root:

```text
python -B perm3/certificates/verify_all.py
python -B perm4/certificates/verify_all.py
python -B perm5/verify_all.py
python -B perm6/verify_all.py
```

`perm4` has the dependency declared in
`perm4/certificates/requirements-replay.txt`. The cross-platform `perm5`
independent checks and all `perm6` checks use only the standard library.
`perm5/verify_all.py --full` is the historical byte-for-byte frozen replay;
it requires Windows and the pinned dependency in
`perm5/computation/requirements-replay.txt` because the immutable manifest
binds CRLF producer outputs.

Every package has its own `MANIFEST.sha256`. Verification does not require
access to the private research repository.
