# Tier 0 Constants — π φ e √ i derived from H_RB

> d* faces (all four are needed to chart ln(10) in Universal Native Space):  
>   d*         = 0.24600          the value the code runs with (Boundary, σ_ζ=½ plane)  
>   d*_taut    = 0.246307201473  A_π/ln10, the Flow (radial unit)  
>   d*_RG      = dimension 8; numeric OPEN, no closed form  the Stability (centre r=0)  
>   d*_ln(10)  = 0.5671432904   d*_taut·ln10 = A_π, the Translator (log bridge)  
> Full story of d*: Ainulindale/wiki/17_alpha_omega_d_star.md; ~/.clauderc_canonical_maths @RCCM_FOUR_DSTAR; FourthAgePapers/DStarRG  


**Module:** `ValaQuenta.modules.constants`
**Import:** `from ValaQuenta.modules.constants.tools import ConstantsModule`
**Theory page:** [constants.md](../constants.md)

---

`constants` · v0.130 · confidence floor **THEORETICAL**

Tier 0 Root Constants: π, φ, e, √, i, A_PI, α_F, d*, Λ — each read at a σ-facet of Ĥ_RB. Two ceilings bound the domain [α_F, A_PI]. d* has four named faces (Boundary, Flow, Stability, Translator). Λ: J_neg at cosmological scale; Sombrero = Hawking pair; A_PI = de Sitter attractor. Einstein wrote it in 1915, removed it 1917, universe re-inserted 1998 at 40σ.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`derive_lambda`** — Λ — Einstein cosmological constant: J_neg at cosmological scale
  params: —  ·  confidence: `OPEN`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_lambda', {})['result']
{'constant': 'Λ  (Einstein cosmological constant)', 'value_omega_lambda': 0.6889, 'sigma_facet': 'σ=∞ (existence); σ≈2 (numerical value)', 'physical_layer': 'J_neg at cos ...
```

**`all_constants`** — All 9 constants — Tier 0: π φ e √ i Ω_ζΣ α_F d* Λ
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('all_constants', {})['result']
{'tier': 'Tier 0 — Root Constants + Ceilings + Domain + Λ', 'claim': 'Root constants and domain boundaries, each read at its σ-facet of Ĥ_RB (programme reading THEORETICA ...
```

**`derive_i`** — i — Cayley-Dickson closure: x²+1=0  [σ=i, democratic facet]
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_i', {})['result']
{'constant': 'i  (imaginary unit)', 'sigma_facet': 'σ = i  (pure phase — democratic)', 'physical_layer': 'Quantum / Phase — wavefunction, interference', 'algebraic_origin ...
```

**`derive_sqrt`** — √ — σ=½ IS the square root: G_p(½)=1/√p  [critical line]
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_sqrt', {})['result']
{'constant': '√  (square root)', 'sigma_facet': 'σ = ½  (the critical line IS the square root line)', 'physical_layer': 'Wave-particle boundary — amplitude envelope of sp ...
```

**`derive_e`** — e — Berry-Keating canonical: ẋ=x → x(t)=e^t  [σ=e, thermodynamic]
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_e', {})['result']
{'constant': "e  (Euler's number)", 'sigma_facet': 'σ = e  (thermodynamic — Boltzmann partition)', 'physical_layer': 'Thermodynamic — entropy, partition functions, Boltzm ...
```

**`derive_pi`** — π — U(1) normalisation (2/π)·π=2 AND Basel ζ(2)=π²/6  [σ=π, gauge]
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_pi', {})['result']
{'constant': 'π  (circle constant)', 'sigma_facet': 'σ = π  (gauge normalisation — U(1) layer)', 'physical_layer': 'U(1) gauge symmetry — phase winding, angular momentum' ...
```

**`derive_phi`** — φ — CD recursion eigenvalue f(x)=1+1/x  [σ=φ, structural]
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_phi', {})['result']
{'constant': 'φ  (golden ratio)', 'sigma_facet': 'σ = φ  (recursion eigenvalue — structural backbone)', 'physical_layer': 'Recursion / Self-similarity — quasicrystal, phy ...
```

**`euler_identity`** — e^{iπ}+1=0 — theorem of H_RB, not a definition
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('euler_identity', {})['result']
{'identity': 'e^{iπ} + 1 = 0', 'type': 'Theorem of complex analysis; its reading as the J_R+J_G+J_B=0 conservation is THEORETICAL', 'assembly': {'e': 'BK canonical equati ...
```

**`derive_omega_zs`** — A_π = W(1) — thermal information ceiling T·e^T=1
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_omega_zs', {})['result']
{'constant': 'A_PI  (A_π)', 'value': 0.5671432904097838, 'sigma_facet': 'Domain ceiling — prime distribution entropy bound', 'physical_layer': 'Thermodynamic ceiling — se ...
```

**`derive_alpha_fermat`** — α_F = 1/137... — causality ceiling v_1=α·c<c
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_alpha_fermat', {})['result']
{'constant': 'α_F  (α / fine structure constant)', 'value': 0.0072973525692838015, 'inverse': 137.035999, 'sigma_facet': 'BK domain floor — minimum coupling, causality fl ...
```

**`derive_d_star`** — d* — four faces: Boundary 0.24600, Flow A_π/ln10, Stability (dim 8, OPEN), Translator A_π
  params: —  ·  confidence: `OPEN`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('derive_d_star', {})['result']
{'constant': 'd*  (four faces)', 'value_real': 0.246, 'sigma_facet': 'σ_ζ=½ plane (Boundary); radial unit (Flow); centre r=0 (Stability); log bridge (Translator)', 'proce ...
```


---

*Theory page: [`constants.md`](../constants.md).*
