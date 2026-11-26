# Σ_RB  RedBlue Summed Integral

> d* faces (all four are needed to chart ln(10) in Universal Native Space):  
>   d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)  
>   d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)  
>   d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)  
>   d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)  
> Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG  


**Module:** `ValaQuenta.modules.h_rb_hat`
**Import:** `from ValaQuenta.modules.h_rb_hat.tools import SigmaRBModule`
**Theory page:** [h_rb_hat.md](../h_rb_hat.md)

---

`h_rb_hat` · v0.120 · confidence floor **THEORETICAL**

Σ_RB = Σ_p p^{-σ} [R̂_p ⊗ ∂̂_∂M + ∂̂_∂M† ⊗ B̂_p]. The RedBlue Summed Integral. The Boundary Generator. The Σ is the summation sign. The RB is Red-Blue. The existence of a distinction. Facet projections: GR (σ=2), Yang-Mills (σ=1), QM/RH (σ=½), NS (σ=1, Im=0), Noether (boundary invariant), Fermat (forbidden zone). All six open Clay Millennium Problems project from this operator.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`sigma_rb_evaluate`** — Σ_RB — RedBlue Summed Integral at (σ, x, p)
  params: `sigma`, `x`, `p_momentum`, `n_primes`  ·  confidence: `THEORETICAL`  ·  signature: `(sigma=0.5, x=1.0, p_momentum=1.0, n_primes=20)`
```python
>>> module.run('sigma_rb_evaluate', {})['result']
{'sigma': 0.5, 'x': 1.0, 'p_momentum': 1.0, 'n_primes': 20, 'terms': [{'prime': 2, 'sigma': 0.5, 'G_p': 0.7071067811865476, 'E_red': 1.0, 'E_blue': 1.5508333333333333, 'b ...
```

