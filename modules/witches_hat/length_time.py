# SPDX-License-Identifier: GPL-3.0-only
r"""
ValaQuenta.modules.witches_hat.length_time
==========================================
LENGTH AND TIME AS ONE THING, and the swap between them.  Each function is a claim that is tested, not assumed.

The setting is any space with a propagation-speed field.  In the hat at energy E a path has speed v(q) = sqrt(2 (E - V(q))), so the potential V is the field that converts length into
time.  Then

1. every classical path is a NULL curve of the optical metric  ds^2 = -v(q)^2 dt^2 + |dq|^2  (length = v dt along it): length and time are the same thing in the unit the space itself
   fixes.  Measured in transit time, rho(r) = integral dr / v (the tortoise coordinate), every radial path is a straight 45-degree line in (rho, t): the potential has become the ruler.
2. length-like and time-like quantities are conjugate:  t = dW/dE  (W = integral p dq, the reduced action, the Jacobi length), and in the forbidden region  dB/dE = -tau  (B = barrier action,
   tau = Euclidean time): the same relation continued across the swap, with real time replaced by imaginary time.
3. the two rulers split: the path of least time (Fermat, speed field v) and the path of least action (Maupertuis/Jacobi, the dynamical path) are different curves unless v is constant, which is
   the one case in which length and time are proportional.  The size of the split is a property of the space.
4. the swap: where v^2 changes sign the optical metric changes signature, and real time becomes Euclidean time.  The turning surface (v -> 0 like a square root) lies at finite transit time and
   finite length; the E = 0 hilltop (v -> 0 like r) lies at INFINITE transit time and FINITE length: an i^+ point.
5. the compactifications: Penrose uses arctan on a time; the Smith chart's Gamma = tanh(rho / 2) uses tanh on a length rho = ln s.  They are the same map under the swap rho -> i t:
   tanh(i x/2) = i tan(x/2); and 2 arctan(tanh(x/2)) = arctan(sinh x) is the Gudermannian function.

Layers
------
ESTABLISHED  Hamilton-Jacobi (t = dW/dE), Fermat's and Maupertuis' principles, the optical / analogue metric, the tortoise coordinate, the Wick rotation, the Gudermannian function.
INTERPRETATION  that "length and time are the same thing" is the null condition in the space's own conversion field, and that the Penrose swap and the Smith-chart compactification are one map
             under rho -> i t (Ainulindale wiki 140).
Units: those of the model (unit mass).
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate, optimize

from .maths import model_plane


def _V(model):
    V2, _ = model_plane(model); return lambda r: float(V2(r, 0.0))


def speed(model: dict, E: float, r: float) -> float:
    """v(r) = sqrt(2 (E - V(r))), zero in the forbidden region (where the speed is imaginary).

    :param model: rotationally symmetric model dict.
    :param E: energy.
    :param r: radius.
    :returns: the speed, or 0.0 where E < V.
    :rtype: float
    """
    return math.sqrt(max(2*(E - _V(model)(r)), 0.0))


def tortoise(model: dict, E: float, r: float, r_ref: float = None) -> float:
    """The transit ruler rho(r) = integral from r_ref to r of dr' / v(r'): length measured in time.  Default r_ref = 0 when the hilltop is reachable at finite time (E > V(0)), else the brim.

    At E = V(0) the integral diverges logarithmically at the hilltop (rho -> -infinity): the hilltop is at infinite transit time.

    :param model: model dict with ``brim_radius``.
    :param E: energy.
    :param r: radius (inside the turning radius).
    :param r_ref: reference radius where rho = 0.
    :returns: rho(r).
    :rtype: float
    """
    V = _V(model); R = float(model["brim_radius"]); v = lambda x: math.sqrt(2*(E - V(x)))
    ref = (0.0 if E > V(0.0) + 1e-12 else R) if r_ref is None else r_ref
    return integrate.quad(lambda x: 1.0/v(x), ref, r, epsabs=1e-13, epsrel=1e-13, limit=400)[0]


def radial_worldline(model: dict, E: float, T: float, n: int = 400) -> dict:
    """The radial path from the brim inward at energy E, integrated as an ODE: arrays t, r, and rho(r(t)) + t (constant if the path is a 45-degree line in (rho, t)).

    :param model: model dict.
    :param E: energy (above the hilltop value so the path reaches the centre).
    :param T: duration.
    :param n: number of samples.
    :returns: dict ``t, r, rho_plus_t, deviation`` (max |rho + t - rho(1)|).
    :rtype: dict
    """
    V2, grad = model_plane(model); R = float(model["brim_radius"]); v0 = speed(model, E, R)
    f = lambda t, y: [y[1], -float(grad(y[0], 0.0)[0])]
    ev = lambda t, y: y[0] - 1e-3; ev.terminal = True; ev.direction = -1
    ts = np.linspace(0, T, n); s = integrate.solve_ivp(f, (0, T), [R, -v0], t_eval=ts, rtol=1e-12, atol=1e-14, method="DOP853", events=ev)
    t, r = s.t, s.y[0]; rho = np.array([tortoise(model, E, x) for x in r]); const = rho + t
    return {"t": t, "r": r, "rho_plus_t": const, "deviation": float(np.max(np.abs(const - const[0])))}


def conjugacy(model: dict, E: float, source=(1.0, 0.0), theta: float = 2.6, t1: float = 1.5, dE: float = 1e-4) -> dict:
    """Check t = dW/dE for a NON-radial path: the reduced action W and the transit time t of the path that joins the same two points at E +/- dE, by central difference.

    A path from ``source`` at angle ``theta`` is integrated to time t1; its endpoint q1 is then reached at E +/- dE by solving for the launch angle and time (2-D Newton on the endpoint).

    :param model: model dict.
    :param E: energy.
    :param source: start point.
    :param theta: launch angle of the reference path.
    :param t1: its duration.
    :param dE: energy step.
    :returns: dict ``t_reference``, ``dW_dE`` (central difference), ``relative_error``, ``W``.
    :rtype: dict
    """
    V2, grad = model_plane(model); A = np.asarray(source, float)
    def shoot(E_, th, tt):
        sp = math.sqrt(2*(E_ - float(V2(*A)))); f = lambda t, y: [y[2], y[3], -float(grad(y[0], y[1])[0]), -float(grad(y[0], y[1])[1]), y[2]**2 + y[3]**2]
        s = integrate.solve_ivp(f, (0, tt), [A[0], A[1], sp*math.cos(th), sp*math.sin(th), 0.0], rtol=1e-12, atol=1e-14, method="DOP853")
        return s.y[:2, -1], s.y[4, -1]
    q1, W0 = shoot(E, theta, t1)
    def at(E_):
        g = lambda x: shoot(E_, x[0], x[1])[0] - q1
        sol = optimize.root(g, [theta, t1], tol=1e-13); return shoot(E_, sol.x[0], sol.x[1])[1]
    dW = (at(E + dE) - at(E - dE))/(2*dE)
    return {"t_reference": t1, "dW_dE": float(dW), "relative_error": float(abs(dW - t1)/t1), "W": W0}


def barrier_conjugacy(model: dict, E: float = 0.02, r2: float = 1.8, dE: float = 1e-4) -> dict:
    """The same relation across the swap: in the forbidden region B(E) = integral sqrt(2 (V - E)) dr (barrier action) and tau(E) = integral dr / sqrt(2 (V - E)) (Euclidean time) satisfy dB/dE = -tau.

    :param model: model dict.
    :param E: energy (between the brim value and the outer rim).
    :param r2: outer end of the barrier region.
    :param dE: energy step.
    :returns: dict ``tau``, ``dB_dE``, ``relative_error``, ``r1`` (the turning radius).
    :rtype: dict
    """
    V = _V(model); R = float(model["brim_radius"])
    def turn(E_): return optimize.brentq(lambda x: V(x) - E_, R, 3.0)
    def B(E_): r1 = turn(E_); return integrate.quad(lambda x: math.sqrt(max(2*(V(x) - E_), 0.0)), r1, r2, epsabs=1e-13, epsrel=1e-13, limit=400)[0]
    def tau(E_):
        r1 = turn(E_); h = lambda x: math.sqrt(2*(V(x) - E_)/(x - r1)) if x > r1 else math.sqrt(2*(V(r1 + 1e-9) - E_)/1e-9)
        return integrate.quad(lambda x: 1.0/h(x), r1, r2, weight="alg", wvar=(-0.5, 0.0), epsabs=1e-13, epsrel=1e-13, limit=400)[0]
    t_ = tau(E); dB = (B(E + dE) - B(E - dE))/(2*dE)
    return {"tau": t_, "dB_dE": float(dB), "relative_error": float(abs(dB + t_)/t_), "r1": turn(E)}


def two_rulers(model: dict, A, B, E: float, N: int = 50, constant_speed: bool = False, invert: bool = False) -> dict:
    """The path of least action (W = sum |dq| v, the Jacobi / dynamical path) and the path of least time (T = sum |dq| / v) between the same two points at the same energy.

    Both are found by minimising the discretised functional over the interior points from the straight line.  For constant speed (V = const) the two coincide and are the straight line.

    :param model: model dict.
    :param A: start point.
    :param B: end point.
    :param E: energy.
    :param N: number of segments.
    :param constant_speed: use v = v(A) everywhere (the control).
    :param invert: replace the speed field v by 1/v: the two functionals exchange roles exactly (the length-time swap).
    :returns: dict ``T_of_action_path``, ``T_min``, ``W_of_action_path``, ``W_of_time_path``, ``split`` (relative excess of the action path's time over the minimum), ``max_separation``, ``action_path``, ``time_path`` (arrays of points).
    :rtype: dict
    """
    V2, _ = model_plane(model); A = np.asarray(A, float); B = np.asarray(B, float); v0 = math.sqrt(2*(E - float(V2(*A))))
    vq = (lambda p: v0*np.ones(len(p))) if constant_speed else (lambda p: np.sqrt(np.maximum(2*(E - np.asarray(V2(p[:, 0], p[:, 1]), float)), 1e-12)))
    if invert: vq_ = vq; vq = lambda p: 1.0/vq_(p)
    def full(x): return np.vstack([A, x.reshape(-1, 2), B])
    def metrics(x):
        P = full(x); d = np.hypot(*(np.diff(P, axis=0)).T); m = 0.5*(P[1:] + P[:-1]); v = vq(m); return np.sum(d*v), np.sum(d/v)
    line = np.linspace(A, B, N + 1)[1:-1].reshape(-1); res = {}
    for name, idx in (("action", 0), ("time", 1)):
        r = optimize.minimize(lambda x: metrics(x)[idx], line, method="L-BFGS-B", options={"maxiter": 5000, "ftol": 1e-15, "gtol": 1e-12}); res[name] = r.x
    Wa, Ta = metrics(res["action"]); Wt, Tt = metrics(res["time"]); sep = float(np.max(np.hypot(*(full(res["action"]) - full(res["time"])).T)))
    return {"T_of_action_path": float(Ta), "T_min": float(Tt), "W_of_action_path": float(Wa), "W_of_time_path": float(Wt), "split": float((Ta - Tt)/Tt), "max_separation": sep, "action_path": full(res["action"]), "time_path": full(res["time"])}


def hilltop_clock(model: dict, E: float = 0.0, radii=(1e-1, 1e-2, 1e-3, 1e-4, 1e-5)) -> dict:
    """At the separatrix E = V(0) the hilltop is at infinite transit time but finite length: rho(r) - rho(1) grows like ln r (slope 1 per e-fold) while the reduced action stays finite.

    :param model: model dict.
    :param E: energy (the hilltop value).
    :param radii: radii at which to read the ruler.
    :returns: dict ``rho`` (list), ``slopes`` (drho / d ln r between successive radii), ``W_to_hilltop``.
    :rtype: dict
    """
    V = _V(model); R = float(model["brim_radius"]); rho = [tortoise(model, E, r, r_ref=R) for r in radii]
    slopes = [(rho[i + 1] - rho[i])/(math.log(radii[i + 1]) - math.log(radii[i])) for i in range(len(radii) - 1)]
    W = integrate.quad(lambda x: math.sqrt(max(2*(E - V(x)), 0.0)), 0, R, epsabs=1e-13, epsrel=1e-13, limit=400)[0]
    return {"rho": rho, "slopes": slopes, "W_to_hilltop": W}


def wall_transit(model: dict, E: float = 0.0) -> dict:
    """The turning surface is at FINITE transit time and length: rho from the brim to the turning radius, and the turning radius.

    :param model: model dict.
    :param E: energy.
    :returns: dict ``r_turn``, ``rho_brim_to_wall``.
    :rtype: dict
    """
    V = _V(model); R = float(model["brim_radius"]); rt = optimize.brentq(lambda x: V(x) - E, R, 3.0)
    h = lambda x: math.sqrt(2*(E - V(x))/(rt - x)) if x < rt else math.sqrt(2*(-(V(rt - 1e-9)) + E)/1e-9)
    rho = integrate.quad(lambda x: 1.0/h(x), R, rt, weight="alg", wvar=(0.0, -0.5), epsabs=1e-13, epsrel=1e-13, limit=400)[0]
    return {"r_turn": rt, "rho_brim_to_wall": rho}


def compactifications(x=None) -> dict:
    """Penrose (arctan of a time) and Smith-chart (tanh of a length) compactifications, and the swap rho -> i t that relates them.

    Checks: tanh(i x/2) = i tan(x/2); 2 arctan(tanh(x/2)) = arctan(sinh(x)) (the Gudermannian function); the Smith map Gamma = (s - 1)/(s + 1) equals tanh(ln(s)/2).

    :param x: sample points (default a grid).
    :returns: dict of maximum residuals.
    :rtype: dict
    """
    x = np.linspace(-6, 6, 241) if x is None else np.asarray(x, float); s = np.exp(x)
    return {"wick_tanh_to_tan": float(np.max(np.abs(np.tanh(1j*x/2) - 1j*np.tan(x/2)))), "gudermannian": float(np.max(np.abs(2*np.arctan(np.tanh(x/2)) - np.arctan(np.sinh(x))))),
            "smith_is_tanh_of_half_log": float(np.max(np.abs((s - 1)/(s + 1) - np.tanh(np.log(s)/2))))}


def signature_map(model: dict, E: float, radii) -> list:
    """Signature of the optical metric -v^2 dt^2 + dr^2 + r^2 dphi^2 at each radius: 'Lorentzian' where E > V, 'null (cone closes)' at E = V, 'Euclidean' where E < V.

    :param model: model dict.
    :param E: energy.
    :param radii: radii.
    :returns: list of ``(r, v2, signature)``.
    :rtype: list
    """
    V = _V(model); out = []
    for r in radii:
        v2 = 2*(E - V(r)); out.append((float(r), v2, "Lorentzian" if v2 > 1e-12 else ("null (cone closes)" if abs(v2) <= 1e-12 else "Euclidean")))
    return out
