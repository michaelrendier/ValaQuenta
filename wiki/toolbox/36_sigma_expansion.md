# Sigma Expansion — J_red/J_blue Balance Curve

**Module:** `ValaQuenta.modules.sigma_expansion`
**Import:** `from ValaQuenta.modules.sigma_expansion.tools import SigmaExpansionModule`
**Theory page:** [`../sigma_expansion.md`](../sigma_expansion.md)

---

`sigma_expansion` · v0.100 · confidence floor **THEORETICAL**

Closed-form Taylor expansion of P_red(sigma)=|J_red|^2/(|J_red|^2+|J_blue|^2) around sigma=1/2. c1, c3 derived (not fitted) from Dirichlet-projection moments. Verified to ~1e-6 near sigma=1/2 against direct computation. Raw |J_red|^2+|J_blue|^2 is NOT constant across sigma -- minimum at 1/2, not a flat quantum-probability-style conservation.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`moments`** — M_n, L_n moments at sigma=1/2 (raw inputs to the derivation)
  params: `text`  ·  confidence: `ESTABLISHED`  ·  signature: `(text='O Captain My Captain')`
```python
>>> module.run('moments', {})['result']
{'M0': 7.595255025289832, 'M1': 13.163215529231053, 'M2': 29.641592954931344, 'M3': 71.61679190871482, 'L_by_channel': {2: ((-0.44091086013182784-7.624197360619537e-16j), (0.373496169476213-1.7052710272580956e-15j), (1.0559962203107724-4.208832663509112e-15j), (3.1288175860422207-1.04327515939044...
```

**`taylor_coefficients`** — c1, c3 — derived (not fitted) Taylor coefficients of P_red(sigma) at 1/2
  params: `text`  ·  confidence: `THEORETICAL`  ·  signature: `(text='O Captain My Captain')`
```python
>>> module.run('taylor_coefficients', {})['result']
{'c1': 0.07545648543103056, 'c3': 0.049215833825092044, 'g0': 1.2953517736776377, 'F1': 0.19548538447713254, 'F2': 1.905274287458193, 'F3': 1.6276136207425198, 'note': 'derived via Taylor expansion, not fitted to data'}
```

**`predict_P_red`** — Cheap closed-form P_red(sigma) prediction (no sigma-sweep needed)
  params: `text, sigma`  ·  confidence: `THEORETICAL`  ·  signature: `(text='O Captain My Captain', sigma=0.6)`
```python
>>> module.run('predict_P_red', {})['result']
0.5075948643769281
```

**`verify_against_actual`** — Error-check: predicted vs. directly-computed P_red(sigma), residuals
  params: `text`  ·  confidence: `ESTABLISHED`  ·  signature: `(text='O Captain My Captain')`
```python
>>> module.run('verify_against_actual', {})['result']
{'coefficients': {'c1': 0.07545648543103056, 'c3': 0.049215833825092044, 'g0': 1.2953517736776377, 'F1': 0.19548538447713254, 'F2': 1.905274287458193, 'F3': 1.6276136207425198, 'note': 'derived via Taylor expansion, not fitted to data'}, 'rows': [{'sigma': 0.04999999999999999, 'd': -0.45, 'predic...
```

---

### Running via the registry

```python
from ValaQuenta.modules.sigma_expansion.tools import SigmaExpansionModule

m = SigmaExpansionModule()
m.formulary()                              # list every Equation this module exposes
m.run('moments', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('moments', {}, 'text')     # -> {'text': '...formatted...'}
```
