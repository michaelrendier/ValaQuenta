"""
ainulindale_engine.modules.scale
===================================
THE SCALE -- decompositional analysis, forwards and backwards.

SCALE is tier-0 (ADD, SCALE, SIGN) -- the most complicated of the three
generational-lineage irreducibles, because pulling it out of a quantity
and studying what is left over (the invariant) is a genuinely different
question depending on the level you ask it at: one point (polar decompose/
recompose, exact), a fold of two-ring readings (the cross-ratio survives
every anchor; the raw angle, tested first, does not), or a whole process
(pathway_decompose, RSA CRT-decrypt as the control case for a genuine
dependency fan-out).

Version: 0.1
"""

from .tools import ScaleModule
from .maths import (
    polar_decompose, polar_recompose, verify_polar_round_trip,
    scale_invariance_under_self_rescale,
    mobius_fold, scale_factor, verify_no_caustic,
    cross_ratio, verify_cross_ratio_is_scale_blind,
    two_ring_point, custom_ring_chart, custom_ring_chart_series,
    fold_is_log_tanh, unfold_is_arctanh_exp, verify_fold_unfold_round_trip,
    verify_locally_square,
    ProcessOperator, pathway_decompose,
    SED_DIM,
)
