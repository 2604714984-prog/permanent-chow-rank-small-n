# Internal audit: computation-free perm5 proof

Date: October 20, 2026. **Disposition: pass.**

Scope: the complete [current source](source/main.tex), SHA-256 `272fe8933808e7e58574a6588082005c0bd35a0dc6e1d1fc4b5939ccb47cd611`. No mathematical source bytes were changed during this audit and canonical publication.

Actual derivative images, not formal factor-product spans, enter the local polarization bound. The small-complement kernel lemma and a divisor formula cover every dependent factor span except one four-dimensional quotient case, which is treated by explicit derivatives. The squarefree triple formula covers independent factors. The rectangular image-span inequality and projected factor-span filtration yield h2 + Delta/2 <= 10N - 150; the endpoint N=15 is excluded.

The sign-sum upper bound is proved directly. All factor tuples, including dependent and repeated factors, and all relevant quotients are covered by the written argument. No computer-generated rank table or certificate is a premise. The result concerns ordinary Chow rank over every characteristic-zero field, not border rank or a general-size formula.

The [combined report](../../audit/20261020-computation-free/REPORT.md) gives the dependency review, independent analytical consistency argument, diagnostic counts and necessary-hypothesis counterexamples. [BUILD.json](BUILD.json) records source-only compilation. [Optional exact checks](verify_supplementary.py) are error-detection tools, not the proof.

This internal review is not external peer review or formal proof-assistant certification. The [earlier computation-assisted package](../archive/README.md) is retained separately with its original hashes.
