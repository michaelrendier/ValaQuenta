# SPDX-License-Identifier: GPL-3.0-only
"""
ValaQuenta.modules.ptycho_weak_lensing.maths
============================================
Weak gravitational lensing, forward and inverse, plus a ptychographic (overlapping-pointing)
reconstruction of the convergence κ.   :CALCULATED unless marked ESTABLISHED.

Orientation (observer-position): flat-sky tangent plane, native object = a SPIN-2 field.
Array index [iy, ix]; pixel size ``dx``; wavenumbers k = 2π·fftfreq.  Spin-2 fields are stored as complex
arrays  f = f₁ + i f₂  (shear γ, ellipticity ε, polarization Q+iU); they turn by 2φ when the axes turn by φ.

ESTABLISHED (Kaiser & Squires 1993; Bartelmann & Schneider 2001; Seitz & Schneider 2001):
    ∇²ψ = 2κ            γ = γ₁ + iγ₂ ,  γ₁ = ½(ψ₁₁ − ψ₂₂),  γ₂ = ψ₁₂
    γ̂(k) = D(k) κ̂(k),   D = (k₁² − k₂² + 2 i k₁k₂)/|k|²   (|D| = 1 for k ≠ 0; D(0) := 0)   κ̂ = D* γ̂
    g = γ/(1 − κ)       μ = 1/((1−κ)² − |γ|²)       ε = (ε_s + g)/(1 + g* ε_s)  for |g| < 1
    mass-sheet degeneracy:  κ → λκ + (1−λ) leaves g unchanged (k = 0 is not measured by shear)

PTYCHOGRAPHY (this engine's reading, THEORETICAL): a *pointing* is a probe window W_j placed at a position in the field;
the object is the one real field κ; the overlap redundancy is that every pointing constrains the same κ, and the object
constraint is "B-mode = 0, κ real".  The iteration is an ePIE / Kaczmarz update over pointings.
"""
from __future__ import annotations
import math
import numpy as np

# ----------------------------------------------------------------------------- grids and the spin-2 operator
def kgrid(n, dx=1.0):
    """Angular wavenumber grids (KX along axis 1, KY along axis 0).

    :param n: pixels per side
    :param dx: pixel size
    :returns: (KX, KY)
    """
    k = 2 * np.pi * np.fft.fftfreq(n, d=dx)
    return np.meshgrid(k, k)          # KX (axis 1), KY (axis 0)

def D_kernel(n, dx=1.0):
    """D(k) = (k₁² − k₂² + 2ik₁k₂)/|k|², D(0) = 0.

    :param n: pixels per side
    :param dx: pixel size
    :returns: the result (see summary)
    """
    KX, KY = kgrid(n, dx); k2 = KX ** 2 + KY ** 2; k2[0, 0] = 1.0
    D = (KX ** 2 - KY ** 2 + 2j * KX * KY) / k2; D[0, 0] = 0.0
    return D

def pad_to(a, factor=2):
    """Zero-pad a square array to ``factor`` times its size, centred.

    :param a: first array / field
    :param factor: padding factor
    :returns: (padded array, offset)
    """
    n = a.shape[0]; m = n * factor; out = np.zeros((m, m), a.dtype); o = (m - n) // 2
    out[o:o + n, o:o + n] = a; return out, o

def crop(a, o, n):
    """Undo ``pad_to``.

    :param a: first array / field
    :param o: padding offset
    :param n: pixels per side
    :returns: the cropped array
    """
    return a[o:o + n, o:o + n]

def kappa_to_gamma(kappa, dx=1.0, pad=2):
    """γ = D κ (FFT; zero-padded by ``pad`` to suppress periodic wrap). The mean of κ is the mass sheet and is not seen.

    :param kappa: convergence map κ
    :param dx: pixel size
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    n = kappa.shape[0]; kp, o = pad_to(kappa.astype(float), pad)
    g = np.fft.ifft2(D_kernel(kp.shape[0], dx) * np.fft.fft2(kp)); return crop(g, o, n)

def kappa_to_psi(kappa, dx=1.0, pad=2):
    """ψ from ∇²ψ = 2κ (k = 0 dropped).

    :param kappa: convergence map κ
    :param dx: pixel size
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    n = kappa.shape[0]; kp, o = pad_to(kappa.astype(float), pad); KX, KY = kgrid(kp.shape[0], dx)
    k2 = KX ** 2 + KY ** 2; k2[0, 0] = 1.0; ph = -2 * np.fft.fft2(kp) / k2; ph[0, 0] = 0
    return crop(np.fft.ifft2(ph).real, o, n)

