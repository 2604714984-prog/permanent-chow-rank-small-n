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

## October 2026 standalone source submissions

The current manuscript revisions have their own inventory-protected entry
points, which also replay the unchanged original public packages:

```text
python -B submissions/20261016/perm5/anc/verify_submission.py
python -B submissions/20261016/perm6/anc/verify_submission.py
```

For a downloaded source ZIP, extract into an empty directory and execute
`python -B anc/verify_submission.py`. No repository checkout or other paper's
files are needed. The wrappers never overwrite frozen evidence.

The source ZIP builder reads, verifies, and never rewrites release inventories:

```text
python -B scripts/build_arxiv_submissions.py
```

The perm5 revision uses the new short-proof finite premises; its old 58-state
computation remains reproducible but does not supply the revised lower bound.
Program PASS markers are computational results, not whole-proof external
review certificates.
