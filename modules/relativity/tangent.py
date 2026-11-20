# SPDX-License-Identifier: GPL-3.0-only
"""The tangent space: where special relativity is legal inside general relativity.  The equivalence principle in two measurements: the
connection can be made to vanish at an event by a change of coordinates, and the curvature cannot."""
from __future__ import annotations
import math
import numpy as np
import sympy as sp
from . import curved as Cv


def equivalence_principle_report(r0: float = 10.0, M: float = 1.0) -> dict:
    """Schwarzschild at radius r0 (geometric units).  1. Gamma(p) is not zero in Schwarzschild coordinates.  2. The coordinate change
    y = (x - p) + 1/2 Gamma(p)(x - p)^2 has Jacobian = identity at p and second derivative d^2x/dy^2 = -Gamma(p); the transformation law
    Gamma' = dy/dx [ dx/dy dx/dy Gamma + d^2 x/dy dy ] then gives Gamma'(p) = 0 (computed here numerically from the law, not assumed).
    3. The Kretschmann scalar at p is unchanged and non-zero: the curvature remains.  4. The local metric deviates from eta at second order
    in distance, with a scale set by K^(-1/4).

    :param r0: radius in units of M
    :param M: mass in geometric units (G = c = 1) unless stated
    :returns: dict with the connection norm before and after, the Kretschmann scalar and the validity length
    """
    g, c = Cv.schwarzschild(); cur = Cv.curvature(g, c); sub = {sp.Symbol("M", positive=True): M, sp.Symbol("r", positive=True): r0, sp.Symbol("theta", positive=True): math.pi / 3}
    n = 4
    Gam = np.array([[[float(cur["Gamma"][a][b][cc].subs(sub)) for cc in range(n)] for b in range(n)] for a in range(n)])
    K = float(Cv.kretschmann(g, c, cur).subs(sub))
    J = np.eye(n)                                           # dx/dy at p
    d2 = -Gam                                               # d^2 x^nu / dy^alpha dy^beta at p
    Jinv = np.linalg.inv(J)                                 # dy/dx at p
    Gam_new = np.einsum("mn,nab->mab", Jinv, np.einsum("ra,sb,nrs->nab", J, J, Gam) + d2)
    return {"Gamma_norm_before": float(np.linalg.norm(Gam)), "Gamma_norm_after": float(np.linalg.norm(Gam_new)), "kretschmann_at_p": K,
            "kretschmann_after": K, "curvature_survives": bool(K > 0), "local_validity_length": K ** -0.25,
            "note": "Kretschmann is a scalar, so it is the same in the new coordinates by definition; the content is that it is not zero."}


def tidal_ellipsoid(r: float, M: float = 1.0) -> dict:
    """The tidal tensor of a static observer in Schwarzschild, orthonormal frame, eigenvalues of the relative acceleration d^2 xi/d tau^2 = -E xi:
    radial +2M/r^3 (stretch), the two tangential -M/r^3 (squeeze); trace zero (vacuum).

    :param r: radius in units of M
    :param M: mass in geometric units
    :returns: dict of the radial, tangential and trace tidal eigenvalues
    """
    s = 2 * M / r ** 3; q = -M / r ** 3
    return {"radial_stretch": s, "tangential": q, "trace": s + 2 * q}
