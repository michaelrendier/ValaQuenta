# Symbol disambiguation notepad (working notes; becomes one Disambiguation wiki page at the end)

Started 2026-11-25. Rule: one row per (symbol, meaning, engine, code name). The **code name** column is what disambiguates; where the code
reuses one name for two things, the row says so and the fix is queued. "seen" = found in code this pass; "canon" = from `~/.clauderc_canonical_maths`
`@RCCM_SYMBOLS` (author's ruling) and not yet re-read in the engine. Updated engine by engine; the final page is built from this file.

## Standing rulings (do not reopen)
| symbol | meaning | code name | note |
|---|---|---|---|
| α_fs | fine-structure constant 1/137.036. In this project also the SOURCE of the rule that a quantity must say the same thing in every version of the maths (the error-check discipline) | `ALPHA_FS` | was `A_PI` before 2026-11-21. Never an ingredient of the horizon mechanism (RHP glossary, 2026-11-12) |
| α_NN | neural fine-structure constant: the neural-network calibration / error-check coupling, defined to say the same thing at every tower layer; α_NN(r) running coupling | `ALPHA_NN` (const, to confirm), `alpha_nn_from_r`, tool `alpha_nn_running` (`modules/lagrangian`) | a different object from α_fs and from A_π; row added 2026-11-26 |
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

## RULE (author, 2026-11-26): never a bare α, Ω, d*, θ (same family as the σ rule)
From now on every symbol that has collided carries its subscript, in prose, code names, notebooks, papers and chat:
| write | never | token |
|---|---|---|
| α_fs | α | `ALPHA_FS` |
| α_NN | α | `ALPHA_NN` |
| A_π (capital Alpha, subscript π; A_Fermat) | Α, α | `A_PI` |
| Ω_ζΣ (= Ω_RZ = d*), ω_H = e^π, Ω(n) | Ω | `OMEGA_ZETA_SIGMA`, `OMEGA_H`, `omega_big` (number of prime factors) |
| σ_ζ = σ_Riemann | σ | `sigma_riemann` |
| θ_…: see the θ table below | θ | per row |
The author confirmed 2026-11-26 that the σ in "θ = πσ" is σ_Riemann (= σ_ζ).

## θ (at least six meanings, plus ϑ) — found 2026-11-26 while chasing the two charts
| written | meaning | where | code token |
|---|---|---|---|
| θ_polar = πσ_ζ | the chart angle of paper §3.2: strip 0<σ_ζ<1 → polar range 0<θ<π, measured from the σ_ζ = 0 pole; critical line θ = π/2. Radians (the paper's table prints degrees for display only) | PAPER §3.2, README | none (prose only) |
| lat_linear = π(σ_ζ − ½) | the same chart as a LATITUDE: 0 on the equator, north = σ_ζ = 1 (|w|<1). lat_linear = θ_polar − π/2 | `rhp/sphere.py` | `latitude_linear` |
| lat_cayley | conformal latitude of the Cayley chart, sin(lat) = (2σ_ζ−1)/(|s|²+|s−1|²) | `rhp/sphere.py` | `latitude_cayley` |
| θ_Hardy(t) | Riemann–Siegel phase, ζ(½+it) = e^{−iθ_Hardy}Z; θ_Hardy = Im lnΓ(¼+it/2) − (t/2)ln π; winds N(T) = θ_Hardy/π + 1 + S times | `rhp/uns.py` | `theta`, `theta_prime` (use `theta_hardy` in new code) |
| θ_k(n) | zero-phase winding of the zero-tone k: γ_k ln n (`'zero'`) or 2πh√n (`'arch'`) | `rhp/zerophase.py` | `theta_winding` (to confirm) |
| Θ(k) = k·22.5° | the Telperion/Laurelin counter-twist per tower level | `AbrikosovTree/render/lattice_planes.py` | `Theta_k` |
| ϑ | Jacobi theta function Σ e^{−πn²t} (modular source of the functional equation) | literature | never `theta` |
| θ_c | critical angle (RCCM_CRITICAL_ANGLE, not re-read this pass) | canon | to check |
Radians vs degrees is NOT the cause of the chart disagreement below (checked 2026-11-26: no radian/degree mismatch in `sphere.py`; degrees appear only in plot labels and the paper's table). The real θ clashes are (a) colatitude θ_polar (paper) vs latitude (code), poles flipped; (b) θ_polar vs θ_Hardy, one set by σ_ζ and one by t.

## The charts of the critical strip (measured and derived 2026-11-26; scratch: scratchpad/charts.py)
Question (author): which mapping makes the equatorial great circle a nodal line, why do `latitude_cayley` and `latitude_linear` disagree, which one belongs to the Riemann-Hypothesis lineage, and what is the mechanics.
| chart | map | latitude | longitude | where |
|---|---|---|---|---|
| `chart_cayley` | w = (s−1)/s, then inverse stereographic (N pole w=0 ⇒ s=1, S pole w=∞ ⇒ s=0) | sin(lat) = (2σ_ζ−1)/(|s|²+|s−1|²): depends on σ_ζ AND t | arg w = π − 2 arctan 2t on the line | `sphere.cayley`, `to_xyz`, `latitude_cayley`, `longitude_cayley`; `unsmap.cayley`, `stereo`, `lift` |
| `chart_linear` | (σ_ζ, t) ↦ (lat, lon) = (π(σ_ζ−½), t) (equirectangular) | π(σ_ζ−½): σ_ζ ONLY | t | `sphere.latitude_linear`; PAPER §3.2; AbrikosovTree `LIFT_KIND='linear'` (a picture, no result rests on it) |
| `chart_hardy` (longitude only) | lon = θ_Hardy(t) mod 2π (the spring end-on) | — | θ_Hardy mod 2π | `sphere.longitude_hardy` |
| `chart_wedge` | z = e^{iπs}: arg z = πσ_ζ, |z| = e^{−πt}; strip → upper half-plane, conformal | — | — | not in code (derived here) |
Note `equator.py` panel (a) is a HYBRID: `latitude_cayley` for latitude with `longitude_hardy` for longitude. It is neither chart_cayley nor chart_linear. Intentional (the dots are zeros on the spring), but it is a third thing and must be named.

### What agrees and what does not
Both charts put the critical line on the equator (as a SET), and both turn s ↦ 1−s̄ into the equatorial reflection at the same longitude (checked: w(1−s̄) = 1/conj w(s), exactly). They disagree on everything else:
* latitude of an off-line point. Real axis: agree only at σ_ζ = 0, ½, 1; between them lat_cayley − lat_linear peaks at 8.15° (σ_ζ = 0.761; 53.13° against 45° at σ_ζ = 0.75). At height: σ_ζ = 0.75, t = 1, 5, 50 gives lat_cayley = 10.98°, 0.566°, 0.006° against 45° every time. lat_cayley ≈ (2σ_ζ−1)/(2t²) → 0 as t → ∞: every line σ_ζ = c except ½ is a small circle through w = 1 (s = ∞, ON the equator), so the strip collapses onto the equator at height. The linear latitude never changes with t.
* conformality (finite differences on the unit sphere, 5 sample points): chart_cayley has |∂X/∂σ_ζ| = |∂X/∂t| = 2/(|s|²+|s−1|²) to 4 digits and cos(angle) = 0: isotropic, angle-preserving. chart_linear has |∂X/∂σ_ζ| = π and |∂X/∂t| = cos(lat): ratio π/cos(lat) = 3.14 on the equator, 4.44 at 45°, 10.17 at 72°. It is never conformal.
* poles. chart_cayley: only the points s = 1, 0 (the actual poles of Λ, residues +1, −1 to 1e−7). chart_linear: the WHOLE lines σ_ζ = 0 and σ_ζ = 1 collapse to the poles.

### The mechanics (why)
1. A chart with latitude a function of σ_ζ alone and longitude a function of t alone is separable. Conformal needs f′(σ_ζ) = cos(f)·g′(t). For equirectangular f′ = π, g′ = 1, so it would need cos(lat) = π: impossible. The only conformal separable chart is Mercator (lat = gd(c(σ_ζ−½)), lon = ct), whose poles are at σ_ζ = ±∞, not at the strip edges.
2. A conformal chart onto the sphere cannot be separable. Gaussian curvature has to be absorbed by mixing σ_ζ and t. The Cayley map is a Möbius map, which is exactly that mixing, and it carries a position-dependent scale factor (the "flattening artifact", |dw/ds| = 1/|s|²).
3. θ_polar = πσ_ζ is a conformal angle, but of a different map: z = e^{iπs} (chart_wedge). There the radius is e^{−πt}: t is scaled by the same π in the exponent. Equirectangular keeps lon = t unscaled, so it is that conformal map with the radial half thrown away.
4. Units are not the cause. The linear chart is Aff(1,ℝ) acting on the σ_ζ axis alone: SCALE by π, ADD −π/2. Cayley is an element of PSL(2,ℂ) acting on the plane. Both are free reparametrisations of the axis; only the second preserves angles and singularities.

### Which chart is the Riemann-Hypothesis lineage's
chart_cayley. It is the chart in which the established structure is true as stated: functional equation = isometric reflection w ↦ 1/w̄; poles at poles; analytic functions stay analytic (the nodal ladder crosses at right angles: 21 rungs ⟂ the line, median 0.38°); the argument principle is Gauss's law of the flow. chart_linear is a labelling of the σ_ζ axis (it is used for the secondary axis label in `equator.py` and the AbrikosovTree Ulam sphere) and no result in the repo depends on it. The Scale engine's `charts(s)` uses the Cayley fold Γ = (s−1)/(s+1) with local scale factor 2/(s+1)²: same mechanism, same group, so the Scale engine is already on the correct chart. Smith dictionary: Z = 2s−1, Γ = (Z−1)/(Z+1) = (s−1)/s. Re Z = 0 ⇔ |Γ| = 1 ⇔ σ_ζ = ½ (the lossless boundary IS the critical line); the conventional chart (R ≥ 0) is the σ_ζ ≥ ½ hemisphere; s ↦ 1−s is Z ↦ −Z, Γ ↦ 1/Γ; the matched point Γ = 0 is s = 1.

### The nodal line (what is and is not established)
Let R be the equatorial reflection (w ↦ 1/w̄ = s ↦ 1−s̄). Checked at three points to 1e−16: Re ξ∘R = Re ξ, Im ξ∘R = −Im ξ. So Φ_odd = Im ξ = (ξ − ξ∘R)/2i is odd under R and vanishes on Fix(R), the equator, for EVERY chart in which σ_ζ = ½ is the equator. This is the trivial half (ξ is real on the line). The Riemann statement is the other half: the zeros are Re ξ = 0 ∩ Im ξ = 0, and RH ⇔ the off-equator Im ξ = 0 curves never meet the Re ξ = 0 curves. Measured (docs/nodal_extractor R2, t ≤ 80): 21 Re ξ = 0 lines (one per zero), 20 off-equator Im ξ = 0 lines (one per extremum of ξ on the line), no crossings off the line. ξ itself is the symmetric function; ζ is not (ζ(1−s) = χ(s)ζ(s)), and the factor π^{s/2}/Γ(s/2) between them is what breaks R: that is the content of "factoring π out". ξ is not a Laplace eigenfunction on the sphere, so Courant's nodal-domain theorem does not apply and the identification with Y₁⁰ (PAPER §3.3, C1) remains open.

### Anomalies chased (all queued, none yet fixed in the paper)
1. PAPER §3.2 θ_polar = πσ_ζ is a colatitude from the σ_ζ = 0 pole; the code's north pole is σ_ζ = 1 (latitude). Orientation clash, relabel only.
2. PAPER §3.3 "w = 2s−1 followed by stereographic projection" does NOT put the critical line on the equator: Re s = ½ is then the imaginary axis |w| from 0 to ∞, whose image is a meridian (x = 0 for all four test points), not the equator. The missing step is the Cayley fold (Z−1)/(Z+1); w = 2s−1 is the Smith chart's Z.
3. PAPER §3.3 J_N(z) = i/z̄: the unit circle is invariant, NOT "fixed" (J_N sends 0.6+0.8i to −0.8+0.6i, a quarter turn); the pointwise-fixed circle belongs to the reflection 1/z̄. J_N = quarter-turn ∘ reflection; J_N² = −z; J_N⁴ = id (true).
4. `equator.py` hybrid chart (above).
5. `zerophase_2026-11-11.md` says "h = 1 is Sacks/Ulam": Ulam's polar angle is π√n (circular sd 0.056 rad over n ≤ 3000, against 2.77 for 2π√n), i.e. h = ½. `pole_density_and_ulam.py` U2: predicted err·k is −2πD/32; the data (and the expansion √(4k²+bk+c) ≈ 2k + b/4 − D/(64k)) give −πD/32, half the written prediction (1.178 vs 2.356, 1.571 vs 3.142).
6. For the Scale engine: the linear chart is its SCALE/ADD on one axis; the Cayley fold is the Möbius element with the position-dependent factor. Same difference, in the engine's own words: separable axis operator (constant factor, anisotropic) versus mixing operator (variable factor, isotropic).

## Header image (Gemini "The Riemann Sphere") — label audit, 2026-11-26
Run by `RiemannHypothesisProof/experiments/image_header_sphere_test.py` (+ `.json`). The image is kept as a picture of a pathway in a sphere; its labels do not match the Cayley chart (chart_cayley):
| Image label | Maths (chart_cayley, w = (s−1)/s) |
|---|---|
| North pole "(∞)" | s = ∞ is w = 1, a point ON THE EQUATOR. The poles are s = 1 (w = 0) and s = 0 (w = ∞). |
| South pole "(trivial zeros, s = 1)" | s = 1 is the pole of ζ. Trivial zeros s = −2k are on the real-axis meridian, southern hemisphere (σ < ½): latitudes −22.6°, −12.7°, −8.8°, −6.7°, −5.5° for k = 1..5, accumulating at w = 1 (the equator). |
| Equator "imaginary axis Re(s) = ½", zeros on it | Correct: |w| = 1 at the first 10 nontrivial zeros (1.0 to machine precision). |
| Helices running pole to pole | Not a ζ object on the s-sphere: each line σ ≠ ½ is a small circle through w = 1; ζ(½+it) is a path on the VALUE sphere (equator |ζ| = 1, zero = south pole, ∞ = north pole), a rosette leaving the pole at each zero, not pole to pole. |
Value sphere, t < 400, 19,975 samples: Re ζ > 0 for 81.9% (76% at 25,000 zeros per the live page); mean ζ = 0.9965 (the n = 1 term); |ζ| > 1 for 56.6% and mean ln|ζ| = −0.001 (no north/south lean); the Riemann–Siegel mirror term e^{−2iθ}S̄ has mean 0.009 (it averages out, so the reflection does NOT rectify); Hardy Z has mean 0.0026 and Z > 0 for 47.6% (AC), mean |Z| = 1.57 (the rectified DC). Twist per zero: mean spacing in θ = 1.0000073 π over 25,000 zeros; θ(γ_n)/π − (n−1) has mean −0.49997 and std 0.298 (Selberg 0.342): a snap per π of twist, the primes set where in the cycle. Dropping the π term of θ over-counts zeros by 4,000 at t = 21,942 (16%).
