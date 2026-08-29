# Engine: Sigma Cavitation

**Module:** `modules/sigma_cavitation/`  
**Claim:** σ-parameterised sedenion cavitation, rendered directly to SVG.

---

This module is deliberately not an equation module: it has no `tools.py`, exports only `generate`, and is absent from the registry. It is a **renderer** — it turns the cavitation geometry into an SVG figure.

Because it is not registered it has no formulary and no confidence tiers. It is documented here so that a visitor does not mistake its absence from the registry for an omission.

## Open

- The physical claim behind σ-cavitation (Bang as phase transition, BEC medium) lives in tier7_cosmos and Ainulindale, not here. This module draws the picture; it does not argue the case.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the σ-cavitation SVG render (not a registered engine) | render σ-cavitation to SVG | 1 · SCALE | LAURELIN | DESCRIPTIVE | **DESCRIPTIVE-OK** |


Calibration: this verdict agrees with the page's stated status (**renderer**).
