# Engine: Corpus

**File:** `corpus.py`  
**Class:** `CorpusProcessor`  
**Claim:** Feed any text archive to ValaQuenta: read files, split to passages, set the semantic domain from context, process every word, record every prime.

---

## What it computes

```
CorpusProcessor — Feed any text archive to the ValaQuenta.
```

`CorpusProcessor` composes `Understand`, `Lexicon` and `SemanticDomain` into a batch pipeline over a directory of text.

The domain is set **from context**, not declared per file — this is the engine that makes `semantic_domain.py`'s 'the description bounds the space' operational at archive scale.

## Open

- **Untested — no binary corpus has been loaded.** This is recorded as an open item in the wiki index and remains open. The pipeline imports and constructs; it has not been run against a real archive at scale.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| corpus statistics over an ingested binary corpus | ingest + count | 3 · ADD | LAURELIN | DEFINITIONAL | **FLAGGED** — deficit: no binary corpus loaded — the construction is defined, never run |


Calibration: this verdict agrees with the page's stated status (**UNTESTED**).
