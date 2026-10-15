"""The addition-matrix engine: the matrix, the column rotors, the law of the factor search, the K = 0 address."""
import importlib.util
import os
import random
import sys
from math import gcd

import pytest

from ValaQuenta.modules.addition_matrix import maths as M


def test_matrix_matches_python_product_and_carries_are_bits():
    rnd = random.Random(0)
    cases = [(0, 0), (1, 10 ** 10 - 1), (10 ** 10 - 1, 10 ** 10 - 1)] + [(rnd.randrange(10 ** 10), rnd.randrange(10 ** 10)) for _ in range(100)]
    for a, b in cases:
        carries, product = M.carry_matrix(a, b)
        assert product == a * b
        assert max(max(r) for r in carries) <= 1


def test_column_period_exact():
    for num1 in (1, 2, 3, 5, 7, 12, 25, 64, 625, 1000):
        for c in range(3):
            assert M.column_period(num1, c) == M.column_period_measured(num1, c)


def test_crt_rule_for_every_unit_affine_map():
    for m in (1, 2, 3):
        M10 = 10 ** m
        bad = [(a, b) for a in range(1, M10) if gcd(a, 10) == 1 for b in range(0, M10, max(1, M10 // 40)) if not M.crt_rule_check(a, b, m)]
        assert not bad


def test_odometer_first_return_is_odometer():
    for m in (2, 3, 4):
        assert M.odometer_first_return(m)["is_odometer_one_scale_down"]
        assert M.affine_cycle_type(1, 1, 10 ** m) == {10 ** m: 1}


def test_solenoid_cycle_lengths_are_powers_of_two():
    for a in (1, 3, 5, 7, 11):
        for b in (0, 1, 3):
            assert all(l & (l - 1) == 0 for l in M.solenoid_cycles(a, b, 8))


def test_closed_form_matches_enumeration_exhaustively():
    for k in (1, 2, 3):
        for N in range(0, 10 ** k * 2 + 50):
            assert M.solution_count_closed(N, k) == M.solution_count_brute(N, k), (N, k)
    for N in (420, 850, 5100, 10 ** 4, 2 ** 10 * 5 ** 3):
        for k in (1, 2, 3):
            assert M.solution_count_closed(N, k) == M.solution_count_brute(N, k), (N, k)


def test_live_states_equal_the_closed_form_below_n():
    for N, n in ((3233, 2), (14351, 3), (420, 2), (850, 2), (5100, 2), (1022117, 4)):
        live = M.live_state_counts(N, n)
        assert live[:n] == [M.solution_count_closed(N, c + 1) for c in range(n)], (N, n, live)


def test_search_ends_with_the_true_pair_and_its_swap():
    for p, q in ((53, 61), (113, 127), (1009, 1013)):
        n = len(str(max(p, q)))
        assert M.live_state_counts(p * q, n)[-1] == 2


def test_unit_group_tower_x10_and_uniform_branching():
    assert [M.unit_group_order(k) for k in (1, 2, 3, 4)] == [4, 40, 400, 4000]
    assert M.lift_branching(14351, 2) == {10: 400 // 10}
    assert M.lift_branching(3233, 1) == {10: 4}
    assert M.torsor_orbits(14351, 3) == 1 and M.torsor_orbits(420, 3) == 6 and M.torsor_orbits(420, 2) is None


def test_K_zero_is_the_true_pair_and_not_isolated():
    prof = M.address_profile(101 * 103, 3)
    assert prof["zero_overflow_pairs"] == [(101, 103), (103, 101)]
    assert prof["smallest_nonzero_K"] >= 1 and prof["solutions"] == 400
    with pytest.raises(ValueError):
        M.unit_solutions(420, 2)


def _explorer():
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.environ.get("MME_PATH", ""), os.path.join(here, "..", "..", "MultiplicationMatrixExplorer")):
        if cand and os.path.exists(os.path.join(cand, "matrix_math.py")):
            return cand
    return None


@pytest.mark.skipif(_explorer() is None, reason="Multiplication Matrix Explorer not found (set MME_PATH)")
def test_agrees_with_the_explorer():
    path = _explorer()
    def load(name):
        spec = importlib.util.spec_from_file_location(name, os.path.join(path, name + ".py"))
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod
    mm, fr = load("matrix_math"), load("factor_reconstruction")
    rnd = random.Random(5)
    for _ in range(30):
        a, b = rnd.randrange(10 ** 10), rnd.randrange(10 ** 10)
        tr = mm.trace_multiplication(a, b)
        carries, product = M.carry_matrix(a, b)
        assert tr.product == product
        assert [s.carry_out for s in tr.steps] == carries
        assert [s.row_digits for s in tr.steps] == M.matrix_rows(a, b)
    for N, n in ((3233, 2), (14351, 3), (420, 2), (1022117, 4)):
        hist = fr.factor_search(N, n)["history"]
        assert [h[2] for h in hist] == M.live_state_counts(N, n)
