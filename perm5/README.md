# ChowRank(perm_5) = 16

This directory is a self-contained public package for the author-reviewed,
computer-assisted characteristic-zero theorem

\[
\operatorname{ChowRank}(\operatorname{perm}_5)=16.
\]

- Reviewer manuscript: [`paper/perm5_chow_rank_16_peer_review.pdf`](paper/perm5_chow_rank_16_peer_review.pdf)
- Complete LaTeX source, including all 58 fixed-six states: [`paper/source/`](paper/source/)
- Expanded proof programs, frozen inputs, exact outputs, and receipts: [`computation/`](computation/)
- Original computational supplement archive: [`downloads/original_computational_supplement.zip`](downloads/original_computational_supplement.zip)
- SHA-256 inventory: [`MANIFEST.sha256`](MANIFEST.sha256)

## Independent checks on any platform

Python 3.11 or newer and the standard library are sufficient:

```bash
python -B perm5/verify_all.py
```

This reconstructs the 58-state table and independently checks the terminal
4100-vertex tangent/Fourier calculation, including `2215 > 2205`.

## Complete frozen replay

The historical v14 manifest binds CRLF bytes emitted by its producers, so the
unchanged byte-for-byte normal and optimized replay is Windows-bound:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r perm5\computation\requirements-replay.txt
.venv\Scripts\python -B perm5\verify_all.py --full
```

Each full run executes 28 active producers and three older definition-level
independent audits. Typical total time for both modes is several minutes.

The theorem has not yet received named external human peer review and has not
been formalized in a proof assistant. No border-rank or general-`n` claim is
made.
