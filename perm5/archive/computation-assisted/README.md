# The Chow Rank of the Five-by-Five Permanent

This directory contains the proof of the characteristic-zero theorem

\[
\operatorname{ChowRank}(\operatorname{perm}_5)=16.
\]

- Manuscript: [`paper/perm5_chow_rank_16.pdf`](paper/perm5_chow_rank_16.pdf)
- Complete LaTeX source, including all 58 fixed-six states: [`paper/source/`](paper/source/)
- Exact proof programs and outputs: [`computation/`](computation/)
- SHA-256 inventory: [`MANIFEST.sha256`](MANIFEST.sha256)

## Verification

Python 3.11 or newer and the standard library are sufficient:

```bash
python -B perm5/verify_all.py
```

This runs the one-intersection scan, reconstructs the 58-state table, streams
the parent-table cases, verifies the terminal 4,100-vertex tangent/Fourier
calculation, and expands Glynn's identity exactly.
