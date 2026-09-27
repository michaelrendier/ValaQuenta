# Σ_RB  RedBlue Summed Integral

**Module:** `ValaQuenta.modules.h_rb_hat`
**Import:** `from ValaQuenta.modules.h_rb_hat.tools import SigmaRBModule`
**Theory page:** [`../h_rb_hat.md`](../h_rb_hat.md)

---

`h_rb_hat` · v0.120 · confidence floor **THEORETICAL**

Σ_RB = Σ_p p^{-σ} [R̂_p ⊗ ∂̂_∂M + ∂̂_∂M† ⊗ B̂_p]. The RedBlue Summed Integral. The Boundary Generator. The Σ is the summation sign. The RB is Red-Blue. The existence of a distinction. Facet projections: GR (σ=2), Yang-Mills (σ=1), QM/RH (σ=½), NS (σ=1, Im=0), Noether (boundary invariant), Fermat (forbidden zone). All six open Clay Millennium Problems project from this operator.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`sigma_rb_evaluate`** — Σ_RB — RedBlue Summed Integral at (σ, x, p)
  params: `sigma, x, p_momentum, n_primes`  ·  confidence: `THEORETICAL`  ·  signature: `(sigma=0.5, x=1.0, p_momentum=1.0, n_primes=20)`
```python
>>> module.run('sigma_rb_evaluate', {})['result']
{'sigma': 0.5, 'x': 1.0, 'p_momentum': 1.0, 'n_primes': 20, 'terms': [{'prime': 2, 'sigma': 0.5, 'G_p': 0.7071067811865476, 'E_red': 1.0, 'E_blue': 1.5508333333333333, 'balance': -0.5508333333333333, 'term_red': 0.7071067811865476, 'term_blue': 1.0966047664901375, 'self_adjoint': False}, {'prime'...
```

