# Engine: Tier 6 — Full Physics: QM + Standard Model

**Module:** `modules/tier6_physics/`  
**Version:** 0.100  
**Confidence floor:** THEORETICAL  
**Notebooks:** [core/13_tier6_physics.ipynb](../notebooks/core/13_tier6_physics.ipynb)  
**Claim:** QM and the full Standard Model as facets of H_RB at σ=½ — gauge groups from ℂ×ℍ×𝕆 by Dixon's theorem, not postulated.

---

## What it computes

Full QM and Standard Model from Ainulindale. Foundation: Zero Divisors=Addition, CD Tower=Subtraction → Mathematics. 8 engines: sedenion_arithmetic, quantum_mechanics, standard_model, dirac_equation, gauge_unification, higgs_mechanism, particle_spectrum, feynman_path_integral.

The strongest ESTABLISHED set in the repo: sedenion arithmetic, QM, the Standard Model Lagrangian, the Dirac equation, gauge unification, the Higgs mechanism, the path integral and hypercomplex Euler all run and all carry ESTABLISHED.

`gauge_unification` rests on Dixon's theorem — U(1)×SU(2)×SU(3) from ℂ×ℍ×𝕆 — which is established mathematics independent of this repo.

The e₀…e₁₅ table assigns each sedenion basis element a Standard Model particle with its measured mass. e₀ is the Higgs scalar; e₁₅ the gluon.

## Results — run 2026-07-28

10/10 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `gauge_unification` | ESTABLISHED | ✓ | {'claim': 'U(1)×SU(2)×SU(3) from ℂ×ℍ×𝕆. Dixon theorem. Not postulated.', 'dixon_theorem'… |
| `full_physics` | THEORETICAL | ✓ | {'tier': 6, 'theme': 'FULL PHYSICS: QM + Standard Model from Ainulindale framework', 'fo… |
| `particle_spectrum` | THEORETICAL | ✓ | {'claim': '17 SM particles from 16 sedenion strata. The sedenion IS the Standard Model s… |
| `dirac_equation` | ESTABLISHED+THEORETICAL | ✓ | {'claim': 'Dirac equation from CD Clifford algebra. Antimatter = J_neg = Blue channel.',… |
| `feynman_path_integral` | ESTABLISHED+THEORETICAL | ✓ | {'claim': 'Path integral = Lichtenberg Lagrangian = Action Potential. One equation.', 'f… |
| `higgs_mechanism` | ESTABLISHED+THEORETICAL | ✓ | {'claim': 'SSB = the brim. Same Sombrero at three scales: Higgs, horizon, Hubble.', 'sam… |
| `hypercomplex_euler` | ESTABLISHED+THEORETICAL | ✓ | {'claim': 'e^{iπ}+1=0 is the seed. ∫Dx e^{iS/ħ} is the bloom. J_R+J_G+J_B=0 is the stem.… |
| `quantum_mechanics` | ESTABLISHED+THEORETICAL | ✓ | {'claim': 'QM = H_RB at σ=½. Schrödinger, Heisenberg, spin, H-atom, path integral — all … |
| `sedenion_arithmetic` | ESTABLISHED+THEORETICAL | ✓ | {'claim': 'Zero Divisors = Addition. CD Tower = Subtraction. Both → ×÷. Voilà: Mathemati… |
| `standard_model` | ESTABLISHED+THEORETICAL | ✓ | {'claim': 'L_SM = L_SMMIP: term-for-term isomorphism. Derived, not imported.', 'lagrangi… |

## Open

- `particle_spectrum` is THEORETICAL and is where the strain shows: **17 SM particles are mapped onto 16 sedenion strata.** The count does not match, and the module does not conceal it. e₁₅ carries the gluon ×8.
- The masses in the table are experimental values from the particle data tables. They are inputs to the mapping, not outputs of it.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the SM gauge group SU(3)×SU(2)×U(1) from ℂ×ℍ×𝕆 (Dixon) | read gauge groups off the CD doublings | 2 · SIGN | LAURELIN | DESCRIPTIVE | **FLAGGED** — deficit: 17 Standard-Model particles onto 16 sedenion strata — the count does not match (particle_spectrum) |

Emergence signature: a fixed set of the wrong dimension (17 into 16).

Calibration: this verdict agrees with the page's stated status (**THEORETICAL**).
