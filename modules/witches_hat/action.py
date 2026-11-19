# SPDX-License-Identifier: GPL-3.0-only
r"""
ValaQuenta.modules.witches_hat.action
=====================================
THE PATH OF ACTION, MAPPED.  Nothing in this file aims, designs or imposes a focal point.  Given a Lagrangian on the hat
potential it computes what is there:

1. the action S[q] of ANY candidate path between two fixed events (``discrete_action``): some paths cost more, some less;
2. the paths on which S is stationary (``stationary_paths``), found by solving delta S = 0 for fixed endpoints and duration, with
   the second variation of S (``morse_index``: how many directions lower the action, i.e. how many conjugate points the path has
   passed) and the spread of S over neighbouring paths (``trial_variations``: positive and negative where the stationary path is
   a saddle, all positive where it is a minimum);
3. the whole family of solutions of the equation of motion leaving one source point (``ray_family``): every launch direction, no
   chosen one.  Where neighbouring paths cross, the map from launch direction to position is singular (its Jacobian vanishes).
   Those places are the caustics (conjugate points); ``caustic_summary`` reports them.  A focus, if there is one, is a
   consequence of the potential's shape and appears here or does not.

Two signatures use the same machinery.  The Lorentzian one moves in V with L = T - V.  The Euclidean one (Wick rotation t -> -i tau)
moves in U = -V and its action is S_E = integral (T + V) d tau; ``euclidean_radial_release`` is the one-dimensional bounce from rest.
Every function takes a ``model`` dict from ``maths.lagrangian_sm`` or ``maths.lagrangian_vap`` (anything with ``model_plane``).

Layers
------
ESTABLISHED  Hamilton's principle (stationary action), the Euler-Lagrange equations, the Morse index as the count of conjugate
             points, the Jacobi / variational equation for neighbouring paths, S = W - E t with W = integral p dq, the Euclidean
             (Wick-rotated) motion in -V.  Closed forms the tests use: the free particle S = |B - A|^2/(2T), the harmonic
             oscillator S = w/(2 sin wT) [(|A|^2 + |B|^2) cos wT - 2 A.B], conjugate point at wT = pi.
THEORETICAL  The author's reading that the cost of a path varies (more work, less work) and evens out at the stationary path, and
             that a focus follows from the hat's shape.  This file measures that reading; it does not assume it.

Units: those of the model (unit mass).  Nothing here uses a framework constant.
"""
from __future__ import annotations
import math
import numpy as np
from scipy import integrate

from .maths import model_plane, hilltop

LORENTZIAN, EUCLIDEAN = "lorentzian", "euclidean"


# ------------------------------------------------------------------ the potential seen by a signature
def _sign(signature: str) -> float:
    if signature == LORENTZIAN: return 1.0
    if signature == EUCLIDEAN: return -1.0
    raise ValueError("signature must be 'lorentzian' or 'euclidean'")


def motion_potential(model: dict, signature: str = LORENTZIAN):
    """Return the potential the motion happens in, for one signature, as three vectorised callables.

    :param model: a model dict (``lagrangian_sm`` or ``lagrangian_vap``).
    :param signature: ``'lorentzian'`` (U = V) or ``'euclidean'`` (U = -V).
    :returns: ``(U, gradU, hessU)``; each takes ``q`` of shape ``(..., 2)`` and returns shape ``(...)``, ``(..., 2)``, ``(..., 2, 2)``.
    :rtype: tuple
    """
    s = _sign(signature); V2, grad = model_plane(model)
    h = 1e-6*float(model.get("brim_radius") or 1.0)

    def U(q):
        q = np.asarray(q, float); return s*np.asarray(V2(q[..., 0], q[..., 1]), float)

    def gU(q):
        q = np.asarray(q, float); gx, gy = grad(q[..., 0], q[..., 1]); return s*np.stack([np.asarray(gx, float), np.asarray(gy, float)], -1)

    def HU(q):
        q = np.asarray(q, float); x, y = q[..., 0], q[..., 1]
        gxp, gyp = grad(x + h, y); gxm, gym = grad(x - h, y); fxp, fyp = grad(x, y + h); fxm, fym = grad(x, y - h)
        Hxx = (np.asarray(gxp, float) - np.asarray(gxm, float))/(2*h); Hyx = (np.asarray(gyp, float) - np.asarray(gym, float))/(2*h)
        Hxy = (np.asarray(fxp, float) - np.asarray(fxm, float))/(2*h); Hyy = (np.asarray(fyp, float) - np.asarray(fym, float))/(2*h)
        off = 0.5*(Hxy + Hyx)
        return s*np.stack([np.stack([Hxx, off], -1), np.stack([off, Hyy], -1)], -2)
    return U, gU, HU


