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

## Related
[circle_atlas.md](circle_atlas.md) · `FourthAgePapers/WitchesHat/simulator/` (the first renders) · `Ainulindale/wiki/29_witches_hat_paper.md`
