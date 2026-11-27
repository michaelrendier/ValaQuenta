# Engine: T32 Nilpotency — Shared Hyperwebster/T32/GF(2) Primitives

**File:** `modules/t32_nilpotency/maths.py`
**Class:** `T32NilpotencyModule`  
**Version:** 0.130
**Claim:** one verified-correct implementation of Hyperwebster address encoding + T32/GF(2) multiplication + nilpotency test, imported by `hypergon_constructibility` (ValaQuenta) and `fermat_monster_engine.py` (FourthAgePapers/FermatMonster, cross-repo), instead of being duplicated across both.


**Reference:** every equation with its parameters — [toolbox](toolbox/37_t32_nilpotency.md) · API — [t32_nilpotency](https://michaelrendier.github.io/ValaQuenta/api/modules/t32_nilpotency.html). This page is the record; it holds no API.

---

## Why This Is Its Own Module

Building `hypergon_constructibility` surfaced two real transcription bugs in a first copy of this exact code: a placeholder `hw_to_t32` claimed (unverified) to match the real implementation, then a fabricated 120-character `_HW_CHARS` retyped from memory instead of the real 97-character QWERTY-row mapping. Both caught by raw-number mismatches, not by inspection. Separating this into one standalone module, imported everywhere it's needed, closes off that entire class of bug — there is now exactly one place this can be wrong, not N copies that can silently diverge.

## Raw Result — 16 Sedenion Basis Primes

```
p=2   t32=0x00000002  nilpotent=False
p=3   t32=0x00000003  nilpotent=True
p=5   t32=0x00000005  nilpotent=True
p=7   t32=0x00000007  nilpotent=False
p=11  t32=0x000000C3  nilpotent=True
p=13  t32=0x000000C5  nilpotent=True
p=17  t32=0x000000C9  nilpotent=True
p=19  t32=0x000000CB  nilpotent=False
p=23  t32=0x00000126  nilpotent=True
p=29  t32=0x0000012C  nilpotent=True
p=31  t32=0x00000185  nilpotent=True
p=37  t32=0x0000018B  nilpotent=False
p=41  t32=0x000001E6  nilpotent=True
p=43  t32=0x000001E8  nilpotent=False
p=47  t32=0x000001EC  nilpotent=True
p=53  t32=0x00000249  nilpotent=True

nilpotent: 11/16 = 68.8%
```

## Cross-Repo Usage — Wired into `fermat_monster_engine.py`

A new function, `t32_nilpotency_check()`, added directly to `FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py`, imports this module (`sys.path` adjusted to reach across repos, falls back to `None` if unavailable rather than failing silently) and cross-references `MOONSHINE_PRIMES` against nilpotency and Niemeier-gap membership:

```
overall_nilpotent_pct = 80.0%
gap_filling_primes_nilpotent_pct (n=5)  = 100.0%
non_gap_primes_nilpotent_pct (n=10)     = 70.0%
```

**Read this carefully, not eagerly (updated 0.120).** The gap primes are 5 of 5 nilpotent, and 5 of 5 happens by chance 1 time in 32 for random words (a random word is nilpotent half the time) but about 1 time in 8 (0.127) for random primes up to the same size, which is the honest control (`matched_prime_control`). The excess of nilpotent primes is a two-digit-range effect; from three digits up primes and composites are both 49–50% nilpotent. This use has now met a prime-matched control and does not stand out. The earlier "70% baseline" (the observed non-gap rate) is withdrawn as a chance rate and kept here as the record. Narrative and table: Ainulindale wiki 78 §6.

## The GF(2) square law and the detector (0.110)

`radical_census(dim)` enumerates every word: x² is always 0 or e₀, so the algebra splits into the nilpotents (the radical) and the involutory units, 128 / 128 at dim 8. `trace_laplacian(w)` = w·𝟏 vanishes exactly on the nilpotents (exhaustive at dim 2, 4, 8; 2,000 random words at dim 32 in `tests/test_t32_nilpotency.py`). Corrected lemma: 𝟏 is not a global annihilator (`e₀·𝟏 = 𝟏`); the earlier UDEO white-paper proof is superseded. Narrative: Ainulindale wiki 78 §5.

## The closed form (0.130)

Chasing the two-digit anomaly to its source gave the rule behind the square law: **w·w = (number of 1 bits of w, mod 2)·e₀** (`weight_parity`). A word is nilpotent exactly when it has an even number of 1 bits and an involutory unit when odd; Δ(w) = w·𝟏 = parity(w)·𝟏; parity(a·b) = parity(a)·parity(b), a ring homomorphism to GF(2) whose kernel is the radical (the even-weight words: closed under XOR, dimension d − 1, an ideal). Checked: every word at d ≤ 16, every pair at d ≤ 8, 20,000 random words at d = 32. The nilpotency indicator of the Hyperwebster word of n is therefore the Thue-Morse sequence of the address, ½ for primes and composites alike; the earlier statement on this page that no closed form was known is withdrawn. The 17-of-21 two-digit prime excess is one 90-number table (hypergeometric P = 0.0016, a window chosen after looking) and is absent at three digits; why three digits wash it out is open (the author's reading: three digits carry the three-part structure, inclination, declination, distance; untested).

## The control (0.120)

`nilpotency_window(lo, hi)` returns the nilpotent rate of primes, composites and composites ending 1, 3, 7, 9; `matched_prime_control(subset)` returns the chance of as many nilpotent among random primes of the same count and maximum. Measured: 10–99 primes 17/21, composites 29/69, composites ending 1,3,7,9 4/15; 100–999 70/143 vs 377/757; 1,000–9,999 523/1,061 vs 3,974/7,939; 10,000–99,999 4,232/8,363 vs 40,752/81,637.

## Gallery

`gallery/t32_nilpotency/` (index and five `canvas2d_*` pages: the 128 | 128 square-law grid, the detector Δ(w) = w·𝟏, primes as T32 words with the control, primes against composites by decimal length, the zero-divisor pair matrix). Every page checks its JavaScript port against this engine on load. Launch with `gallery/t32_nilpotency/serve_gallery.sh`.

## What's Established vs. What Isn't

**ESTABLISHED:** the primitives themselves, the square law and the detector iff (exhaustive / sampled, above), — Hyperwebster encoding, T32/GF(2) multiplication, nilpotency test — verified byte-for-byte and numerically against the original source. The prime-split results are `MEASURED` counts (11 of 16 sedenion basis primes, 12 of 15 Moonshine primes), not a signal.

**NOT validated:** any specific use of these primitives as a signal for anything (factoring, Niemeier-gap membership, or otherwise). Two uses exist now (`hypergon_constructibility`, `fermat_monster_engine.t32_nilpotency_check`); one has already failed a proper control, the other hasn't been tested that way yet.

See also: `Ainulindale/wiki/78_t32_nilpotency.md`, `notebooks/core/17_t32_nilpotency.ipynb`.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the nilpotent elements of T₃₂ (the radical) | the trace-Laplacian test  w·𝟏 = 0 ⟺ w² = 0 | 2 · SIGN | TELPERION | DEFINITIONAL | **CLEAN** |


Calibration: this verdict **disagrees with** the page's stated status (**THEORETICAL**).
