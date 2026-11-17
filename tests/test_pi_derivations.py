"""The Pi Derivation Toolset: routes land, none reads math.pi, the emergent pi, the circle audit."""
import inspect
import math
import re

from ValaQuenta.modules.pi_derivations import maths as M


def test_every_route_within_tolerance():
    bad = [k for k, v in M.verify().items() if v is not True]
    assert bad == []


def test_emergent_pi_is_the_series_zero():
    d = M.emergent_pi()
    assert d["error"] < 1e-13 and d["circle_in"] == "none"


def test_u1_normalisation_is_an_identity_not_a_derivation():
    d = M.derive("u1_normalisation")
    assert d["circle_in"] == "identity" and math.isnan(d["value"])


def test_no_route_reads_math_pi():
    """Route bodies must not mention math.pi / np.pi / an imported pi constant (the comparison _REF lives outside them)."""
    for name, r in M.ROUTES.items():
        src = inspect.getsource(r["fn"])
        assert not re.search(r"math\.pi|np\.pi|numpy\.pi|\b_REF\b", src), name


def test_circle_audit_groups_every_route():
    a = M.circle_audit()
    assert sum(len(v) for v in a.values()) == len(M.ROUTES)
    assert "cos_zero" in a["none"] and "residue_square" in a["path"] and "u1_normalisation" in a["identity"]


def test_chudnovsky_digits():
    assert M.chudnovsky(60).startswith("3.14159265358979323846264338327950288419716939937510")
