"""The documented sigma_rb map (oblique_sigma_rb.py): psi (16) in, sigma_rb (16) out; tilt/axis, sigma_self, strut-blindness, rectifier law, flow saddle.
Reproduces the numbers of ContextPlease/claude/scratchpad/2026-08-31_oblique-gear/oblique_gear_output.txt and Ainulindale wiki 123 Listing 1."""
import cmath
import math
import random

from ValaQuenta.modules.h_rb_hat import oblique_sigma_rb as O


def rand_psi(seed, scale=1.0):
    r = random.Random(seed)
    return [complex(r.gauss(0, scale), r.gauss(0, scale)) for _ in range(16)]


PSI = rand_psi(20260831)


def test_t1_conjugate_pairing_and_documented_values():
    t, a, s = O.tilt_axis(PSI)
    assert max(abs(s[k ^ 4] - s[k].conjugate()) for k in range(16)) < 1e-12
    assert abs(t[0] - -0.4418) < 5e-5 and abs(t[3] - 2.1424) < 5e-5 and abs(a[2] - 2.3840) < 5e-5   # oblique_gear_output.txt


def test_t2_global_phase_is_a_gauge():
    t, a, _ = O.tilt_axis(PSI)
    t2, a2, _ = O.tilt_axis([cmath.exp(0.9137j) * z for z in PSI])
    assert max(abs(x - y) for x, y in zip(t + a, t2 + a2)) < 1e-12


def test_t3_gear_rotation_axis_invariant_tilt_driven():
    t, a, _ = O.tilt_axis(PSI)
    j, jj = O.REP[2], 2
    for th in (0.2, 0.7, 1.3, 2.1, 3.0):
        tr, ar, _ = O.tilt_axis(O.rot_pair(PSI, j, th))
        d2 = abs(PSI[j]) ** 2 - abs(PSI[j ^ 4]) ** 2
        assert abs(ar[jj] - a[jj]) < 1e-12
        assert abs(tr[jj] - (math.cos(2 * th) * t[jj] + 0.5 * math.sin(2 * th) * d2)) < 1e-12


def test_t4_sigma_self_is_half_plus_sum_tilt_over_energy():
    t, _, _ = O.tilt_axis(PSI)
    ss, red, blue = O.sigma_self(PSI)
    assert abs(ss - (0.5 + sum(t) / (red + blue))) < 1e-12 and abs(ss - 0.564721815) < 1e-8


def test_t6_balance_zeroes_tilt_keeps_axis():
    base = rand_psi(7)
    a0 = math.hypot(*O.tilt_axis(base)[1])
    b = O.balanced(base)
    assert abs(sum(O.tilt_axis(b)[0])) < 1e-12 and abs(math.hypot(*O.tilt_axis(b)[1]) - a0) / a0 < 1e-9
    assert abs(O.sigma_self(b)[0] - 0.5) < 1e-12


def test_strut_blindness_and_the_onset_residual():
    D = O.onset_residual()
    assert abs(D - 0.000707357533) < 1e-12
    r = random.Random(0)
    for _ in range(3):
        tl = [r.uniform(-0.3, 0.3) for _ in range(8)]
        m = sum(tl) / 8
        tl = [x + D - m for x in tl]
        assert abs(O.sigma_self(O.embed_tilt(tl))[0] - (0.5 + D)) < 1e-12


def test_rectifier_law_slope():
    r = random.Random(1)
    u = [r.gauss(0, 1) for _ in range(8)]
    m = sum(u) / 8
    u = [x - m for x in u]
    n = math.sqrt(sum(x * x for x in u))
    u = [x / n for x in u]
    D = O.onset_residual()
    lams = [10 ** (2 + 3 * i / 12) for i in range(13)]
    dev = []
    for lam in lams:
        t = [D + lam * x for x in u]
        a = [math.copysign(math.sqrt(abs(x)), x) for x in t]
        b = [math.sqrt(abs(x)) for x in t]
        red = sum(abs(p + q) ** 2 for p, q in zip(a, b)) / 2
        blue = sum(abs(p - q) ** 2 for p, q in zip(a, b)) / 2
        assert abs(red / (red + blue) - O.rectifier_sigma_self(t)) < 1e-9
        dev.append(red / (red + blue) - 0.5)
    sl = (math.log(dev[-1]) - math.log(dev[0])) / (math.log(lams[-1]) - math.log(lams[0]))
    assert abs(sl - -1.0) < 0.02


def test_a_lone_component_is_invisible_and_sits_at_the_critical_line():
    for k in range(16):
        psi = [0.0] * 16
        psi[k] = 1.0
        assert max(abs(z) for z in O.sigma_rb_map(psi)) == 0.0 and abs(O.sigma_self(psi)[0] - 0.5) < 1e-15


def test_flow_saddle_growth_rate_is_about_six():
    def drive(q):
        return O.tilt_axis(q)[0]

    def step(p, g):
        t0, h = drive(p), list(p)
        for k in O.REP:
            h = O.rot_pair(h, k, 0.5 * g * t0[O.REP.index(k)])
        t1, out = drive(h), list(p)
        for k in O.REP:
            out = O.rot_pair(out, k, g * t1[O.REP.index(k)])
        return out
    p = O.balanced(rand_psi(7))
    r = random.Random(5)
    p = [z + 1e-9 * complex(r.gauss(0, 1), r.gauss(0, 1)) for z in p]
    g, hist = 0.0125, []
    for _ in range(60):
        hist.append(max(abs(x) for x in drive(p)))
        p = step(p, g)
    lam = (math.log(hist[40]) - math.log(hist[10])) / (30 * g)
    assert 5.5 < lam < 6.7                                                        # ANOMALY_CHASE.md: 6.1 (midpoint)
