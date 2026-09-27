# Tier 8 — D-CS: Sedenion Self-Organisation Paper

**Module:** `ValaQuenta.modules.tier8_sedenion`
**Import:** `from ValaQuenta.modules.tier8_sedenion.tools import Tier8SedenionModule`
**Theory page:** [`../tier8_sedenion.md`](../tier8_sedenion.md)

---

`tier8_sedenion` · v0.100 · confidence floor **THEORETICAL**

D-CS first paper: sedenion engine as zero-free-parameter prime-hash architecture. 5 engines: self-organisation (16 ops → d*/σ½/D*=1), gnarl validation, OMEGA_ZS 6-family, Hermite timing wheel, orbit trap Hyperwebster address.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`full_sedenion`** — Tier 8 — all 5 D-CS engines
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`

**`sedenion_self_organisation`** — 16 operator names → d*/σ½/D*=1 via prime hash. Zero free parameters.
  params: `—`  ·  confidence: `ESTABLISHED+THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('sedenion_self_organisation', {})['result']
{'claim': '16 SMMIP operators self-organise to d*/σ½/D*=1 via prime hash. Zero free parameters.', 'operators': [{'e_k': 0, 'name': 'IDENTITY', 'hash': 8697, 'sigma': 8.7e-06, 'dim_idx': 9, 'at_brim': False}, {'e_k': 1, 'name': 'EXPANSION', 'hash': 10930, 'sigma': 1.093e-05, 'dim_idx': 2, 'at_brim...
```

**`gnarl_validation`** — Gnarl = sedenion zero-divisor boundary. Mean g = OMEGA_ZS.
  params: `—`  ·  confidence: `ESTABLISHED+THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('gnarl_validation', {})['result']
{'claim': 'Gnarl = zero-divisor boundary in 𝕊. Mean g = OMEGA_ZS. Fractal at dim 14+d*.', 'g_statistics': {'N': 500, 'mean': 1.153725, 'std': 0.0504, 'min': 1.045139, 'max': 1.312101, 'OMEGA_ZS': 0.567143, 'g_vs_OMEGA_ZS': 0.586582}, 'octonion_subspace': {'mean_g': 1.0, 'expected': 1.0, 'g_is_1':...
```

**`omega_zs_6_family`** — OMEGA_ZS = W(1) appears in 6 independent domains simultaneously.
  params: `—`  ·  confidence: `ESTABLISHED+THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('omega_zs_6_family', {})['result']
{'claim': 'OMEGA_ZS = W(1) appears in 6 independent domains simultaneously. It is the σ=½ signature.', 'lambert_w': {'W_1': 0.5671432904, 'verified': True, 'self_ref': True, 'self_ref_eq': 'OMEGA_ZS = e^{-OMEGA_ZS}'}, 'six_family': [{'domain': 'Mathematics (Lambert W)', 'constant': 'W(1) = Ω', 'v...
```

**`hermite_timing_wheel`** — H_n has n zeros = n BAO timing marks. Riemann zeros = BK levels.
  params: `—`  ·  confidence: `ESTABLISHED+THEORETICAL`  ·  signature: `() -> Dict[str, Any]`

**`orbit_trap_address`** — Mandelbrot orbit trap = Hyperwebster sedenion address. c=-3/4 ↔ σ=½.
  params: `—`  ·  confidence: `ESTABLISHED+THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('orbit_trap_address', {})['result']
{'claim': 'Orbit trap = Hyperwebster address. Mandelbrot boundary = gnarl. c=-¾ ↔ σ=½.', 'critical_strip': {'c_sigma_half': -0.75, 'boundary_count': 2, 'total_points': 50, 'fraction_on_boundary': 0.04, 'sample': [{'Im_c': -1.5, 'n_iter': 2, 'smooth': 1.5663, 'on_boundary': False}, {'Im_c': -0.888...
```

**`leech_divergence_inversion`** — Zero-divisors are divergence-inverted sources. φ_ZD = V₂₄ - V₁₆.
  params: `—`  ·  confidence: `ESTABLISHED+THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('leech_divergence_inversion', {})['result']
{'claim': 'Zero-divisors are divergence-inverted sources, not permanent sinks. φ_ZD = V_24 - V_16 = π¹²/12! - π⁸/8! is the phase gate at each ZD firing.', 'ball_volumes': [{'n': 0, 'algebra': 'point', 'V_n': 1.0, 'ratio_V_n_over_V_n2': None, 'ratio_formula': None}, {'n': 2, 'algebra': 'ℂ (U1)', '...
```

**`causality_lattice_packing`** — Causal/total = 23/4095. Golay d=8 = octonion dim = time.
  params: `—`  ·  confidence: `ESTABLISHED+THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('causality_lattice_packing', {})['result']
{'claim': 'Lattice packing (Leech) = atemporal phase space. Causality = H_BK trajectory through 23/4095 of it. Golay d=8 = octonion dim = time. Turbulence = acausal excursion of amplitude phi_ZD.', 'golay_code': {'code': '[24, 12, 8]', 'n': 24, 'k': 12, 'd': 8, 'codewords': 4096, 'non_zero_codewo...
```

---

### Running via the registry

```python
from ValaQuenta.modules.tier8_sedenion.tools import Tier8SedenionModule

m = Tier8SedenionModule()
m.formulary()                              # list every Equation this module exposes
m.run('full_sedenion', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('full_sedenion', {}, 'text')     # -> {'text': '...formatted...'}
```
