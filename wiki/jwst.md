# Engine: JWST  Spectral Pixel  →  𝕆

**Module:** `modules/jwst/`  
**Version:** 0.111  
**Confidence floor:** THEORETICAL  
**Notebooks:** [core/10_jwst.ipynb](../notebooks/core/10_jwst.ipynb)  
**Claim:** A JWST spectral pixel maps to an octonion, giving every pixel an address in the Cayley-Dickson tower.

---

## What it computes

JWST NIRCam spectral pixel module. 8 filter intensities (900–4440nm) → 8 octonion components. Cayley-Dickson addressing: λ → r ∈ (0,1). One 𝕆 element per sky pixel.

`synthetic_hydrogen` and `synthetic_stellar` are ESTABLISHED because they are synthetic: the module generates its own spectra to exercise the map. They are **not** JWST observations, and the ESTABLISHED tag covers the generator, not an astrophysical claim.

`lambda_to_r` round-trips 2000.0 nm → r=0.3107 → 1999.99 nm.

## Results — run 2026-07-28

5/5 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `lambda_to_r` | ESTABLISHED | ✓ | {'wavelength_nm': 2000.0, 'r': 0.31073446327674836, 'lambda_back': 1999.9999999996892} |
| `synthetic_hydrogen` | ESTABLISHED | ✓ | {'type': 'hydrogen', 'intensities': [4.772217220174583e-11, 1.9638082208988035e-06, 0.00… |
| `synthetic_stellar` | ESTABLISHED | ✓ | {'type': 'stellar', 'intensities': [1.0, 0.6150018599635491, 0.31446535401390957, 0.1348… |
| `cd_spectral_address` | THEORETICAL | ✓ | {'pixel': (0, 0), 'pixel_addr': 0, 'alg_R': 1.0, 'alg_C': [1.0, 1.0], 'alg_H': [1.0, 1.0… |
| `spectral_to_octonion` | THEORETICAL | ✓ | {'components': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], 'norm': 2.8284271247461903, 'r_… |

## Open

- The two equations that carry the actual claim — `spectral_to_octonion` and `cd_spectral_address` — are THEORETICAL. No real JWST data is loaded by this module.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the spectral pixel → sedenion channel map (synthetic only) | e_k = ⌊16·(λ−λ_min)/(λ_max−λ_min)⌋ | 1 · SCALE | LAURELIN | DEFINITIONAL | **FLAGGED** — deficit: synthetic spectra only — never run on real JWST data |


Calibration: this verdict agrees with the page's stated status (**THEORETICAL**).
