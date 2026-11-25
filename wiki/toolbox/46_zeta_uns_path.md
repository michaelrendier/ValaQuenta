# The Zeta Pathway in Universal Native Space (rotation, spring, primes)

**Module:** `ValaQuenta.modules.zeta_uns_path`
**Import:** `from ValaQuenta.modules.zeta_uns_path.tools import ZetaUNSPathModule`
**Theory page:** [zeta_uns_path.md](../zeta_uns_path.md)

---

`zeta_uns_path` · v1.0 · confidence floor **ESTABLISHED**

The critical-line path zeta(1/2 + it) = exp(-i theta) Z as a rotation at rate -theta'(t) with a signed radius Z(t): fast Riemann-Siegel evaluation, the UNS cylinder and sphere charts, the radial driver Z'/Z as a sum of zero poles, the prime spring (Euler path), prime resonance heights, and the zero spectrum whose spikes sit at ln p^k.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`theta`** — RIEMANN-SIEGEL THETA and the rotation rate
  params: `t`  ·  confidence: `ESTABLISHED`  ·  signature: `(t=100.0)`
```python
>>> module.run('theta', {})['result']
{'theta': 87.97216523178723, 'rate': -1.3836444764195812}
```

**`hardy_z`** — HARDY Z by Riemann-Siegel, against mpmath
  params: `t`  ·  confidence: `ESTABLISHED`  ·  signature: `(t=100.0)`
```python
>>> module.run('hardy_z', {})['result']
{'Z_rs': 2.6894071203380796, 'Z_exact': 2.6926970566644637, 'abs_err': 0.0032899363263840797}
```

**`pathway`** — THE PATH POINT: zeta, UNS cylinder, sphere
  params: `t`  ·  confidence: `ESTABLISHED`  ·  signature: `(t=100.0)`
```python
>>> module.run('pathway', {})['result']
{'zeta': [2.6893300436424203, -0.02036112195875436], 'cylinder_rho_phi_t': [3.429656550357528, -0.007570931273019122, 100.0], 'sphere': [0.6533120921765286, -0.0049462754 ...
```

**`driver`** — THE RADIAL DRIVER Z'/Z as a sum over the zero poles (first 60 zeros)
  params: `t`  ·  confidence: `ESTABLISHED`  ·  signature: `(t=40.3)`
```python
>>> module.run('driver', {})['result']
{'Z_prime_over_Z': -1.5106869237871108, 'zero_sum_60': -1.914048186818344}
```

**`prime_resonance`** — PRIME RESONANCE HEIGHTS
  params: `p`, `T`  ·  confidence: `CALCULATED`  ·  signature: `(p=2, T=60.0)`
```python
>>> module.run('prime_resonance', {})['result']
{'t': [0.0, 9.0647, 18.1294, 27.1942, 36.2589, 45.3236, 54.3883]}
```

**`euler_path`** — THE PRIME SPRING (Euler path) at height t
  params: `t`, `n`  ·  confidence: `CALCULATED`  ·  signature: `(t=14.1347, n=12)`
```python
>>> module.run('euler_path', {})['result']
{'primes': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37], 'steps': [[-0.5178629381392509, 0.1539925876333255], [-0.45200791657388195, -0.06560792602705331], [-0.3075072405 ...
```

**`spectrum_ticks`** — WHERE THE ZERO SPECTRUM SPIKES: x = ln p^k, weight ln p / p^(k/2)
  params: `xmax`  ·  confidence: `CALCULATED`  ·  signature: `(xmax=2.5)`
```python
>>> module.run('spectrum_ticks', {})['result']
[{'x': 0.6931, 'p': 2, 'k': 1, 'weight': np.float64(0.4901)}, {'x': 1.0986, 'p': 3, 'k': 1, 'weight': np.float64(0.6343)}, {'x': 1.3863, 'p': 2, 'k': 2, 'weight': np.floa ...
```

### Shell commands

`zuns_zeta` · `zuns_theta` · `zuns_Z` · `zuns_path`


---

*Theory page: [`zeta_uns_path.md`](../zeta_uns_path.md).*
