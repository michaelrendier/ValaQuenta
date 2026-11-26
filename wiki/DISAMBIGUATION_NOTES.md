# Symbol disambiguation notepad (working notes; becomes one Disambiguation wiki page at the end)

Started 2026-11-25. Rule: one row per (symbol, meaning, engine, code name). The **code name** column is what disambiguates; where the code
reuses one name for two things, the row says so and the fix is queued. "seen" = found in code this pass; "canon" = from `~/.clauderc_canonical_maths`
`@RCCM_SYMBOLS` (author's ruling) and not yet re-read in the engine. Updated engine by engine; the final page is built from this file.

## Standing rulings (do not reopen)
| symbol | meaning | code name | note |
|---|---|---|---|
| α | fine-structure constant 1/137.036 | `ALPHA_FS` | was `A_PI` before 2026-11-21 |
| A_π (A_Fermat) | Lambert W fixed point W(1) = 0.5671432904 (Fermat side: inertia, speed of causality) | `A_PI` (`OMEGA_ZS` = deprecated alias) | not the standard "omega constant" |
| Ω_ζΣ = Ω_RZ | = d* (Riemann side: Hagedorn ceiling, entropy) | `OMEGA_ZETA_SIGMA` (= `D_STAR_TAUT`) | `OMEGA_ZS` once named A_π's value |
| d* | the value the code runs with, 0.24600 | `D_STAR` | |
| d*_taut | Flow, A_π/ln10 = 0.246307201473 | `D_STAR_TAUT` (`D_STAR_BOUNDARY` deprecated alias) | |
| d*_RG | Stability, dimension 8, numeric OPEN | `D_STAR_RG`, `D_STAR_RG_NUMERIC = None` | |
| d*_ln(10) | Translator, 0.5671432904 | `D_STAR_LN10` | |
| W(0), W(1), W(−1/e) | Lambert W values 0, A_π, −1 | env `LAMBERT_W*` | W(1) is A_π, **not** a separate constant |

## RULE (author, 2026-11-25): never a bare σ
`σ` / `sigma` alone pulls the wrong context in every search. In code, file names, wiki pages, notebooks, gallery pages and papers every sigma carries its own name.
Searchable identifiers (use these tokens, never a bare `sigma`):

| written | code / search token | meaning |
|---|---|---|
| σ_ζ | `sigma_riemann` | Re s, the Dirichlet/Euler exponent; the critical line σ_ζ = ½ |
| σ_RB | `sigma_rb` | the 16-component Ĥ_RB input (real scalar `sigma_riemann` + 15 imaginary); also the oblique-gear tilt/axis `sigma_rb_tilt`, `sigma_rb_axis` (ψ[k]·conj ψ[k⊕4]) — two uses, kept apart by the suffix |
| σ_self | `sigma_self` | red/(red+blue), the derived scalar |
| σ_val | `sigma_valuation` | the σ-valuation / σ-faces (Ainulindale SIGMA_VALUATION_FULL) |
| σ-stratum | `sigma_stratum` | σ₀…σ₄ nested inclusion levels (σ₄ = string / ground state) |
| σ_exp | `sigma_expansion` | the σ-expansion engine |
| σ_cav | `sigma_cavitation` | the cavitation library |
| σ_std | `sigma_std`, `stdev` | standard deviation (`bell_curve`) |
| σ_Pauli | `sigma_pauli_x`… | Pauli matrices (`tier6_physics` uses `sigma_x/y/z`: rename queued) |
| σ_SB | `sigma_stefan_boltzmann` | Stefan–Boltzmann constant, if it appears |
Engine-by-engine audit: every `sigma*` identifier found is listed under its engine below with its new token; renames are queued, not silent.

## σ (at least six meanings)
| meaning | engine (seen) | code name |
|---|---|---|
| Re(s), the coupling exponent / facet pointer of Ĥ_RB; σ = ½ the critical line | `h_rb_hat`, `tier7_cosmos`, `berry_keating` | `sigma`, `SIGMA_CRITICAL` |
| σ_RB: the tilt (Re) + axis (Im) of the oblique gear | `oblique_gear` (canon) | `sigma_rb…` (check) |
| σ-expansion (the Dirichlet/valuation scale) | `sigma_expansion` | `sigma`, `sigma_expansion` |
| standard deviation | `bell_curve` | `sigma`, `stdev`, `sd`, `sigma_to_p` |
| Pauli matrices | `tier6_physics` | `sigma_x`, `sigma_y`, `sigma_z` |
| σ cavitation (library) | `sigma_cavitation` | (no maths.py: library module) |
| Σ_RB: historical name of Ĥ_RB's summed form | `h_rb_hat` | `SigmaRBModule`, `sigma_rb_evaluate` (rename pending, VQ-7) |
| Σ sum sign | everywhere | — |

## Ω and its neighbours
| symbol | meaning | code name |
|---|---|---|
| Ω_ζΣ = Ω_RZ | d* (above) | `OMEGA_ZETA_SIGMA` |
| Ω (standard omega constant) | W(1) in the literature; **not** what the project's Ω means | never used for A_π |
| Ω_H = e^π | Hagedorn thermal ceiling (Gelfond's constant) | `OMEGA_H` |
| Ω as an algebraic object | "Omega dial" | `OMEGA_DIAL` blocks (canon) |

## Ĥ_RB and its currents
| symbol | meaning | code name |
|---|---|---|
| Ĥ_RB | the operator: Noether-current operator (J_red) + Noether-information-current operator (J_blue); in VAPMIP/Monad the Null Operator 0_RB | `h_rb_hat`; 0_RB/∅_RB in the Monad |
| Ĥ_RB − Ĥ_BR = J_red + J_blue | author's statement of the current balance (record: J_red + J_blue = J_green; three-term form is the same with J_green's sign flipped) | `jgreen.py` (scratchpad battery) |
| J_red, J_blue, J_green | Noether current, Noether information current, boundary (green) current | `facet_*`, `sigma_rb_term` (to read) |
| H (Ĥ) | Hamiltonian; also `hamiltonian.py` (E = xp), H_NN, H_nn (neural Planck `H_NN`), Hermite H₁₆ (VAPMIP e03) | `H_NN`, `HBAR_NN` |

## Other collisions noticed so far (to settle engine by engine)
- **Δ**: onset residual (W(1) − d*·ln10), mass-gap label (retired), elliptic discriminant g₂³ − 27g₃² (`h_rb_hat.facet_fermat`), Δσ level spacing (`h_rb_hat` trine), ΔJ = J_red − J_blue (piston).
- **ζ**: Riemann zeta; ζ_RB (to check); `zeta_uns_path`.
- **℘**: Weierstrass function in B̂_p (`blue_energy_weierstrass`); never a power set.
- **γ**: Riemann zero ordinate γ_n; γ₃ in `tier9_chem.cosic_eiip` (free scale c_bio); γ the Euler constant (to check); γ_radial (gamma-radial windspeed, VAPMIP).
- **κ**: coupling in `facet_general_relativity(kappa)`; κ = 1/√d tilt (boxkite note).
- **e**: Euler's number `E`; basis element e_i (`e₀…e₃₁`); e_a ± e_b zero-divisor pairs.
- **L**: left-multiplication matrix L_w (the hypercomplex Laplacian, TuringStack); L_(I|O) the intertwiner/Lagrangian path integral; Lagrangian L.
- **0**: 0 the scalar; e₀ identity/vacuum; 0_RB the Null Operator.
- **T**: T32 (the 32-dimensional Cayley–Dickson algebra); T/L trees; T temperature (`T*`, Hagedorn).
- **n**: dimension, prime index, mode number — check per engine.

## Per-engine log
- engine 0 `engine/constants.py` — rulings above entered; code names fixed.
- engine 1 `h_rb_hat` — σ (Re s) vs Σ_RB vs Δ rows added; VQ-7 pending.

- gallery/hrb + `h_rb_hat/sigma16.py` (2026-11-25): written with `sigma_riemann` / `sigma_rb` only; the d* block text now reads σ_ζ=½ plane everywhere (19 files).
