# Engine: Spherical

**Module:** `modules/spherical/`  
**Notebooks:** [core/11_spherical.ipynb](../notebooks/core/11_spherical.ipynb)  
**Claim:** Standing-wave mode identification: J_N anti-Möbius period 2π → l=1 → Y₁⁰ → Re(s)=½.

---

Like `translator_common` and `sigma_cavitation`, this is a **maths-only module**: `__init__.py` and `maths.py`, no `tools.py`, no registry entry. Its functions are imported directly, including by [notebooks/core/11_spherical.ipynb](../notebooks/core/11_spherical.ipynb).

The chain it asserts: Chladni → Courant → Tesla/Schumann → J_N → ζ(s). The N-ball transformer V(n) and its peak n* live here.

## Open

- Having no formulary, this module carries no confidence tiers. Claims that depend on it inherit the tier of the module that invokes it.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the S² mode: J_N period 2π → l=1 → Y₁⁰ → Re(s)=½ | the Hopf projection chain + spherical harmonic | 2 · SIGN | MINGLING | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**maths-only**).
