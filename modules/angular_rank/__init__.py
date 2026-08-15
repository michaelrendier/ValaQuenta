"""
ainulindale_engine.modules.angular_rank
==========================================
The 16D Oscilloscope -- angular content and subspace occupancy, measured on
a frozen epoch.

One instrument, two applications: the internal/external provenance test
(does the signal reach ker(L_a)?) and the language-agnostic angular-content
test (does the signal carry direction, or is it a scalar wearing 16
coordinates?). Same measurement both times.

Every entry point takes an Epoch, never a live sequence. Measuring a field
that the measured process is concurrently mutating is iterate-while-modify
and drifts silently -- see maths.py, THE EPOCH DISCIPLINE.

Version: 0.1
"""

from .tools import AngularRankModule
from .maths import (
    SEDENION_DIM, CALIBRATION, Epoch,
    snapshot, is_epoch,
    embed_log_bands,
    occupancy, singular_spectrum, numerical_rank, orthonormal_span,
    common_direction, angular_residual, score_against_calibration,
    left_mul_matrix, null_space, verify_null_space,
    null_occupancy, null_occupancy_baseline,
    external_component, principal_angles, precession,
    angular_report,
)
