# Engine: Tier 0 Constants — π φ e √ i derived from H_RB

**Module:** `modules/constants/`  
**Version:** 0.120  
**Confidence floor:** ESTABLISHED  
**Notebooks:** [core/01_constants.ipynb](../notebooks/core/01_constants.ipynb)  
**Claim:** π, φ, e, √, i and Λ are each read as a facet of σ in one operator, with zero free parameters.

---

## What it computes

Tier 0 Root Constants: π, φ, e, √, i, OMEGA_ZS, α_F, d*, Λ — all drop out of H_RB algebraic structure. Two ceilings force domain [α_F, OMEGA_ZS]. d* has 4 values (tower→ln(10) Open Prob 2). Λ: J_neg at cosmological scale; Sombrero = Hawking pair; OMEGA_ZS = de Sitter attractor. Einstein wrote it in 1915, removed it 1917, universe re-inserted 1998 at 40σ.

Each `derive_*` equation returns the constant together with the σ facet it corresponds to — σ=i is pure phase, σ=½ the critical line, σ=e thermodynamic, σ=π gauge normalisation, σ=φ the recursion eigenvalue.

`derive_omega_zs` returns OMEGA_ZS = 0.5671432904097838, which is W(1), the Lambert W function at 1 — an exact special-function value, not a measurement.

## Results — run 2026-07-28

11/11 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `all_constants` | ESTABLISHED | ✓ | {'tier': 'Tier 0 — Root Constants + Ceilings + Domain + Λ', 'claim': 'All root constants… |
| `derive_e` | ESTABLISHED | ✓ | {'constant': "e (Euler's number)", 'sigma_facet': 'σ = e (thermodynamic — Boltzmann part… |
| `derive_i` | ESTABLISHED | ✓ | {'constant': 'i (imaginary unit)', 'sigma_facet': 'σ = i (pure phase — democratic)', 'ph… |
| `derive_omega_zs` | ESTABLISHED | ✓ | {'constant': 'OMEGA_ZS (Ω_ζΣ)', 'value': 0.5671432904097838, 'sigma_facet': 'Domain ceil… |
| `derive_phi` | ESTABLISHED | ✓ | {'constant': 'φ (golden ratio)', 'sigma_facet': 'σ = φ (recursion eigenvalue — structura… |
| `derive_pi` | ESTABLISHED | ✓ | {'constant': 'π (circle constant)', 'sigma_facet': 'σ = π (gauge normalisation — U(1) la… |
| `derive_sqrt` | ESTABLISHED | ✓ | {'constant': '√ (square root)', 'sigma_facet': 'σ = ½ (the critical line IS the square r… |
| `euler_identity` | ESTABLISHED | ✓ | {'identity': 'e^{iπ} + 1 = 0', 'type': 'Theorem of RedBlue Geometries Engine', 'assembly… |
| `derive_alpha_fermat` | THEORETICAL | ✓ | {'constant': 'α_F (Alpha_Fermat / fine structure constant)', 'value': 0.0072973525692838… |
| `derive_d_star` | ESTABLISHED (d*_R); OPEN (full tower) | ✓ | {'constant': 'd* (BK spectral floor, 4 components)', 'value_real': 0.246, 'sigma_facet':… |
| `derive_lambda` | σ=∞ (existence); σ>40 (Nobel 1998); OPEN (value from f) | ✓ | {'constant': 'Λ (Einstein cosmological constant)', 'value_omega_lambda': 0.6889, 'sigma_… |

## Open

- `derive_alpha_fermat` (fine structure constant) is the one equation here at THEORETICAL rather than ESTABLISHED. It is the weakest link in the Tier 0 chain and is marked as such.
- `derive_lambda` carries the σ=∞ tier label, which is not one of the four registry tiers. That is a labelling inconsistency in the module, not a result.
