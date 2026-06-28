"""
ainulindale_engine.modules.spherical
=====================================
Spherical harmonics and resonant cavity mathematics.
Mode identification: J_N anti-Möbius period 2π → l=1 → Y₁⁰ → Re(s)=½.

Standing wave chain: Chladni → Courant → Tesla/Schumann → J_N → ζ(s).
"""

from .maths import (
    Y_lm,
    Y_10,
    assoc_legendre,
    node_latitudes,
    j_n_mode_identification,
    courant_check,
    schumann_frequencies,
    full_chain_report,
    J_N_STEP_ANGLE,
    J_N_PERIOD,
    J_N_ORDER,
    R_CAVITY_KM,
    F1_SCHUMANN,
)

__all__ = [
    'Y_lm',
    'Y_10',
    'assoc_legendre',
    'node_latitudes',
    'j_n_mode_identification',
    'courant_check',
    'schumann_frequencies',
    'full_chain_report',
    'J_N_STEP_ANGLE',
    'J_N_PERIOD',
    'J_N_ORDER',
    'R_CAVITY_KM',
    'F1_SCHUMANN',
]
