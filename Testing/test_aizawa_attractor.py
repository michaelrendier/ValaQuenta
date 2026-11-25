"""Tests for the Aizawa attractor engine, ValaQuenta.modules.aizawa_attractor (v1.0, 2026-11-24)."""
import math, os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ValaQuenta.modules.aizawa_attractor import maths as M
from ValaQuenta.modules.aizawa_attractor.tools import AizawaAttractorModule

ORB = M.orbit(3000)

def test_rk4_is_fourth_order():
    f = lambda s, p=None: np.array([-s[0], 0.0, 0.0])
    def err(h):
        s = np.array([1.0, 0, 0]); n = int(round(1.0 / h))
        for _ in range(n):
            k1 = f(s); k2 = f(s + .5 * h * k1); k3 = f(s + .5 * h * k2); k4 = f(s + h * k3); s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return abs(s[0] - math.exp(-1))
    assert 14 < err(0.1) / err(0.05) < 18

def test_cylindrical_form_is_exact():
    for s in ORB[::15]:
        (rd, pd), (rc, pc) = M.cylindrical_rates(s)
        assert abs(rd - rc) < 1e-10 and abs(pd - pc) < 1e-10          # dr/dt = (z-b) r, dphi/dt = d

def test_axisymmetric_reduction_for_f_zero():
    p0 = dict(M.STANDARD, f=0.0); s = np.array([0.1, 0, 0.0])
    for _ in range(4000): s = M.rk4_step(s, 0.0045, p0)
    red = M.reduced_orbit(1, 3999, 0.0045, p0, (0.1, 0.0))[0]
    assert np.abs(np.array([math.hypot(s[0], s[1]), s[2]]) - red).max() < 1e-6

def test_radius_never_reaches_the_axis():
    assert np.hypot(ORB[:, 0], ORB[:, 1]).min() > 1e-3                # r > 0 stays > 0 (multiplicative radial law)

def test_fixed_points_on_the_axis_with_the_stated_eigenvalues():
    fps = M.fixed_points(); assert len(fps) == 3
    for fp in fps:
        x, y, z = fp['point']; assert x == 0 and y == 0 and abs(M.rhs(fp['point'])).max() < 1e-9
        J = np.zeros((3, 3)); h = 1e-6
        for j in range(3):
            e = np.zeros(3); e[j] = h; J[:, j] = (M.rhs(np.array(fp['point']) + e) - M.rhs(np.array(fp['point']) - e)) / (2 * h)
        num = sorted(np.linalg.eigvals(J), key=lambda c: (c.real, c.imag)); st = sorted(fp['eigenvalues'], key=lambda c: (c.real, c.imag))
        assert np.allclose(num, st, atol=1e-5)

def test_orbit_is_bounded_and_chaotic():
    lo, hi = M.bounds(ORB); assert np.all(np.abs(lo) < 2) and np.all(np.abs(hi) < 2.5)
    assert M.lyapunov_max(steps=30000) > 0.03                          # measured 0.085

def test_long_time_mean_of_z_is_b():
    o = M.orbit(60000, 3000, 0.0045)              # ln r is bounded, so <d ln r/dt> = <z - b> = 0; measured 0.701 against b = 0.7
    assert abs(float(np.mean(o[:, 2])) - M.STANDARD['b']) < 0.02

def test_js_layout_slot_order_and_line_distances():
    pos, line = M.js_layout(ORB[:100], scale=2.0)
    assert np.allclose(pos[:3], [2 * ORB[0, 0], 2 * ORB[0, 2], 2 * ORB[0, 1]], atol=1e-5) and line[0] == 0 and abs(line[-1] - 0.99) < 1e-6

def test_module_contract():
    m = AizawaAttractorModule(); names = [e.name for e in m.formulary()]
    assert names == ['field', 'cylindrical', 'fixed_points', 'orbit', 'lyapunov', 'js_layout']
    for n in names:
        if n != 'lyapunov': assert 'result' in m.run(n, {})
    assert 'text' in m.viewer_data('cylindrical', {}, 'text')
