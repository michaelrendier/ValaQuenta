"""The Witch's Hat engine core: focus closed form, size/depth independence, aim and defocus, energy regimes, exchange-hole hats, zeta pair correlation, plain-data snapshots."""
import math
import os
import numpy as np
import pytest

from ValaQuenta.modules.witches_hat import maths as M

ZEROS = os.path.expanduser("~/Projects/ThePlace/RiemannHypothesisProof/data/zeros_1_to_3600.csv")


def test_focus_closed_form_small_angle():
    assert M.verify()["focus_closed_form_relerr"] < 1e-4


def test_hat_normalisation_every_shape():
    for sh in ("quartic", "fermion1d", "fermion2d", "fermion3d", "dog"):
        V, _ = M.hat_shape(sh)
        assert abs(float(V(0.0))) < 1e-6 and abs(float(V(1.0)) + 1) < 5e-3, sh


def test_standard_model_numbers():
    s = M.sm_hat()
    assert abs(s["lam"] - 0.12938) < 1e-4 and abs(s["Vpp_brim"] - M.M_H**2) < 1e-6
    assert abs(s["m_h_over_v"] - 0.50869) < 1e-4


def test_size_and_depth_drop_out_of_the_resolution():
    a = M.snapshot("quartic", 4, size=1.0, depth=1.0, aim=0.2, spread=0.0, n_psi=1, n_phi=4)
    b = M.snapshot("quartic", 4, size=7.0, depth=0.2, aim=0.2, spread=0.0, n_psi=1, n_phi=4)
    assert abs(a["focus_radius"]/a["size"] - b["focus_radius"]/b["size"]) < 1e-9


def test_point_focus_only_at_zero_aim_and_ring_otherwise():
    d = M.defocus_curve("quartic", 4, 0.0, aims=[0, 0.05, 0.1, 0.2])
    assert d["ring_radius"][0] < 1e-3
    assert np.all(np.diff(d["ring_radius"]) > 0)


def test_energy_regimes_reflected_point_through():
    rows = {r["E"]: r for r in M.energy_regimes("quartic", 4)}
    assert rows[-0.1]["regime"] == "reflected" and abs(rows[-0.1]["r_min"] - 0.2265) < 2e-3
    assert rows[0.0]["regime"] == "point" and rows[0.0]["r_min"] < 1e-3
    assert rows[0.5]["regime"] == "through"


def test_focus_resolution_rises_with_the_exponent():
    r = [M.focus_resolution("quartic", n) for n in (2.5, 4, 10, 20)]
    assert all(r[i] < r[i + 1] for i in range(3))


def test_fermion_hole_is_a_hat_and_boson_is_a_well():
    for kind in ("fermion1d", "fermion2d", "fermion3d"):
        g = M.pair_correlation(kind, np.array([0.0, 0.5, 2.0]))
        assert g[0] < 1e-6 and g[1] < g[2] + 0.2
    b = M.pair_correlation("boson", np.array([0.0, 3.0]))
    assert b[0] > 1.9 and abs(b[1] - 1) < 1e-3
    V, _ = M.hat_shape("boson"); assert float(V(0.0)) < float(V(1.0))


def test_fermion_hats_are_craters_not_sombreros():
    rows = {r["shape"]: r for r in M.shape_table()}
    assert rows["quartic"]["outer_wall"] is True
    assert rows["fermion3d"]["outer_wall"] is False


@pytest.mark.skipif(not os.path.exists(ZEROS), reason="needs RiemannHypothesisProof/data/zeros_1_to_3600.csv")
def test_zeta_pair_correlation_is_the_fermion_kernel_not_poisson():
    g = np.loadtxt(ZEROS, comments="#")
    u, R2 = M.zeta_pair_correlation(g[300:], 3.0, 30)
    sk = M.pair_correlation("fermion1d", u)
    assert np.sqrt(np.mean((R2 - sk)**2)) < 0.1 < np.sqrt(np.mean((R2 - 1)**2))


def test_snapshot_is_plain_data():
    s = M.snapshot("quartic", 4, n_psi=3, n_phi=4)
    assert isinstance(s["paths"], list) and set(s["paths"][0]) >= {"x", "y", "z", "W"}
    assert len(s["surface_r"]) == len(s["surface_z"])
