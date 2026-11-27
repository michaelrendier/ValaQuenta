r"""
ValaQuenta.modules.hypergon_constructibility.maths
==================================================
The factorization engine, built purely: which sedenion basis positions
(hyper-N-gons, N=1..16) are geometrically constructible, and whether
zero-divisor/nilpotency structure actually distinguishes real factor
pairs from random ones. Both questions answered honestly -- one real
positive result, one real negative result, neither smoothed over.

PART 1 -- Gauss-Wantzel constructibility (REAL, ESTABLISHED, 1796/1837):
A regular n-gon is constructible with straightedge and compass if and
only if n = 2^k \* (product of DISTINCT Fermat primes), k >= 0. Only five
Fermat primes are known to exist, ever: 3, 5, 17, 257, 65537 (whether
more exist is a genuine open problem in number theory). Applied uniformly
across the 16 sedenion basis primes {2,3,5,7,11,13,17,19,23,29,31,37,
41,43,47,53}, this generalizes Phase 19 of Tuning-the-Engine.md's single
"13-gon is non-constructible" example to the full sweep: only 4 of 16
positions are constructible (e0=2, e1=3, e2=5, e6=17); the other 12 are
holes. Verified by direct computation below, not assumed.

PART 2 -- Nilpotent-split factorization test (Phase 22's corrected
conjecture, re-tested here with a proper control): does mapping a
composite N's actual prime factors p, q to T32/GF(2) via the Hyperwebster
address show elevated nilpotency versus random, uninvolved primes?
HONEST RESULT: only for small/close-magnitude primes -- and even then,
a random pair of primes (not necessarily factors of any common N) shows
comparable or higher nilpotency than genuine far-apart factor pairs. The
"signal" Phase 22 reported does not survive a magnitude-matched control.
This is reported as a real negative result, not smoothed into a partial
positive -- see verify_nilpotent_split_conjecture().

PART 3 -- The definition of primes this engine actually supports: dual,
not single. Arithmetically (standard): a prime has no non-trivial
factorization -- this is exactly why AbrikosovTree's tree structure has
primes as leaves that survive all 9 CD-tower levels (no ZD pair
possible). Geometrically (Gauss-Wantzel, verified in Part 1): most primes
are NOT constructible in the classical sense -- constructibility is the
exception (2 and the 5 known Fermat primes), not the rule, and this
exceptional status is unrelated to a prime's role in factoring a
composite. Part 2 establishes what does NOT hold: constructibility status
and factoring-relevant nilpotency bias are not the same thing, and
neither survives as "the" mechanism that explains factoring via this
route -- that remains genuinely open.

PART 4 -- The Niemeier gap (the elementary theorem under the "N-shape" claim): an ADE root system of rank 24 whose components all share one
Coxeter number h has h mod 16 outside {1, 11, 15}. PROVEN here in four lines (an odd h forces every component to be A_(h-1), so h-1 divides 24)
and CHECKED by enumerating every such root system (there are exactly 23, Niemeier 1973). The 15 Moonshine primes then cover all eight odd residues
mod 16, the three gap residues included; a control (moonshine_fill_control) says how surprising that is. What is NOT a theorem here: the reading
of a residue k as "the Fermat forbidden zone at sedenion index e_k" and "generalized Fermat IS the 71 holomorphic VOAs" -- those are OURS/THEORETICAL.

Version: 0.200
"""

import math
from itertools import combinations
from typing import Dict, List, Any, Tuple

PRIMES16 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
KNOWN_FERMAT_PRIMES = {3, 5, 17, 257, 65537}  # only 5 ever known to exist


# ── Part 1: Gauss-Wantzel constructibility ──────────────────────────────────

def is_fermat_prime(p: int) -> bool:
    """
    Report whether p is a known Fermat prime, 2^(2^n)+1.

    Whether more exist beyond the five known is a genuine open problem in
    number theory. This checks against the known set; it is not a generative
    test.

    :param p: integer to test
    :returns: True if p is one of the known Fermat primes
    """
    return p in KNOWN_FERMAT_PRIMES


def is_power_of_two(n: int) -> bool:
    """
    Report whether n is a positive power of two.

    :param n: integer to test
    :returns: True if n = 2^k for some k ≥ 0
    """
    return n > 0 and (n & (n - 1)) == 0


