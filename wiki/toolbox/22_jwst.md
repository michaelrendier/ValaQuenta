# JWST  Spectral Pixel  →  𝕆

**Module:** `ValaQuenta.modules.jwst`
**Import:** `from ValaQuenta.modules.jwst.tools import JWSTModule`
**Theory page:** [`../jwst.md`](../jwst.md)

---

`jwst` · v0.111 · confidence floor **THEORETICAL**

JWST NIRCam spectral pixel module. 8 filter intensities (900–4440nm) → 8 octonion components. Cayley-Dickson addressing: λ → r ∈ (0,1). One 𝕆 element per sky pixel.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`spectral_to_octonion`** — 8 NIRCam filters → 𝕆 element
  params: `intensities`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`cd_spectral_address`** — Cayley-Dickson spectral pixel address
  params: `intensities, pixel_x, pixel_y`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`synthetic_hydrogen`** — Synthetic Paschen series spectrum (hydrogen)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('synthetic_hydrogen', {})['result']
{'type': 'hydrogen', 'intensities': [4.772217220174583e-11, 1.9638082208988035e-06, 0.002186124363389384, 1.782133109475818e-11, 1.50270702025214e-34, 1.3269944892818981e-71, 9.93247572170379e-105, 7.790086752643799e-129], 'filters': ['F090W', 'F115W', 'F150W', 'F200W', 'F277W', 'F356W', 'F410M',...
```

**`synthetic_stellar`** — Synthetic blackbody T=5000K spectrum
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('synthetic_stellar', {})['result']
{'type': 'stellar', 'intensities': [1.0, 0.6150018599635491, 0.31446535401390957, 0.13488742972730966, 0.046627019492301594, 0.019520289192429777, 0.01178102739106557, 0.008826258640069248], 'filters': ['F090W', 'F115W', 'F150W', 'F200W', 'F277W', 'F356W', 'F410M', 'F444W'], 'wavelengths': [900.0...
```

**`lambda_to_r`** — λ (nm) → r ∈ (0,1)  radial coordinate
  params: `wavelength_nm`  ·  confidence: `ESTABLISHED`  ·  signature: `(wavelength_nm=2000.0)`
```python
>>> module.run('lambda_to_r', {})['result']
{'wavelength_nm': 2000.0, 'r': 0.31073446327674836, 'lambda_back': 1999.9999999996892}
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`jwst_oct`, `jwst_H`, `jwst_star`, `lambda_r`

---

### Running via the registry

```python
from ValaQuenta.modules.jwst.tools import JWSTModule

m = JWSTModule()
m.formulary()                              # list every Equation this module exposes
m.run('spectral_to_octonion', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('spectral_to_octonion', {}, 'text')     # -> {'text': '...formatted...'}
```
