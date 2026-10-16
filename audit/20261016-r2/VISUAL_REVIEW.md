# Final PDF visual review

The two final PDFs are those compiled from fresh, accepted r2 ZIP extractions,
not the historical preview PDFs. Their exact hashes and font/page preflight
are recorded in `pdf_preflight.json` and `release_artifacts.json`.

All seven perm5 pages and all eleven perm6 draft pages were rendered and
visually inspected. The final accepted PDFs were rendered again at the same
scale and compared pixel by pixel with those reviewed draft renders. Every
perm5 page and ten of the eleven perm6 pages were identical. The only changed
page was perm6 page 5, where the 45,696-case indexing was clarified. That
final page was separately opened and visually re-inspected.

No clipping, overlapping text, missing glyphs or malformed tables were found.
The title pages, formula-heavy local/global sections, explicit perm5 minors,
long ancillary program paths, AI disclosures and reference lists were checked.
All fonts are embedded according to PDF font-descriptor metadata. No font
files were extracted or added to the source packages. No blank page or word
outside its physical page bounds was detected, and neither paper requires
external figure files.

The native MiKTeX final log retains one benign epstopdf warning about disabled
shell escape. There are no EPS figures or conversions in either manuscript,
and no unresolved references, rerun requests or overfull/underfull boxes in
the final log. The actual arXiv-generated preview still requires review at
submission; a local preview is not that server-side approval.

A separate PDFium rendering covered all 18 final pages. The five contact
sheets were visually inspected as a second-renderer check; no clipping,
missing glyphs or disrupted mathematical layout was observed.
