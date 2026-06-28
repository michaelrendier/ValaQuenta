"""
ainulindale_engine.engine
==========================
Core engine: constants, units, and module registry.

Version: 0.111
"""

from .constants import *
from .registry import (
    EquationModule, Equation, ModuleRegistry,
    get_registry, register, CONFIDENCE
)
from .units import (
    to_angular_frequency, to_frequency,
    to_radian_phase, to_cycle_phase,
    lagrangian_norm, apply_lagrangian_norm,
    inversion_transform, inversion_involution,
    ratio_to_fraction, fraction_to_float,
    algebra_to_radian_depth, algebra_depth_sequence,
)
