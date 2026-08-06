"""
ainulindale_engine.modules.box_kite
======================================
The Box-Kite Debugger -- the zero-divisor geometry, made watchable.

The object is PSL(2,7), order 168, Aut(Fano plane) -- NOT G2. Moreno's
G2 homeomorphism is the continuous blow-up that forgets the labelling.
7 box-kites, each an octahedron, 6 Assessors apiece, 42 in all.

Version: 0.2
"""

from .tools import BoxKiteModule
from .maths import (
    cd_multiplication_table, basis_mul, multiply, is_zero, basis_vector,
    associator, commutator, associator_defect, associator_census,
    diagonals, is_assessor, assessors, strut, box_kites,
    zero_divisor_pairs, verify_counts,
    assessors_adjacent, box_kite_graph, chart_spectrum,
    glued_graph, glued_spectrum, associator_field, eigenvalues_symmetric,
    pg32_points, pg32_lines, fano_planes, psl27_order, skeleton_counts,
    e0_is_outside, SEDENION_DIM,
    index_chart_membership, skeleton_overlap, fixed_point_gluing,
    norm, fixed_point_weight, energy_split, diagonal_amplitudes,
    assessor_coordinates, chart_projection, nearest_assessor,
    local_curvature, chart_of, address_census,
)
