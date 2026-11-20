# SPDX-License-Identifier: GPL-3.0-only
"""Curved spacetime: general relativity.  Symbolic curvature from any metric (sympy), the standard solutions as checks, and the measured
numbers (perihelion, light deflection, clocks, binary-pulsar decay).  Geometric units (G = c = 1) in the symbolic parts; SI in the numbers.
ESTABLISHED (Einstein 1915; Schwarzschild 1916; Friedmann 1922; Peters 1964)."""
from __future__ import annotations
import math
import numpy as np
import sympy as sp
from . import maths as R


def curvature(g: sp.Matrix, coords, simplify: bool = True) -> dict:
    """Christoffel Gamma^a_{bc}, Riemann R^a_{bcd}, Ricci R_{bd}, scalar R and Einstein G_{ab} of the metric g(coords).
    Conventions: R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb} + Gamma^a_{ce} Gamma^e_{db} - Gamma^a_{de} Gamma^e_{cb}; R_{bd} = R^a_{bad}.

    :param g: sympy metric matrix
    :param coords: tuple of sympy coordinate symbols
    :param simplify: simplify each component
    :returns: dict with Gamma, Riemann, Ricci, R, Einstein and the inverse metric
    """
    n = len(coords); gi = g.inv(); S = (lambda e: sp.simplify(e)) if simplify else (lambda e: e)
    Gam = [[[S(sum(gi[a, d] * (sp.diff(g[d, c], coords[b]) + sp.diff(g[d, b], coords[c]) - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
             for c in range(n)] for b in range(n)] for a in range(n)]
    Riem = [[[[S(sp.diff(Gam[a][d][b], coords[c]) - sp.diff(Gam[a][c][b], coords[d])
                + sum(Gam[a][c][e] * Gam[e][d][b] - Gam[a][d][e] * Gam[e][c][b] for e in range(n)))
               for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.Matrix(n, n, lambda b, d: S(sum(Riem[a][b][a][d] for a in range(n))))
    Rs = S(sum(gi[b, d] * Ric[b, d] for b in range(n) for d in range(n)))
    Ein = sp.Matrix(n, n, lambda a, b: S(Ric[a, b] - g[a, b] * Rs / 2))
    return {"Gamma": Gam, "Riemann": Riem, "Ricci": Ric, "R": Rs, "Einstein": Ein, "ginv": gi}


def kretschmann(g: sp.Matrix, coords, cur: dict | None = None):
    """K = R_{abcd} R^{abcd}.

    :param g: sympy metric matrix
    :param coords: tuple of sympy coordinate symbols
    :param cur: a precomputed curvature dict, or None
    :returns: the Kretschmann scalar
    """
    cur = cur or curvature(g, coords); n = len(coords); gi = cur["ginv"]; Rm = cur["Riemann"]
    low = [[[[sum(g[a, e] * Rm[e][b][c][d] for e in range(n)) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    # raise all four indices (the metrics used here are diagonal; general case handled by the full contraction)
    up = [[[[sum(gi[b, f] * gi[c, h] * gi[d, k] * Rm[a][f][h][k] for f in range(n) for h in range(n) for k in range(n)) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    return sp.simplify(sum(low[a][b][c][d] * up[a][b][c][d] for a in range(n) for b in range(n) for c in range(n) for d in range(n)))


def divergence_of_einstein(g: sp.Matrix, coords, cur: dict | None = None):
    """The contracted Bianchi identity: nabla_m G^{mn} = d_m G^{mn} + Gamma^m_{m l} G^{l n} + Gamma^n_{m l} G^{m l}; identically zero.

    :param g: sympy metric matrix
    :param coords: tuple of sympy coordinate symbols
    :param cur: a precomputed curvature dict, or None
    :returns: the four components of the divergence (all zero)
    """
    cur = cur or curvature(g, coords); n = len(coords); gi = cur["ginv"]; Gam = cur["Gamma"]
    Gup = gi * cur["Einstein"] * gi
    return [sp.simplify(sum(sp.diff(Gup[m, nu], coords[m]) + sum(Gam[m][m][l] * Gup[l, nu] for l in range(n)) + sum(Gam[nu][m][l] * Gup[m, l] for l in range(n)) for m in range(n))) for nu in range(n)]


# ---- the standard metrics (geometric units)
_t, _r, _th, _ph = sp.symbols("t r theta phi", positive=True)
_M, _L = sp.symbols("M L", positive=True)


def schwarzschild():
    """The Schwarzschild metric (geometric units) and its coordinates (t, r, theta, phi)."""
    f = 1 - 2 * _M / _r
    return sp.diag(-f, 1 / f, _r ** 2, _r ** 2 * sp.sin(_th) ** 2), (_t, _r, _th, _ph)


def de_sitter_static():
    """The static-patch de Sitter metric with curvature radius L and its coordinates."""
    f = 1 - _r ** 2 / _L ** 2
    return sp.diag(-f, 1 / f, _r ** 2, _r ** 2 * sp.sin(_th) ** 2), (_t, _r, _th, _ph)


def flrw_flat():
    """The flat FLRW metric with scale factor a(t) and its coordinates."""
    a = sp.Function("a")(_t); x, y, z = sp.symbols("x y z")
    return sp.diag(-1, a ** 2, a ** 2, a ** 2), (_t, x, y, z)


def flrw_curved():
    """The FLRW metric with spatial curvature k and scale factor a(t), in spherical coordinates."""
    a = sp.Function("a")(_t); k = sp.symbols("k")
    return sp.diag(-1, a ** 2 / (1 - k * _r ** 2), a ** 2 * _r ** 2, a ** 2 * _r ** 2 * sp.sin(_th) ** 2), (_t, _r, _th, _ph)


def solution_checks() -> dict:
    """The field-equation checks: Schwarzschild is vacuum (Ricci = 0) with K = 48 M^2/r^6; static de Sitter has G_{ab} = -Lambda g_{ab} with
    Lambda = 3/L^2; flat FLRW has G_tt = 3 adot^2/a^2 and G_xx = -(2 a addot + adot^2); the Bianchi identity holds for curved FLRW."""
    out = {}
    g, c = schwarzschild(); cur = curvature(g, c)
    out["schwarzschild_ricci_zero"] = bool(cur["Ricci"].is_zero_matrix); out["schwarzschild_kretschmann"] = str(kretschmann(g, c, cur))
    out["schwarzschild_K_is_48M2_over_r6"] = bool(sp.simplify(kretschmann(g, c, cur) - 48 * _M ** 2 / _r ** 6) == 0)
    g, c = de_sitter_static(); cur = curvature(g, c)
    out["desitter_R"] = str(cur["R"]); out["desitter_Einstein_is_minus_Lambda_g"] = bool(sp.simplify(cur["Einstein"] + (3 / _L ** 2) * g).is_zero_matrix)
    g, c = flrw_flat(); cur = curvature(g, c); a = g[1, 1] ** sp.Rational(1, 2); adot = sp.diff(a, _t); addot = sp.diff(a, _t, 2)
    out["flrw_Gtt"] = str(cur["Einstein"][0, 0]); out["flrw_Gtt_ok"] = bool(sp.simplify(cur["Einstein"][0, 0] - 3 * adot ** 2 / a ** 2) == 0)
    out["flrw_Gxx_ok"] = bool(sp.simplify(cur["Einstein"][1, 1] + (2 * a * addot + adot ** 2)) == 0)
    g, c = flrw_curved(); out["bianchi_flrw_curved"] = [str(x) for x in divergence_of_einstein(g, c)]
    out["all_pass"] = bool(out["schwarzschild_ricci_zero"] and out["schwarzschild_K_is_48M2_over_r6"] and out["desitter_Einstein_is_minus_Lambda_g"]
                           and out["flrw_Gtt_ok"] and out["flrw_Gxx_ok"] and all(x == "0" for x in out["bianchi_flrw_curved"]))
    return out


# ---- measured numbers
def schwarzschild_radius(GM: float) -> float:
    """Schwarzschild radius 2GM/c^2 in metres.

    :param GM: mass parameter GM, m^3 s^-2
    :returns: the radius in metres
    """
    return 2.0 * GM / R.C ** 2


def photon_sphere(GM: float) -> float:
    """Photon-sphere radius 3GM/c^2 in metres.

    :param GM: mass parameter GM, m^3 s^-2
    :returns: the radius in metres
    """
    return 3.0 * GM / R.C ** 2


def isco(GM: float) -> float:
    """Innermost stable circular orbit 6GM/c^2 in metres.

    :param GM: mass parameter GM, m^3 s^-2
    :returns: the radius in metres
    """
    return 6.0 * GM / R.C ** 2


def kerr_horizons(M: float, a: float) -> dict:
    """Geometric units: r+- = M +- sqrt(M^2 - a^2); ergosphere on the equator r = 2M.

    :param M: mass in geometric units (G = c = 1) unless stated
    :param a: spin parameter, |a| <= M
    :returns: dict of horizon radii and ergosphere radii (geometric units)
    """
    if abs(a) > M: return {"naked": True}
    s = math.sqrt(M * M - a * a); return {"r_plus": M + s, "r_minus": M - s, "ergosphere_equator": 2 * M, "ergosphere_pole": M + math.sqrt(max(M * M - a * a, 0.0))}


def hawking_temperature(M_kg: float) -> float:
    """T = hbar c^3 / (8 pi G M k_B).

    :param M_kg: mass in kilograms
    :returns: temperature in kelvin
    """
    return R.HBAR * R.C ** 3 / (8 * math.pi * R.G * M_kg * R.K_B)


def perihelion_advance_formula(GM: float, a: float, e: float) -> float:
    """Radians per orbit: 6 pi GM / (c^2 a (1 - e^2)).

    :param GM: mass parameter GM, m^3 s^-2
    :param a: constant proper acceleration (or spin parameter for Kerr)
    :param e: orbital eccentricity
    :returns: advance per orbit in radians
    """
    return 6 * math.pi * GM / (R.C ** 2 * a * (1 - e * e))


def mercury_arcsec_per_century() -> float:
    """Mercury's relativistic perihelion advance in arcseconds per century (a = 5.790905e10 m, e = 0.20563, T = 87.969 d)."""
    a, e, T_days = 5.790905e10, 0.20563, 87.969
    return perihelion_advance_formula(R.GM_SUN, a, e) * (36525.0 / T_days) * R.ARCSEC


def orbit_precession_numeric(p: float, e: float, M: float = 1.0) -> dict:
    """Integrate the Schwarzschild orbit equation u'' + u = M/L^2 + 3 M u^2 (u = 1/r, phi the angle) from periapsis to the next periapsis, with
    L^2 = M p.  Returns the measured advance of periapsis per orbit against 6 pi M / p.

    :param p: see the function
    :param e: orbital eccentricity
    :param M: mass in geometric units (G = c = 1) unless stated
    :returns: dict with the measured advance, the formula and their ratio
    """
    from scipy.integrate import solve_ivp
    L2 = M * p; u0 = (1 + e) / p
    f = lambda phi, y: [y[1], M / L2 - y[0] + 3 * M * y[0] ** 2]
    ev = lambda phi, y: y[1]; ev.direction = -1.0            # u' crosses 0 downward = periapsis (u is largest there)
    s = solve_ivp(f, [0, 4 * math.pi], [u0, 0.0], events=ev, rtol=1e-12, atol=1e-14)
    later = [t for t in s.t_events[0] if t > 1.0]             # ignore the start, which is itself a periapsis
    phi_end = float(later[0]) if later else float("nan")
    adv = phi_end - 2 * math.pi
    return {"advance": adv, "formula_6piM_over_p": 6 * math.pi * M / p, "ratio": adv / (6 * math.pi * M / p)}


def light_deflection_numeric(b: float, M: float = 1.0) -> dict:
    """Null geodesic u'' + u = 3 M u^2 from infinity with impact parameter b; total deflection against 4 M / b.

    :param b: impact parameter in units of M
    :param M: mass in geometric units (G = c = 1) unless stated
    :returns: dict with the measured deflection, 4M/b and the second-order ratio
    """
    from scipy.integrate import solve_ivp
    f = lambda phi, y: [y[1], -y[0] + 3 * M * y[0] ** 2]
    ev = lambda phi, y: y[0]; ev.terminal = True; ev.direction = -1.0
    s = solve_ivp(f, [0, 4 * math.pi], [0.0, 1.0 / b], events=ev, rtol=1e-12, atol=1e-16, first_step=1e-6)
    defl = float(s.t_events[0][0]) - math.pi
    return {"deflection": defl, "formula_4M_over_b": 4 * M / b, "ratio": defl / (4 * M / b), "second_order_ratio": 1 + 15 * math.pi * M / (16 * b)}


def solar_deflection_arcsec() -> float:
    """Grazing ray at the solar limb: 4 GM / (c^2 R)."""
    return 4 * R.GM_SUN / (R.C ** 2 * R.R_SUN) * R.ARCSEC


def clock_rate_offsets(r_orbit: float = 26561750.0) -> dict:
    """Satellite clock against a ground clock at rest on the geoid, microseconds per day: gravitational blueshift GM/c^2 (1/R_E - 1/r), velocity
    -v^2/(2c^2) with v^2 = GM/r.  The net is the GPS correction.

    :param r_orbit: orbital radius in metres
    :returns: dict of microseconds per day (gravitational, velocity, net)
    """
    grav = R.GM_EARTH / R.C ** 2 * (1 / R.R_EARTH - 1 / r_orbit); vel = -(R.GM_EARTH / r_orbit) / (2 * R.C ** 2)
    day = 86400.0
    return {"gravitational_us_per_day": grav * day * 1e6, "velocity_us_per_day": vel * day * 1e6, "net_us_per_day": (grav + vel) * day * 1e6}


def tidal_component_schwarzschild() -> dict:
    """The static observer's radial tidal component R_{t^ r^ t^ r^} = R_{trtr} (orthonormal frame), symbolically: -2M/r^3."""
    g, c = schwarzschild(); n = 4; cur = curvature(g, c)
    Rtrtr = sp.simplify(sum(g[0, e] * cur["Riemann"][e][1][0][1] for e in range(n)))
    f = 1 - 2 * _M / _r
    return {"R_trtr": sp.simplify(Rtrtr), "orthonormal": sp.simplify(Rtrtr / (f * (1 / f))), "equals_minus_2M_over_r3": bool(sp.simplify(Rtrtr + 2 * _M / _r ** 3) == 0)}


def geodesic_deviation_numeric(r0: float = 20.0, dr0: float = 1e-5, M: float = 1.0) -> dict:
    """Radial free fall from rest at r0 and at r0 + dr0 (geometric units).  Each fall is the cycloid r = (R0/2)(1 + cos eta),
    tau = (R0^{3/2} / (2 sqrt(2M)))(eta + sin eta).  The separation xi(tau) = r_2(tau) - r_1(tau) at equal proper time must satisfy
    xi'' = +2M/r^3 xi (the radial tidal stretching).  xi'' is measured by a second difference in proper time.

    :param r0: radius in units of M
    :param dr0: initial separation of the two free fallers
    :param M: mass in geometric units (G = c = 1) unless stated
    :returns: dict with the measured xi'', the prediction and their ratio
    """
    from scipy.optimize import brentq
    pos = lambda R0, eta: ((R0 / 2) * (1 + math.cos(eta)), (R0 ** 1.5 / (2 * math.sqrt(2 * M))) * (eta + math.sin(eta)))
    R2 = r0 + dr0; rows = []
    for eta1 in (0.99, 1.0, 1.01):
        r1, tau = pos(r0, eta1); eta2 = brentq(lambda e: pos(R2, e)[1] - tau, 0.0, 2.0); r2, _ = pos(R2, eta2)
        rows.append((tau, r1, r2 - r1))
    (t0, _, x0), (t1, r_mid, x1), (t2, _, x2) = rows
    h0, h1 = t1 - t0, t2 - t1
    xipp = 2 * (x0 / (h0 * (h0 + h1)) - x1 / (h0 * h1) + x2 / (h1 * (h0 + h1)))
    pred = 2 * M / r_mid ** 3 * x1
    return {"xi_second_derivative": xipp, "prediction_2M_over_r3_xi": pred, "ratio": xipp / pred}


def binary_pulsar_pdot(Pb: float = 27906.98, e: float = 0.6171334, m1: float = 1.4398, m2: float = 1.3886) -> dict:
    """Peters (1964): dPb/dt = -(192 pi / 5) (G^{5/3}/c^5) (Pb/2pi)^{-5/3} f(e) m1 m2 (m1+m2)^{-1/3}, f(e) = (1 + 73/24 e^2 + 37/96 e^4)/(1-e^2)^{7/2}.
    Masses in solar masses; Hulse-Taylor orbital elements from memory (to verify under the Literature Download Protocol).

    :param Pb: orbital period in seconds
    :param e: orbital eccentricity
    :param m1: mass of the pulsar in solar masses
    :param m2: mass of the companion in solar masses
    :returns: dict with the predicted period derivative and the enhancement factor f(e)
    """
    Msun = R.GM_SUN / R.G
    fe = (1 + 73 / 24 * e ** 2 + 37 / 96 * e ** 4) / (1 - e ** 2) ** 3.5
    pdot = -(192 * math.pi / 5) * (R.G ** (5 / 3) / R.C ** 5) * (Pb / (2 * math.pi)) ** (-5 / 3) * fe * (m1 * m2) * (m1 + m2) ** (-1 / 3) * Msun ** (5 / 3)
    return {"Pbdot": pdot, "f_e": fe, "note": "observed magnitude about 2.40e-12 (Weisberg and Huang 2016, from memory)"}


def gravitational_wave_vacuum_check() -> dict:
    """Linearised vacuum Einstein equations for a plane transverse-traceless wave h_xx = -h_yy = cos(w t - k z) (c = 1): the first-order Ricci
    tensor vanishes iff w^2 = k^2.  Returns the first-order Ricci for general (w, k)."""
    t, x, y, z, w, k, eps = sp.symbols("t x y z w k epsilon")
    h = sp.cos(w * t - k * z); g = sp.diag(-1, 1 + eps * h, 1 - eps * h, 1)
    cur = curvature(g, (t, x, y, z), simplify=False)
    R1 = sp.Matrix(4, 4, lambda i, j: sp.simplify(sp.diff(cur["Ricci"][i, j], eps).subs(eps, 0)))
    nz = {f"R_{i}{j}": sp.simplify(R1[i, j]) for i in range(4) for j in range(i, 4) if sp.simplify(R1[i, j]) != 0}
    return {"first_order_ricci_nonzero": {k_: str(v) for k_, v in nz.items()}, "vanishes_when_w2_equals_k2": bool(all(sp.simplify(v.subs(w, k)) == 0 for v in nz.values())) if nz else True}
