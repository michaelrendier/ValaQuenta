"""Test suite for ``ValaQuenta.modules.witches_hat.action`` (the path of action, mapped).

Closed forms first (free particle, harmonic oscillator and its Euclidean twin), then the two independent routes to the same
quantity on the real hat (boundary-value stationary path against the shooting family), then the Euclidean bounce against an
integrated equation of motion.  Nothing here aims a path or expects a focus: the focus tests use the harmonic well, where
the textbook answer is known (every path from A refocuses at -A when wT = pi), and the hat is only checked for consistency.
Run from the scratchpad (the working directory does not matter)::

    PYTHONPATH=/path/to/ThePlace python -m pytest /path/to/ValaQuenta/Testing/test_witches_hat_action.py -p no:cacheprovider
"""
import math

import numpy as np
from scipy import integrate

from ValaQuenta.modules.witches_hat import action as A
from ValaQuenta.modules.witches_hat import maths as M


def harmonic(w):
    """Model dict for V = w^2 |q|^2 / 2 (isotropic oscillator).

    :param w: angular frequency.
    :returns: a model dict understood by ``action``.
    :rtype: dict
    """
    return {"model": "harmonic", "V2": lambda x, y: 0.5*w*w*(np.asarray(x, float)**2 + np.asarray(y, float)**2),
            "grad": lambda x, y: (w*w*np.asarray(x, float), w*w*np.asarray(y, float)), "brim_radius": 1.0}


FREE = {"model": "free", "V2": lambda x, y: 0*np.asarray(x, float), "grad": lambda x, y: (0*np.asarray(x, float), 0*np.asarray(y, float)), "brim_radius": 1.0}
SM = M.lagrangian_sm(mu2=1.0, lam=1.0)            # brim radius 1, depth 1/4, hilltop at the origin
P, Q = (1.0, 0.0), (0.3, 0.4)


def test_free_particle_action_is_the_closed_form():
    """S = |B - A|^2 / (2T) for V = 0, to the discretisation."""
    p = A.stationary_paths(FREE, P, Q, 2.0)
    assert len(p) == 1 and abs(p[0]["S"] - (0.7**2 + 0.4**2)/4.0) < 1e-12 and p[0]["index"] == 0


def test_harmonic_action_converges_to_the_closed_form_at_second_order():
    """S = w/(2 sin wT) [(|A|^2 + |B|^2) cos wT - 2 A.B]; the discrete error falls by 4 when N doubles (second order), so the tolerance is a statement about N.
    Index 0 below wT = pi and 2 above (a 2-D isotropic well refocuses in both directions at once)."""
    cl = lambda T: 1/(2*math.sin(T))*((1.25)*math.cos(T) - 0.6)
    for T, idx in ((0.9*math.pi, 0), (1.1*math.pi, 2)):
        e = [abs(A.stationary_paths(harmonic(1.0), P, Q, T, N=N)[0]["S"] - cl(T)) for N in (100, 200, 400)]
        p = A.stationary_paths(harmonic(1.0), P, Q, T, N=200)
        assert abs(e[0]/e[1] - 4) < 0.1 and abs(e[1]/e[2] - 4) < 0.1 and e[2] < 2e-4 and p[0]["index"] == idx, (T, e)


def test_euclidean_signature_is_the_wick_rotated_action():
    """Euclidean twin of the oscillator: S_E = w/(2 sinh wT) [(|A|^2 + |B|^2) cosh wT - 2 A.B], and the index is 0 (no conjugate points)."""
    T = 1.3; p = A.stationary_paths(harmonic(1.0), P, Q, T, N=200, signature="euclidean")
    assert abs(p[0]["S"] - 1/(2*math.sinh(T))*(1.25*math.cosh(T) - 0.6)) < 5e-4 and p[0]["index"] == 0


def test_the_first_variation_vanishes_and_the_second_has_both_signs_past_a_conjugate_point():
    """Stationary: dS/d eps ~ 0 for every variation.  Below the conjugate point all neighbours cost more; above it two directions cost less."""
    lo = A.stationary_paths(harmonic(1.0), P, Q, 0.9*math.pi, N=160)[0]; hi = A.stationary_paths(harmonic(1.0), P, Q, 1.1*math.pi, N=160)[0]
    a = A.trial_variations(harmonic(1.0), lo, 0.9*math.pi); b = A.trial_variations(harmonic(1.0), hi, 1.1*math.pi)
    assert a["first_variation_max"] < 1e-8 and b["first_variation_max"] < 1e-8
    assert a["fraction_negative"] == 0.0 and np.all(a["eigenmode_dS"] > 0)
    assert np.sum(b["eigenmode_dS"] < 0) == b["index"] == 2 and np.all(b["eigenmode_dS"][2:] > 0)


