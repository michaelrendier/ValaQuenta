"""
ValaQuenta.modules.t32_nilpotency.maths
=======================================
Standalone, minimal, importable primitives: Hyperwebster address encoding,
T32/GF(2) Cayley-Dickson multiplication, nilpotency test.

Deliberately separated out of hypergon_constructibility (which uses these
to test a factorization conjecture) so any other engine -- notably
FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py, the N-shape
engine -- can import the same, single, verified-correct implementation
instead of each maintaining its own copy. hypergon_constructibility now
imports from here rather than duplicating.

Origin of that "verified-correct" qualifier, worth keeping attached to
this module rather than only in hypergon_constructibility's history: a
first attempt at hw_to_t32 was a placeholder that silently didn't match
TuringStack/fermat_sedenion_test.py's real implementation; the fix attempt
then hand-transcribed a fabricated _HW_CHARS from memory and got that
wrong too. Both caught by raw-number mismatches, not by inspection. The
_HW_CHARS literal below was pulled via repr() from the real source and
verified byte-for-byte and numerically identical across 21 test values
before this module was trusted. If this file is ever copied again rather
than imported, that verification needs to be redone -- don't assume a
retyped copy is correct.

Canonical maths added in 0.110 (Ainulindale wiki 78 §5; ~/.clauderc_canonical_maths @RCCM_RING_THEORY_SPINE):

* GF(2) square law: x² ∈ {0, e₀} for every x, so every element is either nilpotent (x² = 0, the radical)
  or an involutory unit (x² = e₀); at dim 8 the algebra splits 128 / 128 (exhaustive).
* One detector: Δ(w) = w·𝟏 (𝟏 = all ones). Δ(w) = 0 ⟺ w² = 0 (exhaustive at dim 2, 4, 8; 20000 random words at dim 32).
* Corrected lemma (2026-08-22, supersedes the UDEO white-paper proof): 𝟏 is NOT a global annihilator;
  e₀·𝟏 = 𝟏 ≠ 0. Only the iff above holds.

Control added in 0.120 (measured 2026-11-26, wiki 78 §6): by the square law a random word is nilpotent half the time (0.4961 in 20,000
random 32-bit words), and the Hyperwebster words of the integers 2..100000 are nilpotent 49.9 % of the time, primes and composites alike
from three digits up. The excess seen in the 16 sedenion basis primes (68.8 %) and the 15 Moonshine primes (80 %) lives in the two-digit
range (21 primes: 81 %; 69 composites: 42 %; the 15 composites ending 1, 3, 7, 9: 27 %), and the baseline for a chance calculation is
therefore 50 %, or the prime-matched control of :func:`matched_prime_control`, not the 70 % an earlier page used.

Closed form found by chasing the two-digit anomaly (0.130, 2026-11-26, wiki 78 §7): w·w = (popcount(w) mod 2)·e₀. The square of a word is
the parity of its number of 1 bits (exhaustive for d ≤ 16, 20,000 random words at d = 32), so nilpotent means an EVEN number of 1 bits and
involutory means ODD. Parity is a ring homomorphism to GF(2): parity(a·b) = parity(a)·parity(b) (every pair at d ≤ 8), and Δ(w) = w·𝟏 =
parity(w)·𝟏. The radical is its kernel, the even-weight words: closed under XOR, dimension d − 1, and an ideal. The nilpotency indicator of the
Hyperwebster word of n is the Thue-Morse sequence of the address, which is why it is ½ for primes and composites alike (cf. Mauduit and Rivat
2010 for the binary digit sum of primes, Post-Hoc). The 17-of-21 excess of two-digit primes is one 90-number table (hypergeometric P = 0.0016,
chosen after looking; it is absent at three digits).

Version: 0.130
"""

from typing import List

# Pulled via repr() directly from TuringStack/fermat_sedenion_test.py's
# real _HW_CHARS (2026-07-11) -- a QWERTY-keyboard-row mapping, not
# alphabetical. Verified byte-for-byte against the source.
_HW_CHARS = '`1234567890-=\tqwertyuiop[]\\asdfghjkl;\'\nzxcvbnm,./ ~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
_HW_IDX = {ch: i for i, ch in enumerate(_HW_CHARS)}
_HW_N = len(_HW_CHARS)  # 97


def hw_address(n: int) -> int:
    """
    Hyperwebster address of str(n): bijective base-97 Horner encoding.

    :param n: integer whose decimal string is encoded
    :returns: the base-97 Horner address of str(n)
    """
    text = str(n)
    address = 0
    for i, ch in enumerate(reversed(text)):
        address += (_HW_IDX[ch] + 1) * (_HW_N ** i)
    return address - 1  # 0-based


