# Tier 0 Constants — π φ e √ i derived from H_RB

**Module:** `ValaQuenta.modules.constants`
**Import:** `from ValaQuenta.modules.constants.tools import ConstantsModule`
**Theory page:** [`../constants.md`](../constants.md)

---

`constants` · v0.120 · confidence floor **ESTABLISHED**

Tier 0 Root Constants: π, φ, e, √, i, OMEGA_ZS, α_F, d*, Λ — all drop out of H_RB algebraic structure. Two ceilings force domain [α_F, OMEGA_ZS]. d* has 4 values (tower→ln(10) Open Prob 2). Λ: J_neg at cosmological scale; Sombrero = Hawking pair; OMEGA_ZS = de Sitter attractor. Einstein wrote it in 1915, removed it 1917, universe re-inserted 1998 at 40σ.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`derive_lambda`** — Λ — Einstein cosmological constant: J_neg at cosmological scale
  params: `—`  ·  confidence: `σ=∞ (existence); σ>40 (Nobel 1998); OPEN (value from f)`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_lambda', {})['result']
{'constant': 'Λ  (Einstein cosmological constant)', 'value_omega_lambda': 0.6889, 'sigma_facet': 'σ=∞ (existence); σ≈2 (numerical value)', 'physical_layer': 'J_neg at cosmological scale — vacuum self-energy', 'algebraic_origin': 'Three-phase balance J_R+J_G+J_B=0 must have Blue (J_neg) term', 'on...
```

**`all_constants`** — All 9 constants — Tier 0: π φ e √ i Ω_ζΣ α_F d* Λ
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('all_constants', {})['result']
{'tier': 'Tier 0 — Root Constants + Ceilings + Domain + Λ', 'claim': 'All root constants and domain boundaries drop out of H_RB structure.', 'table': [{'constant': 'i', 'sigma': 'i', 'origin': 'CD closure x²+1=0', 'physical': 'Quantum/Phase', 'verified': True}, {'constant': '√', 'sigma': '½', 'or...
```

**`derive_i`** — i — Cayley-Dickson closure: x²+1=0  [σ=i, democratic facet]
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_i', {})['result']
{'constant': 'i  (imaginary unit)', 'sigma_facet': 'σ = i  (pure phase — democratic)', 'physical_layer': 'Quantum / Phase — wavefunction, interference', 'algebraic_origin': 'Cayley-Dickson first doubling: (ℝ,ℝ) → ℂ', 'closure_condition': 'x² + 1 = 0  — no real solution; CD element (0,1) solves it...
```

**`derive_sqrt`** — √ — σ=½ IS the square root: G_p(½)=1/√p  [critical line]
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_sqrt', {})['result']
{'constant': '√  (square root)', 'sigma_facet': 'σ = ½  (the critical line IS the square root line)', 'physical_layer': 'Wave-particle boundary — amplitude envelope of spectral oscillations', 'algebraic_origin': 'G_p(½) = p^{−½} = 1/√p; CD norm condition; geometric mean σ=0 and σ=1', 'derivation_...
```

**`derive_e`** — e — Berry-Keating canonical: ẋ=x → x(t)=e^t  [σ=e, thermodynamic]
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_e', {})['result']
{'constant': "e  (Euler's number)", 'sigma_facet': 'σ = e  (thermodynamic — Boltzmann partition)', 'physical_layer': 'Thermodynamic — entropy, partition functions, Boltzmann weights', 'algebraic_origin': 'Berry-Keating canonical equations: ẋ = x → x(t) = x₀·e^t', 'derivation_chain': ['1. BK Lagra...
```

**`derive_pi`** — π — U(1) normalisation (2/π)·π=2 AND Basel ζ(2)=π²/6  [σ=π, gauge]
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_pi', {})['result']
{'constant': 'π  (circle constant)', 'sigma_facet': 'σ = π  (gauge normalisation — U(1) layer)', 'physical_layer': 'U(1) gauge symmetry — phase winding, angular momentum', 'algebraic_origin': 'U(1) normalisation (2/π)·π=2 AND Basel ζ(2)=π²/6 from primes', 'derivation_chain': ['1. SMMIP Lagrangian...
```

**`derive_phi`** — φ — CD recursion eigenvalue f(x)=1+1/x  [σ=φ, structural]
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_phi', {})['result']
{'constant': 'φ  (golden ratio)', 'sigma_facet': 'σ = φ  (recursion eigenvalue — structural backbone)', 'physical_layer': 'Recursion / Self-similarity — quasicrystal, phyllotaxis, Fibonacci', 'algebraic_origin': 'CD recursion f(x)=1+1/x fixed point: x²=x+1, x=(1+√5)/2', 'derivation_chain': ['1. C...
```

**`euler_identity`** — e^{iπ}+1=0 — theorem of H_RB, not a definition
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('euler_identity', {})['result']
{'identity': 'e^{iπ} + 1 = 0', 'type': 'Theorem of RedBlue Geometries Engine', 'assembly': {'e': 'BK canonical equations: ẋ=x → x(t)=e^t', 'i': 'CD first doubling: x²+1=0', 'π': 'U(1) normalisation (2/π)·π=2 and Basel ζ(2)=π²/6', 'φ': 'Structural backbone (CD recursion eigenvalue) — not a channel...
```

**`derive_omega_zs`** — Ω_ζΣ = W(1) — thermal information ceiling T·e^T=1
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_omega_zs', {})['result']
{'constant': 'OMEGA_ZS  (Ω_ζΣ)', 'value': 0.5671432904097838, 'sigma_facet': 'Domain ceiling — prime distribution entropy bound', 'physical_layer': 'Thermodynamic ceiling — self-referential system equilibrium', 'algebraic_origin': 'T·e^T = 1  (self-referential Boltzmann fixed point)', 'derivation...
```

**`derive_alpha_fermat`** — α_F = 1/137... — causality ceiling v_1=α·c<c
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_alpha_fermat', {})['result']
{'constant': 'α_F  (Alpha_Fermat / fine structure constant)', 'value': 0.0072973525692838015, 'inverse': 137.035999, 'sigma_facet': 'BK domain floor — minimum coupling, causality floor', 'physical_layer': 'Electromagnetic / Causality — inertia floor', 'algebraic_origin': 'v_1 = α·c < c  (Bohr vel...
```

**`derive_d_star`** — d* — 4 values: BK spectral floor, gap=0.000707, tower→ln(10) [OPEN]
  params: `—`  ·  confidence: `ESTABLISHED (d*_R); OPEN (full tower)`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_d_star', {})['result']
{'constant': 'd*  (BK spectral floor, 4 components)', 'value_real': 0.246, 'sigma_facet': 'Spectral floor of H_BK on [α_F, OMEGA_ZS]', 'physical_layer': 'BK operator domain — spectral coordinate', 'algebraic_origin': 'Berry-Keating spectral floor; 4 CD strata', 'derivation_chain': ['1. BK operato...
```

---

### Running via the registry

```python
from ValaQuenta.modules.constants.tools import ConstantsModule

m = ConstantsModule()
m.formulary()                              # list every Equation this module exposes
m.run('derive_lambda', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('derive_lambda', {}, 'text')     # -> {'text': '...formatted...'}
```
