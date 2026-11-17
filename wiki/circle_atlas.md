# Engine: The Circle Atlas (H_hat_RB and the Complete Shape of Mathematics)

**Module:** `modules/circle_atlas/` (`maths.py`, `tools.py`, `manifest.json`)
**Class:** `CircleAtlasModule`
**Version:** 0.1 (2026-11-16)
**Confidence floor:** THEORETICAL (status label `THEORETICAL:CALCULATED`; each viewport's closure is ESTABLISHED numerics)
**Notebook:** [notebooks/engines/22_circle_atlas.ipynb](../notebooks/engines/22_circle_atlas.ipynb) · **Proof locale:** `engine/proof_locale/circle_atlas.json` · **Ainulindale:** `wiki/137_the_circle_atlas.md`
**Tests:** `tests/test_circle_atlas.py` (10)
**Atlas name:** The Circle Atlas (sixth row of `ContextPlease/claude/ATLAS_REGISTRY.md`).

## API

`VIEWPORTS`
: dict id → {fn, name, source, tier, pi}; 19 viewports.

`entry(name)`
: :param name: key of `VIEWPORTS`. :returns: dict id, name, source, tier, `to`, `from`, `pi_route`, `pi_value`, `pi_error`, `circle_in`.

`atlas()`
: runs every viewport.

`signposts()`
: list of {id, enters, exits, pi}: the road into fixed-point space, the road out, and the π route.

`gaps()`
: {no_pi_route, to_fails_raw, named_gaps}.

`sign_carriers()`
: axes k with e_k x = x\* e_k for every x in e₀…e₇ (returns e₈…e₁₅).

`census(repos=None, root=None)`
: token counts (pi, trig, phase, circle, wave) over the repositories' Python files; a text census, not proof.

`import_probe()`
: imports every ValaQuenta module and GenerationalLineage toolset; failures are returned, not repaired.

`verify()`
: all viewports close (Berry–Keating raw is a recorded failure), FROM ok, Wick closes, sign carriers = e₈…e₁₅.

`v_waveform`, `v_hamiltonian`, `v_lagrangian`, `v_berry_keating`, `v_cardioid`, `v_epicycles`, `v_smith`, `v_apollonian`, `v_inversion`, `v_hopf`, `v_roots_of_unity`, `v_sedenion`, `v_add_scale_sign`, `v_prime_wheels`, `v_ring`, `v_bao_ring`, `v_polygon`, `v_retraction`, `v_winding`
: each returns {"to": {ok, residual, transform, …}, "from": {ok, residual, fibre, …}}.

## Contract of a viewport
TO (enter fixed-point space): the stated transformation applied to the viewport's own object; `residual` is the departure from |z| = 1 (or closure). A viewport that does not close raw sets `ok False` and, if a transformation fixes it, `ok_transformed` (only `berry_keating`). FROM (exit): the construction back, with `fibre` stating what has to be chosen; FROM is a relation, not the inverse function.

## Reused machinery (modify, never reinvent)
`modules/tier8_sedenion.cd_mul` · `modules/box_kite.zero_divisor_pairs` · `modules/hypergon_constructibility.is_constructible` · `modules/pi_derivations`. The sedenion battery that motivated it is `FourthAgePapers/TheInterface/02_sedenion_battery.py`, `03_sign_test.py`.

## Measured (2026-11-16, executed in notebook 22)
Residuals from the circle: waveform 7e-14, Hamiltonian 6e-15, Lagrangian 9e-6 (discrete action), cardioid multiplier 3e-16, Smith 4e-16, Apollonian tangency 1e-16, inversion 3e-15, Hopf 4e-16, roots of unity 2e-14, sedenion 2e-16 (15 axes, 84 zero-divisor circles, 336 annihilating ordered pairs, 0/300 random circle-point pairs multiply to zero), ADD:SCALE:SIGN 4e-15 (SIGN carriers e₈…e₁₅), prime wheels 2e-16 (Euler product vs Dirichlet at s = 2+3i: 1e-5 level), ring 3e-4, BAO ring (constructed) 3e-3, polygons 3e-8 at 12 doublings, retraction 5e-16, winding 4e-16. **Berry–Keating H = xp raw: residual 6.4 (hyperbola); after t → it: 2e-16.**
Census (text): GenerationalLineage 100 files / 18,106 lines; ValaQuenta 228 / 63,735; RiemannHypothesisProof 118 / 10,877; VAPMIP 308 / 93,356; FourthAgePapers 87 / 31,422; others in the notebook. Import probe: 69 modules/toolsets import, 0 fail.

## Gaps (kept, not hidden)
No π route yet: `apollonian`, `inversion`, `bao_ring`, `retraction`. Named gaps: elliptic curves / modular forms, string-theory cardioid superstrings, wing/bell motions, the point that becomes a circle (the polar blow-up is a candidate, INTERPRETATION), 5:5:5 and 2:11:2 frames, BAO/CMB with data, gauge-theory U(1) circles.
