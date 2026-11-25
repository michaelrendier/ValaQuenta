"""
ValaQuenta.modules.aizawa_attractor.maths
=========================================
THE AIZAWA ATTRACTOR ENGINE -- the three-dimensional strange attractor read as a rotation with a radial driver.

    dx/dt = (z - b) x - d y
    dy/dt = d x + (z - b) y
    dz/dt = c + a z - z^3/3 - (x^2 + y^2)(1 + e z) + f z x^3          standard a=.95 b=.7 c=.6 d=3.5 e=.25 f=.1

In cylindrical coordinates (r, phi, z) the first two equations are EXACT:   dr/dt = (z - b) r,   dphi/dt = d.
So the orbit turns about the z axis at the constant rate d while z sets the growth rate of the radius, and r can never reach the axis (r > 0 stays > 0).
Only the term f z x^3 breaks the rotation symmetry; with f = 0 the system is axisymmetric and the 3-D orbit is the 2-D flow in (r, z) swept round the axis.
ESTABLISHED: the equations (Yoji Aizawa's system), Runge-Kutta 4 (order 4), Benettin's Lyapunov method.  CALCULATED here: every identity above, by residuals in the tests.
The JavaScript animation pages that draw it (the 'Holographic Aizawa Attractor' source, local copy only) use these equations with dt 0.0045, burn-in 3000; the slot order x, z, y.

Version: 1.0
"""
from __future__ import annotations
import math
import numpy as np

STANDARD = dict(a=0.95, b=0.70, c=0.60, d=3.50, e=0.25, f=0.10)

def rhs(s, p=STANDARD):
    """The vector field at s = (x, y, z)."""
    x, y, z = s; a, b, c, d, e, f = (p[k] for k in 'abcdef')
    return np.array([(z - b) * x - d * y, d * x + (z - b) * y, c + a * z - z ** 3 / 3 - (x * x + y * y) * (1 + e * z) + f * z * x ** 3])

def rk4_step(s, h, p=STANDARD):
    """One classical Runge-Kutta step (local error O(h^5))."""
    k1 = rhs(s, p); k2 = rhs(s + 0.5 * h * k1, p); k3 = rhs(s + 0.5 * h * k2, p); k4 = rhs(s + h * k3, p)
    return s + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

def orbit(points=20000, burn_in=3000, h=0.0045, p=STANDARD, start=(0.1, 0.0, 0.0)):
    """The orbit after the burn-in: array (points, 3) of (x, y, z)."""
    s = np.array(start, float)
    for _ in range(burn_in): s = rk4_step(s, h, p)
    out = np.empty((points, 3))
    for i in range(points): s = rk4_step(s, h, p); out[i] = s
    return out

def js_layout(xyz, scale=1.0):
    """The animation page's buffer layout: positions[3i] = x, [3i+1] = z, [3i+2] = y (z drawn up), and lineDistances[i] = i / points."""
    n = len(xyz); pos = np.empty((n, 3), np.float32); pos[:, 0] = xyz[:, 0] * scale; pos[:, 1] = xyz[:, 2] * scale; pos[:, 2] = xyz[:, 1] * scale
    return pos.ravel(), (np.arange(n) / n).astype(np.float32)

# ───────────────────────── cylindrical form ─────────────────────────
def cylindrical_rates(s, p=STANDARD):
    """(dr/dt, dphi/dt) computed from the vector field, and the closed forms ((z-b) r, d) for comparison."""
    x, y, z = s; v = rhs(s, p); r = math.hypot(x, y)
    rdot = (x * v[0] + y * v[1]) / r; phidot = (x * v[1] - y * v[0]) / (r * r)
    return (rdot, phidot), ((z - p['b']) * r, p['d'])

def axisymmetric_rhs(rz, p=STANDARD):
    """With f = 0 the dynamics reduce to (r, z):  dr/dt = (z - b) r,  dz/dt = c + a z - z^3/3 - r^2 (1 + e z)."""
    r, z = rz; return np.array([(z - p['b']) * r, p['c'] + p['a'] * z - z ** 3 / 3 - r * r * (1 + p['e'] * z)])

def reduced_orbit(points=5000, burn_in=2000, h=0.0045, p=None, start=(0.1, 0.0)):
    """The 2-D (r, z) orbit of the axisymmetric system (f = 0)."""
    p = dict(STANDARD, f=0.0) if p is None else p; s = np.array(start, float)
    def step(s):
        k1 = axisymmetric_rhs(s, p); k2 = axisymmetric_rhs(s + 0.5 * h * k1, p); k3 = axisymmetric_rhs(s + 0.5 * h * k2, p); k4 = axisymmetric_rhs(s + h * k3, p)
        return s + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    for _ in range(burn_in): s = step(s)
    out = np.empty((points, 2))
    for i in range(points): s = step(s); out[i] = s
    return out

# ───────────────────────── fixed points and the Lyapunov exponent ─────────────────────────
def fixed_points(p=STANDARD):
    """Fixed points sit on the axis (x = y = 0 because (z-b)^2 + d^2 > 0) at the roots of c + a z - z^3/3 = 0.
       Each has eigenvalues (z* - b) +- i d and a - z*^2 (the radial pair spirals, the axial one is real)."""
    roots = np.roots([-1.0 / 3.0, 0.0, p['a'], p['c']]); out = []
    for z in roots:
        if abs(z.imag) < 1e-9:
            z = z.real; out.append(dict(point=(0.0, 0.0, z), eigenvalues=((z - p['b']) + 1j * p['d'], (z - p['b']) - 1j * p['d'], p['a'] - z * z)))
    return out

def lyapunov_max(steps=30000, h=0.0045, p=STANDARD, burn_in=3000, renorm=10, d0=1e-8, start=(0.1, 0.0, 0.0)):
    """Largest Lyapunov exponent by Benettin's two-orbit method."""
    s = np.array(start, float)
    for _ in range(burn_in): s = rk4_step(s, h, p)
    u = s + np.array([d0, 0, 0]); acc = 0.0
    for i in range(1, steps + 1):
        s = rk4_step(s, h, p); u = rk4_step(u, h, p)
        if i % renorm == 0:
            dist = np.linalg.norm(u - s); acc += math.log(dist / d0); u = s + (u - s) * (d0 / dist)
    return acc / (steps * h)

def bounds(xyz):
    """Axis-aligned extent of an orbit."""
    return xyz.min(axis=0), xyz.max(axis=0)
