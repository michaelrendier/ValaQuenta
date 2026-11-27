"""The Basile engine: the recipe, the toy library, and (when a local copy of the published files exists) the published constants."""
import os
import random

import pytest

from ValaQuenta.modules.basile import maths as M

ALPHA26 = "abcdefghijklmnopqrstuvwxyz"


def test_ordered_address_is_shortlex_rank():
    assert [M.ordered_text_at(n, ALPHA26) for n in (0, 25, 26, 701, 702)] == ["a", "z", "aa", "zz", "aaa"]
    assert all(M.ordered_address(M.ordered_text_at(n, ALPHA26), ALPHA26) == n for n in range(5000))


def test_the_empty_word_is_at_minus_one():
    assert M.ordered_address("", ALPHA26) == -1 and M.ordered_text_at(-1, ALPHA26) == "" and M.ordered_address("a", ALPHA26) == 0
    with pytest.raises(ValueError):
        M.ordered_text_at(-2, ALPHA26)


def test_volume_a_trick_is_a_place_value():
    words = [""] + ["".join(p) for n in range(1, 4) for p in __import__("itertools").product(ALPHA26, repeat=n)]
    assert all(M.ordered_address("a" + w, ALPHA26) - M.ordered_address(w, ALPHA26) == 26 ** len(w) for w in words)


def test_xorshift_inverses_are_exact():
    rnd = random.Random(1)
    for width, s in ((64, 7), (257, 11), (1000, 13)):
        for _ in range(200):
            x = rnd.getrandbits(width)
            assert M.xorshift_right_inverse(M.xorshift_right(x, s), s) == x
            k = width - s
            assert M.xorshift_left_masked_inverse(M.xorshift_left_masked(x, k, s), k, s) == x


def test_scrambler_is_a_bijection_on_the_toy_library():
    n = 29 ** 3
    sc, un = M.power_of_two_scrambler(n)
    assert sorted(sc(x) for x in range(n)) == list(range(n))
    assert all(un(sc(x)) == x for x in range(n))
    assert [M.babel_page(i) for i in range(3)] == ["blr", "lrq", "wfl"]
    assert M.babel_location("blr") == 0


def test_scrambled_neighbours_are_unrelated_ordered_neighbours_are_not():
    n = 29 ** 3
    sc, _ = M.power_of_two_scrambler(n)
    d = lambda a, b: sum(x != y for x, y in zip(a, b))
    ordered = sum(d(M.page_at(i, M.BABEL_ALPHABET, 3), M.page_at(i + 1, M.BABEL_ALPHABET, 3)) for i in range(n - 1)) / (n - 1)
    scrambled = sum(d(M.page_at(sc(i), M.BABEL_ALPHABET, 3), M.page_at(sc(i + 1), M.BABEL_ALPHABET, 3)) for i in range(n - 1)) / (n - 1)
    assert ordered < 1.1 and scrambled > 2.8


def test_prime_power_detection():
    assert M.prime_power(3 ** 50) == (3, 50) and M.prime_power(2 ** 31) == (2, 31) and M.prime_power(3 ** 5 * 2) is None


def test_hull_dobell_conditions():
    assert M.hull_dobell(1 << 15, 1664525, 1013904223, [2])["full_period"]
    assert not M.hull_dobell(1 << 15, 1664527, 1013904223, [2])["full_period"]


def test_published_euclid_array_limit():
    assert M.euclid_inverse_qarray(3, 7) == 5 and M.euclid_inverse_qarray(17, 3120) == 2753
    rnd = random.Random(2)
    over = 0
    for _ in range(100):
        m, a = rnd.getrandbits(64) | (1 << 63) | 1, rnd.getrandbits(63) | 1
        try:
            M.euclid_inverse_qarray(a, m)
        except OverflowError:
            over += 1
    assert over > 90                       # the 25-entry array holds 23 divisions; 64-bit inputs need ~37


def test_scrambler_cycles_and_the_cyclic_lcg():
    n = 29 ** 3
    sc, _ = M.power_of_two_scrambler(n)
    c = M.permutation_cycles(sc, n)
    assert sum(c) == n and len(c) == 11 and c[0] == 9943          # not a single cycle
    big = 1 << 15
    lcg = M.permutation_cycles(lambda x: (1664525 * x + 1013904223) % big, big)
    assert lcg == [big]                                          # Hull-Dobell: one full cycle


def test_site_address_fields():
    r = M.parse_babel_address("jeb0110jlb-w2-s4-v16:19")
    assert (r["wall"], r["shelf"], r["volume"], r["page"], r["volume_index"]) == (2, 4, 16, 19, 271)
    with pytest.raises(ValueError):
        M.parse_babel_address("jeb0110jlb-w5-s1-v01")


def test_lobthis_request_is_data_only():
    r = M.resource_locator_request("x")
    assert r["method"] == "POST" and r["url"].endswith("resourcelocator.cgi") and r["fields"] == {"extension": "x"}


def test_library_scale_matches_the_site():
    s = M.library_scale()
    assert round(s["log10_books"]) == 4677


_CACHE = M.default_cache_dir()
_have = os.path.exists(os.path.join(_CACHE, "PRNG")) and os.path.exists(os.path.join(_CACHE, "imagesearch.cpp"))


@pytest.mark.skipif(not _have, reason="published files not in the cache (M.fetch_published())")
def test_published_constants_are_consistent():
    au = M.Published().audit()
    assert au["a_times_ainverse_mod_m_is_1"] and au["gcd_a_m_is_1"] and au["gcd_c_m_is_1"]
    assert all(au["shared_constants_identical"].values())
    assert au["maskone_is_power_of_two"] and au["masktwo_is_power_of_two"] and au["divver_is_power_of_two"]
    assert au["palette_is_hex_of_index"] and au["image_bits"] == 640 * 416 * 12
    assert au["forward_steps"][0][0] == "R" and len(au["forward_steps"]) == 4
    assert au["m_prime_power"] == (3, 2015755)                       # m is exactly 3**2015755
    assert au["hull_dobell"]["full_period"]                          # so the LCG alone is one cycle of length m


@pytest.mark.skipif(not _have, reason="published files not in the cache (M.fetch_published())")
def test_published_roundtrip_and_multiplicity():
    pub = M.Published()
    rnd = random.Random(3)
    loc = rnd.getrandbits(int(pub.m).bit_length() - 2) % int(pub.m)
    p = pub.forward(loc)
    assert pub.inverse(p) == loc
    pos = pub.unread_positions()[0]                                 # a bit the image never reads
    s = pub.sibling(loc, pos)
    assert s["sibling_differs"] and s["forward_matches"] and s["same_image"]
    assert 60000 < pub.mean_locations_per_image()["mean_locations_per_image"] < 80000


@pytest.mark.skipif(not _have, reason="published files not in the cache (M.fetch_published())")
def test_published_sibling_offsets_add_within_a_location_and_differ_between_locations():
    pub = M.Published()
    rnd = random.Random(4)
    m = int(pub.m)
    l1, l2 = (rnd.getrandbits(m.bit_length() - 2) % m for _ in range(2))
    a = pub.sibling_offsets(l1, pairs=3, seed=1)
    assert a["valid_unread_bits"] == 16 and a["single_offsets_distinct"]
    assert a["pairs_additive"] and a["all_bits_together_additive"]
    pos = pub.unread_positions()[0]
    o1 = (pub.inverse(pub.forward(l1) ^ (1 << pos)) - l1) % m
    o2 = (pub.inverse(pub.forward(l2) ^ (1 << pos)) - l2) % m
    assert o1 != o2
