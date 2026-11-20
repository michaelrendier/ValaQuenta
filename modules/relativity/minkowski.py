# SPDX-License-Identifier: GPL-3.0-only
"""Minkowski space: special relativity.  Coordinates (ct, x, y, z), metric eta = diag(-1, 1, 1, 1).  Every function here is ESTABLISHED
(Einstein 1905; Minkowski 1908) except where the docstring says INTERPRETATION."""
from __future__ import annotations
import math
from fractions import Fraction as Fr
import numpy as np
from . import maths as R

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])


def gamma(beta: float) -> float:
    """Lorentz factor 1/sqrt(1-beta^2).

    :param beta: velocity in units of c
    :returns: 1/sqrt(1 - beta^2)
    """
    if abs(beta) >= 1: raise ValueError("|beta| must be < 1")
    return 1.0 / math.sqrt(1.0 - beta * beta)


def rapidity(beta: float) -> float:
    """phi = atanh(beta): the additive parameter of boosts along one line.

    :param beta: velocity in units of c
    :returns: atanh(beta)
    """
    return math.atanh(beta)


def boost(beta_vec) -> np.ndarray:
    """The 4x4 boost for velocity vector beta_vec (units of c) acting on (ct, x, y, z).

    :param beta_vec: velocity vector in units of c
    :returns: the 4x4 boost matrix
    """
    b = np.asarray(beta_vec, float); b2 = float(b @ b)
    if b2 >= 1: raise ValueError("|beta| must be < 1")
    g = 1.0 / math.sqrt(1.0 - b2); L = np.eye(4)
    L[0, 0] = g; L[0, 1:] = -g * b; L[1:, 0] = -g * b
    if b2 > 0: L[1:, 1:] += (g - 1.0) * np.outer(b, b) / b2
    return L


def invariance_residual(L: np.ndarray) -> float:
    """max |L^T eta L - eta|: zero iff L is a Lorentz transformation.

    :param L: a 4x4 matrix
    :returns: max |L^T eta L - eta|
    """
    return float(np.max(np.abs(L.T @ ETA @ L - ETA)))


def velocity_addition(b1: float, b2: float) -> float:
    """Collinear composition (b1 + b2)/(1 + b1 b2).

    :param b1: first velocity, units of c
    :param b2: second velocity, units of c
    :returns: the composed velocity
    """
    return (b1 + b2) / (1.0 + b1 * b2)


def rapidity_additivity(b1: float, b2: float) -> dict:
    """Velocity addition IS addition of rapidities: atanh(b1 (+) b2) = atanh b1 + atanh b2.

    :param b1: first velocity, units of c
    :param b2: second velocity, units of c
    :returns: dict with both sides and their residual
    """
    s = velocity_addition(b1, b2)
    return {"beta_sum": s, "rapidity_of_sum": rapidity(s), "sum_of_rapidities": rapidity(b1) + rapidity(b2),
            "residual": abs(rapidity(s) - rapidity(b1) - rapidity(b2))}


def interval(d4) -> dict:
    """s^2 = -(c dt)^2 + |dx|^2 and its causal kind.

    :param d4: separation of two events (c dt, dx, dy, dz)
    :returns: dict with s^2 and the causal kind
    """
    d = np.asarray(d4, float); s2 = float(d @ ETA @ d)
    kind = "spacelike" if s2 > 1e-14 else "timelike" if s2 < -1e-14 else "null"
    return {"s2": s2, "kind": kind}


def time_dilation(beta: float, proper_time: float = 1.0) -> float:
    """Coordinate time elapsed for proper time tau of a clock moving at beta: gamma tau.

    :param beta: velocity in units of c
    :param proper_time: proper time of the moving clock
    :returns: coordinate time elapsed
    """
    return gamma(beta) * proper_time


def length_contraction(beta: float, rest_length: float = 1.0) -> float:
    """Length of a rod measured in a frame in which it moves at beta: rest_length / gamma.

    :param beta: velocity in units of c
    :param rest_length: length in the rod's rest frame
    :returns: the contracted length
    """
    return rest_length / gamma(beta)


def doppler_longitudinal(beta: float) -> float:
    """Frequency ratio received/emitted for a source receding at beta (beta > 0 receding): sqrt((1-beta)/(1+beta)).

    :param beta: velocity in units of c
    :returns: received/emitted frequency ratio
    """
    return math.sqrt((1.0 - beta) / (1.0 + beta))


