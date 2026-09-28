"""
ValaQuenta.modules.prime_gauge_field
====================================
The Prime Gauge Field -- the Weyl-shaped local-scale connection built
directly from Smith's Gamma(s)=(s-1)/(s+1), and its curvature.

Two candidate connections, one provably flat (any gradient of a
holomorphic scalar), one genuinely not (Gamma read as an R^2-valued
1-form rather than collapsed to a single complex scalar) -- see
maths.py for the full derivation.

Version: 0.1
"""
from .tools import PrimeGaugeFieldModule
from .maths import (
    gamma, dgamma, connection, curvature, curvature_numeric,
    log_potential_curvature, zero_locus_predicate, prediction_check,
    report, verify,
)

__all__ = ["PrimeGaugeFieldModule"]
