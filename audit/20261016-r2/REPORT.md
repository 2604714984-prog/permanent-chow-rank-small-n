# perm5 / perm6 arXiv preparation — second acceptance report

Date: **2026-10-16** (Asia/Shanghai). Active release: **20261016-r2**.
Starting public commit: `ff27dd3377e341ae89e4fd9017cf3d174f51d7c8`.

## Decision and scope

The two revised source packages have passed the local computational and
technical acceptance described below. The internal mathematical dependency
review identified no outstanding logical obligation in the reviewed proofs.
They are prepared for **author-controlled arXiv submission**, subject to final
author approval, appropriate authorship/attribution and account-side submission
checks, and review of the actual arXiv-generated preview.

This is an AI-assisted internal audit. It is not external peer review, a
proof-assistant formalization, author sign-off or an arXiv moderation decision.
No arXiv upload or public announcement was performed. The earlier October
release is preserved, not retroactively relabelled as this acceptance.

| Item | perm5 | perm6 |
|---|---|---|
| Statement | Ordinary Chow rank 16 in characteristic zero | Ordinary Chow rank 32 in characteristic zero |
| Mathematical review | Short proof, all factor-span cases and endpoint N=15 reviewed | Actual derivative spaces, all dependent profiles and global cancellation reviewed |
| Independent finite computations | 352 coordinate cases; four normal forms; 2,925 cubic coefficients; exact upper bound | 45,696 parameter cases; five normal forms; 8,436 cubic coefficients; graph enumeration; exact upper bound |
| Original public entry point | PASS | PASS |
| Current extracted full entry point | PASS at optimization 0, 1, 2 and foreign CWD | PASS at optimization 0, 1, 2 and foreign CWD |
| Source archive | 21 files; 156,187 bytes | 16 files; 108,705 bytes |
| Final preview | 7 pages; 309,819 bytes | 11 pages; 355,156 bytes |
| Local compilation | Two PDFLaTeX passes; no shell escape | Two PDFLaTeX passes; no shell escape |
| Unresolved mathematical defect found | None identified by this internal review | None identified by this internal review |
| Still unverified | Final author approval; external review; actual arXiv processor/account acceptance | Same |

## Deliverables

- [perm5 complete source ZIP](../../dist/perm5_arxiv_20261016-r2.zip)
  and [reading PDF](../../dist/perm5_chow_rank_16_20261016-r2.pdf).
- [perm6 complete source ZIP](../../dist/perm6_arxiv_20261016-r2.zip)
  and [reading PDF](../../dist/perm6_chow_rank_32_20261016-r2.pdf).
- [Submission guide and metadata](../../submissions/20261016-r2/),
  [artifact checksums](../../dist/SHA256SUMS_20261016-r2), and
  [current handoff](../../HANDOFF.md).

The ZIPs contain `main.tex` at the root and an `anc/` directory. The complete
manuscript, bibliography and required verification inputs are present.
Neither paper needs another proof package, a private receipt, external figure,
custom style file, custom font file, network call or shell-escape operation.
The reading PDFs are separate deliverables, not top-level source-ZIP members.

```
47dafb5120877b536ddbebf5a2c1b5052d254a147a3dc3d50b952fa07ccf3057  perm5_arxiv_20261016-r2.zip
3aea76a790da5456e475a06633938bccb07b32ee7e810ec9620ddc4c44645294  perm5_chow_rank_16_20261016-r2.pdf
3a90428a827e1c808f928e2d0d172c7835fe3604d6c16997180d7e77834a0c15  perm6_arxiv_20261016-r2.zip
7b12c4e53d27c9016f5cf9073de354abeaf628989e5bbcd7bfb83788008d493e  perm6_chow_rank_32_20261016-r2.pdf
```

## Definite problems corrected

