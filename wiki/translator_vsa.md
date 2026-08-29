# Engine: The Translator v2 — VSA / Hyperdimensional

**Module:** `modules/translator_vsa/`
**Class:** `VSATranslator`
**Notebook:** [notebooks/translator/02_vsa.ipynb](../notebooks/translator/02_vsa.ipynb)
**Claim:** Non-commutative bind, superposing bundle, and cyclic permute compose a 4096-dim sentence hypervector that folds to the same 16-dim space as version 1.

Version 2 of two. Source: *The Algebraic Geodesics of Language and Interfacial Physics*, Part A.2 — Pentti Kanerva. See [translator_discocat.md](translator_discocat.md) for version 1.

---

## The three operations

```
Permute  P(a)      cyclic shift — sequence / grammatical position
Bind     a (x) b = P(a) . b      NON-commutative (plain elementwise product is not)
Bundle   sum of vectors, deliberately UN-normalised
```

Bundle is not normalised on purpose: normalising would be a free scaling applied to make downstream similarities look better, and cosine is scale-invariant anyway, so it would buy nothing but a hidden knob.

**No PRNG anywhere.** Textbook VSA draws hypervectors from a random generator; that would make results irreproducible and would let a favourable seed be selected. Role vectors here are the prime-channel expansions of their own names (`ROLE_SUBJECT`, `ROLE_VERB`, `ROLE_OBJECT`).

## Results (run 2026-07-28)

Algebraic identities — **4/4 pass**:

```
PASS  P^-1(P(a)) == a                            residual 0.000e+00
PASS  |P(a)| == |a|                              residual 0.000e+00
PASS  a (x) b != b (x) a   (non-commutativity)   cos = 0.880
PASS  bind distributes over bundle               residual 2.910e-11
```

Capacity probe — quasi-orthogonality **measured, not assumed**:

```
dimension 4096   (Kanerva's stated regime: ~10,000)
mean|cos| = 0.9535      max|cos| = 0.9984
man/cat  +0.9984    dog/cat +0.9967    dog/man +0.9962
```

Unbind probe — constituent recovery from the bundle:

```
ROLE_SUBJECT  correct=dog    top1=True
ROLE_VERB     correct=bites  top1=False
ROLE_OBJECT   correct=man    top1=False

top1 accuracy = 0.333        chance = 0.333
```

**Recovery is exactly at chance.** Word order after folding: cosine +0.9999997 — the engine effectively cannot tell `DOG BITES MAN` from `MAN BITES DOG`.

## Why — and why it is not what Phase 22 predicts

Kanerva's capacity guarantees rest on distinct concepts being near-orthogonal. These vectors are not: ~85% of each is a shared common mode, so every cosine sits near 1 and bundling has nothing to separate.

VAPMIP `Tuning-the-Engine.md` Phase 22 established *resolution = dimension count* and made under-resolution the standing first hypothesis for any flat 16D result. That hypothesis is **testable here and comes back rejected**: the same encoder at 4096 dims is as crowded as at 16 (0.9635 vs 0.9906). Phase 22's collisions were pigeonhole exhaustion of a *discrete* route alphabet (~192 routes vs 4000 words); this is a *continuous* common-mode offset. Same symptom, different mechanism — raising to T32/T64 would not address it.

Recorded as a distinct failure mode, not as a confirmation of Phase 22.

## Confidence

| Claim | Tier |
|---|---|
| bind / bundle / permute algebra and identities | ESTABLISHED |
| bundling is recoverable at this dimension with these vectors | THEORETICAL → **measured, fails** |
| This is The Translator | **OPEN — not shown** |

## Open

- Whether to strip the common mode. That is an encoder change and could be read as tuning to produce a result — **Cody's call.**
- Whether bipolar/sign-quantised vectors (Kanerva's usual regime) would restore quasi-orthogonality without introducing a seed.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| bind / bundle / permute hypervector translation | VSA bind/bundle/permute; then unbind | 1 · SCALE | LAURELIN | DEFINITIONAL | **FLAGGED** — deficit: unbind performs AT CHANCE (0.333) — the construction does not recover the bound value |

Emergence signature: a graded failure at chance, not a one-bit break.

Calibration: this verdict agrees with the page's stated status (**OPEN**).
