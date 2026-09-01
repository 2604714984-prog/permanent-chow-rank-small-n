# ChowRank(perm_6) = 32

This directory is a self-contained public package for the author-reviewed,
computer-assisted characteristic-zero theorem

\[
\operatorname{ChowRank}(\operatorname{perm}_6)=32.
\]

- Reviewer manuscript: [`paper/perm6_chow_rank_32_peer_review.pdf`](paper/perm6_chow_rank_32_peer_review.pdf)
- Complete LaTeX source: [`paper/source/`](paper/source/)
- Exact data, primary verifier, independent verifiers, tests, and receipts: [`computation/`](computation/)
- Original computational supplement archive: [`downloads/original_computational_supplement.zip`](downloads/original_computational_supplement.zip)
- SHA-256 inventory: [`MANIFEST.sha256`](MANIFEST.sha256)

Python 3.11 or newer and only its standard library are required:

```bash
python -B perm6/verify_all.py
```

The command runs the primary exact payload check, nine focused tests, the
independent finite-core enumeration (2,391,496 labelled bipartite graphs and
45,696 coordinate symbol cases), and an independent rational reconstruction
of all five dependent-factor normal forms.

The theorem has not yet received named external human peer review and has not
been formalized in a proof assistant. No border-rank or general-`n` claim is
made.
