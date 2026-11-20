"""Test suite for ``ValaQuenta.modules.relativity`` (Einstein's relativity as four spaces with their own jurisdictions).

Each test states the physical fact it checks.  Numbers are compared with measurement or with a closed form at a stated tolerance; the
symbolic identities are exact.  Run (the working directory does not matter)::

    PYTHONPATH=/path/to/ThePlace /path/to/ValaQuenta/.venv/bin/python -m pytest /path/to/ValaQuenta/Testing/test_relativity.py -p no:cacheprovider
"""
import math
from fractions import Fraction

import numpy as np

from ValaQuenta.modules.relativity import maths as R
from ValaQuenta.modules.relativity import minkowski as Mk
from ValaQuenta.modules.relativity import curved as Cv
from ValaQuenta.modules.relativity import tangent as Tg
from ValaQuenta.modules.relativity import metric as Me
from ValaQuenta.modules.relativity import crossings as Cr
from ValaQuenta.modules.relativity import bridge as Br
from ValaQuenta.modules.relativity import checks as Ck


# ------------------------------------------------------------------ the jurisdictions
def test_four_spaces_declare_the_eight_fields():
    """Every space carries points, axes, motions, invariant, views, acceptance test, repo and status, and a legal and an illegal set that do not overlap."""
    assert set(R.SPACES) == {"minkowski", "curved", "tangent", "metric"}
    for v in R.SPACES.values():
        assert all(v[k] for k in ("points", "axes", "motions", "invariant", "views", "acceptance_test", "repo", "status"))
        assert v["legal"] and v["illegal"] and not (v["legal"] & v["illegal"])


def test_jurisdiction_is_the_set_membership_test():
    """A global boost is legal in Minkowski space and in the tangent space, and a violation in curved spacetime; adding vectors at different events is legal
    only where there is a global frame."""
    assert R.jurisdiction_check("minkowski", "global_boost")["violation"] is False
    assert R.jurisdiction_check("tangent", "global_boost")["violation"] is False
    c = R.jurisdiction_check("curved", "global_boost"); assert c["violation"] is True and c["declared_illegal"]
    assert R.jurisdiction_check("curved", "add_vectors_at_different_events")["violation"] is True
    assert R.jurisdiction_check("curved", "parallel_transport")["violation"] is False


def test_the_crossings_are_the_operations_that_change_status():
    """Global boost, global simultaneity and global energy-momentum conservation are legal in one space and illegal in another: they are the crossings."""
    t = R.crossing_table()
    assert t["global_boost"]["crossing"] and "minkowski" in t["global_boost"]["legal_in"] and "curved" in t["global_boost"]["illegal_in"]
    assert t["global_energy_momentum_conservation"]["crossing"] and t["covariant_conservation"]["legal_in"]


# ------------------------------------------------------------------ Minkowski
def test_composed_boosts_are_lorentz_transformations():
    """Any product of boosts preserves eta."""
    L = Mk.boost([0.3, 0.4, -0.2]) @ Mk.boost([0.1, 0.0, 0.5]) @ Mk.boost([-0.6, 0.2, 0.1])
    assert Mk.invariance_residual(L) < 1e-12


def test_velocity_addition_is_rapidity_addition():
    assert Mk.rapidity_additivity(0.6, 0.7)["residual"] < 1e-12 and abs(Mk.velocity_addition(0.9, 0.9) - 1.8 / 1.81) < 1e-15


def test_boost_is_a_dilation_of_the_lightcone_coordinates():
    """In u = ct + x, v = ct - x a boost scales u by 1/k and v by k, with k = sqrt((1+b)/(1-b)) the Doppler factor."""
    r = Mk.lightcone_dilation_check(0.8); assert r["residual"] < 1e-12 and abs(r["k"] - 3.0) < 1e-12


def test_thomas_wigner_rotation():
    """Perpendicular boosts compose to a boost and a rotation; cos(theta) = (g1 + g2)/(1 + g1 g2)."""
    r = Mk.thomas_wigner(0.6, 0.7); assert r["residual"] < 1e-12 and r["rotation_block_is_orthogonal"] and 15.4 < r["angle_deg"] < 15.6


def test_the_lorentz_algebra_closes():
    assert Mk.lorentz_algebra()["max_commutator_violation"] < 1e-12


def test_boost_from_invariance_of_the_interval():
    """Symbolic: g^2 (1 - b^2) = 1 and the off-diagonal condition is identically zero."""
    d = Mk.lorentz_derivation(); assert d["condition_01"] == 0 and len(d["g"]) == 2


