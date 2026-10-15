"""
ValaQuenta.modules.addition_matrix.maths
========================================
The addition matrix of long multiplication, read as arithmetic modulo ``10^k``.

Grade-school multiplication of ``num1`` by ``num2`` writes one row per digit of
``num2``: row ``j`` is ``num1 * digit_j`` shifted ``j`` places. Adding the rows
column by column gives the product. This module has four parts.

* **A. The matrix itself** (the core of the Multiplication Matrix Explorer):
  the rows, the running sums and the carry matrix, checked against ``*``.
* **B. The columns as rotors**: the digit in column ``c`` is a function of
  ``num2`` with an exact period, ``x -> a x + b`` on ``Z/10^m`` has a cycle type
  that factors through ``Z/2^m x Z/5^m`` (Chinese remainder theorem), and the
  odometer ``x -> x + 1`` returns to a coarser odometer.
* **C. The law of the factor search**: digit-by-digit factor reconstruction
  keeps exactly the pairs ``(p, q) mod 10^(c+1)`` with ``p q = N`` there. The
  number of such pairs has a closed form, a product over the primes 2 and 5.
  For ``N`` with both valuations below ``c + 1`` it is
  ``(v2 + 1)(v5 + 1) phi(10^(c+1))``, i.e. unit-group torsors, times 10 per column.
* **D. The address of the final answer**: for each unit solution mod ``10^n`` the
  overflow ``K = (p' q' - N) / 10^n`` is an integer, and the true factorisation
  is exactly ``K = 0``.

Everything is exact integer arithmetic and standard library only. Where a result
is a count, it is checked by exhaustive enumeration in the tests, not sampled.
Nothing here is a factoring method that beats the search it describes: the live
state count is the quantity the module measures.

Labels: A is ESTABLISHED arithmetic. B and C are ESTABLISHED:CALCULATED (each
statement is a theorem of elementary number theory, and the code checks it
exhaustively over the stated range). D is OURS: the K = 0 address is a
restatement, and the module records that the address is not isolated.
"""

from __future__ import annotations

import statistics
from math import gcd
from typing import Dict, List, Optional, Tuple


# ── A. the matrix ──────────────────────────────────────────────────────────

def digits_lsb(n: int, width: int) -> List[int]:
    """Decimal digits of ``n``, least significant first, zero padded to ``width``.

    Raises ``ValueError`` when ``n`` needs more than ``width`` digits.

    :param n: non-negative integer
    :param width: number of digits to return
    :returns: list of digits
    :raises ValueError: when n needs more than width digits
    """
    out = []
    for _ in range(width):
        out.append(n % 10)
        n //= 10
    if n:
        raise ValueError(f"{n} needs more than {width} digits")
    return out


def matrix_rows(num1: int, num2: int, n_digits: int = 10) -> List[List[Optional[int]]]:
    """The addition matrix: one row per digit of ``num2``; ``None`` marks a blank cell.

    Row ``j`` holds the digits of ``num1 * digit_j`` starting at column ``j``.
    The grid has ``2 n_digits + 1`` columns, the explorer's ``N_COLUMNS`` (the
    widest row has ``n_digits + 1`` digits and the largest shift is
    ``n_digits - 1``; the last column is never used by a product).

    :param num1: the multiplicand
    :param num2: the multiplier
    :param n_digits: digits per input number
    :returns: list of rows, each a list of digits or None
    """
    n_cols = 2 * n_digits + 1
    d2 = digits_lsb(num2, n_digits)
    rows: List[List[Optional[int]]] = []
    for j in range(n_digits):
        cells: List[Optional[int]] = [None] * n_cols
        for k, d in enumerate(digits_lsb(num1 * d2[j], n_digits + 1)):
            cells[j + k] = d
        rows.append(cells)
    return rows


def carry_matrix(num1: int, num2: int, n_digits: int = 10) -> Tuple[List[List[int]], int]:
    """Carries of adding the rows one at a time into a running total.

    Returns ``(carries, product)``, ``carries[j][c]`` being the carry out of
    column ``c`` when row ``j`` is added. Adding two numbers at a time keeps
    every carry in ``{0, 1}``; that is the property the explorer's colour scheme
    relies on and the tests check it.

    :param num1: the multiplicand
    :param num2: the multiplier
    :param n_digits: digits per input number
    :returns: (carries, product)
    """
    n_cols = 2 * n_digits + 1
    total = [0] * n_cols
    carries = []
    for row in matrix_rows(num1, num2, n_digits):
        carry, out = 0, [0] * n_cols
        for c in range(n_cols):
            s = total[c] + (row[c] or 0) + carry
            total[c], carry = s % 10, s // 10
            out[c] = carry
        assert carry == 0
        carries.append(out)
    return carries, sum(d * 10 ** c for c, d in enumerate(total))


