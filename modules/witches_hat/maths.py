# SPDX-License-Identifier: GPL-3.0-only
r"""
ValaQuenta.modules.witches_hat.maths
====================================
THE WITCH'S HAT ENGINE (core).  A static snapshot of the virtual brim, the hat potential and the paths of action,
adjustable by size and shape.  This core is the tooling: it returns plain data (arrays, dicts) and draws nothing;
renderers (the ``spatial-simulation`` skill: OpenSCAD, Blender, matplotlib) read the snapshot and bridge to whatever
rendering is chosen.

Layers, each labelled where it is used
--------------------------------------
ESTABLISHED  Standard-Model Higgs sector: V(h) = -mu^2 h^2/2 + lam h^4/4, m_h = 125.25 GeV, v = 246.22 GeV.
ESTABLISHED  Classical paths of fixed energy E in a central potential V(r): r-dot^2 = 2(E - V) - L^2/r^2, abbreviated action
             W = integral sqrt(2(E - V)) ds (Maupertuis / Jacobi metric).
ESTABLISHED  Pair correlation of free fermions g_F(r) = 1 - |<psi*psi>|^2 (exchange hole) and of bosons g_B(r) = 1 + |<psi*psi>|^2
             (bunching); the 1-D fermion case g_F(u) = 1 - (sin pi u / pi u)^2 is the sine kernel, which is also the
             Montgomery-Odlyzko pair correlation of the Riemann zeros (Montgomery 1973; Dyson).
THEORETICAL  (the author's reading) the hat potential is the fermion exchange-hole waveform and the bundle of paths from the
             brim to the hilltop is the cone of dynamic action L_dynamic = L_(I|O); the focal point is the one aim at which
             the cone closes on a point.

Units: radius in units of the brim radius r_b, energy in units of the depth V_0 (so V(0) = 0, V(brim) = -1) unless a function
takes ``size`` (r_b) and ``depth`` (V_0) and says so.  Nothing here uses a framework constant.
"""
from __future__ import annotations
import math
import numpy as np

# ------------------------------------------------------------------ Standard-Model numbers (ESTABLISHED)
M_H, VEV = 125.25, 246.22                       # GeV
LAM = M_H**2/(2*VEV**2)
MU2 = LAM*VEV**2

def sm_hat() -> dict:
    """the Higgs hat in physical units: brim radius v (GeV), depth lam v^4/4 (GeV^4), curvatures, boson masses (tree level)"""
    g, gp = 0.6517, 0.3583
    return {"lam": LAM, "mu2": MU2, "brim_radius_GeV": VEV, "depth_GeV4": LAM*VEV**4/4, "Vpp_hilltop": -MU2, "Vpp_brim": 2*MU2,
            "m_W_tree": g*VEV/2, "m_Z_tree": 0.5*VEV*math.hypot(g, gp), "m_h_over_v": M_H/VEV}

# ------------------------------------------------------------------ pair-correlation waveforms
def _j1(x):
    x = np.asarray(x, float); out = np.empty_like(x); s = np.abs(x) < 1e-6
    out[s] = x[s]/2
    xs = x[~s]
    # J1 by its integral representation, accurate to ~1e-12 with 4000 trapezoids over [0, pi]
    t = np.linspace(0, math.pi, 4001)
    out[~s] = np.array([np.trapezoid(np.cos(t - v*np.sin(t)), t)/math.pi for v in xs]) if xs.size else 0
    return out

