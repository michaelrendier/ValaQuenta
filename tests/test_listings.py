"""Every documented listing runs cold, and computes what the real module computes."""
import importlib.util
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "docs"))
import gen_listings as g  # noqa: E402


@pytest.mark.parametrize("spec", g.LISTINGS, ids=[s["key"] for s in g.LISTINGS])
def test_listing_runs_cold(spec):
    code = g.build(spec)
    transcript = g.run_cold(code, spec["example"])
    assert ">>> " in transcript and "Traceback" not in transcript


def test_listing_matches_module():
    from ValaQuenta.modules.hyperwebster import maths as hw
    from ValaQuenta.modules.udeo_crypto import maths as ud
    from ValaQuenta.noether import NoetherCurrents
    ns = {}
    exec(g.build(next(s for s in g.LISTINGS if s["key"] == "horner")), ns)
    for word in ("prime", "a", "Hello, World!", "  tab\tnl\n"):
        assert ns["horner_encode"](word) == hw.horner_encode(word)
        assert ns["horner_decode"](ns["horner_encode"](word), len(word)) == word
    ns = {}
    exec(g.build(next(s for s in g.LISTINGS if s["key"] == "p1")), ns)
    for word in ("prime", "zero", "dog"):
        assert ns["p1_zero_index"](word) == ud.p1_zero_index(word)
    ns = {}
    exec(g.build(next(s for s in g.LISTINGS if s["key"] == "sigma")), ns)
    for E, s0 in ((0.5, 0.0), (1000.0, -3.0), (1e4, -3.0), (0.0, 0.3)):
        assert ns["NoetherCurrents"]().forced_sigma(E, s0) == NoetherCurrents().forced_sigma(E, s0) == 0.5


def test_listings_page_is_current():
    """docs/listings.rst is generated; a stale page means the code moved."""
    page = (ROOT / "docs" / "listings.rst").read_text()
    for spec in g.LISTINGS:
        for line in g.build(spec).rstrip("\n").split("\n"):
            assert line.strip() == "" or line in page, f"{spec['key']}: {line!r} not in docs/listings.rst"
