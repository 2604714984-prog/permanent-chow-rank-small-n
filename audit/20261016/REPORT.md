# perm5 / perm6 submission preparation acceptance report

Date: October 16, 2026 (Asia/Shanghai).

## Outcome and review boundary

Two independent complete LaTeX source ZIPs have been prepared, together with
separate compiled preview PDFs. Both have passed clean extraction, local
PDFLaTeX compilation, source inventory checks, and full computational replay.
The internal mathematical audit has identified no remaining gap in the
revised written proofs. It is not external human peer review, and the
author's personal approval of the newly written perm5 proof is not claimed.

| Paper | Mathematical status | Computation status | Source/technical status |
|---|---|---|---|
| perm5, ordinary rank 16 | New self-contained short lower-bound argument internally audited; explicit normal-form minors printed. Author final reading and external review not recorded. | Both new finite implementations, exact upper-bound expansion, and complete original public replay pass. | Seven-page source compiles from an independently extracted ZIP; no final warnings, unembedded fonts, encryption, or JavaScript. |
| perm6, ordinary rank 32 | Existing proof chain retained and internally audited; key written steps expanded and field extension explicit. External review not recorded. | Primary payload, nine tests, 2,391,496 labelled graphs, 45,696 coordinate symbols, independent actual normal forms, and 1,492,992-choice upper-bound expansion pass. | Eleven-page source compiles from an independently extracted ZIP; no final warnings, unembedded fonts, encryption, or JavaScript. |

**Remaining boundary:** actual arXiv processing/preview has not been run and
no paper has been uploaded or announced. Final author review, metadata, and
license selection remain with the author. There is no identified missing
source file, failed computation, hash discrepancy, or unresolved proof step
in the revised packages as assessed by this internal audit. This is not a
guarantee of arXiv moderation acceptance or a substitute for external review.

## Baseline and evidence preservation

The baseline was read through GitHub and cloned at
`a3d161b0e86d6cd1f7926aa34e3cb4ee0b69f0e2`; the default branch then still
pointed to the September 1, 2026 commit. Read-only original reproduction ran:

```text
python -B perm5/verify_all.py
python -B perm6/verify_all.py
```

Both exited successfully. Every line of the original manifests passed:
15 perm5 files and 13 perm6 files. The original top-level package directories
are unchanged. They are also copied byte-for-byte into their respective new
ancillary directories, including their original expected hashes.

The historical private v15 receipt LF/CRLF issue is separate. It has not been
repaired or declared resolved by this work. No expected frozen hash was
weakened, replaced, or recomputed to force verification. The public packages
passed on their own bytes. The current perm5 proof does not depend on the
private receipt chain.

## Determinate issues fixed

1. **perm5 proof completeness:** the public abridged paper referred to
   reductions not established by its five independent finite programs.
   A state-count PASS did not establish its input prolongation constants,
   and the orbit-zero calculation did not establish the full terminal
   classification. The October article replaces that dependency chain with
   a short written argument. The old manuscript and programs are preserved.
2. **perm5 finite premises:** four actual quintic normal-form derivative
   ranks, required cubic inclusions, all 352 squarefree coordinate symbols,
   monomial floors, and local inequalities are reconstructed by two separate
   implementations. The manuscript prints nonzero minors and upper-rank
   relations, making the small rank calculation inspectable without an
   unpublished certificate.
3. **perm6 reproduction path:** the old manuscript's displayed commands were
   relative to its computation subdirectory while the prose said repository
   checkout. The current manuscript gives one entry point that works from a
   standalone extracted submission and never writes over frozen output.
4. **perm6 written details:** elementary coordinate degeneration, direct
   directional projections, and the exceptional kernel integration argument
   are expanded. Section-offset equation tags are corrected.
5. **Field scope:** both current articles explicitly justify equality over
   every characteristic-zero field by an algebraic-closure lower bound and
   rational Glynn upper bound. Neither claims border rank or general-n
   equality.
6. **Source packaging:** each paper has one root `main.tex` and its own
   ancillary tree; preview PDFs are separate. No external figures,
   bibliography database, custom class/style, font download, shell escape,
   or network service is needed to compile or reproduce the proof calculations.

See [MATHEMATICAL_REVIEW.md](MATHEMATICAL_REVIEW.md) for the precise written
dependency audit and distinction between proofs and executable checks.

## Executed checks and evidence