def gamma_to_kappa(gamma, dx=1.0, pad=2):
    """Kaiser–Squires: κ_E + iκ_B = D* γ  (returns the complex pair).

    :param gamma: complex shear field γ₁ + iγ₂
    :param dx: pixel size
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    n = gamma.shape[0]; gp, o = pad_to(gamma.astype(complex), pad)
    k = np.fft.ifft2(np.conj(D_kernel(gp.shape[0], dx)) * np.fft.fft2(gp)); return crop(k, o, n)

def eb_decompose(f, dx=1.0, pad=2):
    """E and B scalar maps of ANY spin-2 field (shear, ellipticity, Q+iU): (E, B) = Re, Im of D* f.

    :param f: complex spin-2 field
    :param dx: pixel size
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    k = gamma_to_kappa(f, dx, pad); return k.real, k.imag

# ----------------------------------------------------------------------------- lensing observables
def reduced_shear(gamma, kappa):
    """g = γ/(1 − κ).

    :param gamma: complex shear field γ₁ + iγ₂
    :param kappa: convergence map κ
    :returns: the result (see summary)
    """
    return gamma / (1.0 - kappa)

def magnification(kappa, gamma):
    """μ = 1/((1−κ)² − |γ|²).

    :param kappa: convergence map κ
    :param gamma: complex shear field γ₁ + iγ₂
    :returns: the result (see summary)
    """
    return 1.0 / ((1.0 - kappa) ** 2 - np.abs(gamma) ** 2)

def apply_shear(eps_s, g):
    """exact: ε = (ε_s + g)/(1 + g* ε_s), |g| < 1.

    :param eps_s: intrinsic ellipticity (complex)
    :param g: reduced shear (complex)
    :returns: the result (see summary)
    """
    return (eps_s + g) / (1.0 + np.conj(g) * eps_s)

def tangential_cross(gamma, centre, dx=1.0):
    """(γ_t, γ_×, r) about ``centre`` (x, y in pixels):  γ_t = −Re(γ e^{−2iφ}),  γ_× = −Im(γ e^{−2iφ}).

    :param gamma: complex shear field γ₁ + iγ₂
    :param centre: (x, y) centre in pixels
    :param dx: pixel size
    :returns: the result (see summary)
    """
    n = gamma.shape[0]; y, x = np.indices(gamma.shape).astype(float)
    dxp, dyp = x - centre[0], y - centre[1]; phi = np.arctan2(dyp, dxp); r = np.hypot(dxp, dyp) * dx
    q = -gamma * np.exp(-2j * phi); return q.real, q.imag, r

def radial_profile(a, r, edges):
    """Mean of ``a`` in radial bins.

    :param a: first array / field
    :param r: radius map or radii
    :param edges: bin edges
    :returns: the result (see summary)
    """
    idx = np.digitize(r.ravel(), edges) - 1; v = a.ravel(); out = np.full(len(edges) - 1, np.nan)
    for i in range(len(edges) - 1):
        m = idx == i
        if m.any(): out[i] = v[m].mean()
    return out

