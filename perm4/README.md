# The Chow Rank of the Four-by-Four Permanent

The current reading version is the **computation-free revision dated October 19, 2026**.

## Current computation-free proof

- [Seven-page PDF](pure_proof_20261019/main.pdf)
- [Complete LaTeX source](pure_proof_20261019/main.tex)
- [Reader's overview](pure_proof_20261019/README.md)
- [Internal proof audit](pure_proof_20261019/AUDIT.md)
- [Research handoff](pure_proof_20261019/HANDOFF.md)
- [Optional exact regression checks](pure_proof_20261019/verify_supplementary.py)

The theorem proved is

\[
\operatorname{ChowRank}(\operatorname{perm}_4)=8.
\]

The proof is for ordinary Chow rank over characteristic-zero fields. It makes no claim about border Chow rank or a general formula for arbitrary matrix size. The manuscript has received internal review, not external peer review or formal proof-assistant certification.

To run the optional regression checks from the repository root:

```sh
python -B perm4/pure_proof_20261019/verify_supplementary.py
```

These checks are not premises of the written proof.

## Historical computation-assisted version

The original version is preserved unchanged:

- [Historical PDF](paper/perm4_chow_rank_8.pdf)
- [Original LaTeX source](paper/source/)
- [Original certificate and replay package](certificates/)
- [Original file inventory](MANIFEST.sha256)

The historical proof relies on exact computational certificates for selected matrix ranks. Do not confuse its PDF with the current computation-free manuscript.
