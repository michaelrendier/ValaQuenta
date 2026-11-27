# The Bell Curve (Statistics, Probability, Statistical Mechanics)

**Module:** `ValaQuenta.modules.bell_curve`
**Import:** `from ValaQuenta.modules.bell_curve.tools import BellCurveModule`
**Theory page:** [bell_curve.md](../bell_curve.md)

---

`bell_curve` · v1.1 · confidence floor **ESTABLISHED**

One statistics machinery for everywhere a probability, a spread or a gradient shows up: streaming mergeable moments, the normal/t/chi-square/F/binomial/Poisson/beta distributions, n-sigma and Six-Sigma, hypothesis tests, effect sizes, resampling, information measures, Bayes, the canonical ensemble and circular statistics. Verified against scipy.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`moments`** — STREAMING MOMENTS: mean, variance, skew, kurtosis in one mergeable pass
  params: `xs`  ·  confidence: `ESTABLISHED`  ·  signature: `(xs=[1.1717, -0.1825, -1.0408, -1.06, 1.3701, 0.3172, 0.2047, -0.5778, -1.1641, 0.0153, -0.5716, -0.6199, -2.3372, -0.4202, -0.3437, -1.1572, 0.7551, -0.5005, 0.6653, -0.7415, -0.953, -0.1127, -0.381, -1.0009, 0.2262, 1.3987, -0.1241, 0.6925, -0.6902, 0.0169, -0.6111, -0.4853, 1.0158, 0.4037, -0.3598, 0.5339, -1.5953, -0.5563, 0.6763, -0.397])`
```python
>>> module.run('moments', {})['result']
{'n': 40, 'mean': -0.21300750000000002, 'std': 0.8143309276245729, 'sem': 0.12875702502056902, 'skew': 0.004366672124164765, 'kurt_excess': -0.015482406976699892}
```

**`normal`** — THE BELL CURVE: pdf, cdf, quantile of the normal distribution
  params: `x`, `mu`, `sigma`  ·  confidence: `ESTABLISHED`  ·  signature: `(x=1.96, mu=0.0, sigma=1.0)`
```python
>>> module.run('normal', {})['result']
{'pdf': 0.058440944333451476, 'cdf': 0.9750021048517795, 'sf': 0.024997895148220435}
```

**`sigma_levels`** — n-SIGMA <-> p-VALUE, and SIX SIGMA
  params: `sigma`  ·  confidence: `ESTABLISHED`  ·  signature: `(sigma=3.0)`
```python
>>> module.run('sigma_levels', {})['result']
{'p_two_sided': 0.0026997960632601913, 'p_one_sided': 0.0013498980316300957, 'dpmo': 66807.20126885809}
```

