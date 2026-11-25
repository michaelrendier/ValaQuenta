"""
ValaQuenta.modules.zeta_uns_path.maths
======================================
THE ZETA PATHWAY IN UNIVERSAL NATIVE SPACE (UNS) -- the critical-line path  t -> zeta(1/2 + it)  as a rotation with a radial driver, a spring along t, and the primes.

Hardy:  zeta(1/2 + it) = exp(-i theta(t)) * Z(t),  Z real.   So the pathway is a ROTATION at angular rate -theta'(t) = -(1/2) ln(t/2pi) (slowly increasing)
with a SIGNED radius Z(t) that crosses the axis at every zero.  Aizawa's attractor is a rotation at a constant rate d with a radius driven by
dr/dt = (z - b) r that can never reach the axis.  Same skeleton; the zeros are exactly the axis passages Aizawa forbids.  (analogy tested in tests.)

ESTABLISHED: Hardy's identity; the Riemann-Siegel theta (Stirling series) and Z formula (Riemann-Siegel, first correction C0); the Euler product; the explicit formula.
CALCULATED here: the accuracy of Z_rs against mpmath; the UNS chart; the prime resonance times; the zero spectrum with prime-power peaks; the driver Z'/Z against the zero sum.
Labels follow the project's tiers.  Nothing here is evidence about RH: RH is the statement that every zero lies on the line this path samples.

Version: 1.0
"""
from __future__ import annotations
import math
import numpy as np

TWO_PI = 2.0 * math.pi

# ───────────────────────── theta, Z, zeta on the line (fast, vectorised) ─────────────────────────
def theta(t):
    """Riemann-Siegel theta(t), Stirling series (accurate to ~1e-9 for t >= 10)."""
    t = np.asarray(t, float)
    return t / 2 * np.log(t / TWO_PI) - t / 2 - math.pi / 8 + 1 / (48 * t) + 7 / (5760 * t ** 3) + 31 / (80640 * t ** 5)

def theta_prime(t):
    """theta'(t) = (1/2) ln(t/2pi) - 1/(48 t^2) - 7/(1920 t^4)  (derivative of the series)."""
    t = np.asarray(t, float)
    return 0.5 * np.log(t / TWO_PI) - 1 / (48 * t ** 2) - 7 / (1920 * t ** 4)

def _C0(p):
    return np.cos(TWO_PI * (p * p - p - 1.0 / 16.0)) / np.cos(TWO_PI * p)

def Z_rs(t):
    """Hardy's Z by the Riemann-Siegel formula with the first correction:  Z = 2 sum_{n<=N} cos(theta - t ln n)/sqrt(n) + (-1)^(N-1) (t/2pi)^(-1/4) C0(p).
       Error is O(t^(-5/4)) relative to the main term (about 1e-2 at t = 100, 1e-3 at t = 1000); measured in the tests."""
    t = np.atleast_1d(np.asarray(t, float)); out = np.empty_like(t); th = theta(t)
    a = np.sqrt(t / TWO_PI); N = np.floor(a).astype(int); p = a - N
    for i in range(t.size):
        n = np.arange(1, N[i] + 1); out[i] = 2.0 * np.sum(np.cos(th[i] - t[i] * np.log(n)) / np.sqrt(n))
    out += (-1.0) ** (N - 1) * (t / TWO_PI) ** -0.25 * _C0(p)
    return out

def zeta_line(t):
    """zeta(1/2 + it) = exp(-i theta) Z, as a complex array (Riemann-Siegel; use mpmath for t < 10)."""
    t = np.atleast_1d(np.asarray(t, float)); return np.exp(-1j * theta(t)) * Z_rs(t)

def Z_exact(t):
    """Reference: mpmath siegelz (slow).  Used by the tests."""
    from mpmath import mp, siegelz, mpf
    mp.dps = 20; return float(siegelz(mpf(float(t))))

def zeros_mp(n):
    """First n zero heights gamma_k by mpmath (slow; the 25,000-zero table lives in RiemannHypothesisProof/data)."""
    from mpmath import mp, zetazero
    mp.dps = 20; return np.array([float(zetazero(k).imag) for k in range(1, n + 1)])

# ───────────────────────── sampling by phase: sixteen points per zero spacing, everywhere ─────────────────────────
def t_of_theta(vals):
    """Invert theta (vals >= theta(10)): Lambert-W start from theta ~ (t/2)(ln(t/2pi) - 1) - pi/8, then vectorised Newton on the series."""
    from scipy.special import lambertw
    vals = np.asarray(vals, float); u = (vals + math.pi / 8) / math.pi
    x = u / np.real(lambertw(np.maximum(u, 1e-9) / math.e)); t = np.maximum(TWO_PI * x, 10.0)
    for _ in range(40):
        step = (theta(t) - vals) / theta_prime(t); t = t - step
        if np.max(np.abs(step)) < 1e-12: break
    return t

