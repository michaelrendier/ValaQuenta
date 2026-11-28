# ADD:SCALE:SIGN (the tier-0 datatype)

**Module:** `ValaQuenta.modules.add_scale_sign`
**Import:** `from ValaQuenta.modules.add_scale_sign.tools import AddScaleSignModule`
**Theory page:** [add_scale_sign.md](../add_scale_sign.md)

---

`add_scale_sign` · v0.3 · confidence floor **ESTABLISHED**

A value type for elements of Aff(1,ℝ) = ADD ⋊ (SCALE × SIGN), x ↦ sign·scale·x + add. Compose with @, invert with ~, take residuals (strip one generator, keep the rest), decompose into an ASSWord. Each generator carries its equation part: ADD → a, SCALE → ln s, SIGN → g; the word is u = g·ln s + a and the fold is Γ = tanh(u/2). Read-out on the orthogonal Smith charts (Γ_SCALE, Γ_ADD, parity). Firing order is recorded — the three-phase camshaft SIGN→SCALE→ADD — and its defect (u_total − Σ u_parts) is non-zero exactly when [SCALE, ADD] = ADD bites. No sedenion here; order matters at THIS tier.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`group_laws_exact`** — THE GROUP LAWS, EXACT:  associativity, identity, inverse, [SCALE, SIGN] = 1, [ADD, ·] a translation
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> 'Dict[str, Any]'`
```python
>>> module.run('group_laws_exact', {})['result']
{'elements': 18, 'triples': 5832, 'associative': True, 'identity': True, 'inverse': True, 'sign_scale_commute': True, 'commutator_add_scale_is_translation': True, 'commut ...
```

**`round_trip`** — THE RETURN PATH: (~T ∘ T)(x) = x, exactly
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `(add=3.0, scale=2.5, sign=-1) -> Dict[str, Any]`
```python
>>> module.run('round_trip', {})['result']
{'element': 'x ↦ -1·2.5·x + 3', 'x': [-2.0, 0.0, 1.0, 7.5], '(~T∘T)(x)': [-2.0, -2.220446049250313e-16, 1.0, 7.500000000000001], 'exact': True}
```

**`equation_parts`** — EACH GENERATOR'S EQUATION PART  (ADD→a, SCALE→ln s, SIGN→g)
  params: `add`, `scale`, `sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add, scale, sign)`
```python
>>> module.run('equation_parts', {...})['result']      # needs its arguments: AddScaleSignModule.formulary.<locals>.<lambda>() missing 3 required positional arguments: 'add', 'scale', and 'sign'
```

**`fold`** — THE FOLD:  Γ = tanh(u/2),  u = g·ln s + a
  params: `add`, `scale`, `sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add, scale, sign)`
```python
>>> module.run('fold', {...})['result']      # needs its arguments: AddScaleSignModule.formulary.<locals>.<lambda>() missing 3 required positional arguments: 'add', 'scale', and 'sign'
```

**`orthogonal_charts`** — THE ORTHOGONAL SMITH CHARTS:  Γ_SCALE ⟂ Γ_ADD, parity g
  params: `add`, `scale`, `sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add=1.5, scale=4.0, sign=-1) -> Dict[str, Any]`
```python
>>> module.run('orthogonal_charts', {})['result']
{'Γ_SCALE': 0.6, 'Γ_ADD': 0.6351489523872873, 'parity': -1, 'quadrant': 'NE′', 'u': 0.11370563888010943, 'Γ': 0.05679164448772534, 'at_now': False, 'notation': 'Γ_SCALE = ...
```

**`camshaft_defect`** — FIRING ORDER:  u_total − Σ u_parts  (non-zero ⇔ [SCALE,ADD]=ADD)
  params: `add`, `scale`, `sign`  ·  confidence: `ESTABLISHED`  ·  signature: `(add=4.0, scale=3.0, sign=1) -> Dict[str, Any]`
```python
>>> module.run('camshaft_defect', {})['result']
{'element': 'x ↦ +1·3·x + 4', 'u_total': 5.09861228866811, 'Σ u_parts': 5.09861228866811, 'firing_defect': 0.0, 'order_matters': False, 'camshaft': ('SIGN', 'SCALE', 'ADD ...
```

**`two_orderings`** — GENERATIONAL LINEAGE:  chrono ordering  vs  zeta ordering
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `(steps=((0.0, 8.0, 1), (2.0, 1.0, 1), (0.0, 0.5, -1))) -> Dict[str, Any]`
```python
>>> module.run('two_orderings', {})['result']
{'chrono': 'ASSWord[chrono]:  SCALE(8)  ∘  ADD(2)  ∘  SCALE(0.5)\n  u = -1·ln 4 + -1 = -2.38629    Γ = tanh(u/2) = -0.831552    [firing defect -2.77: SIGN flipped a non-t ...
```

### Shell commands

`ass` · `apply` · `compose` · `inv` · `residual` · `word` · `smith` · `camshaft` · `roundtrip` · `defect`


---

*Theory page: [`add_scale_sign.md`](../add_scale_sign.md).*
