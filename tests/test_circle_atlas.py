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
