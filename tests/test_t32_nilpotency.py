"""Tests for modules/t32_nilpotency (engine 3): primitives, the GF(2) square law, the detector, and the recorded prime split."""
import random

from ValaQuenta.modules.t32_nilpotency import maths as T
from ValaQuenta.modules.t32_nilpotency.tools import T32NilpotencyModule

SEDENION_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
MOONSHINE = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]


def test_hw_address_and_word_are_the_recorded_values():
    assert [T.hw_to_t32(p) for p in (2, 3, 11, 53)] == [0x2, 0x3, 0xC3, 0x249]


def test_sedenion_prime_split_is_11_of_16():
    r = T.prime_nilpotency_report(SEDENION_PRIMES)
    assert (r["nilpotent_count"], r["total"]) == (11, 16)
    assert [x["prime"] for x in r["rows"] if not x["nilpotent"]] == [2, 7, 19, 37, 43]


def test_moonshine_split_and_the_chance_baseline_is_recorded():
    r = T.prime_nilpotency_report(MOONSHINE)
    assert r["nilpotent_count"] == 12
    gap = [11, 17, 31, 47, 59]
    assert all(row["nilpotent"] for row in r["rows"] if row["prime"] in gap)   # n = 5: 1 in 5.9 by chance, not evidence
    assert abs(0.7 ** 5 - 0.168) < 1e-3


def test_square_law_and_128_128_split_at_dim_8():
    c = T.radical_census(8)
    assert (c["nilpotent"], c["involutory"], c["other"]) == (128, 128, 0)


def test_detector_iff_nilpotent_exhaustive_small_dims():
    for d in (2, 4, 8):
        assert T.radical_census(d)["detector_agrees"]


def test_detector_iff_nilpotent_random_dim_32():
    rng = random.Random(1)
    for _ in range(2000):
        w = rng.getrandbits(32)
        assert (T.trace_laplacian(w) == 0) == (T.square_class(w) == "nilpotent")
        assert T.square_class(w) != "other"


def test_ones_is_not_an_annihilator():
    assert T.t32_mul(1, T.ones(32)) != 0
    assert not T.radical_census(8)["one_is_annihilator"]


def test_zero_divisor_pairs_exist_and_nilpotent_implies_none_with_itself():
    a = next(w for w in range(1, 256) if T.is_nilpotent(w))
    assert T.t32_mul(a, a) == 0
    assert any(T.is_zero_divisor_pair(a, b) for b in range(1, 256))


def test_registry_equation_runs():
    mod = T32NilpotencyModule()
    assert mod.run("radical_census", {"dim": 4})["result"]["words"] == 16
    assert mod.run("prime_nilpotency_report", {})["result"]["total"] == 16
