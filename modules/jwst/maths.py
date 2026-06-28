"""
ainulindale_engine.modules.jwst.maths
=======================================
JWST spectral pixel module.
Cayley-Dickson addressing of spectral data.

Each JWST pixel is a spectral measurement at a specific wavelength.
The Cayley-Dickson tower provides a natural address space:
  λ (wavelength nm) → radial coordinate r ∈ (0,1)
  intensity         → algebra element norm
  8 JWST filters    → 8 octonion components (e0..e7)

JWST NIRCam filters (approximate central wavelengths nm):
  F090W : 900 nm
  F115W : 1150 nm
  F150W : 1500 nm
  F200W : 2000 nm
  F277W : 2770 nm
  F356W : 3560 nm
  F410M : 4100 nm
  F444W : 4440 nm

8 filters → 8 octonion components → one 𝕆 element per sky pixel.

Version: 0.111
"""

import math
from typing import Dict, List, Any, Tuple, Optional


# ── JWST NIRCam filter wavelengths (nm) ───────────────────────────────────────

JWST_FILTERS: Dict[str, float] = {
    'F090W': 900.0,
    'F115W': 1150.0,
    'F150W': 1500.0,
    'F200W': 2000.0,
    'F277W': 2770.0,
    'F356W': 3560.0,
    'F410M': 4100.0,
    'F444W': 4440.0,
}

FILTER_NAMES  = list(JWST_FILTERS.keys())
FILTER_LAMBDA = list(JWST_FILTERS.values())

# Wavelength range for radial mapping
LAMBDA_MIN = FILTER_LAMBDA[0]    # 900 nm
LAMBDA_MAX = FILTER_LAMBDA[-1]   # 4440 nm


# ── Radial mapping ─────────────────────────────────────────────────────────────

def lambda_to_r(wavelength_nm: float) -> float:
    """
    Map wavelength to radial coordinate r ∈ (0,1).
    r = (λ - λ_min) / (λ_max - λ_min)
    """
    return (wavelength_nm - LAMBDA_MIN) / (LAMBDA_MAX - LAMBDA_MIN + 1e-9)


def r_to_lambda(r: float) -> float:
    """Inverse: r → wavelength in nm."""
    return LAMBDA_MIN + r * (LAMBDA_MAX - LAMBDA_MIN)


# ── Spectral pixel → octonion ──────────────────────────────────────────────────

def spectral_to_octonion(intensities: List[float]) -> Dict[str, Any]:
    """
    Map 8 JWST filter intensities to an 𝕆 element.

    intensities: list of 8 floats (one per NIRCam filter), in filter order.
    If fewer than 8 provided, remaining components are 0.

    The 𝕆 element: Ψ = Σ_k I_k · e_k  (k=0..7)
    Norm: |Ψ| = sqrt(Σ I_k²)

    Returns: components, norm, r_coords (radial addresses of each filter)
    """
    comps = (list(intensities) + [0.0] * 8)[:8]
    norm  = math.sqrt(sum(c*c for c in comps))
    r_coords = [lambda_to_r(lam) for lam in FILTER_LAMBDA]

    return {
        'components'  : comps,
        'norm'        : norm,
        'r_coords'    : r_coords,
        'filter_names': FILTER_NAMES,
        'wavelengths' : FILTER_LAMBDA,
        'algebra'     : '𝕆',
        'dim'         : 8,
        'note'        : '8 NIRCam filters → 8 octonion components → one Oct element per pixel',
    }


def octonion_to_spectral(components: List[float]) -> Dict[str, Any]:
    """
    Reverse: 𝕆 components → spectral intensities at filter wavelengths.
    """
    comps = (list(components) + [0.0] * 8)[:8]
    return {
        filter_name: max(0.0, comps[i])
        for i, filter_name in enumerate(FILTER_NAMES)
    }


# ── Cayley-Dickson spectral address ───────────────────────────────────────────

def cd_spectral_address(intensities: List[float],
                         pixel_x: int = 0,
                         pixel_y: int = 0) -> Dict[str, Any]:
    """
    Full Cayley-Dickson address for a JWST spectral pixel.

    The address encodes:
      ℝ layer : mean intensity (scalar)
      ℂ layer : (mean_blue, mean_red) — short vs long wavelength
      ℍ layer : (I_0, I_2, I_4, I_6) — alternate filter components
      𝕆 layer : all 8 components

    Plus: pixel coordinates (x,y) encoded as base-100 integer pair.
    """
    oct_data = spectral_to_octonion(intensities)
    comps    = oct_data['components']
    norm     = oct_data['norm']

    # ℝ: mean
    r_coord = sum(comps) / 8.0

    # ℂ: (short-wave mean, long-wave mean)
    c_re = sum(comps[:4]) / 4.0
    c_im = sum(comps[4:]) / 4.0

    # ℍ: alternating components
    h_coords = [comps[i] for i in (0, 2, 4, 6)]

    # Pixel address: (x,y) → single int via base-10000 encoding
    pixel_addr = pixel_x * 10000 + pixel_y

    # Fano generator path: each component maps to a Fano generator
    fano_gens = [int(abs(c) * 7) % 7 for c in comps]

    return {
        'pixel'        : (pixel_x, pixel_y),
        'pixel_addr'   : pixel_addr,
        'alg_R'        : r_coord,
        'alg_C'        : [c_re, c_im],
        'alg_H'        : h_coords,
        'alg_O'        : comps,
        'norm'         : norm,
        'fano_gens'    : fano_gens,
        'filters'      : FILTER_NAMES,
        'wavelengths'  : FILTER_LAMBDA,
    }


def synthetic_spectrum(emission_type: str = 'hydrogen') -> Dict[str, Any]:
    """
    Generate a synthetic emission spectrum for testing.

    emission_type:
      'hydrogen'   Balmer series (Hα at 656nm outside NIRCam, Pa-α at 1875nm etc.)
      'flat'       uniform across all filters
      'stellar'    blackbody-like declining with wavelength
    """
    if emission_type == 'hydrogen':
        # Paschen series falls in NIRCam range
        # Pa-α: 1875nm, Pa-β: 1282nm, Pa-γ: 1094nm, Pa-δ: 1005nm
        # Approximate relative intensities
        lams = FILTER_LAMBDA
        intensities = []
        pa_lines = [1875.0, 1282.0, 1094.0, 1005.0]
        for lam in lams:
            # Gaussian proximity to nearest Paschen line
            proximity = min(math.exp(-((lam - pa)**2) / (200**2)) for pa in pa_lines)
            intensities.append(proximity)

    elif emission_type == 'stellar':
        # Approximate blackbody T=5000K declining with wavelength
        lams = FILTER_LAMBDA
        T = 5000.0
        h = 6.626e-34; c = 3e8; k = 1.38e-23
        intensities = []
        for lam_nm in lams:
            lam_m = lam_nm * 1e-9
            B = (2 * h * c**2 / lam_m**5) / (math.exp(h*c / (lam_m*k*T)) - 1)
            intensities.append(B)
        mx = max(intensities)
        intensities = [i/mx for i in intensities]

    else:  # flat
        intensities = [1.0] * 8

    return {
        'type'       : emission_type,
        'intensities': intensities,
        'filters'    : FILTER_NAMES,
        'wavelengths': FILTER_LAMBDA,
    }
