# Engine: Hypergon Constructibility — Gauss-Wantzel + Factorization Test

**File:** `modules/hypergon_constructibility/maths.py`
**Class:** `HypergonConstructibilityModule`
**Claim:** Of the 16 sedenion basis primes, only 4 are geometrically constructible (Gauss-Wantzel). Phase 22's corrected factorization conjecture (nilpotent split of p,q) does NOT survive a magnitude-matched control — re-tested honestly, not assumed. Version 0.200 (2026-11-27) adds Part 4, the Niemeier gap: the one finite theorem under the "N-shape" claim, proved and enumerated.


**Reference:** every equation with its parameters — [toolbox](toolbox/33_hypergon_constructibility.md) · API — [hypergon_constructibility](https://michaelrendier.github.io/ValaQuenta/api/modules/hypergon_constructibility.html). This page is the record; it holds no API.

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

### Part 2, explained (v0.200, 2026-11-27)

The close pairs' 76 % was never 110 observations. The 110 pairs are built from **25 distinct primes** (7 to 107), each appearing with the next nineteen primes, so the pairs are not independent draws. Counted once: 18 of the 25 are nilpotent (72 %); the chance of 18 or more of 25 by a fair coin is 0.022 (`close_pairs_distinct_primes`). They are also the shortest Hyperwebster addresses (one base-97 digit below 97, two from 97). Among the one-digit numbers 3 to 95 the odd primes are 18 of 23 nilpotent and the odd composites 8 of 24 (hypergeometric P = 0.0022; all primes 18 of 24 against 30 of 71 composites, P = 0.005). That is a small-number excess of the kind `t32_nilpotency` measures at two digits (P = 0.0016) and that three digits wash out; it is a property of the address map of short words, and not of factoring, because far-apart pairs sit at chance. Why short addresses of primes have even weight is open and is being chased (ledger X-64). Nilpotent means *an even number of 1 bits* in the T32 word (the square law, a ring homomorphism to GF(2)), so far-apart primes sit at 50 % by chance, and they do (47.4 % and 45.4 %). The verdict stands, and now has a reason: a short-address effect counted many times, not a factoring signal.

## Part 4 — The Niemeier gap (the theorem under the "N-shape" claim)  `ESTABLISHED` (the theorem) · `OURS` (its reading)

**Theorem.** Let R be an ADE root system of rank 24 whose components all have the same Coxeter number h (the Niemeier condition). Then h mod 16 ∉ {1, 11, 15}.

*Proof.* D_n has h = 2n − 2 and E6, E7, E8 have h = 12, 18, 30, all even. So an odd h forces every component to be A_(h−1), and k copies of A_(h−1) have rank k(h−1) = 24, so (h − 1) divides 24. The divisors of 24 are 1, 2, 3, 4, 6, 8, 12, 24, which give the odd h = 3, 5, 7, 9, 13, 25, congruent to 3, 5, 7, 9, 13, 9 modulo 16. An even h is never congruent to an odd residue. ∎

`niemeier_root_systems()` generates the root systems from the defining condition (coin-change over the A/D/E components with a given h) and gets **exactly 23** (Niemeier 1973), with h ∈ {2,3,4,5,6,7,8,9,10,12,13,14,16,18,22,25,30,46}, residues {0,2,3,4,5,6,7,8,9,10,12,13,14}. `niemeier_gap_theorem()` checks each step of the proof against that list. The earlier docstring in `FermatMonster` argued the same point through mixed-h examples (`A₁₆.A₇`), which are not Niemeier root systems; the proof above replaces it.

**The Moonshine fill.** The 15 primes dividing |Monster| fall by residue as 1: 17 · 3: 3, 19 · 5: 5 · 7: 7, 23, 71 · 9: 41 · 11: 11, 59 · 13: 13, 29 · 15: 31, 47 (and 2). They reach all three gap residues and all eight odd residues (`moonshine_gap_fill`). The control `moonshine_fill_control` counts every 14-subset of the 19 odd primes up to 71 (11,628 of them): **68 % cover the gap** and 45 % cover all eight odd residues. So the fill is what a prime set that size does anyway; it is an arithmetic fact, not evidence.

**Where the status of "Fermat's N-shape" stands.**

| statement | status |
|---|---|
| Niemeier h mod 16 misses {1, 11, 15} | theorem, proved and enumerated here |
| the 15 Moonshine primes cover the gap | arithmetic fact; 68 % of prime sets of that size do |
| 71 holomorphic c = 24 VOAs = 24 lattice + 47 others | established (Schellekens 1993; completed later) |
| "residue k is the Fermat forbidden zone at sedenion index e_k" | OURS: no definition of the zone as a set of solutions of x^l + y^m = z^n is in code |
| "generalized Fermat IS the 71 VOAs" | THEORETICAL; coverage of 16 residues by 71 objects is not an identification |

The missing link is a definition. Generalized Fermat x^p + y^q = z^r has a known structure (Darmon and Granville 1995; Beukers 1998): the signature (p, q, r) is spherical, Euclidean or hyperbolic according as 1/p + 1/q + 1/r is above, at or below 1, and the spherical signatures (2,2,n), (2,3,3), (2,3,4), (2,3,5) are exactly the A/D/E triples. That is the established place where Fermat's equation meets the ADE classification, and the natural candidate for what an "N-shape" is. It is not yet in code.

**Gauss-Wantzel without a list.** `totient_constructibility_check` tests "φ(n) is a power of 2" for every n ≤ 70,000 against the Fermat-prime test: no disagreement, 139 constructible n ≥ 3. So the five known Fermat primes are complete to 70,000 (the next, 2³² + 1 = 641 · 6,700,417, is composite).

See also: `Ainulindale/wiki/77_hypergon_constructibility.md`, `notebooks/core/16_hypergon_constructibility.ipynb`.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| which regular n-gons are compass-and-straightedge constructible | n = 2^k · ∏(distinct Fermat primes)  (Gauss–Wantzel) | 3 · SIGN | TELPERION | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).
