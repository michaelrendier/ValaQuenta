# Engine: The Translator v1 — DisCoCat

**Module:** `modules/translator_discocat/`
**Classes:** `PregroupType`, `MeaningSpace`, `DisCoCatTranslator`
**Notebook:** [notebooks/translator/01_discocat.ipynb](../notebooks/translator/01_discocat.ipynb)
**Claim:** The pregroup reduction `n·(nʳ·s·nˡ)·n → s` maps functorially onto contraction of an order-3 verb tensor against subject and object vectors, composing a sentence vector in the 16-dim prime-channel space.

Version 1 of two. Source: *The Algebraic Geodesics of Language and Interfacial Physics*, Part A.1 — Coecke, Clark & Grefenstette. See [translator_vsa.md](translator_vsa.md) for version 2.

---

## Results (run 2026-07-28)

Pregroup algebra self-test — **6/6 pass**, including three negative controls that must *not* reduce:

```
PASS  n . n^r                   -> '1'
PASS  n^l . n                   -> '1'
PASS  transitive clause         -> 's'
PASS  n . n   (no cancel)       -> 'n . n'
PASS  n^r . n (wrong order)     -> 'n^r . n'
PASS  n . s^r (mismatch)        -> 'n . s^r'
```

Word order, `DOG BITES MAN` vs `MAN BITES DOG`:

```
cosine = +0.991347        distinguishes_word_order = True
```

It does separate the two readings — but only in the 4th decimal place. See the standing result below.

## Derived dimensions — nothing chosen

```
N = S = 16          the sedenion basis / 16 prime channels (p = 2..53)
verb tensor  n^r.s.n^l   ->  order-3 in N (x) S (x) N  =  16^3 = 4096
```

4096 is **not** a "big enough for HDC" number. It is the transitive-verb tensor order, forced by taking the sedenion as the noun space. That it coincides with the VSA hypervector length is what makes the two engines combinable, and neither was adjusted to make it line up.

## The functor

```
s_j = sum_i sum_k  subj_i * T[i][j][k] * obj_k
```

The two pregroup cancellations `(n nʳ)` and `(nˡ n)` become the two tensor contractions. A clause whose type does not reduce to `s` raises rather than composing anyway — that composition is undefined, not merely low quality.

## Confidence

| Claim | Tier |
|---|---|
| Pregroup reduction `x^(a) x^(a+1) → 1` | ESTABLISHED (Lambek) |
| Reduction ↔ tensor contraction functor | ESTABLISHED (standard DisCoCat) |
| Composed vector is *the meaning* | THEORETICAL |
| This is The Translator | **OPEN — not shown** |

Tiers are deliberately not flattened; see `_crosscutting` item 3 in `.clauderc_ValaQuenta`.

## Standing result — concept crowding

Both Translator versions share the prime-channel encoder, and it does not separate concepts: mean |cos| ≈ 0.99 between distinct tokens at 16 dims. Roughly 85% of every token vector is a single shared direction.

Phase 22 of VAPMIP `docs/wiki/Tuning-the-Engine.md` makes under-resolution the standing first hypothesis for a flat 16D result. **Tested and rejected here** — the identical encoder at 4096 dims is just as crowded (0.9635 vs 0.9906). The cause is a common mode in the encoder, which is dimension-independent, so raising the CD level would not fix it.

Left in place per Prime Directive #2. Not patched, not centred, not rescaled.

## Open

- Whether removing the common mode is legitimate here, or whether it counts as tuning the encoder to produce a result. **Cody's call, not Claude's.**
- Verb tensors are built from the token's own harmonics, so the engine has no notion of a verb's *argument structure* beyond what the string itself encodes.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| pregroup → tensor compositional translation | pregroup contraction → tensor; word-order cos = 0.9913 | 3 · SCALE | LAURELIN | DEFINITIONAL | **FLAGGED** — deficit: the prime-channel encoder carries ~85% common mode with 2–3% content — concepts do not separate |


Calibration: this verdict agrees with the page's stated status (**OPEN**).
