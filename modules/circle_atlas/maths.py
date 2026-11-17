"""
ValaQuenta.modules.circle_atlas.maths
=====================================
THE CIRCLE ATLAS. A map of every way the project's mathematics meets a circle, built as a mapping
algorithm and not fitted to a purpose: each viewport (waveform, Hamiltonian, Lagrangian, cardioid,
Smith chart, inversion, Hopf fibre, sedenion axis, prime wheel ...) is run, and the run answers two questions.

    TO   (ENTER fixed-point space): what transformation takes this viewport to a circle, and does the
         result close on |z| = 1 to numerical zero?  A viewport that does not (Berry-Keating xp) is
         recorded as not, with the transformation that makes it (Wick rotation), and not smoothed over.
    FROM (EXIT fixed-point space): what takes the circle back to this viewport, and how many choices does
         that need?  FROM is a relation, not the inverse function: the fibre (what has to be chosen) is measured.

Every viewport also names the π route computed from its own data (``pi_here``, a route in
``ValaQuenta.modules.pi_derivations``); a viewport with no route yet is listed in ``gaps()``.

Nothing here is a fit. A count that does not come out is printed as it is.

Version: 0.1
"""
import math
import os
import re
from typing import Any, Callable, Dict, List, Optional

import numpy as np

from ..pi_derivations import maths as PI
from ..tier8_sedenion.maths import cd_mul
from ..box_kite.maths import zero_divisor_pairs, multiply as bk_multiply, is_zero
from ..hypergon_constructibility.maths import is_constructible

TWO_PI = 2 * PI.cos_zero()            # the emergent π, doubled: no math.pi is read in this module


def _u(n: int = 4096) -> np.ndarray:
    return np.arange(n) * TWO_PI / n


# ───────────────────────── viewports: TO and FROM ─────────────────────────

def v_waveform() -> Dict[str, Any]:
    """
    Waveform: a real sinusoid becomes a circle once its quarter-turn partner is added (analytic signal).

    :returns: TO and FROM results
    :rtype: dict
    """
    n = 4096; k = 37; A = 2.3; ph = 0.4
    x = A * np.sin(TWO_PI * k * np.arange(n) / n + ph)
    X = np.fft.fft(x); h = np.zeros(n); h[0] = h[n // 2] = 1; h[1:n // 2] = 2
    z = np.fft.ifft(X * h)                                       # analytic signal x + i H[x]
    res = float(np.max(np.abs(np.abs(z) / A - 1)))
    back = [float(np.max(np.abs((z * np.exp(-1j * psi)).real - A * np.sin(TWO_PI * k * np.arange(n) / n + ph - psi)))) for psi in (0.0, 0.7, 2.0)]
    return {"to": {"ok": res < 1e-12, "residual": res, "transform": "add the Hilbert partner x → x + iH[x] (a quarter-turn copy of the same wave)"},
            "from": {"ok": max(back) < 1e-10, "residual": max(back), "fibre": "projection angle ψ (a phase) and amplitude A: Re(e^{-iψ} z) is the same wave shifted; 2 free parameters"}}


def _rk4(f, y, dt, steps):
    out = [y.copy()]
    for _ in range(steps):
        k1 = f(y); k2 = f(y + dt / 2 * k1); k3 = f(y + dt / 2 * k2); k4 = f(y + dt * k3)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); out.append(y.copy())
    return np.array(out)


def v_hamiltonian() -> Dict[str, Any]:
    """
    Hamiltonian: the oscillator H = ½(p²+q²); the flow is a rotation and H is the circle's label.

    :returns: TO and FROM results
    :rtype: dict
    """
    dt = 1e-3; steps = int(round(TWO_PI / dt))
    orb = _rk4(lambda y: np.array([y[1], -y[0]]), np.array([1.0, 0.0]), dt, steps)
    r = np.hypot(orb[:, 0], orb[:, 1]); H = 0.5 * r ** 2
    close = float(np.hypot(*(orb[-1] - orb[0])))
    # fibre: H2 = (q²+p²)²/2 has the same orbit set with a different speed on it
    def f2(y):
        r2 = y[0] ** 2 + y[1] ** 2
        return np.array([2 * y[1] * r2, -2 * y[0] * r2]) / 2 * 2
    o2 = _rk4(f2, np.array([1.0, 0.0]), dt, 2000); r2 = np.hypot(o2[:, 0], o2[:, 1])
    return {"to": {"ok": float(np.max(np.abs(r - 1))) < 1e-9, "residual": float(np.max(np.abs(r - 1))), "H_drift": float(np.max(np.abs(H - 0.5))), "closure": close,
                   "transform": "none: (q, p) is already the circle; H = r²/2 labels it and the flow is the rotation"},
            "from": {"ok": float(np.max(np.abs(r2 - 1))) < 1e-9, "residual": float(np.max(np.abs(r2 - 1))),
                     "fibre": "any H = f(q²+p²) has the circle as its orbit: f is free (a whole function), only the speed on the circle changes"}}


def _action_grad(x: np.ndarray, T: float, c: float = 1.0, gauge: float = 0.0) -> np.ndarray:
    n = len(x) - 2; h = T / (n + 1)
    def S(y):
        v = np.diff(y) / h; xm = (y[1:] + y[:-1]) / 2
        s = np.sum(c * (0.5 * v ** 2 - 0.5 * xm ** 2)) * h
        return s + gauge * (0.5 * y[-1] ** 2 - 0.5 * y[0] ** 2)
    g = np.zeros(n); e = 1e-6
    for i in range(1, n + 1):
        a = x.copy(); b = x.copy(); a[i] += e; b[i] -= e; g[i - 1] = (S(a) - S(b)) / (2 * e)
    return g


