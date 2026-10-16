# perm5 submission verification

Run from the extracted submission root:

```sh
python -B anc/verify_submission.py
```

Python 3.11 or newer, standard library only. No data downloads or external
services are used. Fresh computed outputs go to temporary directories.

The entry point checks the release source inventory and the unchanged
September package inventory, independently checks the finite premises of the
new short proof twice, expands Glynn's identity, replays the original public
package, and checks that its frozen inventory is still unchanged.

`short_proof_exact.json` records the four complete rational matrices, their
nonzero pivot minors, required cubic inclusions, the 352 coordinate symbols,
and elementary partition and inequality checks. `verify_short_proof.py`
constructs derivatives iteratively and uses sparse rational elimination.
`verify_short_proof_independent.py` constructs them by falling factorials and
uses dense rational elimination. Neither imports the other or reads its
output. The manuscript also displays sufficient minors and upper-rank
relations to check the four normal-form ranks by hand.

The written proof still supplies the torus-specialization, rank-four kernel,
rectangular image-span, and filtration arguments. A program PASS does not
constitute an external mathematical review.

`original/` is the complete, unmodified public September perm5 package from
commit `a3d161b0e86d6cd1f7926aa34e3cb4ee0b69f0e2`. It is preserved for evidence
and comparison. The October lower bound does not depend on the old 58-state
classification or its terminal-orbit reduction. The historical private v15
receipt transport issue is not part of this submission's dependency graph.

The only top-level TeX entry is `main.tex`. All non-typesetting material is
under `anc/`. Select PDFLaTeX when processing the upload. This package contains
no author login, license choice, endorsement, or arXiv submission action.
