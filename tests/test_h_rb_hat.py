"""h_rb_hat and engine.constants: the four faces of d*, the single source of the constants, and the 16 equations."""
import math

from ValaQuenta.engine import constants as C
from ValaQuenta.modules.h_rb_hat import maths as M


def test_four_faces_of_dstar():
    f = C.dstar_faces()
    assert f["d*"]["value"] == 0.24600                      # the value the code runs with
    assert abs(f["d*_taut"]["value"] - 0.246307201473) < 1e-12
    assert f["d*_RG"]["value"] is None and f["d*_RG"]["dimension"] == 8   # numeric OPEN
    assert abs(f["d*_ln(10)"]["value"] - 0.5671432904097838) < 1e-15
    assert abs(f["d*_taut"]["value"] * math.log(10) - f["d*_ln(10)"]["value"]) < 1e-15   # closure


def test_a_pi_is_lambert_w_of_one():
    assert abs(C.A_PI * math.exp(C.A_PI) - 1.0) < 1e-15
    assert C.OMEGA_ZS == C.A_PI                              # deprecated alias
    assert abs(C.ALPHA_FS - 1 / 137.035999084) < 1e-15


def test_h_rb_hat_uses_the_single_source():
    assert M.D_STAR is C.D_STAR and M.A_PI == C.A_PI


def test_comment_block_lists_all_four_and_the_story():
    b = C.dstar_comment_block()
    for key in ("d*  ", "d*_taut", "d*_RG", "d*_ln(10)", "Full story of d*"):
        assert key in b


def test_sigma_half_facets_share_the_coupling_sum():
    qm, rz = M.facet_quantum_mechanics(), M.facet_riemann_zeta()
    assert qm["sigma"] == rz["sigma"] == 0.5
    assert abs(qm["coupling_sum"] - 4.989633250806095) < 1e-12 and qm["coupling_sum"] == rz["coupling_sum"]