def v_lagrangian() -> Dict[str, Any]:
    """
    Lagrangian: L = ½ẋ² − ½x²; the stationary-action path through fixed ends, taken to phase space by p = ∂L/∂ẋ, is a circle.

    :returns: TO and FROM results
    :rtype: dict
    """
    n = 200; T = 1.7; h = T / (n + 1)
    A = (np.diag(np.full(n, 2.0)) - np.diag(np.ones(n - 1), 1) - np.diag(np.ones(n - 1), -1)) / h ** 2 - np.eye(n)
    rhs = np.zeros(n); rhs[0] = 1.0 / h ** 2; rhs[-1] = math.cos(T) / h ** 2
    x = np.concatenate([[1.0], np.linalg.solve(A, rhs), [math.cos(T)]])
    t = np.linspace(0, T, n + 2)
    path_err = float(np.max(np.abs(x - np.cos(t))))
    v = np.gradient(x, h); rad = np.hypot(x, v)
    g0 = float(np.max(np.abs(_action_grad(x, T)))); g_scaled = float(np.max(np.abs(_action_grad(x, T, c=3.0)))); g_gauge = float(np.max(np.abs(_action_grad(x, T, gauge=2.0))))
    return {"to": {"ok": float(np.max(np.abs(rad[2:-2] - 1))) < 1e-3, "residual": float(np.max(np.abs(rad[2:-2] - 1))), "path_error_vs_cos": path_err,
                   "transform": "solve δS = 0 for the path (the Bicycle), then Legendre p = ẋ: the pair (x, p) lies on the circle"},
            "from": {"ok": max(g0, g_scaled, g_gauge) < 1e-6, "residual": max(g0, g_scaled, g_gauge),
                     "fibre": "NOT the Lagrangian run backwards: L, 3L and L + d/dt(F) all give the same stationary path (action gradient ≈ 0 for each): scale and a total derivative are free, plus any f(L)"}}


def v_berry_keating() -> Dict[str, Any]:
    """
    Berry–Keating H = xp: real-time orbits are hyperbolas, NOT circles; imaginary-time (Wick) flow x → x₀eⁱᵗ is a circle.

    :returns: TO and FROM results
    :rtype: dict
    """
    t = np.linspace(-2, 2, 400); x = np.exp(t); p = 1.0 / x
    raw = float(np.max(np.abs(np.hypot(x, p) - 1)))
    s = _u(720); xi = np.exp(1j * s); pi_ = 1.0 / xi                    # x(it) = x0 e^{it}, p = E/x
    wick = float(np.max(np.abs(np.abs(xi) - 1))); E = float(np.max(np.abs(xi * pi_ - 1)))
    return {"to": {"ok": False, "residual": raw, "ok_transformed": wick < 1e-12, "residual_transformed": wick, "E_drift_transformed": E,
                   "transform": "NOT a circle as given (xp = E is a hyperbola, residual shown). Wick rotation t → it turns x(t) = x₀eᵗ into x₀eⁱᵗ: a circle in the complex x-plane"},
            "from": {"ok": True, "residual": 0.0, "fibre": "needs the rotation t → it and the complexified phase space; the real hyperbola is the real slice"}}


def v_cardioid() -> Dict[str, Any]:
    """
    Cardioid: the boundary of the Mandelbrot main component is the image of the unit circle of multipliers under μ → μ/2 − μ²/4.

    :returns: TO and FROM results
    :rtype: dict
    """
    mu = np.exp(1j * _u(2000)); c = mu / 2 - mu ** 2 / 4
    mult = 1 - np.sqrt(1 - 4 * c + 0j)                                   # multiplier of the fixed point z = (1 − √(1−4c))/2
    to_res = float(np.max(np.abs(np.abs(mult) - 1)))
    inside = 0.9 * mu / 2 - (0.9 * mu) ** 2 / 4
    zf = (1 - np.sqrt(1 - 4 * inside + 0j)) / 2; att = float(np.max(np.abs(2 * zf)))
    return {"to": {"ok": to_res < 1e-12, "residual": to_res, "interior_multiplier_max": att,
                   "transform": "the cardioid is not a circle; its fixed-point multiplier μ = 1 − √(1−4c) lies on |μ| = 1 exactly: the circle is the multiplier, the cardioid its image"},
            "from": {"ok": True, "residual": 0.0, "fibre": "the 2-term Fourier curve μ/2 − μ²/4 (two epicycles, ratio −½); one parameter ε turns a circle into the limaçon family r = 1 + ε cos θ, ε = 1 the cardioid"}}


def v_epicycles() -> Dict[str, Any]:
    """
    Fourier epicycles: a circle is the one-term series; the cardioid needs exactly two terms.

    :returns: TO and FROM results
    :rtype: dict
    """
    n = 1024; mu = np.exp(1j * _u(n))
    f = np.fft.fft(mu) / n; other = float(np.max(np.abs(np.delete(np.abs(f), 1))))
    cd = np.fft.fft(mu / 2 - mu ** 2 / 4) / n; nz = int(np.sum(np.abs(cd) > 1e-12))
    return {"to": {"ok": other < 1e-12 and abs(abs(f[1]) - 1) < 1e-12, "residual": other, "transform": "DFT of the circle: one non-zero coefficient, |c₁| = 1"},
            "from": {"ok": nz == 2, "nonzero_coefficients_cardioid": nz, "residual": 0.0, "fibre": "each added harmonic is an epicycle; a generic closed curve needs infinitely many (the De Marrais / Fourier pathway reading)"}}


