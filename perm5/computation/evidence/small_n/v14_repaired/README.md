# Repaired v14 small-n manuscript

Version 14 addresses the two load-bearing mathematical gaps in the external
audit of PR #26:

- it proves the universal one-intersection flag theorem, including the closed
  incidence that preserves the nine-dimensional quotient image and the
  arbitrary tenth quotient direction;
- it restores the squarefree-binary-cubic exclusion as a named
  characteristic-zero lemma with an explicit second-derivative proof.

The flag theorem has one exact computational premise.  The standalone program
reconstructs the integral divided-power coordinate matrices, reduces those
integer matrices modulo 3, and exhausts 886,464 coordinate flags.  The modular
rank inequality is used only to upper-bound the characteristic-zero kernel.
The maximum is 26 (attached orbit), while the four-dimensional and external
maxima are 22.

Accordingly, v14 is described as a computer-assisted characteristic-zero
algebraic-geometric proof with finite combinatorial classifications.  It is not
described as program-free or purely combinatorial.

Run the outer and clean inner checks with:

```text
python -m pip install python-flint==0.8.0
python -B verify_assets.py --replay
```

The outer verifier requires the manifest to contain exactly the named PDF and
reviewer ZIP, with unique names, positive byte counts, and syntactically valid
SHA-256 values.  It verifies the extracted package manifest before replay and
again after replay, so a replay program that changes a controlled file cannot
return a false pass.  Inner programs run with `python -B` and
`PYTHONDONTWRITEBYTECODE=1`; extraction is temporary, so cache files and other
uncontrolled replay side effects are not published.

The reviewer ZIP performs all active `n=3`, `n=4`, and new `n=5` exact checks
in that temporary copy and can optionally rebuild the 50-page PDF.  No
historical 10 GB asset is included.

`REVIEW_BOUNDARY.json` binds the clean main-target proof commit and tree, the
unchanged PDF and ZIP identities, the hardened verifier blob, and the local
validation classification.  The exact-head hosted CI run is bound separately
in the pull-request conversation so that recording the run ID does not mutate
the reviewed tree.
The `n=5` endpoint verifier itself uses only the Python standard library;
`python-flint` is required only by the independent `n=4` replay.

The equality claim remains a repaired internal research draft until a fresh
external mathematical review accepts the new bridge.