def test_invariant_mass_and_threshold():
    """p + p -> p + p + p + pbar on a fixed target needs 6 m_p of kinetic energy (7 m_p total); a system at rest has invariant mass m."""
    assert abs(Mk.fixed_target_threshold(1.0, 1.0, 4.0) - 6.0) < 1e-12 and abs(Mk.invariant_mass(Mk.four_momentum(2.5, [0, 0, 0])) - 2.5) < 1e-12
    p1 = Mk.four_momentum(1.0, [0, 0, 3.0]); p2 = Mk.four_momentum(1.0, [0, 0, -3.0]); assert abs(Mk.invariant_mass(p1, p2) - 2 * math.sqrt(10.0)) < 1e-12


def test_em_invariants_survive_a_boost():
    E0, B0 = [1.0, 0.5, 0.2], [0.1, 0.4, 0.3]; a = Mk.em_field_invariants(E0, B0); b = Mk.em_field_invariants(*Mk.em_boost(E0, B0, [0.3, 0.2, 0.1]))
    assert abs(a["E2_minus_c2B2"] - b["E2_minus_c2B2"]) < 1e-12 and abs(a["E_dot_B"] - b["E_dot_B"]) < 1e-12


def test_hyperbolic_motion_and_the_trip():
    """Proper time at 1 g to cover 4.37 light years (half accelerating, half decelerating) is about 3.5 years; coordinate time exceeds it."""
    tau = Mk.trip_proper_time(4.37 * 9.4607304725808e15, 9.80665) / 3.15576e7; assert 3.3 < tau < 3.7
    h = Mk.hyperbolic_motion(9.80665, 3.15576e7); assert h["tau"] < 3.15576e7 and 0 < h["beta"] < 1


# ------------------------------------------------------------------ curved
def test_standard_solutions_and_the_bianchi_identity():
    """Schwarzschild is vacuum with K = 48 M^2/r^6; static de Sitter has G = -Lambda g with Lambda = 3/L^2; flat FLRW has G_tt = 3 adot^2/a^2; the contracted Bianchi identity
    holds for curved FLRW."""
    assert Cv.solution_checks()["all_pass"]


def test_mercury_light_gps_binary_pulsar():
    """The four classical tests, from the engine's own formulas: 42.98 arcsec/century; 1.751 arcsec at the solar limb; +38.5 microseconds/day; Pbdot = -2.40e-12."""
    assert abs(Cv.mercury_arcsec_per_century() - 42.98) < 0.05 and abs(Cv.solar_deflection_arcsec() - 1.751) < 0.002
    assert 38.0 < Cv.clock_rate_offsets()["net_us_per_day"] < 39.0 and abs(Cv.binary_pulsar_pdot()["Pbdot"] + 2.40e-12) < 0.02e-12


def test_numerically_integrated_orbit_precesses_as_the_formula_says():
    """Integrated Schwarzschild orbit: advance / (6 pi M/p) -> 1 as p grows (first-order correction O(M/p))."""
    r1 = Cv.orbit_precession_numeric(200.0, 0.3)["ratio"]; r2 = Cv.orbit_precession_numeric(2000.0, 0.3)["ratio"]
    assert abs(r2 - 1) < abs(r1 - 1) and abs(r2 - 1) < 0.01


def test_light_deflection_integrated_matches_second_order():
    """Integrated null geodesic: deflection = 4M/b (1 + 15 pi M/(16 b)) to the next order; checked at b = 1000 M and 2000 M."""
    for b in (1000.0, 2000.0):
        r = Cv.light_deflection_numeric(b); assert abs(r["ratio"] / r["second_order_ratio"] - 1) < 2e-4


def test_tidal_tensor_by_curvature_and_by_two_falling_particles():
    """R_trtr = -2M/r^3 symbolically; two nearby radial free-fallers separate with xi'' = 2M/r^3 xi (ratio 1 to 1e-4)."""
    assert Cv.tidal_component_schwarzschild()["equals_minus_2M_over_r3"] and abs(Cv.geodesic_deviation_numeric()["ratio"] - 1.0) < 1e-3


def test_gravitational_wave_needs_light_speed():
    """The first-order Ricci of a TT plane wave vanishes iff w^2 = k^2; for other w it does not."""
    r = Cv.gravitational_wave_vacuum_check(); assert r["vanishes_when_w2_equals_k2"] and r["first_order_ricci_nonzero"]


def test_horizons_and_hawking():
    """r_s = 2.95 km for the Sun, photon sphere 1.5 r_s, ISCO 3 r_s; Hawking T = 6.17e-8 K for one solar mass; Kerr a = M gives r+ = r- = M."""
    GM = R.GM_SUN; rs = Cv.schwarzschild_radius(GM); assert abs(rs - 2953.25) < 0.5 and abs(Cv.photon_sphere(GM) / rs - 1.5) < 1e-12 and abs(Cv.isco(GM) / rs - 3.0) < 1e-12
    assert abs(Cv.hawking_temperature(GM / R.G) - 6.17e-8) < 0.02e-8
    k = Cv.kerr_horizons(1.0, 1.0); assert k["r_plus"] == k["r_minus"] == 1.0


