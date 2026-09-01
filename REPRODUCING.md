# Reproducing the four proof packages

Each package is independent. Run its entry point from the repository root:

```text
python -B perm3/certificates/verify_all.py
python -B perm4/certificates/verify_all.py
python -B perm5/verify_all.py
python -B perm6/verify_all.py
```

`perm4` has the dependency declared in
`perm4/certificates/requirements-replay.txt`. The `perm5` and `perm6`
verification programs use only the standard library.

Every package has its own `MANIFEST.sha256`.
