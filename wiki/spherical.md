# Engine: Spherical

**Module:** `modules/spherical/`  
**Notebooks:** [core/11_spherical.ipynb](../notebooks/core/11_spherical.ipynb)  
**Claim:** Standing-wave mode identification: J_N anti-Möbius period 2π → l=1 → Y₁⁰ → Re(s)=½.

---

Like `translator_common` and `sigma_cavitation`, this is a **maths-only module**: `__init__.py` and `maths.py`, no `tools.py`, no registry entry. Its functions are imported directly, including by [notebooks/core/11_spherical.ipynb](../notebooks/core/11_spherical.ipynb).

The chain it asserts: Chladni → Courant → Tesla/Schumann → J_N → ζ(s). The N-ball transformer V(n) and its peak n* live here.

## Open

- Having no formulary, this module carries no confidence tiers. Claims that depend on it inherit the tier of the module that invokes it.