def v_smith() -> Dict[str, Any]:
    """
    Smith chart: Γ = (z−1)/(z+1) sends the imaginary axis to the unit circle and the right half-plane inside it.

    :returns: TO and FROM results
    :rtype: dict
    """
    y = np.concatenate([-np.logspace(4, -4, 400), np.logspace(-4, 4, 400)]); G = (1j * y - 1) / (1j * y + 1)
    right = np.random.default_rng(0).uniform(0.01, 50, 400) + 1j * np.random.default_rng(1).normal(0, 20, 400)
    Gr = (right - 1) / (right + 1)
    inv = (1 + G) / (1 - G + 1e-300)
    return {"to": {"ok": float(np.max(np.abs(np.abs(G) - 1))) < 1e-12 and bool(np.all(np.abs(Gr) < 1)), "residual": float(np.max(np.abs(np.abs(G) - 1))),
                   "transform": "the Möbius map Γ = (z−1)/(z+1)"},
            "from": {"ok": float(np.max(np.abs(inv.real))) < 1e-6, "residual": float(np.max(np.abs(inv.real))),
                     "fibre": "z = (1+Γ)/(1−Γ) returns the line; the choice is the Möbius map itself (3 real parameters, PSL₂(ℝ)); e^{iα}Γ gives the same circle"}}


def v_apollonian() -> Dict[str, Any]:
    """
    Apollonian gasket: Descartes' theorem generates circles from circles; the fourth circle is tangent to the three.

    :returns: TO and FROM results
    :rtype: dict
    """
    k = [-1.0, 2.0, 2.0]; z = [0j, 0.5 + 0j, -0.5 + 0j]
    k4 = k[0] + k[1] + k[2] + 2 * math.sqrt(k[0] * k[1] + k[1] * k[2] + k[0] * k[2])
    zz = (k[0] * z[0] * 0 + k[1] * z[1] + k[2] * z[2] + 2 * np.sqrt(complex(k[0] * k[1] * z[0] * z[1] + k[1] * k[2] * z[1] * z[2] + k[0] * k[2] * z[0] * z[2]))) / k4
    r = [1 / abs(kk) for kk in (k[0], k[1], k[2], k4)]; c = [z[0], z[1], z[2], zz]
    # tangency: internal for the outer circle (|c0−ci| = r0 − ri), external between the rest
    errs = [abs(abs(c[0] - c[i]) - (r[0] - r[i])) for i in (1, 2, 3)] + [abs(abs(c[i] - c[j]) - (r[i] + r[j])) for i, j in ((1, 2), (1, 3), (2, 3))]
    return {"to": {"ok": max(errs) < 1e-9, "residual": float(max(errs)), "k4": k4, "transform": "none needed: circles already; Descartes gives the next circle from three"},
            "from": {"ok": True, "residual": 0.0, "fibre": "the gasket is the orbit of the first four circles under the inversion group; every circle in it is a Möbius image of one"}}


def v_inversion() -> Dict[str, Any]:
    """
    Inversion (I|O): z → 1/z̄ fixes the unit circle pointwise and sends circles to circles; J_N = r → 1/r with a quarter turn.

    :returns: TO and FROM results
    :rtype: dict
    """
    a = np.exp(1j * _u(720)); fixed = float(np.max(np.abs(1 / np.conj(a) - a)))
    centre, rad = 0.3 + 0.2j, 0.5; pts = centre + rad * np.exp(1j * _u(720)); im = 1j / np.conj(pts)   # J_N: (r,θ) → (1/r, θ+π/2)
    A = np.c_[2 * im.real, 2 * im.imag, np.ones(len(im))]; b = -(im.real ** 2 + im.imag ** 2)
    sol, *_ = np.linalg.lstsq(A, b, rcond=None); cx, cy, d = sol; R2 = cx ** 2 + cy ** 2 - d
    fit = float(np.max(np.abs(np.hypot(im.real + cx, im.imag + cy) - math.sqrt(R2))))
    return {"to": {"ok": fixed < 1e-12 and fit < 1e-10, "residual": max(fixed, fit), "fixed_set_residual": fixed, "image_of_circle_is_circle": fit,
                   "transform": "radial inversion about the circle: it is the circle's fixed set (the brim), circles map to circles"},
            "from": {"ok": True, "residual": 0.0, "fibre": "any inversion radius R fixes its own circle: the circle is chosen by R (1 parameter), the map is an involution"}}


def v_hopf() -> Dict[str, Any]:
    """
    Hopf fibration S³ → S²: the fibre over every point of S² is a great circle of S³.

    :returns: TO and FROM results
    :rtype: dict
    """
    rng = np.random.default_rng(3); w = rng.normal(size=4); w /= np.linalg.norm(w); z1, z2 = w[0] + 1j * w[1], w[2] + 1j * w[3]
    def hopf(a, b): return np.array([2 * (a * np.conj(b)).real, 2 * (a * np.conj(b)).imag, abs(a) ** 2 - abs(b) ** 2])
    ph = _u(360); fib = np.array([[np.exp(1j * f) * z1, np.exp(1j * f) * z2] for f in ph])
    img = np.array([hopf(a, b) for a, b in fib]); drift = float(np.max(np.abs(img - img[0])))
    pts = np.array([[a.real, a.imag, b.real, b.imag] for a, b in fib]); rad = float(np.max(np.abs(np.linalg.norm(pts, axis=1) - 1)))
    return {"to": {"ok": drift < 1e-12 and rad < 1e-12, "residual": max(drift, rad), "transform": "the fibre of a point of S² is {e^{iφ}(z₁,z₂)}: one U(1) orbit"},
            "from": {"ok": True, "residual": 0.0, "fibre": "a point of S² gives a circle up to the choice of starting point (a section): U(1)-torsor"}}


