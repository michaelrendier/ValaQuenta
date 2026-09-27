# L_(I|O) Photon Path Engine (GR)

**Module:** `ValaQuenta.modules.l_io_photon_path`
**Import:** `from ValaQuenta.modules.l_io_photon_path.tools import LIOPhotonPathModule`
**Theory page:** [`../l_io_photon_path.md`](../l_io_photon_path.md)

---

`l_io_photon_path` · v0.2 · confidence floor **THEORETICAL**

GR version of L_(I|O): Kaiser-Squires shear->convergence, Poisson solve for the lensing potential, deflection field, and the lens equation beta=theta-alpha(theta). The difference between the clean (undeflected) path theta and the actual (bent) source position beta is the real, measured L_(I|O) deviation. L_(I|O)-L is identified with -psi(theta), the Fermat potential -- established GR, not a new operator. Requires real shear input; no synthetic fallback.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`bounded_lensing_pipeline`** — Full pipeline w/ non-periodic boundary handler
  params: `gamma1, gamma2, pixel_scale_arcsec, taper_frac, pad_factor`  ·  confidence: `THEORETICAL`  ·  signature: `(gamma1, gamma2, pixel_scale_arcsec, taper_frac=0.1, pad_factor=2.0)`

**`kaiser_squires_kappa`** — Kaiser-Squires: shear -> convergence
  params: `gamma1, gamma2`  ·  confidence: `ESTABLISHED`  ·  signature: `(gamma1, gamma2)`

**`lensing_potential`** — Poisson solve: convergence -> lensing potential
  params: `kappa`  ·  confidence: `ESTABLISHED`  ·  signature: `(kappa)`

**`deflection_field`** — alpha = grad(psi)  -- the actual bending
  params: `psi, pixel_scale_arcsec`  ·  confidence: `ESTABLISHED`  ·  signature: `(psi, pixel_scale_arcsec)`

**`trace_photon`** — Lens equation: beta = theta - alpha(theta)
  params: `theta1, theta2, alpha1, alpha2`  ·  confidence: `ESTABLISHED`  ·  signature: `(theta1, theta2, alpha1, alpha2)`

**`l_io_deficit`** — L_(I|O) - L := -psi(theta)  [wiki/52 target #1, formalized]
  params: `psi`  ·  confidence: `THEORETICAL`  ·  signature: `(psi)`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`ks_kappa`, `psi`, `alpha`, `trace`, `l_io_stats`

---

### Running via the registry

```python
from ValaQuenta.modules.l_io_photon_path.tools import LIOPhotonPathModule

m = LIOPhotonPathModule()
m.formulary()                              # list every Equation this module exposes
m.run('bounded_lensing_pipeline', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('bounded_lensing_pipeline', {}, 'text')     # -> {'text': '...formatted...'}
```
