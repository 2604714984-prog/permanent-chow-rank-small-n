# arXiv submission continuation — 2026-10-18

## Actual state

Release: **20261016-r2**, input commit `99c3af555199a8f7932e9bd720c1f0bf79bf2d74`.

| Paper | Archive preflight | arXiv workflow | arXiv-generated PDF / ancillary inspection | Public submission |
| --- | --- | --- | --- | --- |
| perm5 | PASS, 21 files | Existing incomplete draft; Start attempted; upload blocked by missing math.AG endorsement | Not performed: no files uploaded | Not submitted by this session |
| perm6 | PASS, 16 files | Not created; same account/category prerequisite remains unresolved | Not performed: no files uploaded | Not submitted by this session |

The author explicitly selected the **arXiv.org perpetual, non-exclusive license** for both papers and authorized acceptance of the Submission Agreement to continue upload/preview. In the existing perm5 draft, contact certification, authorship declaration, agreement acceptance, the non-exclusive license, and Mathematics / Algebraic Geometry were entered. Continue was used, but the endorsement validation failed. Reopening the draft later showed the Start controls reset; these declarations were not persisted as a completed Start step.

The server returned **"You are not endorsed for this archive."** The math.AG endorsement page explicitly requires endorsement from another user. Opening the site's request-endorsement link caused arXiv to report that it had sent an endorsement-code email to the account address. No code, private account information, or draft identifier is stored here; no request was forwarded to an endorser by this session.

The account page still lists the existing workflow as incomplete. Its title, source files, and metadata have not been entered. No second empty draft was opened, because math.AG eligibility is an account-level prerequisite for the intended route. No alternate category was selected to avoid the endorsement requirement. The current blocker is **math.AG endorsement**, not missing license consent, a compilation error, or exhausted submission capacity.

