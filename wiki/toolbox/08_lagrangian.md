# L_NN  Ainulindale Lagrangian

**Module:** `ValaQuenta.modules.lagrangian`
**Import:** `from ValaQuenta.modules.lagrangian.tools import LagrangianModule`
**Theory page:** [`../lagrangian.md`](../lagrangian.md)

---

`lagrangian` · v0.111 · confidence floor **THEORETICAL**

The four-term SMNNIP Lagrangian density L_NN = (2/π)∮[L_kin + L_mat + (1/φ)L_bias + L_coup] r dr dθ. Running coupling α_NN(r) = g²/(4π·ħ_NN·ln(1/r)). RG flow per algebra stratum. Mastery crystallization condition.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`polar_lagrangian`** — Full L_NN — polar integral
  params: `psi_norms, A_comps, beta_norms, algebra, layer`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`L_kinetic`** — L_kin = -1/4 · F_μν^a · F^{μν,a}
  params: `A_comps, g, algebra`  ·  confidence: `ESTABLISHED`  ·  signature: `(A_comps, g, algebra)`

**`L_matter`** — L_mat = i·Ψ̄·γ^μ·D_μ·Ψ
  params: `psi_norms, A_comps, g, hbar_nn, algebra`  ·  confidence: `THEORETICAL`  ·  signature: `(psi_norms, A_comps, g, hbar_nn, algebra)`

**`L_bias`** — L_bias — Mexican hat / Higgs potential
  params: `beta_norms, mu_sq, lam`  ·  confidence: `ESTABLISHED`  ·  signature: `(beta_norms, mu_sq, lam)`

**`L_coupling`** — L_coup = -(1/φ)·Γ_ij·Ψ̄^L·β·Ψ^R  (Yukawa)
  params: `psi_norms, beta_norms, g`  ·  confidence: `THEORETICAL`  ·  signature: `(psi_norms, beta_norms, g)`

**`alpha_nn_running`** — α_NN(r) = g²/(4π·ħ_NN·ln(1/r))  running coupling
  params: `g, hbar_nn, r`  ·  confidence: `THEORETICAL`  ·  signature: `(g, hbar_nn, r)`

**`rg_flow`** — RG flow α_NN(l), ħ_NN(l) — all strata
  params: `alpha_0, hbar_0, algebra, max_layer`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`mastery_check`** — Mastery: vev_distance < ħ_NN/2
  params: `beta_norms, vev, hbar_nn`  ·  confidence: `THEORETICAL`  ·  signature: `(beta_norms, vev, hbar_nn)`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`lagrangian`, `alpha_r`, `rg`

---

### Running via the registry

```python
from ValaQuenta.modules.lagrangian.tools import LagrangianModule

m = LagrangianModule()
m.formulary()                              # list every Equation this module exposes
m.run('polar_lagrangian', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('polar_lagrangian', {}, 'text')     # -> {'text': '...formatted...'}
```
