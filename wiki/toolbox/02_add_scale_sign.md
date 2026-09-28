# ADD:SCALE:SIGN (the tier-0 datatype)

**Module:** `ValaQuenta.modules.add_scale_sign`
**Import:** `from ValaQuenta.modules.add_scale_sign.tools import AddScaleSignModule`
**Theory page:** [`../add_scale_sign.md`](../add_scale_sign.md)

---

`add_scale_sign` · v0.1 · confidence floor **ESTABLISHED**

A value type for elements of Aff(1,ℝ) = ADD ⋊ (SCALE × SIGN), x ↦ sign·scale·x + add. Compose with @, invert with ~, take residuals (strip one generator, keep the rest), decompose into an ASSWord. Each generator carries its equation part: ADD → a, SCALE → ln s, SIGN → g; the word is u = g·ln s + a and the fold is Γ = tanh(u/2). Read-out on the orthogonal Smith charts (Γ_SCALE, Γ_ADD, parity). Firing order is recorded — the three-phase camshaft SIGN→SCALE→ADD — and its defect (u_total − Σ u_parts) is non-zero exactly when [SCALE, ADD] = ADD bites.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`round_trip`** — THE RETURN PATH: (~T ∘ T)(x) = x, exactly
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(add=3.0, scale=2.5, sign=-1)`
```python
>>> module.run('round_trip', {})['result']
{'element': 'x ↦ -1·2.5·x + 3', 'x': [-2.0, 0.0, 1.0, 7.5], '(~T∘T)(x)': [-2.0, -2.220446049250313e-16, 1.0, 7.500000000000001], 'exact': True}
```

**`equation_parts`** — EACH GENERATOR'S EQUATION PART (ADD→a, SCALE→ln s, SIGN→g)
  params: `add, scale, sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add, scale, sign)`

**`fold`** — THE FOLD: Γ = tanh(u/2), u = g·ln s + a
  params: `add, scale, sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add, scale, sign)`

**`orthogonal_charts`** — THE ORTHOGONAL SMITH CHARTS: Γ_SCALE ⟂ Γ_ADD, parity g
  params: `add, scale, sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add=1.5, scale=4.0, sign=-1)`
```python
>>> module.run('orthogonal_charts', {})['result']
{'Γ_SCALE': 0.6, 'Γ_ADD': 0.6351489523872873, 'parity': -1, 'quadrant': 'NE′', 'u': 0.11370563888010943, 'Γ': 0.05679164448772534, 'at_now': False, 'notation': 'Γ_SCALE = tanh(½·ln 4) = 0.6   Γ_ADD = tanh(½·1.5) = 0.635149   parity -1'}
```

**`camshaft_defect`** — FIRING ORDER: u_total − Σ u_parts (non-zero ⇔ [SCALE,ADD]=ADD)
  params: `add, scale, sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add=4.0, scale=3.0, sign=1)`
```python
>>> module.run('camshaft_defect', {})['result']
{'element': 'x ↦ +1·3·x + 4', 'u_total': 5.09861228866811, 'Σ u_parts': 5.09861228866811, 'firing_defect': 0.0, 'order_matters': False, 'camshaft': ('SIGN', 'SCALE', 'ADD')}
```

**`two_orderings`** — GENERATIONAL LINEAGE: chrono ordering vs zeta ordering
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `(steps=((0.0,8.0,1),(2.0,1.0,1),(0.0,0.5,-1)))`
```python
>>> module.run('two_orderings', {})['result']
{'chrono': 'ASSWord[chrono]:  SCALE(8)  ∘  ADD(2)  ∘  SCALE(0.5)\n  u = -1·ln 4 + -1 = -2.38629    Γ = tanh(u/2) = -0.831552 ...', 'zeta': 'ASSWord[zeta]: ... (same element, ordered by |u_k| descending)', 'same_element': 'x ↦ -1·4·x + -2'}
```

### Reading the Noether direction with this tool (2026-09-28)

`camshaft_defect` is the probe for "does SIGN matter here?" — its `firing_defect`
is `(g−1)·ln s`, so it is zero exactly when SIGN or SCALE is at its identity.
Theory and tables: [`../add_scale_sign.md`](../add_scale_sign.md) § *SIGN and the
direction of the Noether currents*.

```python
>>> for p in ({'add':0.0,'scale':2.0,'sign':-1}, {'add':0.0,'scale':1.0,'sign':-1}, {'add':0.0,'scale':2.0,'sign':1}):
...     r = module.run('camshaft_defect', p)['result']
...     print(p, r['u_total'], r['firing_defect'], r['order_matters'])
{'add': 0.0, 'scale': 2.0, 'sign': -1}  -0.693147  -1.386294  True     # SIGN flipped a real SCALE
{'add': 0.0, 'scale': 1.0, 'sign': -1}   0.0        0.0       False    # SCALE = 1: the flip does nothing
{'add': 0.0, 'scale': 2.0, 'sign':  1}   0.693147   0.0       False    # SIGN = +1: nothing to flip
```

The Noether identity `ln F − ln B = E(1−2σ)` is `ASS(add=0, scale=2E, sign=−1)`
applied to `σ − ½`; evaluate it with the `ASS` object directly
(`ASS(0.0, 2*E, -1)(sigma - 0.5)`). Measured values: scratchpad
`ContextPlease/claude/scratchpad/2026-09-28_sign_noether_direction/`.

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`ass`, `apply`, `compose`, `inv`, `residual`, `word`, `smith`, `camshaft`, `roundtrip`, `defect`

---

### Running via the registry

```python
from ValaQuenta.modules.add_scale_sign.tools import AddScaleSignModule

m = AddScaleSignModule()
m.formulary()                              # list every Equation this module exposes
m.run('round_trip', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('round_trip', {}, 'text')     # -> {'text': '...formatted...'}
```
