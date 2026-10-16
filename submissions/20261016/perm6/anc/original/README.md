# The Chow Rank of the Six-by-Six Permanent

This directory contains the proof of the characteristic-zero theorem

\[
\operatorname{ChowRank}(\operatorname{perm}_6)=32.
\]

- Manuscript: [`paper/perm6_chow_rank_32.pdf`](paper/perm6_chow_rank_32.pdf)
- Complete LaTeX source: [`paper/source/`](paper/source/)
- Exact data, verification programs, and tests: [`computation/`](computation/)
- SHA-256 inventory: [`MANIFEST.sha256`](MANIFEST.sha256)

Python 3.11 or newer and only its standard library are required:

```bash
python -B perm6/verify_all.py
```

The command runs the primary exact payload check, nine focused tests, the
independent finite-core enumeration (2,391,496 labelled bipartite graphs and
45,696 coordinate symbol cases), and an independent rational reconstruction
of all five dependent-factor normal forms.
