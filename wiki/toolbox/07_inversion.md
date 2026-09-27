# Inside-Out Inversion Engine  (I|O)

**Module:** `ValaQuenta.modules.inversion`
**Import:** `from ValaQuenta.modules.inversion.tools import InversionModule`
**Theory page:** [`../inversion.md`](../inversion.md)

---

`inversion` · v0.111 · confidence floor **ESTABLISHED**

The (I|O) inversion map J_N: (r, theta) -> (1/r, theta + pi/2). The 2-stroke engine of the SMNNIP framework: compression stroke (r -> 1/r) and expansion stroke (1/r -> r). Unifies Schwarzschild, Hawking, Dirac sea, and Ptolemy inversion as the same map at different recursion depths. Fixed point r=1 is the horizon. Recursion attractor is phi. The sedenion is where the expansion stroke fails: top dead center, one-way ratchet.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`inversion_map`** — (I|O) Inversion Map J_N
  params: `r, theta_rad`  ·  confidence: `ESTABLISHED`  ·  signature: `(r, theta_rad)`

**`derive_horizon_rotation`** — Horizon rotation pi/2, derived not assumed
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('derive_horizon_rotation', {})['result']
{'pi_basel': 3.141587878949809, 'full_turn_derived': 6.283175757899618, 'n_division_algebras': 4, 'phi_derived': 1.5707939394749044, 'phi_assumed': 1.5707963267948966, 'residual': 2.387319992136483e-06, 'matches': True, 'confidence': 'ESTABLISHED', 'note': "phi = (Basel-derived 2*pi) / (Hurwitz-f...
```

**`involution_check`** — (I|O) Involution: J_N applied twice
  params: `r, theta_rad`  ·  confidence: `ESTABLISHED`  ·  signature: `(r, theta_rad)`

**`gradient_flow`** — Gradient flow: r=1 to phi attractor
  params: `r0, max_steps`  ·  confidence: `ESTABLISHED`  ·  signature: `(r0, max_steps=1000)`

**`phi_crossing_step`** — phi-crossing step = H/4 = (pi/2) hbar_NN
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('phi_crossing_step', {})['result']
{'H_NN_over_4': 0.025, 'pi_over_2_times_hbar': 0.024999999999999998, 'match': True, 'status': 'ESTABLISHED numerically — formal derivation OPEN'}
```

**`d_star_gap`** — d* x ln(10) vs OMEGA_ZS  [OPEN — gap = 0.00070]
  params: `—`  ·  confidence: `OPEN`  ·  signature: `()`
```python
>>> module.run('d_star_gap', {})['result']
{'d_star': 0.246, 'd_star_x_ln10': 0.5664359328765353, 'OMEGA_ZS': 0.5671432904097838, 'gap': 0.000707357533248576, 'status': 'OPEN — highest priority derivation'}
```

**`four_horizons`** — (I|O) unifies four physical horizons
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('four_horizons', {})['result']
[{'name': 'Schwarzschild horizon', 'mechanism': 'r < r_s: (t,r) coordinates exchange roles', 'coordinate_shift': '(t,r) -> (r,t)', 'preservation': 'Spacetime interval', 'status': 'ESTABLISHED'}, {'name': 'Hawking pair production', 'mechanism': 'Conjugate pair (r_N, 1/r_N) at horizon', 'coordinate...
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`io`, `flow`, `phi_step`, `gap`, `observer`, `horizons`

---

### Running via the registry

```python
from ValaQuenta.modules.inversion.tools import InversionModule

m = InversionModule()
m.formulary()                              # list every Equation this module exposes
m.run('inversion_map', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('inversion_map', {}, 'text')     # -> {'text': '...formatted...'}
```