def pair_correlation(kind: str, u):
    """g(u) for u = k r (k_F r).  kind: fermion1d (sine kernel, u in units of pi), fermion2d, fermion3d, boson.

    :param kind: 'fermion1d', 'fermion2d', 'fermion3d' or 'boson'
    :param u: scaled separation (array)
    :returns: g(u), float array; raises ValueError for an unknown kind
    """
    u = np.asarray(u, float)
    if kind == "fermion1d":                                  # 1 - (sin(pi u)/(pi u))^2, u = k_F r / pi
        x = math.pi*u; s = np.where(np.abs(x) < 1e-9, 1.0, np.sin(x)/np.where(np.abs(x) < 1e-9, 1, x)); return 1 - s**2
    if kind == "fermion2d":
        x = np.where(u == 0, 1e-12, u); return 1 - (2*_j1(x)/x)**2
    if kind == "fermion3d":
        x = np.where(u == 0, 1e-6, u)
        small = x < 0.05                                         # series: (sin x - x cos x)/x^3 = 1/3 - x^2/30 + x^4/840 (the direct form cancels badly)
        f = np.where(small, 1/3 - x**2/30 + x**4/840, (np.sin(x) - x*np.cos(x))/np.where(small, 1.0, x)**3)
        return 1 - 9*f**2
    if kind == "boson":
        return 1 + np.exp(-u**2)
    raise ValueError(kind)

# ------------------------------------------------------------------ hat shapes: V(x), x = r/r_b, V(0) = 0, min = -1 at x = 1
def quartic_family(n):
    """The quartic hat family V(x) = (2 x^n - n x^2)/(n - 2): V(0) = 0, minimum -1 at x = 1; n = 4 is the Standard Model.

    :param n: exponent, n > 2
    :returns: a function V(x) of x = r / r_b
    """
    n = float(n); return lambda x: (2*np.asarray(x, float)**n - n*np.asarray(x, float)**2)/(n - 2)

def _fermion_hat(kind, xmax=6.0):
    u = np.linspace(0, xmax, 24001)
    g = pair_correlation(kind, u)
    # brim = first maximum of g after the hole
    d = np.diff(g); i = np.where((d[:-1] > 0) & (d[1:] <= 0))[0][0] + 1
    u0, gmax = float(u[i]), float(g[i])
    return (lambda x: -np.interp(np.asarray(x, float)*u0, u, g)/gmax), u0, gmax

def hat_shape(shape: str = "quartic", n: float = 4.0):
    """returns V(x) with V(0) = 0 and brim (first minimum) at x = 1, depth 1.
    shapes: quartic (family exponent n; n = 4 is the Standard Model), fermion1d / fermion2d / fermion3d (V = -g_F: the exchange
    hole is the hat; the tail keeps its Friedel-type oscillation), boson (V = -g_B: a well, no hat, for contrast), dog (difference of
    Gaussians, the Mexican-hat wavelet).

    :param shape: 'quartic', 'fermion1d', 'fermion2d', 'fermion3d', 'boson' or 'dog'
    :param n: quartic exponent (used only by 'quartic')
    :returns: (V, meta): the potential function and a dict describing it
    """
    if shape == "quartic": return quartic_family(n), {"shape": shape, "n": n}
    if shape.startswith("fermion"):
        f, u0, gmax = _fermion_hat(shape); return f, {"shape": shape, "brim_u": u0, "g_max": gmax}
    if shape == "boson":
        return (lambda x: -(1 + np.exp(-(np.asarray(x, float)*1.0)**2))/2 + 0.0), {"shape": shape, "note": "well at the centre, no hilltop"}
    if shape == "dog":
        # broad Gaussian (constructive, boson-like bump) minus narrow Gaussian (destructive, fermion-like hole): V = -(broad - narrow)
        f = lambda x: -(np.exp(-np.asarray(x, float)**2/8.0) - np.exp(-np.asarray(x, float)**2/2.0))
        xs = np.linspace(0, 8, 8001); i = int(np.argmin(f(xs))); x0, fm = float(xs[i]), float(f(xs[i]))
        return (lambda x: f(np.asarray(x, float)*x0)/abs(fm)), {"shape": shape, "brim_x": x0}
    raise ValueError(shape)

