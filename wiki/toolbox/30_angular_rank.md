# The 16D Oscilloscope (Angular Rank)

**Module:** `ValaQuenta.modules.angular_rank`
**Import:** `from ValaQuenta.modules.angular_rank.tools import AngularRankModule`
**Theory page:** [`../angular_rank.md`](../angular_rank.md)

---

`angular_rank` · v0.1 · confidence floor **ESTABLISHED**

Measures three things about any signal embedded in the 16 sedenion dimensions, without knowing its language, its meaning, or its author: ANGULAR CONTENT (how much direction survives once the common mode is removed -- a scalar address scores exactly 0, the Phase 23 character encoder 0.0002, the phonetic face 0.402), OCCUPANCY AND RANK (which dimensions are populated, and the numerical rank of the accumulated trace), and NULL OCCUPANCY (how much energy lands in ker(L_a), the four dimensions a zero divisor annihilates). The third is the internal/external provenance test: the internal channel is a functional of its own state and cannot emit into the kernel of its own operator. The first is the language-agnostic stress test. THEY ARE ONE MEASUREMENT. Every entry point takes an immutable content-stamped Datum and refuses a live sequence -- measuring a span that the measured process is concurrently growing is iterate-while-modify, and it does not raise, it drifts until the instrument reports 'all quiet' forever. Mutation is not forbidden; it is DATED, via bearing() between two datums. Two mandatory nulls are built in: the isotropic baseline for null occupancy is exactly nullity/dim = 4/16 = 0.25, so a raw fraction near 0.25 is evidence of NOTHING and only the excess is reportable; and the calibration constants are EMBEDDING-SPECIFIC and do not transfer. Reproduces the published {4,8,4} split (nullity 4, rank 12, singular values sqrt2 x4 / 1 x8 / 0 x4) as a CHECK, not an input, and cross-checks L_a against box_kite's independent multiply().

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify_null_space`** — THE HONEST CHECK: nullity 4, rank 12, {sqrt2 x4, 1 x8, 0 x4}
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify_null_space', {})['result']
{'assessor': (1, 2), 'strut': 3, 'nullity': 4, 'rank': 12, 'singular_counts': {'sqrt2': 4, 'one': 8, 'zero': 4}, 'expected_counts': {'sqrt2': 4, 'one': 8, 'zero': 4}, 'matches_published': True}
```

**`null_occupancy_baseline`** — THE MANDATORY NULL: isotropic energy in ker(L_a) is exactly 4/16
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('null_occupancy_baseline', {})['result']
{'nullity': 4, 'analytic_baseline': 0.25, 'measured_baseline': 0.25096808363015455, 'agreement': True, 'rule': 'report EXCESS over baseline, never the raw fraction'}
```

**`angular_residual`** — ANGULAR CONTENT: sin of the angle to the common direction
  params: `datum`  ·  confidence: `ESTABLISHED`  ·  signature: `(datum)`

**`calibration`** — THE PUBLISHED REFERENCES: 0.0000 / 0.0002 / 0.4020 (Phase 27.2)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('calibration', {})['result']
{'scalar_address': {'angular_residual': 0.0, 'collapse_cos': 1.0, 'note_': 'by construction -- text enters 0_RB as one scalar (Phase 27.1)'}, 'character_encoder': {'angular_residual': 0.0002, 'collapse_cos': 0.9998, 'note_': 'Phase 23 encoder -- collapsed onto the common direction'}, 'phonetic_fa...
```

**`null_occupancy`** — PROVENANCE: energy landing in ker(L_a) -- what the internal channel cannot reach
  params: `datum`  ·  confidence: `THEORETICAL`  ·  signature: `(datum)`

**`external_component`** — Energy of a signal outside a FROZEN internal span
  params: `signal, internal`  ·  confidence: `THEORETICAL`  ·  signature: `(signal, internal)`

**`bearing`** — THE DRIFT METER: how far the span moved between two datums
  params: `before, after`  ·  confidence: `ESTABLISHED`  ·  signature: `(before, after)`

**`numerical_rank`** — Rank of the accumulated trace, with its tolerance
  params: `datum`  ·  confidence: `ESTABLISHED`  ·  signature: `(datum)`

**`occupancy`** — Per-dimension energy fraction and participation ratio
  params: `datum`  ·  confidence: `ESTABLISHED`  ·  signature: `(datum)`

**`embed_log_bands`** — THE LANGUAGE-AGNOSTIC EMBEDDING: 16 log-spaced band energies
  params: `power_spectrum`  ·  confidence: `ESTABLISHED`  ·  signature: `(power_spectrum)`

**`angular_report`** — THE STRESS TEST, one card -- every entry stamped with its datum
  params: `datum`  ·  confidence: `THEORETICAL`  ·  signature: `(datum)`

**`null_space`** — ker(L_a) for an arbitrary sedenion a
  params: `a`  ·  confidence: `ESTABLISHED`  ·  signature: `(a)`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`verify`, `baseline`, `snap`, `ang`, `score`, `calib`, `rank`, `occ`, `spec`, `common`, `ker`, `kerocc`, `ext`, `bear`, `sight`, `angles`, `lmul`, `bands`, `report`

---

### Running via the registry

```python
from ValaQuenta.modules.angular_rank.tools import AngularRankModule

m = AngularRankModule()
m.formulary()                              # list every Equation this module exposes
m.run('verify_null_space', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('verify_null_space', {}, 'text')     # -> {'text': '...formatted...'}
```
