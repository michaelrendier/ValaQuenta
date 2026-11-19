"""Test suite for ``ValaQuenta.modules.witches_hat.semiclassical``: where hbar comes from in the hat.

Closed-form actions, the exact quantum thresholds against the classical action, and the Weyl count.  Hat: mu = lambda = 1.
Run from the scratchpad::

    PYTHONPATH=/path/to/ThePlace /path/to/ValaQuenta/.venv/bin/python -m pytest /path/to/ValaQuenta/Testing/test_witches_hat_semiclassical.py -p no:cacheprovider
"""
import math

from ValaQuenta.modules.witches_hat import maths as M
from ValaQuenta.modules.witches_hat import semiclassical as SC

SM = M.lagrangian_sm(mu2=1.0, lam=1.0)


def test_separatrix_actions_closed_forms_and_the_tip_height():
    """W_direct = (2/3)(1 - 2^(-3/2)), W_wall = (2/3) 2^(-3/2), W_total = 2/3 agree with quadrature; in the hat's action unit S0 = V0 tau0 the wall action is 2/3, the sheet spacing 4/3,
    the tip stands at (2/3)(2 sqrt 2 - 1) and the gap above the hilltop is exactly (4 sqrt 2 - 5)/3 = 0.218951."""
    a = SC.separatrix_actions(SM)
    for k in ("W_direct", "W_wall", "W_total"): assert abs(a[k] - a["checks"][k]) < 1e-11
    assert abs(a["wall_in_S0"] - 2/3) < 1e-12 and abs(a["sheet_spacing_in_S0"] - 4/3) < 1e-12 and abs(a["gap"] - (4*math.sqrt(2) - 5)/3) < 1e-12 and abs(a["gap"] - 0.218951) < 1e-6


def test_the_closed_forms_do_not_depend_on_mu_and_lambda_in_natural_units():
    """The ratios in units of S0 are universal for the quartic hat: the same 2/3, 4/3 and gap for any mu and lambda."""
    b = SC.separatrix_actions(M.lagrangian_sm(mu2=2.5, lam=0.7)); assert abs(b["wall_in_S0"] - 2/3) < 1e-12 and abs(b["gap"] - (4*math.sqrt(2) - 5)/3) < 1e-12


def test_exact_quantum_thresholds_follow_the_classical_action_with_a_constant_offset():
    """A new bound state appears at E = 0 at hbar = 0.3412, 0.13082, 0.08091 (exact radial Schroedinger equation, outer radius 2.6 R: converged to these digits).  They follow W_total = pi hbar (n + gamma) with the SAME
    gamma = 0.622 to 0.623 for every n (not the 1/2 of a plain two-turning-point rule); the plain rule is off by 24 %, 8 %, 5 % and the gap closes as n grows."""
    th = SC.exact_thresholds(SM, n_states=3, n_grid=500)
    assert abs(th[0] - 0.3412) < 3e-4 and abs(th[1] - 0.13082) < 1e-4 and abs(th[2] - 0.08091) < 1e-4
    g = SC.offset_gamma(SM, th); assert all(0.61 < x < 0.63 for x in g) and max(g) - min(g) < 0.003


def test_the_weyl_law_counts_the_states_below_the_hilltop():
    """N(hbar) = 1/(6 hbar^2) for the hat (phase-space volume 2 pi^2/3): at hbar = 0.10 the exact count is 16 against 16.67; the law holds to within a few states from hbar = 0.14 down."""
    assert abs(SC.weyl_count(SM, 0.10) - 1/(6*0.10**2)) < 1e-9
    assert abs(SC.exact_count_2d(SM, 0.10) - SC.weyl_count(SM, 0.10)) < 2