def is_constructible(n: int) -> bool:
    """
    Gauss-Wantzel: report whether the regular n-gon is constructible.

    True iff n is 2^k times a product of DISTINCT Fermat primes (k ≥ 0). For a
    single prime p this reduces to: p == 2, or p is itself a Fermat prime.

    :param n: number of sides
    :returns: True if the regular n-gon is constructible
    """
    if is_power_of_two(n):
        return True
    if is_fermat_prime(n):
        return True
    # general n (not prime): factor out powers of 2, check remaining
    # factors are distinct Fermat primes -- included for completeness,
    # though the sedenion basis application only needs the prime case.
    m = n
    while m % 2 == 0:
        m //= 2
    remaining = m
    for fp in sorted(KNOWN_FERMAT_PRIMES):
        if remaining % fp == 0:
            remaining //= fp
            if remaining % fp == 0:
                return False  # not DISTINCT -- repeated factor fails Gauss-Wantzel
    return remaining == 1


def sedenion_hypergon_sweep() -> Dict[str, Any]:
    """THE comprehensive test across all 16 hyper-N-gons for the sedenion
    basis -- generalizes Phase 19's single '13-gon' example."""
    rows = []
    constructible_count = 0
    for i, p in enumerate(PRIMES16):
        fermat = is_fermat_prime(p)
        pow2 = is_power_of_two(p)
        constructible = fermat or pow2
        constructible_count += constructible
        rows.append({
            'channel': f'e{i}', 'prime': p,
            'fermat_prime': fermat, 'power_of_2': pow2,
            'constructible': constructible,
        })
    return {
        'rows': rows,
        'constructible_count': constructible_count,
        'hole_count': 16 - constructible_count,
        'constructible_channels': [r['channel'] for r in rows if r['constructible']],
        'hole_channels': [r['channel'] for r in rows if not r['constructible']],
    }


# ── Part 2: Nilpotent-split factorization test (re-verified, not assumed) ──
#
# t32_mul, is_nilpotent, hw_address, hw_to_t32, sieve now live in
# t32_nilpotency.maths (2026-07-11 refactor) -- imported, not duplicated,
# specifically to avoid the two transcription bugs this file's git history
# shows (a placeholder hw_to_t32 claimed to match without checking, then a
# fabricated _HW_CHARS retyped from memory). One verified copy, imported
# everywhere it's needed, including by FourthAgePapers/FermatMonster's
# fermat_monster_engine.py.

from ..t32_nilpotency.maths import (
    t32_mul, is_nilpotent, hw_address, hw_to_t32, sieve,
)


