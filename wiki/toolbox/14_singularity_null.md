# Singularity-NULL Engine — The Singularity IS Identity. Tower Collapses.

**Module:** `ValaQuenta.modules.singularity_null`
**Import:** `from ValaQuenta.modules.singularity_null.tools import SingularityNullModule`
**Theory page:** [`../singularity_null.md`](../singularity_null.md)

---

`singularity_null` · v0.100 · confidence floor **THEORETICAL**

The Singularity IS identity. The Hamiltonian sees only one thing: AWAY. Engines: circle-null modes (Ptolemy inversion = 1 word), tower collapse snakes (n-ball volume = Snakes & Ladders board, peak n*≈5.257), Berry-Keating singularity (H=xp, repulsive fixed point, σ=½ equatorial geodesic), FLT prime extinction sieve (primes defined by negative space, σ=½ as FLT boundary).

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`full_singularity_null`** — All 4 Singularity-NULL engines
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('full_singularity_null', {})['result']
{'theme': 'Singularity-NULL Engine — The Singularity IS Identity. The Tower Collapses.', 'circle_null_modes': {'claim': 'Circle says NULL exactly ONE way: the Ptolemy inversion. Every zero-divisor pair is this word, spoken in a different subspace.', 'ptolemy_inversion': {'map': 'z → R_H²/z̄', 'R_...
```

**`circle_null_modes`** — How many ways can circle say NULL? Exactly 1: Ptolemy inversion.
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('circle_null_modes', {})['result']
{'claim': 'Circle says NULL exactly ONE way: the Ptolemy inversion. Every zero-divisor pair is this word, spoken in a different subspace.', 'ptolemy_inversion': {'map': 'z → R_H²/z̄', 'R_H': 0.70710678, 'R_H_formula': 'R_H = 1/√2', 'fixed_circle': '|z| = R_H = 1/√2', 'sends_0_to': '∞', 'sends_inf...
```

**`tower_collapse_snakes`** — Snakes & Ladders = Cayley-Dickson tower. V(n) = board height. Peak n*≈5.257.
  params: `n_max`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_max=30)`
```python
>>> module.run('tower_collapse_snakes', {})['result']
{'claim': 'Snakes and Ladders IS the Cayley-Dickson tower. V(n) = board height. Peak at n*≈5.257. Tower collapses back to the singularity.', 'n_star': {'value': 5.2569464, 'V_star': 5.27776802, 'between': 'Between ℍ (n=4) and 𝕆 (n=8)', 'bao_connection': 'n* = BAO freeze point. Peak semantic densi...
```

**`berry_keating_singularity`** — H=xp: singularity is repulsive fixed point. σ=½ is equatorial geodesic.
  params: `max_t`  ·  confidence: `ESTABLISHED`  ·  signature: `(max_t=50.0)`
```python
>>> module.run('berry_keating_singularity', {})['result']
{'claim': 'The singularity is the repulsive fixed point of H_BK=xp. σ=½ is the equatorial geodesic between singularity and infinity. The Hamiltonian sees only one thing at x=0: AWAY.', 'bk_hamiltonian': {'classical': 'H_BK = xp', 'quantum': 'H = -iℏ(x d/dx + ½)', 'conjecture': 'eigenvalues ↔ Im(R...
```

**`flt_prime_extinction_sieve`** — FLT defines primes by extinction. Negative space = primary identity.
  params: `N`  ·  confidence: `ESTABLISHED`  ·  signature: `(N=100)`
```python
>>> module.run('flt_prime_extinction_sieve', {})['result']
{'claim': 'FLT defines primes by extinction. What cannot be factored IS prime. They exist on σ=½ because their negative space defines them first.', 'primes_to_N': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97], 'prime_count': 25, 'pythagorean_trip...
```

---

### Running via the registry

```python
from ValaQuenta.modules.singularity_null.tools import SingularityNullModule

m = SingularityNullModule()
m.formulary()                              # list every Equation this module exposes
m.run('full_singularity_null', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('full_singularity_null', {}, 'text')     # -> {'text': '...formatted...'}
```
