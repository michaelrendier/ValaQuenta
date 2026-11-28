# SPDX-License-Identifier: GPL-3.0-only
"""
ValaQuenta.modules.ptycho_weak_lensing.shapes
=============================================
From pixels to shear: the step the catalogue-level engine (``maths.py``) assumed. A weak-lensing catalogue is only as good as the
shapes in it, and a shape from a stack or mosaic carries the point-spread function (PSF) and the detector with it. This file measures
galaxy ellipticities from image stamps with the PSF forward-modelled (not subtracted), builds the PSF itself from stars, simulates
stamps with a known shear, and calibrates the whole chain. Its catalogue output is the dict ``maths.mock_catalogue`` returns, so
``maths.ks_map`` takes it unchanged.   :CALCULATED unless marked ESTABLISHED.

Conventions (the same as ``maths.py``): the complex ellipticity is ε = (a − b)/(a + b)·e^{2iφ} (a, b the semi-axes, φ the position angle
of the major axis); a circular source sheared by the reduced shear g has ε = g, and an elliptical source ε_s sheared by g has
ε = (ε_s + g)/(1 + g* ε_s) (``maths.apply_shear``). The elliptical isophote of ellipticity ε is the circle mapped by the area-preserving
symmetric matrix M(ε) = [[1 − ε₁, −ε₂], [−ε₂, 1 + ε₁]]/√(1 − |ε|²).

THE MEASUREMENT (ESTABLISHED idea, Bernstein & Jarvis 2002; Miller et al. 2007 "lensfit"; Sheldon & Huff 2017 for the calibration
route): fit an elliptical Gaussian, convolved with the local PSF stamp, to the pixels, weighting by the noise; the fitted (ε₁, ε₂) is
the PSF-corrected shape. The galaxy is not a Gaussian, so the estimator is biased; the bias is measured, not assumed away, by
``calibrate_shear_from_pixels`` (simulated galaxies of another profile, paired with their 90°-rotated twins so the shape noise cancels).

THE PSF (ESTABLISHED): stars are the PSF sampled at points; ``psf_fit_polynomial`` fits each stamp pixel as a polynomial of position
(order 0–3) and ``psf_at`` evaluates it anywhere. Euclid ships a PSF file with each stacked frame; JWST's can be modelled and checked
against its own stars; the same interface takes either.

NOT HERE: detection and deblending, source selection by colour or redshift, multi-exposure joint fitting, intrinsic alignments,
and the additive-bias terms that depend on the survey. Those are named in the wiki as what is still to build.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from .maths import apply_shear

# ----------------------------------------------------------------------------- geometry and profiles
def shape_matrix(e1, e2):
    """The area-preserving symmetric matrix M(ε) that maps a circle onto the isophote of complex ellipticity ε = e1 + i e2.

    :param e1: first ellipticity component, |ε| < 1
    :param e2: second ellipticity component
    :returns: 2×2 matrix with det 1
    """
    s = np.sqrt(1.0 - e1 * e1 - e2 * e2)
    return np.array([[1.0 - e1, -e2], [-e2, 1.0 + e1]]) / s


def stamp_grid(size):
    """Pixel-centre coordinates of a square stamp, the origin at the middle pixel.

    :param size: stamp side in pixels (odd)
    :returns: (X, Y) arrays of shape (size, size), X along axis 1
    """
    h = size // 2
    y, x = np.mgrid[-h:size - h, -h:size - h]
    return x.astype(float), y.astype(float)


def _radius2(X, Y, x0, y0, e1, e2):
    M = shape_matrix(e1, e2)
    dx, dy = X - x0, Y - y0
    u = M[0, 0] * dx + M[0, 1] * dy
    v = M[1, 0] * dx + M[1, 1] * dy
    return u * u + v * v


def gaussian_profile(X, Y, flux, x0, y0, sigma, e1, e2):
    """Elliptical Gaussian of total flux ``flux`` and ellipticity (e1, e2): the circle of width σ mapped by M(ε).

    :param X: x pixel coordinates
    :param Y: y pixel coordinates
    :param flux: total flux
    :param x0: centre x
    :param y0: centre y
    :param sigma: circular-equivalent width in pixels
    :param e1: first ellipticity component
    :param e2: second ellipticity component
    :returns: the image on the grid (point-sampled at pixel centres)
    """
    return flux / (2 * np.pi * sigma ** 2) * np.exp(-_radius2(X, Y, x0, y0, e1, e2) / (2 * sigma ** 2))


def exponential_profile(X, Y, flux, x0, y0, hlr, e1, e2):
    """Elliptical exponential disc (Sérsic n = 1) of total flux ``flux``, half-light radius ``hlr`` (circular equivalent).

    :param X: x pixel coordinates
    :param Y: y pixel coordinates
    :param flux: total flux
    :param x0: centre x
    :param y0: centre y
    :param hlr: half-light radius in pixels
    :param e1: first ellipticity component
    :param e2: second ellipticity component
    :returns: the image on the grid
    """
    rs = hlr / 1.678
    return flux / (2 * np.pi * rs ** 2) * np.exp(-np.sqrt(_radius2(X, Y, x0, y0, e1, e2)) / rs)


def psf_gaussian(size, sigma, e1=0.0, e2=0.0):
    """A Gaussian PSF stamp, unit sum, centred on the middle pixel.

    :param size: stamp side (odd)
    :param sigma: circular-equivalent width in pixels
    :param e1: PSF ellipticity, first component
    :param e2: PSF ellipticity, second component
    :returns: the stamp
    """
    X, Y = stamp_grid(size)
    p = gaussian_profile(X, Y, 1.0, 0.0, 0.0, sigma, e1, e2)
    return p / p.sum()


def _psf_fft(psf, size):
    """FFT of a PSF stamp placed for circular convolution on a size × size grid (centre at index 0)."""
    big = np.zeros((size, size))
    h = psf.shape[0] // 2
    big[:psf.shape[0], :psf.shape[1]] = psf
    big = np.roll(np.roll(big, -h, axis=0), -h, axis=1)
    return np.fft.rfft2(big)


def convolve(stamp, psf):
    """Circular convolution of a stamp with a PSF stamp of the same or smaller size (the PSF centre is its middle pixel).

    :param stamp: image stamp
    :param psf: PSF stamp, unit sum
    :returns: the convolved stamp
    """
    return np.fft.irfft2(np.fft.rfft2(stamp) * _psf_fft(psf, stamp.shape[0]), s=stamp.shape)


# ----------------------------------------------------------------------------- the PSF from stars
def psf_fit_polynomial(positions, stamps, order=1):
    """Fit the PSF as a polynomial in position: each pixel of the unit-sum star stamps is a polynomial of (x, y) of total degree ``order``.

    :param positions: (n, 2) star positions
    :param stamps: (n, s, s) star stamps (sky-subtracted)
    :param order: polynomial degree, 0 to 3
    :returns: the model dict ({'coef', 'order', 'size', 'centre', 'scale'}) for ``psf_at``
    """
    P = np.asarray(positions, float)
    S = np.asarray(stamps, float)
    S = S / S.sum(axis=(1, 2), keepdims=True)
    centre, scale = P.mean(axis=0), max(P.std(axis=0).max(), 1e-9) * 2
    A = _design(P, centre, scale, order)
    coef, *_ = np.linalg.lstsq(A, S.reshape(len(S), -1), rcond=None)
    return {"coef": coef, "order": order, "size": S.shape[1], "centre": centre, "scale": scale}


def _design(P, centre, scale, order):
    u = (np.atleast_2d(P) - centre) / scale
    cols = [u[:, 0] ** i * u[:, 1] ** j for d in range(order + 1) for i in range(d + 1) for j in [d - i]]
    return np.stack(cols, axis=1)


def psf_at(model, x, y):
    """Evaluate the polynomial PSF model at a position; the stamp is renormalised to unit sum.

    :param model: dict from ``psf_fit_polynomial``
    :param x: x position
    :param y: y position
    :returns: the PSF stamp at (x, y)
    """
    a = _design(np.array([[x, y]]), model["centre"], model["scale"], model["order"])
    s = (a @ model["coef"]).reshape(model["size"], model["size"])
    return s / s.sum()


# ----------------------------------------------------------------------------- the shape measurement
def fit_shape(stamp, psf, noise_sigma, sigma0=2.0):
    """PSF-corrected ellipticity of one galaxy: fit an elliptical Gaussian convolved with ``psf`` to the stamp (noise-weighted least squares).

    :param stamp: sky-subtracted galaxy stamp (square, odd side)
    :param psf: PSF stamp at the galaxy, unit sum, same side or smaller
    :param noise_sigma: pixel noise (one number)
    :param sigma0: starting width in pixels
    :returns: dict with e1, e2 (ε), err (1σ per component, from the Jacobian), flux, sigma, chi2_red, ok
    """
    size = stamp.shape[0]
    if not np.all(np.isfinite(stamp)):
        return {"e1": 0.0, "e2": 0.0, "err": float("inf"), "flux": 0.0, "sigma": 0.0, "chi2_red": float("inf"), "ok": False}
    X, Y = stamp_grid(size)
    F = _psf_fft(psf, size)
    flux0 = max(float(stamp.sum()), 1e-9)

    def model(p):
        return np.fft.irfft2(np.fft.rfft2(gaussian_profile(X, Y, p[0], p[1], p[2], p[3], p[4], p[5])) * F, s=stamp.shape)

    def resid(p):
        return ((model(p) - stamp) / noise_sigma).ravel()

    best = None
    for e0 in ((0.0, 0.0), (0.2, 0.0), (-0.2, 0.0), (0.0, 0.2), (0.0, -0.2)):
        r = least_squares(resid, [flux0, 0.0, 0.0, sigma0, *e0], bounds=([0, -3, -3, 0.5, -0.9, -0.9], [np.inf, 3, 3, size / 3, 0.9, 0.9]), method="trf")
        if best is None or r.cost < best.cost:
            best = r
        if r.cost / stamp.size < 1.5:
            break
    r = best
    J = r.jac
    try:
        cov = np.linalg.inv(J.T @ J)
        err = float(np.sqrt(0.5 * (cov[4, 4] + cov[5, 5])))
    except np.linalg.LinAlgError:
        err = float("inf")
    return {"e1": float(r.x[4]), "e2": float(r.x[5]), "err": err, "flux": float(r.x[0]), "sigma": float(r.x[3]),
            "chi2_red": float(2 * r.cost / (stamp.size - 6)), "ok": bool(r.success and abs(r.x[4]) < 0.89 and abs(r.x[5]) < 0.89)}


def measure_image(image, positions, psf, noise_sigma, size=31, sigma_e=0.26, dx=1.0):
    """Measure the PSF-corrected ellipticity of every galaxy of a square image and return the catalogue ``maths.ks_map`` takes.

    :param image: square sky-subtracted image
    :param positions: (n, 2) galaxy (x, y) pixel positions
    :param psf: a PSF stamp, or a function (x, y) → PSF stamp (e.g. ``lambda x, y: psf_at(model, x, y)``)
    :param noise_sigma: pixel noise
    :param size: stamp side (odd)
    :param sigma_e: intrinsic ellipticity dispersion per component, for the weights
    :param dx: pixel size for the catalogue
    :returns: dict {'x', 'y', 'e' (complex), 'sigma_e', 'n', 'dx', 'err', 'w', 'ok'} for the galaxies whose stamp fits inside the image and whose fit converged
    """
    n = image.shape[0]
    if image.shape[1] != n:
        raise ValueError("measure_image needs a square image (ks_map takes one grid size)")
    h = size // 2
    xs, ys, es, errs, oks = [], [], [], [], []
    for x, y in np.asarray(positions, float):
        ix, iy = int(round(x)), int(round(y))
        if ix - h < 0 or iy - h < 0 or ix + h + 1 > n or iy + h + 1 > n:
            continue
        stamp = image[iy - h:iy + h + 1, ix - h:ix + h + 1]
        p = psf(x, y) if callable(psf) else psf
        r = fit_shape(stamp, p, noise_sigma)
        xs.append(x), ys.append(y), es.append(complex(r["e1"], r["e2"])), errs.append(r["err"]), oks.append(r["ok"])
    ok = np.array(oks, bool)
    err = np.array(errs)
    cat = {"x": np.array(xs)[ok], "y": np.array(ys)[ok], "e": np.array(es)[ok], "sigma_e": sigma_e, "n": n, "dx": dx, "err": err[ok]}
    cat["w"] = 1.0 / (sigma_e ** 2 + cat["err"] ** 2)
    cat["ok"] = int(ok.sum())
    return cat


def shear_estimate(e, w=None):
    """Weighted mean ellipticity: the weak-shear estimate ĝ = ⟨ε⟩ (the shear is small, and the intrinsic ellipticities average to zero).

    :param e: complex ellipticities
    :param w: weights (default equal)
    :returns: (ĝ, its standard error per component, computed from the scatter)
    """
    e = np.asarray(e)
    w = np.ones(len(e)) if w is None else np.asarray(w)
    g = np.sum(w * e) / np.sum(w)
    var = np.sum(w ** 2 * np.abs(e - g) ** 2) / np.sum(w) ** 2 / 2
    return g, float(np.sqrt(var))


def psf_leakage(e_gal, e_psf):
    """PSF leakage α in ε_gal = α·ε_psf + (the rest): the regression of galaxy ellipticity on the PSF ellipticity at the same positions. A shear-free field with a clean pipeline has α = 0.

    :param e_gal: complex galaxy ellipticities
    :param e_psf: complex PSF ellipticities at the galaxies' positions
    :returns: α (real) and its standard error
    """
    eg, ep = np.asarray(e_gal), np.asarray(e_psf)
    a = float(np.real(np.sum(eg * np.conj(ep))) / np.sum(np.abs(ep) ** 2))
    res = eg - a * ep
    return a, float(np.sqrt(np.sum(np.abs(res) ** 2) / 2 / max(len(eg) - 1, 1) / np.sum(np.abs(ep) ** 2) * 2))


# ----------------------------------------------------------------------------- simulations and calibration
def simulate_stamp(g, es, psf, peak_snr=30.0, hlr=2.5, flux=1.0, profile="exp", rng=None, size=31, offset=(0.0, 0.0)):
    """One galaxy stamp: intrinsic ellipticity ``es`` sheared by ``g`` (``maths.apply_shear``), rendered, convolved with the PSF, plus noise.

    :param g: reduced shear (complex)
    :param es: intrinsic ellipticity (complex)
    :param psf: PSF stamp
    :param peak_snr: peak signal over pixel noise
    :param hlr: half-light radius in pixels (for the Gaussian profile, hlr/1.178 is σ)
    :param flux: total flux
    :param profile: 'exp' (exponential disc) or 'gauss'
    :param rng: numpy random Generator
    :param size: stamp side
    :param offset: sub-pixel centre offset (x, y)
    :returns: (stamp, noise_sigma, the observed ellipticity ε before the PSF)
    """
    rng = rng or np.random.default_rng(0)
    e = complex(apply_shear(np.array([es]), np.array([g]))[0])
    X, Y = stamp_grid(size)
    prof = exponential_profile if profile == "exp" else gaussian_profile
    size_param = hlr if profile == "exp" else hlr / 1.178
    clean = convolve(prof(X, Y, flux, offset[0], offset[1], size_param, e.real, e.imag), psf)
    noise = clean.max() / peak_snr
    return clean + rng.normal(0, noise, clean.shape), noise, e


def rotated_pair_shear(g, psf, n_pairs=60, peak_snr=30.0, profile="exp", sigma_e=0.25, rng=None, hlr=2.5):
    """Mean measured ellipticity of galaxies sheared by ``g``, each intrinsic shape paired with its 90°-rotated twin (ε_s → −ε_s) so the shape noise cancels.

    :param g: reduced shear (complex)
    :param psf: PSF stamp
    :param n_pairs: number of pairs
    :param peak_snr: peak signal over pixel noise
    :param profile: 'exp' or 'gauss'
    :param sigma_e: intrinsic ellipticity dispersion per component
    :param rng: numpy random Generator
    :param hlr: half-light radius in pixels
    :returns: (mean ε over the pairs, standard error per component)
    """
    rng = rng or np.random.default_rng(0)
    meas = []
    for _ in range(n_pairs):
        es = complex(rng.normal(0, sigma_e), rng.normal(0, sigma_e))
        if abs(es) > 0.7:
            es *= 0.7 / abs(es)
        off = (rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5))
        pair = []
        for s in (es, -es):
            st, nz, _ = simulate_stamp(g, s, psf, peak_snr, hlr, 1.0, profile, rng, offset=off)
            r = fit_shape(st, psf, nz)
            if r["ok"]:
                pair.append(complex(r["e1"], r["e2"]))
        if len(pair) == 2:
            meas.append(0.5 * (pair[0] + pair[1]))
    m = np.array(meas)
    return complex(m.mean()), float(np.sqrt(np.var(m.real) + np.var(m.imag)) / np.sqrt(2) / np.sqrt(len(m)))


def calibrate_shear_from_pixels(psf, g_values=(-0.06, 0.0, 0.06), n_pairs=60, peak_snr=30.0, profile="exp", rng=None):
    """The shear calibration of the pixel pipeline: ε̂ = (1 + m)·g + c from rotated-pair simulations at several known shears (both components).

    :param psf: PSF stamp
    :param g_values: the true shears to inject (real values, used for g₁ and for g₂ in turn)
    :param n_pairs: pairs per shear
    :param peak_snr: peak signal over pixel noise
    :param profile: the true galaxy profile ('exp' or 'gauss')
    :param rng: numpy random Generator
    :returns: dict {'m', 'm_err', 'c1', 'c2', 'c_err'}
    """
    rng = rng or np.random.default_rng(1)
    gt, gm, ge = [], [], []
    for comp in (0, 1):
        for gv in g_values:
            g = complex(gv, 0) if comp == 0 else complex(0, gv)
            e, err = rotated_pair_shear(g, psf, n_pairs, peak_snr, profile, rng=rng)
            gt.append(gv), gm.append(e.real if comp == 0 else e.imag), ge.append(max(err, 1e-4))
    gt, gm, ge = np.array(gt), np.array(gm), np.array(ge)
    comp = np.array([0] * len(g_values) + [1] * len(g_values))
    A = np.stack([gt, (comp == 0).astype(float), (comp == 1).astype(float)], axis=1) / ge[:, None]
    sol, *_ = np.linalg.lstsq(A, gm / ge, rcond=None)
    cov = np.linalg.inv(A.T @ A)
    return {"m": float(sol[0] - 1.0), "m_err": float(np.sqrt(cov[0, 0])), "c1": float(sol[1]), "c2": float(sol[2]), "c_err": float(np.sqrt(cov[1, 1]))}


def render_field(cat, psf, peak_snr=30.0, hlr=2.5, profile="exp", size=31, rng=None):
    """Render a square image of the galaxies of a catalogue (``maths.mock_catalogue``: x, y, ε) convolved with the PSF, plus Gaussian noise.

    :param cat: catalogue dict with 'x', 'y', 'e' (the observed complex ellipticity of each galaxy) and 'n' (the image side)
    :param psf: a PSF stamp, or a function (x, y) → PSF stamp
    :param peak_snr: peak signal over pixel noise for a reference galaxy
    :param hlr: half-light radius in pixels (every galaxy the same)
    :param profile: 'exp' or 'gauss'
    :param size: stamp side for rendering each galaxy (odd)
    :param rng: numpy random Generator
    :returns: (image, noise_sigma)
    """
    rng = rng or np.random.default_rng(0)
    n, h = cat["n"], size // 2
    X, Y = stamp_grid(size)
    prof = exponential_profile if profile == "exp" else gaussian_profile
    par = hlr if profile == "exp" else hlr / 1.178
    img = np.zeros((n, n))
    ref = None
    for x, y, e in zip(cat["x"], cat["y"], cat["e"]):
        ix, iy = int(round(x)), int(round(y))
        if abs(e) >= 0.95:
            e = e * 0.95 / abs(e)                       # an ellipticity must stay inside the unit disc
        p = psf(x, y) if callable(psf) else psf
        s = convolve(prof(X, Y, 1.0, x - ix, y - iy, par, float(np.real(e)), float(np.imag(e))), p)
        if ref is None:
            ref = s.max()
        x0, y0 = max(ix - h, 0), max(iy - h, 0)
        x1, y1 = min(ix + h + 1, n), min(iy + h + 1, n)
        img[y0:y1, x0:x1] += s[y0 - (iy - h):size - ((iy + h + 1) - y1), x0 - (ix - h):size - ((ix + h + 1) - x1)]
    noise = ref / peak_snr
    return img + rng.normal(0, noise, img.shape), noise


def isolated_subset(cat, min_sep):
    """Keep only galaxies with no earlier-kept neighbour closer than ``min_sep`` pixels. The fit here has no deblending, so a blended galaxy would be measured as one object: crowded fields must be thinned (or deblended upstream) before ``measure_image``.

    :param cat: catalogue dict with 'x', 'y' (and any parallel arrays 'e', 'err', 'w')
    :param min_sep: minimum separation in pixels
    :returns: a new catalogue dict with the kept galaxies
    """
    keep = []
    xy = np.c_[cat["x"], cat["y"]]
    for i, p in enumerate(xy):
        if all(np.hypot(*(p - xy[j])) >= min_sep for j in keep):
            keep.append(i)
    out = dict(cat)
    for k, v in cat.items():
        if isinstance(v, np.ndarray) and len(v) == len(xy):
            out[k] = v[keep]
    return out


def verify_shapes(seed=3):
    """Self-checks of the pixel pipeline, small enough to run in seconds: PSF from stars, PSF correction, calibration.

    :param seed: random seed
    :returns: dict of named results (numbers and booleans)
    """
    rng = np.random.default_rng(seed)
    out = {}
    # 1. a position-dependent PSF recovered from stars
    size, pos, stars = 25, [], []
    for _ in range(40):
        x, y = rng.uniform(0, 100, 2)
        pos.append((x, y))
        s = psf_gaussian(size, 1.6, 0.02 + 0.0006 * x, -0.0004 * y)
        stars.append(s + rng.normal(0, 2e-4, s.shape))
    model = psf_fit_polynomial(pos, stars, order=1)
    truth = psf_gaussian(size, 1.6, 0.02 + 0.0006 * 77, -0.0004 * 12)
    out["PSF from 40 stars: max error at a new position / peak"] = float(np.abs(psf_at(model, 77, 12) - truth).max() / truth.max())
    # 2. an anisotropic PSF: ignoring it fakes a shear, forward-modelling it does not
    psf = psf_gaussian(25, 1.8, 0.10, 0.0)
    delta = np.zeros((25, 25)); delta[12, 12] = 1.0
    naive, corr = [], []
    for _ in range(40):
        es = complex(rng.normal(0, 0.2), rng.normal(0, 0.2))
        pair = []
        for s in (es, -es):
            st, nz, _ = simulate_stamp(0j, s, psf, 40.0, 2.5, 1.0, "gauss", rng, size=25)
            rn, rc = fit_shape(st, delta, nz), fit_shape(st, psf, nz)
            pair.append((complex(rn["e1"], rn["e2"]), complex(rc["e1"], rc["e2"])))
        naive.append(0.5 * (pair[0][0] + pair[1][0])); corr.append(0.5 * (pair[0][1] + pair[1][1]))
    out["no PSF correction: mean ε₁ of zero-shear galaxies (PSF ε₁ = 0.10)"] = float(np.mean(np.real(naive)))
    out["PSF forward-modelled: mean ε₁ of zero-shear galaxies"] = float(np.mean(np.real(corr)))
    # 3. calibration with the true profile different from the fitted one
    cal = calibrate_shear_from_pixels(psf_gaussian(25, 1.8, 0.0, 0.0), g_values=(-0.05, 0.05), n_pairs=30, peak_snr=40.0, profile="exp", rng=rng)
    out["calibration, exponential truth fitted by a Gaussian: m"] = cal["m"]
    out["calibration: m error (1σ)"] = cal["m_err"]
    return out
