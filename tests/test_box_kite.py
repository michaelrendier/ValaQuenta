"""box_kite (engine 5): the sedenion zero-divisor geometry, re-derived independently of the module's own table where it can be."""
import math
import random

import pytest

from ValaQuenta.modules.box_kite import maths as bk


def cd_mul(x, y):
    """Independent Cayley-Dickson product on lists of floats: (a, b)(c, d) = (ac - d* b, d a + b c*)."""
    n = len(x)
    if n == 1:
        return [x[0] * y[0]]
    h = n // 2
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    conj = lambda v: [v[0]] + [-t for t in v[1:]] if len(v) > 1 else list(v)
    left = [p - q for p, q in zip(cd_mul(a, c), cd_mul(conj(d), b))]
    right = [p + q for p, q in zip(cd_mul(d, a), cd_mul(b, conj(c)))]
    return left + right


def test_multiplication_agrees_with_an_independent_cayley_dickson():
    rng = random.Random(7)
    for _ in range(20):
        x = [rng.uniform(-1, 1) for _ in range(16)]
        y = [rng.uniform(-1, 1) for _ in range(16)]
        mine = bk.multiply(x, y)
        ref = cd_mul(x, y)
        assert max(abs(p - q) for p, q in zip(mine, ref)) < 1e-12


def test_counts_are_derived_not_quoted():
    v = bk.verify_counts()
    for key, val in v.items():
        if key.endswith(tuple(("_expect_42", "_expect_84", "_expect_168", "_expect_336", "_expect_7"))) or key in ("all_verified_assessors", "aligned_planes_empty", "sizes_all_6"):
            assert val is True, key
    assert (v["assessors"], v["diagonals"], v["unit_points"], v["ordered_zd_pairs"], v["kills_per_diagonal"], v["box_kites"]) == (42, 84, 168, 336, 4, 7)
    assert v["psl27_order"] == 168


def test_each_box_kite_is_an_octahedron_with_the_closed_form_spectrum():
    for s in range(1, 8):
        g = bk.box_kite_graph(s)
        assert g["is_octahedron"]
        lap = [round(x, 9) + 0.0 for x in sorted(bk.chart_spectrum(s))]
        assert lap == [0, 4, 4, 4, 6, 6]


def test_associator_census():
    c = bk.associator_census()
    assert (c["total"], c["nonzero"], c["zero"]) == (4096, 1848, 2248)


def test_the_octonions_are_alternative_and_168_ordered_triples_are_not_associative():
    """Among imaginary octonion units the associator vanishes unless the three are distinct and not on one line: 168 of the 210 ordered triples."""
    n = 0
    for i in range(1, 8):
        for j in range(1, 8):
            for k in range(1, 8):
                if any(abs(t) > 1e-12 for t in bk.associator(i, j, k)):
                    n += 1
    assert n == 168


def test_the_labelled_group_is_8_times_168_and_acts_transitively_on_the_168_points():
    out = bk.labelled_automorphisms()
    assert out["fano_permutations"] == bk.psl27_order() == 168
    assert out["signed_automorphisms"] == 1344 and out["sign_kernel"] == 8
    assert out["extend_to_sedenions"] is True
    assert out["orbits_on_unit_points"] == [168] and out["point_stabiliser"] == 8


def test_e0_is_not_part_of_the_geometry():
    out = bk.e0_is_outside()
    assert out['e0_is_outside_the_geometry'] and out['e0_associator_always_vanishes']
    assert not out['e0_is_a_pg32_point'] and not out['e0_in_any_assessor']


def test_skeleton_counts_of_pg32():
    s = bk.skeleton_counts()
    assert (s["points"], s["lines"], s["planes"], s["plane_size"]) == (15, 35, 15, 7)
