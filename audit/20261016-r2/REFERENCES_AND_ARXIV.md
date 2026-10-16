# Reference and arXiv requirement check — 2026-10-16

This check concerns the two manuscripts in `submissions/20261016-r2/`. It is a targeted dependency and metadata audit, not an exhaustive novelty search or a moderation decision.

## Mathematical references

**Glynn.** D. G. Glynn, *The permanent of a square matrix*, European Journal of Combinatorics 31(7) (2010), 1887–1891, DOI `10.1016/j.ejc.2010.01.010`. The publisher index and the author's institutional record agree with the bibliography. The displayed upper-bound identity is also proved by its sign-cancellation argument and independently expanded by the supplied exact-integer verifier; the lower bounds do not depend on an unverified quotation of this identity.

Sources: [publisher](https://www.sciencedirect.com/science/article/pii/S0195669810000211), [author's university record](https://researchnow.flinders.edu.au/en/publications/the-permanent-of-a-square-matrix).

**Ilten–Teitler.** N. Ilten and Z. Teitler, *Product Ranks of the 3 × 3 Determinant and Permanent*, Canadian Mathematical Bulletin 59(2) (2016), 311–319, DOI `10.4153/CMB-2015-076-1`. The citation's year, volume, issue, pages and DOI are correct. It supplies terminology and small-case context, not either new lower bound.

Sources: [publisher](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/product-ranks-of-the-3-3-determinant-and-permanent/500D1FBA4640EE1B4333186D75C5C8D9), [author preprint](https://arxiv.org/abs/1503.00822).

**Han–Song.** J. I. Han and J. Song, *The rank of the 5 × 5 permanent tensor is sixteen*, arXiv:2608.09708. The current abstract page lists v2, dated 2026-08-27, following v1 on 2026-08-10. Its theorem concerns tensor rank. A tensor-rank lower bound cannot simply be substituted for the unrestricted ordinary Chow-rank lower bound proved in the perm5 manuscript. The manuscript correctly makes that distinction and does not use Han–Song as a lower-bound lemma. The unversioned PDF retrieved during this audit bore a v1 stamp; current-version metadata was checked separately rather than treating that cached PDF as v2.

Source: [arXiv record and version history](https://arxiv.org/abs/2608.09708).

**Borel.** A. Borel, *Linear Algebraic Groups*, second edition, Graduate Texts in Mathematics 126, Springer, 1991, DOI `10.1007/978-1-4612-0941-6`. The publisher confirms this metadata. In perm6 it is background for fixed-point methods. The needed one-parameter projective specialization and its coordinate fixed-subspace consequence are explained in the manuscript; an unstated general Borel-fixed-point theorem is not a missing computational premise.

Source: [publisher](https://link.springer.com/book/10.1007/978-1-4612-0941-6).

## Earlier withdrawn work is not a proof dependency

The public arXiv record for Rongyu Xu and Edinah Gnang, *On the Chow-rank of the permanent*, arXiv:2311.05890, lists v3 and v4 as withdrawn and carries the comment “Wrong main theorem”. Neither r2 manuscript invokes that theorem. This audit does not restore the withdrawn claim, establish an arbitrary-n equality, or silently repair that separate arXiv record. Authorship and the appropriate relationship to earlier joint work remain matters for the author to confirm before submission.

Source: [withdrawn record](https://arxiv.org/abs/2311.05890).

## Technical requirements and policy applied

[Ancillary-file instructions](https://info.arxiv.org/help/ancillary_files.html) require a root-level `anc/` directory and say not to place TeX sources there. Therefore r2 includes the byte-exact computational subset of each original package, not the historical manuscripts inside `anc/original/`. The complete historical packages and r1 archives remain unchanged in this repository. Each r2 manuscript itself is a complete root-level `main.tex`.

[TeX submission instructions](https://info.arxiv.org/help/submit_tex.html) and [the supported TeX Live page](https://info.arxiv.org/help/faq/texlive.html) were checked. As of this check, arXiv supports TeX Live 2023 and 2025, with 2025 the default. Select PDFLaTeX. These sources have no external figures, bibliography database, custom font files, shell-escape requirement or dynamically generated TeX input. Native MiKTeX compilation is local evidence, not a claim that arXiv's exact processor has already accepted the upload.

The [generative-AI section of the moderation policy](https://info.arxiv.org/help/moderation/index.html) requires disclosure of significant use and retains responsibility with human authors. Both manuscripts now include a factual disclosure of ChatGPT's assistance with arguments, exposition, verification and submission materials. No author approval or external peer review is asserted by that disclosure.

The [official 2026-10-01 rate-limit announcement](https://blog.arxiv.org/2026/10/01/updated-rate-limit-policy/) and current moderation policy specify two new submissions per author per calendar month, and at most three active submissions. The author's current account usage was not inspected. Endorsement, license selection, final metadata and the actual server-generated preview must be checked in the submission workflow; preparing two valid source archives does not establish those account-side facts.