**`self_adjoint_demonstration`** — Self-adjointness: 1=1 is adjoint to 1!=1
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('self_adjoint_demonstration', {})['result']
{'statement': 'Self-adjointness preserves truth, not form.', '1_equals_1': 1, '1_factorial': 1, 'adjoint_check': True, 'n2_identity': 2, 'n2_factorial': 2, 'n3_identity': ...
```

**`sigma_phase_diagram`** — σ phase diagram — which σ → which theory
  params: `n_points`  ·  confidence: `THEORETICAL`  ·  signature: `(n_points=20)`
```python
>>> module.run('sigma_phase_diagram', {})['result']
{'diagram': [{'sigma': 0.0, 'theory': 'Trivial / Poincaré', 'euler_mag': 1.0, 'euler_re': 1.0, 'converges': False, 'critical_line': False}, {'sigma': 0.1316, 'theory': 'F ...
```

**`euler_product`** — Euler product ζ(s) = Π_p (1−p^{−s})^{−1}
  params: `sigma`, `t`, `n_primes`  ·  confidence: `ESTABLISHED`  ·  signature: `(sigma=0.5, t=0.0, n_primes=20)`
```python
>>> module.run('euler_product', {})['result']
{'result': (583.7119433744068+0j), 'magnitude': 583.7119433744068}
```

**`facet_gr`** — Facet: General Relativity (σ=2)
  params: `kappa`  ·  confidence: `ESTABLISHED`  ·  signature: `(kappa=1.0)`
```python
>>> module.run('facet_gr', {})['result']
{'facet': 'General Relativity', 'sigma': 2.0, 'coupling_sum': 0.4497032182086859, 'action': 'S_EH = (c⁴/16πG) ∫ R √{-g} d⁴x', 'field_equation': 'G_μν + Λg_μν = (8πG/c⁴) T ...
```

**`facet_yang_mills`** — Facet: Yang-Mills / Standard Model (σ=1)
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_yang_mills', {})['result']
{'facet': 'Yang-Mills / Standard Model', 'sigma': 1.0, 'coupling_sum': 1.7428669168860038, 'G_per_prime': [(2, 0.5), (3, 0.3333333333333333), (5, 0.2), (7, 0.142857142857 ...
```

**`facet_qm`** — Facet: Quantum Mechanics (σ=½)
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_qm', {})['result']
{'facet': 'Quantum Mechanics', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'equation': 'iħ ∂|ψ⟩/∂t = H|ψ⟩', 'time_independent': 'H|ψ_n⟩ = E_n|ψ_n⟩', 'noether_current ...
```

**`facet_navier_stokes`** — Facet: Navier-Stokes (σ=1, Im=0) — lacks i
  params: `galaxy_size_ly`  ·  confidence: `THEORETICAL`  ·  signature: `(galaxy_size_ly=50000.0)`
```python
>>> module.run('facet_navier_stokes', {})['result']
{'facet': 'Navier-Stokes', 'sigma': 1.0, 'imaginary': 0.0, 'coupling_sum': 1.7428669168860038, 'equation': 'ρ(∂u/∂t + u·∇u) = −∇p + μ∇²u + f', 'incompressibility': '∇·u = ...
```

**`facet_riemann`** — Facet: Riemann Zeta / Berry-Keating (σ=½)
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_riemann', {})['result']
{'facet': 'Riemann Zeta / Berry-Keating', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'riemann_zeros': [14.134725, 21.02204, 25.010858, 30.424876, 32.935062, 37.5861 ...
```

**`facet_noether`** — Facet: Noether Current (boundary invariant)
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_noether', {})['result']
{'facet': 'Noether Current', 'sigma': 'all σ', 'theorem': 'Every continuous symmetry → one conserved current.', 'current_formula': 'J^μ = ∂L / ∂(∂_μφ)', 'conservation': ' ...
```

**`facet_fermat`** — Facet: Fermat constraint (forbidden zone, σ<½)
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('facet_fermat', {})['result']
{'facet': "Fermat's Last Theorem", 'sigma': '< ½  (forbidden zone)', 'theorem': 'No aⁿ + bⁿ = cⁿ for integer a,b,c > 0, n ≥ 3.', 'flt_proof': 'Wiles 1995 — via modularity ...
```

**`dark_matter_halo`** — Dark matter halo — standing gravitational wave resonance
  params: `galaxy_size_ly`  ·  confidence: `THEORETICAL`  ·  signature: `(galaxy_size_ly=50000.0)`
```python
>>> module.run('dark_matter_halo', {})['result']
{'galaxy_size_ly': 50000.0, 'period_yr': 100000.0, 'frequency_per_yr': 1e-05, 'wavelength_ly': 100000.0, 'observation_yr': 500.0, 'ratio_T_to_obs': 200.0, 'appears_static ...
```

**`sigma_rb_baseline`** — SIGMA_RB — Σ_RB at σ=½ (forced by Noether balance)
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('sigma_rb_baseline', {})['result']
{'engine': 'SIGMA_RB', 'sigma': 0.5, 'coupling_sum': 4.989633250806095, 'forcing_condition': 'R̂† = B̂  (Noether balance forces σ=½)', 'energy_balance': 'E_Red = E_Blue a ...
```

**`precession_stroke`** — Precession stroke — one L_(I|O) cycle = one hat revolution
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('precession_stroke', {})['result']
{'identification': 'Precession revolution = L_(I|O) cycle (one complete I→O→I)', 'half_cycle': 'I→O or O→I alone = one STROKE = half a precession revolution', 'full_cycle ...
```

**`oblique_crank`** — Oblique crank — arctan(d*) converts stroke to precession
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('oblique_crank', {})['result']
{'identification': 'The Witches Hat half-angle IS the oblique crank throw', 'crank_throw_deg': 13.820339527010455, 'crank_throw_rad': 0.24121042848984825, 'd_star': 0.246 ...
```

**`trine_configuration`** — Trine — three quantum-force strokes per precession revolution
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('trine_configuration', {})['result']
{'identification': 'Three quantum-force levels = three Wankel faces = trine', 'sigma_levels': [{'sigma': 0.75, 'level': 'ℂ', 'force': 'U(1)', 'name': 'Electromagnetism',  ...
```


---

*Theory page: [`h_rb_hat.md`](../h_rb_hat.md).*
