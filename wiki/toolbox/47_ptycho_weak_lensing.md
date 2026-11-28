# Ptycho-Weak-Lensing (shear, mass map, pointings, polarization)

**Module:** `ValaQuenta.modules.ptycho_weak_lensing`
**Import:** `from ValaQuenta.modules.ptycho_weak_lensing.tools import PtychoWeakLensingModule`
**Theory page:** [ptycho_weak_lensing.md](../ptycho_weak_lensing.md)

---

`ptycho_weak_lensing` · v0.2 · confidence floor **THEORETICAL**

Weak gravitational lensing as a spin-2 inverse problem. Forward: kappa -> psi -> gamma -> g -> epsilon -> galaxy catalogue (NFW / Gaussian halos, flat LCDM efficiency). Inverse: Kaiser-Squires with the reduced-shear iteration, E/B decomposition, the 45-degree rotation and shuffle nulls, shear calibration (m, c). Ptychographic part: overlapping pointings are the probe windows, the object is one real field kappa with B = 0, the iteration is ePIE/Kaczmarz over pointings; an intensity-only (modulus) Gerchberg-Saxton variant is the genuine phase-retrieval case. Polarization (Q+iU) is a second spin-2 field through the same E/B machinery. Built so a calculated mass map can be matched against published shear / DM maps as a control.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify`** — THE HONEST CHECKS: |D|=1, Gaussian halo gamma_t, KS round trip, mass sheet, pure-E polarization, calibration
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify', {})['result']
{'|D| = 1 for k ≠ 0': True, 'Gaussian halo: γ_t = κ̄(<r) − κ (max |err|)': 0.001049924736696961, 'cross component γ_× ≈ 0 (rms)': 6.155232135211071e-06, 'KS round trip, κ ...
```

**`forward`** — FORWARD: NFW halo -> shear profile, magnification
  params: `kappa_s`, `r_s`, `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(kappa_s=0.18, r_s=10.0, n=128)`
```python
>>> module.run('forward', {})['result']
{'kappa_peak': 4.8631167858761035, 'gamma_t_profile_r=2,5,10,20,40': [0.25562, 0.14009, 0.08259, 0.04407], 'gamma_x_rms': 0.013820751920685687, 'max_magnification': 11.95 ...
```

**`reconstruct`** — INVERSE: mock catalogue -> Kaiser-Squires mass map vs truth
  params: `n_per_pix`, `smooth`, `seed`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_per_pix=12.0, smooth=2.0, seed=1)`
```python
>>> module.run('reconstruct', {})['result']
{'corr': 0.932828432648602, 'rms': 0.01475941068447717, 'peak_true': (64, 42), 'peak_rec': (64, 42), 'peak_offset_pix': 0.0, 'B_mode_rms': 0.011379342152457474, 'N_galaxi ...
```

**`null_tests`** — CONTROLS: rotate 45 degrees, shuffle orientations, B-mode floor
  params: `n_per_pix`, `smooth`, `seed`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_per_pix=12.0, smooth=2.0, seed=1)`
```python
>>> module.run('null_tests', {})['result']
{'signal corr': 0.932828432648602, 'rot45: corr of κ_E with truth': 0.014254760601122837, 'rot45: κ_B recovers the lens': 0.9418591890585747, 'shuffled orientation: corr' ...
```

**`calibrate`** — CALIBRATION: inject constant shear and (m, c), recover
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('calibrate', {})['result']
{'gamma_in': (0.03, 0.0), 'm_in': 0.05, 'c_in': 0.002, 'mean_e': (np.float64(0.03436933279865051), np.float64(4.141446792285597e-05)), 'm_recovered': np.float64(0.0789777 ...
```

**`pixel_shapes`** — FROM PIXELS: PSF from stars, PSF forward-modelled, shear calibration (exponential truth, Gaussian model)
  params: `seed`  ·  confidence: `THEORETICAL`  ·  signature: `(seed=3)`
```python
>>> module.run('pixel_shapes', {})['result']
{'PSF from 40 stars: max error at a new position / peak': 0.0038175015227589074, 'no PSF correction: mean ε₁ of zero-shear galaxies (PSF ε₁ = 0.10)': 0.03999501630583876, ...
```

**`pixel_field`** — FROM PIXELS: render a lensed field, measure every shape with the PSF, compare with the truth
  params: `n`, `density`, `min_sep`, `seed`  ·  confidence: `THEORETICAL`  ·  signature: `(n=192, density=0.02, min_sep=20.0, seed=5)`
```python
>>> module.run('pixel_field', {})['result']
{'isolated galaxies': 60, 'fits accepted': 39, 'corr(ε₁ measured, true)': 0.998705724663156, 'slope ε₁ (Gaussian model, exponential truth)': 0.9317728194543924, 'rms diff ...
```

**`ptycho`** — PTYCHOGRAPHY: overlapping pointings (with gaps) -> kappa, vs the naive mosaic
  params: `n_per_pix`, `gaps`, `n_iter`, `tile`, `step`, `seed`  ·  confidence: `THEORETICAL`  ·  signature: `(n_per_pix=12.0, gaps=(1, 4, 6), n_iter=60, tile=48, step=40, seed=2)`
```python
>>> module.run('ptycho', {})['result']
{'pointings': 9, 'observed': 6, 'covered fraction': 0.74664306640625, 'naive mosaic (corr, rms)': (0.8641559083192167, 0.022406649190182412), 'ptychographic (corr, rms)': ...
```

**`modulus`** — INTENSITY-ONLY: recover kappa from |gamma| alone (Gerchberg-Saxton)
  params: `n_iter`  ·  confidence: `THEORETICAL`  ·  signature: `(n_iter=300)`
```python
>>> module.run('modulus', {})['result']
{'start = |gamma|': {'corr(kappa)': 0.8041188881756786, 'corr(-kappa)': -0.8041188881756786, 'data residual': 0.0005234957556618785}, 'start = flat +0.05': {'corr(kappa)' ...
```

**`polarization`** — SECOND FIELD: Q+iU through the same E/B machinery; correlation with shear
  params: `seed`  ·  confidence: `THEORETICAL`  ·  signature: `(seed=1)`
```python
>>> module.run('polarization', {})['result']
{'pol E/B rms (potential-born)': 0.16808733788616564, 'shear E/B rms (lens)': 0.139432392350452, 'corr(shear E, polarization E) independent fields': 0.04735115237701899}
```

**`efficiency`** — SOURCE REDSHIFT: beta = D_ls/D_s and Sigma_crit (flat LCDM)
  params: `z_l`, `z_s`  ·  confidence: `ESTABLISHED`  ·  signature: `(z_l=0.3, z_s=1.0)`
```python
>>> module.run('efficiency', {})['result']
{'beta': np.float64(0.6384810061997637), 'sigma_crit_Msun_per_Mpc2': np.float64(2834055609282049.5)}
```

### Shell commands

`lens_verify` · `lens_ptycho` · `lens_reconstruct` · `lens_nulls`


---

*Theory page: [`ptycho_weak_lensing.md`](../ptycho_weak_lensing.md).*
