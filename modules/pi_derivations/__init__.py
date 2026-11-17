"""
ValaQuenta.modules.pi_derivations
=================================
The Pi Derivation Toolset, kept beside the 0_RB toolset (``h_rb_hat``): every route to π the project meets,
each computed without reading ``math.pi`` and each labelled with what of the circle its inputs already contain.
``cos_zero`` is the emergent π (twice the first positive zero of the cosine power series).

Version: 0.1
"""
from .tools import PiDerivationsModule
from .maths import (
    ROUTES, derive, all_routes, circle_audit, emergent_pi, verify,
    cos_zero, oscillator_period, archimedes, gregory_leibniz, machin, madhava, wallis, viete, basel, euler_product,
    coprime_probability, gaussian_integral, gamma_half, stirling_ratio, gauss_legendre, ramanujan_1_over_pi, chudnovsky,
    bbp_digit_sum, grid_circle_area, residue_square, cardioid_area, smith_arc_length, jacobi_conjugate_point,
    sedenion_exp_period, ring_eigenvalue, u1_normalisation,
)

__all__ = ["PiDerivationsModule"]
