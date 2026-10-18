# arXiv submission continuation — 2026-10-18

## Actual state

Release: **20261016-r2**, input commit `99c3af555199a8f7932e9bd720c1f0bf79bf2d74`.

| Paper | Archive preflight | arXiv source upload | arXiv-generated PDF / ancillary inspection | Public submission |
| --- | --- | --- | --- | --- |
| perm5 | PASS, 21 files | Not performed | Not performed | Not submitted by this session |
| perm6 | PASS, 16 files | Not performed | Not performed | Not submitted by this session |

An authenticated author session was inspected. One empty new-submission workflow was opened, intended for perm5; its title and files have not been entered. No second draft was opened. Resume that existing workflow rather than creating duplicates. Private account details and draft identifiers are intentionally not included in this public repository.

The actual Start page requires contact-information certification, acceptance of the Submission Agreement, authorship declaration, and license selection **before Add Files**. All those controls remain unaccepted/unselected. Mathematics / Algebraic Geometry was selected in the current form only; it has not been submitted. Category availability does not prove math.AG endorsement.

The author explicitly reserved identity, final manuscript, license, and public submission decisions. Permission to upload and preview does not authorize accepting those declarations. The first blocking gate is therefore author confirmation, not compilation.

## Frozen package preflight

See [machine-readable receipt](package_preflight.json). The ZIP bytes were fetched from the pinned commit, decoded without rebuilding, and checked locally against the frozen SHA-256 list. ZIP CRCs, safe paths, uniqueness, every SOURCE_MANIFEST payload hash, and all 37 member Git blob IDs match. No manuscript, certificate, expected hash, source archive, or prior audit record was edited. No mathematical verification was rerun and no CI was requested.

| Item | perm5 | perm6 |
| --- | --- | --- |
| Bytes | 156187 | 108705 |
| ZIP members / ancillary files | 21 / 20 | 16 / 15 |
| Form abstract characters | 529 | 841 |
| Root TeX | main.tex | main.tex |
| Intended processor | PDFLaTeX | PDFLaTeX |

Archive SHA-256:
- perm5: `47dafb5120877b536ddbebf5a2c1b5052d254a147a3dc3d50b952fa07ccf3057`
- perm6: `3a90428a827e1c808f928e2d0d172c7835fe3604d6c16997180d7e77834a0c15`

Both titles and the source author Rongyu Xu match the prepared metadata. Each exact source abstract matches its metadata entry; the form abstract differs only by whitespace normalization, macro expansion and inline-math delimiters. Both form abstracts are ASCII and below arXiv's 1920-character limit. No institutional affiliation is asserted in either manuscript. Do not copy an unconfirmed affiliation from an account into the paper.

## Current policy and classification

Official pages were read on 2026-10-18.