# ------------------------------------------------------------------ paths in a central potential
def turning_radius(V, psi: float, E: float = 0.0, x0: float = 1.0, nscan: int = 20000):
    """closest approach (units r_b) of a ray leaving the brim x0 at angle psi to the inward radial, energy E (units V_0).
    returns (r_min, regime) where regime in {'point', 'ring', 'reflected', 'through'}

    :param V: potential V(x) in units of V_0
    :param psi: launch angle from the inward radial (rad)
    :param E: energy in units of V_0
    :param x0: launch radius (the brim)
    :param nscan: points of the logarithmic radius scan
    :returns: (r_min, regime)
    """
    k = E - float(V(x0))                                   # kinetic energy at the brim (units V_0)
    if k <= 0: return x0, "stuck"
    L2 = 2*k*(x0*math.sin(psi))**2
    xs = np.logspace(-9, math.log10(x0), nscan)
    f = 2*(E - V(xs)) - L2/xs**2
    inside = np.where((f[1:] > 0) & (f[:-1] <= 0))[0]
    radial = abs(psi) < 1e-5
    if len(inside) == 0:
        return 0.0, "through"
    i = inside[-1]; a, b = xs[i], xs[i + 1]
    for _ in range(80):
        m = 0.5*(a + b); fm = 2*(E - V(m)) - L2/m**2
        if fm > 0: b = m
        else: a = m
    r = 0.5*(a + b)
    if radial: return r, ("reflected" if E < -1e-9 else ("point" if abs(E) <= 1e-9 else "through"))
    return r, "ring"

def trace(V, psi: float, E: float = 0.0, x0: float = 1.0, steps: int = 600, dt_scale: float = 0.02):
    """a path as arrays x, y, z=V(r), W (cumulative abbreviated action), by leapfrog until the closest approach.
    unit mass; speed at the brim sqrt(2(E - V(x0))).

    :param V: potential V(x)
    :param psi: launch angle from the inward radial (rad)
    :param E: energy in units of V_0
    :param x0: launch radius
    :param steps: nominal step count (the loop allows 20 times this)
    :param dt_scale: time step as a fraction of x0 over the brim speed
    :returns: dict with arrays x, y, V, W and the float r_min
    """
    h = 1e-5
    dV = lambda r: (float(V(r + h)) - float(V(max(r - h, 1e-9))))/(r + h - max(r - h, 1e-9))
    v0 = math.sqrt(max(2*(E - float(V(x0))), 0))
    pos = np.array([x0, 0.0]); vel = np.array([-v0*math.cos(psi), v0*math.sin(psi)])
    out = [(pos[0], pos[1], float(V(x0)), 0.0)]; W = 0.0
    dt = dt_scale/max(v0, 1e-6)
    prev_r = x0
    for _ in range(steps*20):
        r = float(np.hypot(*pos)); a = -dV(r)*pos/max(r, 1e-9)
        vel = vel + 0.5*dt*a; pos = pos + dt*vel
        r = float(np.hypot(*pos)); a = -dV(r)*pos/max(r, 1e-9); vel = vel + 0.5*dt*a
        W += float(np.dot(vel, vel))*dt
        out.append((pos[0], pos[1], float(V(r)), W))
        if float(np.dot(pos, vel)) > 0 and r < x0: break             # past closest approach
        prev_r = r
    a = np.array(out); return {"x": a[:, 0], "y": a[:, 1], "V": a[:, 2], "W": a[:, 3], "r_min": float(np.hypot(a[:, 0], a[:, 1]).min())}

