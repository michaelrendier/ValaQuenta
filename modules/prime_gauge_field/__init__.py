"""
ainulindale_engine.modules.prime_gauge_field
================================================
The Prime Gauge Field -- the Weyl-shaped local-scale connection built
directly from Smith's Gamma(s)=(s-1)/(s+1), and its curvature.

Origin: the 2026-09-21 gauge-field experiment
(`.claude/scratchpad/2026-09-21_smith_apollonian_uft_probe/`) found
Gamma's Schwarzian derivative exactly zero -- a single, fixed, global
Mobius map correctly carries no classical gauge curvature. "Gauge" is
Weyl's own word (1918): he tried to unify gravity and electromagnetism by
making SCALE a LOCAL freedom rather than a global constant, and it is
THAT connection's curvature this module tests, not the global map's.

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