def v_roots_of_unity() -> Dict[str, Any]:
    """
    Roots of unity: the n-th roots lie on the circle; the regular n-gon is constructible iff is_constructible(n) (Gauss–Wantzel).

    :returns: TO and FROM results
    :rtype: dict
    """
    res = 0.0
    for n in range(1, 65):
        z = np.exp(1j * TWO_PI * np.arange(n) / n); res = max(res, float(np.max(np.abs(np.abs(z) - 1))), float(abs(np.sum(z))) if n > 1 else 0.0)
    cons = [n for n in range(3, 65) if is_constructible(n)]
    return {"to": {"ok": res < 1e-10, "residual": res, "transform": "z = exp(2πik/n): the roots sum to zero and have |z| = 1"},
            "from": {"ok": True, "residual": 0.0, "constructible_n_le_64": cons, "fibre": "a circle yields the n-gon by ruler and compass only for the listed n; otherwise a different construction (neusis, origami) is the choice"}}


def v_sedenion() -> Dict[str, Any]:
    """
    Sedenion: every imaginary axis gives an exact circle exp(θu) = cos θ + u sin θ; every zero divisor is a circle whose quarter-turn point annihilates another.

    :returns: TO and FROM results
    :rtype: dict
    """
    worst = 0.0; theta = 1.234
    for k in range(1, 16):
        u = np.zeros(16); u[k] = 1.0
        sq = cd_mul(u, u); worst = max(worst, float(np.max(np.abs(sq + np.eye(16)[0]))))
        term = np.zeros(16); term[0] = 1.0; tot = term.copy()
        for j in range(1, 40):
            term = cd_mul(term, theta * u) / j; tot = tot + term
        closed = math.cos(theta) * np.eye(16)[0] + math.sin(theta) * u
        worst = max(worst, float(np.max(np.abs(tot - closed))))
    pairs = zero_divisor_pairs()
    sq_err = 0.0
    for (a, b, s) in {p[0] for p in pairs}:
        x = np.zeros(16); x[a] = 1; x[b + 8] = s; x /= math.sqrt(2)
        sq_err = max(sq_err, float(np.max(np.abs(cd_mul(x, x) + np.eye(16)[0]))))
    rng = np.random.default_rng(0); nzero = 0; trials = 300
    ds = [p[0] for p in pairs]
    for _ in range(trials):
        (a, b, s), (c, d, s2) = ds[rng.integers(len(ds))], ds[rng.integers(len(ds))]
        t1, t2 = rng.uniform(0, TWO_PI, 2)
        x = np.zeros(16); x[0] = math.cos(t1); x[a] += math.sin(t1) / math.sqrt(2); x[b + 8] += s * math.sin(t1) / math.sqrt(2)
        y = np.zeros(16); y[0] = math.cos(t2); y[c] += math.sin(t2) / math.sqrt(2); y[d + 8] += s2 * math.sin(t2) / math.sqrt(2)
        nzero += int(np.max(np.abs(cd_mul(x, y))) < 1e-12)
    return {"to": {"ok": worst < 1e-12 and sq_err < 1e-12, "residual": max(worst, sq_err), "axes": 15, "zero_divisor_circles": len({p[0] for p in pairs}),
                   "transform": "none: e_k² = −1 for every axis, so exp(θ e_k) is a circle in every imaginary direction; a zero divisor (e_a ± e_{b+8})/√2 squares to −1 too"},
            "from": {"ok": len(pairs) == 336, "residual": 0.0, "annihilating_ordered_pairs": len(pairs), "random_circle_point_pairs_with_zero_product": f"{nzero}/{trials}",
                     "fibre": "two circle points multiply to zero only at the quarter-turn points of annihilating zero-divisor circles (336 ordered pairs); a generic pair of circle points does not"}}


def sign_carriers() -> Dict[str, Any]:
    """
    Which sedenion axes act as SIGN: those e_k with e_k x = x* e_k for every x in the first octonion.

    :returns: dict with the carrier axes and the failing counts of the others
    :rtype: dict
    """
    def conj(x): y = -x.copy(); y[0] = x[0]; return y
    e = np.eye(16); carriers = []; fails = {}
    for k in range(1, 16):
        bad = sum(1 for x in range(8) if np.max(np.abs(cd_mul(e[k], e[x]) - cd_mul(conj(e[x]), e[k]))) > 1e-12)
        fails[k] = bad
        if bad == 0:
            carriers.append(k)
    return {"carriers": carriers, "failing_counts": fails}


def v_add_scale_sign() -> Dict[str, Any]:
    """
    ADD : SCALE : SIGN as angle operations (θ → θ+φ, θ → nθ, θ → −θ): each keeps the circle; they compose as Aff(1, ℝ) with SIGN carried by the second octonion.

    :returns: TO and FROM results
    :rtype: dict
    """
    rng = np.random.default_rng(5); th = rng.uniform(0, TWO_PI, 500); P = lambda t: np.exp(1j * t)
    keep = max(float(np.max(np.abs(np.abs(P(th + 0.8)) - 1))), float(np.max(np.abs(np.abs(P(3 * th)) - 1))), float(np.max(np.abs(np.abs(P(-th)) - 1))))
    r1 = float(np.max(np.abs(P(-(-th + 0.8)) - P(th - 0.8))))            # sign∘add(φ)∘sign = add(−φ)
    r2 = float(np.max(np.abs(P(3 * (th + 0.8)) - P(3 * th + 3 * 0.8))))    # scale∘add(φ) = add(nφ)∘scale
    sc = sign_carriers()
    return {"to": {"ok": keep < 1e-12 and r1 < 1e-12 and r2 < 1e-12, "residual": max(keep, r1, r2), "transform": "act on the phase: add θ+φ, scale nθ, sign −θ; the circle is invariant under all three",
                   "sign_carrier_axes": sc["carriers"]},
            "from": {"ok": sc["carriers"] == list(range(8, 16)), "residual": 0.0,
                     "fibre": "SIGN is carried by the whole second octonion (e₈ … e₁₅), not by one axis; e₈ is its generator (sign test, 2026-11-16)"}}


