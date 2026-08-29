# Engine: Σ_RB  RedBlue Summed Integral

**Module:** `modules/h_rb_hat/`  
**Version:** 0.120  
**Confidence floor:** THEORETICAL  
**Notebooks:** [h_rb_hat/01_fermat_riemann_dual_currents.ipynb](../notebooks/h_rb_hat/01_fermat_riemann_dual_currents.ipynb)  
**Claim:** One summed integral Σ_RB, evaluated at different σ, reproduces GR (σ=2), Yang-Mills (σ=1), QM (σ=½) and Riemann (σ=½) as facets.

---

## What it computes

Σ_RB = Σ_p p^{-σ} [R̂_p ⊗ ∂̂_∂M + ∂̂_∂M† ⊗ B̂_p]. The RedBlue Summed Integral. The Boundary Generator. The Σ is the summation sign. The RB is Red-Blue. The existence of a distinction. Facet projections: GR (σ=2), Yang-Mills (σ=1), QM/RH (σ=½), NS (σ=1, Im=0), Noether (boundary invariant), Fermat (forbidden zone). All six open Clay Millennium Problems project from this operator.

The facet equations are the substance: each returns the σ it lives at and its coupling sum. QM and Riemann both return σ=0.5 with coupling sum 4.9896332508 — the same number, which is the module's central claim.

`facet_fermat` is the interesting one: it returns σ='< ½ (forbidden zone)'. Fermat is not a facet at a value of σ, it is the statement that a region of σ is unreachable.

`self_adjoint_demonstration` is ESTABLISHED and states the operative principle: self-adjointness preserves truth, not form.

## Results — run 2026-07-28