# ------------------------------------------------------------------ 1. the action of any path
def discrete_action(model: dict, q, T: float, signature: str = LORENTZIAN) -> float:
    """Action of a candidate path sampled at equal time steps: S = sum [ |dq|^2/(2 dt) - dt (U_i + U_(i+1))/2 ].

    :param model: model dict.
    :param q: array ``(N + 1, 2)``, the path from q[0] to q[N] in total time ``T``.
    :param T: duration.
    :param signature: ``'lorentzian'`` (S = integral T - V) or ``'euclidean'`` (S_E = integral T + V).
    :returns: the action (units of the model).
    :rtype: float
    """
    q = np.asarray(q, float); n = len(q) - 1; dt = T/n; U, _, _ = motion_potential(model, signature)
    kin = 0.5*np.sum(np.diff(q, axis=0)**2)/dt; u = U(q)
    return float(kin - dt*np.sum(0.5*(u[:-1] + u[1:])))


# ------------------------------------------------------------------ 2. stationary paths and what surrounds them
def _newton(model, A, B, T, N, signature, q0, tol=1e-10, maxit=80):
    U, gU, HU = motion_potential(model, signature); dt = T/N; d = 2*(N - 1)
    q = np.array(q0, float); q[0], q[-1] = A, B
    def resid(qq):
        r = (qq[2:] - 2*qq[1:-1] + qq[:-2])/dt**2 + gU(qq[1:-1]); return r
    def jac(qq):
        H = HU(qq[1:-1]); J = np.zeros((d, d)); I2 = np.eye(2)/dt**2
        for i in range(N - 1):
            J[2*i:2*i + 2, 2*i:2*i + 2] = -2*I2 + H[i]
            if i > 0: J[2*i:2*i + 2, 2*i - 2:2*i] = I2
            if i < N - 2: J[2*i:2*i + 2, 2*i + 2:2*i + 4] = I2
        return J
    r = resid(q); nr = float(np.max(np.abs(r)))
    for _ in range(maxit):
        if nr < tol: break
        try: step = np.linalg.solve(jac(q), -r.reshape(-1)).reshape(-1, 2)
        except np.linalg.LinAlgError: break
        lam = 1.0
        while lam > 1e-6:
            qn = q.copy(); qn[1:-1] += lam*step; rn = resid(qn); nn = float(np.max(np.abs(rn)))
            if nn < nr: break
            lam *= 0.5
        else: break
        q, r, nr = qn, rn, nn
    return q, nr


def morse_index(model: dict, q, T: float, signature: str = LORENTZIAN, tol: float = 1e-9) -> dict:
    """Second variation of the action at a path with fixed endpoints: the eigenvalues of the Hessian of S over the interior points.

    The number of negative eigenvalues is the Morse index: the number of independent directions in which the action goes DOWN,
    equal to the number of conjugate points the path has passed.  Index 0 means the stationary path is a local minimum of S.

    :param model: model dict.
    :param q: stationary path ``(N + 1, 2)``.
    :param T: duration.
    :param signature: ``'lorentzian'`` or ``'euclidean'``.
    :param tol: eigenvalues with absolute value below this are counted as zero (a degenerate, i.e. conjugate, path).
    :returns: ``{'index', 'zero_modes', 'eigenvalues', 'eigenvectors'}``; column k of ``eigenvectors`` is the interior displacement (flattened ``(N - 1, 2)``) of eigenvalue k.
    :rtype: dict
    """
    q = np.asarray(q, float); N = len(q) - 1; dt = T/N; _, _, HU = motion_potential(model, signature); H = HU(q[1:-1]); d = 2*(N - 1)
    S = np.zeros((d, d))
    for i in range(N - 1):
        S[2*i:2*i + 2, 2*i:2*i + 2] = 2*np.eye(2)/dt - dt*H[i]
        if i > 0: S[2*i:2*i + 2, 2*i - 2:2*i] = -np.eye(2)/dt
        if i < N - 2: S[2*i:2*i + 2, 2*i + 2:2*i + 4] = -np.eye(2)/dt
    ev, vec = np.linalg.eigh(0.5*(S + S.T)); scale = float(np.max(np.abs(ev)))
    return {"index": int(np.sum(ev < -tol*scale)), "zero_modes": int(np.sum(np.abs(ev) <= tol*scale)), "eigenvalues": ev, "eigenvectors": vec}