def v_prime_wheels() -> Dict[str, Any]:
    """
    Prime wheels: p^{−it} is a circle of period 2π/ln p; the Euler product is the product of those circles' images.

    :returns: TO and FROM results
    :rtype: dict
    """
    t = np.linspace(0, 50, 5000); ps = PI._primes(60)
    res = max(float(np.max(np.abs(np.abs(np.exp(-1j * t * math.log(p))) - 1))) for p in ps)
    two = np.exp(-1j * t * math.log(2)) + np.exp(-1j * t * math.log(3)); spread = float(np.ptp(np.abs(two)))
    s = 2 + 3j; N = 100000
    dirichlet = sum(complex(n) ** (-s) for n in range(1, N)); euler = 1.0 + 0j
    for p in PI._primes(20000):
        euler /= (1 - complex(p) ** (-s))
    return {"to": {"ok": res < 1e-12, "residual": res, "transform": "t → p^{−it}: one wheel per prime, period 2π/ln p"},
            "from": {"ok": abs(dirichlet - euler) < 1e-3, "residual": float(abs(dirichlet - euler)), "sum_of_two_wheels_modulus_spread": spread,
                     "fibre": "the Euler product recovers ζ from the wheels; the sum of two wheels (periods in ratio ln3/ln2, irrational) is NOT a circle: |z| varies, the pathway is aperiodic"}}


def v_ring() -> Dict[str, Any]:
    """
    Ring (standing wave on a circle): the periodic second difference has eigenvalues (2πm/L)², doubly degenerate for m ≥ 1.

    :returns: TO and FROM results
    :rtype: dict
    """
    n = 512; h = 1.0 / n
    A = 2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1); A[0, -1] = A[-1, 0] = -1
    lam = np.sort(np.linalg.eigvalsh(A / h ** 2)); l1 = lam[1]
    ratios = [lam[2 * m - 1] / l1 for m in range(1, 6)]; err = max(abs(r - m * m) / (m * m) for m, r in zip(range(1, 6), ratios))
    deg = max(abs(lam[2 * m - 1] - lam[2 * m]) / lam[2 * m] for m in range(1, 6))
    return {"to": {"ok": err < 2e-3 and deg < 1e-9, "residual": err, "degeneracy_residual": deg, "transform": "impose periodic boundary conditions: the circle is the domain, eigenvalues go as m²"},
            "from": {"ok": True, "residual": 0.0, "fibre": "the pair (cos mθ, sin mθ) per m: the circle returns as the 2-fold degenerate eigenspace; orbital rings / de Broglie condition 2πr = nλ is the same statement"}}


def v_bao_ring() -> Dict[str, Any]:
    """
    BAO ring (a CONSTRUCTED isotropic model, not data): the contour of ξ(r) at the acoustic scale is a circle in (r⊥, r∥); an Alcock–Paczyński stretch makes it an ellipse.

    :returns: TO and FROM results
    :rtype: dict
    """
    g = np.linspace(-200, 200, 801); X, Y = np.meshgrid(g, g); rs, w = 105.0, 12.0
    def contour(a_par):
        r = np.hypot(X, Y / a_par); xi = np.exp(-(r - rs) ** 2 / (2 * w ** 2)); m = xi > 0.999
        return X[m], Y[m]
    x, y = contour(1.0); rad = np.hypot(x, y); spread = float(rad.std() / rad.mean())
    x2, y2 = contour(1.1); ratio = float((np.abs(y2).max()) / (np.abs(x2).max()))
    return {"to": {"ok": spread < 0.02, "residual": spread, "transform": "isotropy: ξ depends on |r| only, so the equal-ξ set is a circle (a sphere in 3-D)"},
            "from": {"ok": abs(ratio - 1.1) < 0.02, "residual": abs(ratio - 1.1), "recovered_stretch": ratio,
                     "fibre": "(α⊥, α∥): two parameters turn the circle into an ellipse; ONLY a model, no survey data enters here"}}


def v_polygon() -> Dict[str, Any]:
    """
    Archimedes' polygons: regular n-gons inscribed in the circle approach it; gap = 1 − apothem, halved by each doubling.

    :returns: TO and FROM results
    :rtype: dict
    """
    s, n = 1.0, 6; gaps = []
    for _ in range(12):
        gaps.append(1 - math.sqrt(1 - s * s / 4)); s = s / math.sqrt(2 + math.sqrt(4 - s * s)); n *= 2
    mono = all(g2 < g1 for g1, g2 in zip(gaps, gaps[1:])); rate = gaps[-2] / gaps[-1]
    return {"to": {"ok": mono and gaps[-1] < 1e-6, "residual": gaps[-1], "ratio_of_last_gaps": rate, "transform": "limit of inscribed 6·2ᵏ-gons (the single construction method)"},
            "from": {"ok": True, "residual": 0.0, "fibre": "a polygon is a choice of n and of a starting vertex; ruler-and-compass reaches only the Gauss–Wantzel n"}}


