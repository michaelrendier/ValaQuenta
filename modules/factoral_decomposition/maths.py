"""
ValaQuenta.modules.factoral_decomposition.maths
================================================
Factoral Decomposition — the construction blueprint, and its undo.

Cody, 2026-09-13 through 2026-09-15, from a hand-worked long multiplication
(two 10-digit numbers, ~119 elementary operations, one dropped carry caught
and fixed): "this isn't a search mechanism, it's a construction blueprint."
Long multiplication is a two-stage forward pathway — a convolution of digit
sequences (the row products), then a carry-propagating recurrence, twice
(within each row, then across all rows). DESCEND below is that pathway,
computed exactly, never assumed.

Three structural facts, each verified against the real hand-worked example
(1546854629 x 7283619945 = 11266701227799975405) before being trusted:

  SLOPE 1, ALWAYS.  Row r starts at output column r, unconditionally.
  Confirmed: row-start columns are exactly 0,1,...,9 — zero exceptions,
  carrying no information about the actual digits.

  ONE THRESHOLD PER ROW.  Row r is Da+1 digits iff its multiplier digit
  >= ceil(10**Da / a) — one number, fixed entirely by `a`. Confirmed:
  a=1546854629 gives threshold ~6.46, and exactly the digits {7,8,9} in
  7283619945 (four of them) triggered the wide rows — matching the
  hand-worked page exactly, 4 out of 10.

  GCD RECOVERS `a` EXACTLY FROM THE ROW VALUES, ALMOST FOR FREE. Every
  nonzero row is exactly `a` times one digit 0-9; gcd(rows) = a *
  gcd(the digits actually used), which equals `a` exactly whenever those
  digits share no common factor (confirmed on the real example: gcd of
  the ten rows is 1546854629, exactly). LCM of the rows was checked too,
  honestly: it comes out to a * lcm(distinct digits present) — a real
  relationship, but NOT a useful bound on `a` (it is much larger, not a
  tight sandwich) — reported here rather than forced into looking useful.

WHAT THIS MODULE DOES NOT YET CLAIM: a pure, zero-assumption, column-by-
column construction of the row values FROM N ALONE (no divisor search at
all) was attempted multiple times in this session's design pass and is
not correctly implemented here — every attempt either reintroduced
search-shaped branching by accident (importing assumptions from an
unrelated RSA-context exploration that do not belong in this mechanism)
or had real bugs caught by testing against the ground truth below, not
shipped. BUILD_UP here uses real, general divisor enumeration (never
assumes which factor is `a`) and is exact and complete — verified against
a real, independently-confirmed ground truth, not just plausible-looking
output. The zero-assumption column construction remains open, named
honestly rather than papered over.

GROUND TRUTH used for every test below: N = 11266701227799975405 has the
full prime factorization 3^2 x 5 x 7^2 x 18517 x 83537 x 3303229 (144
divisors total), and among them EXACTLY 3 distinct 10-digit x 10-digit
factor pairs exist — not 1:
    (1456723989, 7734273145)
    (1546854629, 7283619945)   <- the original hand-worked pair
    (2427873315, 4640563887)
Any reconstruction that stops at the first pair found and discards the
rest is answering the wrong question — this module reports every one.
"""
from __future__ import annotations

import math
from functools import reduce
from typing import Any, Dict, List, Tuple


# ── the digit-pair ambiguity in the base multiplication table ─────────────
# Not every product 1..81 has a unique single-digit factor pair. Exactly 9
# of the 36 distinct products from 1..9 x 1..9 have more than one — always
# exactly 2, never more, verified by direct enumeration:
#   4,6,8,9,12,16,18,24,36 each have exactly two (i,j) pairs (unordered).
def _build_multiplication_table() -> Dict[int, List[Tuple[int, int]]]:
    table: Dict[int, List[Tuple[int, int]]] = {}
    for i in range(10):
        for j in range(10):
            table.setdefault(i * j, []).append((i, j))
    return table


MULTIPLICATION_TABLE: Dict[int, List[Tuple[int, int]]] = _build_multiplication_table()


