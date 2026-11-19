# The Witch's Hat Engine (virtual brim, hat potential, paths of action)

**Module:** `ValaQuenta.modules.witches_hat`
**Import:** `from ValaQuenta.modules.witches_hat.tools import WitchesHatModule`
**Theory page:** [witches_hat.md](../witches_hat.md)

---

`witches_hat` · v0.1 · confidence floor **THEORETICAL**

Static snapshots of the Witch's Hat: the hat potential (the Standard-Model Higgs quartic, a family of exponents, the fermion exchange hole, the boson bunching well, the difference of Gaussians), the brim, and the classical paths of action from the brim, with size, depth, energy and aim adjustable; the focal resolution, the defocus cone, the energy regimes; the zeta pair correlation against the 1-D fermion kernel. Returns plain data: rendering is done elsewhere.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify`** — VERIFY: closed form and Standard-Model numbers
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify', {})['result']
{'focus_closed_form_relerr': np.float64(8.839186331542999e-06), 'hat_brim': -1.0, 'hat_top': 0.0, 'sm': {'lam': 0.12938347743146458, 'mu2': 7843.78125, 'brim_radius_GeV': ...
```

**`snapshot`** — SNAPSHOT: hat, brim, path bundle
  params: `shape`, `n`, `size`, `depth`, `E`, `aim`, `spread`  ·  confidence: `THEORETICAL`  ·  signature: `(shape='quartic', n=4.0, size=1.0, depth=1.0, E=0.0, aim=0.0, spread=0.3)`
```python
>>> module.run('snapshot', {})['result']
{'meta': {'shape': 'quartic', 'n': 4.0}, 'size': 1.0, 'depth': 1.0, 'E': 0.0, 'aim': 0.0, 'spread': 0.3, 'surface_r': array([0.        , 0.02372881, 0.04745763, 0.0711864 ...
```

**`focus`** — FOCUS: resolution of the bundle
  params: `shape`, `n`, `E`  ·  confidence: `ESTABLISHED`  ·  signature: `(shape='quartic', n=4.0, E=0.0)`
```python
>>> module.run('focus', {})['result']
0.3868204322816247
```

**`defocus`** — DEFOCUS: the ring caustic against the aim offset
  params: `shape`, `n`, `E`  ·  confidence: `ESTABLISHED`  ·  signature: `(shape='quartic', n=4.0, E=0.0)`
```python
>>> module.run('defocus', {})['result']
{'aim': array([0.  , 0.05, 0.1 , 0.15, 0.2 , 0.25, 0.3 , 0.35, 0.4 , 0.45, 0.5 ]), 'ring_radius': array([0.        , 0.18883842, 0.26813618, 0.32963887, 0.38197269,
      ...
```

**`regimes`** — ENERGY REGIMES: reflected, point, through
  params: `shape`, `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(shape='quartic', n=4.0)`
```python
>>> module.run('regimes', {})['result']
[{'E': -0.5, 'r_min': np.float64(0.5411961001473122), 'regime': 'reflected'}, {'E': -0.1, 'r_min': np.float64(0.22653190053219796), 'regime': 'reflected'}, {'E': -0.01, ' ...
```

**`shapes`** — SHAPES: resolution of every hat
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('shapes', {})['result']
[{'shape': 'quartic', 'V(0)': 0.0, 'V(1)': -1.0, 'V(4)': 224.0, 'resolution': 0.3868204322816247, 'matching_quartic_n': 4.014023372287145, 'outer_wall': True}, {'shape':  ...
```

**`compare`** — COMPARE: Standard Model and VAPMIP Lagrangians
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('compare', {})['result']
{'standard_model': {'brim_radius': 246.22, 'depth': 118880914.16162813, 'm_over_v': 0.5086914141824385, 'tilt': 0.0, 'scale': 1.0, 'focus_resolution': 0.3868204322816247} ...
```

**`vap_snapshot`** — VAPMIP SNAPSHOT: the monad Lagrangian's hat and paths
  params: `g`, `psi_x`, `psi_y`  ·  confidence: `THEORETICAL`  ·  signature: `(g=0.2, psi_x=1.0, psi_y=0.0)`
```python
>>> module.run('vap_snapshot', {})['result']
{'model': 'vapmip_ssb', 'brim_radius': 1.4142135623730951, 'depth': 0.3090169943749474, 'hilltop': array([0.20426116, 0.        ]), 'E': 0.012489551233891755, 'X': array( ...
```

**`l_io`** — L_(I|O) as the action of the actual path
  params: `model`  ·  confidence: `THEORETICAL`  ·  signature: `(model='sm')`
```python
>>> module.run('l_io', {})['result']
{'aim': array([0.  , 0.05, 0.1 , 0.15, 0.2 , 0.25, 0.3 , 0.35, 0.4 ]), 'W': array([2295496.88292931, 2299003.2118398 , 2297877.80773756,
       2297656.12505286, 2294048. ...
```

**`sm_hat`** — STANDARD MODEL HAT
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('sm_hat', {})['result']
{'lam': 0.12938347743146458, 'mu2': 7843.78125, 'brim_radius_GeV': 246.22, 'depth_GeV4': 118880914.16162813, 'Vpp_hilltop': -7843.78125, 'Vpp_brim': 15687.5625, 'm_W_tree ...
```

### Shell commands

`hat_snapshot` · `hat_focus` · `hat_defocus` · `hat_regimes` · `hat_shapes` · `hat_compare` · `hat_l_io` · `hat_snapshot_plane` · `hat_sm` · `hat_verify` · `hat_action` · `hat_stationary_paths` · `hat_morse_index` · `hat_trial_variations` · `hat_rays` · `hat_caustics` · `hat_caustic_summary` · `hat_closest_approach` · `hat_euclidean_release`


---

*Theory page: [`witches_hat.md`](../witches_hat.md).*
