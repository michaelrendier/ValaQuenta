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


def test_zero_divisor_pair_counts_and_commutativity_small_dims():
    """The gallery's matrix page states these: 1 / 25 / 2689 ordered pairs, and the algebra is commutative at d = 2, 4, 8."""
    for d, pairs in ((2, 1), (4, 25), (8, 2689)):
        n = 1 << d
        assert all(T.t32_mul(a, b, d) == T.t32_mul(b, a, d) for a in range(n) for b in range(n))
        assert sum(1 for a in range(1, n) for b in range(1, n) if T.t32_mul(a, b, d) == 0) == pairs


def test_random_words_are_half_nilpotent_and_integers_are_half_nilpotent_from_three_digits():
    rng = random.Random(1)
    assert abs(sum(T.is_nilpotent(rng.getrandbits(32)) for _ in range(20000)) / 20000 - 0.5) < 0.02
    w = T.nilpotency_window(100, 3000)
    assert abs(w["primes"]["rate"] - 0.5) < 0.06 and abs(w["composites"]["rate"] - 0.5) < 0.03


def test_two_digit_window_holds_the_whole_prime_excess_recorded_in_wiki_78():
    w = T.nilpotency_window(10, 100)
    assert (w["primes"]["nilpotent"], w["primes"]["n"]) == (17, 21)
    assert (w["composites"]["nilpotent"], w["composites"]["n"]) == (29, 69)
    assert (w["composites_ending_1379"]["nilpotent"], w["composites_ending_1379"]["n"]) == (4, 15)


def test_prime_matched_control_makes_the_gap_set_unremarkable():
    c = T.matched_prime_control([11, 17, 31, 47, 59], trials=4000)
    assert c["observed"] == 5 and 0.08 < c["p_all"] < 0.18            # about 1 in 8, not 1 in 32
    assert T.matched_prime_control([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53], trials=50)["p_at_least"] == 1.0   # vacuous: the subset is its pool


def test_registry_control_equation_runs():
    r = T32NilpotencyModule().run("nilpotency_control", {})["result"]
    assert r["window"]["primes"]["n"] == 21 and r["control"]["n"] == 5


def test_square_is_the_parity_of_the_weight_and_parity_is_a_ring_homomorphism():
    """Found by chasing the two-digit anomaly (wiki 78 §7): w*w = (popcount(w) mod 2) * e0; the nilpotents are the even-weight words."""
    for d in (2, 4, 8):
        c = T.radical_census(d)
        assert c["square_is_weight_parity"] and c["parity_is_homomorphism"]
    assert T.radical_census(16)["square_is_weight_parity"]
    rng = random.Random(7)
    for _ in range(2000):
        w = rng.getrandbits(32)
        assert T.t32_mul(w, w) == T.weight_parity(w)
        assert T.trace_laplacian(w) == (T.ones(32) if T.weight_parity(w) else 0)
    nil = [w for w in range(256) if not T.weight_parity(w)]
    assert len(nil) == 128 and all(not T.weight_parity(a ^ b) for a in nil[:40] for b in nil[:40])   # the radical is closed under XOR


def test_two_digit_excess_is_one_table_with_a_small_hypergeometric_p_and_absent_at_three_digits():
    from math import comb
    nums = list(range(10, 100)); P = set(T.sieve(100))
    nil = {n: T.weight_parity(T.hw_to_t32(n)) == 0 for n in nums}
    K, N, pr = sum(nil.values()), 90, [n for n in nums if n in P]
    kp = sum(nil[n] for n in pr)
    p = sum(comb(K, x) * comb(N - K, len(pr) - x) for x in range(kp, min(K, len(pr)) + 1)) / comb(N, len(pr))
    assert (K, len(pr), kp) == (46, 21, 17) and 0.001 < p < 0.003
    assert abs(T.nilpotency_window(100, 1000)["primes"]["rate"] - 0.5) < 0.06