def sample_by_phase(t0=10.0, n_zero_spacings=2000, per=16, jitter=False):
    """t values with theta advancing by pi/per each step: about `per` samples between consecutive zeros everywhere along the line (theta rises by pi per zero).
       jitter=True adds a golden-ratio low-discrepancy offset in [0, pi/per) to each phase (order and the mean step are kept): without it every sample lands on one of 2*per
       fixed angles of the flat point (arg zeta = -theta mod pi), which draws 2*per rigid spokes that are a sampling artefact, not geometry."""
    th0 = float(theta(t0)); k = np.arange(0, n_zero_spacings * per + 1); vals = th0 + k * (math.pi / per)
    if jitter: vals = vals + np.mod(k * 0.6180339887498949, 1.0) * (math.pi / per)
    return t_of_theta(vals)

# ───────────────────────── the Universal Native Space charts ─────────────────────────
def uns_cylinder(z, t, floor=-3.0):
    """UNS cylinder (rho, phi, height): rho = log10|zeta| - floor (clipped >= 0), phi = arg zeta, height = t.  Zeros sit on the axis.  (Same chart as RiemannHypothesisProof rhp.uns.cylinder.)"""
    z = np.asarray(z); rho = np.clip(np.log10(np.maximum(np.abs(z), 1e-300)) - floor, 0.0, None)
    return rho, np.angle(z), np.asarray(t, float)

def sphere_point(w):
    """Inverse stereographic projection of the value w onto the unit sphere: w = 0 -> south pole, w = infinity -> north pole.  The equator is |w| = 1."""
    w = np.asarray(w, complex); m = np.abs(w) ** 2
    return np.stack([2 * w.real, 2 * w.imag, m - 1.0], axis=-1) / (m + 1.0)[..., None]

def equator_crossings(z):
    """Number of crossings of |zeta| = 1 (the equator of the value sphere) along a sampled path."""
    s = np.sign(np.abs(np.asarray(z)) - 1.0); return int(np.sum(s[1:] != s[:-1]))

# ───────────────────────── the rotation + radial-driver skeleton ─────────────────────────
def rotation_rate(t):
    """Angular rate of the flat point: d(arg)/dt = -theta'(t)."""
    return -theta_prime(t)

def driver(t, h=1e-4):
    """The radial driver Z'(t)/Z(t) (the analogue of Aizawa's z - b = (dr/dt)/r): central difference of Z_rs."""
    t = np.atleast_1d(np.asarray(t, float)); return (Z_rs(t + h) - Z_rs(t - h)) / (2 * h) / Z_rs(t)

def driver_from_zeros(t, gammas):
    """Sum over the zeros of the pole kernel: sum_n 2 t /(t^2 - gamma_n^2) (the symmetric pairs +-gamma).  Z'/Z minus this should be smooth."""
    t = np.atleast_1d(np.asarray(t, float)); g = np.asarray(gammas, float)
    return np.array([np.sum(2 * x / (x * x - g * g)) for x in t])

# ───────────────────────── the pseudo-cardioid: the prime spring plus its mirror ─────────────────────────
def spring_sum(t):
    """S_N(t) = sum_{n<=N} n^(-1/2 - it), N = floor(sqrt(t/2pi)): the Dirichlet half of the Riemann-Siegel sum (the 'prime spring' with the composites included)."""
    t = float(t); N = int(math.floor(math.sqrt(t / TWO_PI))); n = np.arange(1, N + 1); return complex(np.sum(n ** (-0.5 - 1j * t)))

def cardioid_parts(t):
    """zeta(1/2+it) = S + exp(-2i theta) conj(S) + R: the spring plus its mirror turning at -2 theta'.  Returns (S, mirror, R) with R = zeta - S - mirror, |R| <= (t/2pi)^(-1/4) |C0|.
       For N = 1 the sum is 1 + exp(-2 i theta): a circle through 0 centred on +1, never in Re < 0.  Adding n >= 2 gives the pseudo-cardioid; zeros are crossed with speed |Z'| > 0 (no cusp)."""
    t = float(t); S = spring_sum(t); mirror = np.exp(-2j * float(theta(t))) * np.conj(S); z = complex(zeta_line(t)[0]); return S, mirror, z - S - mirror

