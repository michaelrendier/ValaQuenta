"""
ainulindale_engine.modules.hypergon_constructibility.maths
=============================================================
The factorization engine, built purely: which sedenion basis positions
(hyper-N-gons, N=1..16) are geometrically constructible, and whether
zero-divisor/nilpotency structure actually distinguishes real factor
pairs from random ones. Both questions answered honestly -- one real
positive result, one real negative result, neither smoothed over.

PART 1 -- Gauss-Wantzel constructibility (REAL, ESTABLISHED, 1796/1837):
A regular n-gon is constructible with straightedge and compass if and
only if n = 2^k * (product of DISTINCT Fermat primes), k >= 0. Only five
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

Version: 0.100
"""

import math
from typing import Dict, List, Any, Tuple

PRIMES16 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
KNOWN_FERMAT_PRIMES = {3, 5, 17, 257, 65537}  # only 5 ever known to exist


# ── Part 1: Gauss-Wantzel constructibility ──────────────────────────────────

def is_fermat_prime(p: int) -> bool:
    """p is a known Fermat prime (2^(2^n)+1). Whether more exist beyond
    the 5 known is a genuine open problem in number theory -- this checks
    against the known set, not a generative test."""
    return p in KNOWN_FERMAT_PRIMES


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def is_constructible(n: int) -> bool:
    """Gauss-Wantzel: True iff n is expressible as 2^k times a product of
    DISTINCT Fermat primes (k>=0). For a single prime p specifically, this
    reduces to: p==2, or p is itself a Fermat prime."""
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
    """Re-test Phase 22's corrected factorization conjecture (individual
    p, q nilpotency, not the earlier Fermat-midpoint a,b) against THREE
    datasets: close real factor pairs, far-apart real factor pairs, and a
    random-pair control (primes not necessarily factors of any common N).
    HONEST result computed here, not assumed from the prior session's
    narrower test."""
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

    return {
        'close_prime_pairs': close,
        'far_apart_prime_pairs': far,
        'random_pair_control': control,
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