def doppler_factor(beta: float) -> float:
    """k = sqrt((1+beta)/(1-beta)) = e^phi: the factor by which a boost scales the light-cone coordinate v = ct - x.

    :param beta: velocity in units of c
    :returns: sqrt((1+beta)/(1-beta))
    """
    return math.sqrt((1.0 + beta) / (1.0 - beta))


def lightcone_dilation_check(beta: float) -> dict:
    """In u = ct + x, v = ct - x a boost along x acts as u -> u/k, v -> k v with k = Doppler factor: a pure dilation, not a rotation.

    :param beta: velocity in units of c
    :returns: dict with the scalings and their residual
    """
    k = doppler_factor(beta); L = boost([beta, 0, 0]); ev = np.array([1.3, 0.4, 0, 0]); e2 = L @ ev
    u, v = ev[0] + ev[1], ev[0] - ev[1]; u2, v2 = e2[0] + e2[1], e2[0] - e2[1]
    return {"k": k, "u_scaled": u2 / u, "expected_u": 1 / k, "v_scaled": v2 / v, "expected_v": k,
            "residual": max(abs(u2 / u - 1 / k), abs(v2 / v - k))}


def thomas_wigner(beta1: float, beta2: float) -> dict:
    """Two perpendicular boosts do not compose to a boost: the product is a boost times a rotation (the Thomas-Wigner rotation).  The angle
    is read from the rotation part R = B^-1 L of L = B(y, beta2) B(x, beta1), and compared with cos(theta) = (g1 + g2)/(1 + g1 g2).

    :param beta1: speed of the first boost, units of c
    :param beta2: speed of the second boost, units of c
    :returns: dict with the measured and formula cosines and the angle
    """
    L = boost([0, beta2, 0]) @ boost([beta1, 0, 0]); u = L[:, 0]; Bc = boost(-u[1:] / u[0]); Rm = np.linalg.inv(Bc) @ L
    cos_meas = (np.trace(Rm[1:, 1:]) - 1.0) / 2.0; g1, g2 = gamma(beta1), gamma(beta2)
    cos_form = (g1 + g2) / (1.0 + g1 * g2)
    return {"cos_theta_measured": float(cos_meas), "cos_theta_formula": cos_form, "angle_deg": math.degrees(math.acos(max(-1, min(1, cos_meas)))),
            "residual": abs(cos_meas - cos_form), "rotation_block_is_orthogonal": bool(np.allclose(Rm[1:, 1:].T @ Rm[1:, 1:], np.eye(3), atol=1e-12))}


def lorentz_algebra() -> dict:
    """The six generators J_i (rotations) and K_i (boosts) of so(3,1) and their commutators: [J_i,J_j] = e_ijk J_k, [J_i,K_j] = e_ijk K_k,
    [K_i,K_j] = - e_ijk J_k.  Returns the largest violation (should be 0)."""
    J, K = [], []
    for i in range(3):
        j = np.zeros((4, 4)); a, b = [(2, 3), (3, 1), (1, 2)][i]; j[a, b] = -1; j[b, a] = 1; J.append(j)
        k = np.zeros((4, 4)); k[0, i + 1] = 1; k[i + 1, 0] = 1; K.append(k)
    comm = lambda A, B: A @ B - B @ A; eps = lambda i, j, k: (i - j) * (j - k) * (k - i) / 2
    worst = 0.0
    for i in range(3):
        for j in range(3):
            for kk in range(3):
                e = eps(i, j, kk)
                worst = max(worst, np.max(np.abs(comm(J[i], J[j])[:] - sum(eps(i, j, m) * J[m] for m in range(3)))),
                            np.max(np.abs(comm(J[i], K[j]) - sum(eps(i, j, m) * K[m] for m in range(3)))),
                            np.max(np.abs(comm(K[i], K[j]) + sum(eps(i, j, m) * J[m] for m in range(3)))))
    return {"generators": 6, "max_commutator_violation": float(worst), "dimension_of_group": 6}


def four_momentum(m: float, p_vec, c: float = 1.0) -> np.ndarray:
    """(E/c, p) with E = sqrt((pc)^2 + (mc^2)^2).

    :param m: rest mass
    :param p_vec: three-momentum
    :param c: speed of light in the units in use
    :returns: the array (E/c, p)
    """
    p = np.asarray(p_vec, float); E = math.sqrt((c * np.linalg.norm(p)) ** 2 + (m * c * c) ** 2)
    return np.array([E / c, *p])


def invariant_mass(*four_momenta, c: float = 1.0) -> float:
    """sqrt(-(sum p)^2 c^2): the invariant mass of a system, the same in every frame.

    :param c: speed of light in the units in use (the four-momenta are passed positionally)
    :returns: the invariant mass of the system
    """
    P = np.sum(four_momenta, axis=0); s = -(P @ ETA @ P)
    return math.sqrt(max(s, 0.0)) / c