# ----------------------------------------------------------------------------- halos
def nfw_kappa(shape, centre, kappa_s, r_s, dx=1.0, r_cut=None):
    """projected NFW (Bartelmann 1996):  κ = 2κ_s (1 − F(x))/(x² − 1),  x = r/r_s;  κ(1) = 2κ_s/3.  Optional smooth truncation r_cut.

    :param shape: (ny, nx)
    :param centre: (x, y) centre in pixels
    :param kappa_s: NFW characteristic convergence κ_s
    :param r_s: NFW scale radius
    :param dx: pixel size
    :param r_cut: smooth truncation radius
    :returns: the result (see summary)
    """
    y, x = np.indices(shape).astype(float); r = np.hypot(x - centre[0], y - centre[1]) * dx; xx = np.maximum(r / r_s, 1e-6)
    out = np.empty_like(xx); lo = xx < 1 - 1e-6; hi = xx > 1 + 1e-6; mid = ~(lo | hi)
    F_lo = np.arccosh(1 / xx[lo]) / np.sqrt(1 - xx[lo] ** 2); F_hi = np.arccos(1 / xx[hi]) / np.sqrt(xx[hi] ** 2 - 1)
    out[lo] = 2 * kappa_s * (1 - F_lo) / (xx[lo] ** 2 - 1); out[hi] = 2 * kappa_s * (1 - F_hi) / (xx[hi] ** 2 - 1); out[mid] = 2 * kappa_s / 3
    if r_cut: out *= np.exp(-(r / r_cut) ** 4)
    return out

def gaussian_kappa(shape, centre, amp, sigma, dx=1.0):
    """Gaussian convergence profile.

    :param shape: (ny, nx)
    :param centre: (x, y) centre in pixels
    :param amp: peak amplitude of κ
    :param sigma: Gaussian width
    :param dx: pixel size
    :returns: the result (see summary)
    """
    y, x = np.indices(shape).astype(float); r2 = ((x - centre[0]) ** 2 + (y - centre[1]) ** 2) * dx ** 2
    return amp * np.exp(-r2 / (2 * sigma ** 2))

def gaussian_gamma_t(r, amp, sigma):
    """exact axisymmetric result γ_t(r) = κ̄(<r) − κ(r),  κ̄ = 2A σ²(1 − e^{−r²/2σ²})/r².

    :param r: radius map or radii
    :param amp: peak amplitude of κ
    :param sigma: Gaussian width
    :returns: the result (see summary)
    """
    r = np.maximum(r, 1e-9); kb = 2 * amp * sigma ** 2 * (1 - np.exp(-r ** 2 / (2 * sigma ** 2))) / r ** 2
    return kb - amp * np.exp(-r ** 2 / (2 * sigma ** 2))

def merging_cluster(n=128, dx=1.0, separation=0.35, kappa_s=(0.18, 0.10), r_s=(10.0, 7.0)):
    """two NFW halos on the x axis (a bullet-like synthetic merger) — κ_true.

    :param n: pixels per side
    :param dx: pixel size
    :param separation: halo separation as a fraction of the field
    :param kappa_s: NFW characteristic convergence κ_s
    :param r_s: NFW scale radius
    :returns: the result (see summary)
    """
    c = n / 2; s = separation * n / 2
    k = nfw_kappa((n, n), (c - s, c), kappa_s[0], r_s[0], dx, r_cut=0.45 * n * dx) + nfw_kappa((n, n), (c + s, c), kappa_s[1], r_s[1], dx, r_cut=0.45 * n * dx)
    return k

# ----------------------------------------------------------------------------- cosmology (flat ΛCDM, numeric)
def _E(z, Om): return math.sqrt(Om * (1 + z) ** 3 + 1 - Om)

_trap = getattr(np, "trapezoid", None) or getattr(np, "trapz")

def comoving_distance(z, H0=70.0, Om=0.3, n=2000):
    """Comoving distance in Mpc (flat ΛCDM, trapezoid).

    :param z: redshift
    :param H0: Hubble constant, km/s/Mpc
    :param Om: matter density parameter Ω_m (flat ΛCDM)
    :param n: pixels per side
    :returns: the result (see summary)
    """
    zz = np.linspace(0, z, n); f = 1.0 / np.sqrt(Om * (1 + zz) ** 3 + 1 - Om); return 299792.458 / H0 * _trap(f, zz)

def angular_diameter_distance(z1, z2=None, H0=70.0, Om=0.3):
    """D_A(z1, z2) in Mpc, flat universe.

    :param z1: first redshift
    :param z2: second redshift (None = to the observer)
    :param H0: Hubble constant, km/s/Mpc
    :param Om: matter density parameter Ω_m (flat ΛCDM)
    :returns: the result (see summary)
    """
    if z2 is None: return comoving_distance(z1, H0, Om) / (1 + z1)
    return (comoving_distance(z2, H0, Om) - comoving_distance(z1, H0, Om)) / (1 + z2)

