# J_info  Information Current

**Module:** `ValaQuenta.modules.noether_information`
**Import:** `from ValaQuenta.modules.noether_information.tools import NoetherInformationModule`
**Theory page:** [`../noether_information.md`](../noether_information.md)

---

`noether_information` · v0.111 · confidence floor **CONJECTURE**

Noether current for information-translation symmetry of L_NN. I_information = Shannon entropy of activation distribution. Phi_flux = information flux through algebra boundary. t_e = entropic time (layer where I_info is maximal). Entropic arrow: ∂_l I_info ≥ 0.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`information_current`** — J_info^μ — information Noether current
  params: `psi_norms, algebra, layer, total_layers`  ·  confidence: `CONJECTURE`  ·  signature: `None`

**`entropic_arrow`** — Entropic arrow: ∂_l I_info ≥ 0
  params: `n_steps, algebra`  ·  confidence: `CONJECTURE`  ·  signature: `None`

**`delta_J_info`** — ΔJ_info — cycle-averaged information current violation
  params: `psi_norms, algebra, layer`  ·  confidence: `CONJECTURE`  ·  signature: `None`

**`information_capacity`** — C_max = n_neurons × log₂(dim_algebra) bits
  params: `algebra, n_neurons`  ·  confidence: `THEORETICAL`  ·  signature: `(algebra, n_neurons)`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`J_info`, `I_info`, `capacity`

---

### Running via the registry

```python
from ValaQuenta.modules.noether_information.tools import NoetherInformationModule

m = NoetherInformationModule()
m.formulary()                              # list every Equation this module exposes
m.run('information_current', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('information_current', {}, 'text')     # -> {'text': '...formatted...'}
```