# ── B. the columns as rotors ───────────────────────────────────────────────

def column_period(num1: int, c: int) -> int:
    """Exact period in ``num2`` of the digit in column ``c`` of ``num1 * num2``.

    Column ``c`` of the product depends on ``num2`` only modulo ``10^(c+1)``.
    The digit is ``floor(num1 * x / 10^c) mod 10``, and the period of
    ``x -> num1 * x mod 10^(c+1)`` is ``10^(c+1) / gcd(num1, 10^(c+1))``.

    :param num1: the multiplicand
    :param c: column index, 0 = units
    :returns: the period
    """
    m = 10 ** (c + 1)
    return m // gcd(num1, m)


def column_period_measured(num1: int, c: int) -> int:
    """The least ``t > 0`` with ``digit_c(num1 * (x + t)) == digit_c(num1 * x)`` for every ``x``.

    Found by trying the divisors of ``10^(c+1)`` in increasing order and testing
    every ``x`` in one full range, so it is exact, not sampled.

    :param num1: the multiplicand
    :param c: column index, 0 = units
    :returns: the least period found
    """
    m = 10 ** (c + 1)
    f = lambda x: (num1 * x // 10 ** c) % 10
    divisors = sorted(d for d in range(1, m + 1) if m % d == 0)
    for t in divisors:
        if all(f(x + t) == f(x) for x in range(m)):
            return t
    return m


def cycle_type(perm_next, size: int) -> Dict[int, int]:
    """Cycle lengths of a permutation of ``range(size)`` as ``{length: count}``.

    ``perm_next(x)`` must be a bijection; the function raises ``ValueError``
    otherwise (a non-unit multiplier gives a map that is not a permutation).

    :param perm_next: function giving the image of each point
    :param size: number of points
    :returns: {cycle length: number of cycles}
    :raises ValueError: when perm_next is not a bijection
    """
    seen = bytearray(size)
    if len({perm_next(x) for x in range(size)}) != size:
        raise ValueError("not a permutation")
    out: Dict[int, int] = {}
    for s in range(size):
        if seen[s]:
            continue
        n, x = 0, s
        while not seen[x]:
            seen[x] = 1
            x = perm_next(x)
            n += 1
        out[n] = out.get(n, 0) + 1
    return out


def affine_cycle_type(a: int, b: int, m: int) -> Dict[int, int]:
    """Cycle type of ``x -> a x + b`` on ``Z/m`` (requires ``gcd(a, m) = 1``).

    :param a: multiplier, coprime to m
    :param b: increment
    :param m: modulus
    :returns: {cycle length: number of cycles}
    """
    return cycle_type(lambda x: (a * x + b) % m, m)


def crt_combine(t2: Dict[int, int], t5: Dict[int, int]) -> Dict[int, int]:
    """Cycle type of a product of two permutations acting on coprime factors.

    A cycle of length ``l1`` and one of length ``l2`` give ``gcd(l1, l2)`` cycles
    of length ``lcm(l1, l2)``.

    :param t2: cycle type on the first factor, {length: count}
    :param t5: cycle type on the second factor, {length: count}
    :returns: {cycle length: number of cycles}
    """
    out: Dict[int, int] = {}
    for l1, n1 in t2.items():
        for l2, n2 in t5.items():
            g = gcd(l1, l2)
            l = l1 * l2 // g
            out[l] = out.get(l, 0) + n1 * n2 * g
    return out


def crt_rule_check(a: int, b: int, m: int) -> bool:
    """Whether the cycle type of ``x -> a x + b`` on ``Z/10^m`` equals the CRT combination of its types on ``Z/2^m`` and ``Z/5^m``.

    :param a: multiplier, coprime to 10
    :param b: increment
    :param m: exponent: the modulus is 10^m
    :returns: True when the two computations agree
    """
    whole = affine_cycle_type(a, b, 10 ** m)
    return whole == crt_combine(affine_cycle_type(a, b, 2 ** m), affine_cycle_type(a, b, 5 ** m))


def odometer_first_return(m: int) -> Dict[str, object]:
    """First-return map of ``x -> x + 1`` on ``Z/10^m`` to the set ``x = 0 mod 10``.

    The induced map on that set, relabelled by ``x / 10``, is the odometer on
    ``Z/10^(m-1)``. Returns the induced map's cycle length and whether it equals
    ``x -> x + 1`` on the quotient exactly.

    :param m: exponent: the odometer runs on Z/10^m
    :returns: dict with set size, whether the induced map is the odometer one scale down, and its cycle type
    """
    M = 10 ** m
    sub = [x for x in range(0, M, 10)]
    induced = {x: (x + 10) % M for x in sub}  # first return of +1 to multiples of 10
    ok = all(induced[x] // 10 == (x // 10 + 1) % (M // 10) for x in sub)
    cyc = cycle_type(lambda y: (y + 1) % (M // 10), M // 10)
    return {"set_size": len(sub), "is_odometer_one_scale_down": ok, "cycle_type": cyc}


def solenoid_cycles(a: int, b: int, n: int) -> Dict[int, int]:
    """Cycle type of ``x -> a x + b`` on ``Z/2^n`` (``a`` odd): every length is a power of two.

    :param a: odd multiplier
    :param b: increment
    :param n: exponent: the modulus is 2^n
    :returns: {cycle length: number of cycles}
    """
    return affine_cycle_type(a, b, 2 ** n)


# ── C. the law of the factor search ────────────────────────────────────────

def valuation(N: int, p: int, cap: Optional[int] = None) -> int:
    """The exponent of the prime ``p`` in ``N`` (``cap`` stops the count; ``N = 0`` gives ``cap``).

    :param N: integer
    :param p: prime
    :param cap: stop counting here; None for no limit
    :returns: the exponent of p in N
    """
    if N == 0:
        return cap if cap is not None else 10 ** 9
    v = 0
    while N % p == 0 and (cap is None or v < cap):
        N //= p
        v += 1
    return v


def phi_prime_power(p: int, k: int) -> int:
    """Euler's phi of ``p^k``.

    :param p: prime
    :param k: exponent
    :returns: phi(p^k)
    """
    return p ** (k - 1) * (p - 1)


def prime_power_solutions(N: int, p: int, k: int) -> int:
    """Number of ``(a, b)`` in ``(Z/p^k)^2`` with ``a b = N`` modulo ``p^k``.

    With ``v = min(v_p(N), k)``: ``(v + 1) phi(p^k)`` when ``v < k``, and
    ``k phi(p^k) + p^k`` when ``N`` is 0 mod ``p^k``. Each valuation split
    ``v(a) = i`` contributes ``phi(p^k)`` pairs; when ``N = 0`` the pair with
    ``a = 0`` contributes ``p^k`` more.

    :param N: target product
    :param p: prime
    :param k: exponent: the modulus is p^k
    :returns: the number of pairs
    """
    v = valuation(N, p, cap=k)
    if v < k:
        return (v + 1) * phi_prime_power(p, k)
    return k * phi_prime_power(p, k) + p ** k


def solution_count_closed(N: int, k: int) -> int:
    """Closed form for the number of ``(p, q)`` mod ``10^k`` with ``p q = N`` there: the product over the primes 2 and 5 (CRT).

    :param N: target product
    :param k: exponent: the modulus is 10^k
    :returns: the number of pairs
    """
    return prime_power_solutions(N, 2, k) * prime_power_solutions(N, 5, k)


def solution_count_brute(N: int, k: int) -> int:
    """The same count by enumeration: for each ``a``, the equation ``a b = N`` mod ``M`` has ``gcd(a, M)`` solutions when ``gcd(a, M)`` divides ``N``, else none.

    :param N: target product
    :param k: exponent: the modulus is 10^k
    :returns: the number of pairs
    """
    M = 10 ** k
    return sum(gcd(a, M) for a in range(M) if (N % M) % gcd(a, M) == 0)


def live_state_counts(N: int, n_digits: int) -> List[int]:
    """Live states after each column of the digit-by-digit factor search for ``n_digits``-digit factors.

    The search extends both factors by one digit per column and keeps a pair
    only when the column's digit of ``p q`` equals the digit of ``N``. For
    columns beyond ``n_digits`` there is no new digit and the pair is kept
    only if the digit still matches. Element ``c`` is the count after column ``c``.

    :param N: the number to factor
    :param n_digits: digits allowed in each factor
    :returns: live states after each column
    """
    states = [(0, 0)]
    counts = []
    for c in range(2 * n_digits):
        mod = 10 ** (c + 1)
        target = N % mod
        nxt = []
        if c < n_digits:
            step = 10 ** c
            for p, q in states:
                for dp in range(10):
                    P = p + dp * step
                    for dq in range(10):
                        Q = q + dq * step
                        if (P * Q) % mod == target:
                            nxt.append((P, Q))
        else:
            nxt = [(p, q) for p, q in states if (p * q) % mod == target]
        states = nxt
        counts.append(len(states))
    return counts


def torsor_orbits(N: int, k: int) -> Optional[int]:
    """Number of unit-group orbits in the solution set mod ``10^k`` when both valuations are below ``k``.

    The unit group acts by ``(p, q) -> (u p, u^-1 q)``. Each valuation split
    ``(i, j)`` with ``i <= v2``, ``j <= v5`` is one orbit and the orbit is a
    torsor of the unit group, so the count is ``(v2 + 1)(v5 + 1)``. Returns
    ``None`` when either valuation is ``>= k``.

    :param N: target product
    :param k: exponent: the modulus is 10^k
    :returns: number of orbits, or None when a valuation is at least k
    """
    v2, v5 = valuation(N, 2, cap=k), valuation(N, 5, cap=k)
    if v2 >= k or v5 >= k:
        return None
    return (v2 + 1) * (v5 + 1)


def unit_group_order(k: int) -> int:
    """Order of ``(Z/10^k)^x``: ``4 * 10^(k-1)``.

    :param k: exponent: the modulus is 10^k
    :returns: 4 * 10^(k-1)
    """
    return phi_prime_power(2, k) * phi_prime_power(5, k)


# ── D. the address of the final answer ─────────────────────────────────────

def unit_solutions(N: int, n: int) -> List[Tuple[int, int, int]]:
    """Every unit pair ``(p', q')`` mod ``10^n`` with ``p' q' = N`` there, with its overflow ``K``.

    ``K = (p' q' - N) / 10^n`` is an integer. ``p'`` runs over the residues
    coprime to 10 and ``q' = N / p'`` is taken in ``[0, 10^n)``. The true
    factorisation of ``N`` into two ``n``-digit numbers is ``K = 0``.
    Requires ``gcd(N, 10) = 1`` (otherwise the pairs are not all units).

    :param N: target product, coprime to 10
    :param n: exponent: the modulus is 10^n
    :returns: list of (p, q, K)
    :raises ValueError: when gcd(N, 10) is not 1
    """
    M = 10 ** n
    if gcd(N, 10) != 1:
        raise ValueError("unit_solutions needs N coprime to 10")
    out = []
    for p in range(1, M):
        if gcd(p, 10) != 1:
            continue
        q = (N * pow(p, -1, M)) % M
        out.append((p, q, (p * q - N) // M))
    return out


def address_profile(N: int, n: int) -> Dict[str, object]:
    """How the ``K = 0`` address sits among the unit solutions of ``N`` mod ``10^n``.

    Reports the number of solutions, how many have ``K = 0`` (the true pair and
    its swap, plus the trivial pair when ``N < 10^n``), and the smallest, median
    and largest nonzero ``|K|``: the address exists and is unique among the
    zero-overflow solutions, but near-misses with small ``|K|`` also exist.

    :param N: target product, coprime to 10
    :param n: exponent: the modulus is 10^n
    :returns: dict of counts and the nonzero-K statistics
    """
    sols = unit_solutions(N, n)
    ks = [abs(k) for _, _, k in sols]
    nz = sorted(k for k in ks if k)
    return {
        "n": n, "solutions": len(sols), "zero_overflow": ks.count(0),
        "smallest_nonzero_K": nz[0] if nz else None,
        "median_nonzero_K": statistics.median(nz) if nz else None,
        "largest_K": max(ks), "median_K_all": statistics.median(ks),
        "zero_overflow_pairs": sorted((p, q) for p, q, k in sols if k == 0),
    }


def lift_branching(N: int, k: int) -> Dict[int, int]:
    """Children per unit solution when lifting from ``10^k`` to ``10^(k+1)``, as ``{children: count}``.

    Every unit solution mod ``10^k`` has exactly ten lifts mod ``10^(k+1)``
    (one factor's new digit is free, the other is then forced): the tree of
    solutions is uniformly 10-ary, which is the measured ×10 per digit.

    :param N: target product, coprime to 10
    :param k: exponent of the lower modulus 10^k
    :returns: {children: number of solutions}
    """
    lo = {(p, q) for p, q, _ in unit_solutions(N, k)}
    hi = [(p, q) for p, q, _ in unit_solutions(N, k + 1)]
    kids: Dict[Tuple[int, int], int] = {s: 0 for s in lo}
    M = 10 ** k
    for p, q in hi:
        kids[(p % M, q % M)] += 1
    out: Dict[int, int] = {}
    for n_ in kids.values():
        out[n_] = out.get(n_, 0) + 1
    return out
