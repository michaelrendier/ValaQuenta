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
: dict id → {fn, name, source, tier, pi}; 25 viewports (19 + sphere, hypersphere, field_axis, native_units, kite_spectrum, added the same day).

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

## Second pass (2026-11-16): sphere, field axes, native units, the kite as a spectrum

`ball_volume(n)`, `ball_table()`
: V_n = π^{n/2}/Γ(n/2+1); table, peak dimension (volume peaks at n = 5, surface area at n = 7), recursion V_n = (2π/n)V_{n−2} to 1e-15. V₁₆ = 0.2353 (the sedenion's n).

`v_sphere`, `v_hypersphere`
: every plane section of S² and every great circle of S^n (n = 1, 3, 7, 15, 31) closes to 1e-14. **Norm defect of unit products** (max over 2000 random pairs): dim 2, 4, 8: 4e-16; dim 16: 0.366. S¹, S³, S⁷ are closed under the product; S¹⁵ is a sphere of circles that is not.

`v_field_axis(...)`, `real_component_effect(theta)`
: exp(θu) = cos θ + u sin θ for any unit imaginary u ∈ S¹⁴ (200 random axes: 2e-14), and for a path of axes u(s) on S¹⁴; the 15 axes are one basis of that field. Re(exp(θe_k)·z) = r cos θ − y_k sin θ and L(e_k)² = −1 for all 15 k (residual 0): each axis pairs Real with e_k and the other 14 into seven planes (the planes of e₈…e₁₅ pair (j, j+8)).

`native_coords(z)`, `from_native(a, b)`, `v_native_units`
: z = 10^a · e^{iπb}: a = log₁₀|z| decades (unit ln 10), b = arg z/π half-turns (unit π). Product adds both (500 random pairs: 4e-16). The unit circle is a = 0, period 2 in b. In these units circumference 2 and disc area 1 are identities of the unit choice, not a derivation of π. ln 10/π is transcendental (Baker, after Gelfond), INTERPRETATION that these are the two native units.

`kite_spectrum()`, `v_kite_spectrum`
: L_d for a zero-divisor diagonal d is skew (residual 0). **Emit:** the same three lines for all 84 diagonals, singular values 0 (×4), √2 (×8), 2 (×4); a non-zero-divisor diagonal e_a ± e_{a+8} has one line √2 (×16). The flow exp(tL_d) of a zero-divisor operator has two incommensurate frequencies (ratio √2): a torus, not a circle, although the NUMBER d/|d| is an exact circle. **Interpret:** the lines say "zero divisor" and give |d|²; one signature for all 84, so the spectrum does **not** say which kite. The nullspace of L_d (its eigenvectors) gives the four annihilating partners and so the kite: 84/84 round trips.

`anchored_readings()`, `KITE_CONSTRUCTS`
: from an anchor a, the reading σ(L_a L_b) splits the 84 diagonals into 7 classes (2, 2, 4, 4 inside the anchor's kite; 8, 32, 32 outside), the same from every anchor. This is the **De Marrais-kite analogue of the scalar kite's string** (Pencil/Flashlight, from the pivot/anchor to each tetrahedron: where it is attached orients the kite). `KITE_CONSTRUCTS` notates three different objects: the De Marrais kite (static, symmetric, no vantage), the Scalar Boxkite (7 ordered pairs, discrete, string from the anchor), and the Scaled Boxkite / Mind's Eye (the De Marrais kite carried by G2, the tetrahedra grab the anchor). The scaled kite is **not computed here** and none of the string machinery is applied to it.

## Gaps (kept, not hidden)
No π route yet: `apollonian`, `inversion`, `bao_ring`, `retraction`. Named gaps: elliptic curves / modular forms, string-theory cardioid superstrings, wing/bell motions, the point that becomes a circle (the polar blow-up is a candidate, INTERPRETATION), 5:5:5 and 2:11:2 frames, BAO/CMB with data, gauge-theory U(1) circles.

## Added 2026-11-17: `v_photon_sphere` (25th viewport)
The circular null orbit of Schwarzschild at r = 3M (G = c = 1). Integrating u'' + u = 3u² from u = 1/3 over a full turn leaves the orbit on r = 3M to 9e-16; the critical impact parameter is 3√3 M = 5.196. It is **unstable**: a perturbation of 1e-8 grows by 267.75 per turn, cosh 2π = 267.747 by the linearisation. It is the circle where "in" turns into "out": rays with b < 3√3 M fall in, b > 3√3 M escape. In the gravastar picture (interior de Sitter, thin shell near r = 2M, Schwarzschild outside) the photon sphere sits outside the shell at 1.5 × its radius (1.4985 for a shell at 2.002 M), and the de Sitter interior's own horizon radius 1/H (2.003 M, from H² = 2M/a³) meets the shell. That the interior de Sitter space of a gravastar is our universe is the author's reading, `INTERPRETATION`; the photon sphere has no π route yet (listed in `gaps()`).
