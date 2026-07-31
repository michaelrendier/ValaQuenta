# Engine: T32 Nilpotency — Shared Hyperwebster/T32/GF(2) Primitives

**File:** `modules/t32_nilpotency/maths.py`
**Class:** `T32NilpotencyModule`
**Claim:** one verified-correct implementation of Hyperwebster address encoding + T32/GF(2) multiplication + nilpotency test, imported by `hypergon_constructibility` (ValaQuenta) and `fermat_monster_engine.py` (FourthAgePapers/FermatMonster, cross-repo), instead of being duplicated across both.

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

**Read this carefully, not eagerly.** n=5 is small — at a 70% baseline rate, getting 5/5 nilpotent by pure chance happens about 1 time in 6. Real correlation, not yet evidence. It has NOT been run through the same magnitude-matched-control discipline that caught the factoring use of this same mechanism as an artifact (see `hypergon_constructibility`) — don't treat this number as more settled than that until it has been.

## What's Established vs. What Isn't

**ESTABLISHED:** the primitives themselves — Hyperwebster encoding, T32/GF(2) multiplication, nilpotency test — verified byte-for-byte and numerically against the original source.

**NOT validated:** any specific use of these primitives as a signal for anything (factoring, Niemeier-gap membership, or otherwise). Two uses exist now (`hypergon_constructibility`, `fermat_monster_engine.t32_nilpotency_check`); one has already failed a proper control, the other hasn't been tested that way yet.

See also: `Ainulindale/wiki/78_t32_nilpotency.md`, `notebooks/core/17_t32_nilpotency.ipynb`.
