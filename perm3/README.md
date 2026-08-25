# ChowRank(perm3) = 4

This directory is a self-contained characteristic-zero proof package for

\[
\operatorname{ChowRank}(\operatorname{perm}_3)=4.
\]

- Manuscript: [`paper/perm3_chow_rank_4_proof_zh_ams.pdf`](paper/perm3_chow_rank_4_proof_zh_ams.pdf)
- AMS LaTeX source: [`paper/source/`](paper/source/)
- Exact certificate: [`certificates/`](certificates/)

Replay with:

```bash
python -B perm3/certificates/verify_all.py
```

The mathematical proof is hand-checkable; the exact script independently
reconstructs the displayed Koszul ranks and Glynn decomposition.
