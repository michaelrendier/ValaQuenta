# Engine: L_SM, the Standard Model Lagrangian

**Module:** `modules/lagrangian_sm/` (`maths.py`, `compare.py`, `tools.py`, `manifest.json`)
**Class:** `LagrangianSMModule`
**Version:** 0.1 (2026-11-19)
**Confidence floor:** ESTABLISHED
**Notebook:** [notebooks/engines/25_lagrangian_sm.ipynb](../notebooks/engines/25_lagrangian_sm.ipynb) · **Proof locale:** `engine/proof_locale/lagrangian_sm.json`
**Tests:** `Testing/test_lagrangian_sm.py` (20) · **Toolbox:** [toolbox/42_lagrangian_sm.md](toolbox/42_lagrangian_sm.md)
**Narrative:** `Ainulindale/wiki/139_three_lagrangians.md`
**External packages:** `numpy`, `scipy`, `sympy`, `particle` (PDG tables, installed 2026-11-19 with `uncertainties`)

The engine builds the Standard Model Lagrangian from its gauge group and field content and checks it against measured numbers. It is the control for L_NN (`modules/lagrangian`) and L_(I|O) (`modules/l_io_photon_path`). It uses no framework constant.

## `maths.py`

`pdg_mass(name)` → `(mass_GeV, uncertainty_GeV)` from the PDG tables. `pdg_masses()` → the 9 charged-fermion masses, W, Z, H. `INPUTS` → typed PDG/NuFIT inputs with sources (verify against the live PDG before quoting).

`field_content()` → list of dicts `name, su3, su2, Y (Fraction), chirality, generations`. `degrees_of_freedom()` → Weyl fermions (45), real scalars (4), gauge bosons (12).

`anomaly_check()` → exact rational anomaly sums over one generation (`U1^3`, `SU3^2 U1`, `SU2^2 U1`, `grav^2 U1`) and the Witten parity.
`hypercharges_from_anomalies(n_colours=3)` → the hypercharge solution given the multiplets, `Y_H = 1/2` and Yukawa invariance; `charges` holds Q_u, Q_d, Q_e and the uud charge.
`su5_embedding()` → the 15 Weyl fermions as 5̄ ⊕ 10 of SU(5): hypercharges from the traceless generator, traces, `A(10) + A(5̄)`.
`su2_generators()`, `su3_generators()`, `structure_constants(T)`, `group_checks()` → closure, Jacobi and Casimir residuals.
`parameter_count(neutrinos)` → `'massless'` 19, `'dirac'` 26, `'majorana'` 28, counted from the Yukawa structure and the flavour symmetry.

`ew_mass_matrix_symbolic()` → sympy quadratic form of `|D H|²`, its Hessian and eigenvalues (m_W², m_Z², 0). `higgs_potential_expansion()` → sympy coefficients of V(h); `m_h² = 2λv²`. `higgs_sector(m_h, v)` → λ, μ², depth, trilinear, quartic. `fermi_vev()` → `(√2 G_F)^(-1/2)`. `ew_tree()` → e, g, g′, tree m_W, m_Z against the PDG masses, ρ. `yukawas(v)` → `y = √2 m/v`.
`ckm_matrix(...)`, `pmns_matrix()`, `jarlskog(V)`, `unitarity_residual(V)`. `z_couplings(sin2w)`. `vertex_inventory()`, `term_inventory()`.
`gauge_initial()`, `rge_gauge(mu)` (analytic one loop), `gauge_crossings()`, `rge_top_higgs(mu_max, n)` (one-loop g1, g2, g3, y_t, λ; illustrative).
`hat_model()` → the SM hat as a model dict for `witches_hat.action`. `verify()`.

## `compare.py`

`measured_exponents()` → the degree of each term in the field amplitudes, SM against the coded L_NN (double a field, read n in `term ∝ amplitude^n`).
`bias_conventions()` → hat or bowl for μ² = ±1 as coded. `one_over_phi_on_bias()` → whether `polar_lagrangian` applies 1/φ to `L_bias`. `seagull_correspondence()` → ratio of the coded `L_matter` to the SM scalar-gauge seagull term (constant 8/n).
`lio_integrand(E, n)` → J_red·J_blue over σ. `parameters_NN()`, `comparison_table()`.

## Registered equations (19)
`verify, fields, anomalies, hypercharges, su5, groups, parameters, ew_symbolic, higgs_symbolic, higgs, ew_tree, yukawas, ckm, zcouplings, vertices, running, compare, exponents, hat`

## Measured results (2026-11-19, notebook 25)
| result | value | tier |
|---|---|---|
| anomaly sums | all exactly 0; Witten parity even | ESTABLISHED |
| hypercharges from anomalies | unique; = observed (1/6, 2/3, −1/3, −1/2, −1) | ESTABLISHED |
| SU(5) embedding | 15 = 5̄ + 10, traceless Y, A(10) + A(5̄) = 0 | ESTABLISHED |
| quark charges for N_c = 1…5 | Q_u = ½ + 1/(2N_c); N_c = 3 gives 2/3, −1/3, proton 1 | ESTABLISHED |
| parameters | 19 / 26 / 28 | ESTABLISHED |
| v, λ | 246.22 GeV, 0.1291 | ESTABLISHED:CALCULATED |
| tree m_W, m_Z vs PDG | −0.16 %, +0.35 %; Δr = 0.0364 accounts for it | ESTABLISHED:CALCULATED |
| CKM Jarlskog J | 3.1e-5; unitarity residual 1e-16 | ESTABLISHED:CALCULATED |
| one-loop crossings | 1e13, 2e14, 1e17 GeV (spread 3.97 decades) | ESTABLISHED:CALCULATED |
| one-loop λ → 0 scale | swings from none below 1e19 to 1e5 GeV for y_t(M_Z) 0.92 → 1.00 | not quotable |

## Recorded findings on the other Lagrangians (measured on the code)
| finding | measured |
|---|---|
| `L_bias` of L_NN equals −V_SM exactly for μ² > 0 | max difference 5.6e-17 |
| gauge kinetic degree in A | SM 4 (non-Abelian), L_NN 2 |
| fermion-gauge degree | SM ψ²A¹, L_NN ψ²A² |
| Yukawa degree | SM ψ²h¹, L_NN ψ¹β¹ |
| coded `L_matter` vs SM scalar-gauge seagull | ratio 8/n for every input (identical form) |
| `polar_lagrangian` applies 1/φ to `L_bias` | **no** (docstring and wiki 04 say it does) |
| μ² < 0 (the docstring's symmetry-breaking sign) | bowl, no brim |
| L_(I|O) integrand J_red·J_blue | constant e^(−E) in σ |

## Not done
``requirements.txt` and `pyproject.toml` list the new packages (`particle`, `uncertainties`). The two-loop running and threshold corrections are not included. PMNS and CKM values are typed from the reviews.