def verify_nilpotent_split_conjecture(seed: int = 20260711) -> Dict[str, Any]:
    """
    Re-test Phase 22's corrected factorization conjecture (individual
    p, q nilpotency, not the earlier Fermat-midpoint a,b) against THREE
    datasets: close real factor pairs, far-apart real factor pairs, and a
    random-pair control (primes not necessarily factors of any common N).
    HONEST result computed here, not assumed from the prior session's
    narrower test.

    :param seed: random seed for the control pairs
    :returns: nilpotency rates for the close, far-apart and random-control datasets, and the verdict
    """
    import random
    primes = sieve(10000)

    def nilpotency_rates(pairs):
        n = len(pairs)
        p_nil = sum(is_nilpotent(hw_to_t32(p)) for p, q in pairs)
        q_nil = sum(is_nilpotent(hw_to_t32(q)) for p, q in pairs)
        both = sum(is_nilpotent(hw_to_t32(p)) and is_nilpotent(hw_to_t32(q)) for p, q in pairs)
        return {'n': n, 'p_pct': 100 * p_nil / n, 'q_pct': 100 * q_nil / n, 'both_pct': 100 * both / n}

    close_pairs = []
    for i, p in enumerate(primes):
        if p < 7:
            continue
        for q in primes[i + 1:i + 20]:
            if q > 10 * p:
                break
            close_pairs.append((p, q))
        if len(close_pairs) >= 97:
            break

    random.seed(seed)
    lower = [p for p in primes if 1000 <= p < 4000]
    upper = [p for p in primes if 6000 <= p < 10000]
    far_pairs = []
    while len(far_pairs) < 97:
        p, q = random.choice(lower), random.choice(upper)
        if p != q:
            far_pairs.append((min(p, q), max(p, q)))

    random_pairs = [(random.choice(primes), random.choice(primes)) for _ in range(97)]

    close = nilpotency_rates(close_pairs)
    far = nilpotency_rates(far_pairs)
    control = nilpotency_rates(random_pairs)

    # Honest verdict: does far-apart beat the random (non-factor) control?
    # If not, the "signal" is a magnitude artifact, not a factoring signal.
    survives_control = far['q_pct'] > control['q_pct'] and far['p_pct'] > control['p_pct']

    # Where the close-pair "elevation" comes from: the 110 close pairs are built from a handful of primes, each counted many times
    # (a prime p appears with each of the next 19 primes), so the pairs are not independent draws.  Count the primes once.
    distinct = sorted({x for pq in close_pairs for x in pq})
    d_nil = sum(is_nilpotent(hw_to_t32(x)) or hw_to_t32(x) == 0 for x in distinct)
    d_n = len(distinct)
    tail = sum(math.comb(d_n, k) for k in range(d_nil, d_n + 1)) / 2 ** d_n   # exact P(at least d_nil of d_n | each nilpotent with probability 1/2)

    return {
        'close_prime_pairs': close,
        'far_apart_prime_pairs': far,
        'random_pair_control': control,
        'close_pairs_distinct_primes': {'n': d_n, 'smallest': distinct[0], 'largest': distinct[-1], 'nilpotent': d_nil,
                                        'rate_pct': 100 * d_nil / d_n, 'p_at_least_by_chance': tail},
        'survives_magnitude_matched_control': survives_control,
        'verdict': (
            'REAL SIGNAL' if survives_control else
            'ARTIFACT — close-prime elevation does not survive far-apart + '
            'random-control comparison; likely a small-magnitude artifact of '
            'the Hyperwebster address mapping, not evidence the mechanism '
            'tracks factoring relationships'
        ),
    }


# ── Part 3: Synthesis ────────────────────────────────────────────────────────

def prime_definition_report() -> Dict[str, Any]:
    """What 'prime' actually means, per what THIS engine has verified —
    dual definition, arithmetic and geometric, explicitly NOT unified by
    a working factoring mechanism (that remains open, see Part 2)."""
    hypergon = sedenion_hypergon_sweep()
    return {
        'arithmetic_definition': (
            'A prime has no non-trivial factorization — a<1<a<p with a*b=p '
            'impossible for 1<a,b<p. This is why AbrikosovTree\'s CD-tower '
            'structure has primes as leaves surviving all 9 levels: no '
            'factorization means no zero-divisor pair can form, so the norm '
            'never fails and the prime reaches T_256 intact.'
        ),
        'geometric_definition': (
            f'Of the 16 primes in the sedenion basis, only '
            f'{hypergon["constructible_count"]} are constructible in the '
            f'classical Gauss-Wantzel sense (regular-polygon-constructible '
            f'by straightedge and compass): {", ".join(str(PRIMES16[int(c[1:])]) for c in hypergon["constructible_channels"])}. '
            f'The remaining {hypergon["hole_count"]} '
            f'({", ".join(str(PRIMES16[int(c[1:])]) for c in hypergon["hole_channels"])}) '
            'are non-constructible — geometric "holes," extinction dimensions '
            'in the Dirichlet projection sense of Phase 19. Constructibility '
            'is the exception among primes, not the rule.'
        ),
        'unification_status': (
            'NOT unified into a single working mechanism. Part 2 shows the '
            'nilpotent-split conjecture (which would have connected '
            'geometric/algebraic structure directly to factoring) does not '
            'survive a magnitude-matched control — it is very likely an '
            'artifact of small-prime address mapping, not a real factoring '
            'signal. The arithmetic and geometric definitions of "prime" are '
            'both real and verified; a working bridge between them and actual '
            'factoring remains genuinely open.'
        ),
        'hypergon_sweep': hypergon,
    }


