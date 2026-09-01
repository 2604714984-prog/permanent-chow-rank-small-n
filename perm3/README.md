# The Chow Rank of the Three-by-Three Permanent

This directory is a self-contained characteristic-zero proof package for

\[
\operatorname{ChowRank}(\operatorname{perm}_3)=4.
\]

- Manuscript: [`paper/perm3_chow_rank_4.pdf`](paper/perm3_chow_rank_4.pdf)
- AMS LaTeX source: [`paper/source/`](paper/source/)
- Exact certificate: [`certificates/`](certificates/)
- File inventory: [`MANIFEST.sha256`](MANIFEST.sha256)

Replay with:

```bash
python -B perm3/certificates/verify_all.py
```

The mathematical proof is hand-checkable; the exact script independently
reconstructs the displayed Koszul ranks and Glynn decomposition.
