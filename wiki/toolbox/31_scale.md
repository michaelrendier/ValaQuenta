# The Scale (Decompositional Analysis, Forwards and Backwards)

**Module:** `ValaQuenta.modules.scale`
**Import:** `from ValaQuenta.modules.scale.tools import ScaleModule`
**Theory page:** [`../scale.md`](../scale.md)

---

`scale` · v0.1 · confidence floor **ESTABLISHED**

SCALE is tier-0 (ADD, SCALE, SIGN) -- this module pulls it out of a quantity and names what is left over, both directions. polar_decompose/recompose is the exact forward/backward pair for ONE point (r=scale, theta=scale-blind under self-rescaling, verified round-trip). The two-ring Mobius fold (mobius_fold/scale_factor) has its OWN scale-blind object, a different and harder question: the raw angle does NOT survive the fold (a rejected candidate, kept in the record), but the cross-ratio of any four points is exactly invariant under every choice of anchor -- verified directly, not asserted. pathway_decompose applies the same forward/backward discipline to a real algorithm (RSA CRT-decrypt as the control case), representing genuine dependency fan-out rather than forcing a linear chain.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`polar_round_trip`** — THE RETURN PATH: recompose(*decompose(Z)) == Z, exactly
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('polar_round_trip', {})['result']
{'n_samples': 5, 'max_round_trip_error': 1.1641532182693481e-10, 'holds': True}
```

**`scale_invariance_under_self_rescale`** — theta is unchanged as Z is rescaled by any positive real
  params: `Z`  ·  confidence: `ESTABLISHED`  ·  signature: `(Z)`

**`scale_factor`** — THE FLATTENING ARTIFACT: |dGamma/dZ|, exact
  params: `Z, Z0`  ·  confidence: `ESTABLISHED`  ·  signature: `(Z, Z0)`

**`verify_no_caustic`** — NO TRUE CAUSTIC: the fold's derivative never vanishes, only diverges at one pole
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify_no_caustic', {})['result']
{'test_points': ['(0.001+0j)', '(100+0j)', '(1+50j)', '(-50+0.1j)', '(1000000+1j)'], 'scale_factors': [1.9960059920099886, 0.00019605920988138416, 0.0007987220447284345, 0.0008329827864107189, 1.999996000004e-12], 'any_zero': False, 'holds': True}
```

**`cross_ratio_is_scale_blind`** — THE SCALE INVARIANT: cross-ratio survives every anchor; the angle does not
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('cross_ratio_is_scale_blind', {})['result']
{'cross_ratio_before': (-0.4888595912986158-0.6375741595253791j), 'cross_ratio_after_each_anchor': [(-0.48885959129861584-0.6375741595253792j), (-0.4888595912986156-0.6375741595253793j), (-0.4888595912986152-0.6375741595253785j), (-0.48885959129860845-0.637574159525401j)], 'anchors': [(1+0j), (0....
```

**`two_ring_point`** — THE TWO-RING INSTRUMENT: any pair of readings, folded
  params: `ring1, ring2, Z0`  ·  confidence: `ESTABLISHED`  ·  signature: `(ring1, ring2, Z0)`

**`fold_unfold_round_trip`** — THE MASTER IDENTITY: Gamma=tanh(log(Z/Z0)/2), exact, any complex Z
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('fold_unfold_round_trip', {})['result']
{'n_samples': 4, 'max_round_trip_error': 2.5736952517654053e-13, 'holds': True}
```

**`locally_square`** — AUTOMATIC, NOT CONDITIONAL: any two rings give locally-square cells
  params: `Z, Z0`  ·  confidence: `ESTABLISHED`  ·  signature: `(Z, Z0)`

**`custom_ring_chart_demo`** — USER-DEFINED RINGS: any two functions of any object, folded
  params: `obj, ring1_fn, ring2_fn, Z0`  ·  confidence: `ESTABLISHED`  ·  signature: `(obj, ring1_fn, ring2_fn, Z0)`

**`rsa_pathway_control`** — PROCESS DECOMPOSITION CONTROL CASE: RSA CRT-decrypt, a genuine fan-out
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('rsa_pathway_control', {})['result']
{'real': 65, 'imaginary': (('m1', 4), ('m2', 12), ('h', 1)), 'dim': 4, 'order': ['m1', 'm2', 'h', 'm_out'], 'all': {'input': 2790, 'm1': 4, 'm2': 12, 'h': 1, 'm_out': 65}}
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`polar`, `unpolar`, `roundtrip`, `fold`, `sf`, `nocaustic`, `cr`, `crblind`, `tworing`, `custom`, `fold_log`, `unfold_exp`, `roundtrip2`, `square`, `rsapath`

---

### Running via the registry

```python
from ValaQuenta.modules.scale.tools import ScaleModule

m = ScaleModule()
m.formulary()                              # list every Equation this module exposes
m.run('polar_round_trip', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('polar_round_trip', {}, 'text')     # -> {'text': '...formatted...'}
```
