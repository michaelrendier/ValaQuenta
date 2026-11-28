"""bracketing_firing_order (engine 7): the counts, the four orderings of brackets run on 16-component vectors, the two readings of a plan."""
import itertools
import math
import random
from fractions import Fraction as F

import numpy as np
import pytest

from ValaQuenta.modules.bracketing_firing_order import maths as bf
from ValaQuenta.modules.h_rb_hat import sigma16


def unit(k):
    return tuple(F(int(i == k)) for i in range(16))


def rand_vecs(n, seed):
    rng = random.Random(seed)
    return [tuple(F(rng.randint(-2, 2)) for _ in range(16)) for _ in range(n)]


def leaves_of(vs):
    return [bf.Leaf.of(chr(65 + i), v) for i, v in enumerate(vs)]


def test_bell_and_firing_counts():
    assert [bf.bell_number(n) for n in range(7)] == [1, 1, 2, 5, 15, 52, 203]
    assert bf.bell_number(16) == 10_480_142_147
    assert len(bf.set_partitions(list("abcd"))) == 15 and bf.firing_order_count(5) == 120
    assert bf.apply_firing_order(["Scale", "Sign", "Add"], (3, 1, 2)) == ["Add", "Scale", "Sign"]
    assert bf.bracketing_report(list(range(13)))["enumerable"] is False


def test_set_membership_and_jurisdiction():
    steps = [lambda x: x + 2, lambda x: x - 2]
    assert bf.collisions(steps, 1.0) == [(0, 2, 1.0)]
    assert bf.would_collide([steps[0]], steps[1], 1.0) and not bf.would_collide([steps[0]], lambda x: x + 5, 1.0)
    jm = {"lineage": {"descend"}, "emerger": {"build_up"}}
    assert bf.jurisdiction_violation("lineage", "build_up", jm)["violation"] is True
    assert bf.jurisdiction_violation("emerger", "build_up", jm)["violation"] is False


def test_the_exact_product_agrees_with_an_independent_float_one():
    """sigma16 builds its table from index arithmetic; this module doubles on the fly: two routes to one product."""
    rng = np.random.RandomState(5)
    for _ in range(10):
        a, b = rng.randint(-3, 4, 16), rng.randint(-3, 4, 16)
        assert np.allclose([float(v) for v in bf.sedenion_mul(a.tolist(), b.tolist())], sigma16.mul(a, b))
        assert np.allclose(np.array(bf.left_matrix(a.tolist()), dtype=float), sigma16.L(a))


def test_the_counts_of_the_four_orderings():
    for n in range(1, 8):
        c = bf.mode_counts(n)
        cat = math.comb(2 * (n - 1), n - 1) // n
        assert c == {"A": cat, "B": math.factorial(n), "C": cat * 2 ** (n - 1), "D": math.factorial(n) * cat}
        assert c["D"] == math.factorial(2 * n - 2) // math.factorial(n - 1)     # every ordered binary product of n labelled items
    for n in (2, 3, 4, 5):
        ls = [bf.Leaf(str(i)) for i in range(n)]
        c = bf.mode_counts(n)
        assert (len(bf.plans_bracketing(ls)), len(bf.plans_firing_order(ls)), len(bf.plans_firing_of_brackets(ls)),
                len(bf.plans_bracketing_of_firing(ls))) == (c["A"], c["B"], c["C"], c["D"])


def test_firing_orders_reached_by_each_kind():
    """A reaches one order; B and D reach all n!; C (written bracketing, orders at the brackets) reaches only the separable permutations: 6, 22, 90."""
    for n, sep in ((3, 6), (4, 22), (5, 90)):
        ls = [bf.Leaf(str(i)) for i in range(n)]
        assert [bf.reachable_orders(ls, m) for m in "ABCD"] == [1, math.factorial(n), sep, math.factorial(n)]


def test_generic_sedenions_give_a_different_output_for_every_plan_in_the_element_reading():
    r3 = bf.compare_modes(rand_vecs(3, 3))
    assert [(r3[m]["plans"], r3[m]["distinct_outputs"]) for m in "ABCD"] == [(2, 2), (6, 6), (8, 8), (12, 12)]
    r4 = bf.compare_modes(rand_vecs(4, 4))
    assert [(r4[m]["plans"], r4[m]["distinct_outputs"]) for m in "ABCD"] == [(5, 5), (24, 24), (40, 40), (120, 120)]


def test_every_plan_of_A_B_and_C_is_also_a_plan_of_D_by_value():
    """D is the whole universe of ordered products of n labelled items, so A, B and C are subsets of it."""
    ls = leaves_of(rand_vecs(4, 9))
    d = {bf.plan_value(p) for p in bf.plans_bracketing_of_firing(ls)}
    for make in (bf.plans_bracketing, bf.plans_firing_order, bf.plans_firing_of_brackets):
        assert {bf.plan_value(p) for p in make(ls)} <= d


def test_the_operator_reading_is_associative_so_only_the_firing_order_changes_it():
    vs, x = rand_vecs(4, 11), rand_vecs(1, 12)[0]
    r = bf.compare_modes(vs, "operator", x)
    assert r["A"]["distinct_outputs"] == 1                       # every bracketing at written order, one output
    assert r["B"]["distinct_outputs"] == 24                       # every firing order, its own output
    assert r["C"]["distinct_outputs"] == 22 and r["D"]["distinct_outputs"] == 24   # outputs follow the fire sequence only