def lensing_efficiency(z_l, z_s, H0=70.0, Om=0.3):
    """β = D_ls / D_s  (κ and γ of a source at z_s are β/β_∞ times those at infinity).

    :param z_l: lens redshift
    :param z_s: source redshift
    :param H0: Hubble constant, km/s/Mpc
    :param Om: matter density parameter Ω_m (flat ΛCDM)
    :returns: the result (see summary)
    """
    if z_s <= z_l: return 0.0
    return angular_diameter_distance(z_l, z_s, H0, Om) / angular_diameter_distance(z_s, None, H0, Om)

def sigma_crit(z_l, z_s, H0=70.0, Om=0.3):
    """Σ_cr = c² D_s/(4πG D_l D_ls) in M☉/Mpc².

    :param z_l: lens redshift
    :param z_s: source redshift
    :param H0: Hubble constant, km/s/Mpc
    :param Om: matter density parameter Ω_m (flat ΛCDM)
    :returns: the result (see summary)
    """
    c2_over_4piG = 1.6625e18  # M☉/Mpc : c²/(4πG)
    Dl = angular_diameter_distance(z_l, None, H0, Om); Ds = angular_diameter_distance(z_s, None, H0, Om); Dls = angular_diameter_distance(z_l, z_s, H0, Om)
    return c2_over_4piG * Ds / (Dl * Dls)

# ----------------------------------------------------------------------------- catalogues
def mock_catalogue(kappa, n_per_pix, sigma_e=0.26, dx=1.0, rng=None, window=None, efficiency=1.0, shear_bias=(0.0, 0.0)):
    """Galaxies on the field: N ~ Poisson(n_per_pix · pixels · window). The true reduced shear is interpolated bilinearly.
    ``efficiency`` scales κ,γ (source redshift); ``shear_bias`` = (m, c): ε_meas = (1+m)·ε + c (calibration test).

    :param kappa: convergence map κ
    :param n_per_pix: mean galaxies per pixel
    :param sigma_e: intrinsic ellipticity dispersion per component
    :param dx: pixel size
    :param rng: numpy random Generator
    :param window: galaxy-selection window map
    :param efficiency: source-plane efficiency η = D_ls/D_s scaling κ and γ
    :param shear_bias: (m, c): ε_meas = (1+m)ε + c
    :returns: the result (see summary)
    """
    rng = rng or np.random.default_rng(0); n = kappa.shape[0]
    gam = efficiency * kappa_to_gamma(kappa, dx); kap = efficiency * kappa; g = reduced_shear(gam, kap)
    w = np.ones_like(kappa) if window is None else window
    ngal = rng.poisson(float(n_per_pix * w.sum())); p = (w / w.sum()).ravel()
    pix = rng.choice(w.size, size=ngal, p=p); iy, ix = np.divmod(pix, n); fy = iy + rng.random(ngal); fx = ix + rng.random(ngal)
    gi = _bilinear(g, fx, fy)
    es = rng.normal(0, sigma_e, ngal) + 1j * rng.normal(0, sigma_e, ngal); big = np.abs(es) >= 0.95; es[big] *= 0.95 / np.abs(es[big])
    e = apply_shear(es, gi); m, c = shear_bias; e = (1 + m) * e + c
    return {"x": fx, "y": fy, "e": e, "sigma_e": sigma_e, "n": n, "dx": dx}

def _bilinear(a, x, y):
    n = a.shape[0]; x = np.clip(x - 0.5, 0, n - 1.001); y = np.clip(y - 0.5, 0, n - 1.001)
    x0 = x.astype(int); y0 = y.astype(int); fx = x - x0; fy = y - y0
    return (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy) + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)