16/16 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `euler_product` | ESTABLISHED | ✓ | {'result': (583.7119433744068+0j), 'magnitude': 583.7119433744068} |
| `facet_fermat` | ESTABLISHED | ✓ | {'facet': "Fermat's Last Theorem", 'sigma': '< ½ (forbidden zone)', 'theorem': 'No aⁿ + … |
| `facet_gr` | ESTABLISHED | ✓ | {'facet': 'General Relativity', 'sigma': 2.0, 'coupling_sum': 0.4497032182086859, 'actio… |
| `facet_noether` | ESTABLISHED | ✓ | {'facet': 'Noether Current', 'sigma': 'all σ', 'theorem': 'Every continuous symmetry → o… |
| `facet_qm` | ESTABLISHED | ✓ | {'facet': 'Quantum Mechanics', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'equatio… |
| `oblique_crank` | ESTABLISHED | ✓ | {'identification': 'The Witches Hat half-angle IS the oblique crank throw', 'crank_throw… |
| `precession_stroke` | ESTABLISHED | ✓ | {'identification': 'Precession revolution = L_(I\|O) cycle (one complete I→O→I)', 'half_… |
| `self_adjoint_demonstration` | ESTABLISHED | ✓ | {'statement': 'Self-adjointness preserves truth, not form.', '1_equals_1': 1, '1_factori… |
| `sigma_rb_baseline` | ESTABLISHED | ✓ | {'engine': 'SIGMA_RB', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'forcing_conditi… |
| `trine_configuration` | ESTABLISHED | ✓ | {'identification': 'Three quantum-force levels = three Wankel faces = trine', 'sigma_lev… |
| `dark_matter_halo` | THEORETICAL | ✓ | {'galaxy_size_ly': 50000.0, 'period_yr': 100000.0, 'frequency_per_yr': 1e-05, 'wavelengt… |
| `facet_navier_stokes` | THEORETICAL | ✓ | {'facet': 'Navier-Stokes', 'sigma': 1.0, 'imaginary': 0.0, 'coupling_sum': 1.74286691688… |
| `facet_riemann` | THEORETICAL | ✓ | {'facet': 'Riemann Zeta / Berry-Keating', 'sigma': 0.5, 'coupling_sum': 4.98963325080609… |
| `facet_yang_mills` | THEORETICAL | ✓ | {'facet': 'Yang-Mills / Standard Model', 'sigma': 1.0, 'coupling_sum': 1.742866916886003… |
| `sigma_phase_diagram` | THEORETICAL | ✓ | {'diagram': [{'sigma': 0.0, 'theory': 'Trivial / Poincaré', 'euler_mag': 1.0, 'euler_re'… |
| `sigma_rb_evaluate` | THEORETICAL | ✓ | {'sigma': 0.5, 'x': 1.0, 'p_momentum': 1.0, 'n_primes': 20, 'terms': [{'prime': 2, 'sigm… |

## Open

- Roughly half this module is THEORETICAL, including the σ phase diagram and the Navier-Stokes facet.
- `dark_matter_halo` produces a galactic period from a 50,000 ly galaxy; it is a consistency check, not an independent measurement.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| Ĥ_RB and its σ-facets (GR σ=2, YM σ=1, QM/Riemann σ=½) | project Ĥ_RB at each σ | 0 · SIGN | TELPERION | DEFINITIONAL | **FLAGGED** — deficit: a rigorous self-adjoint domain for Ĥ_RB (⇒ real spectrum) |

Calibration: this verdict agrees with the page's stated status (**THEORETICAL**).

### Piece-by-piece — does the equation's shape match what 0_RB requires?

`SedenionFactoralRelativity/engine/valaquenta_calibration.py :: decompose_h_rb_hat()`
decomposes `Σ_RB = Σ_p p^{-σ}[R̂_p ⊗ ∂̂_∂M + ∂̂_∂M† ⊗ B̂_p]` against the tier‑0
floor, then compares its shape to **0_RB** — the operator the geometries
*require* ("read off all the geometric operators at once when each is empty but
present").

| piece | tier · root | Two Trees | reading |
|---|---|---|---|
| `Σ_p` | 0 · ADD | — | forward accumulation; the Dirichlet march |
| `p^{-σ}` (G_p) | 0 · SCALE | — | `p⁰=1` at σ=0 (the identity); **σ is the real scalar that selects the facet** |
| `R̂_p = xp` | 0 · SCALE | LAURELIN | Berry–Keating; Red; "what IS" — a product |
| `B̂_p = ½p² + ℘(x;g₂,g₃)` | 2 · SIGN | TELPERION | Fermat–Weierstrass; Blue; "what CANNOT BE" — a fixed landscape; ℘ doubly-periodic = the lattice ± |
| `∂̂_∂M` | 1 · SIGN | MINGLING | REFLECT — ∂M is a reflection locus; the seam between Red and Blue (J₃) |
| `⊗` | 0 · SCALE | — | a product structure |
| `†` (`R̂_p† = B̂_p`) | 0 · SIGN | MINGLING | the functional equation ξ(s)=ξ(1−s) as an involution — one bit, `†∘†=id` |
| `+` | 0 · ADD | — | the two-term sum |
| `Σ_RB = Σ_RB†` | 2 · SIGN | MINGLING | self-adjointness = the fixed set of `†` — **this IS the σ=½ locus** |

**Shape match — YES.** Same tier‑0 floor: all of ADD·SCALE·SIGN present, same
roles, weighted **2·ADD / 3·SCALE / 4·SIGN** — the operator is SIGN‑heavy, and
correctly so: it is fundamentally a *reflection* (the functional equation, the
boundary ∂̂, and self‑adjointness are all SIGN). Same Two‑Trees span (Telperion
B̂ ⊕ Laurelin R̂ ⊕ Mingling ∂̂/†/σ=½ — the *whole tree*, which is the signature
of 0_RB itself). Same **8 independent DOF** (the octonion core, `σ_RB[k]=σ_RB[k⊕4]`,
engine e10). Same †‑fixed self‑adjoint structure.

**The one divergence:** the equation carries **one import** the geometry does
not — *"a dense domain on which Σ_RB is essentially self-adjoint (deficiency
indices (0,0))"* (the OP‑4 / C1 open item). That single import **is** the gap
between "the equation has the right shape" and "the equation is proven" — and
it is the same *kind* of import RH carries (the zero‑set locus), which is
consistent: they are the same operator (Σ_RB self‑adjoint ⇒ RH by Stone).
