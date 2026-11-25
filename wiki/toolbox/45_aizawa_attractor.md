# The Aizawa Attractor (rotation with a radial driver)

**Module:** `ValaQuenta.modules.aizawa_attractor`
**Import:** `from ValaQuenta.modules.aizawa_attractor.tools import AizawaAttractorModule`
**Theory page:** [aizawa_attractor.md](../aizawa_attractor.md)

---

`aizawa_attractor` · v1.0 · confidence floor **ESTABLISHED**

The Aizawa strange attractor as a rotation about the z axis at the constant rate d with a radius driven by dr/dt = (z-b) r: RK4 orbit, the exact cylindrical form, the axisymmetric reduction (f = 0), the fixed points on the axis, the largest Lyapunov exponent, and the JavaScript animation's buffer layout.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`field`** — AIZAWA VECTOR FIELD
  params: `x`, `y`, `z`  ·  confidence: `ESTABLISHED`  ·  signature: `(x=0.8, y=0.3, z=0.9)`
```python
>>> module.run('field', {})['result']
{'x': -0.89, 'y': 2.8600000000000003, 'z': 0.36382999999999976}
```

**`cylindrical`** — CYLINDRICAL FORM: dr/dt = (z-b) r, dphi/dt = d (exact)
  params: `x`, `y`, `z`  ·  confidence: `ESTABLISHED`  ·  signature: `(x=0.8, y=0.3, z=0.9)`
```python
>>> module.run('cylindrical', {})['result']
{'from_field': (np.float64(0.17088007490635065), np.float64(3.5000000000000004)), 'closed_form': (0.17088007490635068, 3.5)}
```

**`fixed_points`** — FIXED POINTS (on the axis) and their eigenvalues
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('fixed_points', {})['result']
[{'point': (0.0, 0.0, np.float64(1.9432643761741544)), 'eigenvalues': [(1.2432643761741544+3.5j), (1.2432643761741544-3.5j), (-2.826276435707525+0j)]}, {'point': (0.0, 0. ...
```

**`orbit`** — RK4 ORBIT (seeded start, burn-in discarded)
  params: `points`, `h`  ·  confidence: `ESTABLISHED`  ·  signature: `(points=2000, h=0.0045)`
```python
>>> module.run('orbit', {})['result']
{'min': [-1.3128101475077565, -1.4530565072100605, -0.18164336065846046], 'max': [1.2705541478405469, 0.9380954443104083, 1.8248115198703958]}
```

**`lyapunov`** — LARGEST LYAPUNOV EXPONENT (Benettin)
  params: `steps`  ·  confidence: `ESTABLISHED`  ·  signature: `(steps=20000)`
```python
>>> module.run('lyapunov', {})['result']
{'lambda_max': 0.0645762398486777}
```

**`js_layout`** — JAVASCRIPT PAGE BUFFER LAYOUT (x, z, y) and lineDistances
  params: `points`  ·  confidence: `ESTABLISHED`  ·  signature: `(points=1000)`
```python
>>> module.run('js_layout', {})['result']
{'n_floats': 3000, 'line_last': 0.9990000128746033}
```

### Shell commands

`az_field` · `az_orbit` · `az_lyapunov` · `az_fixed`


---

*Theory page: [`aizawa_attractor.md`](../aizawa_attractor.md).*