def gauss_smooth(a, sigma_pix):
    """Gaussian smoothing in Fourier space.

    :param a: first array / field
    :param sigma_pix: Gaussian width in pixels
    :returns: the result (see summary)
    """
    if sigma_pix <= 0: return a
    n = a.shape[0]; k = 2 * np.pi * np.fft.fftfreq(n); K2 = k[None, :] ** 2 + k[:, None] ** 2
    return np.fft.ifft2(np.fft.fft2(a) * np.exp(-K2 * sigma_pix ** 2 / 2)).real if not np.iscomplexobj(a) else \
        np.fft.ifft2(np.fft.fft2(a) * np.exp(-K2 * sigma_pix ** 2 / 2))

def grid_catalogue(cat, smooth=2.0):
    """(ε map, count map): the smoothed mean ellipticity per pixel and the smoothed galaxy density.

    :param cat: catalogue dict from ``mock_catalogue``
    :param smooth: Gaussian smoothing in pixels
    :returns: the result (see summary)
    """
    n = cat["n"]; ix = np.clip(cat["x"].astype(int), 0, n - 1); iy = np.clip(cat["y"].astype(int), 0, n - 1)
    cnt = np.zeros((n, n)); es = np.zeros((n, n), complex)
    np.add.at(cnt, (iy, ix), 1.0); np.add.at(es, (iy, ix), cat["e"])
    c = gauss_smooth(cnt, smooth); s = gauss_smooth(es, smooth)
    with np.errstate(invalid="ignore", divide="ignore"): emap = np.where(c > 1e-3, s / np.maximum(c, 1e-3), 0.0)
    return emap, c