- [Submission overview](https://info.arxiv.org/help/submit/index.html): use TeX sources; inspect the processor PDF and metadata before Submit Article.
- [Ancillary instructions](https://info.arxiv.org/help/ancillary_files.html): keep the root `anc/` directory. There are no TeX or PDF files inside these packages' ancillary directories.
- [TeX Live support](https://info.arxiv.org/help/faq/texlive.html): 2025 is the default; 2023 is also available. Local MiKTeX acceptance remains distinct from arXiv processor acceptance.
- [Metadata](https://info.arxiv.org/help/prep.html): author identity and affiliation must be accurate, and all authors must consent.
- [Endorsement](https://info.arxiv.org/help/endorsement.html): a new category can require endorsement. This has not been established for math.AG.
- [Moderation](https://info.arxiv.org/help/moderation/index.html): significant generative-AI assistance must be disclosed and human authors retain responsibility. Both r2 manuscripts already contain a disclosure covering argument development, auditing, exposition, verification, and submission materials. Its factual accuracy and completeness still require author approval.
- [Rate-limit announcement](https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/): two new submissions per calendar month, three active at once; the FAQ clarifies that limits attach to the submitter, across categories. Rejections count. Recheck actual remaining capacity before final submission.
- [Licenses](https://info.arxiv.org/help/license/index.html) and [Submittal Agreement](https://info.arxiv.org/help/policies/submission_agreement.html): the author must have rights to the work and included material. Each posted version's license is irrevocable. CC BY 4.0 permits attributed reuse/adaptation, including commercial use; arXiv's non-exclusive distribution license provides narrower reuse permissions. No license was chosen.

Recommended primary category: **math.AG**, based on the Chow/product-rank subject and the directly relevant [Ilten–Teitler paper](https://arxiv.org/abs/1503.00822), which is classified there. **cs.CC** is a possible cross-list if justified by the intended algebraic-complexity audience; it is not a substitute for an endorsement check. Existing MSC 2020 values remain 15A69, 14N05, 68V05. Final category choice remains for author approval.

## Relation to withdrawn joint work

[arXiv:2311.05890](https://arxiv.org/abs/2311.05890) remains withdrawn, with Rongyu Xu and Edinah Gnang listed as authors and the public reason identifying an incorrect main theorem. Its [v2 text](https://arxiv.org/html/2311.05890v2) develops general row-homogeneous, orbital and symmetric-polynomial arguments. The r2 papers instead claim unrestricted ordinary Chow ranks for n=5 and n=6 using derivative-space and quotient-symbol methods. This is evidence of different scope and proof organization, not proof of independent intellectual contribution or permission to omit attribution.

Neither current `main.tex` cites 2311.05890 or names Gnang. Prior handoffs also leave this relationship unresolved. The author must explain whether earlier joint results, proof ideas, text, or other contributions carry into either new paper, and whether attribution, acknowledgement or coauthorship is needed. A withdrawn theorem must not be treated as valid evidence. Withdrawal does not erase the earlier record or eliminate appropriate attribution.

The [submission overview](https://info.arxiv.org/help/submit/index.html) requires corrections/errata to use replacement, and [replacement guidance](https://info.arxiv.org/help/replace.html) preserves version history. Moderation may consolidate similar submissions. No blanket rule was found requiring every distinct later paper to replace an earlier withdrawn paper. Accordingly, two new submissions are a proposed route, not a cleared moderation determination. If the author says these are corrections of the old work, resolve the replacement route before proceeding. If uncertainty remains, prepare a factual enquiry for arXiv support; do not send it without authorization.

Any needed manuscript citation, acknowledgement, or authorship change requires an explicit successor release and acceptance of the changed submission material. Do not silently patch r2 or edit historical certificate hashes.

## Resume procedure and approvals

1. Obtain the author's confirmation of identity and current account contact/affiliation details. Correct a confirmed profile typo only with authorization; do not infer current affiliation from historical study status.
2. Resolve the contribution relationship and proposed new-work route. Confirm the two r2 proofs and AI disclosure, or make an explicitly authorized successor release.
3. Obtain a specific license choice and authorization to accept the actual Submittal Agreement, while keeping public submission separately gated.
4. Resume the existing empty draft; confirm math.AG eligibility and capacity, upload only the perm5 r2 ZIP, select `main.tex` and PDFLaTeX, retain every ancillary member.
5. Inspect the actual arXiv-generated PDF, logs, metadata, and downloadable ancillary files. Record observed page count and any processor-induced file changes. Do not label the local 7-page / 11-page PDFs as arXiv previews.
6. Create and process the separate perm6 draft in the same way.
7. Present both exact server previews, metadata, licenses, and any remaining warnings. Obtain explicit final authorization before Submit Article. Record actual status transitions and identifiers privately, publishing only announced identifiers to the public handoff.

No public submission, license acceptance, author certification, external message, or change to the withdrawn record occurred in this continuation.

## Author clarification — 2026-10-18, 11:21 Asia/Shanghai

The author confirmed the account identity and current affiliation, and authorized correction of the affiliation spelling. The profile correction was saved and the account page confirmed success. Private contact details remain outside this repository.

The author stated that the new manuscripts contain no contribution from the earlier coauthor and that the withdrawn joint paper is research background only. This records the author's contribution statement; it is not an independent authorship determination. This resolves the contribution question previously marked open and supports proceeding with the proposed two-new-work route, subject to arXiv moderation. No manuscript text or attribution was changed.

The author asked for an explanation of license differences, rather than selecting a license. License choice and acceptance of the Submittal Agreement remain unapproved. The existing draft is still incomplete; no source files have been uploaded. Approval of final content, AI disclosure, and public submission remains outstanding.
