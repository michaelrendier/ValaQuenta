"""Tests for modules/constants (engine 2): the identities, the single source for d*, A_pi and alpha, and the superseded readings."""
import math

from ValaQuenta.engine import constants as C
from ValaQuenta.modules.constants import maths as M
from ValaQuenta.modules.constants.tools import ConstantsModule


def test_every_equation_runs_argument_free():
    mod = ConstantsModule()
    for eq in mod.formulary():
        assert isinstance(mod.run(eq.name, {})["result"], dict), eq.name


def test_identities():
    assert M.euler_identity()["holds"]
    assert M.derive_phi()["factorisation_holds"]
    assert abs(M.derive_phi()["fibonacci_identity"]["φ²=φ+1 residual"]) < 1e-12


def test_a_pi_is_lambert_w_one():
    r = M.derive_omega_zs()
    assert abs(r["value"] - C.A_PI) < 1e-15
    assert abs(C.A_PI * math.exp(C.A_PI) - 1.0) < 1e-14


def test_alpha_single_source():
    assert abs(M.derive_alpha_fermat()["value"] - C.ALPHA_FS) < 1e-15


def test_d_star_four_faces_single_source():
    r = M.derive_d_star()
    assert r["faces"]["d*"]["value"] == C.D_STAR
    assert r["faces"]["d*_RG"]["value"] is None            # OPEN: never given a number
    assert abs(C.D_STAR_TAUT * math.log(10) - C.A_PI) < 1e-12
    assert abs(r["residual"]["A_π − d*·ln10"] - C.D_STAR_GAP) < 1e-8


def test_d_star_superseded_tower_is_recorded_not_computed():
    r = M.derive_d_star()
    assert "tower_claim" not in r and "four_values" not in r
    assert "BAO" in r["superseded"]                         # the withdrawn label is named, as the record


def test_confidence_floor_is_the_lowest_tier():
    assert ConstantsModule().confidence_floor == "THEORETICAL"