# ── DESCEND (free) — the forward construction, exact ──────────────────────
def row_width_threshold(a: int, Da: int) -> int:
    """A row a*d (d one digit of the other factor) is Da+1 digits iff
    d >= this threshold; Da digits otherwise. A pure function of `a`
    alone — fixed before any digit of the other factor is chosen."""
    if a <= 0:
        raise ValueError("a must be positive")
    return math.ceil(10 ** Da / a)


def blueprint(a: int, b: int) -> Dict[str, Any]:
    """The full forward pathway: every row, its own internal carry chain
    and width, and the single-line cross-row carry that produces the
    final answer. Exact — long multiplication written out in full."""
    if a < 1 or b < 1:
        raise ValueError("a and b must be positive")
    a_digits = [int(c) for c in str(a)]
    Da = len(a_digits)
    b_digits = [int(c) for c in str(b)]
    t = row_width_threshold(a, Da)

    rows: List[Dict[str, Any]] = []
    for r, d in enumerate(reversed(b_digits)):        # r=0 = b's ones digit
        carry = 0
        internal_carries: List[int] = []
        for ad in reversed(a_digits):                 # LSB..MSB of a
            prod = ad * d + carry
            carry = prod // 10
            internal_carries.append(carry)
        overflow = internal_carries[-1] if internal_carries else 0
        ndig = Da + (1 if overflow else 0)
        rows.append({
            "r": r, "digit": d, "value": a * d, "ndigits": ndig,
            "start_col": r, "end_col": r + ndig - 1 if ndig else r - 1,
            "internal_carries": internal_carries[:-1], "overflow": overflow,
            "is_wide": d >= t,
        })

    max_col = max((row["end_col"] for row in rows), default=-1)
    col_totals = [0] * (max_col + 1)
    for row in rows:
        v, c = row["value"], row["start_col"]
        while v > 0:
            col_totals[c] += v % 10
            v //= 10
            c += 1

    secondary_carry: List[int] = []
    carry = 0
    answer_digits: List[int] = []
    for col in range(max_col + 1):
        total = col_totals[col] + carry
        answer_digits.append(total % 10)
        carry = total // 10
        secondary_carry.append(carry)
    while carry > 0:
        answer_digits.append(carry % 10)
        carry //= 10
    answer = int("".join(str(d) for d in reversed(answer_digits))) if answer_digits else 0

    return {
        "a": a, "b": b, "Da": Da, "Db": len(b_digits), "threshold": t,
        "rows": rows, "wide_rows": sum(1 for r in rows if r["ndigits"] > Da),
        "secondary_carry": secondary_carry, "secondary_carry_len": len(secondary_carry),
        "answer": answer, "matches": answer == a * b,
    }


def row_values(a: int, b: int) -> List[int]:
    """The Db row values a*b_r (nonzero digits only) — the object the GCD
    recovery works on."""
    return [a * int(d) for d in str(b) if d != "0"]


