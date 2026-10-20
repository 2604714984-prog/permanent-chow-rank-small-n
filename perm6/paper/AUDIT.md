# Internal audit: computation-free perm6 proof

Date: October 20, 2026. **Disposition: pass.**

Scope: the complete [current source](source/main.tex), SHA-256 `a13191fce613d530ebb1634b373597e178a8f843b15707f0d8f3d65bff1f4b40`. No mathematical source bytes were changed during this audit and canonical publication.

The four-cycle and essential-variable arguments supply the permanent structure. The squarefree count treats quotient ranks at most five; full rank uses the actual permanent intersection, not the false assertion for arbitrary quadratic quotients. In five-dimensional factor span, actual squarefree derivatives and elementary product bounds give a codimension budget paid by half the middle-rank defect. The two global inequalities cancel the identical defect and force N>=32.

The sign-sum upper bound is proved directly. All factor tuples, including dependent and repeated factors, and all relevant quotients are covered by the written argument. No computer-generated rank table or certificate is a premise. The result concerns ordinary Chow rank over every characteristic-zero field, not border rank or a general-size formula.

The [combined report](../../audit/20261020-computation-free/REPORT.md) gives the dependency review, independent analytical consistency argument, diagnostic counts and necessary-hypothesis counterexamples. [BUILD.json](BUILD.json) records source-only compilation. [Optional exact checks](verify_supplementary.py) are error-detection tools, not the proof.

This internal review is not external peer review or formal proof-assistant certification. The [earlier computation-assisted package](../archive/README.md) is retained separately with its original hashes.