def ks_map(cat, smooth=2.0, iterations=3, dx=1.0, pad=2):
    """Kaiser–Squires with the reduced-shear correction  γ = g(1 − κ)  iterated.  Returns (κ_E, κ_B).

    :param cat: catalogue dict from ``mock_catalogue``
    :param smooth: Gaussian smoothing in pixels
    :param iterations: reduced-shear iterations
    :param dx: pixel size
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    emap, c = grid_catalogue(cat, smooth); kap = np.zeros(emap.shape); kb = np.zeros(emap.shape)
    for _ in range(max(1, iterations)):
        gam = emap * (1 - kap); k = gamma_to_kappa(gam, dx, pad); kap, kb = k.real, k.imag
    return kap, kb

# ----------------------------------------------------------------------------- controls
def rotate45(cat):
    """every galaxy rotated by 45° (ε → iε): a real lens signal must vanish in κ_E.

    :param cat: catalogue dict from ``mock_catalogue``
    :returns: the result (see summary)
    """
    out = dict(cat); out["e"] = 1j * cat["e"]; return out

def shuffle_orientation(cat, rng=None):
    """Randomly permute the galaxies' ellipticities (null test).

    :param cat: catalogue dict from ``mock_catalogue``
    :param rng: numpy random Generator
    :returns: the result (see summary)
    """
    rng = rng or np.random.default_rng(1); out = dict(cat); out["e"] = cat["e"][rng.permutation(len(cat["e"]))]; return out

def mass_sheet(kappa, lam):
    """κ → λκ + (1 − λ): g is unchanged.

    :param kappa: convergence map κ
    :param lam: mass-sheet scale λ
    :returns: the result (see summary)
    """
    return lam * kappa + (1 - lam)

def calibrate_shear(n=96, gamma_in=(0.03, 0.0), n_per_pix=8.0, sigma_e=0.26, bias=(0.05, 0.002), seed=3):
    """Inject a constant shear and a known (m, c) and recover them — the multiplicative/additive bias test.

    :param n: pixels per side
    :param gamma_in: (γ₁, γ₂) injected constant shear
    :param n_per_pix: mean galaxies per pixel
    :param sigma_e: intrinsic ellipticity dispersion per component
    :param bias: (m, c) injected shear bias
    :param seed: random seed
    :returns: the result (see summary)
    """
    rng = np.random.default_rng(seed); g = complex(*gamma_in); tot = 0; N = int(n * n * n_per_pix)
    es = rng.normal(0, sigma_e, N) + 1j * rng.normal(0, sigma_e, N); e = apply_shear(es, g); m, c = bias; e = (1 + m) * e + c
    est = e.mean(); err = sigma_e / math.sqrt(N)
    m_rec = (est.real - c) / g.real - 1.0
    return {"gamma_in": gamma_in, "m_in": m, "c_in": c, "mean_e": (est.real, est.imag), "m_recovered": m_rec, "stat_error_on_gamma": err, "N": N}

def compare_maps(true, rec, mask=None):
    """Correlation, rms, and peak offset of a recovered map against the truth.

    :param true: true map
    :param rec: recovered map
    :param mask: boolean region to score
    :returns: the result (see summary)
    """
    m = np.ones_like(true, bool) if mask is None else mask; t = true[m] - true[m].mean(); r = rec[m] - rec[m].mean()
    corr = float((t * r).sum() / math.sqrt((t ** 2).sum() * (r ** 2).sum() + 1e-300)); rms = float(np.sqrt(np.mean((t - r) ** 2)))
    pt = np.unravel_index(np.argmax(true), true.shape); pr = np.unravel_index(np.argmax(np.where(m, rec, -1e9)), rec.shape)
    return {"corr": corr, "rms": rms, "peak_true": tuple(int(v) for v in pt), "peak_rec": tuple(int(v) for v in pr),
            "peak_offset_pix": float(math.hypot(pt[0] - pr[0], pt[1] - pr[1]))}

# ----------------------------------------------------------------------------- the ptychographic part
def tile_windows(n, tile, step, taper=4):
    """overlapping square pointings: [(y0, x0, W)], W a cosine-tapered window of side ``tile`` placed in an n×n field.

    :param n: pixels per side
    :param tile: pointing side in pixels
    :param step: pointing step in pixels
    :param taper: cosine taper width in pixels
    :returns: the result (see summary)
    """
    out = []; ramp = np.ones(tile)
    t = min(taper, tile // 2)
    if t > 0:
        r = 0.5 * (1 - np.cos(np.pi * (np.arange(t) + 0.5) / t)); ramp[:t] = r; ramp[-t:] = r[::-1]
    w2 = np.outer(ramp, ramp)
    for y0 in range(0, n - tile + 1, step):
        for x0 in range(0, n - tile + 1, step):
            W = np.zeros((n, n)); W[y0:y0 + tile, x0:x0 + tile] = w2; out.append((y0, x0, W))
    return out

def simulate_pointings(kappa, windows, n_per_pix, efficiencies=None, sigma_e=0.26, dx=1.0, smooth=1.5, seed=0, skip=()):
    """one catalogue per pointing (own window, own source efficiency, own density). ``skip`` = indices left unobserved (gaps).

    :param kappa: convergence map κ
    :param windows: list of (y0, x0, W) pointings
    :param n_per_pix: mean galaxies per pixel
    :param efficiencies: source efficiencies η_j cycled over pointings
    :param sigma_e: intrinsic ellipticity dispersion per component
    :param dx: pixel size
    :param smooth: Gaussian smoothing in pixels
    :param seed: random seed
    :param skip: indices of unobserved pointings
    :returns: the result (see summary)
    """
    rng = np.random.default_rng(seed); data = []
    for j, (y0, x0, W) in enumerate(windows):
        if j in skip: continue
        eff = 1.0 if efficiencies is None else efficiencies[j % len(efficiencies)]
        cat = mock_catalogue(kappa, n_per_pix, sigma_e, dx, rng, window=W, efficiency=eff)
        emap, cnt = grid_catalogue(cat, smooth); data.append({"j": j, "W": W, "eff": eff, "e": emap, "count": cnt, "cat": cat})
    return data

def naive_mosaic(data, dx=1.0, iterations=3, pad=2):
    """stack all pointings (weighted by galaxy counts, rescaled by efficiency) and apply Kaiser–Squires once.

    :param data: list of pointing dicts from ``simulate_pointings``
    :param dx: pixel size
    :param iterations: reduced-shear iterations
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    num = sum(d["count"] * d["e"] / max(d["eff"], 1e-6) for d in data); den = sum(d["count"] for d in data)
    emap = np.where(den > 1e-3, num / np.maximum(den, 1e-3), 0.0); kap = np.zeros(emap.shape); kb = kap
    for _ in range(iterations):
        k = gamma_to_kappa(emap * (1 - kap), dx, pad); kap, kb = k.real, k.imag
    return kap, kb