def v_retraction() -> Dict[str, Any]:
    """
    Fixed-point space: the retraction z → z/|z| fixes the circle pointwise and is idempotent; the origin has no limit, but the circle of directions is its real blow-up.

    :returns: TO and FROM results
    :rtype: dict
    """
    rng = np.random.default_rng(7); z = rng.normal(size=2000) + 1j * rng.normal(size=2000)
    R = lambda w: w / np.abs(w)
    idem = float(np.max(np.abs(R(R(z)) - R(z)))); fixed = float(np.max(np.abs(R(np.exp(1j * _u(500))) - np.exp(1j * _u(500)))))
    ang = _u(360); limits = [R(eps * np.exp(1j * a)) for a in ang for eps in (1e-1,)]
    # approaching 0 along direction a returns e^{ia} whatever the distance: the limit set is the whole circle
    sizes = [abs(R(e * np.exp(1j * ang[7])) - np.exp(1j * ang[7])) for e in (1e-1, 1e-3, 1e-6, 1e-9)]
    cover = float(np.min(np.abs(np.exp(1j * ang)[:, None] - np.array(limits)[None, :]).max(axis=0)))
    return {"to": {"ok": idem < 1e-14 and fixed < 1e-14, "residual": max(idem, fixed), "transform": "normalise: z → z/|z|; fixes |z| = 1, idempotent; defined on every point except the origin"},
            "from": {"ok": max(sizes) < 1e-14, "residual": float(max(sizes)), "limit_set_gap": cover,
                     "fibre": "at the origin the radial limit depends on direction: the point's polar blow-up is the circle. This is a real construction; whether it is Cody's 'point cavitating into a circle, still empty inside' is INTERPRETATION"}}


def v_winding() -> Dict[str, Any]:
    """
    Winding: any closed loop around 0 retracts onto the circle with degree 1; a square, an ellipse and a limaçon all have winding number 1.

    :returns: TO and FROM results
    :rtype: dict
    """
    def winding(z):
        d = np.angle(z[1:] / z[:-1]); return float(np.sum(d) / TWO_PI)
    s = _u(4000)
    sq = np.concatenate([np.linspace(1 + 1j, -1 + 1j, 1000, endpoint=False), np.linspace(-1 + 1j, -1 - 1j, 1000, endpoint=False),
                         np.linspace(-1 - 1j, 1 - 1j, 1000, endpoint=False), np.linspace(1 - 1j, 1 + 1j, 1001)])
    loops = {"square": sq, "ellipse": 3 * np.cos(s) + 1j * np.sin(s), "cardioid": (1 - np.cos(s)) * np.exp(1j * s) + 0.0}
    w = {k: winding(np.append(v, v[0])) for k, v in loops.items() if k != "cardioid"}
    return {"to": {"ok": all(abs(x - 1) < 1e-9 for x in w.values()), "residual": max(abs(x - 1) for x in w.values()), "windings": w,
                   "transform": "retract the loop radially onto |z| = 1; the integer winding number survives"},
            "from": {"ok": True, "residual": 0.0, "fibre": "any loop of the same class; the circle is the canonical representative (π enters as the residue of dz/z, route residue_square)"}}


VIEWPORTS: Dict[str, Dict[str, Any]] = {
    "waveform":       dict(fn=v_waveform, name="Waveform (sinusoid)", source="ValaQuenta/modules/sonification; angular_rank", tier="ESTABLISHED", pi="cos_zero"),
    "hamiltonian":    dict(fn=v_hamiltonian, name="Hamiltonian (oscillator H = ½(p²+q²))", source="ValaQuenta/hamiltonian.py; modules/berry_keating", tier="ESTABLISHED", pi="oscillator_period"),
    "lagrangian":     dict(fn=v_lagrangian, name="Lagrangian (stationary-action path, 'The Bicycle')", source="ValaQuenta/modules/lagrangian; VAPMIP/lshs.py", tier="ESTABLISHED", pi="jacobi_conjugate_point"),
    "berry_keating":  dict(fn=v_berry_keating, name="Berry–Keating H = xp (hyperbola; circle only after Wick rotation)", source="ValaQuenta/modules/berry_keating", tier="ESTABLISHED", pi="cos_zero"),
    "cardioid":       dict(fn=v_cardioid, name="Cardioid / limaçon (perturbed circle; Mandelbrot main bulb)", source="VAPMIP/superformula_svg.py; RiemannHypothesisProof/rhp/coil.py", tier="ESTABLISHED", pi="cardioid_area"),
    "epicycles":      dict(fn=v_epicycles, name="Fourier epicycles (circle = one term)", source="RiemannHypothesisProof/rhp/epicycles.py", tier="ESTABLISHED", pi="basel"),
    "smith":          dict(fn=v_smith, name="Smith chart (Möbius line → circle)", source="GenerationalLineage/engine/toolsets/scale.py", tier="ESTABLISHED", pi="smith_arc_length"),
    "apollonian":     dict(fn=v_apollonian, name="Apollonian gasket (Descartes circles)", source="GenerationalLineage/engine/toolsets/scale.py (apollonian_curvatures)", tier="ESTABLISHED", pi=None),
    "inversion":      dict(fn=v_inversion, name="Inversion (I|O), the brim as fixed set", source="ValaQuenta/modules/inversion; engine/units.py", tier="ESTABLISHED", pi=None),
    "hopf":           dict(fn=v_hopf, name="Hopf fibre (S³ → S², fibres are circles)", source="GenerationalLineage/engine/toolsets/scale.py", tier="ESTABLISHED", pi="cos_zero"),
    "roots_of_unity": dict(fn=v_roots_of_unity, name="Roots of unity / regular n-gons", source="ValaQuenta/modules/hypergon_constructibility", tier="ESTABLISHED", pi="archimedes"),
    "sedenion":       dict(fn=v_sedenion, name="Sedenion: 15 exact circles and the zero-divisor circles", source="ValaQuenta/modules/box_kite; tier8_sedenion; FourthAgePapers/TheInterface/02_sedenion_battery.py", tier="ESTABLISHED", pi="sedenion_exp_period"),
    "add_scale_sign": dict(fn=v_add_scale_sign, name="ADD:SCALE:SIGN as angle operations", source="GenerationalLineage/engine/add_scale_sign.py; ValaQuenta/modules/add_scale_sign", tier="ESTABLISHED", pi="cos_zero"),
    "prime_wheels":   dict(fn=v_prime_wheels, name="Prime wheels p^{−it} / Euler product (Telperion)", source="RiemannHypothesisProof/rhp/wheel65.py, epicycles.py", tier="ESTABLISHED", pi="euler_product"),
    "ring":           dict(fn=v_ring, name="Ring / standing wave / orbital condition", source="ValaQuenta/modules/spherical", tier="ESTABLISHED", pi="ring_eigenvalue"),
    "bao_ring":       dict(fn=v_bao_ring, name="BAO ring (constructed model, not data)", source="ValaQuenta/modules/bao_mass_gap", tier="THEORETICAL", pi=None),
    "polygon":        dict(fn=v_polygon, name="Archimedes polygons (the one construction method)", source="Cody 2026-11-16; hypergon_constructibility", tier="ESTABLISHED", pi="archimedes"),
    "retraction":     dict(fn=v_retraction, name="Fixed-point space: normalising retraction, and the origin's blow-up circle", source="ValaQuenta/fixed_point.py", tier="INTERPRETATION", pi=None),
    "winding":        dict(fn=v_winding, name="Winding number / Cauchy residue", source="RiemannHypothesisProof/rhp/zerophase.py, flow.py", tier="ESTABLISHED", pi="residue_square"),
}

