"""
ainulindale_engine.modules.t32_nilpotency.maths
===================================================
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

Version: 0.100
"""

from typing import List

# Pulled via repr() directly from TuringStack/fermat_sedenion_test.py's
# real _HW_CHARS (2026-07-11) -- a QWERTY-keyboard-row mapping, not
# alphabetical. Verified byte-for-byte against the source.
_HW_CHARS = '`1234567890-=\tqwertyuiop[]\\asdfghjkl;\'\nzxcvbnm,./ ~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
_HW_IDX = {ch: i for i, ch in enumerate(_HW_CHARS)}
_HW_N = len(_HW_CHARS)  # 97


def hw_address(n: int) -> int:
    """Hyperwebster address of str(n): bijective base-97 Horner encoding."""
    text = str(n)
    address = 0
    for i, ch in enumerate(reversed(text)):
        address += (_HW_IDX[ch] + 1) * (_HW_N ** i)
    return address - 1  # 0-based


def hw_to_t32(n: int) -> int:
    """Map integer n -> T32/GF(2) word via Hyperwebster address mod 2^32."""
    return hw_address(n) & 0xFFFFFFFF


def t32_mul(a: int, b: int, dim: int = 32) -> int:
    """Recursive Cayley-Dickson multiplication over GF(2), dim a power of 2.
    Same construction that builds the sedenions from the reals (R->C->H->
    O->S), one doubling further, over binary field arithmetic instead of
    continuous numbers."""
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
    return a != 0 and b != 0 and t32_mul(a, b) == 0


def is_nilpotent(a: int) -> bool:
    """a != 0 but a*a = 0 under T32 multiplication -- impossible in
    ordinary arithmetic, a real signature of zero-divisor structure."""
    return a != 0 and t32_mul(a, a) == 0


def sieve(limit: int) -> List[int]:
    is_p = bytearray([1]) * (limit + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = bytearray(len(is_p[i * i::i]))
    return [i for i, v in enumerate(is_p) if v]


def prime_nilpotency_report(primes: List[int]) -> dict:
    """For a given list of primes, report each one's T32 word and
    nilpotency status. The one function this module offers beyond the
    raw primitives -- meant for other engines to call directly with
    whatever prime list is relevant to them (e.g. the N-shape engine's
    Moonshine primes)."""
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
