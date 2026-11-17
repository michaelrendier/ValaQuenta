"""The Circle Atlas: viewports close on the circle (or fail as recorded), FROM carries its fibre, the sign test, the census, the import probe."""
import math
import pytest

from ValaQuenta.modules.circle_atlas import maths as M


def test_verify_all_checks_pass():
    bad = [k for k, v in M.verify().items() if v is not True]
    assert bad == []


def test_berry_keating_raw_is_not_a_circle_but_wick_is():
    e = M.entry("berry_keating")
    assert e["to"]["ok"] is False and e["to"]["residual"] > 0.1
    assert e["to"]["ok_transformed"] is True and e["to"]["residual_transformed"] < 1e-12


def test_sedenion_has_fifteen_exact_circles_and_336_annihilating_pairs():
    e = M.entry("sedenion")
    assert e["to"]["axes"] == 15 and e["to"]["residual"] < 1e-12
    assert e["from"]["annihilating_ordered_pairs"] == 336


def test_sign_is_carried_by_the_second_octonion():
    assert M.sign_carriers()["carriers"] == list(range(8, 16))


def test_lagrangian_fibre_is_not_a_single_inverse():
    f = M.entry("lagrangian")["from"]
    assert f["ok"] and "L + d/dt" in f["fibre"]


def test_cardioid_multiplier_lies_on_the_circle_and_has_two_epicycles():
    assert M.entry("cardioid")["to"]["residual"] < 1e-12
    assert M.entry("epicycles")["from"]["nonzero_coefficients_cardioid"] == 2


def test_inversion_fixes_the_unit_circle():
    assert M.entry("inversion")["to"]["fixed_set_residual"] < 1e-12


def test_every_viewport_pi_route_is_a_real_route():
    from ValaQuenta.modules.pi_derivations import maths as PI
    for k, v in M.VIEWPORTS.items():
        assert v["pi"] is None or v["pi"] in PI.ROUTES, k


def test_gaps_are_reported_not_hidden():
    g = M.gaps()
    assert "apollonian" in g["no_pi_route"] and g["named_gaps"]


def test_census_counts_this_repository():
    c = M.census(["ValaQuenta"])
    assert c["ValaQuenta"]["files"] > 100 and c["ValaQuenta"]["tokens"]["pi"] > 0


def test_import_probe_records_without_raising():
    r = M.import_probe()
    assert len(r["ok"]) > 40 and isinstance(r["failed"], list)


def test_second_pass_viewports_close():
    for k in ("sphere", "hypersphere", "field_axis", "native_units", "kite_spectrum"):
        e = M.entry(k)
        assert e["to"]["ok"] and e["from"]["ok"], k


def test_n_ball_peaks_and_recursion():
    t = M.ball_table()
    assert t["peak_volume_dim"] == 5 and t["peak_area_dim"] == 7 and t["recursion_residual"] < 1e-12


def test_sedenion_sphere_is_not_closed_under_product():
    d = M.entry("hypersphere")["to"]["norm_defect_of_unit_products"]
    assert d[8] < 1e-12 and d[16] > 0.1


def test_kite_spectrum_lines_and_read_back():
    k = M.kite_spectrum()
    assert k["kites"] == 7 and k["single_signature_for_all_zd"] and k["nullspace_round_trip"] == "84/84"
    assert k["skew_residual_LT_plus_L"] == 0.0 and k["flow_is_periodic_zd"] is False


def test_real_component_law():
    assert M.real_component_effect()["all_laws_hold"]


def test_native_units_homomorphism():
    import cmath
    z, w = 1.7 - 0.3j, -0.4 + 2.2j
    a, b = M.native_coords(z * w); (a1, b1), (a2, b2) = M.native_coords(z), M.native_coords(w)
    assert abs(a - a1 - a2) < 1e-13 and abs(abs(b - b1 - b2) % 2) < 1e-12 or abs(abs(b - b1 - b2) - 2) < 1e-12
    assert abs(M.from_native(a1, b1) - z) < 1e-12


def test_anchor_splits_the_one_bare_spectrum():
    r = M.anchored_readings()
    assert r["same_for_every_anchor"] and r["class_sizes"] == [(2, 2, 4, 4, 8, 32, 32)] and len(r["constructs"]) == 3