**`nball`** — N-BALL: volume and sphere area at any real dimension, and where they peak
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n=16.0)`
```python
>>> module.run('nball', {})['result']
{'volume': 0.23533063035889346, 'sphere_area': 3.7652900857422895, 'volume_peak_n': 5.256946404470526, 'area_peak_n': 7.256946404529922}
```

**`welch_t`** — WELCH t-TEST: two means, unequal variances
  params: `xs`, `ys`  ·  confidence: `ESTABLISHED`  ·  signature: `(xs=[1.1717, -0.1825, -1.0408, -1.06, 1.3701, 0.3172, 0.2047, -0.5778, -1.1641, 0.0153, -0.5716, -0.6199, -2.3372, -0.4202, -0.3437, -1.1572, 0.7551, -0.5005, 0.6653, -0.7415, -0.953, -0.1127, -0.381, -1.0009, 0.2262, 1.3987, -0.1241, 0.6925, -0.6902, 0.0169, -0.6111, -0.4853, 1.0158, 0.4037, -0.3598, 0.5339, -1.5953, -0.5563, 0.6763, -0.397], ys=[-0.2102, 0.2512, -0.995, 1.1177, 0.4996, 0.889, 1.0421, -0.4414, 1.2861, 1.3904, -0.6524, -0.036, 0.7242, -0.7036, 1.4525, -0.202, -0.252, 0.6888, 0.3035, 0.9282, 0.4665, -0.2073, 0.9669, 1.6684, -0.0877, 2.6841, -0.4651, 0.5836, 0.9804, 1.4707, 0.6666, 0.9954, -1.3526, 0.6338, 1.9473, 1.2414, -0.4787, 0.821, 0.486, 0.9021])`
```python
>>> module.run('welch_t', {})['result']
{'t': -3.9670836008411072, 'df': 77.8615613550955, 'p': 0.00016063596652293732, 'diff': -0.7380950000000002, 'ci': (-1.1085120540575555, -0.36767794594244474), 'd': -0.88 ...
```

**`proportion`** — BINOMIAL PROPORTION: Wilson interval and z-test
  params: `k`, `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(k=7, n=40)`
```python
>>> module.run('proportion', {})['result']
{'wilson_95': (0.0874541374603592, 0.31949990331787714), 'phat': 0.175}
```

**`chi_square`** — CHI-SQUARE: goodness of fit and independence
  params: `table`  ·  confidence: `ESTABLISHED`  ·  signature: `(table=((20, 30, 10), (15, 25, 40)))`
```python
>>> module.run('chi_square', {})['result']
{'chi2': 16.65151515151515, 'df': 2, 'p': 0.00024219737240771533, 'cramers_v': 0.34487591092941516}
```

**`mann_whitney`** — MANN-WHITNEY U and AUC: distribution-free two-sample test
  params: `xs`, `ys`  ·  confidence: `ESTABLISHED`  ·  signature: `(xs=[1.1717, -0.1825, -1.0408, -1.06, 1.3701, 0.3172, 0.2047, -0.5778, -1.1641, 0.0153, -0.5716, -0.6199, -2.3372, -0.4202, -0.3437, -1.1572, 0.7551, -0.5005, 0.6653, -0.7415, -0.953, -0.1127, -0.381, -1.0009, 0.2262, 1.3987, -0.1241, 0.6925, -0.6902, 0.0169, -0.6111, -0.4853, 1.0158, 0.4037, -0.3598, 0.5339, -1.5953, -0.5563, 0.6763, -0.397], ys=[-0.2102, 0.2512, -0.995, 1.1177, 0.4996, 0.889, 1.0421, -0.4414, 1.2861, 1.3904, -0.6524, -0.036, 0.7242, -0.7036, 1.4525, -0.202, -0.252, 0.6888, 0.3035, 0.9282, 0.4665, -0.2073, 0.9669, 1.6684, -0.0877, 2.6841, -0.4651, 0.5836, 0.9804, 1.4707, 0.6666, 0.9954, -1.3526, 0.6338, 1.9473, 1.2414, -0.4787, 0.821, 0.486, 0.9021])`
```python
>>> module.run('mann_whitney', {})['result']
{'U': 425.0, 'z': 3.603627930191914, 'p': 0.00031380618277474377, 'auc': 0.265625}
```

**`kappa`** — COHEN KAPPA: chance-corrected agreement of two raters
  params: `a`, `b`  ·  confidence: `ESTABLISHED`  ·  signature: `(a=(0, 1, 1, 0, 1, 0, 0, 1), b=(0, 1, 0, 0, 1, 0, 1, 1))`
```python
>>> module.run('kappa', {})['result']
{'kappa': 0.5, 'po': 0.75, 'pe': 0.5, 'se': 0.30618621784789724}
```

**`multiple_testing`** — MULTIPLE TESTING: Bonferroni, Holm, Benjamini-Hochberg
  params: `ps`  ·  confidence: `ESTABLISHED`  ·  signature: `(ps=(0.001, 0.008, 0.039, 0.041, 0.2))`
```python
>>> module.run('multiple_testing', {})['result']
{'bonferroni': [0.005, 0.04, 0.195, 0.20500000000000002, 1.0], 'holm': [0.005, 0.032, 0.11699999999999999, 0.11699999999999999, 0.2], 'bh': [0.005, 0.02, 0.05125000000000 ...
```

**`bootstrap`** — BOOTSTRAP CONFIDENCE INTERVAL (seeded)
  params: `xs`  ·  confidence: `ESTABLISHED`  ·  signature: `(xs=[1.1717, -0.1825, -1.0408, -1.06, 1.3701, 0.3172, 0.2047, -0.5778, -1.1641, 0.0153, -0.5716, -0.6199, -2.3372, -0.4202, -0.3437, -1.1572, 0.7551, -0.5005, 0.6653, -0.7415, -0.953, -0.1127, -0.381, -1.0009, 0.2262, 1.3987, -0.1241, 0.6925, -0.6902, 0.0169, -0.6111, -0.4853, 1.0158, 0.4037, -0.3598, 0.5339, -1.5953, -0.5563, 0.6763, -0.397])`
```python
>>> module.run('bootstrap', {})['result']
{'stat': -0.21300749999999996, 'ci': (-0.43840737499999993, 0.007230187499999951), 'se': 0.12057012613996596}
```

**`information`** — ENTROPY, KL and JENSEN-SHANNON
  params: `p`, `q`  ·  confidence: `ESTABLISHED`  ·  signature: `(p=(0.5, 0.25, 0.25), q=(0.4, 0.4, 0.2))`
```python
>>> module.run('information', {})['result']
{'H_p': 1.5, 'KL': 0.07192809488736233, 'JS': 0.01862176307426544, 'perplexity': 2.8284271247461903}
```

**`bayes`** — BETA-BINOMIAL POSTERIOR
  params: `successes`, `trials`  ·  confidence: `ESTABLISHED`  ·  signature: `(successes=7, trials=20)`
```python
>>> module.run('bayes', {})['result']
{'a': 8.0, 'b': 14.0, 'mean': 0.36363636363636365, 'credible': (0.18107162554017364, 0.5696754829041275)}
```

**`canonical_ensemble`** — CANONICAL ENSEMBLE: Z, U, S, F, Cv (softmax is one)
  params: `energies`, `T`, `kB`  ·  confidence: `ESTABLISHED`  ·  signature: `(energies=(0.0, 1.0, 2.5, 4.0), T=0.8, kB=1.0)`
```python
>>> module.run('canonical_ensemble', {})['result']
{'Z': 1.337179677482683, 'lnZ': 0.2905626776339923, 'U': 0.31656098731019816, 'F': -0.23245014210719384, 'S': 0.6862639117717401, 'Cv': 0.6250537386874628}
```

**`ising_1d`** — 1-D ISING RING, exact by transfer matrix
  params: `N`, `J`, `h`, `beta`  ·  confidence: `ESTABLISHED`  ·  signature: `(N=8, J=1.0, h=0.3, beta=0.7)`
```python
>>> module.run('ising_1d', {})['result']
{'Z': 2946.527094968332, 'lambda_plus': 2.712594283320591, 'lambda_minus': 1.4040444700196044, 'free_energy_per_spin': -1.426496874978715}
```

**`circular`** — CIRCULAR STATISTICS: mean direction, resultant length, Rayleigh test
  params: `angles`  ·  confidence: `ESTABLISHED`  ·  signature: `(angles=(0.1, 0.2, 0.15, 6.2, 0.05, 0.12))`
```python
>>> module.run('circular', {})['result']
{'R': 0.9959830337608319, 'Z': 5.951893221236582, 'p': 0.00037602804646711497, 'mean_direction': 0.0895695092116332}
```

### Shell commands

`bc_norm_cdf` · `bc_norm_ppf` · `bc_sigma_p` · `bc_p_sigma` · `bc_t` · `bc_moments` · `bc_wilson` · `bc_canonical` · `bc_check`


---

*Theory page: [`bell_curve.md`](../bell_curve.md).*
