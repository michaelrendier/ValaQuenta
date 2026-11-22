"""Tests for the Broca-Wernicke Rings Scale in ValaQuenta.modules.scale (2026-11-21)."""
import cmath
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ValaQuenta.modules.scale import (
    BW_CONVENTION, broca_wernicke_ring_chart, broca_wernicke_ring_series, two_pathways,
    spiral_similarity, verify_spiral_is_add_in_log_chart, custom_ring_chart, cross_ratio,
    mobius_fold, polar_decompose)

OBJ = {'w': 0.35, 'b': 4.0}
bro = lambda o: o['b']
wer = lambda o: o['w']


def test_axes_wernicke_horizontal_broca_vertical():
    pt = broca_wernicke_ring_chart(OBJ, bro, wer, 1.0)
    assert pt['Z'] == complex(0.35, 4.0)
    assert pt['wernicke'] == 0.35 and pt['broca'] == 4.0
    assert 'horizontal' in BW_CONVENTION and 'vertical' in BW_CONVENTION


def test_special_case_of_custom_ring_chart():
    a = broca_wernicke_ring_chart(OBJ, bro, wer, 1.0)
    b = custom_ring_chart(OBJ, wer, bro, 1.0)
    assert a['gamma'] == b['gamma'] and a['scale_factor'] == b['scale_factor']


def test_cross_ratio_survives_every_anchor():
    objs = [{'w': 0.2, 'b': 1.0}, {'w': 0.5, 'b': 3.0}, {'w': 0.9, 'b': 2.0}, {'w': 0.3, 'b': 5.0}]
    zs = [complex(o['w'], o['b']) for o in objs]
    base = cross_ratio(*zs)
    for Z0 in (1.0, 2.5 + 0.5j, 0.1):
        g = [mobius_fold(z, Z0) for z in zs]
        assert abs(cross_ratio(*g) - base) < 1e-9


def test_series_buckets_cells():
    objs = [{'w': 0.4, 'b': 1.2}, {'w': 0.45, 'b': 0.9}, {'w': 2.2, 'b': 3.1}]
    s = broca_wernicke_ring_series(objs, bro, wer, 1.0)
    assert len(s['readings']) == 3
    assert s['cells'][(0, 1)] == [0, 1] and s['cells'][(2, 3)] == [2]


def test_two_pathways_are_inverse_and_balance():
    for Z in (0.35 + 4j, 2.0 - 1.0j, 0.1 + 0.1j):
        p = two_pathways(Z, 1.3)
        assert p['balanced'] and p['involution']
        assert abs(p['gamma_outward'] + p['gamma_inward']) < 1e-12
    p = two_pathways(1.3 + 0j, 1.3)            # the matched load: both pathways sit at the centre
    assert abs(p['gamma_inward']) < 1e-12 and abs(p['gamma_outward']) < 1e-12


def test_spiral_similarity_is_add_in_log_chart():
    assert verify_spiral_is_add_in_log_chart()['holds']
    z = 2 + 1j
    w = spiral_similarity(z, 0.5, 0.3)
    (r0, t0), (r1, t1) = polar_decompose(z), polar_decompose(w)
    assert abs(r1 / r0 - 0.5) < 1e-12 and abs((t1 - t0) - 0.3) < 1e-12