def hw_to_t32(n: int) -> int:
    """
    Map integer n -> T32/GF(2) word via Hyperwebster address mod 2^32.

    :param n: integer to map
    :returns: the T32 word: the Hyperwebster address mod 2³²
    """
    return hw_address(n) & 0xFFFFFFFF


def t32_mul(a: int, b: int, dim: int = 32) -> int:
    """
    Recursive Cayley-Dickson multiplication over GF(2), dim a power of 2.
    Same construction that builds the sedenions from the reals (R->C->H->
    O->S), one doubling further, over binary field arithmetic instead of
    continuous numbers.

    :param a: T32 word
    :param b: T32 word
    :param dim: algebra dimension; a power of 2
    :returns: the product a·b as a T32 word
    """
    if dim == 1:
        return a & b
    half = dim >> 1
    mask = (1 << half) - 1
    a1, a2 = a & mask, a >> half
    b1, b2 = b & mask, b >> half
    lo = t32_mul(a1, b1, half) ^ t32_mul(b2, a2, half)
    hi = t32_mul(b2, a1, half) ^ t32_mul(a2, b1, half)
    return lo | (hi << half)


def is_zero_divisor_pair(a: int, b: int) -> bool:
    """
    Report whether a and b are nonzero words whose T32 product is zero.

    :param a: T32 word
    :param b: T32 word
    :returns: True if a ≠ 0, b ≠ 0 and a·b = 0
    """
    return a != 0 and b != 0 and t32_mul(a, b) == 0


def is_nilpotent(a: int) -> bool:
    r"""
    a != 0 but a\*a = 0 under T32 multiplication -- impossible in
    ordinary arithmetic, a real signature of zero-divisor structure.

    :param a: T32 word
    :returns: True if a ≠ 0 and a·a = 0
    """
    return a != 0 and t32_mul(a, a) == 0


def sieve(limit: int) -> List[int]:
    """
    Return the primes up to `limit` by the sieve of Eratosthenes.

    :param limit: inclusive upper bound
    :returns: the primes ≤ limit, ascending
    """
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = bytearray(len(is_p[i * i::i]))
    return [i for i, v in enumerate(is_p) if v]


def prime_nilpotency_report(primes: List[int]) -> dict:
    """
    For a given list of primes, report each one's T32 word and
    nilpotency status. The one function this module offers beyond the
    raw primitives -- meant for other engines to call directly with
    whatever prime list is relevant to them (e.g. the N-shape engine's
    Moonshine primes).

    :param primes: the primes to report on
    :returns: dict giving each prime's T32 word and nilpotency status
    """
    rows = []
    for p in primes:
        t32 = hw_to_t32(p)
        rows.append({'prime': p, 't32_word': t32, 'nilpotent': is_nilpotent(t32)})
    nilpotent_count = sum(r['nilpotent'] for r in rows)
    return {
        'rows': rows,
        'nilpotent_count': nilpotent_count,
        'total': len(primes),
        'nilpotent_pct': 100 * nilpotent_count / len(primes) if primes else 0.0,
    }


def ones(dim: int = 32) -> int:
    """
    The all-ones word of the algebra, 𝟏 = 2^dim − 1.

    :param dim: algebra dimension; a power of 2
    :returns: the word with every bit set
    """
    return (1 << dim) - 1


def trace_laplacian(w: int, dim: int = 32) -> int:
    """
    The trace-Laplacian detector Δ(w) = w·𝟏 over GF(2).

    Δ(w) = 0 exactly when w² = 0 (the corrected lemma); 𝟏 itself is not an annihilator.

    :param w: T32 word
    :param dim: algebra dimension; a power of 2
    :returns: the product w·𝟏 as a word
    """
    return t32_mul(w, ones(dim), dim)


def square_class(w: int, dim: int = 32) -> str:
    """
    Classify w by the GF(2) square law x² ∈ {0, e₀}.

    :param w: T32 word
    :param dim: algebra dimension; a power of 2
    :returns: ``'nilpotent'`` if w² = 0 (this includes w = 0), ``'involutory'`` if w² = e₀, else ``'other'``
        (the square law says ``'other'`` never occurs)
    """
    sq = t32_mul(w, w, dim)
    return 'nilpotent' if sq == 0 else 'involutory' if sq == 1 else 'other'