def ptycho_reconstruct(data, n_iter=60, alpha=0.9, dx=1.0, pad=2, seed=0, smooth_final=1.0, track=None):
    """ePIE-style / Kaczmarz over pointings, κ real:  for each pointing j (random order)

      model = η_j · D κ ;  R = M_j (ε_j − model(1−η_jκ)) ;  κ ← κ + α · Re[D* R]/η_j,   M_j = count-weight · window

    where M_j is normalised by the field's total weight (the ePIE |P|² denominator).  The real part is the object constraint
    (B = 0); the pointings' overlap is the redundancy.  Returns (κ, history of the data-consistency χ², final B-mode leak).

    :param data: list of pointing dicts from ``simulate_pointings``
    :param n_iter: number of sweeps
    :param alpha: update step 0 < α ≤ 1
    :param dx: pixel size
    :param pad: zero-padding factor
    :param seed: random seed
    :param smooth_final: final smoothing in pixels
    :param track: optional callback (iteration, κ)
    :returns: the result (see summary)
    """
    rng = np.random.default_rng(seed); n = data[0]["e"].shape[0]; kap = np.zeros((n, n)); hist = []
    wsum = sum(d["count"] for d in data); wmax = max(wsum.max(), 1e-9)
    for it in range(n_iter):
        chi = 0.0
        for j in rng.permutation(len(data)):
            d = data[j]; eta = max(d["eff"], 1e-6); M = d["count"] / wmax
            gam = eta * kappa_to_gamma(kap, dx, pad); model = gam / (1 - eta * kap)
            R = M * (d["e"] - model); chi += float(np.sum(d["count"] * np.abs(d["e"] - model) ** 2 * (d["count"] > 1e-3)))
            kap = kap + alpha * gamma_to_kappa(R, dx, pad).real / eta / np.maximum(M.max(), 1e-9) * M.max()
        hist.append(chi)
        if track is not None: track(it, kap)
    out = gauss_smooth(kap, smooth_final) if smooth_final else kap
    emap_final = sum(d["count"] * d["e"] / max(d["eff"], 1e-6) for d in data) / np.maximum(wsum, 1e-3)
    _, B = eb_decompose(emap_final, dx, pad)
    return out, hist, float(np.sqrt(np.mean(B ** 2)))

def overlap_error(data):
    """pairwise disagreement of overlapping pointings' (efficiency-rescaled) ε maps where both have counts: the ptychographic overlap check.

    :param data: list of pointing dicts from ``simulate_pointings``
    :returns: the result (see summary)
    """
    errs = []
    for a in range(len(data)):
        for b in range(a + 1, len(data)):
            m = (data[a]["count"] > 0.5) & (data[b]["count"] > 0.5)
            if m.sum() > 20: errs.append(float(np.sqrt(np.mean(np.abs(data[a]["e"][m] / data[a]["eff"] - data[b]["e"][m] / data[b]["eff"]) ** 2))))
    return float(np.mean(errs)) if errs else float("nan")

