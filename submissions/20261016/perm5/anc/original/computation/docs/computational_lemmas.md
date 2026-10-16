# Computational Lemmas for the Five-by-Five Permanent

The written proof uses the following finite computations.

| Lemma | Program | Exact conclusion |
|---|---|---|
| One-intersection endpoint | [`perm5_one_intersection_independent_multifield.py`](../scripts/perm5_one_intersection_independent_multifield.py) | All 886,464 flags are checked over each of `F_3`, `F_5`, and `F_7`; every extremum is rechecked over `Q`, giving maxima `22, 26, 22`. |
| Fixed-six state exhaustion | [`perm5_fixed_six_state_table.py`](../scripts/perm5_fixed_six_state_table.py) | Exactly 58 admissible states are assigned uniquely to the eight routes. |
| Relative parent table | [`perm5_d11_d12_parent_table_independent.py`](../scripts/perm5_d11_d12_parent_table_independent.py) | Streaming all 53,130 coordinate five-planes gives maxima `4, 4, 5, 7`. |
| Terminal rank gap | [`perm5_terminal_independent_verification.py`](../scripts/perm5_terminal_independent_verification.py) | The 4,100-vertex tangent graph and rational Fourier calculation give `2215 > 2205`. |
| Glynn identity | [`perm5_glynn_upper_bound_independent.py`](../scripts/perm5_glynn_upper_bound_independent.py) | Exact expansion gives coefficient one on the 120 permutation monomials and zero on the other 3,005 row-choice monomials. |

The stored state table and terminal calculation are in [`evidence/`](../evidence/).
Run every computation from the repository root with:

```text
python -B perm5/verify_all.py
```
