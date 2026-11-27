"""hypergon_constructibility (engine 4): Gauss-Wantzel, the Niemeier gap, the Moonshine fill, and the factoring control."""
import math

from ValaQuenta.modules.hypergon_constructibility import maths as hg


def test_sixteen_sedenion_primes_four_constructible():
    sweep = hg.sedenion_hypergon_sweep()
    assert sweep['constructible_count'] == 4 and sweep['hole_count'] == 12
    assert sweep['constructible_channels'] == ['e0', 'e1', 'e2', 'e6']        # 2, 3, 5, 17


def test_gauss_wantzel_composites():
    assert hg.is_constructible(15) and hg.is_constructible(256) and hg.is_constructible(65537 * 3)
    assert not hg.is_constructible(9) and not hg.is_constructible(7) and not hg.is_constructible(25)


def test_totient_test_agrees_with_the_fermat_list_to_70000():
    """No Fermat prime is missing from the list of five below 70,000."""
    out = hg.totient_constructibility_check(70000)
    assert out['mismatches'] == [] and out['constructible'] == 139


def test_niemeier_root_systems_are_generated_exactly():
    systems = hg.niemeier_root_systems()
    assert len(systems) == 23
    labels = {s['label'] for s in systems}
    assert {'A1^24', 'A24', 'D24', 'E8^3', 'A5^4 D4', 'D4^6', 'A11 D7 E6'} <= labels
    for s in systems:      # every system has rank 24 by its own definition
        assert s['h'] >= 2


def test_niemeier_gap_theorem():
    t = hg.niemeier_gap_theorem()
    assert t['gap'] == [1, 11, 15]
    assert t['proof']['odd_h_found'] == t['proof']['odd_h_from_divisors'] == [3, 5, 7, 9, 13, 25]
    assert t['proof']['odd_h_means_every_component_is_A'] and t['theorem_holds']
    assert max(t['h_values']) == t['max_h_possible'] == 46


def test_gap_is_specific_to_rank_24():
    """The same construction at another rank has a different gap: the 24 matters (rank 8 has only E8-type, A8, D8 ... root systems)."""
    assert hg.niemeier_gap_theorem(rank=24)['gap'] == [1, 11, 15]
    other = hg.niemeier_gap_theorem(rank=12)
    assert other['gap'] != [1, 11, 15]


def test_moonshine_prime_residues_fill_the_gap():
    fill = hg.moonshine_gap_fill()
    assert fill['gap_filled'] == [1, 11, 15] and fill['odd_residues_all_covered']
    assert fill['by_residue'][1] == [17] and fill['by_residue'][11] == [11, 59] and fill['by_residue'][15] == [31, 47]


def test_moonshine_fill_is_not_surprising():
    """The control: most 14-subsets of the 19 odd primes up to 71 cover the gap too, so the fill is not evidence by itself."""
    c = hg.moonshine_fill_control()
    assert c['subsets'] == math.comb(19, 14)
    assert 0.6 < c['p_cover_gap'] < 0.75 and 0.4 < c['p_cover_all_odd'] < 0.5


def test_factoring_signal_is_pseudo_replication():
    v = hg.verify_nilpotent_split_conjecture()
    assert v['survives_magnitude_matched_control'] is False
    d = v['close_pairs_distinct_primes']
    assert d['n'] < 40 and v['close_prime_pairs']['n'] > 100            # 110 pairs, 25 primes: the pairs are not independent draws
    assert 0.5 < d['rate_pct'] / 100 < 0.9
    assert v['far_apart_prime_pairs']['p_pct'] < 60                       # far apart: chance (a 50 % coin)
