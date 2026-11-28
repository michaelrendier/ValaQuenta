"""add_scale_sign (engine 6): the Aff(1,R) value type, its exact group laws, the wiki's bracket table and its word/fold readout."""
import math
from fractions import Fraction as Fr
from itertools import product

import pytest

from ValaQuenta.modules.add_scale_sign import ASS, CAMSHAFT, compose, group_laws_exact, word

A, S, G = ASS.ADD(3), ASS.SCALE(2), ASS.SIGN(-1)


def key(e):
    return (e.add, e.scale, e.sign)


def comm(x, y):
    """Group commutator x⁻¹ y⁻¹ x y, the convention of wiki/add_scale_sign.md section 3."""
    return ~x @ ~y @ x @ y


def test_apply_is_sign_scale_x_plus_add():
    assert ASS(3.0, 2.5, -1)(4.0) == -1 * 2.5 * 4.0 + 3.0


def test_group_laws_hold_exactly_in_fraction_arithmetic():
    out = group_laws_exact()
    assert out["elements"] == 18 and out["triples"] == 5832
    assert all(out[k] for k in ("associative", "identity", "inverse", "sign_scale_commute",
                                "commutator_add_scale_is_translation", "commutator_add_sign_is_translation", "exact"))


def test_inverse_of_a_fraction_element_is_a_fraction_element():
    t = ASS(Fr(1, 3), Fr(5, 2), -1)
    inv = ~t
    assert (inv.add, inv.scale, inv.sign) == (Fr(1, 3) * Fr(2, 5), Fr(2, 5), -1)
    assert isinstance(inv.add, Fr) and isinstance(inv.scale, Fr)
    assert key(t @ inv) == (0, 1, 1)


def test_inverse_keeps_negative_zero_out_of_the_add():
    assert math.copysign(1.0, (~ASS(0.0, 2.0, -1)).add) > 0


def test_the_inverse_formula_in_the_toolbox_latex():
    a, s, g = 3.0, 2.5, -1
    assert key(~ASS(a, s, g)) == (-g * a / s, 1 / s, g)


def test_compose_is_left_to_right_and_the_camshaft_rebuilds_the_element():
    e = ASS(2.0, 3.0, -1)
    s, sc, ad = e.parts()
    assert key(ad @ sc @ s) == key(e)
    assert CAMSHAFT == ("SIGN", "SCALE", "ADD")
    assert key(compose(G, S, A)) == key(A @ S @ G)


def test_the_bracket_table_of_the_wiki():
    assert key(S @ G) == key(G @ S) == (0, 2, -1)                       # SIGN and SCALE commute
    assert key(G @ A) == (-3, 1, -1) and key(A @ G) == (3, 1, -1)        # the offset is reflected
    assert key(S @ A) == (6, 2, 1) and key(A @ S) == (3, 2, 1)
    assert key(comm(S, G)) == (0, 1, 1)
    assert key(comm(A, G)) == (-6, 1, 1)
    assert key(comm(A, S)) == (-1.5, 1, 1)


def test_the_noether_identity_lnF_minus_lnB_is_an_ass_element_applied_to_sigma_minus_half():
    for E, sigma in product((0.5, 2.0, 10.0), (0.0, 0.25, 0.5, 0.75, 1.0)):
        lhs = (-sigma * E) - (-(1 - sigma) * E)
        assert abs(lhs - ASS(0.0, 2 * E, -1)(sigma - 0.5)) < 1e-12


def test_u_is_a_readout_not_a_homomorphism():
    """u(a@b) ≠ u(a) + u(b) in general: the word's Σ runs over recorded steps, the element's u does not add."""
    a, b = ASS(1.5, 2.0, 1), ASS(0.5, 3.0, -1)
    assert abs((a @ b).u() - (a.u() + b.u())) > 0.5
    w = (a @ b).lineage("chrono")
    assert abs(w.u_sum_of_steps() - (a.u() + b.u())) < 1e-12 and abs(w.u_total() - w.u_sum_of_steps()) > 0.5


def test_firing_defect_is_g_minus_one_times_ln_s():
    for add, s, g in product((0.0, 2.0), (0.5, 1.0, 2.0, 10.0), (-1, 1)):
        w = ASS(add, s, g).lineage()
        assert abs(w.firing_defect() - (g - 1) * math.log(s)) < 1e-12
        assert w.additive() == (g == 1 or s == 1.0)


def test_flipping_sign_changes_u_by_minus_two_ln_s():
    for s in (0.5, 2.0, 10.0):
        assert abs(ASS(1.0, s, -1).u() - ASS(1.0, s, 1).u() - (-2 * math.log(s))) < 1e-12


def test_ground_has_u_zero_and_gamma_zero():
    g = ASS.GROUND
    assert g.is_ground() and g.u() == 0 and g.gamma() == 0 and g.to_smith()["at_now"]


def test_word_builds_the_pure_scale_with_that_word():
    assert abs(word(0.7).u() - 0.7) < 1e-12 and abs(word(0.7).gamma() - math.tanh(0.35)) < 1e-12


def test_inverse_reverses_and_inverts_the_record():
    e = compose(ASS.ADD(1.0), ASS.SCALE(4.0), ASS.SIGN(-1))
    assert [key(s) for s in (~e).steps] == [key(~s) for s in reversed(e.steps)]
    assert len(e.record()) == 3


def test_trajectory_and_the_flip_test_for_a_candidate_step():
    w = compose(ASS.ADD(1.0), ASS.ADD(-1.0)).lineage("chrono")
    assert w.trajectory(1.0) == (1.0, 2.0, 1.0)
    assert w.collisions(1.0) == [(0, 2, 1.0)]
    assert not w.would_collide(ASS.ADD(5.0)) and w.would_collide(ASS.ADD(0.0))


def test_the_constructors_reject_what_is_not_in_the_group():
    with pytest.raises(ValueError):
        ASS(0.0, -1.0, 1)
    with pytest.raises(ValueError):
        ASS(0.0, 1.0, 0)
    with pytest.raises(ValueError):
        ASS(0.0, 2.0, 1).residual("NOPE")
    with pytest.raises(ValueError):
        ASS(0.0, 2.0, 1).lineage("alphabetical")