# ------------------------------------------------------------------ the snapshot (the core's product)
def snapshot(shape: str = "quartic", n: float = 4.0, size: float = 1.0, depth: float = 1.0, E: float = 0.0,
             aim: float = 0.0, spread: float = 0.3, n_psi: int = 7, n_phi: int = 12, extent: float = 1.4, grid: int = 60) -> dict:
    """a static snapshot of one hat and its bundle.  size = brim radius (physical length unit), depth = V_0 (physical energy unit).
    aim = angle (rad) all rays are rotated from the inward radial: 0 aims at the hilltop; spread = half-width of the launch-angle fan.
    Returns plain data: surface (r, z), brim ring, paths (x, y, z, W per path in physical units), closest approaches, regime, focus.

    :param shape: hat shape name (see hat_shape)
    :param n: quartic exponent
    :param size: brim radius in length units
    :param depth: V_0 in energy units
    :param E: energy in units of V_0
    :param aim: rotation of every ray from the inward radial (rad)
    :param spread: half-width of the launch-angle fan (rad)
    :param n_psi: launch angles in the fan
    :param n_phi: azimuths per launch angle
    :param extent: surface drawn out to this many brim radii
    :param grid: surface sample count
    :returns: dict of plain data (surface, brim, paths, r_min, psi, regime, focus_radius, focus_spread, caustic_ring_radius)
    """
    V, meta = hat_shape(shape, n)
    psis = np.linspace(aim - spread, aim + spread, n_psi)
    paths, rmins, regimes = [], [], []
    for p in psis:
        r_min, reg = turning_radius(V, abs(p), E)
        tr = trace(V, abs(p), E)
        for k in range(n_phi):
            a = 2*math.pi*k/n_phi; c, s = math.cos(a), math.sin(a); sg = 1 if p >= 0 else -1
            paths.append({"psi": float(p), "x": (c*tr["x"] - s*sg*tr["y"])*size, "y": (s*tr["x"] + c*sg*tr["y"])*size, "z": tr["V"]*depth, "W": tr["W"]*size*math.sqrt(depth)})
        rmins.append(r_min); regimes.append(reg)
    rs = np.linspace(0, extent, grid)
    focus = float(np.median(rmins)); spot = float(np.max(rmins) - np.min(rmins))
    regime = "point" if (abs(aim) < 1e-12 and spread < 1e-12 and E >= 0) else regimes[len(regimes)//2]
    return {"meta": meta, "size": size, "depth": depth, "E": E, "aim": aim, "spread": spread,
            "surface_r": rs*size, "surface_z": np.asarray(V(rs))*depth,
            "brim": {"r": size, "z": float(V(1.0))*depth}, "paths": paths, "r_min": np.array(rmins)*size, "psi": psis,
            "regime": regime, "focus_radius": focus*size, "focus_spread": spot*size,
            "caustic_ring_radius": float(turning_radius(V, abs(aim), E)[0])*size}

def focus_resolution(shape: str = "quartic", n: float = 4.0, E: float = 0.0, psi_max: float = 0.4, count: int = 40) -> float:
    """median closest approach of the bundle psi in (0, psi_max], units r_b: the resolution (smaller = tighter)

    :param shape: hat shape name
    :param n: quartic exponent
    :param E: energy in units of V_0
    :param psi_max: largest launch angle (rad)
    :param count: launch angles sampled
    :returns: median closest approach, float, in brim radii
    """
    V, _ = hat_shape(shape, n)
    return float(np.median([turning_radius(V, p, E)[0] for p in np.linspace(psi_max/count, psi_max, count)]))

def defocus_curve(shape: str = "quartic", n: float = 4.0, E: float = 0.0, aims=None) -> dict:
    """caustic ring radius against the aim offset: 0 only at aim = 0 (the point focus); a hollow cone otherwise

    :param shape: hat shape name
    :param n: quartic exponent
    :param E: energy in units of V_0
    :param aims: aim offsets (rad); None means 11 values from 0 to 0.5
    :returns: dict {aim, ring_radius}
    """
    V, _ = hat_shape(shape, n); aims = np.linspace(0, 0.5, 11) if aims is None else np.asarray(aims)
    return {"aim": aims, "ring_radius": np.array([turning_radius(V, a, E)[0] for a in aims])}

def energy_regimes(shape: str = "quartic", n: float = 4.0, energies=(-0.5, -0.1, -0.01, 0.0, 0.1, 0.5), psi: float = 1e-6) -> list:
    """Closest approach and regime of a near-radial ray at each energy.

    :param shape: hat shape name
    :param n: quartic exponent
    :param energies: energies in units of V_0
    :param psi: launch angle (rad), near radial
    :returns: list of dicts {E, r_min, regime}
    """
    V, _ = hat_shape(shape, n)
    return [{"E": e, "r_min": turning_radius(V, psi, e)[0], "regime": turning_radius(V, psi, e)[1]} for e in energies]

# ------------------------------------------------------------------ zeta: Montgomery-Odlyzko pair correlation from zero data
def unfold(gammas):
    """Unfold zero heights to unit mean spacing: N(gamma) = (gamma/2pi) ln(gamma/2pi e) + 7/8.

    :param gammas: zero heights gamma_n > 0
    :returns: float array of unfolded positions
    """
    g = np.asarray(gammas, float); return (g/(2*math.pi))*np.log(g/(2*math.pi*math.e)) + 7.0/8.0

def zeta_pair_correlation(gammas, umax=3.0, bins=60):
    """empirical R2(u) of the unfolded zeros (histogram of all differences up to umax, normalised by N and the bin width)

    :param gammas: zero heights
    :param umax: largest unfolded difference
    :param bins: histogram bins
    :returns: (bin midpoints, R2)
    """
    u = unfold(gammas); N = len(u); counts = np.zeros(bins); edges = np.linspace(0, umax, bins + 1)
    for i in range(N):
        d = u[i + 1:] - u[i]; d = d[d < umax]; counts += np.histogram(d, edges)[0]
    mid = 0.5*(edges[1:] + edges[:-1]); R2 = counts/(N*(edges[1] - edges[0]))        # pairs with positive difference; R2 -> 1 at large u (unit mean spacing)
    return mid, R2

def verify() -> dict:
    """quick closure checks used by the tests"""
    V4, _ = hat_shape("quartic", 4)
    r, _ = turning_radius(V4, 1e-4, 0.0)
    pred = math.sqrt(math.sin(1e-4))*(0.5)**0.25
    return {"focus_closed_form_relerr": abs(r - pred)/pred, "hat_brim": float(V4(1.0)), "hat_top": float(V4(0.0)),
            "sm": sm_hat()}


def shape_table(shapes=("quartic", "fermion1d", "fermion2d", "fermion3d", "dog"), psi_max: float = 0.4) -> list:
    """every shape: depth, hilltop, focus resolution at E = 0, the quartic exponent n that gives the same resolution, and whether
    the shape has an outer wall (rises again beyond the brim) or is a crater (flat or rising to the hilltop level)

    :param shapes: shape names to tabulate
    :param psi_max: largest launch angle for the focus resolution
    :returns: list of dicts, one per shape
    """
    ns = np.linspace(2.05, 40, 600); res = np.array([focus_resolution("quartic", n, 0.0, psi_max) for n in ns]); out = []
    for sh in shapes:
        V, meta = hat_shape(sh, 4); r = focus_resolution(sh, 4, 0.0, psi_max); x = np.linspace(1.0, 4.0, 200)
        out.append({"shape": sh, "V(0)": float(V(0.0)), "V(1)": float(V(1.0)), "V(4)": float(V(4.0)), "resolution": r,
                    "matching_quartic_n": float(ns[np.argmin(abs(res - r))]), "outer_wall": bool(V(4.0) > V(1.0) + 0.5)})
    return out


# ================================================================== the two Lagrangians, kept separate, compared after
PHI = (1 + math.sqrt(5))/2

def lagrangian_sm(mu2: float = None, lam: float = None, vev: float = None) -> dict:
    """STANDARD MODEL hat, ESTABLISHED.  L = |D phi|^2 - V,  V(h) = -mu^2 h^2/2 + lam h^4/4 (h real, vev v).  Defaults: measured m_h, v.

    :param mu2: mu^2; None means lam * VEV^2
    :param lam: quartic coupling; None means the measured value
    :param vev: accepted but not used: the brim radius is sqrt(mu2/lam)
    :returns: model dict with brim_radius, depth, m_over_v, tilt, scale and the function V(r)
    """
    lam = LAM if lam is None else lam; mu2 = (lam*VEV**2 if mu2 is None else mu2)
    v = math.sqrt(mu2/lam); return {"model": "standard_model", "mu2": mu2, "lam": lam, "brim_radius": v, "depth": lam*v**4/4,
                                     "m_over_v": math.sqrt(2*mu2)/v, "tilt": 0.0, "scale": 1.0,
                                     "V": lambda r, mu2=mu2, lam=lam: -0.5*mu2*np.asarray(r, float)**2 + 0.25*lam*np.asarray(r, float)**4}

def lagrangian_vap(mu_sq: float = -1.0, lam: float = 0.5, g: float = 0.01, psi=(1.0, 0.0), convention: str = "ssb") -> dict:
    """THE VAPMIP (monad) LAGRANGIAN, the author's L_NN (ValaQuenta/modules/lagrangian):
        L = (2/pi) oint [ L_kin + L_mat + (1/phi) L_bias + L_coup ],
        L_bias = (1/2) mu^2 beta^2 - (1/4) lam beta^4   (as coded),  L_coup = -(1/phi) g psi.beta  (Yukawa, 1/phi scaled).
    Only L_bias and L_coup depend on the bias field beta, so the potential on the beta-plane is  V_vap = -( (1/phi) L_bias + L_coup ).
    convention 'as_coded':  V = -(1/phi)(mu^2 b^2/2 - lam b^4/4) + (g/phi) psi.b : with the code's default mu^2 = -1 this is a plain bowl (no hat).
    convention 'ssb' (the docstring's intent, 'mu^2 < 0 breaks the symmetry'): V = (1/phi)(mu^2 b^2/2 + lam b^4/4) + (g/phi) psi.b : a hat, brim at sqrt(-mu^2/lam).
    The code's default vev = 1.0 against the brim sqrt(-mu^2/lam) = sqrt(2) at the defaults: a recorded inconsistency, not corrected here.

    :param mu_sq: mu^2 of the bias field
    :param lam: quartic coupling
    :param g: Yukawa-type coupling
    :param psi: the source vector (psi_1, psi_2)
    :param convention: 'ssb' (a hat) or 'as_coded' (the code's sign, a bowl)
    :returns: model dict with V2, grad, brim_radius (None if there is no hat), depth, scale, m_over_v, tilt
    """
    psi = np.asarray(psi, float)
    if convention == "as_coded": a, b = -0.5*mu_sq, 0.25*lam          # V/(1/phi) = -(mu^2/2) r^2 + (lam/4) r^4
    else:                        a, b = 0.5*mu_sq, 0.25*lam
    def V2(x, y, a=a, b=b):
        r2 = np.asarray(x, float)**2 + np.asarray(y, float)**2
        return (a*r2 + b*r2**2 + g*(psi[0]*np.asarray(x, float) + psi[1]*np.asarray(y, float)))/PHI
    def grad(x, y, a=a, b=b):
        r2 = x*x + y*y; f = (2*a + 4*b*r2)/PHI
        return f*x + g*psi[0]/PHI, f*y + g*psi[1]/PHI
    brim = math.sqrt(-a/(2*b)) if (a < 0 < b) else None
    return {"model": "vapmip_" + convention, "mu_sq": mu_sq, "lam": lam, "g": g, "psi": psi, "convention": convention, "V2": V2, "grad": grad,
            "brim_radius": brim, "depth": ((a*a/(4*b))/PHI if brim else None), "scale": 1/PHI,
            "m_over_v": (math.sqrt(-4*a/PHI*1.0)/brim if brim else None), "tilt": g/PHI*float(np.hypot(*psi))}

def model_plane(model: dict):
    """(V2, grad) on the (beta1, beta2) plane for either model (the SM hat is rotationally symmetric)

    :param model: a model dict from lagrangian_sm or lagrangian_vap
    :returns: (V2, grad): the potential and its gradient on the (beta1, beta2) plane
    """
    if "V2" in model: return model["V2"], model["grad"]
    mu2, lam = model["mu2"], model["lam"]
    return (lambda x, y: -0.5*mu2*(np.asarray(x, float)**2 + np.asarray(y, float)**2) + 0.25*lam*(np.asarray(x, float)**2 + np.asarray(y, float)**2)**2,
            lambda x, y: ((-mu2 + lam*(x*x + y*y))*x, (-mu2 + lam*(x*x + y*y))*y))

def hilltop(model: dict):
    """the local maximum of V near the origin (the point the paths aim at): origin for the symmetric hat, shifted by the coupling tilt

    :param model: a model dict from lagrangian_sm or lagrangian_vap
    :returns: numpy array (x, y), found by Newton iteration on the gradient
    """
    V2, grad = model_plane(model); p = np.zeros(2)
    for _ in range(60):
        g = np.array(grad(*p)); h = 1e-5
        Hxx = (grad(p[0] + h, p[1])[0] - grad(p[0] - h, p[1])[0])/(2*h); Hyy = (grad(p[0], p[1] + h)[1] - grad(p[0], p[1] - h)[1])/(2*h)
        p = p - g/np.array([Hxx if abs(Hxx) > 1e-12 else 1e-12, Hyy if abs(Hyy) > 1e-12 else 1e-12])
    return p

def trace_plane(model: dict, start, aim_point, aim: float = 0.0, E: float = None, steps: int = 4000, dt_scale: float = 0.01):
    """leapfrog path in the beta-plane from `start` (on the brim) launched toward `aim_point` rotated by `aim`; unit mass, energy E
    (default: V at the hilltop, the separatrix).  Returns x, y, z=V, W (cumulative abbreviated action = integral p.dq).

    :param model: a model dict from lagrangian_sm or lagrangian_vap
    :param start: (x, y) launch point on the brim
    :param aim_point: (x, y) the point aimed at (the hilltop)
    :param aim: rotation of the launch direction (rad)
    :param E: energy; None means V at the hilltop
    :param steps: maximum steps
    :param dt_scale: time step as a fraction of the start-to-target distance over the launch speed
    :returns: dict with arrays x, y, z, W and the float closest
    """
    V2, grad = model_plane(model); top = np.array(aim_point, float)
    E = float(V2(*top)) if E is None else E
    pos = np.array(start, float); d = top - pos; d = d/np.linalg.norm(d)
    c, s = math.cos(aim), math.sin(aim); d = np.array([c*d[0] - s*d[1], s*d[0] + c*d[1]])
    sp = math.sqrt(max(2*(E - float(V2(*pos))), 0.0)); vel = sp*d
    dt = dt_scale*float(np.linalg.norm(pos - top))/max(sp, 1e-12); out = [(pos[0], pos[1], float(V2(*pos)), 0.0)]; W = 0.0; rmin = np.hypot(*(pos - top)); back = 0
    for _ in range(steps):
        a = np.array(grad(*pos)); vel = vel - 0.5*dt*a; pos = pos + dt*vel; a = np.array(grad(*pos)); vel = vel - 0.5*dt*a
        W += float(vel @ vel)*dt; out.append((pos[0], pos[1], float(V2(*pos)), W))
        r = np.hypot(*(pos - top))
        if r > rmin + 1e-9 and np.dot(pos - top, vel) > 0 and r < np.hypot(*(np.array(start) - top)): break
        rmin = min(rmin, r)
    a = np.array(out); return {"x": a[:, 0], "y": a[:, 1], "z": a[:, 2], "W": a[:, 3], "closest": float(rmin)}

def snapshot_plane(model: dict, aim: float = 0.0, aims=(-0.3, -0.15, 0.0, 0.15, 0.3), n_start: int = 12, extent: float = 1.4, grid: int = 70) -> dict:
    """a static 2-D snapshot for either Lagrangian: the surface z = V(beta1, beta2), the brim ring, the hilltop, and the bundle of paths
    from n_start brim points x len(aims) aim offsets toward the hilltop.  Plain data.

    :param model: a model dict from lagrangian_sm or lagrangian_vap
    :param aim: common aim rotation (rad)
    :param aims: aim offsets added to it, one path set each
    :param n_start: launch points around the brim
    :param extent: surface drawn out to this many brim radii
    :param grid: surface sample count
    :returns: dict of plain data (X, Y, Z, ring, ring_z, hilltop, E, paths)
    """
    V2, _ = model_plane(model); R = model["brim_radius"]; top = hilltop(model); E = float(V2(*top))
    xs = np.linspace(-extent*R, extent*R, grid); X, Y = np.meshgrid(xs, xs)
    th = np.linspace(0, 2*math.pi, 200); ring = np.stack([R*np.cos(th), R*np.sin(th)], 1)
    paths = []
    for k in range(n_start):
        a = 2*math.pi*k/n_start; st = (R*math.cos(a), R*math.sin(a))
        for off in aims:
            p = trace_plane(model, st, top, aim + off, E); p["aim"] = aim + off; paths.append(p)
    return {"model": model["model"], "brim_radius": R, "depth": model["depth"], "hilltop": top, "E": E, "X": X, "Y": Y, "Z": V2(X, Y),
            "ring": ring, "ring_z": V2(ring[:, 0], ring[:, 1]), "paths": paths}

def l_io_action(model: dict, psis=None) -> dict:
    """L_(I|O) read as the action of the actual path against the stationary straight one (the canonical form: L_(I|O) - L = -psi_Fermat,
    the bent path's functional minus the straight one).  W(aim) = integral p.dq along the path to its closest approach to the hilltop;
    dW = W(aim) - W(0).  This is the identification used here (THEORETICAL); J_red.J_blue is not separately defined in code.

    :param model: a model dict from lagrangian_sm or lagrangian_vap
    :param psis: aim angles (rad); None means 9 values from 0 to 0.4
    :returns: dict {aim, W, dW}
    """
    psis = np.linspace(0, 0.4, 9) if psis is None else np.asarray(psis); V2, _ = model_plane(model); top = hilltop(model); R = model["brim_radius"]
    W = []
    for a in psis:
        p = trace_plane(model, (R, 0.0), top, float(a), None); W.append(p["W"][-1])
    W = np.array(W); return {"aim": psis, "W": W, "dW": W - W[0]}

def compare(sm=None, vap=None) -> dict:
    """the two Lagrangians side by side, in their own units and in the normalised chart (brim radius 1, depth 1)

    :param sm: Standard Model model dict; None builds the default
    :param vap: VAPMIP model dict; None builds the 'ssb' default
    :returns: dict of the two models' numbers side by side
    """
    sm = sm or lagrangian_sm(); vap = vap or lagrangian_vap(convention="ssb")
    out = {}
    for m in (sm, vap):
        out[m["model"]] = {k: m[k] for k in ("brim_radius", "depth", "m_over_v", "tilt", "scale")}
        out[m["model"]]["focus_resolution"] = focus_resolution("quartic", 4)           # both are exact quartics: the normalised shape is identical
    out["as_coded_is_a_bowl"] = lagrangian_vap(convention="as_coded")["brim_radius"] is None
    out["code_default_vev_vs_brim"] = {"vev_default": 1.0, "brim": vap["brim_radius"]}
    return out