def test_the_element_reading_is_not_associative():
    """(e_i e_j) e_k against e_i (e_j e_k) over the 455 triples of distinct imaginary basis units: 252 do not associate (computed with sigma16's own table, an independent route)."""
    e = np.eye(16)
    bad = [t for t in itertools.combinations(range(1, 16), 3)
           if not np.allclose(sigma16.mul(sigma16.mul(e[t[0]], e[t[1]]), e[t[2]]), sigma16.mul(e[t[0]], sigma16.mul(e[t[1]], e[t[2]])))]
    assert len(bad) == 252
    a, b, c = (bf.Leaf.of(n, unit(k)) for n, k in zip("abc", bad[0]))
    assert bf.plan_value(bf.Bracket([bf.Bracket([a, b]), c])) != bf.plan_value(bf.Bracket([a, bf.Bracket([b, c])]))


def test_notation_nesting_and_the_fire_sequence():
    ls = {n: bf.Leaf(n) for n in "ABC"}
    plan = bf.parse_plan("((A B | 2 1) C | 2 1)", ls)
    assert bf.notation(plan) == "((A B | 2 1) C | 2 1)" and bf.fire_sequence(plan) == ["C", "B", "A"]
    with pytest.raises(ValueError):
        bf.Bracket([ls["A"], ls["B"]], (1, 1))
    with pytest.raises(ValueError):
        bf.parse_plan("(A Z)", ls)


def test_the_operator_reading_of_a_nested_plan_is_the_matrices_in_fire_order():
    vs = rand_vecs(3, 21)
    L = {n: bf.Leaf.of(n, v) for n, v in zip("ABC", vs)}
    M = {n: L[n].matrix for n in "ABC"}
    plan = bf.parse_plan("((A B | 2 1) C | 2 1)", L)
    assert bf.plan_operator(plan) == bf._matmul(bf._matmul(M["A"], M["B"]), M["C"])     # C fires first, then B, then A


def test_evolve_operator_ends_at_the_output_and_starts_at_the_input():
    vs, x = rand_vecs(3, 31), rand_vecs(1, 32)[0]
    L = {n: bf.Leaf.of(n, v) for n, v in zip("ABC", vs)}
    plan = bf.parse_plan("((A B | 2 1) C | 2 1)", L)
    st = bf.evolve_operator(plan, x)
    assert [s[0] for s in st] == ["input", "C", "B", "A"] and st[0][1] == x and st[-1][1] == bf.apply_plan(plan, x)
    assert st[1][1] == bf.sedenion_mul(vs[2], x) and st[2][1] == bf.sedenion_mul(vs[1], st[1][1])     # each step is a left multiplication


def test_evolve_value_ends_at_the_value_and_names_each_product():
    vs = rand_vecs(3, 41)
    L = {n: bf.Leaf.of(n, v) for n, v in zip("ABC", vs)}
    plan = bf.parse_plan("((A B | 2 1) C | 2 1)", L)
    st = bf.evolve_value(plan)
    assert st[-1][1] == bf.plan_value(plan) and [s[0] for s in st] == ["C", "B", "A", "(B A)", "(C (B A))"]
    assert st[-1][1] == bf.sedenion_mul(vs[2], bf.sedenion_mul(vs[1], vs[0]))


def test_the_two_octonion_halves_of_a_sedenion():
    """L_a = R + I for the real-octonion half R and the imaginary-octonion half I, and the two firing orders of (R I) differ."""
    a = rand_vecs(1, 51)[0]
    R = bf.left_matrix(a[:8] + (F(0),) * 8)
    I = bf.left_matrix((F(0),) * 8 + a[8:])
    La = bf.left_matrix(a)
    assert all(La[r][c] == R[r][c] + I[r][c] for r in range(16) for c in range(16))
    assert bf._matmul(R, I) != bf._matmul(I, R)


def test_the_worked_example_of_the_wiki_differs_in_72_of_256_entries():
    a = tuple(F(x) for x in (1, 2, 0, 1, 0, 0, 3, 0, 0, 1, 0, 0, 2, 0, 0, 1))
    R, I = bf.left_matrix(a[:8] + (F(0),) * 8), bf.left_matrix((F(0),) * 8 + a[8:])
    d, e = bf._matmul(R, I), bf._matmul(I, R)
    assert sum(1 for r in range(16) for c in range(16) if d[r][c] != e[r][c]) == 72


def test_three_kinds_of_bracketing_at_sixteen_components():
    """Set partitions (Bell), contiguous blocks (compositions, the Emerger's {4:8:4}) and trees (Catalan) are three different counts."""
    assert bf.bell_number(16) == 10_480_142_147 and 2 ** 15 == 32768
    assert bf.mode_counts(16) == {"A": 9_694_845, "B": 20_922_789_888_000, "C": 317_680_680_960, "D": 202_843_204_931_727_360_000}


def test_the_hrb_hat_lift_b_is_a_one_leaf_plan_on_the_sixteen_component_input():
    """Ĥ_RB (lift B) is x ↦ L_C x: as a plan it is one leaf, and the output sedenion is the product C·σ_RB."""
    sig = np.array([0.5, 0.1, 0, 0, 0, 0, 0, 0, 0, 0.2, 0, 0, 0, 0, 0, 0.3])
    C = sigma16.coupling(sig, 10)
    out = np.array([float(v) for v in bf.apply_plan(bf.Leaf("H_RB", matrix=bf.left_matrix([F(float(c)) for c in C])), [F(float(s)) for s in sig])])
    assert np.allclose(out, sigma16.mul(C, sig), atol=1e-9)
