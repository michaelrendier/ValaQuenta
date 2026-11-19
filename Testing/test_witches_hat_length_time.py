"""Test suite for ``ValaQuenta.modules.witches_hat.length_time``: length and time as one thing, and the swap between them.

Each test is a claim of Ainulindale wiki 140.  The hat is the Standard-Model quartic with mu = lambda = 1 (brim radius 1, depth 1/4); energies are chosen so the speed field v = sqrt(2 (E - V)) is
positive in the allowed region (E = 0.05) or, for the separatrix claims, exactly zero at the hilltop (E = 0).
Run from the scratchpad::

    PYTHONPATH=/path/to/ThePlace /path/to/ValaQuenta/.venv/bin/python -m pytest /path/to/ValaQuenta/Testing/test_witches_hat_length_time.py -p no:cacheprovider
"""
import math

import numpy as np

from ValaQuenta.modules.witches_hat import action as A
from ValaQuenta.modules.witches_hat import length_time as LT
from ValaQuenta.modules.witches_hat import maths as M

SM = M.lagrangian_sm(mu2=1.0, lam=1.0)


def test_every_classical_path_is_null_in_the_optical_metric():
    """|dq/dt| = v(q) = sqrt(2 (E - V)) along every path of the family: length = v dt, an interval of zero length in -v^2 dt^2 + |dq|^2."""
    fam = A.ray_family(SM, (1.0, 0.0), E=0.05, n_theta=12, t_max=3.0, n_t=200); V = lambda q: -0.5*np.sum(q**2, -1) + 0.25*np.sum(q**2, -1)**2
    dev = np.abs(np.hypot(fam["v"][..., 0], fam["v"][..., 1]) - np.sqrt(2*(0.05 - V(fam["q"])))); assert dev.max() < 1e-7


def test_in_the_transit_ruler_a_radial_path_is_a_45_degree_line():
    """rho(r) = integral dr/v (length measured in time): rho(r(t)) + t is constant along the radial path to 1e-9: the potential has become the ruler."""
    assert LT.radial_worldline(SM, 0.05, 6.0)["deviation"] < 1e-9


def test_time_is_the_energy_derivative_of_the_action_and_the_relation_survives_the_swap():
    """t = dW/dE for a non-radial path (central difference at fixed endpoints) and, in the forbidden region, dB/dE = -tau (barrier action against Euclidean time)."""
    c = LT.conjugacy(SM, 0.05); b = LT.barrier_conjugacy(SM, 0.02)
    assert c["relative_error"] < 1e-6 and b["relative_error"] < 1e-6 and abs(b["r1"] - 1.4280) < 1e-3


def test_least_time_and_least_action_are_different_paths_unless_the_speed_is_constant():
    """Same endpoints, same energy: the path of least action and the path of least time differ (time excess 35 % for one pair, 5 % for another); with a constant speed they coincide."""
    r = LT.two_rulers(SM, (1.0, 0.0), (-0.6, 0.8), 0.05); r2 = LT.two_rulers(SM, (1.0, 0.0), (0.2, -0.3), 0.05); r0 = LT.two_rulers(SM, (1.0, 0.0), (-0.6, 0.8), 0.05, constant_speed=True)
    assert r["split"] > 0.3 and r["max_separation"] > 0.4 and r2["split"] > 0.03 and r0["split"] < 1e-9 and r0["max_separation"] < 1e-6


def test_inverting_the_speed_field_exchanges_the_two_rulers():
    """v -> 1/v exchanges the functionals sum |dq| v and sum |dq|/v: the least-action path of the inverted world is the least-time path of the original (and W and T swap)."""
    a = LT.two_rulers(SM, (1.0, 0.0), (-0.6, 0.8), 0.05, N=100); b = LT.two_rulers(SM, (1.0, 0.0), (-0.6, 0.8), 0.05, N=100, invert=True)
    assert abs(b["W_of_action_path"] - a["T_min"]) < 1e-6 and abs(b["T_min"] - a["W_of_action_path"]) < 1e-6        # the two discrete functionals are identical; the residual is the optimiser (1.8e-6 at N = 50, 2e-7 at N = 100)


def test_the_hilltop_is_at_infinite_time_and_finite_length_and_the_wall_at_finite_time():
    """E = 0: rho grows like ln r (slope 1) toward the hilltop while the action W stays 0.43096; the turning circle r = sqrt 2 is reached in rho = ln(1 + sqrt 2) = 0.88137."""
    h = LT.hilltop_clock(SM); w = LT.wall_transit(SM, 0.0)
    assert all(abs(s - 1.0) < 2e-3 for s in h["slopes"]) and abs(h["W_to_hilltop"] - 0.43096) < 1e-4
    assert abs(w["r_turn"] - math.sqrt(2)) < 1e-9 and abs(w["rho_brim_to_wall"] - math.log(1 + math.sqrt(2))) < 1e-7        # quadrature near the square-root endpoint: 4e-9


def test_the_optical_signature_swaps_at_the_turning_circle():
    """At E = 0: Lorentzian for 0 < r < sqrt 2, the cone closes at the hilltop and at r = sqrt 2, Euclidean beyond (time becomes imaginary)."""
    sig = dict((round(r, 3), s) for r, v, s in LT.signature_map(SM, 0.0, [0.0, 0.5, 1.0, 1.3, math.sqrt(2), 1.6]))
    assert sig[0.0].startswith("null") and sig[0.5] == "Lorentzian" and sig[1.3] == "Lorentzian" and sig[1.414].startswith("null") and sig[1.6] == "Euclidean"


def test_penrose_arctan_and_smith_tanh_are_one_map_under_the_swap():
    """tanh(i x/2) = i tan(x/2); 2 arctan(tanh(x/2)) = arctan(sinh x) (Gudermannian); the Smith map (s - 1)/(s + 1) = tanh(ln(s)/2): all to rounding."""
    c = LT.compactifications(); assert max(c.values()) < 1e-12


def test_simple_zero_is_at_infinite_time_and_square_root_zero_at_finite_time():
    """The horizon property classified: v ~ kappa (r - r_h) gives rho ~ (1/kappa) ln distance (infinite transit time): the hat's E = 0 hilltop has kappa = 1 and Schwarzschild's f = 1 - 2M/r (M = 1)
    has kappa = 1/(2M) = 0.5; a square-root zero (the turning circle) has finite transit time."""
    V = lambda r: -0.5*r*r + 0.25*r**4
    hill = LT.zero_of_the_conversion_field(lambda r: math.sqrt(max(-2*V(r), 0.0)), 0.0, side=1); schw = LT.zero_of_the_conversion_field(lambda r: 1 - 2.0/r, 2.0, side=1)
    wall = LT.zero_of_the_conversion_field(lambda r: math.sqrt(max(-2*V(r), 1e-300)), math.sqrt(2), side=-1)
    assert abs(hill["kappa"] - 1.0) < 0.01 and abs(schw["kappa"] - 0.5) < 0.01 and wall["finite"]
