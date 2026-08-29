# Engine: Hypergon Constructibility — Gauss-Wantzel + Factorization Test

**File:** `modules/hypergon_constructibility/maths.py`
**Class:** `HypergonConstructibilityModule`
**Claim:** Of the 16 sedenion basis primes, only 4 are geometrically constructible (Gauss-Wantzel). Phase 22's corrected factorization conjecture (nilpotent split of p,q) does NOT survive a magnitude-matched control — re-tested honestly, not assumed.

---

## Part 1 — Raw Result: All 16 Hyper-N-Gons

```
e0   p=2   fermat_prime=False  power_of_2=True   CONSTRUCTIBLE
e1   p=3   fermat_prime=True   power_of_2=False  CONSTRUCTIBLE
e2   p=5   fermat_prime=True   power_of_2=False  CONSTRUCTIBLE
e3   p=7   fermat_prime=False  power_of_2=False  hole
e4   p=11  fermat_prime=False  power_of_2=False  hole
e5   p=13  fermat_prime=False  power_of_2=False  hole
e6   p=17  fermat_prime=True   power_of_2=False  CONSTRUCTIBLE
e7   p=19  fermat_prime=False  power_of_2=False  hole
e8   p=23  fermat_prime=False  power_of_2=False  hole
e9   p=29  fermat_prime=False  power_of_2=False  hole
e10  p=31  fermat_prime=False  power_of_2=False  hole
e11  p=37  fermat_prime=False  power_of_2=False  hole
e12  p=41  fermat_prime=False  power_of_2=False  hole
e13  p=43  fermat_prime=False  power_of_2=False  hole
e14  p=47  fermat_prime=False  power_of_2=False  hole
e15  p=53  fermat_prime=False  power_of_2=False  hole
```

**4/16 constructible (e0, e1, e2, e6), 12/16 holes.** This is real, established mathematics — the Gauss-Wantzel theorem (1796/1837): a regular n-gon is constructible with straightedge and compass iff n = 2^k × (product of distinct Fermat primes). Only five Fermat primes are known to exist, ever: 3, 5, 17, 257, 65537 (whether more exist is a genuine open problem in number theory). This generalizes Phase 19's single "13-gon is non-constructible" observation to the full 16-position sweep, computed directly rather than extrapolated from one example.

## Part 2 — Raw Result: Re-Testing Phase 22's Factorization Conjecture

Phase 22 (Tuning-the-Engine.md, 2026-06-30) corrected the factoring conjecture from "Fermat midpoint parameters a,b land on ZD pairs" to "the actual prime factors p, q individually sit in the nilpotent locus of T32/GF(2)," reporting q at +26 percentage points above the 50% baseline. That number was reproduced here — but only for close-magnitude pairs, and it does not survive being checked against a proper control:

```
close_prime_pairs   (n=110):  p=69.1%  q=76.4%  both=52.7%
far_apart_prime_pairs (n=97): p=47.4%  q=45.4%  both=22.7%
random_pair_control  (n=97):  p=50.5%  q=56.7%  both=26.8%

survives_magnitude_matched_control = False
```

If the mechanism tracked genuine factoring structure, far-apart real factor pairs should beat the random (non-factor) control. They don't — the random control's q (56.7%) is actually *higher* than the far-apart real factor pairs' q (45.4%). The close-pair elevation Phase 22 reported is consistent with a magnitude artifact of how small numbers map through the Hyperwebster base-97 address encoding into T32/GF(2), not with the mechanism actually distinguishing real factor pairs from arbitrary primes.

## Two Real Bugs Caught During This Engine's Own Construction

Not hidden, flagged directly in `maths.py`'s comments:

1. A first draft of `hw_to_t32` was a placeholder (`n & 0xFFFFFFFF`) with a docstring claiming it "matches TuringStack/fermat_sedenion_test.py's hw_to_t32 exactly" — a claim made without checking. It did not match. Caught by a raw-number discrepancy between this module's first run and an earlier standalone verification in the same session.
2. The fix attempt then hand-transcribed `_HW_CHARS` (the base-97 Hyperwebster character set) from a vague recollection of a docstring fragment seen earlier — a fabricated 120-character alphabetical string, when the real one is a 97-character QWERTY-keyboard-row mapping. Caught the same way: numbers still didn't match, so the string itself was diffed character-by-character against the real source rather than assumed correct.

Final fix: the real `_HW_CHARS` was pulled via `repr()` and pasted verbatim, then verified byte-for-byte and numerically identical to the original across 21 test values before trusting any further output.

## Part 3 — The Definition of Primes This Engine Actually Supports

**Arithmetic:** a prime has no non-trivial factorization. This is exactly why AbrikosovTree's CD-tower structure has primes as leaves surviving all 9 levels — no factorization means no zero-divisor pair can form, so the norm never fails.

**Geometric:** constructibility (Part 1, verified) is the exception among primes, not the rule — 4 of 16 basis primes, not most of them.

**Unification status: open.** Part 2 shows the one candidate bridge between geometric/algebraic structure and actual factoring (the nilpotent-split conjecture) does not survive a fair test. The arithmetic and geometric definitions are both real; a working mechanism connecting either to factoring a composite N remains genuinely unsolved.

See also: `Ainulindale/wiki/77_hypergon_constructibility.md`, `notebooks/core/16_hypergon_constructibility.ipynb`.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| which regular n-gons are compass-and-straightedge constructible | n = 2^k · ∏(distinct Fermat primes)  (Gauss–Wantzel) | 3 · SIGN | TELPERION | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).
