# H_NN  Berry-Keating Operator

**Module:** `ValaQuenta.modules.berry_keating`
**Import:** `from ValaQuenta.modules.berry_keating.tools import BerryKeatingModule`
**Theory page:** [`../berry_keating.md`](../berry_keating.md)

---

`berry_keating` · v0.111 · confidence floor **OPEN**

H_NN candidate xp operator. d* gap workbench (gap=0.000707). T coordinate map scaffold. Open Problems 2 & 3.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`d_star_gap_report`** — d* gap workbench  [gap = 0.000707  OPEN]
  params: `—`  ·  confidence: `OPEN`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('d_star_gap_report', {})['result']
{'d_star_spec': 0.246, 'd_star_taut': 0.24630720147342253, 'ln_10': 2.302585092994046, 'omega_zs': 0.5671432904097838, 'd_star_x_ln10': 0.5664359328765353, 'gap': 0.000707357533248576, 'gap_taut': 0.0, 'status': 'OPEN — algebraic derivation needed', 'candidate_1_W': 0.452910851609152, 'candidate_...
```

**`gap_candidates`** — Gap candidate expressions — sorted by proximity to Ω
  params: `—`  ·  confidence: `OPEN`  ·  signature: `(d_star: float = 0.246) -> List[Dict[str, Any]]`
```python
>>> module.run('gap_candidates', {})['result']
[{'expression': 'Omega/ln(10)', 'value': 0.24630720147342253, 'x_ln10': 0.5671432904097838, 'gap': 0.0, 'better': True}, {'expression': '1/ln(10^2)', 'value': 0.21714724095162588, 'x_ln10': 0.49999999999999994, 'gap': 0.0671432904097839, 'better': False}, {'expression': '1/(pi+phi)', 'value': 0.2...
```

**`h_nn_eigenvalues`** — H_NN eigenvalues — harmonic oscillator approximation
  params: `hbar_nn, n_max`  ·  confidence: `OPEN`  ·  signature: `(hbar_nn=0.1, n_max=10)`
```python
>>> module.run('h_nn_eigenvalues', {})['result']
{'hbar_nn': 0.1, 'eigenvalues': [0.05, 0.15000000000000002, 0.25, 0.35000000000000003, 0.45, 0.55, 0.65, 0.75, 0.8500000000000001, 0.9500000000000001, 1.05], 'spacings': [0.10000000000000002, 0.09999999999999998, 0.10000000000000003, 0.09999999999999998, 0.10000000000000003, 0.09999999999999998, ...
```

**`xp_spectrum`** — Classical xp torus  x·p = d*·ħ_NN
  params: `hbar_nn`  ·  confidence: `OPEN`  ·  signature: `(hbar_nn=0.1)`
```python
>>> module.run('xp_spectrum', {})['result']
{'x_values': [0.1, 0.2571428571428571, 0.41428571428571426, 0.5714285714285715, 0.7285714285714285, 0.8857142857142857, 1.042857142857143, 1.2, 1.3571428571428572, 1.5142857142857145, 1.6714285714285715, 1.8285714285714287, 1.985714285714286, 2.1428571428571432, 2.3, 2.4571428571428573, 2.6142857...
```

**`T_map`** — T coordinate map at single x  [Open Problem 3]
  params: `x`  ·  confidence: `OPEN`  ·  signature: `(x=1.0)`
```python
>>> module.run('T_map', {})['result']
{'x': 1.0, 'd_star': 0.246, 'ln_x': 0.0, 'phase': 0.0, 'T_re': 1.0, 'T_im': 0.0, 'T_mod': 1.0, 'T_arg': 0.0, 'note': 'Scaffold only — xp T coordinate open; T_transform (interior/exterior) = Eichler-Shimura = Wiles 1995 (RESOLVED)', 'latex': 'T:x\\mapsto x\\,e^{i\\,d^*\\ln x}'}
```

**`T_map_trajectory`** — T map curve  x ∈ [x_min, x_max]
  params: `x_min, x_max`  ·  confidence: `OPEN`  ·  signature: `(x_min=0.1, x_max=10.0)`
```python
>>> module.run('T_map_trajectory', {})['result']
{'trajectory': [{'x': 0.1, 'd_star': 0.246, 'ln_x': -2.3025850929940455, 'phase': -0.5664359328765352, 'T_re': 0.08438189087849014, 'T_im': -0.053662803614520395, 'T_mod': 0.1, 'T_arg': -0.5664359328765352, 'note': 'Scaffold only — xp T coordinate open; T_transform (interior/exterior) = Eichler-S...
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`bk_gap`, `T_map`, `H_nn`

---

### Running via the registry

```python
from ValaQuenta.modules.berry_keating.tools import BerryKeatingModule

m = BerryKeatingModule()
m.formulary()                              # list every Equation this module exposes
m.run('d_star_gap_report', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('d_star_gap_report', {}, 'text')     # -> {'text': '...formatted...'}
```