def test_neighbouring_paths_cost_more_and_less_on_the_real_hat_over_a_long_time():
    """On the hat (the real quartic), a long enough stationary path has negative directions: some neighbours do less work."""
    p = A.stationary_paths(SM, (1.0, 0.0), (-0.2, 0.3), 9.0, N=200)
    assert p and any(f["index"] >= 1 for f in p)
    f = [f for f in p if f["index"] >= 1][0]; tv = A.trial_variations(SM, f, 9.0)
    assert np.any(tv["eigenmode_dS"] < 0) and tv["first_variation_max"] < 1e-4


def test_conjugate_point_of_the_harmonic_well_emerges_from_the_family():
    """Every path from A refocuses at -A at wT = pi: found as the SECOND caustic (order 2) from the Jacobian, with no aim given.  The first (order 1) is the fold,
    the envelope of the orbits, which lies between radius 1 and sqrt(2E) = sqrt 2 at times pi/4 to 3 pi/4."""
    fam = A.ray_family(harmonic(1.0), (1.0, 0.0), E=1.0, n_theta=36, t_max=3.5, n_t=700)
    c = A.caustic_points(fam); two = c["xy"][c["order"] == 2]; one = c["xy"][c["order"] == 1]
    assert len(two) >= 30 and np.allclose(two[:, 0], -1.0, atol=2e-3) and np.allclose(two[:, 1], 0.0, atol=2e-3) and np.allclose(c["t"][c["order"] == 2], math.pi, atol=1e-2)
    r1 = np.hypot(one[:, 0], one[:, 1]); assert r1.min() > 0.99 and r1.max() < math.sqrt(2) + 1e-3


def test_a_free_family_has_no_caustic_and_the_family_conserves_energy():
    """V = 0: paths never cross again, so D has no sign change.  On the hat the energy E = v^2/2 + U is conserved along every path."""
    fam = A.ray_family(FREE, (1.0, 0.0), E=0.5, n_theta=24, t_max=4.0, n_t=300)
    assert len(A.caustic_points(fam)["xy"]) == 0
    fam = A.ray_family(SM, (1.0, 0.0), E=0.0, n_theta=12, t_max=4.0, n_t=300); U, _, _ = A.motion_potential(SM)
    En = 0.5*np.sum(fam["v"]**2, -1) + U(fam["q"]); assert np.max(np.abs(En - 0.0)) < 1e-7


def test_two_independent_routes_to_the_action_agree_on_the_hat():
    """The shooting family gives S = W - E t along a path; the boundary-value solver finds ALL stationary paths between the same two events.  The shot path is one of them
    (same action, same shape) and it has Morse index 1: a lower-action stationary path with the same endpoints exists (more work on one, less on the other)."""
    fam = A.ray_family(SM, (1.0, 0.0), E=0.0, n_theta=9, t_max=2.0, n_t=201); i, j = 2, 200
    B = fam["q"][i, j]; T = fam["t"][j]; ps = A.stationary_paths(SM, (1.0, 0.0), B, T, N=200)
    match = [p for p in ps if abs(p["S"] - fam["S"][i, j]) < 5e-4 and np.max(np.abs(p["q"][100] - fam["q"][i, 100])) < 5e-3]
    assert len(match) == 1 and match[0]["index"] == 1 and ps[0]["S"] < match[0]["S"] - 1e-3 and ps[0]["index"] == 0


def test_euclidean_bounce_speed_time_and_action_against_integrated_motion():
    """Radial release at rest in -V: speed at the hilltop = sqrt(2 (U(r0) - U(0))), the time against an integrated equation of motion,
    and the time grows without bound as r0 approaches the brim."""
    U0 = lambda r: r*r/2 - r**4/4
    for r0 in (0.5, 0.8):
        e = A.euclidean_radial_release(SM, r0)
        assert abs(e["speed_at_hilltop"] - math.sqrt(2*U0(r0))) < 1e-9
        ev = lambda t, y: y[0]; ev.terminal = True; ev.direction = -1
        s = integrate.solve_ivp(lambda t, y: [y[1], -(y[0] - y[0]**3)], (0, 50), [r0, 0.0], events=ev, rtol=1e-11, atol=1e-13)
        assert abs(e["tau"] - s.t_events[0][0]) < 1e-9, (r0, e["tau"], s.t_events[0][0])
        assert abs(e["S_E"] - (e["W"] - e["E_U"]*e["tau"])) < 1e-12
    t = [A.euclidean_radial_release(SM, r)["tau"] for r in (0.5, 0.9, 0.99, 0.999)]
    assert all(b > a for a, b in zip(t, t[1:])) and t[-1] - t[-2] > t[-2] - t[-3] - 1.0