def stationary_paths(model: dict, A, B, T: float, N: int = 160, signature: str = LORENTZIAN, seeds=None, tol: float = 1e-9) -> list:
    """Every stationary path (delta S = 0) between two fixed events that the solver reaches, with its action and Morse index.

    The solver is started from several seeds (the straight line and sine-mode bulges).  A seed is only a starting point: a path is
    kept only if it satisfies the discrete Euler-Lagrange equations to ``tol``; distinct paths are told apart by their action and
    shape.  Several stationary paths between the same two events is itself the signature of having crossed a caustic.

    :param model: model dict.
    :param A: start point ``(x, y)``.
    :param B: end point ``(x, y)``.
    :param T: duration.
    :param N: number of time steps.
    :param signature: ``'lorentzian'`` or ``'euclidean'``.
    :param seeds: optional list of bulge amplitudes (in units of |B - A| or of the start radius); default a small symmetric set.
    :param tol: maximum residual of the Euler-Lagrange equations for a path to count.
    :returns: list of dicts ``{'q', 't', 'S', 'residual', 'index', 'zero_modes'}``, sorted by action.
    :rtype: list
    """
    A = np.asarray(A, float); B = np.asarray(B, float); t = np.linspace(0, T, N + 1); s = (t/T)[:, None]; line = A + s*(B - A)
    chord = B - A; nrm = float(np.hypot(*chord)); perp = np.array([-chord[1], chord[0]])/nrm if nrm > 1e-12 else np.array([0.0, 1.0])
    amp = float(np.hypot(*A)) if nrm < 1e-9 else nrm
    amps = [0.0] if seeds is None else list(seeds)
    if seeds is None: amps = [0.0, 0.3, -0.3, 0.8, -0.8, 1.6, -1.6]
    found = []
    for k in (1, 2):
        for a in amps:
            if a == 0.0 and k == 2: continue
            q0 = line + a*amp*np.sin(k*math.pi*s)*perp
            q, nr = _newton(model, A, B, T, N, signature, q0)
            if nr > tol: continue
            S = discrete_action(model, q, T, signature)
            if any(abs(S - f["S"]) < 1e-6*max(1.0, abs(S)) and np.max(np.abs(q - f["q"])) < 1e-4*max(1.0, amp) for f in found): continue
            mi = morse_index(model, q, T, signature)
            found.append({"q": q, "t": t, "S": S, "residual": nr, "index": mi["index"], "zero_modes": mi["zero_modes"]})
    return sorted(found, key=lambda f: f["S"])


def trial_variations(model: dict, path: dict, T: float, signature: str = LORENTZIAN, n: int = 300, amplitude: float = 0.05,
                     modes: int = 6, seed: int = 0) -> dict:
    """The cost of neighbouring paths relative to a stationary one: dS = S[q + eps delta] - S[q] for n random smooth variations.

    Variations are sums of sine modes (fixed endpoints), scaled so the largest displacement is ``amplitude`` times the path's own
    size.  Where the stationary path is a minimum every dS is positive.  Past a conjugate point some are negative: the path costs
    more work than some neighbours and less than others, and the first variation is zero.

    :param model: model dict.
    :param path: one entry of ``stationary_paths`` (needs ``q``).
    :param T: duration.
    :param signature: ``'lorentzian'`` or ``'euclidean'``.
    :param n: number of random variations.
    :param amplitude: maximum displacement as a fraction of the path's extent.
    :param modes: number of sine modes in a variation.
    :param seed: random seed (reproducible).
    :returns: ``{'dS', 'fraction_negative', 'fraction_positive', 'min', 'max', 'first_variation_max', 'eigenmode_dS', 'index'}``.
              ``first_variation_max`` is the largest first-order change of S over the variations (a symmetric difference with the cubic term removed
              by Richardson extrapolation), which must be ~0 at a stationary path.  ``eigenmode_dS`` is dS for the four cheapest directions (the lowest eigenvectors of the second
              variation, scaled to the same amplitude): negative entries are directions in which the path does LESS work than this one;
              their number is ``index``.
    :rtype: dict
    """
    q = np.asarray(path["q"], float); N = len(q) - 1; rng = np.random.default_rng(seed); t = np.linspace(0, T, N + 1); S0 = discrete_action(model, q, T, signature)
    ext = max(float(np.ptp(q[:, 0])), float(np.ptp(q[:, 1])), 1e-9); dS = []; first = 0.0
    for _ in range(n):
        d = np.zeros_like(q)
        for k in range(1, modes + 1): d += np.sin(k*math.pi*t/T)[:, None]*rng.normal(size=2)[None, :]/k
        d *= amplitude*ext/max(float(np.max(np.abs(d))), 1e-12); sp = discrete_action(model, q + d, T, signature); sm = discrete_action(model, q - d, T, signature)
        hp = discrete_action(model, q + d/2, T, signature); hm = discrete_action(model, q - d/2, T, signature)
        dS += [sp - S0, sm - S0]; q1 = (sp - sm)/2; q2 = (hp - hm); first = max(first, abs((4*q2 - q1)/3))     # Richardson: removes the cubic term of an anharmonic potential
    mi = morse_index(model, q, T, signature); em = []
    for k in range(min(4, mi["eigenvectors"].shape[1])):
        d = np.zeros_like(q); d[1:-1] = mi["eigenvectors"][:, k].reshape(-1, 2); d *= amplitude*ext/max(float(np.max(np.abs(d))), 1e-12); em.append(discrete_action(model, q + d, T, signature) - S0)
    dS = np.array(dS); return {"eigenmode_dS": np.array(em), "index": mi["index"], "dS": dS, "fraction_negative": float(np.mean(dS < 0)), "fraction_positive": float(np.mean(dS > 0)),
                               "min": float(dS.min()), "max": float(dS.max()), "first_variation_max": first/amplitude/ext}