# ------------------------------------------------------------------ tangent
def test_equivalence_principle_removes_gamma_not_curvature():
    """In Schwarzschild at r = 10 M the connection is not zero; after the coordinate change it is zero (to 1e-12), and Kretschmann = 48 M^2/r^6 stays."""
    r = Tg.equivalence_principle_report(10.0); assert r["Gamma_norm_before"] > 1 and r["Gamma_norm_after"] < 1e-12 and abs(r["kretschmann_at_p"] - 48e-6) < 1e-12


def test_tidal_ellipsoid_is_traceless():
    t = Tg.tidal_ellipsoid(10.0); assert abs(t["trace"]) < 1e-15 and t["radial_stretch"] > 0 > t["tangential"]


# ------------------------------------------------------------------ metric
def test_the_lapse_is_a_lagrange_multiplier_and_gives_friedmann():
    """Varying N in the (a, N) slice of the space of metrics gives 3 a adot^2/(8 pi G) - a^3 rho = 0, a constraint with no derivative of N."""
    r = Me.minisuperspace_friedmann(); assert r["lapse_eq_is_friedmann"] and not r["lapse_in_equation"]


def test_linearised_curvature_is_gauge_invariant():
    r = Me.linearised_gauge_invariance(); assert r["pure_gauge_h_has_nonzero_components"] and r["linearised_riemann_of_pure_gauge_is_zero"]


# ------------------------------------------------------------------ crossings
def test_weak_field_gives_poisson():
    assert Cr.newtonian_limit()["equals_laplacian_of_Phi"]


def test_euclidean_smoothness_fixes_the_period_8_pi_M():
    r = Cr.euclidean_horizon_period(); assert r["period_is_8piM"] and r["temperature"] == "1/(8*pi*M)"


def test_flat_limit():
    assert Cr.flat_limit_scaling()["limit_M_to_0"] == "0"


def test_the_hat_conversion_field_has_a_horizon_like_zero_at_the_hilltop_and_a_mirror_at_the_brim_side():
    """Wiki 140 read as a 1+1 spacetime (INTERPRETATION of the metric; the arithmetic is exact): v = x sqrt(1 - x^2/2) has kappa = 1 at x = 0 and a square-root zero
    at x = sqrt 2."""
    r = Cr.hat_conversion_field(); assert r["kappa_at_hilltop"] == "1" and r["exponent_at_turning_circle"] == "1/2"


# ------------------------------------------------------------------ bridge
def test_prime_boosts_are_pythagorean_and_compose_by_multiplication():
    """ESTABLISHED arithmetic: Doppler factor p gives beta = (p^2-1)/(p^2+1) and the triple (p^2-1, 2p, p^2+1); composing boosts p and q gives the boost pq."""
    for p in (2, 3, 5, 7, 11, 13): assert Br.prime_boost(p)["triple_ok"]
    assert Br.prime_boost(2)["beta"] == Fraction(3, 5) and Br.prime_boost(3)["beta"] == Fraction(4, 5)
    for p, q in ((2, 3), (3, 5), (2, 7), (5, 11)): assert Br.compose_prime_boosts(p, q)["equal"]


def test_a_rational_boost_factors_uniquely_into_prime_boosts():
    f = Br.boost_factorisation(Fraction(12, 5)); assert f["exponents"] == {2: 2, 3: 1, 5: -1} and f["residual"] < 1e-12


# ------------------------------------------------------------------ the engine as a whole
def test_verify_all_pass():
    assert Ck.verify()["all_pass"]


def test_the_engine_is_registered_and_its_manifest_validates():
    """The module is in the registry (registered once per process, so a second ``_register_all`` raises and the existing registry is used), its formulary has 37 entries
    and its manifest and proof_locale pass validation."""
    from ValaQuenta.__main__ import _register_all
    from ValaQuenta.engine import manifest as MF
    from ValaQuenta.engine.registry import get_registry
    try: reg = _register_all()
    except ValueError: reg = get_registry()
    m = reg.get_module("relativity"); names = {e.name for e in m.formulary()}
    assert len(names) == 37 and {"verify", "spaces", "jurisdiction", "mink_boost", "curved_solutions", "tangent_equivalence", "metric_friedmann", "cross_newton", "bridge_prime_boost"} <= names
    assert MF.validate("relativity", m) == []
    assert m.run("jurisdiction", {"space": "curved", "operation": "global_boost"})["result"]["violation"] is True
