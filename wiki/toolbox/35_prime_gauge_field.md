# The Prime Gauge Field

**Module:** `ValaQuenta.modules.prime_gauge_field`
**Import:** `from ValaQuenta.modules.prime_gauge_field.tools import PrimeGaugeFieldModule`
**Theory page:** [`../prime_gauge_field.md`](../prime_gauge_field.md)

---

`prime_gauge_field` · v0.1 · confidence floor **THEORETICAL**

The Weyl-shaped local-scale connection the earlier Schwarzian-derivative check did not test. Gamma(s)=(s-1)/(s+1) (the SCALE engine's own conformal map) read two ways: as a gradient (A=grad(log|Gamma|), provably flat for ANY holomorphic scalar, Poincare lemma -- confirms the earlier flat-Schwarzian result was never special to Gamma) and as a genuine connection (A=(Re Gamma, Im Gamma), NOT a gradient -- this one carries real curvature, closed form F(s)=2*Im(dGamma/ds), verified against a finite-difference derivative). The pre-registered prediction (FastInverse/README.md) was that the flat locus is the construction's trivial/vacuum point; found instead: F=0 exactly on the real axis (Gamma real-valued -- a defensible 'trivial phase' reading, partial match) AND on sigma=-1 (Gamma's own pole line -- not predicted, reported honestly as a new feature, not folded into the prediction after the fact).

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify`** — THE HONEST CHECKS: closed form vs numeric, flatness, the prediction
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify', {})['result']
{'ok': True, 'n_checked': 200, 'closed_form_vs_numeric_max_err': 4.2800429866929335e-11, 'log_potential_curvature_max': 5.551115123125783e-12, 'zero_locus_prediction_all_match': True, 'zero_locus_n_mismatches': 0}
```

**`report`** — ONE POINT, FULL READOUT: Gamma, connection, both curvatures
  params: `s`  ·  confidence: `THEORETICAL`  ·  signature: `(s='0.5+0.1j')`
```python
>>> module.run('report', {})['result']
{'s': (0.5+0.1j), 'Gamma': (-0.3274336283185841+0.08849557522123894j), '|Gamma|': 0.3391817326856071, 'connection': (-0.3274336283185841, 0.08849557522123894), 'curvature': -0.23494400501213872, 'log_potential_curvature': 0.0, 'zero_locus': {'s': (0.5+0.1j), 'on_real_axis': False, 'on_pole_line':...
```

**`curvature`** — F(s) = curl of the connection A=(Re Gamma, Im Gamma) -- NOT flat
  params: `s`  ·  confidence: `THEORETICAL`  ·  signature: `(s='0.5+0.1j')`
```python
>>> module.run('curvature', {})['result']
{'s': (0.5+0.1j), 'curvature': -0.23494400501213872, 'curvature_numeric': -0.2349440050113116}
```

**`log_potential_curvature`** — THE FLAT READING: A = grad(log|Gamma|), curl always zero
  params: `s`  ·  confidence: `ESTABLISHED`  ·  signature: `(s='0.5+0.1j')`
```python
>>> module.run('log_potential_curvature', {})['result']
{'s': (0.5+0.1j), 'log_potential_curvature': 0.0}
```

**`prediction_check`** — THE PRE-REGISTERED PREDICTION, checked over a random sample
  params: `n_samples`  ·  confidence: `THEORETICAL`  ·  signature: `(n_samples=2000)`
```python
>>> module.run('prediction_check', {})['result']
{'n_samples': 2000, 'n_mismatches': 0, 'all_match': True, 'mismatches': []}
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`gauge_report`, `gauge_curvature`, `gauge_verify`

---

### Running via the registry

```python
from ValaQuenta.modules.prime_gauge_field.tools import PrimeGaugeFieldModule

m = PrimeGaugeFieldModule()
m.formulary()                              # list every Equation this module exposes
m.run('verify', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('verify', {}, 'text')     # -> {'text': '...formatted...'}
```