**`self_adjoint_demonstration`** — Self-adjointness: 1=1 is adjoint to 1!=1
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('self_adjoint_demonstration', {})['result']
{'statement': 'Self-adjointness preserves truth, not form.', '1_equals_1': 1, '1_factorial': 1, 'adjoint_check': True, 'n2_identity': 2, 'n2_factorial': 2, 'n3_identity': 3, 'n3_factorial': 6, 'factorial_fixed_points': [1, 2], 'note_fixed_points': 'n! = n only at n=0,1 — these are the factorial p...
```

**`sigma_phase_diagram`** — σ phase diagram — which σ → which theory
  params: `n_points`  ·  confidence: `THEORETICAL`  ·  signature: `(n_points=20)`
```python
>>> module.run('sigma_phase_diagram', {})['result']
{'diagram': [{'sigma': 0.0, 'theory': 'Trivial / Poincaré', 'euler_mag': 1.0, 'euler_re': 1.0, 'converges': False, 'critical_line': False}, {'sigma': 0.1316, 'theory': 'Fermat Forbidden Zone', 'euler_mag': 255797756.70818964, 'euler_re': 255797756.70818964, 'converges': False, 'critical_line': Fa...
```

**`euler_product`** — Euler product ζ(s) = Π_p (1−p^{−s})^{−1}
  params: `sigma, t, n_primes`  ·  confidence: `ESTABLISHED`  ·  signature: `(sigma=0.5, t=0.0, n_primes=20)`
```python
>>> module.run('euler_product', {})['result']
{'result': (583.7119433744068+0j), 'magnitude': 583.7119433744068}
```

**`facet_gr`** — Facet: General Relativity (σ=2)
  params: `kappa`  ·  confidence: `ESTABLISHED`  ·  signature: `(kappa=1.0)`
```python
>>> module.run('facet_gr', {})['result']
{'facet': 'General Relativity', 'sigma': 2.0, 'coupling_sum': 0.4497032182086859, 'action': 'S_EH = (c⁴/16πG) ∫ R √{-g} d⁴x', 'field_equation': 'G_μν + Λg_μν = (8πG/c⁴) T_μν', 'noether_current': '∂_μ T^μν = 0  (energy-momentum conservation)', 'domain': 'smooth 4-manifold, metric g_μν', 'R_hat_map...
```

**`facet_yang_mills`** — Facet: Yang-Mills / Standard Model (σ=1)
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_yang_mills', {})['result']
{'facet': 'Yang-Mills / Standard Model', 'sigma': 1.0, 'coupling_sum': 1.7428669168860038, 'G_per_prime': [(2, 0.5), (3, 0.3333333333333333), (5, 0.2), (7, 0.14285714285714285), (11, 0.09090909090909091), (13, 0.07692307692307693), (17, 0.058823529411764705), (19, 0.05263157894736842)], 'lagrangi...
```

**`facet_qm`** — Facet: Quantum Mechanics (σ=½)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_qm', {})['result']
{'facet': 'Quantum Mechanics', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'equation': 'iħ ∂|ψ⟩/∂t = H|ψ⟩', 'time_independent': 'H|ψ_n⟩ = E_n|ψ_n⟩', 'noether_current': 'J^μ = iħ (ψ* ∂^μ ψ − ψ ∂^μ ψ*) / 2m  (probability current)', 'domain': 'Hilbert space L²(ℝ³)', 'R_hat_maps_to': 'kinetic te...
```

**`facet_navier_stokes`** — Facet: Navier-Stokes (σ=1, Im=0) — lacks i
  params: `galaxy_size_ly`  ·  confidence: `THEORETICAL`  ·  signature: `(galaxy_size_ly=50000.0)`
```python
>>> module.run('facet_navier_stokes', {})['result']
{'facet': 'Navier-Stokes', 'sigma': 1.0, 'imaginary': 0.0, 'coupling_sum': 1.7428669168860038, 'equation': 'ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u + f', 'incompressibility': '∇·u = 0', 'noether_current': '∂_μ T^{μν} = 0  (momentum conservation)', 'domain': "Diff(M) — diffeomorphism group (Arnol'd 1966)", '...
```

**`facet_riemann`** — Facet: Riemann Zeta / Berry-Keating (σ=½)
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_riemann', {})['result']
{'facet': 'Riemann Zeta / Berry-Keating', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'riemann_zeros': [14.134725, 21.02204, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073, 48.005151, 49.773832, 52.970321, 56.446247, 59.347044, 60.831779, 65.112544, 67.079811, 69.546402, 72...
```

**`facet_noether`** — Facet: Noether Current (boundary invariant)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_noether', {})['result']
{'facet': 'Noether Current', 'sigma': 'all σ', 'theorem': 'Every continuous symmetry → one conserved current.', 'current_formula': 'J^μ = ∂L / ∂(∂_μφ)', 'conservation': '∂_μ J^μ = 0', 'J_red': 1.0, 'J_blue': -1.5508333333333333, 'J_3': -0.27541666666666664, 'three_phase_balance': -0.8262499999999...
```

**`facet_fermat`** — Facet: Fermat constraint (forbidden zone, σ<½)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_fermat', {})['result']
{'facet': "Fermat's Last Theorem", 'sigma': '< ½  (forbidden zone)', 'theorem': 'No aⁿ + bⁿ = cⁿ for integer a,b,c > 0, n ≥ 3.', 'flt_proof': 'Wiles 1995 — via modularity of elliptic curves (Shimura-Taniyama).', 'h_rb_connection': 'B̂_p poles cannot be rational (Wiles). Therefore the Blue channel...
```

**`dark_matter_halo`** — Dark matter halo — standing gravitational wave resonance
  params: `galaxy_size_ly`  ·  confidence: `THEORETICAL`  ·  signature: `(galaxy_size_ly=50000.0)`
```python
>>> module.run('dark_matter_halo', {})['result']
{'galaxy_size_ly': 50000.0, 'period_yr': 100000.0, 'frequency_per_yr': 1e-05, 'wavelength_ly': 100000.0, 'observation_yr': 500.0, 'ratio_T_to_obs': 200.0, 'appears_static': True, 'halo_is': 'Antinode of Re(ψ) — maximum space compression = maximum apparent mass.', 'dark_matter_is': 'Im(ψ) of the g...
```

**`sigma_rb_baseline`** — SIGMA_RB — Σ_RB at σ=½ (forced by Noether balance)
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('sigma_rb_baseline', {})['result']
{'engine': 'SIGMA_RB', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'forcing_condition': 'R̂† = B̂  (Noether balance forces σ=½)', 'energy_balance': 'E_Red = E_Blue at σ=½ — the reversible engine point', 'action': 'L_(I|O) = e^{-E} at σ=½ — maximum coupling', 'am_gm': 'AM(J_red, J_blue) = GM(...
```

**`precession_stroke`** — Precession stroke — one L_(I|O) cycle = one hat revolution
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('precession_stroke', {})['result']
{'identification': 'Precession revolution = L_(I|O) cycle (one complete I→O→I)', 'half_cycle': 'I→O or O→I alone = one STROKE = half a precession revolution', 'full_cycle': 'I→O→I = one CYCLE = one complete precession revolution', 'linear_component': 'ΔJ = J_red − J_blue  (differential through σ ...
```

**`oblique_crank`** — Oblique crank — arctan(d*) converts stroke to precession
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('oblique_crank', {})['result']
{'identification': 'The Witches Hat half-angle IS the oblique crank throw', 'crank_throw_deg': 13.820339527010455, 'crank_throw_rad': 0.24121042848984825, 'd_star': 0.246, 'sin_theta': 0.23887818716461426, 'cos_theta': 0.9710495413195701, 'effective_torque': 'τ_eff = (J_red + J_blue) × d* / √(1 +...
```

**`trine_configuration`** — Trine — three quantum-force strokes per precession revolution
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('trine_configuration', {})['result']
{'identification': 'Three quantum-force levels = three Wankel faces = trine', 'sigma_levels': [{'sigma': 0.75, 'level': 'ℂ', 'force': 'U(1)', 'name': 'Electromagnetism', 'loss': 'ordering (ℝ→ℂ)'}, {'sigma': 0.5, 'level': 'ℍ', 'force': 'SU(2)', 'name': 'Weak force', 'loss': 'commutativity (ℂ→ℍ)'},...
```

---

### Running via the registry

```python
from ValaQuenta.modules.h_rb_hat.tools import SigmaRBModule

m = SigmaRBModule()
m.formulary()                              # list every Equation this module exposes
m.run('sigma_rb_evaluate', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('sigma_rb_evaluate', {}, 'text')     # -> {'text': '...formatted...'}
```