# ------------------------------------------------------------------ 3. the whole family of solutions from a source
def ray_family(model: dict, source, E: float, n_theta: int = 360, t_max: float = 6.0, n_t: int = 1200, signature: str = LORENTZIAN,
               theta_range=(0.0, 2*math.pi)) -> dict:
    """All solutions of the equation of motion at energy E leaving ``source``: one for every launch direction, none chosen.

    Integrated together with the variational equation (J = dq/d theta, dJ/dt = Jdot, dJdot/dt = -Hess U J), so that
    D(t) = J x v, the Jacobian of (theta, t) -> position, comes out exactly.  D changes sign where neighbouring paths cross
    (a caustic, a conjugate point of the source).  The action accumulates as S = W - E t with W = integral |v|^2 dt = integral p dq.

    :param model: model dict.
    :param source: start point ``(x, y)`` (for the hat: any point, for example on the brim).
    :param E: energy in the motion potential (must exceed U at the source).
    :param n_theta: number of launch directions, equally spaced over ``theta_range``.
    :param t_max: duration of each path.
    :param n_t: time samples per path.
    :param signature: ``'lorentzian'`` or ``'euclidean'``.
    :param theta_range: launch angles ``(lo, hi)``; the default is the full circle (endpoint excluded).
    :returns: ``{'theta', 't', 'q', 'v', 'D', 'W', 'S', 'E', 'signature', 'source'}`` as arrays shaped ``(n_theta, n_t, ...)``.
    :rtype: dict
    :raises ValueError: if E does not exceed U at the source.
    """
    U, gU, HU = motion_potential(model, signature); A = np.asarray(source, float); k0 = E - float(U(A))
    if k0 <= 0: raise ValueError("E must exceed the potential at the source")
    sp = math.sqrt(2*k0); lo, hi = theta_range; full = abs((hi - lo) - 2*math.pi) < 1e-9
    th = np.linspace(lo, hi, n_theta, endpoint=not full); ts = np.linspace(0, t_max, n_t)
    Q = np.zeros((n_theta, n_t, 2)); V = np.zeros_like(Q); D = np.zeros((n_theta, n_t)); W = np.zeros((n_theta, n_t))
    def rhs(t, y):
        q = y[0:2]; v = y[2:4]; J = y[4:6]; Jd = y[6:8]; g = gU(q); H = HU(q)
        return np.concatenate([v, -g, Jd, -H@J, [v@v]])
    for i, a in enumerate(th):
        c, s = math.cos(a), math.sin(a); y0 = np.concatenate([A, sp*np.array([c, s]), [0, 0], sp*np.array([-s, c]), [0.0]])
        sol = integrate.solve_ivp(rhs, (0, t_max), y0, t_eval=ts, rtol=1e-10, atol=1e-12, method="DOP853")
        Y = sol.y.T; m = len(Y); Q[i, :m] = Y[:, 0:2]; V[i, :m] = Y[:, 2:4]; D[i, :m] = Y[:, 4]*Y[:, 3] - Y[:, 5]*Y[:, 2]; W[i, :m] = Y[:, 8]
    return {"theta": th, "t": ts, "q": Q, "v": V, "D": D, "W": W, "S": W - E*ts[None, :], "E": E, "signature": signature, "source": A}


def caustic_points(family: dict, t_skip: float = 1e-3) -> dict:
    """Where the family's Jacobian D = J x v changes sign: the caustic (conjugate) points of the source, read off, not designed.

    :param family: result of ``ray_family``.
    :param t_skip: ignore times before this (D starts at zero at the source).
    :returns: ``{'xy': (m, 2), 'theta', 't', 'order'}`` where ``order`` counts the sign changes along each path (1 = first conjugate point).
    :rtype: dict
    """
    D = family["D"]; t = family["t"]; Q = family["q"]; th = family["theta"]; pts = []; k0 = int(np.searchsorted(t, t_skip))
    for i in range(D.shape[0]):
        order = 0
        for j in range(max(k0, 1), D.shape[1]):
            a, b = D[i, j - 1], D[i, j]
            if a == 0.0 or b == 0.0 or a*b > 0: continue
            f = a/(a - b); xy = Q[i, j - 1] + f*(Q[i, j] - Q[i, j - 1]); order += 1; pts.append((xy[0], xy[1], th[i], t[j - 1] + f*(t[j] - t[j - 1]), order))
    arr = np.array(pts) if pts else np.zeros((0, 5)); return {"xy": arr[:, :2], "theta": arr[:, 2], "t": arr[:, 3], "order": arr[:, 4].astype(int)}


