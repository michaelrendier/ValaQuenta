# SPDX-License-Identifier: GPL-3.0-only
"""The space of metrics: where Einstein's equations live.  The Einstein-Hilbert action on the (a, N) slice of the space of metrics (flat
FLRW with a lapse), its variation, and the gauge invariance of the linearised curvature."""
from __future__ import annotations
import sympy as sp
from . import curved as Cv


def minisuperspace_friedmann() -> dict:
    """Restrict the metric to ds^2 = -N(t)^2 dt^2 + a(t)^2 dx^2 (a two-dimensional slice of the space of metrics).  The action
    S = (1/16 pi G) int N a^3 R dt - int N a^3 rho(a) dt.  Varying the lapse N gives the first Friedmann equation as a CONSTRAINT: the
    lapse is a Lagrange multiplier, not a dynamical variable.  Computed with sympy's Euler-Lagrange equations (second derivatives allowed)."""
    t = sp.Symbol("t"); x, y, z = sp.symbols("x y z"); Gc = sp.Symbol("G", positive=True)
    N = sp.Function("N")(t); a = sp.Function("a")(t); rho = sp.Function("rho")
    g = sp.diag(-N ** 2, a ** 2, a ** 2, a ** 2); cur = Cv.curvature(g, (t, x, y, z))
    Lag = N * a ** 3 * cur["R"] / (16 * sp.pi * Gc) - N * a ** 3 * rho(a)
    from sympy.calculus.euler import euler_equations
    eqs = euler_equations(Lag, [N, a], t)
    EN = sp.simplify(eqs[0].lhs.subs(N, 1).doit()); Ea = sp.simplify(eqs[1].lhs.subs(N, 1).doit())
    adot = sp.diff(a, t); friedmann_form = sp.simplify(EN + a ** 3 * (rho(a) - 3 * adot ** 2 / (8 * sp.pi * Gc * a ** 2)))
    friedmann_form_neg = sp.simplify(EN - a ** 3 * (rho(a) - 3 * adot ** 2 / (8 * sp.pi * Gc * a ** 2)))
    return {"lapse_equation": str(EN), "scale_factor_equation": str(Ea), "lapse_eq_is_friedmann": bool(friedmann_form == 0 or friedmann_form_neg == 0),
            "lapse_in_equation": bool(EN.has(sp.diff(N, t))), "note": "N is a Lagrange multiplier: its equation contains no time derivative of N."}


def linearised_gauge_invariance() -> dict:
    """Linearised Riemann R_{abcd} = 1/2 (d_b d_c h_{ad} + d_a d_d h_{bc} - d_a d_c h_{bd} - d_b d_d h_{ac}) is unchanged by h -> h + d_a xi_b + d_b xi_a
    (an infinitesimal diffeomorphism).  Checked for explicit non-trivial xi: the residual is exactly zero."""
    t, x, y, z = sp.symbols("t x y z"); X = (t, x, y, z)
    xi = [sp.sin(x * y) + t ** 2, t * z ** 2 + x, sp.exp(y) * z, x * y * z * t]
    h = sp.Matrix(4, 4, lambda a, b: sp.diff(xi[b], X[a]) + sp.diff(xi[a], X[b]))
    def lin(hm): return [[[[sp.Rational(1, 2) * (sp.diff(hm[a, d], X[b], X[c]) + sp.diff(hm[b, c], X[a], X[d]) - sp.diff(hm[b, d], X[a], X[c]) - sp.diff(hm[a, c], X[b], X[d]))
                            for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    L = lin(h); worst = max(sp.simplify(L[a][b][c][d]) != 0 for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    return {"pure_gauge_h_has_nonzero_components": bool(any(h[a, b] != 0 for a in range(4) for b in range(4))), "linearised_riemann_of_pure_gauge_is_zero": not bool(worst)}