def modulus_ptycho(E_modulus, kappa0, n_iter=200, dx=1.0, pad=2):
    """INTENSITY-ONLY variant (the genuine phase-retrieval case): only |γ| is known (orientation lost). Gerchberg–Saxton:
    κ → γ = Dκ → keep the phase, impose the measured modulus → κ = Re D*γ.   Sign of κ is fixed by the starting guess κ0.

    :param E_modulus: measured shear modulus |γ| (orientation lost)
    :param kappa0: starting guess for κ
    :param n_iter: number of sweeps
    :param dx: pixel size
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    kap = kappa0.copy(); res = []
    for _ in range(n_iter):
        gam = kappa_to_gamma(kap, dx, pad); ph = gam / np.maximum(np.abs(gam), 1e-12)
        gam = E_modulus * ph; kap = gamma_to_kappa(gam, dx, pad).real
        res.append(float(np.sqrt(np.mean((np.abs(kappa_to_gamma(kap, dx, pad)) - E_modulus) ** 2))))
    return kap, res

# ----------------------------------------------------------------------------- polarization (a second spin-2 field)
def polarization_from_potential(phi, dx=1.0, pad=2):
    """Q + iU = D·(−∇²φ/2) : a polarization (spin-2) field generated by a scalar potential — pure E-mode by construction.

    :param phi: scalar potential map
    :param dx: pixel size
    :param pad: zero-padding factor
    :returns: the result (see summary)
    """
    n = phi.shape[0]; pp, o = pad_to(phi, pad); KX, KY = kgrid(pp.shape[0], dx); k2 = KX ** 2 + KY ** 2
    kap = np.fft.ifft2(k2 / 2 * np.fft.fft2(pp)).real; return crop(np.fft.ifft2(D_kernel(pp.shape[0], dx) * np.fft.fft2(kap)), o, n)

def polarization_angle(QU):
    """EVPA χ = ½ atan2(U, Q) and fractional-independent polarized intensity P = |Q + iU|.

    :param QU: complex spin-2 field Q + iU
    :returns: the result (see summary)
    """
    return 0.5 * np.arctan2(QU.imag, QU.real), np.abs(QU)

def field_correlation(a, b):
    """Pearson correlation of two maps.

    :param a: first array / field
    :param b: second array / field
    :returns: the result (see summary)
    """
    a = a - a.mean(); b = b - b.mean(); return float((a * b).sum() / math.sqrt((a ** 2).sum() * (b ** 2).sum() + 1e-300))

# ----------------------------------------------------------------------------- the honest checks
def verify(seed=0):
    """The honest checks: closed-form and exact self-tests of the lensing algebra.

    :param seed: random seed
    :returns: the result (see summary)
    """
    out = {}; n = 128; D = D_kernel(n)
    nz = np.abs(D) > 0; out["|D| = 1 for k ≠ 0"] = bool(np.allclose(np.abs(D[nz]), 1.0, atol=1e-12) and D[0, 0] == 0)
    kap = gaussian_kappa((n, n), (n / 2, n / 2), 0.3, 8.0); g = kappa_to_gamma(kap, pad=3)
    gt, gx, r = tangential_cross(g, (n / 2, n / 2)); edges = np.linspace(3, 30, 10); prof = radial_profile(gt, r, edges); mid = 0.5 * (edges[1:] + edges[:-1])
    ex = gaussian_gamma_t(mid, 0.3, 8.0); out["Gaussian halo: γ_t = κ̄(<r) − κ (max |err|)"] = float(np.nanmax(np.abs(prof - ex)))
    out["cross component γ_× ≈ 0 (rms)"] = float(np.sqrt(np.mean(gx[(r > 3) & (r < 30)] ** 2)))
    k2 = gamma_to_kappa(g, pad=3); dk = (k2.real - kap)[32:96, 32:96]; out["KS round trip, κ_E error after removing the mass sheet (rms)"] = float(np.sqrt(np.mean((dk - dk.mean()) ** 2)))
    out["round trip B-mode (rms)"] = float(np.sqrt(np.mean(k2.imag[32:96, 32:96] ** 2)))
    out["mass-sheet: γ blind to a constant added to κ (max |Δγ|, unpadded)"] = float(np.max(np.abs(kappa_to_gamma(kap + 0.5, pad=1) - kappa_to_gamma(kap, pad=1))))
    ph = np.fromfunction(lambda y, x: np.exp(-(((x - 64) / 15) ** 2 + ((y - 64) / 20) ** 2)), (n, n)); Q = polarization_from_potential(ph)
    E, B = eb_decompose(Q); out["potential-born polarization is pure E (|B|/|E| rms)"] = float(np.sqrt(np.mean(B[32:96, 32:96] ** 2)) / np.sqrt(np.mean(E[32:96, 32:96] ** 2)))
    c = calibrate_shear(); out["calibration: (m recovered − m injected) in sigma"] = float((c["m_recovered"] - c["m_in"]) / (c["stat_error_on_gamma"] / c["gamma_in"][0]))
    return out