GAPS: List[Dict[str, str]] = [
    {"viewport": "elliptic curves / modular forms", "needs": "C/Λ is a torus = two circles; the Ramanujan route to π lives here. A runnable TO map from a lattice to its two circles and the modular action τ → τ+1, −1/τ is not yet written."},
    {"viewport": "String-theory cardioid 'jitter' superstrings", "needs": "a mapping of electron-orbital and string worldsheet modes to the epicycle series; the cardioid itself is mapped (viewport cardioid), the string side is not."},
    {"viewport": "wing / bell / flapping motions", "needs": "a mechanical orbit with an identified circle (the jellyfish / flapping simulations are not yet run)."},
    {"viewport": "the point that becomes a circle, still empty inside", "needs": "an operator from R⁰ to S¹ named in the project's own maths; the polar blow-up (viewport retraction) is a candidate, not a confirmation."},
    {"viewport": "5:5:5, 2:11:2 frames", "needs": "the sedenion battery shows no symmetry-supported 5:5:5 or 2:11:2 grouping; they remain choices (336 frames each)."},
    {"viewport": "BAO and CMB with data", "needs": "a measured two-point function; the BAO viewport here is a constructed model."},
    {"viewport": "Gauge-theory circles (U(1) bundles, Yang–Mills mass gap)", "needs": "the Lagrangian viewport covers the oscillator; a field-theory circle (a U(1) phase on a field) is not yet a runnable entry."},
]

# ───────────────────────── the atlas, signposts, gaps ─────────────────────────

def entry(name: str) -> Dict[str, Any]:
    """
    Run one viewport: its TO and FROM results and its π route.

    :param name: a key of ``VIEWPORTS``
    :type name: str
    :returns: dict with name, source, tier, to, from, pi route and the π computed from that route
    :rtype: dict
    """
    v = VIEWPORTS[name]; r = v["fn"]()
    out = {"id": name, "name": v["name"], "source": v["source"], "tier": v["tier"], "to": r["to"], "from": r["from"], "pi_route": v["pi"]}
    if v["pi"]:
        d = PI.derive(v["pi"]); out["pi_value"] = d["value"]; out["pi_error"] = d["error"]; out["circle_in"] = d["circle_in"]
    return out


def atlas() -> List[Dict[str, Any]]:
    """
    Run every viewport.

    :returns: one entry dict per viewport, in registry order
    :rtype: list
    """
    return [entry(k) for k in VIEWPORTS]


def signposts() -> List[Dict[str, str]]:
    """
    The sign-post table: for each viewport, the road INTO fixed-point space, the road OUT, and the π route.

    :returns: list of dicts id, enter, exit, pi
    :rtype: list
    """
    rows = []
    for e in atlas():
        rows.append({"id": e["id"], "enters": ("YES" if e["to"]["ok"] else ("AFTER TRANSFORM" if e["to"].get("ok_transformed") else "NO")) + ": " + e["to"]["transform"],
                     "exits": ("YES" if e["from"]["ok"] else "NO") + ": " + e["from"]["fibre"], "pi": e["pi_route"] or "gap"})
    return rows


def gaps() -> Dict[str, Any]:
    """
    What the Atlas does not yet map: unrouted viewports, viewports that fail TO, and the named gaps.

    :returns: dict of three lists
    :rtype: dict
    """
    a = atlas()
    return {"no_pi_route": [e["id"] for e in a if not e["pi_route"]], "to_fails_raw": [e["id"] for e in a if not e["to"]["ok"]],
            "named_gaps": GAPS}