def caustic_summary(model: dict, family: dict, caustics: dict = None) -> dict:
    """Describe what the map produced, without judging it: where the caustics lie relative to the hilltop and the brim, how large
    they are, and the closest any path of the family comes to the hilltop.

    :param model: model dict (for the brim radius and the hilltop).
    :param family: result of ``ray_family``.
    :param caustics: result of ``caustic_points`` (computed if omitted).
    :returns: ``{'n_caustic_points', 'first_order_extent_over_brim', 'nearest_caustic_to_hilltop_over_brim', 'closest_path_to_hilltop_over_brim',
                 'theta_of_closest_path', 'brim', 'hilltop'}``; entries are None when there are no caustic points.
    :rtype: dict
    """
    caustics = caustics or caustic_points(family); R = float(model.get("brim_radius") or 1.0); top = hilltop(model); xy = caustics["xy"]
    d = np.hypot(family["q"][..., 0] - top[0], family["q"][..., 1] - top[1]); per = d.min(axis=1); i = int(np.argmin(per))
    out = {"n_caustic_points": int(len(xy)), "closest_path_to_hilltop_over_brim": float(per[i]/R), "theta_of_closest_path": float(family["theta"][i]),
           "brim": R, "hilltop": top, "first_order_extent_over_brim": None, "nearest_caustic_to_hilltop_over_brim": None}
    if len(xy):
        first = xy[caustics["order"] == 1]
        if len(first): out["first_order_extent_over_brim"] = float(max(np.ptp(first[:, 0]), np.ptp(first[:, 1]))/R)
        out["nearest_caustic_to_hilltop_over_brim"] = float(np.min(np.hypot(xy[:, 0] - top[0], xy[:, 1] - top[1]))/R)
    return out


def closest_approach_profile(model: dict, family: dict) -> dict:
    """For every launch direction, how close the path comes to the hilltop (a measurement of the family, not a target).

    :param model: model dict.
    :param family: result of ``ray_family``.
    :returns: ``{'theta', 'closest_over_brim', 'time_of_closest'}``, arrays of length ``n_theta``.
    :rtype: dict
    """
    top = hilltop(model); R = float(model.get("brim_radius") or 1.0)
    d = np.hypot(family["q"][..., 0] - top[0], family["q"][..., 1] - top[1]); j = np.argmin(d, axis=1)
    return {"theta": family["theta"], "closest_over_brim": d[np.arange(len(j)), j]/R, "time_of_closest": family["t"][j]}


# ------------------------------------------------------------------ the Euclidean half: the bounce
def euclidean_radial_release(model: dict, r0: float) -> dict:
    """Release at rest at radius r0 (inside the brim) and move in U = -V (the Wick-rotated motion) to the hilltop.

    E_U = U(r0); the speed at the hilltop is sqrt(2 (U(r0) - U(0))); the time tau to reach it is found by integrating the equation of motion to the hilltop (the quadrature integral dr / sqrt(2 (U(r0) - U(r))) loses its digits to cancellation near the singular end), finite for
    r0 below the brim and diverging logarithmically as r0 approaches it (the brim is a ring of equilibria of -V).  W_E = integral v^2 dt = integral v dr and
    S_E = integral (T + V) d tau = W_E - E_U tau, with U = -V.

    :param model: model dict.
    :param r0: release radius, 0 < r0 < brim.
    :returns: ``{'tau', 'speed_at_hilltop', 'W', 'S_E', 'E_U'}``.
    :rtype: dict
    :raises ValueError: if r0 is not inside the brim.
    """
    R = float(model["brim_radius"]) if model.get("brim_radius") else None; U, _, _ = motion_potential(model, EUCLIDEAN)
    if R is None or not 0 < r0 < R: raise ValueError("r0 must lie inside the brim (0 < r0 < brim_radius)")
    u = lambda r: float(U(np.array([r, 0.0]))); E_U = u(r0); u0 = u(0.0)
    _, gU, _ = motion_potential(model, EUCLIDEAN)
    ev = lambda t, y: y[0]; ev.terminal = True; ev.direction = -1
    sol = integrate.solve_ivp(lambda t, y: [y[1], -float(gU(np.array([y[0], 0.0]))[0]), y[1]**2], (0, 1e4), [r0, 0.0, 0.0], events=ev, rtol=1e-12, atol=1e-14, method="DOP853")
    tau = float(sol.t_events[0][0]); Wc = float(sol.y_events[0][0][2])
    return {"tau": tau, "speed_at_hilltop": math.sqrt(2*(E_U - u0)), "W": Wc, "S_E": Wc - E_U*tau, "E_U": E_U}


