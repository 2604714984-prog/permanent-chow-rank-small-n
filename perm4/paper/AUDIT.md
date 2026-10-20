# Internal audit: computation-free perm4 proof

Date: October 20, 2026. **Disposition: pass.**

Scope: the complete [current source](source/main.tex), SHA-256 `263843c3a06f3f9d5d74c2eaa410afac107d8be0f7d806a97c0791fdbcafcca1`. No mathematical source bytes were changed during this audit and canonical publication.

The gradient description of the Koszul kernel proves the base ranks 560 and 92. The missing-derivative classification covers repeated interior variables and reconnects the one missing matching comparison. Row-column scaling gives the uniform rank-99 quotient statement in the correct specialization direction. Low-rank quadratic structure and row/image intersection bounds then give the residual rank 559, contradicting 552 for six terms.

The sign-sum upper bound is proved directly. All factor tuples, including dependent and repeated factors, and all relevant quotients are covered by the written argument. No computer-generated rank table or certificate is a premise. The result concerns ordinary Chow rank over every characteristic-zero field, not border rank or a general-size formula.

The [combined report](../../audit/20261020-computation-free/REPORT.md) gives the dependency review, independent analytical consistency argument, diagnostic counts and necessary-hypothesis counterexamples. [BUILD.json](BUILD.json) records source-only compilation. [Optional exact checks](verify_supplementary.py) are error-detection tools, not the proof.

This internal review is not external peer review or formal proof-assistant certification. The [earlier computation-assisted package](../archive/README.md) is retained separately with its original hashes.
