# Exact Chow Ranks of the 3x3 and 4x4 Permanents

This repository contains a characteristic-zero proof of

\[
\operatorname{ChowRank}(\operatorname{perm}_3)=4,
\qquad
\operatorname{ChowRank}(\operatorname{perm}_4)=8.
\]

The complete manuscript is
[`paper/perm34_chow_rank_exact_proofs_zh_ams.pdf`](paper/perm34_chow_rank_exact_proofs_zh_ams.pdf).
The AMS LaTeX source is under [`paper/source/`](paper/source/), and every exact
certificate used in the proof is under [`certificates/`](certificates/).

## Reproduction

```bash
python -m pip install -r certificates/requirements-replay.txt
python -B certificates/verify_all.py
```

The replay checks the frozen 3x3 certificate, independently reconstructs the
4x4 rational chart calculation, and replays the complete 659 by 659 minor at
two primes and multiple parameter values. Numerical optimization and
floating-point rank decisions are not proof evidence.

## Review status

The package has passed exact author-side replay on Windows and GitHub Actions
on Linux. Named independent human peer review remains pending.
