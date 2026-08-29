# Engine: Translator Common

**Module:** `modules/translator_common/`  
**Claim:** The shared substrate both Translator versions are built on: the derived vector space, the prime-channel encoder, and the combination harness.

---

Explicitly **not a registered engine** — no `tools.py`, no EquationModule, absent from the registry by design, and its own docstring says so.

It matters because it is the common cause of both translators' central failure: the prime-channel encoder puts roughly 85% common mode into every vector, so distinct concepts do not separate. Both [translator_discocat.md](translator_discocat.md) and [translator_vsa.md](translator_vsa.md) inherit that from here.

**No PRNG anywhere.** Role vectors are prime-channel expansions of their own names, so results are reproducible and no favourable seed can be picked.

## Open

- Whether to strip the common mode. It would likely fix both translators, and it would be an encoder change made because the result was disappointing — which is tuning. **Cody's call.** Recorded, not acted on.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the shared prime-channel encoder (no PRNG anywhere) | deterministic encode into the 16 prime channels | 0 · ADD | LAURELIN | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**substrate**).
