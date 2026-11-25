"""Tests for the zeta pathway engine, ValaQuenta.modules.zeta_uns_path (v1.0, 2026-11-24).  The 25,000-zero tests need RiemannHypothesisProof/data/zeros_25000_hp.tsv and skip without it."""
import math, os, sys
import numpy as np
import pytest
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, ROOT)
from ValaQuenta.modules.zeta_uns_path import maths as M
from ValaQuenta.modules.zeta_uns_path.tools import ZetaUNSPathModule
ZF = os.path.join(ROOT, 'RiemannHypothesisProof', 'data', 'zeros_25000_hp.tsv')
need_zeros = pytest.mark.skipif(not os.path.exists(ZF), reason='zero table not present')
def zeros():
    return np.array([float(l.split()[1]) for l in open(ZF) if l[0].isdigit()])

def test_theta_matches_mpmath():
    from mpmath import mp, siegeltheta, mpf; mp.dps = 20
    for t in (10., 50., 300., 5000.): assert abs(float(M.theta(t)) - float(siegeltheta(mpf(t)))) < 1e-8

def test_theta_prime_is_the_derivative():
    for t in (20., 200., 2000.): assert abs(float(M.theta_prime(t)) - (float(M.theta(t + 1e-5)) - float(M.theta(t - 1e-5))) / 2e-5) < 1e-6

@pytest.mark.parametrize('t,tol', [(100., 5e-3), (500., 5e-4), (2000., 3e-4), (10000., 2e-5)])
def test_riemann_siegel_Z_against_mpmath(t, tol):
    assert abs(float(M.Z_rs(t)[0]) - M.Z_exact(t)) < tol

def test_Z_changes_sign_at_each_of_the_first_30_zeros():
    g = M.zeros_mp(30)
    for x in g:
        assert abs(float(M.Z_rs(x)[0])) < 0.02                         # one-term R-S error is ~1e-2 near t = 25 (measured max 0.0103 over the first 30 zeros)
        assert float(M.Z_rs(x - 0.05)[0]) * float(M.Z_rs(x + 0.05)[0]) < 0

def test_flat_point_turns_at_minus_theta_prime():
    t = np.linspace(30, 60, 4000); z = M.zeta_line(t); Z = M.Z_rs(t); ph = np.unwrap(np.angle(z)); d = np.gradient(ph, t)
    away = np.abs(Z) > 0.6; assert away.sum() > 500 and np.abs(d[away] - M.rotation_rate(t)[away]).max() < 1e-3

def test_phase_sampling_is_monotone_sixteen_per_spacing():
    for jit in (False, True):
        ts = M.sample_by_phase(10.0, 40, 16, jitter=jit); assert np.all(np.diff(ts) > 0) and abs(np.mean(np.diff(M.theta(ts))) - math.pi / 16) <= (math.pi / 16) / (len(ts) - 1) + 1e-9      # jitter shifts the mean step by at most one step / n
    g = M.zeros_mp(30); ts = M.sample_by_phase(10.0, 40, 16, jitter=True)
    cnt = [int(np.sum((ts >= g[i]) & (ts < g[i + 1]))) for i in range(len(g) - 1)]; assert 14 <= np.mean(cnt) <= 18

def test_jitter_removes_the_angle_lattice():
    t0 = M.sample_by_phase(10.0, 400, 16, jitter=False); t1 = M.sample_by_phase(10.0, 400, 16, jitter=True)
    a0 = np.unique(np.round(np.mod(-M.theta(t0), math.pi), 6)); a1 = np.unique(np.round(np.mod(-M.theta(t1), math.pi), 6))
    assert len(a0) <= 20 and len(a1) > 1000

def test_sphere_and_cylinder_charts():
    assert np.allclose(M.sphere_point(0j), [0, 0, -1]) and abs(np.linalg.norm(M.sphere_point(3 - 4j)) - 1) < 1e-14
    rho, phi, h = M.uns_cylinder(np.array([1e-3 + 0j, 1 + 0j, 10 + 0j]), [1., 2., 3.]); assert np.allclose(rho, [0, 3, 4]) and h.tolist() == [1., 2., 3.]

@need_zeros
def test_driver_is_the_sum_of_zero_poles_away_from_zeros():
    g = zeros(); tt = np.linspace(30, 300, 400); far = np.array([np.min(np.abs(g - x)) > 0.8 for x in tt])
    D = M.driver(tt); R = (D - M.driver_from_zeros(tt, g))[far]
    assert np.std(D[far]) > 0.3 and np.std(R) < 0.02                  # measured 0.573 -> 0.007; a constant ~0.75 remains

@need_zeros
def test_zero_spectrum_spikes_at_primes_and_prime_powers():
    g = zeros(); xs = np.linspace(0.3, 5.0, 8000); S = np.array([np.sum(np.cos(g * x)) for x in xs]) / len(g); bg = np.median(np.abs(S))
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        j = int(np.argmin(np.abs(xs - math.log(p)))); assert np.abs(S[max(0, j - 3):j + 4]).max() > 15 * bg
    for p, k in ((2, 2), (2, 3), (3, 2), (5, 2)):
        j = int(np.argmin(np.abs(xs - k * math.log(p)))); assert np.abs(S[max(0, j - 3):j + 4]).max() > 15 * bg

def test_euler_steps_are_prime_steps():
    P = M.primes_upto(2000)[20:]; t = 14.1347; cum, steps = M.euler_path(t, P); z = P ** (-0.5 - 1j * t)
    assert np.abs(steps - z).max() < 0.02 and np.all(np.abs(np.abs(steps) - P ** -0.5) < 0.5 * P ** -1.0 * 1.2)

def test_prime_resonance_heights():
    tk = M.prime_resonance_times(2, 100.0); assert np.allclose(np.diff(tk), 2 * math.pi / math.log(2)) and np.all(np.abs(np.mod(tk * math.log(2) + 1e-9, 2 * math.pi)) < 1e-6)

def test_pseudo_cardioid_decomposition_and_no_cusp():
    for tv in (200., 1000., 5000., 20000.):
        S, mirror, R = M.cardioid_parts(tv); assert abs(R) <= (tv / (2 * math.pi)) ** -0.25 * 1.0 + 1e-9
    th = M.theta(np.linspace(200, 400, 2000)); c1 = 1 + np.exp(-2j * th); assert c1.real.min() > -1e-9      # n = 1 alone: a circle through 0 that never enters Re < 0
    for x in M.zeros_mp(20): assert abs((float(M.Z_rs(x + 1e-4)[0]) - float(M.Z_rs(x - 1e-4)[0])) / 2e-4) > 0.3     # speed at a zero is not 0: measured min 0.62 over 1,500 zeros

@need_zeros
def test_mean_value_one_and_re_negative_share_grows_slowly():
    ts = M.sample_by_phase(10.0, 25000, 16, jitter=True); z = M.zeta_line(ts); dt = np.gradient(ts); sh = []
    for nz in (100, 25000):
        k = nz * 16 + 1; w = dt[:k] / dt[:k].sum(); assert abs(complex(np.sum(z[:k] * w)) - 1) < 0.01; sh.append(M.re_negative_share(z[:k], dt[:k]))
    assert 0.15 < sh[0] < 0.21 and 0.22 < sh[1] < 0.26 and sh[1] > sh[0]          # measured 0.174 -> 0.240

def test_module_contract():
    m = ZetaUNSPathModule(); names = [e.name for e in m.formulary()]
    assert names == ['theta', 'hardy_z', 'pathway', 'driver', 'prime_resonance', 'euler_path', 'spectrum_ticks']
    for n in names: assert 'result' in m.run(n, {})
