# Engine: Sonification  ω = pitch

**Module:** `modules/sonification/`  
**Version:** 0.111  
**Confidence floor:** ESTABLISHED  
**Notebooks:** [core/08_sonification.ipynb](../notebooks/core/08_sonification.ipynb)  
**Claim:** Every particle and stratum in the tower has a frequency. ω = pitch, exactly and without tuning.

---

## What it computes

Equation-derived audio. ω (angular frequency) = pitch. Radian transform made audible. fractions.Fraction throughout; float only at WAV render boundary. Viewer renders waveform and plays via SonificationPanel. Standalone Ainulindale Synthesizer is a separate repo.

The frequency table is the result. Every tone is ESTABLISHED because every tone is a computation, not a choice: higgs 110.0 Hz, photon 1760.0 Hz, electron 550.0 Hz, Z0 55.0 Hz, gluon 220.0 Hz, d_star 137.5 Hz.

These land on recognisable musical relationships — 110, 220, 440, 880 are octaves of A — because the ratios in the tower are powers of two. That is the CD doubling audible.

The strata: ℝ 110.0, ℂ 275.0, ℍ 330.0, 𝕆 880.0 Hz.

## Results — run 2026-07-28

19/19 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `quasiparticle_rests` | ESTABLISHED | ✓ | {'phonon': 5512, 'exciton': 11025, 'magnon': 8268, 'roton': 16537, 'plasmon': 22050, 'gr… |
| `tone_W_minus` | ESTABLISHED | ✓ | {'omega': 3686.135380212024, 'freq_hz': 586.6666666666666, 'label': 'W_minus'} |
| `tone_W_plus` | ESTABLISHED | ✓ | {'omega': 4146.9023027385265, 'freq_hz': 660.0, 'label': 'W_plus'} |
| `tone_Z0` | ESTABLISHED | ✓ | {'omega': 345.57519189487726, 'freq_hz': 55.0, 'label': 'Z0'} |
| `tone_d_star` | ESTABLISHED | ✓ | {'omega': 863.9379797371931, 'freq_hz': 137.5, 'label': 'd_star'} |
| `tone_electron` | ESTABLISHED | ✓ | {'omega': 3455.7519189487725, 'freq_hz': 550.0, 'label': 'electron'} |
| `tone_gluon_1` | ESTABLISHED | ✓ | {'omega': 1382.300767579509, 'freq_hz': 220.0, 'label': 'gluon_1'} |
| `tone_higgs` | ESTABLISHED | ✓ | {'omega': 691.1503837897545, 'freq_hz': 110.0, 'label': 'higgs'} |
| `tone_phi_attractor` | ESTABLISHED | ✓ | {'omega': 4607.66922526503, 'freq_hz': 733.3333333333334, 'label': 'phi_attractor'} |
| `tone_photon` | ESTABLISHED | ✓ | {'omega': 11058.406140636072, 'freq_hz': 1760.0, 'label': 'photon'} |
| `tone_stratum_C` | ESTABLISHED | ✓ | {'omega': 1727.8759594743863, 'freq_hz': 275.0, 'label': 'stratum_C'} |
| `tone_stratum_H` | ESTABLISHED | ✓ | {'omega': 2073.4511513692632, 'freq_hz': 330.0, 'label': 'stratum_H'} |
| `tone_stratum_O` | ESTABLISHED | ✓ | {'omega': 5529.203070318036, 'freq_hz': 880.0, 'label': 'stratum_O'} |
| `tone_stratum_R` | ESTABLISHED | ✓ | {'omega': 691.1503837897545, 'freq_hz': 110.0, 'label': 'stratum_R'} |
| `wavetable_fano` | ESTABLISHED | ✓ | {'name': 'fano', 'samples': [0.0, 0.05198921484745657, 0.103821958304852, 0.155342545458… |
| `wavetable_higgs_hat` | ESTABLISHED | ✓ | {'name': 'higgs_hat', 'samples': [1.0, 0.9998494055682458, 0.9993976676303487, 0.9986449… |
| `wavetable_phi_recursion` | ESTABLISHED | ✓ | {'name': 'phi_recursion', 'samples': [1.0, -0.3090169943749476, 0.12732200375003455, -0.… |
| `wavetable_rydberg` | ESTABLISHED | ✓ | {'name': 'rydberg', 'samples': [0.0, 0.04002023527729629, 0.07950999640342718, 0.1179550… |
| `wavetable_sine` | ESTABLISHED | ✓ | {'name': 'sine', 'samples': [0.0, 0.012271538285719925, 0.024541228522912288, 0.03680722… |

## Open

- That the mapping is *audible* is established. That it is *meaningful* — that hearing the tower tells you something the numbers do not — is not a claim this module tests.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the zero → audible frequency map (ω = γ/2π) | scale γₙ into the audible band | 1 · SCALE | LAURELIN | DEFINITIONAL | **CLEAN** |


Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).
