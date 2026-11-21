# Engine: Inductive onset residual

**Module:** `ValaQuenta/modules/inductive_onset_residual` · `maths.py` + `tools.py` · **Registry name:** `inductive_onset_residual` · **Version:** 0.2 · **Equations:** 10
**Replaces:** `bao_mass_gap` (2026-11-21). The old name is retired because no BAO data, scale or measurement enters the residual.
**Name:** from the Inductive Self-Adjoint Geometric Coupling Hamiltonian (Ĥ_RB); the primes are its inductive base cases, and the construction below is also an induction.

## What it computes (all of it runs)

1. **`induction`**: iterate x → e^(−x). The error shrinks by W(1) per step, so the iteration gains −log₁₀ W(1) digits per step; because ln W(1) = −W(1), that rate is W(1)/ln 10 = **0.2463072015**, the Boundary face of d*. Measured from five starting values: 0.24630720 to about seven digits.
2. **`running_value`**: the d* the code runs with, `engine.constants.D_STAR = 0.24600`, beside the induced rate.
3. **`onset_residual`**: Δ = W(1) − D_STAR·ln 10 = **0.000707357533** = ln 10 · (d*_induced − d*_running); the two d* agree on 3 decimals; Δ · 10³ = 0.70736.
4. **`hub_fiber`**: 0_RB is pure e₀; `box_kite.fixed_point_weight` gives 1 − depth² for a fiber; the depth at which the weight equals W(1), d*, ½.
5. **`couplings`**: G_p(σ) = p^(−σ) of Ĥ_RB at the σ facets; G₂(½) = 2^(−½).
6. **`explicit_formula`**: ψ(x) from the zeros (each γ > 0 counted with its conjugate) against the exact Chebyshev ψ. At x = 10.5 with 20 zeros the error is −0.248.
7. **`census`**: a live scan of the sibling repositories for the files that write each d* value (about 120 code files write 0.246/0.24600; about 15 write 0.2463x).
8. **`symbols`**: which symbol names which constant, by source. The sources disagree (the codebase: Ω_ζΣ = W(1), A_π = 1/137.036; the RHP measurement: d* on the Riemann/entropy side, W(1) on the Fermat/inertia side; the author, 2026-11-21: Ω_RZ = d*, A_Fermat = W(1)). Recorded, not settled.
9. **`validate`**: ten checks, each comparing two independently computed quantities (no check compares a constant to itself).

## Readings (not computed; see `maths.interpretations()`)
BAO residual, Yang–Mills mass gap, M-theory compactification scale, "a point becomes a circle", G₂(½) = 1/√2: each is `CONJECTURE`, with what it would take to test it.

## Record
- `experiments/inductive_onset_tests.py`: both readings of "inductive" tested against the numbers (predictions registered first).
- Note on the Higgs VEV, the first-day near-identity and Ĥ_RB: `modules/h_rb_hat/NOTES_2026-11-21_d_star_and_the_vev.md`.
- The previous engine's text is kept in `modules/inductive_onset_residual/NOTES_2026-08-31_bao_mass_gap_original.md`.

## Use
```python
from ValaQuenta.modules.inductive_onset_residual import maths as m
m.summary(); m.induction(); m.onset_residual(); m.census(); m.validate()
```

## Labels removed 2026-11-21 (tested, then stripped)
`BAO` and `Yang–Mills mass gap` were names for Δ = A_π − d*·ln 10 in the wiki, notebooks and docstrings. `FourthAgePapers/DStar/bao_test.py` registered the prediction that no expression of {A_π, Ω_ζΣ, φ, π, e, ln 10, Δ} reproduces z_drag, z_*, θ_* or ℓ_A within Planck's errors more often than chance, and it held (0 hits on each target, against 0.05–0.13 expected). No engine line computes a BAO quantity. The names are removed from the wiki, notebooks and docstrings. `telperion.py` keeps `BAO_MPC = 150 Mpc` because that is the measured physical scale used for the watch-second calculation. The tier-7/8 statements "zeros = BAO frequencies" and "Hermite zeros = BAO timing marks" are separate claims, not covered by this test; they are listed in `wiki/STALENESS_CATALOG.md`.