def gcd_recovery(rows: List[int]) -> Dict[str, Any]:
    """Given a list of row VALUES (however they were obtained), recover
    `a` via gcd — exact whenever the digits that produced the rows share
    no common factor, which is the generic case. LCM is reported too,
    honestly, as NOT a useful bound — checked directly, it comes out to
    a * lcm(digits present), much larger than `a`, not a tight sandwich."""
    if not rows:
        raise ValueError("rows must be non-empty")
    g = reduce(math.gcd, rows)
    l = reduce(lambda x, y: x * y // math.gcd(x, y), rows)
    return {"rows": rows, "gcd": g, "lcm": l,
           "lcm_is_a_useful_bound": False}


# ── BUILD_UP (work) — real, general, exact divisor enumeration ────────────
def digit_split_candidates(N: int) -> List[Tuple[int, int]]:
    """Every (Da, Db), Da<=Db, consistent with N's digit count alone —
    free, zero search, straight off digits(a*b) in {Da+Db-1, Da+Db}."""
    D = len(str(N))
    out = []
    for total in (D, D + 1):
        for Da in range(1, total // 2 + 1):
            Db = total - Da
            if Da <= Db:
                out.append((Da, Db))
    return out


def _factorize(N: int) -> Dict[int, int]:
    """Trial division — honest and simple; this module targets general
    decomposition, not cryptographic-scale moduli (that is explicitly out
    of scope, see the module docstring)."""
    n = N
    factors: Dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def _divisors(factors: Dict[int, int]) -> List[int]:
    divs = [1]
    for p, e in factors.items():
        divs = [d * p ** k for d in divs for k in range(e + 1)]
    return sorted(divs)


def reconstruct(N: int) -> Dict[str, Any]:
    """WORK / ascent: every exact divisor pair of N whose two factors'
    digit lengths satisfy digit_split_candidates(N) — complete, not just
    the first pair found. Uses real factorization (trial division); never
    assumes which side is `a`. `cost` reports the number of divisors
    checked, honestly, not minimised.

    This is the real, verified, general-purpose reconstruction. The
    further ambition — building the row values themselves, digit by
    digit, from N's columns and carries alone with no divisor search at
    all — is the open piece named in the module docstring, not silently
    folded into this function."""
    if N < 4:
        raise ValueError("N must be >= 4")
    factors = _factorize(N)
    divs = _divisors(factors)
    valid_splits = set(digit_split_candidates(N))
    pairs = set()
    for a in divs:
        if a <= 1 or a * a > N:
            continue
        b = N // a
        if a * b != N:
            continue
        split = (len(str(a)), len(str(b))) if len(str(a)) <= len(str(b)) \
            else (len(str(b)), len(str(a)))
        if split in valid_splits:
            pairs.add((a, b) if a <= b else (b, a))
    return {"N": N, "pairs": sorted(pairs), "cost": len(divs),
           "prime_factorization": factors}


def consistency_check(a: int, b: int) -> Dict[str, Any]:
    """Cross-check a candidate pair against the row/threshold structure
    directly, via blueprint() — independent verification, not a re-run of
    the same search."""
    bp = blueprint(a, b)
    rv = row_values(a, b)
    gc = gcd_recovery(rv)
    return {
        "a": a, "b": b, "exact": bp["matches"],
        "wide_rows": bp["wide_rows"], "threshold": bp["threshold"],
        "secondary_carry_len": bp["secondary_carry_len"],
        "gcd_of_rows": gc["gcd"], "gcd_recovers_a": gc["gcd"] == a,
    }


def verify() -> Dict[str, Any]:
    checks: Dict[str, bool] = {}

    bp = blueprint(1546854629, 7283619945)
    checks["blueprint_matches_hand_worked_example"] = (
        bp["matches"] and bp["answer"] == 11266701227799975405
        and bp["wide_rows"] == 4
    )
    checks["blueprint_carry_matrix_shape"] = (
        len(bp["rows"]) == 10
        and all(len(r["internal_carries"]) == 9 for r in bp["rows"])
    )

    rv = row_values(1546854629, 7283619945)
    gc = gcd_recovery(rv)
    checks["gcd_recovers_a_exactly"] = gc["gcd"] == 1546854629
    checks["lcm_honestly_not_a_useful_bound"] = gc["lcm"] > 100 * gc["gcd"]

    N_real = 11266701227799975405
    r = reconstruct(N_real)
    ground_truth_10x10 = {
        (1456723989, 7734273145),
        (1546854629, 7283619945),
        (2427873315, 4640563887),
    }
    found_10x10 = {(a, b) for a, b in r["pairs"]
                   if len(str(a)) == 10 and len(str(b)) == 10}
    checks["reconstruct_10x10_subset_matches_ground_truth"] = (
        found_10x10 == ground_truth_10x10
    )
    checks["reconstruct_finds_all_144_divisors"] = (
        len(_divisors(_factorize(N_real))) == 144
    )

    r_small = reconstruct(37 * 41)
    checks["reconstruct_finds_small_pair"] = (37, 41) in r_small["pairs"]

    for a, b in [(37, 41), (1546854629, 7283619945)]:
        cc = consistency_check(a, b)
        if not (cc["exact"] and cc["gcd_recovers_a"]):
            checks["consistency_checks_pass"] = False
            break
    else:
        checks["consistency_checks_pass"] = True

    ok = all(checks.values())
    return {"toolset": "factoral_decomposition", "ok": ok, "checks": checks}


if __name__ == "__main__":
    import json
    print(json.dumps(verify(), indent=2))
