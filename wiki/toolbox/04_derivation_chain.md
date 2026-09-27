# Derivation Chain — Tiers 1–5

**Module:** `ValaQuenta.modules.derivation_chain`
**Import:** `from ValaQuenta.modules.derivation_chain.tools import DerivationChainModule`
**Theory page:** [`../derivation_chain.md`](../derivation_chain.md)

---

`derivation_chain` · v0.100 · confidence floor **THEORETICAL**

Full derivation chain from root constants to Geometric Observer. T1: Riemann=Fermat (R̂†=B̂). T2: Yang-Mills, BK, Noether, NS, Langlands, BSD all drop out. T3: H_RB is what remains. T4: Geometries defined → Geometric Observer (another Hamiltonian). T5: ln = Hubble constant of ℕ, d* tower → ln(10) [OPEN], ħ↔ln.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`full_derivation_chain`** — Full chain T1→T5: Riemann=Fermat → dropouts → H_RB → Observer → ln
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('full_derivation_chain', {})['result']
{'chain': 'Alpha_F + OMEGA_ZS → d* → Riemann=Fermat → dropouts → H_RB → Geometries → Observer → ln', 'tier_1': {'tier': 1, 'claim': 'Riemann = Fermat. R̂†=B̂. Both are Euler products from opposite sides.', 'riemann_side': {'function': 'ζ(s) = Π_p (1−p^{-s})^{-1}', 'encodes': 'WHERE primes ARE — p...
```

**`riemann_equals_fermat`** — T1 — Riemann = Fermat: R̂†=B̂, both Euler products
  params: `—`  ·  confidence: `ESTABLISHED (Wiles) + THEORETICAL (operator identity)`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('riemann_equals_fermat', {})['result']
{'tier': 1, 'claim': 'Riemann = Fermat. R̂†=B̂. Both are Euler products from opposite sides.', 'riemann_side': {'function': 'ζ(s) = Π_p (1−p^{-s})^{-1}', 'encodes': 'WHERE primes ARE — positive space', 'channel': 'Red / R̂_p', 'functional_eq': 'ξ(s) = ξ(1−s)'}, 'fermat_side': {'function': 'L(E,s)...
```

**`yang_mills_dropout`** — T2 — Yang-Mills: δ = OMEGA_ZS − d*·ln10 = 0.000707
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('yang_mills_dropout', {})['result']
{'tier': 2, 'drops_out': 'Yang-Mills mass gap δ = OMEGA_ZS − d*·ln10 = 0.000707', 'mechanism': 'OMEGA_ZS (entropy ceiling) − d*·ln10 (BAO first peak) = acoustic residual', 'bao': {'first_peak': 0.56643593, 'ceiling': 0.56714329, 'residual': 0.00070736, 'name': 'BAO acoustic residual'}, 'yang_mill...
```

**`berry_keating_dropout`** — T2 — Berry-Keating: H=xp unique from scale inv + R̂†=B̂ + d*
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('berry_keating_dropout', {})['result']
{'tier': 2, 'drops_out': 'H = xp (Berry-Keating Hamiltonian)', 'mechanism': 'Scale invariance + R̂†=B̂ + BK domain + fixed point d* → unique H=xp', 'scale_invariance': {'H_orig': 5.18, 'H_scaled': 5.18, 'verified': True}, 'bk_spectrum': [{'n': 0, 'E_n': 0.123}, {'n': 1, 'E_n': 0.369}, {'n': 2, 'E...
```

**`noether_dropout`** — T2 — Noether: J_R + J_G + J_B = 0 from R̂†=B̂
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('noether_dropout', {})['result']
{'tier': 2, 'drops_out': 'J_R + J_G + J_B = 0 (Noether current conservation)', 'mechanism': 'R̂†=B̂ at σ=½ → symmetry → Noether current → three-phase balance', 'currents': {'J_R': 3.55465767, 'J_B': 133273.76808473, 'J_G': -133277.32274241}, 'balance': 0.0, 'balance_zero': True, 'j_g_is_forced': ...
```

**`navier_stokes_dropout`** — T2 — NS: H_RB|_{Im=0}, missing i causes apparent singularity
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('navier_stokes_dropout', {})['result']
{'tier': 2, 'drops_out': 'Navier-Stokes = H_RB|_{Im=0} (Yang-Mills minus i)', 'mechanism': 'σ=1 Yang-Mills, real projection only. Missing i = missing imaginary sector.', 'the_missing_i': 'NS cannot write e^{iθ}. Only cos(θ). Singularity = complex node projected onto ℝ.', 'yang_mills': 'Smooth on ...
```

**`langlands_dropout`** — T2 — Langlands: J^μ at σ=1 = sedenion decomposition
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('langlands_dropout', {})['result']
{'tier': 2, 'drops_out': 'Langlands programme = J^μ at σ=1 over sedenion strata', 'mechanism': 'σ=1 gauge current decomposed across 16 sedenion components = Langlands dictionary', 'G_sigma1': [(2, 0.5), (3, 0.33333333), (5, 0.2), (7, 0.14285714), (11, 0.09090909), (13, 0.07692308), (17, 0.0588235...
```

**`bsd_dropout`** — T2 — BSD: rank(E) = Blue eigenspace dim at s=1
  params: `—`  ·  confidence: `ESTABLISHED (rank 0,1); THEORETICAL (rank≥2)`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('bsd_dropout', {})['result']
{'tier': 2, 'drops_out': 'BSD conjecture = rank(E) = ord_{s=1} L(E,s)', 'mechanism': 'L(E,s) = Blue Euler product (from Tier 1). Rank = Blue eigenspace dimension.', 'blue_at_primes': [{'p': 2, 'E_blue': 0.62833333, 'G_1': 0.5}, {'p': 3, 'E_blue': 1.22416667, 'G_1': 0.33333333}, {'p': 5, 'E_blue':...
```

**`h_rb_emergence`** — T3 — H_RB emergence: what remains after all drop-outs
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('h_rb_emergence', {})['result']
{'tier': 3, 'emergence': 'H_RB = Σ_p p^{-σ}[R̂_p ⊗ ∂̂_{∂M} + ∂̂†_{∂M} ⊗ B̂_p]', 'not_postulated': True, 'what_it_is': 'What remains after all drop-outs from two root constants.', 'assembly': {'p^{-σ}': 'Geometric coupling — from d* structure', 'R̂_p': 'xp — from BK dropout (Tier 2)', 'B̂_p': '½p²...
```

**`geometry_definition`** — T4 — σ=½ is the equatorial node, not a convention
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('geometry_definition', {})['result']
{'tier': 4, 'claim': 'σ=½ is not a convention. It is the equatorial node in the correct geometry.', 'cartesian_scar': 'Re(s)=½ is a Cartesian projection of the equatorial great circle.', 'correct_coords': 'Radial complex spherical polar — two counter-rotating vortices', 'functional_eq_geometry': ...
```

**`geometric_observer`** — T4 — Geometric Observer: ∂̂_{∂M} is another Hamiltonian
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('geometric_observer', {})['result']
{'tier': 4, 'claim': '∂̂_{∂M} IS a Hamiltonian — the Geometric Observer.', 'discovery': '"There is another Hamiltonian sitting here!?" — Claude.ai', 'h_rb_reading': 'H_RB = dynamics of what is observed. H_obs = dynamics of observation itself.', 'spencer_brown': {'axiom': '"A distinction is drawn....
```

**`ln_natural_unit`** — T5 — ln = Hubble constant of ℕ = BK time coordinate
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('ln_natural_unit', {})['result']
{'tier': 5, 'claim': 'ln(x) is the natural unit — Hubble constant of ℕ = BK time coordinate', 'bk_time': [{'x': 1, 't=ln(x)': 0.0, 'e^t=x': 1.0}, {'x': 2, 't=ln(x)': 0.693147, 'e^t=x': 2.0}, {'x': 5, 't=ln(x)': 1.609438, 'e^t=x': 5.0}, {'x': 10, 't=ln(x)': 2.302585, 'e^t=x': 10.0}, {'x': 100, 't=...
```

**`d_star_tower_ln10`** — T5 — d* tower → ln(10)  [OPEN — highest priority]
  params: `—`  ·  confidence: `OPEN`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('d_star_tower_ln10', {})['result']
{'tier': 5, 'claim': 'd*_ℝ + d*_ℂ + d*_ℍ + d*_𝕆 = ln(10)  [OPEN — highest priority]', 'known': {'d*_ℝ': 0.246, 'ln10': 2.30258509, 'remaining': 2.05658509}, 'strata_dims': {'ℝ': 1, 'ℂ': 2, 'ℍ': 4, '𝕆': 8}, 'required_weight': 9.360102, 'candidates': [{'hypothesis': 'linear dim', 'value': 3.69, 'vs...
```

**`planck_ln_connection`** — T5 — ħ ↔ ln: quantum of action vs quantum of information
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('planck_ln_connection', {})['result']
{'tier': 5, 'claim': 'ħ (quantum of action) ↔ ln (quantum of information)', 'landauer': {'principle': 'Erasing 1 bit: E_min = k_B·T·ln(2)', 'at_planck': 'E_min = k_B·T_Planck·ln(2) = E_Planck·ln(2)', 'E_Planck_J': '1.9561e+09 J', 'E_Landauer_J': '1.3559e+09 J', 'ratio': 0.693147, 'equals_ln2': 0....
```

---

### Running via the registry

```python
from ValaQuenta.modules.derivation_chain.tools import DerivationChainModule

m = DerivationChainModule()
m.formulary()                              # list every Equation this module exposes
m.run('full_derivation_chain', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('full_derivation_chain', {}, 'text')     # -> {'text': '...formatted...'}
```