def fixed_target_threshold(m_beam: float, m_target: float, m_products_total: float) -> float:
    """Minimum beam kinetic energy (units of mc^2 of the same unit as the masses) to make products of total mass M on a fixed target:
    T = ((M^2 - (m1 + m2)^2) / (2 m2)) c^2.  For p + p -> p + p + p + pbar (M = 4 m_p, m1 = m2 = m_p): T = 6 m_p c^2.

    :param m_beam: mass of the beam particle
    :param m_target: mass of the target particle
    :param m_products_total: total mass of the products
    :returns: the minimum beam kinetic energy
    """
    return (m_products_total ** 2 - (m_beam + m_target) ** 2) / (2.0 * m_target)


def hyperbolic_motion(a: float, t: float, c: float = R.C) -> dict:
    """Constant proper acceleration a from rest: proper time tau = (c/a) asinh(a t / c), distance x = (c^2/a)(sqrt(1 + (a t/c)^2) - 1).

    :param a: constant proper acceleration
    :param t: coordinate time
    :param c: speed of light in the units in use
    :returns: dict with proper time, distance and velocity
    """
    return {"tau": (c / a) * math.asinh(a * t / c), "x": (c * c / a) * (math.sqrt(1.0 + (a * t / c) ** 2) - 1.0), "beta": (a * t / c) / math.sqrt(1.0 + (a * t / c) ** 2)}


def trip_proper_time(distance: float, a: float, c: float = R.C) -> float:
    """Proper time for a journey of length `distance` at constant proper acceleration a for the first half, deceleration for the second:
    tau = 2 (c/a) acosh(1 + a d / (2 c^2)).

    :param distance: length of the journey
    :param a: constant proper acceleration (or spin parameter for Kerr)
    :param c: speed of light in the units in use
    :returns: proper time of the traveller
    """
    return 2.0 * (c / a) * math.acosh(1.0 + a * distance / (2.0 * c * c))


def em_field_invariants(E, B, c: float = 1.0) -> dict:
    """E^2 - c^2 B^2 and E.B are Lorentz invariants of the electromagnetic field.  Returns them and their values after a boost (they must agree).

    :param E: electric field vector
    :param B: magnetic field vector
    :param c: speed of light in the units in use
    :returns: dict with E^2 - c^2 B^2 and E.B
    """
    E = np.asarray(E, float); B = np.asarray(B, float)
    return {"E2_minus_c2B2": float(E @ E - c * c * (B @ B)), "E_dot_B": float(E @ B)}


def em_boost(E, B, beta_vec, c: float = 1.0):
    """Fields in a frame moving with velocity beta (units of c): E'_par = E_par, E'_perp = g(E + v x B)_perp, B'_perp = g(B - v x E/c^2)_perp.

    :param E: electric field vector
    :param B: magnetic field vector
    :param beta_vec: velocity vector in units of c
    :param c: speed of light in the units in use
    :returns: the transformed (E, B)
    """
    E = np.asarray(E, float); B = np.asarray(B, float); b = np.asarray(beta_vec, float); v = b * c; b2 = float(b @ b)
    if b2 == 0: return E, B
    g = 1.0 / math.sqrt(1 - b2); n = b / math.sqrt(b2)
    Epar = (E @ n) * n; Bpar = (B @ n) * n
    E2 = Epar + g * (E - Epar + np.cross(v, B)); B2 = Bpar + g * (B - Bpar - np.cross(v, E) / (c * c))
    return E2, B2


def lorentz_derivation() -> dict:
    """Derive the boost's form from the invariance of the interval.  A symmetric, unit-determinant-sign map of (ct, x) with equal diagonal g and
    off-diagonal -g b (parity and the relativity principle make these the only freedoms) preserves -(ct)^2 + x^2 iff g^2 (1 - b^2) = 1, i.e.
    g = 1/sqrt(1 - b^2), b = v/c.  Done symbolically."""
    import sympy as sp
    g, b = sp.symbols("g b", positive=True)
    M = sp.Matrix([[g, -g * b], [-g * b, g]]); eta = sp.diag(-1, 1)
    eq = sp.simplify(M.T * eta * M - eta)
    sol = sp.solve(eq[0, 0], g)
    return {"condition_00": sp.simplify(eq[0, 0]), "condition_01": sp.simplify(eq[0, 1]), "condition_11": sp.simplify(eq[1, 1]), "g": [sp.simplify(x) for x in sol]}