# ------------------------------------------------------------------ a time-dependent background: the original L_dynamic (wiki 51, 2026-06-12)
def moving_hat_exchange(model: dict, start, velocity, u, T: float, n: int = 2000) -> dict:
    """A particle in the hat while the hat moves with constant velocity u (V(q - u t)): the energy it exchanges with the moving field.

    For an explicitly time-dependent potential the energy E = |v|^2/2 + V(q - u t) is not conserved: dE/dt = dV/dt|_q = -u . grad V (established mechanics).
    The 'slingshot' of the original L_dynamic (L_standard + integral J_red d(J_blue)/dt, wiki 51) is this exchange.  Returned: the energy along the path, the
    accumulated exchange, their difference (an identity, ~0), and the largest excursion against the final value (energy borrowed and returned).

    :param model: model dict (the hat is centred at the origin at t = 0).
    :param start: initial position ``(x, y)``.
    :param velocity: initial velocity ``(vx, vy)``.
    :param u: velocity of the hat ``(ux, uy)``.
    :param T: duration.
    :param n: number of output samples.
    :returns: ``{'t', 'q', 'E', 'exchange', 'identity_residual', 'dE_final', 'dE_max_excursion'}``.
    :rtype: dict
    """
    V2, grad = model_plane(model); u = np.asarray(u, float)
    def rhs(t, y):
        c = u*t; gx, gy = grad(y[0] - c[0], y[1] - c[1]); gx, gy = float(gx), float(gy)
        return [y[2], y[3], -gx, -gy, -(u[0]*gx + u[1]*gy)]          # last component: dV/dt at fixed q, accumulated
    y0 = [start[0], start[1], velocity[0], velocity[1], 0.0]; ts = np.linspace(0, T, n)
    sol = integrate.solve_ivp(rhs, (0, T), y0, t_eval=ts, rtol=1e-11, atol=1e-13, method="DOP853"); q = sol.y[:2].T; v = sol.y[2:4].T; ex = sol.y[4]
    E = 0.5*np.sum(v*v, 1) + np.array([float(V2(q[i, 0] - u[0]*ts[i], q[i, 1] - u[1]*ts[i])) for i in range(len(ts))])
    dE = E - E[0]
    return {"t": ts, "q": q, "E": E, "exchange": ex, "identity_residual": float(np.max(np.abs(dE - ex))), "dE_final": float(dE[-1]), "dE_max_excursion": float(np.max(np.abs(dE)))}


# ------------------------------------------------------------------ the whole bundle from the brim, and the tip of the action cone
def ray_bundle(model: dict, starts, velocities, T: float, n_steps: int = 1500, u=(0.0, 0.0), target=None, store_every: int = 10) -> dict:
    """Integrate many paths at once (vectorised RK4) in the hat, which may drift with constant velocity u: V(q - u t).

    Each path carries the Lagrangian action S = integral (|v|^2/2 - V) dt, the reduced action W = integral |v|^2 dt = integral p dq and the arc length s = integral |v| dt.
    ``target`` (a point, fixed in the hat's frame) records each path's closest approach to it: distance, time, position (hat frame), W, S and s at that moment.

    :param model: model dict.
    :param starts: array ``(N, 2)`` of start positions (lab frame at t = 0).
    :param velocities: array ``(N, 2)`` of initial lab-frame velocities.
    :param T: duration.
    :param n_steps: number of RK4 steps (dt = T/n_steps).
    :param u: velocity of the hat.
    :param target: hat-frame point whose closest approach is tracked (default the hilltop).
    :param store_every: keep every this-many steps of the trajectory.
    :returns: dict ``t, q (N, m, 2), W, S, s (N, m)`` (lab frame, sampled), ``closest`` with ``dist, t, q_rel, W, S, s`` (each of length N), ``E_final`` and ``E_initial`` (lab energy).
    :rtype: dict
    """
    V2, grad = model_plane(model); target = hilltop(model) if target is None else np.asarray(target, float); u = np.asarray(u, float)
    q = np.array(starts, float); v = np.array(velocities, float); N = len(q); dt = T/n_steps; S = np.zeros(N); W = np.zeros(N); s = np.zeros(N)
    def acc(qq, t):
        c = u*t; gx, gy = grad(qq[:, 0] - c[0], qq[:, 1] - c[1]); return -np.stack([np.asarray(gx, float), np.asarray(gy, float)], 1)
    def Vq(qq, t):
        c = u*t; return np.asarray(V2(qq[:, 0] - c[0], qq[:, 1] - c[1]), float)
    best = np.full(N, np.inf); bt = np.zeros(N); bq = np.zeros((N, 2)); bW = np.zeros(N); bS = np.zeros(N); bs = np.zeros(N); E0 = 0.5*np.sum(v*v, 1) + Vq(q, 0.0)
    m = n_steps//store_every + 1; Q = np.zeros((N, m, 2)); Wm = np.zeros((N, m)); Sm = np.zeros((N, m)); sm = np.zeros((N, m)); tm = np.zeros(m); Q[:, 0] = q
    def note(i, t):
        rel = q - u*t; d = np.hypot(rel[:, 0] - target[0], rel[:, 1] - target[1]); upd = d < best
        best[upd] = d[upd]; bt[upd] = t; bq[upd] = rel[upd]; bW[upd] = W[upd]; bS[upd] = S[upd]; bs[upd] = s[upd]
    note(0, 0.0)
    for i in range(n_steps):
        t = i*dt
        def f(qq, vv, tt): return vv, acc(qq, tt), 0.5*np.sum(vv*vv, 1) - Vq(qq, tt), np.sum(vv*vv, 1), np.hypot(vv[:, 0], vv[:, 1])
        k1 = f(q, v, t); k2 = f(q + 0.5*dt*k1[0], v + 0.5*dt*k1[1], t + 0.5*dt); k3 = f(q + 0.5*dt*k2[0], v + 0.5*dt*k2[1], t + 0.5*dt); k4 = f(q + dt*k3[0], v + dt*k3[1], t + dt)
        q = q + dt/6*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]); v = v + dt/6*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
        S = S + dt/6*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2]); W = W + dt/6*(k1[3] + 2*k2[3] + 2*k3[3] + k4[3]); s = s + dt/6*(k1[4] + 2*k2[4] + 2*k3[4] + k4[4])
        note(i + 1, (i + 1)*dt)
        if (i + 1) % store_every == 0:
            j = (i + 1)//store_every; Q[:, j] = q; Wm[:, j] = W; Sm[:, j] = S; sm[:, j] = s; tm[j] = (i + 1)*dt
    E1 = 0.5*np.sum(v*v, 1) + Vq(q, T)
    return {"t": tm, "q": Q, "W": Wm, "S": Sm, "s": sm, "closest": {"dist": best, "t": bt, "q_rel": bq, "W": bW, "S": bS, "s": bs}, "E_initial": E0, "E_final": E1}


