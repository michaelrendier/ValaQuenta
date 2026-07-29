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
