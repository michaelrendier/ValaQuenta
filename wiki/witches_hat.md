# Engine: The Witch's Hat Engine (core)

**Module:** `modules/witches_hat/` (`maths.py`, `tools.py`, `manifest.json`)
**Class:** `WitchesHatModule`
**Version:** 0.1 (2026-11-17)
**Confidence floor:** THEORETICAL (status label `THEORETICAL:CALCULATED`; Higgs numbers, path mechanics and pair correlations are ESTABLISHED)
**Notebook:** [notebooks/engines/24_witches_hat.ipynb](../notebooks/engines/24_witches_hat.ipynb) · **Proof locale:** `engine/proof_locale/witches_hat.json`
**Tests:** `tests/test_witches_hat.py` (11)

**This core is the tooling.** It returns plain data (arrays and dicts) and draws nothing. Renderers (the `spatial-simulation` skill: OpenSCAD, Blender, matplotlib) read a snapshot and bridge to whatever rendering is chosen.

## API
`snapshot(shape, n, size, depth, E, aim, spread, n_psi, n_phi)`
: a static snapshot: surface (r, z), the brim, the path bundle (x, y, z, W per path, in physical units), closest approaches, regime, focus radius and spread, caustic ring radius.
`hat_shape(shape, n)`
: V(x), x = r/r_b, V(0) = 0, brim −1. Shapes: `quartic` (exponent n; n = 4 is the Standard Model), `fermion1d/2d/3d` (V = −g_F, the exchange hole), `boson` (V = −g_B, a well), `dog` (difference of Gaussians).
`turning_radius`, `trace`, `focus_resolution`, `defocus_curve`, `energy_regimes`, `shape_table`, `sm_hat`, `pair_correlation`, `unfold`, `zeta_pair_correlation`, `verify`.

## What is measured (see the notebook)
- A bundle aimed at the hilltop closes on a point only at aim 0 and E = 0 (the separatrix); E < 0 reflects at r_c = √(−E/2) (n = 4); E > 0 passes through; any aim offset δ opens a hollow cone with ring radius √(sin δ)((n−2)/n)^¼.
- Size and depth drop out (tested): the figure is the same in units of the brim.
- Shape is the knob: resolution rises with the exponent n. The exchange-hole hats are craters (no outer wall) and match the quartic family only at n ≈ 2.1–2.3: the fermion hole is **not** the Standard-Model quartic hat (failed identification, kept).
- The zeros of ζ: pair correlation within rms 0.066 of the 1-D fermion kernel 1 − sinc², against 0.36 for no correlation (3066 tabulated zeros).

## The two Lagrangians (added 2026-11-18), kept separate and compared after
`lagrangian_sm()`: the Standard-Model Higgs hat (ESTABLISHED). `lagrangian_vap(mu_sq, lam, g, psi, convention)`: the VAPMIP (monad) Lagrangian L_NN (`modules/lagrangian`), V_vap = −((1/φ)·L_bias + L_coup): the 1/φ-scaled Mexican-hat bias term plus the Yukawa coupling −(g/φ)ψ·β. `snapshot_plane(model)`: surface on the β-plane, brim ring, hilltop, path bundle; `trace_plane`, `hilltop`, `l_io_action`, `compare`.
- **Isometric without coupling:** VAPMIP (g = 0) and Standard-Model hats give identical action and closest approaches in the normalised chart (tested). Both are the same quartic.
- **The coupling is the aim:** the linear Yukawa term tilts the hat toward ψ and moves the hilltop (0.144 brim radii at g = 0.2).
- **Two defects of the coded bias term, recorded not corrected:** with the default μ² = −1 the coded `L_bias = ½μ²β² − ¼λβ⁴` gives V = −L a bowl (no hat); and the default vev 1.0 differs from the brim √(−μ²/λ) = √2 at λ = 0.5.
- **L_(I|O) read as the action of the actual path:** W = ∫p·dq to the closest approach, nearly independent of the launch angle (0.8619 → 0.8314, aim 0.01 → 0.4). An earlier simulator reported arc length as action; corrected.
- Stills: `FourthAgePapers/WitchesHat/simulator/particle_views.html` (branch `witches-hat`).

## Path of action, mapped (`modules/witches_hat/action.py`, added 2026-11-19)
Nothing aims. `discrete_action(model, q, T, signature)` gives S of any candidate path; `stationary_paths` finds every path with δS = 0 between two fixed events (and the Morse index, `morse_index`); `trial_variations` measures neighbouring paths (more work, less work); `ray_family` integrates every launch direction with the variational equation, `caustic_points` / `caustic_summary` read the caustics off, `closest_approach_profile` measures the funnel; `euclidean_radial_release` is the Wick-rotated bounce in −V. Signatures `'lorentzian'` (U = V) and `'euclidean'` (U = −V). `ray_bundle(model, starts, velocities, T, n_steps, u, target)` integrates many paths at once (vectorised RK4, optional drifting hat) carrying S, W and arc length and each path's closest approach to a target; `brim_bundle(model, E, n_sources, n_dirs, T, n_steps, eps, u)` launches every brim point in every direction and keeps the paths that pass within eps of the hilltop (selected by outcome, not aimed); `tip_report(model, bundle)` gives the tip position, its distance from the hilltop, its height, and the **sheets** of the multivalued action; `cone_tip_height(model, E)` is the exact radial cone; `natural_units(model)` the units (R, V0, tau0 = R/sqrt(2 V0), brim level, z_V) that put energy and action on one vertical scale. Tests: `Testing/test_witches_hat_action.py` (13).
- **The action cone, measured (SM hat, E = 0):** tip 0.0015 R from the hilltop; W_tip = 0.4310 (closed form (2/3)[(1 − r²/2)^(3/2)] from r = 1 to 0); height 0.2189 depth above the hilltop; second sheet W = 0.9025 = 0.4310 + 2 × 0.2357 (out to the wall at r = √2 and back). Figures: `FourthAgePapers/WitchesHat/papers/figures/lagrangians/v2.0/`.
- Harmonic closed form, free particle and the Euclidean twin match; the discrete error falls as 1/N² (ratios 3.99, 4.00, 4.00).
- Past a conjugate point the Morse index counts the cheaper directions (two in a 2-D isotropic well).
- On the real hat (μ² = λ = 1) between one pair of events there are three stationary paths (S = 0.7742 index 0, 0.7906 index 1, 10.88 index 2); the shot ray is the index-1 one.
- Time-dependent hat (the original L_dynamic's setting, `moving_hat_exchange`): static hat conserves E to 1e-12; a hat moving at u = 0.6 exchanges energy by dE = ∫∂V/∂t dt (identity to 1e-11): the particle's energy rises 0.913 and ends +0.383 (borrowed, partly returned). Test `test_static_hat_conserves_energy_and_moving_hat_exchanges_it_by_the_identity`.
- The unaimed family from a brim point at E = 0: closest approach to the hilltop ∝ (offset from the radial)^0.504 (closed form 0.5), coefficient 0.858 (0.841); the first caustics lie 0.51 brim radii from the hilltop. A funnel, not a point caustic.

## Related
[circle_atlas.md](circle_atlas.md) · `FourthAgePapers/WitchesHat/simulator/` (the first renders) · `Ainulindale/wiki/29_witches_hat_paper.md`