def brim_bundle(model: dict, E: float = None, n_sources: int = 24, n_dirs: int = 1441, T: float = 6.0, n_steps: int = 1500, eps: float = 0.15, u=(0.0, 0.0), chunk: int = 6000) -> dict:
    """The bundle of paths from every brim point in every launch direction at energy E (default: the value at the hilltop), and the part of it that reaches the tip.

    Nothing is aimed: sources are equally spaced on the brim ring, directions equally spaced over the full circle, speeds fixed by E.  A path is *selected* by what it does
    (it passes within ``eps`` brim radii of the hilltop), not by how it was launched.  Selected paths are returned truncated at their closest approach.

    :param model: model dict with a ``brim_radius``.
    :param E: energy (lab frame at t = 0).
    :param n_sources: sources on the brim ring.
    :param n_dirs: launch directions per source.
    :param T: duration.
    :param n_steps: RK4 steps.
    :param eps: selection radius, in brim radii.
    :param u: velocity of the hat.
    :param chunk: number of paths integrated at once.
    :returns: dict ``paths`` (list of dicts ``q, W, S, s, t`` truncated at the closest approach, plus ``source, direction, dist``), ``n_total``, ``n_selected``, ``r_min`` (all paths), ``E``, ``R``, ``hilltop``.
    :rtype: dict
    """
    R = float(model["brim_radius"]); V2, _ = model_plane(model); top = hilltop(model); E = float(V2(*top)) if E is None else E
    al = 2*math.pi*np.arange(n_sources)/n_sources; th = 2*math.pi*np.arange(n_dirs)/n_dirs
    st = np.stack([R*np.cos(al), R*np.sin(al)], 1); S0 = np.repeat(st, n_dirs, 0); V0 = np.asarray(V2(S0[:, 0], S0[:, 1]), float); sp = np.sqrt(np.maximum(2*(E - V0), 0.0))
    vel = np.stack([sp*np.tile(np.cos(th), n_sources), sp*np.tile(np.sin(th), n_sources)], 1); src = np.repeat(np.arange(n_sources), n_dirs); dirn = np.tile(np.arange(n_dirs), n_sources)
    paths = []; rmins = []
    for a in range(0, len(S0), chunk):
        b = min(a + chunk, len(S0)); r = ray_bundle(model, S0[a:b], vel[a:b], T, n_steps, u=u, target=top); cl = r["closest"]; rmins.append(cl["dist"]/R)
        for k in np.where(cl["dist"] < eps*R)[0]:
            m = int(np.searchsorted(r["t"], cl["t"][k])) + 1; m = max(2, min(m, len(r["t"])))
            paths.append({"q": r["q"][k, :m], "W": r["W"][k, :m], "S": r["S"][k, :m], "s": r["s"][k, :m], "t": r["t"][:m], "source": int(src[a + k]), "direction": int(dirn[a + k]), "dist": float(cl["dist"][k]/R),
                          "closest": {kk: (vv[k] if np.ndim(vv) else vv) for kk, vv in cl.items()}})
    return {"paths": paths, "n_total": len(S0), "n_selected": len(paths), "r_min": np.concatenate(rmins), "E": E, "R": R, "hilltop": top}


