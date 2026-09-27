# Spectral Representation of the Primes (Spin / Wobble)

**Module:** `ValaQuenta.modules.spectral_primes`
**Import:** `from ValaQuenta.modules.spectral_primes.tools import SpectralPrimesModule`
**Theory page:** *(page pending — see `wiki/00_index.md`)*

---

`spectral_primes` · v0.1 · confidence floor **OPEN**

The theta(t)-rotation construction (RiemannHypothesisProof/ADDENDUM_toroidal_theta_structure_2026-09-25.md) split into two rotations: spin (the major loop, theta'(t), the smooth non-resonant carrier) and wobble (the minor loop, the fluctuation riding on it). Primes are not an artifact of the wobble -- they are its genuine classical spectral content (Riemann/von Mangoldt/Weil), demonstrated here by reconstructing psi(x)'s prime-power jumps from the same zero set that gives a strictly monotonic, non-resonant spin. A separate claim -- that the real-axis tilt (Omega proportional to sin(tilt), the oblique-gearing secondary rotation) IS the wobble by minimum-information identification -- is REFUTED AS TESTED: direct correlation is ~0.037, essentially zero, with a named methodological gap (pointwise vs interval sampling) left open, not smoothed over. Finally: the crossing of the Real Tilt (the trajectory's own instantaneous position) and the Axis (the central t-axis, Re=Im=0) is an isolated, simple, transversal zero -- pinned at sigma=0.500000 to machine precision at every zero tested, moving up the t-axis but never sideways in sigma.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`spin_is_monotonic`** — SPIN: theta'(t), the major loop — non-resonant
  params: `n_zeros`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_zeros=60)`
```python
>>> module.run('spin_is_monotonic', {})['result']
{'n_steps': 59, 'n_non_monotonic': 0, 'monotonic': True, 'range': (0.40527437216202367, 1.6280299759886958), 'confidence': 'ESTABLISHED'}
```

**`wobble_carries_primes_demo`** — WOBBLE: the minor loop carries the primes (psi(x) reconstruction)
  params: `n_zeros`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_zeros=60)`
```python
>>> module.run('wobble_carries_primes_demo', {})['result']
{'n_zeros_used': 60, 'rows': [{'x': 2, 'psi_exact': 0.6931471805599453, 'psi_reconstructed': 0.3539732829093463, 'difference': -0.33917389765059897, 'at_prime_power': True}, {'x': 2.5, 'psi_exact': 0.6931471805599453, 'psi_reconstructed': 0.7033591872336061, 'difference': 0.010212006673660845, 'a...
```

**`tilt_vs_wobble_correlation`** — TILT vs WOBBLE — REFUTED AS TESTED
  params: `n_zeros`  ·  confidence: `OPEN`  ·  signature: `(n_zeros=60)`
```python
>>> module.run('tilt_vs_wobble_correlation', {})['result']
{'n': 59, 'correlation': 0.03670287862731935, 'refuted': True, 'confidence': 'OPEN', 'verdict': 'REFUTED AS TESTED — correlation ~0, the naive pointwise-vs-interval comparison does not show tilt=wobble', 'known_gap': 'tilt is sampled POINTWISE at each zero; wobble is an INTERVAL quantity between ...
```

**`crossing_does_not_drift`** — THE CROSSING: isolated, simple, pinned at sigma=1/2
  params: `n_zeros, n_test`  ·  confidence: `ESTABLISHED (for zeros tested)`  ·  signature: `(n_zeros=60, n_test=5)`
```python
>>> module.run('crossing_does_not_drift', {})['result']
{'rows': [{'gamma': 14.134725141734695, 'crossing_sigma': 0.5, 'min_abs_value': 6.207072341948442e-31, 'pinned_at_half': True}, {'gamma': 21.022039638771556, 'crossing_sigma': 0.5, 'min_abs_value': 4.331483172259611e-31, 'pinned_at_half': True}, {'gamma': 25.01085758014569, 'crossing_sigma': 0.5,...
```

**`full_report`** — Everything this module knows, in one call
  params: `n_zeros`  ·  confidence: `OPEN`  ·  signature: `(n_zeros=60)`
```python
>>> module.run('full_report', {})['result']
{'n_zeros': 60, 'spin': {'n_steps': 59, 'n_non_monotonic': 0, 'monotonic': True, 'range': (0.40527437216202367, 1.6280299759886958), 'confidence': 'ESTABLISHED'}, 'wobble_carries_primes': {'n_zeros_used': 60, 'rows': [{'x': 2, 'psi_exact': 0.6931471805599453, 'psi_reconstructed': 0.35397328290934...
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`spin`, `wobble`, `tilt`, `crossing`, `report`

---

### Running via the registry

```python
from ValaQuenta.modules.spectral_primes.tools import SpectralPrimesModule

m = SpectralPrimesModule()
m.formulary()                              # list every Equation this module exposes
m.run('spin_is_monotonic', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('spin_is_monotonic', {}, 'text')     # -> {'text': '...formatted...'}
```
