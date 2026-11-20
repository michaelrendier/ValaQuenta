# SPDX-License-Identifier: GPL-3.0-only
"""Verification of the relativity engine: fast numeric checks (``verify``) and the slower symbolic checks (``verify_symbolic``)."""
from __future__ import annotations
import math
from fractions import Fraction as Fr
from . import maths as R, minkowski as Mk, curved as Cv, tangent as Tg, crossings as Cr, bridge as Br


def verify() -> dict:
    """Numeric checks, each against a stated tolerance.  All must pass."""
    ck = {}
    L = Mk.boost([0.3, 0.4, -0.2]) @ Mk.boost([0.1, 0.0, 0.5]); ck["composed_boosts_are_lorentz"] = Mk.invariance_residual(L) < 1e-12
    ck["rapidity_additive"] = Mk.rapidity_additivity(0.6, 0.7)["residual"] < 1e-12
    ck["lightcone_dilation"] = Mk.lightcone_dilation_check(0.6)["residual"] < 1e-12
    ck["thomas_wigner_formula"] = Mk.thomas_wigner(0.6, 0.7)["residual"] < 1e-12
    ck["lorentz_algebra_closes"] = Mk.lorentz_algebra()["max_commutator_violation"] < 1e-12
    ck["pair_production_threshold_6mp"] = abs(Mk.fixed_target_threshold(1.0, 1.0, 4.0) - 6.0) < 1e-12
    p = Mk.four_momentum(1.0, [0.0, 0.0, 0.0]); ck["invariant_mass_rest"] = abs(Mk.invariant_mass(p) - 1.0) < 1e-12
    ck["mercury_43_arcsec"] = abs(Cv.mercury_arcsec_per_century() - 42.98) < 0.05
    ck["solar_deflection_1p75"] = abs(Cv.solar_deflection_arcsec() - 1.751) < 0.005
    ck["gps_net_38us"] = 38.0 < Cv.clock_rate_offsets()["net_us_per_day"] < 39.0
    ck["precession_numeric_vs_formula"] = abs(Cv.orbit_precession_numeric(200.0, 0.3)["ratio"] - 1.0) < 0.05
    ck["deflection_numeric_vs_formula"] = abs(Cv.light_deflection_numeric(2000.0)["ratio"] / Cv.light_deflection_numeric(2000.0)["second_order_ratio"] - 1.0) < 0.01
    ck["tidal_deviation"] = abs(Cv.geodesic_deviation_numeric()["ratio"] - 1.0) < 1e-3
    ck["prime_boost_pythagorean"] = all(Br.prime_boost(q)["triple_ok"] for q in (2, 3, 5, 7, 11, 13))
    ck["prime_boost_composition"] = all(Br.compose_prime_boosts(a, b)["equal"] for a, b in ((2, 3), (3, 5), (2, 7), (5, 11)))
    ck["jurisdiction_curved_no_global_boost"] = R.jurisdiction_check("curved", "global_boost")["violation"] is True
    ck["jurisdiction_minkowski_global_boost"] = R.jurisdiction_check("minkowski", "global_boost")["violation"] is False
    eq = Tg.equivalence_principle_report(); ck["gamma_removed_curvature_stays"] = eq["Gamma_norm_before"] > 1e-6 and eq["Gamma_norm_after"] < 1e-12 and eq["curvature_survives"]
    return {"checks": ck, "all_pass": all(ck.values()), "n": len(ck)}


def verify_symbolic() -> dict:
    """Symbolic checks (sympy; a few seconds to a minute)."""
    from . import metric as Me
    ck = {}; s = Cv.solution_checks(); ck["solutions"] = s["all_pass"]
    ck["tidal_minus_2M_over_r3"] = Cv.tidal_component_schwarzschild()["equals_minus_2M_over_r3"]
    ck["friedmann_from_lapse"] = Me.minisuperspace_friedmann()["lapse_eq_is_friedmann"]
    ck["gauge_invariance"] = Me.linearised_gauge_invariance()["linearised_riemann_of_pure_gauge_is_zero"]
    ck["newtonian_limit"] = Cr.newtonian_limit()["equals_laplacian_of_Phi"]
    ck["euclidean_period_8piM"] = Cr.euclidean_horizon_period()["period_is_8piM"]
    ck["gw_vacuum_when_w2_k2"] = Cv.gravitational_wave_vacuum_check()["vanishes_when_w2_equals_k2"]
    return {"checks": ck, "all_pass": all(ck.values()), "n": len(ck)}
