# Engine: Relativity, four spaces with their own jurisdictions

**Module:** `modules/relativity/` (`maths.py`, `minkowski.py`, `curved.py`, `tangent.py`, `metric.py`, `crossings.py`, `bridge.py`, `checks.py`, `tools.py`, `manifest.json`)
**Class:** `RelativityModule`
**Version:** 0.1 (2026-11-19)
**Confidence floor:** ESTABLISHED (the bridge file labels its readings INTERPRETATION)
**Notebook:** [notebooks/engines/26_relativity.ipynb](../notebooks/engines/26_relativity.ipynb) · **Proof locale:** `engine/proof_locale/relativity.json`
**Tests:** `Testing/test_relativity.py` (31) · **Toolbox:** [toolbox/43_relativity.md](toolbox/43_relativity.md)
**Narrative:** `Ainulindale/wiki/143_relativity_four_spaces.md`
**External packages:** `numpy`, `scipy`, `sympy`

The engine is organised by **space**, not by field content (contrast `lagrangian_sm`). Each of the four spaces is declared with the eight fields of the `spatial-simulation` skill (points, axes, motions, invariant, views, acceptance test, repo engine, status) and a **jurisdiction**: the set of operations that are legal in it. The legality test is `bracketing_firing_order.jurisdiction_violation`, reused.

## `maths.py`

`SPACES` → the four declarations (`minkowski`, `curved`, `tangent`, `metric`) with `legal` and `illegal` operation sets. `jurisdiction_map()` → `{space: legal set}`. `jurisdiction_check(space, operation)` → the verdict, plus `declared_illegal` when the space names the operation illegal. `crossing_table()` → every operation named anywhere, with where it is legal and where illegal; an operation legal in one and illegal in another is a *crossing*. Constants: `C`, `G`, `GM_SUN`, `GM_EARTH`, `R_SUN`, `R_EARTH`, `HBAR`, `K_B`, `ARCSEC` with sources in the comments.

## `minkowski.py` (special relativity)

`gamma`, `rapidity`, `boost(beta_vec)`, `invariance_residual(L)`, `velocity_addition`, `rapidity_additivity`, `interval`, `time_dilation`, `length_contraction`, `doppler_longitudinal`, `doppler_factor`, `lightcone_dilation_check(beta)` (a boost scales u = ct + x by 1/k and v = ct − x by k), `thomas_wigner(b1, b2)`, `lorentz_algebra()`, `four_momentum`, `invariant_mass`, `fixed_target_threshold`, `hyperbolic_motion`, `trip_proper_time`, `em_field_invariants`, `em_boost`, `lorentz_derivation()` (symbolic: g²(1 − b²) = 1).

## `curved.py` (general relativity)

`curvature(g, coords)` → Christoffel, Riemann, Ricci, scalar and Einstein tensors of any sympy metric. `kretschmann`, `divergence_of_einstein` (the contracted Bianchi identity). Metrics: `schwarzschild`, `de_sitter_static`, `flrw_flat`, `flrw_curved`. `solution_checks()` → Ricci = 0, K = 48M²/r⁶, G = −Λg, FLRW G_tt, Bianchi. Numbers: `schwarzschild_radius`, `photon_sphere`, `isco`, `kerr_horizons`, `hawking_temperature`, `perihelion_advance_formula`, `mercury_arcsec_per_century` (42.98), `orbit_precession_numeric`, `light_deflection_numeric` (4M/b · (1 + 15πM/16b)), `solar_deflection_arcsec` (1.751), `clock_rate_offsets` (GPS +38.5 µs/day), `tidal_component_schwarzschild`, `geodesic_deviation_numeric`, `binary_pulsar_pdot` (−2.40×10⁻¹²), `gravitational_wave_vacuum_check` (first-order Ricci of a plane wave vanishes iff ω² = k²).

## `tangent.py`, `metric.py`, `crossings.py`

`equivalence_principle_report(r0)` (Γ removed at a point, the curvature scalar survives), `tidal_ellipsoid`. `minisuperspace_friedmann()` (the lapse of the (a, N) slice of the space of metrics is a Lagrange multiplier and its equation is the first Friedmann equation), `linearised_gauge_invariance()`. `newtonian_limit()` (R₀₀ = ∇²Φ), `euclidean_horizon_period()` (smoothness fixes 8πM), `conversion_field_curvature(v)` and `hat_conversion_field()` (wiki 140's v(q) read as the 1+1 metric −v²dt² + dx², R = −2v″/v; INTERPRETATION of the metric), `flat_limit_scaling()`.

## `bridge.py` (the project's own structure)

`prime_boost(p)` (ESTABLISHED arithmetic: the boost with Doppler factor p has β = (p²−1)/(p²+1) and the Pythagorean triple (p²−1, 2p, p²+1)), `compose_prime_boosts(p, q)` (boost(p)∘boost(q) = boost(pq)), `boost_factorisation(k)` (a rational Doppler factor is a unique product of prime boosts: rapidity = Σ e_p ln p). **Reading, INTERPRETATION:** Lorentz composition along a line is prime factorisation of the Doppler factor. Not claimed: that Einstein's equations are contained in or derived from the Null Operator.

## `tools.py`, `checks.py`

`RelativityModule` (37 formulary entries, grouped by space: `mink_*`, `curved_*`, `tangent_*`, `metric_*`, `cross_*`, `bridge_*`); `verify()` (18 numeric checks) and `verify_symbolic()` (7 symbolic checks).

## Findings recorded while building

- Light deflection: the second-order coefficient is 15π/16 · (M/b), not 15π/4 (first draft of the docstring was wrong; the integrated geodesic agrees with 15π/16).
- Thomas–Wigner: the stored boost has −γβ in its first column, so the velocity read from L e₀ is minus u_spatial/u₀.
- Orbit precession: the next periapsis is a *downward* crossing of u′ = 0; the upward crossing is apoapsis.
- Precession at p = 200 M is 4 % above 6πM/p (first-order correction O(M/p)); the ratio tends to 1 as p grows (test).

---

## Gamma function: the n-ball (added 2026-11-27)

Gamma appears in this engine (see the code for where). It is also the bookkeeping of a hypersphere: the Gaussian integral of e^(−|x|²) over n dimensions is (√π)^n = (S/2)·Γ(n/2), so the unit ball has volume V(n) = π^(n/2)/Γ(n/2 + 1) and the unit sphere area S(n) = 2π^(n/2)/Γ(n/2) = n·V(n) for every real n. At n = 2 these are π and 2π, the circle. V peaks at n = 5.2569464 and S at n = 7.2569464 (`bell_curve.nball_peak`, which is the `n* ≈ 5.257` of the Ainulindale texts; its identification with the BAO freeze point is THEORETICAL, not computed). Machinery: `ValaQuenta/modules/bell_curve/maths.py` (`nball_volume`, `nsphere_area`, `nball_peak`); pictures: `gallery/hypergon_constructibility/canvas2d_nball.html` (the curves, the poles of Γ at 0, −1, −2, …) and `canvas2d_frame3d.html` (the curve in the frame n, V, S).
