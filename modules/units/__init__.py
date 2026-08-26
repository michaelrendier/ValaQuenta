"""
ainulindale_engine.modules.units
===================================
UNITS -- dimensional exponent vectors as a fourth domain for this project's
factoral-decomposition discipline (numbers, processes, and now physical
units), plus THE EQUATION INDEX: a unit's dimension signature narrows the
space of candidate physical laws, the same move context_vector already
makes for words narrowing to candidate synsets.

Version: 0.1
"""

from .tools import UnitsModule
from .maths import (
    SI_BASE, unit_vector, unit_mul, unit_div, unit_pow,
    unit_lineage_decompose, LINEAGE_TABLE, verify_lineage_table,
    verify_cancellation, EQUATION_INDEX, equation_index_lookup,
)
