# Engine: Tier 0 Constants — π φ e √ i derived from H_RB

> d* faces (all four are needed to chart ln(10) in Universal Native Space):  
>   d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)  
>   d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)  
>   d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)  
>   d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)  
> Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG  


**Module:** `modules/constants/`  
**Version:** 0.130  
**Confidence floor:** THEORETICAL (the lowest tier in the formulary: `derive_alpha_fermat`)  
**Notebooks:** [core/01_constants.ipynb](../notebooks/core/01_constants.ipynb)  
**Claim:** π, φ, e, √, i and Λ are each read as a σ-facet of Ĥ_RB. The identities are ESTABLISHED; that the engine produces the constants rather than rewriting inputs it supplies is THEORETICAL and not demonstrated ([Ainulindale wiki 22 §6](https://github.com/michaelrendier/Ainulindale/blob/main/wiki/22_constant_facets.md)).


**Reference:** every equation with its parameters — [toolbox](toolbox/03_constants.md) · API — [constants](https://michaelrendier.github.io/ValaQuenta/api/modules/constants.html). This page is the record; it holds no API.

---

## What it computes

Tier 0 Root Constants: π, φ, e, √, i, A_PI, α_F, d*, Λ — each read at a σ-facet of Ĥ_RB. Two ceilings bound the domain [α_F, A_PI]. d* has four named faces (Boundary, Flow, Stability, Translator). Λ: J_neg at cosmological scale; Sombrero = Hawking pair; A_PI = de Sitter attractor. Einstein wrote it in 1915, removed it 1917, universe re-inserted 1998 at 40σ.

Each `derive_*` equation returns the constant together with the σ facet it corresponds to — σ=i is pure phase, σ=½ the critical line, σ=e thermodynamic, σ=π gauge normalisation, σ=φ the recursion eigenvalue.

`derive_omega_zs` returns A_PI = 0.5671432904097838, which is W(1), the Lambert W function at 1 — an exact special-function value, not a measurement.

## Results — run 2026-07-28

11/11 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `all_constants` | ESTABLISHED | ✓ | {'tier': 'Tier 0 — Root Constants + Ceilings + Domain + Λ', 'claim': 'All root constants… |
| `derive_e` | ESTABLISHED | ✓ | {'constant': "e (Euler's number)", 'sigma_facet': 'σ = e (thermodynamic — Boltzmann part… |
| `derive_i` | ESTABLISHED | ✓ | {'constant': 'i (imaginary unit)', 'sigma_facet': 'σ = i (pure phase — democratic)', 'ph… |
| `derive_omega_zs` | ESTABLISHED | ✓ | {'constant': 'A_PI (A_π)', 'value': 0.5671432904097838, 'sigma_facet': 'Domain ceil… |
| `derive_phi` | ESTABLISHED | ✓ | {'constant': 'φ (golden ratio)', 'sigma_facet': 'σ = φ (recursion eigenvalue — structura… |
| `derive_pi` | ESTABLISHED | ✓ | {'constant': 'π (circle constant)', 'sigma_facet': 'σ = π (gauge normalisation — U(1) la… |
| `derive_sqrt` | ESTABLISHED | ✓ | {'constant': '√ (square root)', 'sigma_facet': 'σ = ½ (the critical line IS the square r… |
| `euler_identity` | ESTABLISHED | ✓ | {'identity': 'e^{iπ} + 1 = 0', 'type': 'Theorem of RedBlue Geometries Engine', 'assembly… |
| `derive_alpha_fermat` | THEORETICAL | ✓ | {'constant': 'α_F (α / fine structure constant)', 'value': 0.0072973525692838… |
| `derive_d_star` | ESTABLISHED (d*_taut, d*_ln(10)); OPEN (d*_RG numeric) | ✓ | {'constant': 'd* (BK spectral floor, 4 components)', 'value_real': 0.246, 'sigma_facet':… |
| `derive_lambda` | σ=∞ (existence); σ>40 (Nobel 1998); OPEN (value from f) | ✓ | {'constant': 'Λ (Einstein cosmological constant)', 'value_omega_lambda': 0.6889, 'sigma_… |

## Open

- `derive_alpha_fermat` (fine structure constant) is the one equation here at THEORETICAL rather than ESTABLISHED. It is the weakest link in the Tier 0 chain and is marked as such.
- `derive_lambda`'s tier label is now ESTABLISHED (existence; observed at 40 standard deviations, 1998) / OPEN (value). It formerly read σ=∞, which is not a registry tier and collided with the coupling σ; fixed 2026-11-26.
- Withdrawn in 0.130 and kept as the record: the Cayley-Dickson tower reading of d\* (d*_ℝ+d*_ℂ+d*_ℍ+d*_𝕆 → ln 10) and the label "BAO first acoustic peak" on d*·ln 10 = 0.56644. `derive_d_star` now returns the four faces from `engine.constants`; `A_π − d*·ln10 = 0.000707` is the working value's rounding residual.
- Withdrawn in 0.130: "π φ e √ i are OUTPUTS, not inputs" and "Euler's identity is a theorem of this engine" (Ainulindale wiki 22 §6). Euler's identity is a theorem of complex analysis.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| π φ e √ i Λ as σ-facets; A_π = W(1) | derive each constant from the framework | 0 · SCALE | MINGLING | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).
