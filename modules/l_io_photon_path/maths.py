"""
ainulindale_engine.modules.l_io_photon_path.maths
====================================================
L_(I|O) as General Relativity: the actual (bent) photon path vs.
the clean (stationary-action, flat-space) path — computed from real
measured weak-lensing shear, not a toy model.

Ainulindale/wiki/52 defines L_(I|O) philosophically: "Photons are not
undisturbed paths... The light's path was not clean. The path was
L_(I|O)." Two formal targets in that document were left open:
  (1) define L_(I|O) formally, distinguish it from L (stationary action)
  (4) formalize light bending/slingshot within L_(I|O)
Claude's 2026-07-10 addendum to that file proposed a specific, testable
hypothesis: L_(I|O) is not a different operator from L at all — it is L
computed honestly with the REAL (curved) metric, where the curvature is
sourced by real mass. This module tests that hypothesis directly using
established weak-lensing GR, not a new formalism:

    1. Kaiser & Squires (1993) shear->convergence inversion (EXACT linear
       transform of the real measured shear field, no fitting).
    2. Poisson equation nabla^2 psi = 2 kappa  ->  lensing potential
       (EXACT FFT solve, no fitting).
    3. Deflection field alpha = grad(psi)  (EXACT, no fitting).
    4. Lens equation beta = theta - alpha(theta):
         theta      = apparent (observed) position  -- the CLEAN path
                       endpoint, i.e. what a straight, undeflected photon
                       would trace (alpha=0)
         beta       = true source position implied by the ACTUAL bent path
       The difference IS the messy, real-time-adjusted path wiki/52
       describes -- not asserted, computed from the real shear data.
    5. L_(I|O) - L := -psi(theta)  (the Fermat/time-delay potential term).
       This is the standard GR statement that the actual light-travel-time
       functional differs from the flat-space one by exactly the lensing
       potential. It is not a new operator; it is the established one,
       named to match wiki/52's language.

Everything here is a closed-form linear transform of the input shear
array. No free parameters are fit to any expected outcome. If the real
Bullet Cluster shear is noise-dominated at this depth, kappa/psi/alpha
will reflect that honestly -- this module does not smooth, clip, or
rescale to make the output look like a clean lens.

Known, stated (not hidden) limitation of step 1: Kaiser-Squires
convergence is defined only up to an additive constant and an overall
sign/mass-sheet degeneracy (kappa -> lambda*kappa + (1-lambda) is
observationally indistinguishable from shear alone). This module reports
kappa as reconstructed; it does not claim an absolute mass normalization.

BOUNDARY ROLE (2026-07-21 addendum -- interpretive framing on established
math, does not change any equation above): (I|O)_RB (renamed from
H_hat_RB) defines WHERE a boundary/degenerate locus is -- the zero-divisor
crossing, structurally the origin a pathway is measured outward from, not
an endpoint. This module is the general TEMPLATE for HOW to actually get
through such a boundary once (I|O)_RB has defined it: kaiser_squires_kappa's
`kappa_hat[0,0] = 0.0` is not a special-case patch, it is the general
method -- at the transform's own degenerate point (k=0 here; a
zero-divisor element in the sedenion case), do not let the direct formula
blow up (1/|k|^2 -> inf) and do not silently exclude the point either;
assign the point's value EXPLICITLY, by a stated convention (here: the
mean is not observable from shear alone), and say why. That is the
reusable content of "L_(I|O) is how you get through the boundary" --
independent of gravitational lensing specifically.

CONJECTURE, explicitly not established (flagged, not asserted -- see
Ainulindale wiki companion page for the argument in full): the Riemann
zeta function's simple pole at s=1 (zeta(s) ~ 1/(s-1) + gamma, gamma =
Euler-Mascheroni constant, finite residue extracted at the divergent
point) is the SAME CATEGORY of construction as kappa_hat's k=0 zeroing --
both regularize a transform at its own singular point by explicit,
stated convention rather than fit or omission. The zeta functional
equation zeta(s) = 2^s pi^(s-1) sin(pi s/2) Gamma(1-s) zeta(1-s), an
s<->1-s involution fixed at Re(s)=1/2, is likewise the same SHAPE as this
module's theta/beta (apparent/true) pair. Category match, not identity:
nothing here shows zeta(s) is DERIVABLE as a parameter setting of
kaiser_squires_kappa/lensing_potential's actual functional form. That
derivation does not exist yet. Do not upgrade this tier without it.

Version: 0.2
"""

