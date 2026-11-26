"""The 16-component sigma_rb input of h_rb_hat (sigma16.py): exact identities and the measured direction classes. All CALCULATED."""
import numpy as np

from ValaQuenta.modules.h_rb_hat import maths as M
from ValaQuenta.modules.h_rb_hat import sigma16 as S

E = np.eye(16)


def test_known_zero_divisor_pair_and_L_spectrum():
    a, b = (E[1] + E[10]) / np.sqrt(2), (E[4] - E[15]) / np.sqrt(2)
    assert np.linalg.norm(S.mul(a, b)) < 1e-12
    sv = np.sort(S.invariants(S.L(a))["sv"])
    assert np.allclose(sv, np.sort([0.0] * 4 + [1.0] * 8 + [2 ** 0.5] * 4), atol=1e-9)   # the {4, 8, 4} split


def test_coupling_reproduces_the_scalar_engine():
    c = S.coupling(S.sigma_rb_vector(0.5))
    assert abs(c[0] - M.facet_quantum_mechanics()["coupling_sum"]) < 1e-12 and np.abs(c[1:]).max() < 1e-15


def test_asymmetry_is_beta_times_ad_of_the_direction():
    rng = np.random.default_rng(3)
    u = rng.normal(size=15)
    s = S.sigma_rb_vector(0.7, u, 2.3)
    uh = np.zeros(16)
    uh[1:] = u / np.linalg.norm(u)
    b = S.beta_alpha(0.7, 2.3)["beta"]
    assert np.abs(S.lift_b(s)["asym"] - b * (S.L(uh) - S.R(uh))).max() < 1e-12


def test_real_sigma_rb_has_zero_current_balance():
    assert np.abs(S.lift_b(S.sigma_rb_vector(1.0))["asym"]).max() < 1e-15      # H_RB = H_BR on the real axis


def test_lift_a_direction_is_a_gauge():
    assert S.lift_a_equivariance(0.5, 3.0) < 1e-12


def test_direction_classes_basis_and_pairs():
    atlas = [S.asym_of_unit(E[k])["rank"] for k in range(1, 16)]
    assert set(atlas) == {14}
    zd = 0
    for i in range(1, 16):
        for j in range(i + 1, 16):
            for sg in (1, -1):
                a = (E[i] + sg * E[j]) / np.sqrt(2)
                if S.zero_divisor_partners(a) == 4:
                    zd += 1
                    assert S.asym_of_unit(a)["rank"] == 10
    assert zd == 84                                                              # exactly the 84 known zero-divisor directions


def test_hrb_is_singular_only_at_zero_real_part_in_zero_divisor_directions():
    zd = (E[1] + E[10]) / np.sqrt(2)
    assert S.invariants(S.L(0.0 * E[0] + zd))["nullity"] == 4
    assert S.invariants(S.L(1.0 * E[0] + zd))["nullity"] == 0
    assert S.invariants(S.L(0.0 * E[0] + E[1]))["nullity"] == 0


def test_scalar_balance_does_not_depend_on_sigma_riemann():
    b = [M.sigma_rb_term(2, s, 1.0, 1.0)["balance"] for s in (0.5, 1.0, 2.0)]    # finding VQ-9: docstring says zero on the critical line
    assert max(b) - min(b) == 0
