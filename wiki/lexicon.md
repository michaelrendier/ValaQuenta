# Engine: Lexicon

**File:** `lexicon.py`  
**Class:** `Lexicon`  
**Claim:** Accumulated experience: maps Riemann zeros (primes) to the surface forms that point at them, persists across sessions, grows with every corpus.

---

## What it computes

```
Lexicon — The accumulated experience of the ValaQuenta.
```

The lexicon is deliberately the inverse of a dictionary. A dictionary maps a string to a meaning; this maps a prime — a Riemann zero — to the set of strings observed pointing at it. The prime preexists the alphabet.

It persists to disk, so experience accumulates across runs.

## Open

- **Untested at scale for the same reason as `corpus.py`** — no binary corpus loaded. Paired open item in the wiki index.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| lexicon statistics over an ingested binary corpus | ingest + index | 3 · ADD | LAURELIN | DEFINITIONAL | **FLAGGED** — deficit: no binary corpus loaded — defined, never run |


Calibration: this verdict agrees with the page's stated status (**UNTESTED**).