import numpy as np
from typing import Dict, Any, Tuple


# ── Step 0: non-periodic boundary handler ─────────────────────────────────────
#
# kaiser_squires_kappa() and lensing_potential() are exact, parameter-free
# transforms -- but both use plain FFT, which implicitly treats the input as
# PERIODIC (wraps the right edge into the left, top into bottom). A single
# finite JWST frame is not periodic; its real edge gets a false wraparound
# discontinuity, and dividing by |k|^2 near k=0 amplifies whatever low-frequency
# power that discontinuity injects. That is what produced the ~700-1700 arcsec
# deflections: a boundary-condition artifact, not signal.
#
# The fix below is a boundary-condition correction, not a fit: it does not
# adjust any value toward an expected outcome. It tapers the real field to
# zero at its real edges (Tukey window -- flat in the interior, cosine roll-off
# only in a fixed fraction of the border) and zero-pads around it, so the FFT's
# forced periodicity wraps zero into zero instead of signal into signal. The
# padding is cropped back off after the solve. taper_frac/pad_factor control
# how much of the domain is treated as boundary, not what the answer should be.

def _tukey_window(n: int, taper_frac: float) -> np.ndarray:
    """1D Tukey window: flat centre, cosine taper over taper_frac at each edge."""
    if taper_frac <= 0:
        return np.ones(n)
    w = np.ones(n)
    edge = max(1, int(taper_frac * n / 2))
    ramp = 0.5 * (1 - np.cos(np.pi * np.arange(edge) / edge))
    w[:edge] = ramp
    w[-edge:] = ramp[::-1]
    return w


def apodize_and_pad(field: np.ndarray, taper_frac: float = 0.1,
                     pad_factor: float = 2.0) -> Tuple[np.ndarray, Tuple[int, int]]:
    """Taper a real (non-periodic) field to zero at its edges, then zero-pad it."""
    ny, nx = field.shape
    window = np.outer(_tukey_window(ny, taper_frac), _tukey_window(nx, taper_frac))
    tapered = field * window

    pad_y = int(ny * (pad_factor - 1) / 2)
    pad_x = int(nx * (pad_factor - 1) / 2)
    padded = np.pad(tapered, ((pad_y, pad_y), (pad_x, pad_x)), mode='constant')
    return padded, (pad_y, pad_x)


def crop_padding(padded_field: np.ndarray, pad: Tuple[int, int],
                  orig_shape: Tuple[int, int]) -> np.ndarray:
    """Inverse of apodize_and_pad's zero-padding step."""
    pad_y, pad_x = pad
    ny, nx = orig_shape
    return padded_field[pad_y:pad_y + ny, pad_x:pad_x + nx]


def bounded_lensing_pipeline(gamma1: np.ndarray, gamma2: np.ndarray,
                              pixel_scale_arcsec: float,
                              taper_frac: float = 0.1,
                              pad_factor: float = 2.0) -> Dict[str, np.ndarray]:
    """
    Full pipeline with the boundary handler applied: taper+pad the real shear,
    run the exact Kaiser-Squires + Poisson steps on the padded field (now
    legitimately periodic-safe: zero wraps into zero), then crop every output
    back to the original frame. kaiser_squires_kappa() and lensing_potential()
    themselves are untouched -- this only changes what they're fed.
    """
    orig_shape = gamma1.shape
    g1_pad, pad = apodize_and_pad(gamma1, taper_frac, pad_factor)
    g2_pad, _ = apodize_and_pad(gamma2, taper_frac, pad_factor)

    kappa_pad = kaiser_squires_kappa(g1_pad, g2_pad)
    psi_pad = lensing_potential(kappa_pad)
    a1_pad, a2_pad = deflection_field(psi_pad, pixel_scale_arcsec)

    return {
        'kappa': crop_padding(kappa_pad, pad, orig_shape),
        'psi':   crop_padding(psi_pad, pad, orig_shape),
        'alpha1': crop_padding(a1_pad, pad, orig_shape),
        'alpha2': crop_padding(a2_pad, pad, orig_shape),
    }


# ── Step 1: Kaiser-Squires shear -> convergence (EXACT, no fitting) ──────────

