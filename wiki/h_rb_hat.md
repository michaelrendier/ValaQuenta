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
