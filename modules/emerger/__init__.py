"""
ainulindale_engine.modules.emerger
====================================
The Emerger -- Sedenion Bracketing & Firing Order.

A dynamic permutative bracketer. Works in the imaginary domain; e_0 (the
real component) is the fixed anchor -- the tilt to the i axis -- never
bracketed, always the reference each group is paired against. A bracketing
is an ordered partition of the imaginary indices; each group + the anchor
spans a domain (C / H / O / FRAGMENT). The order the groups are approached
(the firing order) is load-bearing: each bracket is conditioned on the
ones before it. Order can be canonical (dependency), sigma_RB-phased, or
any permutation.

The ascent-dual of Generational Lineage: descent = what built this
(differentiate down, writing); ascent = what emerges and in what order
(integrate up, reading -- spectroscopy, factoral decomposition).

Version: 0.1
"""
from .tools import EmergerModule
from .maths import (
    SEDENION_DIM, REAL_ANCHOR, basis, cd_conj, cd_mul, norm_sq,
    left_matrix, mat_rank, is_zero_divisor, on_zd_equator, coerce_vec,
    sigma_rb, firing_phase, firing_order,
    STANDARD_BRACKETINGS, CANONICAL_ORDER, BRACKET_ROLE,
    domain_of, gain_class, legal_orders,
    emerge, scale_partitions, verify, lineage_report,
)

__all__ = ["EmergerModule"]