def test_summary_and_profile_are_descriptive_plain_data():
    """The reports return plain data and invent nothing: counts match the points, the profile has one entry per launch direction."""
    fam = A.ray_family(SM, (1.0, 0.0), E=0.0, n_theta=24, t_max=4.0, n_t=300); c = A.caustic_points(fam); s = A.caustic_summary(SM, fam, c); pr = A.closest_approach_profile(SM, fam)
    assert s["n_caustic_points"] == len(c["xy"]) and len(pr["closest_over_brim"]) == 24 and s["brim"] == 1.0
    assert abs(s["closest_path_to_hilltop_over_brim"] - pr["closest_over_brim"].min()) < 1e-12


def test_static_hat_conserves_energy_and_moving_hat_exchanges_it_by_the_identity():
    """Original L_dynamic (wiki 51): a time-dependent background.  Static hat: E conserved.  Moving hat: dE/dt = dV/dt at fixed q, so the energy change equals the accumulated
    exchange to integration accuracy (an identity, tested), and for a fast hat the energy is borrowed and only partly returned (max excursion above the final change)."""
    r0 = A.moving_hat_exchange(SM, (1.0, 0.0), (0.0, 0.7), (0.0, 0.0), 20.0)
    assert r0["dE_max_excursion"] < 1e-8 and r0["identity_residual"] < 1e-8
    r = A.moving_hat_exchange(SM, (1.0, 0.0), (0.0, 0.7), (0.6, 0.0), 20.0)
    assert r["identity_residual"] < 1e-8 and abs(r["dE_final"]) > 0.1 and r["dE_max_excursion"] > 1.5*abs(r["dE_final"])


def test_ray_bundle_agrees_with_the_variational_integrator():
    """The vectorised bundle and the single-source integrator (``ray_family``) give the same paths, reduced action and arc length for the same launch."""
    fam = A.ray_family(SM, (1.0, 0.0), E=0.0, n_theta=5, t_max=2.0, n_t=201)
    th = fam["theta"]; sp = math.sqrt(2*(0.0 - float(M.lagrangian_sm(mu2=1.0, lam=1.0)["V"](1.0)))); vel = np.stack([sp*np.cos(th), sp*np.sin(th)], 1)
    b = A.ray_bundle(SM, np.tile([[1.0, 0.0]], (5, 1)), vel, 2.0, n_steps=2000, store_every=20)
    assert np.max(np.abs(b["q"][:, -1] - fam["q"][:, -1])) < 1e-6 and np.max(np.abs(b["W"][:, -1] - fam["W"][:, -1])) < 1e-6
    assert np.max(np.abs(b["E_final"] - b["E_initial"])) < 1e-9


def test_the_action_cone_tip_is_the_closed_form_and_the_bundle_finds_it_without_aiming():
    """Radial family at E = 0: W_tip = (2/3)[(1 - r^2/2)^(3/2)] from r = 1 to 0 = 0.43096 (mu = lambda = 1), natural-unit height 1.2192 (gap 0.2192 above the hilltop).  The brim bundle (every source, every direction,
    selected only by passing within 0.15 of the hilltop) places its tip on the hilltop and reproduces that height."""
    c = A.cone_tip_height(SM, 0.0)
    assert abs(c["W_tip"] - (2/3)*(1 - 0.5**1.5)) < 1e-9 and abs(c["gap"] - 0.2192) < 1e-3 and c["p_tip"] == 0.0
    b = A.brim_bundle(SM, n_sources=8, n_dirs=721, T=6.0, n_steps=1200, eps=0.15); r = A.tip_report(SM, b)
    assert b["n_selected"] > 20 and r["offset"] < 0.02 and abs(r["W_tip"] - c["W_tip"]) < 0.01
    assert len(r["sheets"]) == 2 and abs(r["sheets"][1]["W"] - (c["W_tip"] + 2*0.23572)) < 0.01         # the second sheet: out to the wall and back (2 x the action from the brim to r = sqrt 2)
