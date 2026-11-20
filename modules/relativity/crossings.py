# SPDX-License-Identifier: GPL-3.0-only
"""Crossings: where one jurisdiction hands over to another.  Weak field (curved -> Newton), the horizon's Euclidean smoothness (curved ->
Euclidean), and the conversion-field metric of the Witch's Hat length-time page (Ainulindale wiki 140) read as a 1+1 spacetime."""
from __future__ import annotations
import math
import sympy as sp
from . import curved as Cv
from . import maths as R


def newtonian_limit() -> dict:
    """Weak static field g_00 = -(1 + 2 eps Phi), g_ij = (1 - 2 eps Phi) delta_ij.  The first-order Ricci component R_00 is the Laplacian of Phi:
    the field equation R_00 = 4 pi G (rho + 3p) -> nabla^2 Phi = 4 pi G rho for dust.  Computed with an arbitrary function Phi(x, y, z)."""
    t, x, y, z, eps = sp.symbols("t x y z epsilon"); Phi = sp.Function("Phi")(x, y, z)
    g = sp.diag(-(1 + 2 * eps * Phi), (1 - 2 * eps * Phi), (1 - 2 * eps * Phi), (1 - 2 * eps * Phi))
    cur = Cv.curvature(g, (t, x, y, z), simplify=False)
    R00 = sp.simplify(sp.diff(cur["Ricci"][0, 0], eps).subs(eps, 0)); lap = sum(sp.diff(Phi, v, 2) for v in (x, y, z))
    return {"R00_first_order": str(R00), "equals_laplacian_of_Phi": bool(sp.simplify(R00 - lap) == 0)}


def euclidean_horizon_period() -> dict:
    """Schwarzschild continued to Euclidean time t = -i tau: near r = 2M the metric is dr^2/f + f dtau^2 ~ d rho^2 + kappa^2 rho^2 dtau^2 with
    kappa = f'(2M)/2; it is smooth (no conical singularity) iff tau has period 2 pi/kappa = 8 pi M.  Hence T = 1/(8 pi M) (geometric units)."""
    r, M = sp.symbols("r M", positive=True); f = 1 - 2 * M / r
    kappa = sp.simplify(sp.diff(f, r).subs(r, 2 * M) / 2)
    return {"kappa": str(kappa), "period": str(sp.simplify(2 * sp.pi / kappa)), "temperature": str(sp.simplify(kappa / (2 * sp.pi))),
            "period_is_8piM": bool(sp.simplify(2 * sp.pi / kappa - 8 * sp.pi * M) == 0)}


def conversion_field_curvature(v_expr, x=None) -> dict:
    """Read a conversion field v(x) (Ainulindale wiki 140: length = v x time) as the 1+1 metric ds^2 = -v(x)^2 dt^2 + dx^2.  Its scalar curvature
    is R = -2 v''/v.  At a simple zero x0 of v the surface gravity is kappa = v'(x0) (a horizon: infinite transit time, finite length); at a
    square-root zero the transit time is finite (a mirror).  Rindler (v = kappa x) is flat.

    :param v_expr: sympy expression for the conversion field v(x)
    :param x: sympy symbol for the position
    :returns: dict with the scalar curvature and the check R = -2 v''/v
    """
    t = sp.Symbol("t"); x = x or sp.Symbol("x", real=True)
    g = sp.diag(-v_expr ** 2, 1); cur = Cv.curvature(g, (t, x))
    return {"R": sp.simplify(cur["R"]), "R_equals_minus_2vpp_over_v": bool(sp.simplify(cur["R"] + 2 * sp.diff(v_expr, x, 2) / v_expr) == 0)}


def hat_conversion_field() -> dict:
    """The Witch's Hat at E = 0 (mu = lambda = 1): v^2 = 2(E - V) = x^2 - x^4/2, v = x sqrt(1 - x^2/2).  Near the hilltop x = 0 the zero of v is
    simple with kappa = 1 (a horizon-like zero; wiki 140: infinite transit time); at the turning circle x = sqrt(2) it is a square-root zero
    (a mirror).  The curvature of the 1+1 conversion-field metric is computed."""
    x = sp.Symbol("x", positive=True); v = x * sp.sqrt(1 - x ** 2 / 2)
    k0 = sp.limit(v / x, x, 0); cf = conversion_field_curvature(v, x)
    # classify the zero at sqrt(2): v ~ C (sqrt2 - x)^p
    s = sp.Symbol("s", positive=True); vs = sp.simplify(v.subs(x, sp.sqrt(2) - s)); p = sp.limit(sp.log(vs) / sp.log(s), s, 0, "+")
    return {"kappa_at_hilltop": str(k0), "curvature": str(cf["R"]), "exponent_at_turning_circle": str(p), "zero_at_turning_circle": "square-root (mirror)" if p == sp.Rational(1, 2) else "other"}


def flat_limit_scaling() -> dict:
    """Schwarzschild M -> 0: the metric tends to Minkowski and every curvature invariant vanishes: Kretschmann 48 M^2 / r^6 -> 0 as M^2.  The
    crossing from curved to minkowski is the limit of vanishing mass (or of distance large against M)."""
    r, M = sp.symbols("r M", positive=True); K = 48 * M ** 2 / r ** 6
    return {"K_over_M2": str(sp.simplify(K / M ** 2)), "limit_M_to_0": str(sp.limit(K, M, 0)), "limit_r_to_oo": str(sp.limit(K, r, sp.oo))}