| Check | Result and archived evidence |
|---|---|
| Original perm5 complete reproduction | PASS; `logs/perm5_public_baseline.log` |
| Original perm6 complete reproduction | PASS; `logs/perm6_public_baseline.log` |
| Fresh ZIP extraction and full perm5 replay | PASS; `perm5_release_qa.json`, `logs/perm5_release_replay.log` |
| Fresh ZIP extraction and full perm6 replay | PASS; `perm6_release_qa.json`, `logs/perm6_release_replay.log` |
| Complete optimized-Python replays | PASS for both; `logs/perm5_optimized_replay.log`, `logs/perm6_optimized_replay.log` |
| Missing/altered source, verifier, and frozen evidence | All expected nonzero exits, in normal and optimized modes; 16 cases in `failure_mode_checks.json`; no expected hash edited. |
| Deterministic source rebuild | Both rebuilt ZIP SHA-256 values match the released ZIPs byte-for-byte. The builder reads and never rewrites inventories. |
| Noncoordinate local counterexample screen | All 5,656,160 quotient/quadric pairs over F3 pass; `quintic_local_stress.json`. Diagnostic only, not a characteristic-zero inference. |
| Actual Glynn image-span integration | Both bounds sharp on actual decompositions; `glynn_global_consistency.json`. Diagnostic only, not a lower-bound proof by itself. |
| Clean source compilation | Two PDFLaTeX passes each, `-no-shell-escape -recorder`; final logs have no undefined references, LaTeX warnings, or over/underfull boxes. |
| PDF properties and visual review | Seven and eleven pages; all fonts embedded; no encryption/JavaScript. Final pages rendered and inspected; see the PDF metadata/font logs. |

Environment: Python 3.12.14, pdfTeX 1.40.25 / TeX Live 2023 (Debian).
TeX Live 2025 and arXiv's live processor were not executed here.
No GitHub Actions workflow was dispatched.

## References and arXiv technical requirements

The active references were checked against primary publisher/arXiv metadata:

- Glynn, *The permanent of a square matrix*, European Journal of Combinatorics
  31(7), 2010, 1887--1891,
  <https://doi.org/10.1016/j.ejc.2010.01.010>.
- Ilten and Teitler, *Product ranks of the 3 x 3 determinant and permanent*,
  Canadian Mathematical Bulletin 59(2), 2016, 311--319,
  <https://doi.org/10.4153/CMB-2015-076-1>.
- Borel, *Linear Algebraic Groups*, second edition, GTM 126, 1991,
  <https://doi.org/10.1007/978-1-4612-0941-6>. The current perm6 text supplies
  its own elementary torus-specialization argument rather than depending on
  the earlier unchecked chapter/theorem pinpoint.
- Han and Song, *The rank of the 5 x 5 permanent tensor is sixteen*,
  <https://arxiv.org/abs/2608.09708>. The title, authors, date and tensor-rank
  result were checked from arXiv-indexed abstract metadata. Full-text access
  was unavailable in this session. This is contextual related work, not a
  premise of either proof; tensor rank is explicitly distinguished from
  ordinary Chow rank in the perm5 article.

The earlier Xu--Gnang arXiv record <https://arxiv.org/abs/2311.05890>
currently states that it is withdrawn with a wrong main theorem. It is not
used as authority for either present lower bound or for a general-n result.
No claim is made that the new internal audit reverses that withdrawal.

Current official arXiv instructions were consulted:

- <https://info.arxiv.org/help/submit_tex.html>: compile from the submission
  root, include required source/figures, remove top-level output/auxiliary
  files, provide bibliography inputs if needed, and inspect the processor PDF.
- <https://info.arxiv.org/help/ancillary_files.html>: scientific code and
  data belong under root `anc/`.

The release archives follow that layout. Their embedded references use
`thebibliography`; there are no figures or missing `.bib`/`.bbl` dependencies.

## Deliverables

- [perm5 source ZIP](../../dist/perm5_arxiv_20261016.zip)
- [perm5 preview PDF](../../dist/perm5_chow_rank_16_20261016.pdf)
- [perm6 source ZIP](../../dist/perm6_arxiv_20261016.zip)
- [perm6 preview PDF](../../dist/perm6_chow_rank_32_20261016.pdf)
- [Release SHA-256 list](../../dist/SHA256SUMS)
- [Project handoff](../../HANDOFF.md)

These relative links point to the repository's retained deliverables. The
source and computation acceptance receipts record actual command exits and
log hashes, separately from the internal mathematical judgment above.
