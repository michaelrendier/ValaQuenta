"""
ainulindale_engine.modules.archimedes_screw
==============================================
The Archimedes Screw -- Prime Coordinate Engine

0_RB is the water. The screw is the logarithm: the machine that turns
rotation into lift, one pitch of ln p per prime.

Version: 0.1
"""

from .tools import ArchimedesScrewModule
from .maths import (
    lambert_w, screw_pitch, u_axis, digits_of,
    li, prime_count_log10, nth_prime_estimate,
    zero_count_smooth, zero_height_lambert, zero_height, zeros_upto,
    mean_gap, total_spaces, gap_at_zero_scale,
    von_mangoldt, chebyshev_psi_exact, chebyshev_psi_explicit,
    leaf_drops, tone, tone_sum, interference_profile,
    amplitude_envelope, envelope_ratio,
    kronecker, fundamental_discriminant, splitting_type,
    splitting_vector, ramified_primes,
    screw_coordinates, shake_order,
    OMEGA_ZS, ZEROS_KNOWN,
)