def kaiser_squires_kappa(gamma1: np.ndarray, gamma2: np.ndarray) -> np.ndarray:
    """
    kappa_hat(k) = D*(k) . gamma_hat(k)
    D(k) = (k1^2 - k2^2 + 2i k1 k2) / |k|^2   (Kaiser & Squires 1993, eq. 2.2)

    Exact linear inversion of the real measured shear. k=0 mode (the
    additive mass-sheet degeneracy) is set to zero -- not fit, just the
    standard convention: KS reconstruction is only defined relative to a
    mean, and that mean is not observable from shear alone.
    """
    ny, nx = gamma1.shape
    k1 = np.fft.fftfreq(nx) * 2 * np.pi
    k2 = np.fft.fftfreq(ny) * 2 * np.pi
    K1, K2 = np.meshgrid(k1, k2)
    k2mag = K1**2 + K2**2
    k2mag[0, 0] = 1.0  # avoid divide-by-zero; k=0 mode zeroed explicitly below

    gamma_hat = np.fft.fft2(gamma1 + 1j * gamma2)
    D_conj = (K1**2 - K2**2 - 2j * K1 * K2) / k2mag
    kappa_hat = D_conj * gamma_hat
    kappa_hat[0, 0] = 0.0

    return np.fft.ifft2(kappa_hat).real


# ── Step 2+3: Poisson solve for lensing potential, then deflection ───────────

def lensing_potential(kappa: np.ndarray) -> np.ndarray:
    """
    nabla^2 psi = 2 kappa  ->  psi_hat(k) = -2 kappa_hat(k) / |k|^2
    Exact FFT Poisson solve. No fitting.
    """
    ny, nx = kappa.shape
    k1 = np.fft.fftfreq(nx) * 2 * np.pi
    k2 = np.fft.fftfreq(ny) * 2 * np.pi
    K1, K2 = np.meshgrid(k1, k2)
    k2mag = K1**2 + K2**2
    k2mag[0, 0] = 1.0

    kappa_hat = np.fft.fft2(kappa)
    psi_hat = -2.0 * kappa_hat / k2mag
    psi_hat[0, 0] = 0.0

    return np.fft.ifft2(psi_hat).real


def deflection_field(psi: np.ndarray, pixel_scale_arcsec: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    alpha = grad(psi), converted from per-pixel to arcsec using the real
    JWST pixel scale (no fitting -- this is a unit conversion, not a
    parameter chosen to match an outcome).
    """
    dpsi_dy, dpsi_dx = np.gradient(psi)
    alpha1 = dpsi_dx / pixel_scale_arcsec
    alpha2 = dpsi_dy / pixel_scale_arcsec
    return alpha1, alpha2


# ── Step 4: the lens equation -- clean path vs. actual (bent) path ──────────

def trace_photon(theta1: np.ndarray, theta2: np.ndarray,
                  alpha1: np.ndarray, alpha2: np.ndarray) -> Dict[str, np.ndarray]:
    """
    theta = apparent (observed) position -- the CLEAN path endpoint
            (what an undeflected photon, alpha=0, would trace).
    beta  = theta - alpha(theta) -- the ACTUAL source position implied by
            the real, deflected (L_(I|O)) path.

    Returns both so the deviation (beta - theta = -alpha) is explicit:
    that deviation IS the "unclean" part of the path, computed, not assumed.
    """
    beta1 = theta1 - alpha1
    beta2 = theta2 - alpha2
    return {
        'theta1': theta1, 'theta2': theta2,      # clean-path endpoint
        'beta1':  beta1,  'beta2':  beta2,       # actual-path source
        'deflection_mag': np.sqrt(alpha1**2 + alpha2**2),
    }


# ── Step 5: L_(I|O) - L, the real Fermat-potential deficit ──────────────────

def l_io_deficit(psi: np.ndarray) -> Dict[str, float]:
    """
    L_(I|O) - L := -psi(theta)  (Fermat potential term, standard GR lensing).

    This is reported as raw statistics of the ACTUAL computed field --
    no rescaling, no clipping to a "typical" range, no fit to any target
    value. If the field is dominated by shot noise from ~2500 discrete
    background galaxies (it may well be, honestly stated), that shows up
    directly in these numbers.
    """
    return {
        'mean':   float(np.nanmean(psi)),
        'std':    float(np.nanstd(psi)),
        'min':    float(np.nanmin(psi)),
        'max':    float(np.nanmax(psi)),
        'median': float(np.nanmedian(psi)),
    }