Final manuscript approval, confirmation of the existing AI-use disclosure, and permission to publicly submit remain outstanding. These should be obtained after the actual server-generated previews can be inspected. The user's upload/preview authorization does not authorize Submit Article.

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
- [Endorsement](https://info.arxiv.org/help/endorsement.html): the actual Start submission now confirms that this account is not endorsed for math.AG. The request page says an eligible endorser must have submitted four papers in the listed mathematics categories more than three months and less than five years ago; check an author's eligibility through the link on their article's abstract page. Endorsement is necessary but does not guarantee acceptance.
- [Moderation](https://info.arxiv.org/help/moderation/index.html): significant generative-AI assistance must be disclosed and human authors retain responsibility. Both r2 manuscripts already contain a disclosure covering argument development, auditing, exposition, verification, and submission materials. Its factual accuracy and completeness still require author approval.
- [Rate-limit announcement](https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/): two new submissions per calendar month, three active at once; the FAQ clarifies that limits attach to the submitter, across categories. Rejections count. Recheck actual remaining capacity before final submission.
- [Licenses](https://info.arxiv.org/help/license/index.html) and [Submittal Agreement](https://info.arxiv.org/help/policies/submission_agreement.html): the author must have rights to the work and included material. Each posted version's license is irrevocable. CC BY 4.0 permits attributed reuse/adaptation, including commercial use; arXiv's non-exclusive distribution license provides narrower reuse permissions. The author subsequently chose the arXiv non-exclusive license for both papers; it was selected in the attempted perm5 Start form. The blocked Start step did not persist those controls after reopening.

Recommended primary category: **math.AG**, based on the Chow/product-rank subject and the directly relevant [Ilten–Teitler paper](https://arxiv.org/abs/1503.00822), which is classified there. **cs.CC** is a possible cross-list if justified by the intended algebraic-complexity audience; it is not a substitute for an endorsement check. Existing MSC 2020 values remain 15A69, 14N05, 68V05. math.AG was used for the actual Start eligibility check; no cross-list has been entered.

## Relation to withdrawn joint work

[arXiv:2311.05890](https://arxiv.org/abs/2311.05890) remains withdrawn, with Rongyu Xu and Edinah Gnang listed as authors and the public reason identifying an incorrect main theorem. Its [v2 text](https://arxiv.org/html/2311.05890v2) develops general row-homogeneous, orbital and symmetric-polynomial arguments. The r2 papers instead claim unrestricted ordinary Chow ranks for n=5 and n=6 using derivative-space and quotient-symbol methods. This is evidence of different scope and proof organization, not proof of independent intellectual contribution or permission to omit attribution.

Neither current `main.tex` cites 2311.05890 or names Gnang. The author has now stated that the earlier joint paper is background only and that the earlier coauthor has no contribution to these new manuscripts. This resolves the contribution question on the basis of the author's statement and supports the proposed two-new-work route, subject to moderation; it is not an independent authorship determination. A withdrawn theorem must not be treated as valid evidence. Withdrawal does not erase the earlier record or eliminate appropriate attribution.

The [submission overview](https://info.arxiv.org/help/submit/index.html) requires corrections/errata to use replacement, and [replacement guidance](https://info.arxiv.org/help/replace.html) preserves version history. Moderation may consolidate similar submissions. No blanket rule was found requiring every distinct later paper to replace an earlier withdrawn paper. Accordingly, two new submissions are a proposed route, not a cleared moderation determination. If the author says these are corrections of the old work, resolve the replacement route before proceeding. If uncertainty remains, prepare a factual enquiry for arXiv support; do not send it without authorization.

Any needed manuscript citation, acknowledgement, or authorship change requires an explicit successor release and acceptance of the changed submission material. Do not silently patch r2 or edit historical certificate hashes.

## Resume procedure and approvals

1. Have a qualified arXiv author complete math.AG endorsement using the email arXiv sent to the account holder. Do not publish the code or forward it to anyone without the author's instruction.
2. Resume the existing perm5 draft and recheck eligibility and capacity. Identity/affiliation, contribution relationship, license selection for both papers, and agreement acceptance for upload/preview have already been authorized; do not ask again unless their substance changes.
3. Upload only the frozen perm5 r2 ZIP, select `main.tex` and PDFLaTeX, and retain every ancillary member. No full mathematical re-audit is needed.
4. Inspect the actual arXiv-generated PDF, logs, metadata, and downloadable ancillary files. Record observed page count and any processor-induced file changes. Do not label the local 7-page / 11-page PDFs as arXiv previews.
5. Create and process the separate perm6 draft using the already authorized non-exclusive license and agreement, after the shared eligibility gate is resolved.
6. Present both exact server previews, metadata, licenses, and any remaining warnings. Obtain explicit author approval of final content, AI disclosure, and public submission before Submit Article. Record private draft identifiers privately and publish only announced identifiers to the public handoff.

No source upload, server PDF generation, public submission, contact with an external endorser, or change to the withdrawn record occurred. The only automated message observed was arXiv's endorsement-code email to the account holder.

## Earlier author clarification — 2026-10-18, 11:21 Asia/Shanghai

The author confirmed the account identity and current affiliation, and authorized correction of the affiliation spelling. The profile correction was saved and the account page confirmed success. Private contact details remain outside this repository.

The author stated that the new manuscripts contain no contribution from the earlier coauthor and that the withdrawn joint paper is research background only. This records the author's contribution statement; it is not an independent authorship determination. This resolves the contribution question previously marked open and supports proceeding with the proposed two-new-work route, subject to arXiv moderation. No manuscript text or attribution was changed.

The author asked for an explanation of license differences, rather than selecting a license. License choice and acceptance of the Submittal Agreement remain unapproved. The existing draft is still incomplete; no source files have been uploaded. Approval of final content, AI disclosure, and public submission remains outstanding.

## Subsequent license authorization and eligibility result — 2026-10-18

The author then explicitly chose the arXiv non-exclusive license and accepted the Submission Agreement for both upload/preview workflows. This supersedes the earlier license-pending note above. The agreement was accepted through the actual terms dialog and Continue was used on the perm5 Start form. The server's math.AG endorsement requirement prevented progression to Add Files. The frozen r2 artifacts and mathematical evidence remain unchanged.
