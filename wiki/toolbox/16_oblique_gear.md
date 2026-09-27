# The Oblique Gear Across Scale (Black Hole / Galaxy)

**Module:** `ValaQuenta.modules.oblique_gear`
**Import:** `from ValaQuenta.modules.oblique_gear.tools import ObliqueGearModule`
**Theory page:** *(page pending — see `wiki/00_index.md`)*

---

`oblique_gear` · v0.1 · confidence floor **OPEN**

Tests FourthAgePapers/ChiralityBlackHole's second claim: is the black-hole-scale crank angle theta_crank = arctan(d*) (h_rb_hat's Witches Hat half-angle, ESTABLISHED 2026-06-17) the same fact as the galaxy-scale Stokes-drift rotation curve's own tangent angle at its transition radius r=r_t (galactic_cavity.py, SPARC-confirmed p=0.794), or merely the same constant d* appearing on both sides independently? Computed directly (sympy-verified): REFUTED as stated -- a real ~3.84 degree gap between 13.82 deg (crank) and 17.66 deg (galaxy tangent at r_t), not a rounding artifact. The shared-constant, shared-arctan-family kinship survives; the stronger 'same mechanism' claim, in this specific formulation, does not. Reported honestly per this framework's Chase Every Anomaly rule -- a legal, computed result, not a failure.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`crank_angle_deg`** — Black-hole side: theta_crank = arctan(d*)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('crank_angle_deg', {})['result']
13.820339527010455
```

**`stokes_dimensionless`** — Galaxy side: y(x) = (2/pi)*atan(x), x = r/r_t
  params: `x`  ·  confidence: `ESTABLISHED`  ·  signature: `(x)`

**`stokes_tangent_angle_deg`** — Tangent angle of the galaxy curve at any x = r/r_t
  params: `x`  ·  confidence: `ESTABLISHED`  ·  signature: `(x)`

**`crank_vs_galaxy_tangent_check`** — THE CHECK: does the galaxy tangent angle at r=r_t equal theta_crank?
  params: `—`  ·  confidence: `OPEN`  ·  signature: `()`
```python
>>> module.run('crank_vs_galaxy_tangent_check', {})['result']
{'theta_crank_deg': 13.820339527010455, 'theta_galaxy_at_rt_deg': 17.65678715141286, 'difference_deg': 3.836447624402405, 'matches': False, 'verdict': 'REFUTED AS STATED — real ~3.836 deg gap, not a rounding artifact', 'confidence': 'OPEN:CALCULATED', 'what_survives': 'Both sides independently ke...
```

**`find_matching_radius`** — Where WOULD the tangent angle equal theta_crank?
  params: `—`  ·  confidence: `OPEN`  ·  signature: `()`
```python
>>> module.run('find_matching_radius', {})['result']
{'x_solution': 1.260113190759764, 'r_over_r_t': 1.260113190759764, 'nearest_candidate': 'cbrt(2)', 'nearest_value': 1.2599210498948732, 'gap': 0.00019214086489083293, 'significant': False, 'note': "No candidate matches tighter than d*'s own input precision -- treated as an unremarkable root, not ...
```

**`full_report`** — Everything this module knows, in one call
  params: `—`  ·  confidence: `OPEN`  ·  signature: `()`
```python
>>> module.run('full_report', {})['result']
{'black_hole_side': {'source': 'h_rb_hat/maths.py::oblique_crank()', 'theta_crank_deg': 13.820339527010455, 'd_star': 0.246, 'status': 'ESTABLISHED — 2026-06-17'}, 'galaxy_side': {'source': 'ValaQuenta/galactic_cavity.py::stokes_velocity()', 'form': 'v(r) = v_flat * (2/pi) * atan(r/r_t),  r_t = d...
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`crank`, `stokes`, `tangent`, `check`, `probe`, `report`

---

### Running via the registry

```python
from ValaQuenta.modules.oblique_gear.tools import ObliqueGearModule

m = ObliqueGearModule()
m.formulary()                              # list every Equation this module exposes
m.run('crank_angle_deg', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('crank_angle_deg', {}, 'text')     # -> {'text': '...formatted...'}
```
