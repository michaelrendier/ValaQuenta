"""The arithmetic the README quotes, recomputed from its definition."""
import math

import pytest


def test_gap_is_recomputed_not_looked_up():
    from ValaQuenta import bao_mass_gap as b
    assert abs((b.OMEGA_ZS - b.D_STAR * b.LN10) - 0.000707357533248576) < 1e-15
    assert b.validate()["all_pass"]


def test_omega_is_lambert_w_of_one():
    from ValaQuenta import bao_mass_gap as b
    assert abs(b.OMEGA_ZS * math.exp(b.OMEGA_ZS) - 1.0) < 1e-15


@pytest.mark.parametrize("E,sigma0", [(0.0, 0.3), (0.5, 0.0), (10.0, 0.0), (100.0, 0.25),
                                       (1e3, 0.0), (1e4, -3.0), (745.0, -1.0)])
def test_forced_sigma_is_half_everywhere(E, sigma0):
    from ValaQuenta.noether import NoetherCurrents
    assert NoetherCurrents().forced_sigma(E, sigma0) == 0.5


def test_hamiltonian_conserves_E():
    from ValaQuenta.hamiltonian import HamiltonianXP
    h = HamiltonianXP()
    x, p = h.trajectory(1.0, 1.0, 1.0)
    assert abs(x * p - 1.0) < 1e-12
    assert h.scale_check(2, 3, lam=2.0)


def test_red_blue_sum_vanishes_only_on_the_locus():
    from ValaQuenta.hamiltonian import RedBlueHamiltonian
    rb = RedBlueHamiltonian()
    assert abs(rb.functional_equation_check(1.3, 0.7259587)) < 1e-4
    assert abs(rb.functional_equation_check(1.3, 1.0259587)) > 0.05


def test_box_kite_counts():
    from ValaQuenta.modules.box_kite import maths as bk
    assessors = [(a, b) for a in range(1, 8) for b in range(1, 8) if a != b and bk.is_assessor(a, b)]
    assert len(assessors) == 42
    assert all(bk.box_kite_graph(s)["is_octahedron"] for s in range(1, 8))


def test_bell_numbers_and_firing_orders():
    from ValaQuenta.modules.bracketing_firing_order import maths as bf
    assert [bf.bell_number(n) for n in range(6)] == [1, 1, 2, 5, 15, 52]
    assert bf.bell_number(16) == 10480142147
    assert bf.apply_firing_order(["Scale", "Sign", "Add"], (3, 1, 2)) == ["Add", "Scale", "Sign"]