def natural_units(model: dict) -> dict:
    """The hat's own units for putting energy and action on one vertical scale: R (brim radius), V_0 (depth), tau_0 = R / sqrt(2 V_0) (the crossing time at the brim speed of the untilted
    hat), the brim level (the ring average of V, exact for a linear tilt) and the function z_V(q) = (V(q) - brim level)/V_0, which is 0 on the brim and 1 at the symmetric hilltop.
    A path's action cone stands at z = z_V(start) + W/(V_0 tau_0).

    :param model: model dict with ``brim_radius`` and ``depth``.
    :returns: dict ``R, depth, tau, level, zV``.
    :rtype: dict
    """
    V2, _ = model_plane(model); R = float(model["brim_radius"]); depth = float(model["depth"]); a = np.linspace(0, 2*math.pi, 256, endpoint=False)
    level = float(np.mean(V2(R*np.cos(a), R*np.sin(a)))); tau = R/math.sqrt(2*depth)
    return {"R": R, "depth": depth, "tau": tau, "level": level, "zV": (lambda q: (np.asarray(V2(np.asarray(q, float)[..., 0], np.asarray(q, float)[..., 1]), float) - level)/depth)}


def tip_report(model: dict, bundle: dict) -> dict:
    """Where the selected paths meet and how high the action cone stands there, sheet by sheet.

    The reduced action W is multivalued at the tip: paths that arrive directly, and paths that first go out and are turned back by the outer wall, reach the same point with different W
    (measured on the SM hat at E = 0: 0.4310 and 0.9025 = 0.4310 + 2 x 0.2357).  The selected paths are grouped into sheets by gaps in W; the lowest sheet is the cone.  Heights use the
    natural units of ``natural_units``: each path's cone starts on the surface at its source and rises by W/(V_0 tau_0); the hilltop stands at z_V(top) (1 for a symmetric hat); ``gap`` is
    the mean height of the lowest sheet's tip above the hilltop, in units of the depth.  The convention is stated because action and energy differ by a time.

    :param model: model dict.
    :param bundle: result of ``brim_bundle``.
    :returns: dict ``tip_xy``, ``offset`` (tip to hilltop, brim radii), ``spread`` (rms of the closest-approach points about the tip, brim radii), ``W_tip``, ``W_spread``, ``z_tip``,
              ``z_tip_spread`` (across the sources: zero for a level brim), ``gap``, ``arc_tip``, ``n`` (paths on the lowest sheet), ``sheets`` (list of ``{'W', 'n'}``), ``sheet_of``, ``units``.
    :rtype: dict
    """
    U = natural_units(model); R = U["R"]; top = bundle["hilltop"]; P = bundle["paths"]
    if not P: return {"n": 0}
    qs = np.array([p["closest"]["q_rel"] for p in P]); Ws = np.array([p["closest"]["W"] for p in P]); ss = np.array([p["closest"]["s"] for p in P]); z0 = np.array([float(U["zV"](p["q"][0])) for p in P])
    order = np.argsort(Ws); cut = 0.15*float(np.median(Ws)); sheet = np.zeros(len(Ws), int); k = 0
    for a, b in zip(order[:-1], order[1:]):
        if Ws[b] - Ws[a] > cut: k += 1
        sheet[b] = k
    sheets = [{"W": float(Ws[sheet == i].mean()), "n": int((sheet == i).sum())} for i in range(k + 1)]; low = sheet == 0
    tip = qs[low].mean(0); zt = z0[low] + Ws[low]/(U["depth"]*U["tau"]); ztop = float(U["zV"](top))
    return {"tip_xy": tip, "offset": float(np.hypot(*(tip - top))/R), "spread": float(np.sqrt(np.mean(np.sum((qs[low] - tip)**2, 1)))/R), "W_tip": float(Ws[low].mean()), "W_spread": float(Ws[low].std()),
            "z_tip": float(zt.mean()), "z_tip_spread": float(zt.std()), "z_top": ztop, "gap": float(zt.mean() - ztop), "arc_tip": float(ss[low].mean()), "n": int(low.sum()), "sheets": sheets, "sheet_of": sheet, "units": {k_: v for k_, v in U.items() if k_ != "zV"}}


def cone_tip_height(model: dict, E: float = None) -> dict:
    """The action cone of the radial family in a symmetric hat, exactly: W_tip = integral_0^R sqrt(2 (E - V(r))) dr (E at or above the hilltop value so the tip is reached), the momentum
    at the tip, the natural-unit height and the gap above the hilltop.

    :param model: model dict with ``brim_radius`` and ``depth`` (rotationally symmetric).
    :param E: energy (default the hilltop value).
    :returns: dict ``W_tip``, ``p_tip``, ``z_tip`` (= W/(V_0 tau_0) + z at the brim), ``gap`` (above the hilltop), ``depth``, ``tau``.
    :rtype: dict
    """
    U = natural_units(model); V2, _ = model_plane(model); R = U["R"]; v = lambda r: float(V2(r, 0.0)); E = v(0.0) if E is None else E
    W = integrate.quad(lambda r: math.sqrt(max(2*(E - v(r)), 0.0)), 0, R, epsabs=1e-13, epsrel=1e-13, limit=400)[0]; z = W/(U["depth"]*U["tau"]); ztop = (v(0.0) - U["level"])/U["depth"]
    return {"W_tip": W, "p_tip": math.sqrt(max(2*(E - v(0.0)), 0.0)), "depth": U["depth"], "tau": U["tau"], "z_tip": z, "gap": z - ztop}