**Ancillary TeX files.** The r1 archives put full historical manuscripts inside
`anc/original/`. The [arXiv ancillary instructions](https://info.arxiv.org/help/ancillary_files.html)
say not to include TeX sources in that directory. R2 therefore carries the
byte-exact computational subset: 9 original input/program files for perm5,
7 for perm6, plus each complete, unchanged historical manifest. The six
noncomputational historical files omitted from each r2 ancillary tree remain
available unchanged in the original public packages and r1 release. Inclusion
and omission are explicit in ORIGIN.json and the ancillary README, not hidden
behind a false full-inventory PASS.

**Missing AI-assistance disclosure.** Both manuscript bodies now disclose
ChatGPT's assistance with argument development/auditing, exposition,
verification and submission preparation. The disclosure does not infer author
approval or present AI as an author. The [official moderation policy](https://info.arxiv.org/help/moderation/index.html)
was checked for this requirement.

**ZIP portability.** The old builder inherited Windows creator-platform
metadata. Fixing that alone did not reproduce the legacy compressed bytes:
Windows Python here uses zlib-ng, whose DEFLATE output also differs. Every
legacy member's uncompressed bytes were identical. R2 uses `ZIP_STORED`, fixed
creator platform, timestamp and permissions. Tests confirm byte-identical r2
rebuilds, including when the compression backend is deliberately unavailable.
The old ZIPs and their published SHA-256 values are unchanged. See
`zip_portability_before.json`, `zip_portability_after_metadata_fix.json` and
`release_contract_tests.json`. The exhaustive raw offset diagnosis is
preserved locally; its hash is recorded in the compact diagnosis.

**Windows checkout integrity.** The baseline protected the original `perm5/`
and `perm6/` directories from EOL conversion but not the new frozen submission
trees. A real fresh checkout with `core.autocrlf=true` caused both r1 source
inventories to fail, with CRLF conversion observed. The revised Git attributes
protect all submission and audit bytes. See the before/after checkout receipts
for this separately demonstrated public-checkout issue. It is not the unrelated
private v15 transport incident, which was neither changed nor declared fixed.

**Paths and case-domain precision.** Two perm6 program paths now resolve from
the standalone package. The 45,696-case domain is explicitly indexed by
triples `(r,B,A)`, with `0<=r<=3` and `|A|<=r`. Its count includes occurrences
at different relation bounds; it is not a claim of 45,696 distinct pairs after
forgetting r. No table value, frozen certificate or expected hash changed.

## Mathematical review

The [full dependency review](MATHEMATICAL_REVIEW.md) treats the written proofs
separately from finite replay. It checks the torus specializations and correct
semicontinuity directions, the prolongation identity, the small-intersection
bounds, every local quotient-symbol case, and the injections used in the
global filtration increments.

For perm5, the two global bounds give `h2+Delta/2 <= 10N-150`. Nonnegativity
excludes N<=14; at N=15 the intersection bound contradicts a ten-dimensional
term derivative image inside E2. The new proof does not depend on the older
58-state/terminal-orbit route.

For perm6, the symmetric image-span inequality gives
`h<=10N-200-Delta/2`, while the filtered local bound gives
`h>=120-Delta/2`. Their common full defect cancels, proving N>=32 without
assuming that all terms have independent factors or maximal middle rank.
The actual derivative images are not replaced by larger formal factor-product
spans. The documented T2 and T3 discrepancies are retained as regression tests.

Both upper bounds are rational Glynn decompositions. Lower bounds proved over
an algebraic closure and upper bounds over the original field correctly give
the statements over every characteristic-zero field. Neither proof asserts a
border-rank equality, a positive-characteristic theorem or a general-n result.
The relevant tensor-rank reference is contextual, not a substitute for an
unrestricted Chow-rank lower bound.

Reference metadata and the separate withdrawn earlier arXiv record are reviewed
in [REFERENCES_AND_ARXIV.md](REFERENCES_AND_ARXIV.md). This is a targeted
citation/dependency check, not an exhaustive priority determination.

## Executed computation and integrity acceptance

The native environment is Windows 11, Python **3.14.4** and MiKTeX PDFLaTeX.
The reader's computational programs use only Python's standard library. Source
compatibility is declared for Python 3.11+; this second acceptance does not
pretend to have run an unavailable Python 3.11 interpreter.

Both original public entry points were run independently, and the prior r1
standalone packages were checked before making revisions. R2 was then tested
from a fresh extraction of the exact ZIPs, not merely from the developer's
source tree. For each paper, the full wrapper ran at inherited optimization
levels 0, 1 and 2 and once from a foreign working directory. All passed.
The 19 active ancillary Python files contain no Python `assert` checks that
would disappear in optimized execution.

The original perm6 finite-core program covers **2,391,496** labelled bipartite
edge sets and all **45,696** parameterized symbol cases. The independent
normal-form computations agree with all five actual dimension pairs. The
Glynn expansions check **50,000** signed row choices for perm5 and **1,492,992**
for perm6, leaving **120** and **720** permutation monomials respectively.

The new independent prolongation checker reconstructs the entire cubic
coefficient system over exact rationals: 2,925 cubic monomials for perm5 and
8,436 for perm6. Its surviving spaces are exactly the 100 and 400 subpermanent
basis blocks. It imports neither the historical verifier nor its reference
JSON. This strengthens the finite evidence but does not turn the written
geometric and global arguments into a formal proof certificate.

All **8 negative probes** fail as expected under optimization: altered
certificate, missing certificate, duplicate source-manifest entry and extra
ancillary file, for each paper. Original expected certificate hashes are not
edited in these fixtures. The **16 release-contract tests** pass at normal
and optimized settings; they also test unsafe/missing source members,
fixed metadata, historical payload compatibility and no compression dependency.

Primary receipts: [release_acceptance.json](release_acceptance.json),
[release_contract_tests.json](release_contract_tests.json),
[prolongation_independent.json](prolongation_independent.json),
[checkout before](checkout_eol_before.json),
[checkout after](checkout_eol_after.json), and
[baseline acceptance](acceptance.json).

The first r2 acceptance-driver attempt hit a Windows cross-drive path-recording
error while reporting a temporary negative fixture. The recorder was fixed,
the incomplete receipt was preserved under `attempts/`, and the full acceptance
was repeated from a new extraction. This was not repaired by changing a
mathematical input or certificate.

## Compilation and PDF inspection

Both extracted sources compiled twice with automatic package installation
disabled and `-no-shell-escape`. No external graphics or bibliography build
step is required. Final logs have no missing references, rerun requests,
overfull boxes or underfull boxes. MiKTeX emits one benign epstopdf warning
that shell escape is disabled; no EPS conversion is used by these papers.
Accordingly this report does not claim literally warning-free native logs.

The final PDF page counts are **7** and **11**. All fonts are embedded, no
font file was extracted or distributed, there are no blank pages or embedded
attachments, and no word is outside its page bounds. All 18 pages were rendered
and visually reviewed. The final accepted renders were compared with the
reviewed draft; only perm6 page 5 changed and was separately re-inspected.
A second PDFium rendering was also generated for all pages.
See [PDF preflight](pdf_preflight.json) and [visual review](VISUAL_REVIEW.md).

The [current arXiv TeX page](https://info.arxiv.org/help/faq/texlive.html)
lists TeX Live 2023 and 2025, defaulting to 2025. Native MiKTeX acceptance is
useful local evidence, not a claim that the exact arXiv processor image was
executed. Its generated preview must still be checked during real submission.

## Preservation and remaining gates

The original public package trees, historical submission source trees, legacy
ZIPs/PDFs and their expected checksums were not changed. New inventories belong
to an explicit r2 revision. Root navigation and reproduction instructions now
select r2. No local Codex session, redundant scheduler, GitHub Actions dispatch,
quant database operation or data-provider request was used.

The remaining author/account actions are: approve the revised mathematical
content, authorship and relationship to earlier work; confirm the factual
AI-use disclosure, final metadata and license; check endorsement and current
submission capacity; inspect arXiv's generated PDF and ancillary list. The
account's remaining quota was not inspected. External peer review remains
unperformed, but is not misrepresented as a source-file compilation test or
an automatically satisfied condition of this internal audit.
