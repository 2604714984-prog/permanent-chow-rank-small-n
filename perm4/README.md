# The Chow Rank of the Four-by-Four Permanent

This directory is a self-contained characteristic-zero proof package for

\[
\operatorname{ChowRank}(\operatorname{perm}_4)=8.
\]

- Manuscript: [`paper/perm4_chow_rank_8.pdf`](paper/perm4_chow_rank_8.pdf)
- AMS LaTeX source: [`paper/source/`](paper/source/)
- Exact certificates and independent replay: [`certificates/`](certificates/)
- File inventory: [`MANIFEST.sha256`](MANIFEST.sha256)

Replay with:

```bash
python -m pip install -r perm4/certificates/requirements-replay.txt
python -B perm4/certificates/verify_all.py
```

The replay independently reconstructs the rational chart calculation and the
complete 659 by 659 minor at two primes and multiple parameter values.
