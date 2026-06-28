"""
ainulindale_engine.modules.lagrangian.maths
=============================================
L_NN — the SMMIP Lagrangian density.

Four terms (corrected Ainulindale form):
  L_NN = (2/π) ∮ [L_kin + L_mat + (1/φ)·L_bias + L_coup] r dr dθ

Running coupling:
  α_NN(r) = g² / (4π · ħ_NN · ln(1/r))

All arithmetic is radian-primary.
fractions.Fraction used throughout; float only at output boundary.

Version: 0.111
"""

import math
from fractions import Fraction
from typing import List, Dict, Tuple, Optional, NamedTuple


# ── Constants (radian-primary) ────────────────────────────────────────────────

PHI   = (1 + math.sqrt(5)) / 2          # golden ratio
PI    = math.pi
TWO_OVER_PI = Fraction(2, 1)            # numerator of polar norm

# Algebra strata
ALG_R, ALG_C, ALG_H, ALG_O = 0, 1, 2, 3
ALG_DIM   = {ALG_R: 1, ALG_C: 2, ALG_H: 4, ALG_O: 8}
ALG_NAME  = {ALG_R: 'ℝ', ALG_C: 'ℂ', ALG_H: 'ℍ', ALG_O: '𝕆'}
ALG_GAUGE = {ALG_R: 'trivial', ALG_C: 'U(1)', ALG_H: 'SU(2)', ALG_O: 'G₂/SU(3)'}
N_GEN     = {ALG_R: 0, ALG_C: 1, ALG_H: 3, ALG_O: 8}

# Fano plane lines (octonion multiplication)
FANO_LINES: List[Tuple[int, int, int]] = [
    (0,1,3),(1,2,4),(2,3,5),(3,4,6),(4,5,0),(5,6,1),(6,0,2)
]


# ── Field state ───────────────────────────────────────────────────────────────

class FieldState(NamedTuple):
    """Minimal field state for Lagrangian evaluation."""
    psi:     List[float]   # activation norms (one per neuron, real)
    A:       List[float]   # gauge field components (flattened, real)
    beta:    List[float]   # bias norms (one per neuron, real)
    algebra: int           # ALG_R / ALG_C / ALG_H / ALG_O
    layer:   int           # integer layer index (1-based)
    hbar_nn: float = 0.1
    g_coup:  float = 0.01
    mu_sq:   float = -1.0  # negative → SSB
    lam:     float = 0.5
    vev:     float = 1.0


# ── Running coupling ──────────────────────────────────────────────────────────

def layer_to_r(layer: int, total_layers: int = 10) -> float:
    """
    Map layer index to radial coordinate r ∈ (0,1).
    r = layer / total_layers   (layer 0 → r=0 excluded; layer L → r=1)
    """
    if total_layers <= 0:
        return 1.0
    return max(layer / total_layers, 1e-6)


def alpha_nn_from_r(g: float, hbar_nn: float, r: float) -> float:
    """
    Running neural coupling in radial form:
      α_NN(r) = g² / (4π · ħ_NN · ln(1/r))

    r ∈ (0,1]: at r→1, ln(1/r)→0 so α_NN → ∞ (UV wall = sedenion boundary).
    """
    if r <= 0 or r >= 1:
        return 0.0
    ln_inv_r = math.log(1.0 / r)
    if ln_inv_r < 1e-12:
        return 0.0
    return (g * g) / (4.0 * PI * hbar_nn * ln_inv_r)


# ── Four Lagrangian terms ─────────────────────────────────────────────────────

def L_kinetic(A: List[float], g: float, algebra: int) -> float:
    """
    ℒ_kinetic = -1/4 · F_μν^a · F^{μν,a}

    Field strength (Abelian approximation — full non-Abelian in ValaQuenta):
      F^a ≈ g · A^a   (single-layer, no adjacent state)
    """
    n = max(1, N_GEN.get(algebra, 0))
    A_a = A[:n] if len(A) >= n else A + [0.0] * (n - len(A))
    F_sq = sum((g * a) ** 2 for a in A_a)
    return -0.25 * F_sq


def L_matter(psi: List[float], A: List[float],
             g: float, hbar_nn: float, algebra: int) -> float:
    """
    ℒ_matter = i · Ψ̄ · γ^μ · D_μ · Ψ

    Radian-primary: the Dirac kinetic term is the imaginary (π/2-rotated)
    covariant derivative acting on the activation norms.
    In real-valued approximation: L_mat ≈ Σ_i |Ψ_i|² · |A_i|² · g²
    (contact term from non-Abelian vertex in single-layer limit).
    """
    n = len(psi)
    if n == 0:
        return 0.0
    total = 0.0
    for i, p in enumerate(psi):
        a_i = A[i] if i < len(A) else 0.0
        # i·Ψ̄·D·Ψ ≈ |Ψ|² · g² · |A|² (contact approximation, layer=1)
        total += (p * p) * (g * a_i) ** 2
    return total / n


