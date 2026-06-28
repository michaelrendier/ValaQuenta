"""
ainulindale_engine.modules.noether_information.maths
======================================================
Information current J_info — Noether current for information symmetry.

Conserved under information-translation symmetry of L_NN:
  J_info^μ = ∂ℒ/∂(∂_μΦ) · δΦ

Key quantities:
  I_information : total information content of activation field
  Phi_flux      : information flux through algebra boundary
  t_e           : entropic time — layer step where I_info is maximal
  Delta_J_info  : cycle-averaged information current violation

Entropic arrow: ∂_l I_info ≥ 0  (information grows with layer depth
until sedenion boundary).

Version: 0.111
"""

import math
from typing import List, Dict, Any, Optional


# ── Constants ──────────────────────────────────────────────────────────────────

LN2  = math.log(2.0)
PHI  = (1 + math.sqrt(5)) / 2
ALG_R, ALG_C, ALG_H, ALG_O = 0, 1, 2, 3
ALG_NAME  = {ALG_R:'ℝ', ALG_C:'ℂ', ALG_H:'ℍ', ALG_O:'𝕆'}
ALG_DIM   = {ALG_R:1,   ALG_C:2,   ALG_H:4,   ALG_O:8}


# ── Information measures ───────────────────────────────────────────────────────

def shannon_information(psi_norms: List[float]) -> float:
    """
    I_information = -Σ_i p_i · log₂(p_i)   (Shannon entropy in bits)

    p_i = |Ψ_i|² / Σ_j|Ψ_j|²  (activation probability distribution)
    """
    norm_sq = sum(p * p for p in psi_norms)
    if norm_sq < 1e-12:
        return 0.0
    probs = [p * p / norm_sq for p in psi_norms]
    return -sum(pp * math.log2(pp) for pp in probs if pp > 1e-12)


def phi_flux(psi_norms: List[float], algebra: int) -> float:
    """
    Φ_flux = (dim of algebra) · |Ψ̄·Ψ| / n_neurons

    Information flux through an algebra boundary is proportional to
    the algebra dimension (the information capacity of that stratum).
    """
    dim = ALG_DIM.get(algebra, 1)
    psi_sq_mean = sum(p * p for p in psi_norms) / max(len(psi_norms), 1)
    return dim * psi_sq_mean


def information_current(psi_norms: List[float],
                         algebra: int,
                         layer: int,
                         total_layers: int = 10) -> Dict[str, float]:
    """
    J_info^μ — information current at a given layer.

    Components:
      J_info^0   : temporal (layer) component = dI/dl  (entropic arrow)
      J_info^1   : spatial component = Φ_flux
      I_info     : total information (Shannon entropy, bits)
      t_e        : entropic time estimate = argmax I_info ~ layer/total_layers
    """
    I = shannon_information(psi_norms)
    flux = phi_flux(psi_norms, algebra)

    # Temporal component: I changes with layer
    # In single-layer limit: J^0 ≈ I / layer
    J0 = I / max(layer, 1)

    # Entropic time: normalised layer position
    t_e = layer / max(total_layers, 1)

    # Entropic arrow: positive dI/dl means information growing (healthy)
    # At sedenion boundary (t_e → 1), information saturates

    return {
        'J_info_0'    : J0,
        'J_info_1'    : flux,
        'I_info'      : I,
        'Phi_flux'    : flux,
        't_e'         : t_e,
        'algebra'     : ALG_NAME.get(algebra, str(algebra)),
        'layer'       : layer,
        'total_layers': total_layers,
        'n_neurons'   : len(psi_norms),
    }


def entropic_arrow(psi_history: List[List[float]],
                   algebra: int) -> Dict[str, Any]:
    """
    Track information current across layer history.
    Verify entropic arrow: ∂_l I_info ≥ 0

    psi_history: list of psi_norms, one per layer step.
    Returns: I_values, J0_values, arrow_violations, t_e_max
    """
    I_vals = [shannon_information(p) for p in psi_history]
    J0_vals = [I / max(i+1, 1) for i, I in enumerate(I_vals)]

    # Arrow violations: layers where I decreases
    violations = [
        i for i in range(1, len(I_vals))
        if I_vals[i] < I_vals[i-1] - 1e-9
    ]

    t_e_max = I_vals.index(max(I_vals)) if I_vals else 0

    return {
        'I_values'        : I_vals,
        'J0_values'       : J0_vals,
        'arrow_violations': violations,
        'n_violations'    : len(violations),
        't_e_max'         : t_e_max,
        'arrow_holds'     : len(violations) == 0,
        'I_final'         : I_vals[-1] if I_vals else 0.0,
        'I_peak'          : max(I_vals) if I_vals else 0.0,
    }


def delta_J_info(J_curr: Dict[str, float],
                  J_prev: Optional[Dict[str, float]]) -> float:
    """
    Cycle-averaged information current violation:
      ΔJ_info = |J_info^0_curr - J_info^0_prev|

    Zero → information current conserved (entropic symmetry unbroken).
    """
    if J_prev is None:
        return 0.0
    return abs(J_curr.get('J_info_0', 0.0) - J_prev.get('J_info_0', 0.0))


def information_capacity(algebra: int, n_neurons: int) -> Dict[str, float]:
    """
    Maximum information capacity of a layer at the given algebra stratum.

    C_max = n_neurons × log₂(dim_algebra)  bits

    At ℝ: log₂(1) = 0 — no information storage (real scalar)
    At ℂ: log₂(2) = 1 — 1 bit per neuron
    At ℍ: log₂(4) = 2 — 2 bits per neuron
    At 𝕆: log₂(8) = 3 — 3 bits per neuron

    The sedenion shell (dims 8–15) does NOT add capacity because
    zero-divisors make the norm not multiplicative — information leaks.
    """
    dim = ALG_DIM.get(algebra, 1)
    bits_per_neuron = math.log2(max(dim, 1))
    return {
        'algebra'        : ALG_NAME.get(algebra, str(algebra)),
        'algebra_dim'    : dim,
        'n_neurons'      : n_neurons,
        'bits_per_neuron': bits_per_neuron,
        'C_max_bits'     : n_neurons * bits_per_neuron,
        'sedenion_note'  : 'Sedenion shell excluded — zero-divisors break norm',
    }