# ── Part 4: the Niemeier gap and the Moonshine fill ─────────────────────────
#
# The "N-shape" claim of FourthAgePapers/FermatMonster rests on one finite fact about the number 24 and the number 16.  It is a theorem,
# and short enough to prove and to check exhaustively; the reading of it as a statement about Fermat's equation is a separate matter.

MOONSHINE_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41, 47, 59, 71]   # the primes dividing |Monster| (Ogg 1975)


def _components(h: int, max_rank: int) -> List[Tuple[str, int]]:
    """The A/D/E irreducible root systems of rank at most ``max_rank`` whose Coxeter number is ``h``: A_n (h = n+1), D_n (n ≥ 4, h = 2n-2), E6/E7/E8 (h = 12, 18, 30)."""
    out = []
    if 1 <= h - 1 <= max_rank:
        out.append((f'A{h - 1}', h - 1))
    if h % 2 == 0 and 4 <= (h + 2) // 2 <= max_rank:
        out.append((f'D{(h + 2) // 2}', (h + 2) // 2))
    for name, rank, coxeter in (('E6', 6, 12), ('E7', 7, 18), ('E8', 8, 30)):
        if coxeter == h and rank <= max_rank:
            out.append((name, rank))
    return out


def niemeier_root_systems(rank: int = 24) -> List[Dict[str, Any]]:
    """
    Every ADE root system of the given rank whose components all have the same Coxeter number: the root systems of the Niemeier lattices.

    Generated from the defining condition, not typed in: for each Coxeter number h, choose how many components of each type with that h
    sum to the rank (a coin-change enumeration). For rank 24 the answer is exactly 23 root systems (Niemeier 1973); the Leech lattice has none.

    :param rank: total rank (24 for the Niemeier lattices)
    :returns: list of dicts ``h``, ``label`` (for example ``'A5^4 D4'``) and ``multiplicities`` ({component: count})
    """
    found = []
    for h in range(2, 2 * rank):
        comps = _components(h, rank)

        def split(i, left, chosen):
            if left == 0:
                if chosen:
                    found.append((h, dict(chosen)))
                return
            if i == len(comps):
                return
            name, r = comps[i]
            for k in range(left // r, -1, -1):
                split(i + 1, left - k * r, chosen + ([(name, k)] if k else []))

        split(0, rank, [])
    return [{'h': h, 'multiplicities': m,
             'label': ' '.join(f'{n}^{k}' if k > 1 else n for n, k in m.items())} for h, m in sorted(found, key=lambda t: (t[0], str(t[1])))]


def niemeier_gap_theorem(rank: int = 24, modulus: int = 16) -> Dict[str, Any]:
    """
    The Niemeier gap: the residues of the Coxeter number h modulo 16 that no Niemeier root system reaches.

    THEOREM (elementary). If an ADE root system of rank 24 has all components with one Coxeter number h, then h mod 16 is not 1, 11 or 15.
    Proof. D_n and E_n have even Coxeter number (2n-2; 12, 18, 30), so an odd h forces every component to be A_(h-1), and k copies of A_(h-1) have
    rank k(h-1) = 24, so (h-1) divides 24. The divisors of 24 are 1, 2, 3, 4, 6, 8, 12, 24, so the odd h are 3, 5, 7, 9, 13, 25, which are
    3, 5, 7, 9, 13, 9 modulo 16. An even h is never congruent to an odd residue. Hence the odd residues 1, 11, 15 are never reached. ∎
    The function checks the proof's steps and, independently, the enumeration of all 23 root systems.

    :param rank: total rank (24)
    :param modulus: the modulus (16, the number of sedenion basis elements)
    :returns: dict with the 23 ``root_systems``, ``h_values``, ``residues_reached``, ``gap``, the ``proof`` steps as data, and ``theorem_holds``
    """
    systems = niemeier_root_systems(rank)
    hs = sorted({s['h'] for s in systems})
    reached = sorted({h % modulus for h in hs})
    gap = sorted(set(range(modulus)) - set(reached))
    odd_h = sorted(h for h in hs if h % 2)
    divisors = [d for d in range(1, rank + 1) if rank % d == 0]
    odd_from_divisors = sorted(d + 1 for d in divisors if (d + 1) % 2)
    only_a = all(len(s['multiplicities']) == 1 and next(iter(s['multiplicities'])).startswith('A') for s in systems if s['h'] % 2)
    # beyond the largest possible Coxeter number nothing exists: a component of rank <= 24 has h <= 46
    max_h = max(2 * rank - 2, rank + 1, 30)      # D_rank, A_rank, E8: the largest Coxeter number of any component of rank <= 24
    return {'root_systems': systems, 'count': len(systems), 'h_values': hs, 'max_h_possible': max_h,
            'residues_reached': reached, 'gap': gap,
            'proof': {'odd_h_means_every_component_is_A': only_a, 'divisors_of_rank': divisors,
                      'odd_h_from_divisors': odd_from_divisors, 'odd_h_found': odd_h,
                      'odd_h_residues': sorted({h % modulus for h in odd_h})},
            'theorem_holds': (len(systems) == 23 and odd_h == odd_from_divisors and only_a and gap == [1, 11, 15])}


def moonshine_gap_fill(modulus: int = 16) -> Dict[str, Any]:
    """
    Which Moonshine primes land in which residue class modulo 16, and whether they cover the Niemeier gap.

    :param modulus: the modulus (16)
    :returns: dict ``by_residue`` ({residue: [primes]}), ``gap`` (from niemeier_gap_theorem), ``gap_filled`` (the gap residues the primes reach),
        ``odd_residues_all_covered``
    """
    by = {}
    for p in MOONSHINE_PRIMES:
        by.setdefault(p % modulus, []).append(p)
    gap = niemeier_gap_theorem(modulus=modulus)['gap']
    odd = [r for r in range(modulus) if r % 2]
    return {'by_residue': dict(sorted(by.items())), 'gap': gap, 'gap_filled': [r for r in gap if r in by],
            'odd_residues_all_covered': all(r in by for r in odd)}


def moonshine_fill_control(modulus: int = 16) -> Dict[str, Any]:
    """
    How surprising is the Moonshine fill? Exact count, no sampling.

    The 14 odd Moonshine primes are 14 of the 19 odd primes up to 71. Enumerate every 14-subset of those 19 and count how many reach the gap residues,
    and how many reach all eight odd residues. If most subsets do too, the fill is what a prime set that size does anyway and says little.

    :param modulus: the modulus (16)
    :returns: dict ``subsets``, ``cover_gap``, ``cover_all_odd``, and the two fractions ``p_cover_gap``, ``p_cover_all_odd``
    """
    pool = [p for p in range(3, 72) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    gap = set(niemeier_gap_theorem(modulus=modulus)['gap'])
    odd = {r for r in range(modulus) if r % 2}
    n = gap_n = odd_n = 0
    for sub in combinations(pool, len([p for p in MOONSHINE_PRIMES if p % 2])):
        res = {p % modulus for p in sub}
        n += 1
        gap_n += gap <= res
        odd_n += odd <= res
    return {'pool_size': len(pool), 'subsets': n, 'cover_gap': gap_n, 'cover_all_odd': odd_n,
            'p_cover_gap': gap_n / n, 'p_cover_all_odd': odd_n / n}


def totient_constructibility_check(limit: int = 70000) -> Dict[str, Any]:
    """
    Gauss-Wantzel the other way, with no list of Fermat primes: a regular n-gon is constructible iff Euler's phi(n) is a power of 2.

    Compares that test with is_constructible for every n up to ``limit``. A disagreement would mean a Fermat prime missing from KNOWN_FERMAT_PRIMES;
    agreement shows the list of five is complete up to ``limit`` (the next candidate, 2^32 + 1 = 641 × 6700417, is composite).

    :param limit: largest n tested
    :returns: dict ``limit``, ``constructible`` (how many n ≥ 3), ``mismatches`` (list, expected empty)
    """
    phi = list(range(limit + 1))
    for i in range(2, limit + 1):
        if phi[i] == i:
            for j in range(i, limit + 1, i):
                phi[j] -= phi[j] // i
    bad, count = [], 0
    for n in range(3, limit + 1):
        by_phi = is_power_of_two(phi[n])
        count += by_phi
        if by_phi != is_constructible(n):
            bad.append(n)
    return {'limit': limit, 'constructible': count, 'mismatches': bad}