def radical_census(dim: int = 8) -> dict:
    """
    Exhaustive census of the algebra by the square law, with the detector check.

    :param dim: algebra dimension, a power of 2 up to 16 (2^dim words are enumerated)
    :returns: dict: ``words``, ``nilpotent`` (counting 0), ``involutory``, ``other``,
        ``detector_agrees`` (Δ(w) = 0 ⟺ w² = 0 for every word), ``one_is_annihilator`` (False),
        ``square_is_weight_parity`` (w·w = weight_parity(w) for every word), ``parity_is_homomorphism`` (every pair; None above d = 8)
    """
    if dim > 16:
        raise ValueError('radical_census enumerates 2**dim words; dim must be <= 16')
    counts = {'nilpotent': 0, 'involutory': 0, 'other': 0}
    agrees = True
    for w in range(1 << dim):
        counts[square_class(w, dim)] += 1
        agrees &= (trace_laplacian(w, dim) == 0) == (t32_mul(w, w, dim) == 0)
    one = ones(dim)
    parity_law = all(t32_mul(w, w, dim) == weight_parity(w) for w in range(1 << dim))
    homomorphism = (all(weight_parity(t32_mul(a, b, dim)) == (weight_parity(a) & weight_parity(b))
                        for a in range(1 << dim) for b in range(1 << dim)) if dim <= 8 else None)
    return {'dim': dim, 'words': 1 << dim, **counts, 'detector_agrees': agrees,
            'one_is_annihilator': t32_mul(1, one, dim) == 0,
            'square_is_weight_parity': parity_law, 'parity_is_homomorphism': homomorphism}


def nilpotency_window(lo: int, hi: int) -> dict:
    """
    Nilpotent rate of the Hyperwebster words of the integers in [lo, hi): primes against composites, with a last-digit-matched control.

    The control is the composites whose last decimal digit is 1, 3, 7 or 9 (the last digits primes above 5 can have).

    :param lo: first integer of the window (≥ 2)
    :param hi: one past the last integer of the window
    :returns: dict with ``primes``, ``composites`` and ``composites_ending_1379``, each ``{'nilpotent', 'n', 'rate'}``
    """
    is_p = set(sieve(hi))

    def tally(ns):
        ns = list(ns)
        k = sum(is_nilpotent(hw_to_t32(n)) or hw_to_t32(n) == 0 for n in ns)
        return {'nilpotent': k, 'n': len(ns), 'rate': k / len(ns) if ns else 0.0}

    pr = [n for n in range(lo, hi) if n in is_p]
    co = [n for n in range(lo, hi) if n not in is_p]
    return {'lo': lo, 'hi': hi, 'primes': tally(pr), 'composites': tally(co),
            'composites_ending_1379': tally(n for n in co if n % 10 in (1, 3, 7, 9))}


def matched_prime_control(subset: List[int], trials: int = 20000, seed: int = 1) -> dict:
    """
    Prime-matched chance control for a set of primes: how often do random primes of the same count and magnitude do as well?

    Draws ``len(subset)`` primes at random, without replacement, from the primes up to ``max(subset)`` and counts how often at least as many are
    nilpotent as in ``subset``. This is the magnitude-matched control the factoring use of the mechanism failed; it replaces the
    70 % baseline an earlier wiki page used. A subset that is every prime up to its maximum (the 16 sedenion basis primes) is its own pool, so the
    control is vacuous there (``p_at_least`` = 1); it is informative for subsets of a larger prime range.

    :param subset: the primes under test
    :param trials: number of random draws
    :param seed: seed of the random generator (fixed, so the result is reproducible)
    :returns: dict: ``observed``, ``n``, ``pool_size``, ``p_at_least`` (fraction of draws with ≥ observed nilpotent),
        ``p_all`` (fraction of draws with all n nilpotent), ``random_word_rate`` baseline 0.5
    """
    import random
    rng = random.Random(seed)
    pool = sieve(max(subset))
    nil = {p: (is_nilpotent(hw_to_t32(p)) or hw_to_t32(p) == 0) for p in pool}
    obs = sum(nil[p] for p in subset)
    ge = al = 0
    for _ in range(trials):
        k = sum(nil[p] for p in rng.sample(pool, len(subset)))
        ge += k >= obs
        al += k == len(subset)
    return {'observed': obs, 'n': len(subset), 'pool_size': len(pool), 'p_at_least': ge / trials,
            'p_all': al / trials, 'random_word_rate': 0.5}


def weight_parity(w: int) -> int:
    """
    The parity of the number of 1 bits of w: the closed form of the square law.

    w·w = weight_parity(w)·e₀, so w is nilpotent exactly when this is 0 (including w = 0) and an involutory unit when it is 1. The map
    is a ring homomorphism to GF(2): weight_parity(a·b) = weight_parity(a)·weight_parity(b).

    :param w: T32 word
    :returns: 0 if w has an even number of 1 bits, 1 if odd
    """
    return bin(w).count('1') & 1