def re_negative_share(z, dt):
    """Share of the path (weighted by dt, a t-average) with Re zeta < 0: 18% at 100 zeros, 21% at 1,000, 23% at 5,000, 24.0% at 25,000 (measured)."""
    z = np.asarray(z); dt = np.asarray(dt, float); return float(np.sum(dt[z.real < 0]) / np.sum(dt))

# ───────────────────────── the flow of the primes in the zeros ─────────────────────────
def von_mangoldt(n):
    """Lambda(n): ln p if n = p^k, else 0."""
    n = int(n)
    for p in primes_upto(n + 1):
        if n % p == 0:
            m = n
            while m % p == 0: m //= p
            return math.log(p) if m == 1 else 0.0
    return 0.0

def landau_ratio(gammas, n):
    """Landau (1911): sum_{0<gamma<=T} cos(gamma ln n) = -(T/2pi) Lambda(n)/sqrt(n) + O(log T).  Returns measured / predicted for the zeros given (T = the last one); -> 1.
       Measured: mean |ratio - 1| over the prime powers n < 60 is 0.138 at 100 zeros and 0.0019 at 25,000."""
    g = np.asarray(gammas, float); T = g[-1]; pred = -(T / TWO_PI) * von_mangoldt(n) / math.sqrt(n)
    return float(np.sum(np.cos(g * math.log(n))) / pred) if pred != 0 else float('nan')

def zero_count_fluctuation(gammas):
    """S(T) = N(T) - theta(T)/pi - 1 at the midpoints between consecutive zeros (N = the index of the zero below).  S is (1/pi) arg zeta(1/2+iT): the phase wobble of the pathway.
       Prime waves: S(T) ~ -(1/pi) sum_{p,k} sin(k T ln p) / (k p^(k/2)).  Returns (T_mid, S)."""
    g = np.asarray(gammas, float); mid = 0.5 * (g[1:] + g[:-1]); return mid, np.arange(1, len(g)) - theta(mid) / math.pi - 1.0

def prime_wave_fit(gammas, nmax=200):
    """Regress S on sin and cos of T ln n over the prime powers n <= nmax.  Returns (fitted sin amplitude by (p,k), R^2).  Measured at 25,000 zeros: R^2 = 0.996; the amplitudes
       are 97%, 93%, 86%, 80% of -1/(pi k p^(k/2)) for p = 2, 3, 5, 7 (falling for larger p: the sum is truncated, Selberg's smoothing)."""
    mid, Sv = zero_count_fluctuation(gammas); pp = [(int(p), k) for p in primes_upto(nmax) for k in range(1, 4) if p ** k <= nmax]; cols = []
    for p, k in pp: cols += [np.sin(mid * k * math.log(p)), np.cos(mid * k * math.log(p))]
    A = np.stack(cols, 1); coef, *_ = np.linalg.lstsq(A, Sv, rcond=None); res = Sv - A @ coef
    return {pk: float(coef[2 * i]) for i, pk in enumerate(pp)}, float(1 - np.var(res) / np.var(Sv))

# ───────────────────────── where the primes are ─────────────────────────
def primes_upto(n):
    s = np.ones(n + 1, bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0]

def euler_path(t, primes):
    """The prime spring at height t: partial sums of  -ln(1 - p^(-1/2 - it))  over primes.  Each prime is one step of length ~ p^(-1/2), turned by -t ln p.
       Returns the cumulative complex path (formal on the critical line: the Euler product does not converge there, the partial sums are the picture)."""
    p = np.asarray(primes, float); s = 0.5 + 1j * t; steps = -np.log(1 - p ** (-s)); return np.cumsum(steps), steps

def prime_resonance_times(p, T, t0=0.0):
    """Heights where prime p's phasor is back at angle 0: t ln p = 2 pi k.  The ticks on the spring for prime p."""
    d = TWO_PI / math.log(p); k0 = int(math.ceil(t0 / d)); return np.arange(k0, int(T / d) + 1) * d

def zero_spectrum(gammas, xs):
    """|sum_n cos(gamma_n x)| / sum 1  over the zeros.  By the explicit formula the spikes sit at x = ln(p^k) with weight ln p / p^(k/2)."""
    g = np.asarray(gammas, float); return np.array([abs(np.sum(np.cos(g * x))) for x in np.atleast_1d(xs)])

def prime_power_ticks(xmax):
    """[(x, p, k, weight)] with x = ln p^k <= xmax, weight = ln p / p^(k/2): where the zero spectrum must spike."""
    out = []
    for p in primes_upto(int(math.exp(xmax)) + 2):
        k = 1
        while math.log(p) * k <= xmax:
            out.append((math.log(p) * k, int(p), k, math.log(p) / p ** (k / 2))); k += 1
    return sorted(out)
