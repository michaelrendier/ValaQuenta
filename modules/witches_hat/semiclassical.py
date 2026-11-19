# SPDX-License-Identifier: GPL-3.0-only
r"""
ValaQuenta.modules.witches_hat.semiclassical
============================================
Where hbar comes from in the hat.  Nothing here inserts a value of hbar: the hat's own actions are computed in closed form, and the values of hbar at which exact quantum mechanics changes
character (a new bound state appears at the hilltop energy) are read off the exact Schroedinger equation and compared with what the classical actions predict.

The E = 0 (separatrix) actions of the hat V = -mu^2 r^2/2 + lambda r^4/4, with R = mu/sqrt(lambda), V0 = mu^4/(4 lambda), tau0 = R/sqrt(2 V0) and the natural action unit S0 = V0 tau0:

    W_direct = (2 mu^3 / 3 lambda)(1 - 2^(-3/2))     brim -> hilltop            (the direct sheet at the tip)
    W_wall   = (2 mu^3 / 3 lambda) 2^(-3/2)           brim -> the turning circle r = sqrt 2 R
    W_total  = 2 mu^3 / (3 lambda)                    hilltop -> turning circle  = W_direct + W_wall
    in units of S0:  W_wall = 2/3,  sheet spacing 2 W_wall = 4/3,  tip height (2/3)(2 sqrt 2 - 1) = 1.218951,  gap above the hilltop (4 sqrt 2 - 5)/3 = 0.218951.

Layers
------
ESTABLISHED  Bohr-Sommerfeld / WKB quantisation, the Weyl law (number of states = phase-space volume / (2 pi hbar)^d), Sturm oscillation (nodes of the solution count the states below E).
INTERPRETATION  that closure of a loop of phases (PhiSpiral: e^{i pi} e^{i phi} e^{i(pi - phi)} = 1) is the condition that makes hbar emerge as the unit in which a closed-loop action is 2 pi.
MEASURED  the constant offset gamma = 0.622-0.623 in W_total/(pi hbar_n) = n + gamma for the hat's thresholds (not the 1/2 of a plain two-turning-point rule); it is not derived here.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate, optimize
from scipy.linalg import eigh_tridiagonal

from .maths import model_plane


def _V(model):
    V2, _ = model_plane(model); return lambda r: float(V2(r, 0.0))


def separatrix_actions(model: dict) -> dict:
    """The E = 0 actions of the quartic hat in closed form, with the natural unit S0 = V0 tau0 and the numbers they fix.

    :param model: model dict from ``lagrangian_sm`` (needs ``mu2`` and ``lam``).
    :returns: dict ``W_direct, W_wall, W_total, S0, wall_in_S0 (2/3), sheet_spacing_in_S0 (4/3), tip_height_in_S0, gap`` and ``checks`` (the same actions by quadrature).
    :rtype: dict
    """
    mu = math.sqrt(model["mu2"]); lam = model["lam"]; R = mu/math.sqrt(lam); V0 = mu**4/(4*lam); S0 = V0*R/math.sqrt(2*V0); k = 2*mu**3/(3*lam)
    Wd = k*(1 - 2**-1.5); Ww = k*2**-1.5; Wt = k; V = _V(model); p = lambda r: math.sqrt(max(-2*V(r), 0.0))
    q = lambda a, b: integrate.quad(p, a, b, epsabs=1e-13, epsrel=1e-13, limit=400)[0]
    return {"W_direct": Wd, "W_wall": Ww, "W_total": Wt, "S0": S0, "wall_in_S0": Ww/S0, "sheet_spacing_in_S0": 2*Ww/S0, "tip_height_in_S0": Wd/S0, "gap": Wd/S0 - 1.0,
            "checks": {"W_direct": q(0, R), "W_wall": q(R, math.sqrt(2)*R), "W_total": q(0, math.sqrt(2)*R)}}


def _u_end(model, hbar, rmax):
    V = _V(model); f = lambda r, y: [y[1], 2*V(r)/hbar**2*y[0]]
    return integrate.solve_ivp(f, (0, rmax), [0.0, 1.0], rtol=1e-12, atol=1e-30, method="DOP853").y[0, -1]


def exact_thresholds(model: dict, n_states: int = 3, h_hi: float = 0.6, h_lo: float = 0.04, n_grid: int = 700) -> list:
    """The values of hbar at which a new bound state appears AT the hilltop energy (E = 0), from the exact radial Schroedinger equation (1-D, Dirichlet at the centre).

    At E = 0 the solution regular at the centre must decay beyond the turning circle; its growing part changes sign exactly at a threshold.  hbar decreases from ``h_hi``; thresholds come out
    in decreasing order.  The outer radius of the integration is 2.6 R: the thresholds depend on it until it clears the turning circle (n = 0 reads 0.296, 0.3303, 0.3410, 0.3412 at 1.55, 1.8, 2.2, 2.6 R;
    the higher ones are converged by 1.8 R).

    :param model: model dict.
    :param n_states: how many thresholds to return.
    :param h_hi: largest hbar scanned.
    :param h_lo: smallest hbar scanned.
    :param n_grid: grid size of the scan (thresholds are then refined by root finding).
    :returns: list of hbar_n, n = 0, 1, ...
    :rtype: list
    """
    R = float(model["brim_radius"]); rmax = 2.6*R; hs = np.linspace(h_hi, h_lo, n_grid); us = [_u_end(model, h, rmax) for h in hs]; out = []
    for i in range(len(hs) - 1):
        if us[i]*us[i + 1] < 0: out.append(optimize.brentq(lambda h: _u_end(model, h, rmax), hs[i + 1], hs[i], xtol=1e-12))
        if len(out) >= n_states: break
    return out


def offset_gamma(model: dict, thresholds: list) -> list:
    """gamma_n = W_total/(pi hbar_n) - n: the constant offset in the quantisation condition W_total = pi hbar (n + gamma) at the separatrix (a plain two-turning-point rule would give 1/2).

    :param model: model dict.
    :param thresholds: list from ``exact_thresholds``.
    :returns: list of gamma_n.
    :rtype: list
    """
    Wt = separatrix_actions(model)["W_total"]; return [Wt/(math.pi*h) - n for n, h in enumerate(thresholds)]


def weyl_count(model: dict, hbar: float) -> float:
    """The Weyl-law number of 2-D bound states below the hilltop: phase-space volume / (2 pi hbar)^2.  For the hat V(r), E < 0: volume = 4 pi^2 integral of (-V) r dr over V < 0.

    :param model: model dict.
    :param hbar: hbar.
    :returns: N(hbar) (for mu = lambda = 1 this is 1/(6 hbar^2)).
    :rtype: float
    """
    V = _V(model); R = float(model["brim_radius"]); vol = 4*math.pi**2*integrate.quad(lambda r: -V(r)*r, 0, math.sqrt(2)*R, epsabs=1e-13, epsrel=1e-13)[0]
    return vol/(2*math.pi*hbar)**2


def exact_count_2d(model: dict, hbar: float, mmax: int = 40, N: int = 3000) -> int:
    """The exact number of 2-D bound states below the hilltop (E < 0): radial equations for every angular momentum m, counting +/- m twice.

    :param model: model dict.
    :param hbar: hbar.
    :param mmax: largest |m|.
    :param N: radial grid points.
    :returns: the count.
    :rtype: int
    """
    V = _V(model); R = float(model["brim_radius"]); x = np.linspace(0, 2.6*R, N + 2)[1:-1]; dx = x[1] - x[0]; Vx = np.array([V(r) for r in x]); tot = 0
    for m in range(mmax):
        d = hbar**2/dx**2 + Vx + hbar**2*(m*m - 0.25)/(2*x**2); e = -hbar**2/(2*dx**2)*np.ones(N - 1)
        w = eigh_tridiagonal(d, e, select="v", select_range=(-1, 0.0))[0]; tot += len(w)*(1 if m == 0 else 2)
    return tot