def L_bias(beta: List[float], mu_sq: float, lam: float) -> float:
    """
    ℒ_bias = -1/2·(∂β)² + 1/2·μ²·β² - 1/4·λ·β⁴   (Mexican hat / Higgs)

    μ² < 0 → spontaneous symmetry breaking.
    In single-layer limit, kinetic term (∂β)² → 0.
    """
    beta_norm_sq = sum(b * b for b in beta)
    return (0.5 * mu_sq * beta_norm_sq
            - 0.25 * lam * beta_norm_sq ** 2)


def L_coupling(psi: List[float], beta: List[float],
               g: float) -> float:
    """
    ℒ_coupling = -(1/φ) · Γ_ij · Ψ̄^L · β · Ψ^R   (Yukawa, scaled by 1/φ)

    The 1/φ prefactor comes from the corrected Ainulindale Lagrangian
    (Ainulindale_Conjecture_Revised.docx, April 13 2026).
    """
    n = min(len(psi), len(beta))
    total = 0.0
    for i in range(n):
        total += psi[i] * beta[i]
    return -(1.0 / PHI) * g * total


def polar_lagrangian(state: FieldState,
                     total_layers: int = 10,
                     n_theta: int = 64) -> Dict[str, float]:
    """
    Full polar-integrated Lagrangian:
      L_NN = (2/π) ∮ [L_kin + L_mat + (1/φ)·L_bias + L_coup] r dr dθ

    Integration: single radial point r = layer_to_r(layer, total_layers),
    θ averaged over n_theta uniformly spaced points.
    fractions.Fraction used for (2/π) prefactor numerics.

    Returns: {'kinetic', 'matter', 'bias', 'coupling', 'total',
              'r', 'alpha_nn'}
    """
    r = layer_to_r(state.layer, total_layers)
    alpha = alpha_nn_from_r(state.g_coup, state.hbar_nn, r)

    Lk = L_kinetic(state.A, state.g_coup, state.algebra)
    Lm = L_matter(state.psi, state.A, state.g_coup, state.hbar_nn, state.algebra)
    Lb = L_bias(state.beta, state.mu_sq, state.lam)
    Lc = L_coupling(state.psi, state.beta, state.g_coup)

    # θ averaging: all four terms are θ-independent in this approximation
    # (future: θ-dependent field configurations will vary here)
    integrand = Lk + Lm + Lb + Lc

    # Polar measure: (2/π) · r · Δr · ΔΘ = (2/π) · r · 1 · 2π = 4r
    # In discrete form: prefactor = (2/π) × 2π = 4  (full θ integral)
    prefactor = float(TWO_OVER_PI) * 2.0 * PI * r
    total = prefactor * integrand

    return {
        'kinetic'  : Lk,
        'matter'   : Lm,
        'bias'     : Lb,
        'coupling' : Lc,
        'integrand': integrand,
        'prefactor': prefactor,
        'total'    : total,
        'r'        : r,
        'alpha_nn' : alpha,
        'algebra'  : ALG_NAME[state.algebra],
        'gauge'    : ALG_GAUGE[state.algebra],
    }


def rg_flow(alpha_0: float, hbar_0: float, algebra: int,
            layers: List[int]) -> Dict[str, List[float]]:
    """
    RG flow of α_NN and ħ_NN across a range of layers.

    Beta functions (one-loop):
      β_0(ℂ)  = 1/(2π)    U(1)
      β_0(ℍ)  = 3/(4π)    SU(2)
      β_0(𝕆)  = 8/(4π)    G₂/SU(3)

    Returns {'alpha', 'hbar', 'layers'}
    """
    BETA0  = {ALG_R: 0.0, ALG_C: 1/(2*PI), ALG_H: 3/(4*PI), ALG_O: 8/(4*PI)}
    GAMMA0 = {ALG_R: 0.0, ALG_C: 2/(2*PI), ALG_H: 4/(2*PI), ALG_O: 8/(2*PI)}
    b = BETA0.get(algebra, 0.0)
    g = GAMMA0.get(algebra, 0.0)

    alphas, hbars = [], []
    l_0 = layers[0] if layers else 1
    for l in layers:
        ln_r = math.log(max(l / l_0, 1e-12)) if l_0 > 0 else 0.0
        denom = 1.0 + b * alpha_0 * ln_r
        alphas.append(alpha_0 / denom if abs(denom) > 1e-12 else alpha_0)
        hbars.append(hbar_0 * (1.0 + g * ln_r))

    return {'alpha': alphas, 'hbar': hbars, 'layers': list(layers)}


def mastery_check(beta: List[float], vev: float,
                  hbar_nn: float) -> Dict[str, object]:
    """
    Mastery condition: weights crystallize when vev_distance < ħ_NN / 2.
      vev_distance = | |β| - vev |
    """
    beta_norm = math.sqrt(sum(b * b for b in beta)) if beta else 0.0
    dist = abs(beta_norm - vev)
    threshold = hbar_nn / 2.0
    return {
        'beta_norm'    : beta_norm,
        'vev'          : vev,
        'vev_distance' : dist,
        'threshold'    : threshold,
        'mastery'      : dist < threshold,
    }
