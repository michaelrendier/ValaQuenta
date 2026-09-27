# The Emerger (Sedenion Bracketing & Firing Order)

**Module:** `ValaQuenta.modules.emerger`
**Import:** `from ValaQuenta.modules.emerger.tools import EmergerModule`
**Theory page:** [`../emerger.md`](../emerger.md)

---

`emerger` · v0.1 · confidence floor **THEORETICAL**

A dynamic permutative bracketer for Cayley-Dickson algebras. The real component e_0 is the fixed anchor -- the tilt to the i axis -- never bracketed; every imaginary group is paired against it so the bracket-vs-real relationship stays visible. A BRACKETING is an ordered partition of the imaginary indices {1..15}; each group + the anchor spans span({e_0} u G), classified by closure as C / H / O / FRAGMENT (the fragment is where zero divisors live). Five canonical brackets: {1:15} grades the algebra (Re, N, conj, inverse); {2:14} is the pointer plane (e_0, e_8) carrying Omega_ZS; {8:8} is the CD double (J_red/J_blue, the ZD equator, the J_2 L-vs-R asymmetry); {4:4:4:4} is four SU(2) phases and the sigma_RB tilt/axis (Sigma_tilt = net work around the loop, = 0 iff sigma=1/2); {4:8:4} is the gain spectrum 0/1/sqrt2. The FIRING ORDER -- the order groups are approached -- is load-bearing: each bracket is conditioned on the ones before it. It can be canonical (dependency), sigma_RB-phased (Sigma_tilt rotates the entry point into the 12-step precession, 4 d* faces : 3 Lambert-W faces), or any permutation (legality reported, not enforced -- a finding: some sigma_RB phases select a non-dependency-legal order). ZD tests are exact (rank-deficiency of L_x; equator = purely imaginary + norm-balanced across the CD-double boundary). The exact ZD geometry is box_kite's PSL(2,7); G_2 is the continuous blow-up. The Emerger is the ascent-dual of Generational Lineage: descent tracks what built a thing, the Emerger runs what emerges and in what order -- reading, spectroscopy, factoral decomposition.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify`** — THE HONEST CHECKS: 14 exact self-checks + legal firing orders
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify', {})['result']
{'all_pass': True, 'checks': {'Sigma_axis == 0 for e1+e10': True, 'Sigma_axis == 0 for random-ish': True, 'T1 holds (e1+e10)': True, 'e1+e10 is a zero divisor': True, 'e1+e10 on the ZD equator': True, 'e1+e2 is NOT a zero divisor': True, 'e1+e2 NOT on the ZD equator': True, 'e0 is a unit (not ZD)...
```

**`emerge`** — THE READOUT: run x through the 5 brackets in firing order
  params: `x, mode`  ·  confidence: `THEORETICAL`  ·  signature: `(x='e1+e10', mode='sigma_rb')`
```python
>>> module.run('emerge', {})['result']
{'input_norm': 1.4142135623730951, 'firing_order': {'Sigma_tilt': 0.0, 'precession_step_of_12': 6, 'entry_bracket_index': 1, 'canonical': ['{1:15}', '{2:14}', '{8:8}', '{4:4:4:4}', '{4:8:4}'], 'sigma_rb_phased': ['{2:14}', '{8:8}', '{4:4:4:4}', '{4:8:4}', '{1:15}'], 'order': ['{2:14}', '{8:8}', '...
```

**`firing_order`** — THE CLOCK: sigma_RB tilt-phase -> entry bracket in the 12-step precession
  params: `x, mode`  ·  confidence: `THEORETICAL`  ·  signature: `(x='e1+e10', mode='sigma_rb')`
```python
>>> module.run('firing_order', {})['result']
{'Sigma_tilt': 0.0, 'precession_step_of_12': 6, 'entry_bracket_index': 1, 'canonical': ['{1:15}', '{2:14}', '{8:8}', '{4:4:4:4}', '{4:8:4}'], 'sigma_rb_phased': ['{2:14}', '{8:8}', '{4:4:4:4}', '{4:8:4}', '{1:15}'], 'order': ['{2:14}', '{8:8}', '{4:4:4:4}', '{4:8:4}', '{1:15}'], 'phased_is_legal'...
```

**`sigma_rb`** — tilt (Scale / Perfect Perturbation) and axis (Flow); Sigma_axis = 0 identically
  params: `x`  ·  confidence: `THEORETICAL`  ·  signature: `(x='e1+e10')`
```python
>>> module.run('sigma_rb', {})['result']
{'tilt': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'axis': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'Sigma_tilt': 0.0, 'Sigma_axis': 0.0, 'sigma_is_half': True, 'T1_holds': True}
```

**`domain_of`** — CLASSIFY a bracket group: C / H / O / FRAGMENT (by closure)
  params: `indices`  ·  confidence: `ESTABLISHED`  ·  signature: `(indices=(1, 2, 3))`
```python
>>> module.run('domain_of', {})['result']
'H'
```

**`scale_partitions`** — THE PERMUTATION SPACE: partitions of {1..15} into C/H/O-sized groups
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('scale_partitions', {})['result']
{'imaginary_count': 15, 'part_sizes_allowed': [1, 3, 7], 'distinct_shapes': [(7, 7, 1), (7, 3, 3, 1, 1), (7, 3, 1, 1, 1, 1, 1), (7, 1, 1, 1, 1, 1, 1, 1, 1), (3, 3, 3, 3, 3), (3, 3, 3, 3, 1, 1, 1), (3, 3, 3, 1, 1, 1, 1, 1, 1), (3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1), (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,...
```

**`legal_orders`** — THE DEPENDENCY LATTICE: firing orders that respect emergence prerequisites
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('legal_orders', {})['result']
{'legal_orders': [['{1:15}', '{2:14}', '{8:8}', '{4:4:4:4}', '{4:8:4}'], ['{1:15}', '{8:8}', '{2:14}', '{4:4:4:4}', '{4:8:4}'], ['{1:15}', '{8:8}', '{4:4:4:4}', '{2:14}', '{4:8:4}'], ['{1:15}', '{8:8}', '{4:4:4:4}', '{4:8:4}', '{2:14}']], 'count': 4}
```

**`lineage_report`** — ASCENT DUAL: per bracket -- tier, what it descends from, what it emerges
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('lineage_report', {})['result']
[{'bracket': '{1:15}', 'tier': 'DERIVED', 'descends_from': 'the CD grading', 'emerges': 'Re, N=|x|^2, conj, inverse -- grades the algebra'}, {'bracket': '{2:14}', 'tier': 'THEORETICAL', 'descends_from': '{1:15} (needs Re)', 'emerges': 'the pointer z = x0 + i x8; |z|; |z| - Omega_ZS -- read head'}...
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`emerge`, `firing_order`, `emerger_verify`

---

### Running via the registry

```python
from ValaQuenta.modules.emerger.tools import EmergerModule

m = EmergerModule()
m.formulary()                              # list every Equation this module exposes
m.run('verify', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('verify', {}, 'text')     # -> {'text': '...formatted...'}
```