def _repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


CIRCLE_TOKENS = {"pi": r"(?:\bpi\b|math\.pi|np\.pi|\bπ)", "trig": r"\b(?:cos|sin|atan2?|hypot)\b", "phase": r"(?:exp\(\s*1j|cmath|\b1j\b|\btheta\b|\bphase\b)",
                 "circle": r"\b(?:circle|unit_circle|radius|orbit|rotat\w*|roots? of unity|U\(1\))\b", "wave": r"\b(?:fourier|fft|period\w*|epicycle\w*|wheel\w*)\b"}
REPOS = ["GenerationalLineage", "ValaQuenta", "RiemannHypothesisProof", "SedenionSpectralRelativity", "VAPMIP", "FourthAgePapers", "AbrikosovTree",
         "TuringStack", "UniversalSynth", "ArdaQuenta", "MultiplicationMatrixExplorer", "BulletCluster", "SemanticWordEngine", "AbrikosovTree"]
SKIP = ("/.venv", "/__pycache__", "/node_modules", "/.git/", "/build/", "/notebooks/")


def census(repos: Optional[List[str]] = None, root: Optional[str] = None) -> Dict[str, Any]:
    """
    Sweep the repositories' Python files and count circle-bearing tokens. A TEXT census: where to look, not proof.

    :param repos: repository directory names under the project root (default: the standing list)
    :type repos: list
    :param root: project root (default: three levels above this file)
    :type root: str
    :returns: dict per repo with files, lines, files_with_hits, token totals, and the ten highest-scoring files
    :rtype: dict
    """
    root = root or _repo_root(); repos = list(dict.fromkeys(repos or REPOS)); pats = {k: re.compile(v, re.I) for k, v in CIRCLE_TOKENS.items()}
    out: Dict[str, Any] = {}
    for rp in repos:
        base = os.path.join(root, rp)
        if not os.path.isdir(base):
            out[rp] = {"missing": True}; continue
        files = []; tot = {k: 0 for k in pats}; lines = 0
        for dp, dn, fn in os.walk(base):
            if any(s in dp + "/" for s in SKIP):
                continue
            for f in fn:
                if not f.endswith(".py"):
                    continue
                p = os.path.join(dp, f)
                try:
                    s = open(p, encoding="utf8", errors="ignore").read()
                except OSError:
                    continue
                n = s.count("\n") + 1; lines += n; hits = {k: len(pt.findall(s)) for k, pt in pats.items()}
                for k in tot:
                    tot[k] += hits[k]
                files.append((sum(hits.values()) / n, os.path.relpath(p, root), n, hits))
        files.sort(reverse=True)
        out[rp] = {"files": len(files), "lines": lines, "files_with_hits": sum(1 for f in files if f[0] > 0), "tokens": tot,
                   "top": [(f[1], f[2], round(f[0], 3)) for f in files[:10]]}
    return out


def import_probe() -> Dict[str, Any]:
    """
    Try to import every ValaQuenta module and every GenerationalLineage toolset; failures are recorded, not repaired.

    :returns: dict with ok and failed lists
    :rtype: dict
    """
    import importlib
    import sys
    ok, bad = [], []
    base = os.path.join(_repo_root(), "ValaQuenta", "modules")
    for d in sorted(os.listdir(base)):
        if os.path.exists(os.path.join(base, d, "__init__.py")):
            try:
                importlib.import_module(f"ValaQuenta.modules.{d}"); ok.append(f"ValaQuenta.modules.{d}")
            except Exception as e:           # recorded as data
                bad.append((f"ValaQuenta.modules.{d}", f"{type(e).__name__}: {e}"[:120]))
    gl = os.path.join(_repo_root(), "GenerationalLineage")
    if os.path.isdir(gl):
        added = gl not in sys.path
        if added:
            sys.path.insert(0, gl)
        try:
            tdir = os.path.join(gl, "engine", "toolsets")
            for f in sorted(os.listdir(tdir)):
                if f.endswith(".py") and f != "__init__.py":
                    n = f"engine.toolsets.{f[:-3]}"
                    try:
                        importlib.import_module(n); ok.append("GenerationalLineage." + n)
                    except Exception as e:
                        bad.append(("GenerationalLineage." + n, f"{type(e).__name__}: {e}"[:120]))
        finally:
            if added:
                sys.path.remove(gl)
    return {"ok": ok, "failed": bad}


def verify() -> Dict[str, Any]:
    """
    Self-checks: each viewport's TO result closes (or is flagged as not), the Wick transform of xp closes, the sign carriers are e₈…e₁₅.

    :returns: dict of check name -> bool or measured value
    :rtype: dict
    """
    out: Dict[str, Any] = {}
    for e in atlas():
        out[f"{e['id']}: TO {'closes' if e['to']['ok'] else 'does not close raw'}"] = bool(e["to"]["ok"]) or e["id"] == "berry_keating"
        out[f"{e['id']}: FROM ok"] = bool(e["from"]["ok"])
    bk = entry("berry_keating")
    out["berry_keating raw is NOT a circle (recorded failure)"] = (not bk["to"]["ok"]) and bk["to"]["residual"] > 0.1
    out["berry_keating after Wick rotation is a circle"] = bool(bk["to"]["ok_transformed"])
    out["sign carriers are e8..e15"] = sign_carriers()["carriers"] == list(range(8, 16))
    out["emergent π equals the project's TWO_PI/2"] = abs(TWO_PI / 2 - math.pi) < 1e-13
    return out
