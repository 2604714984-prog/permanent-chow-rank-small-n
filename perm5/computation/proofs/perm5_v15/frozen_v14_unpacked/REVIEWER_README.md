# perm345 v14 repaired reviewer packet

This packet repairs the two load-bearing mathematical gaps identified in the
external audit of PR #26.

1. The manuscript now proves a named universal one-intersection flag theorem.
   A closed projective incidence keeps the nine-dimensional quotient image at
   the torus-fixed endpoint; the arbitrary tenth quotient direction is included.
2. Its finite endpoint is a theorem premise: a standard-library-only program
   reconstructs the integral divided-power matrices and checks 886,464 flags
   exactly after reduction modulo 3.  Modular rank is used only in the valid
   direction: it gives an upper bound for the characteristic-zero kernel.
3. The compressed binary-cubic sentence is replaced by a named characteristic-
   zero lemma with an explicit two-variable second-derivative proof.
4. The result is labelled computer-assisted characteristic-zero algebraic
   geometry with finite combinatorial classifications, not program-free or
   purely combinatorial.

The theorem claim is a repaired research draft pending a fresh external review.
No SAT/DRAT archive, historical 10 GB asset, GPU computation, random diagnostic,
or unpublished data is required.

## Fail-closed verification

Python 3.11 or later is recommended.  The active `n=5` endpoint verifier uses
only the standard library.  The full `n=3,4,5` replay also runs the independent
`n=4` audit, which requires `python-flint==0.8.0`.  From the extracted packet
root, run:

```text
python -m pip install -r requirements-replay.txt
python verify_manifest.py
python replay_active_proof.py
```

The replay driver copies the packet to a temporary directory before running any
producer.  It verifies the frozen packet both before and after replay, so the
review copy remains byte-for-byte unchanged.  The final lines must include:

```text
PACKAGE_VERIFY_PASS
PERM5_ONE_INTERSECTION_FLAG_STANDALONE_PASS
ACTIVE_PROOF_REPLAY_PASS
```

If XeLaTeX and `pypdf` are installed, this also rebuilds the 50-page PDF:

```text
python replay_active_proof.py --with-pdf
```

The manuscript source is under `latex/perm345_v14_repaired/`.  The PDF embeds
the same source, proof-facing programs, compact certificates, and an attachment
manifest.  Appendix A.4 is a complete independent implementation specification
for the one-intersection flag certificate.
