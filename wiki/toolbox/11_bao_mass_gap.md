# The Mass Gap — spectral residue of BAO

**Module:** `ValaQuenta.modules.bao_mass_gap`
**Import:** `from ValaQuenta.modules.bao_mass_gap.tools import BaoMassGapModule`
**Theory page:** [`../bao_mass_gap.md`](../bao_mass_gap.md)

---

`bao_mass_gap` · v0.131 · confidence floor **ESTABLISHED**

The mass gap as the residue of the BAO spectral decomposition. The explicit formula splits the prime distribution into a de Sitter ground state plus one standing wave per zero; read at the BAO scale that is the CMB acoustic spectrum. What no standing wave absorbs between the acoustic floor D*·ln10 and the thermal ceiling Ω_ζΣ is the residue: Δ = 0.0007073575 = 1/(1000√2). Zero free parameters. Δ is consumed across the codebase as the compactification scale and spectral floor; this module is where it is computed.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`summary`** — Mass gap — Δ = 0.0007073575 = 1/(1000√2)  [headline]
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('summary', {})['result']
{'title': 'The Mass Gap — spectral residue of BAO', 'headline': 0.000707357533248576, 'derivation': ['Ceiling  Ω_ζΣ       = 0.5671432904   thermal information bound', 'Floor    D*·ln10    = 0.5664359329   BAO acoustic ground state', 'Residue  Δ          = 0.0007073575   absorbed by no standing wa...
```

**`gap_value`** — Δ = Ω_ζΣ − D*·ln(10) — two constants, one subtraction
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('gap_value', {})['result']
{'formula': 'Δ = Ω_ζΣ − D*·ln(10)', 'derivation': ['Take Ω_ζΣ = W(1) = 0.5671432904 — the thermal information ceiling.', 'Take D* = 0.246 — the spectral ground state of the recursion attractor.', 'Convert the ground state to information units: D*·ln(10) = 0.5664359329.', 'Subtract floor from ceil...
```

**`spectral_residue`** — Spectral residue of BAO — why the gap IS a residue
  params: `n_zeros`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_zeros: int = 20) -> Dict[str, Any]`
```python
>>> module.run('spectral_residue', {})['result']
{'explicit_formula': 'ψ(x) = x − Σ_ρ x^ρ/ρ − ln(2π) − ½ln(1−x⁻²)', 'derivation': ['Write the explicit formula: ψ(x) = x − Σ_ρ x^ρ/ρ − ln(2π) − ½ln(1−x⁻²).', 'The x term is the de Sitter expansion — the acoustic ground state.', 'Σ_ρ x^ρ/ρ is the acoustic oscillations, one standing wave per zero γ_...
```

**`gap_identity`** — Δ = 1/(1000√2) — the Red/Blue symmetry point
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('gap_identity', {})['result']
{'formula': 'Δ = 1/(1000·√2) = 1/√(2×10⁶)', 'derivation': ['Compute Δ from the two constants: Δ = 0.000707357533.', 'Compute the closed form: 1/(1000√2) = 0.000707106781.', 'Residual: |Δ − 1/(1000√2)| = 2.508e-07  (0.0354%).', 'Invert for the D* that makes it exact: D* = 0.2460001089.', 'Carried ...
```

**`bao_consistency`** — Δ vs Planck 2018 r_s = 147.09 ± 0.26 Mpc — resolvable
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('bao_consistency', {})['result']
{'derivation': ['Take Planck 2018 r_s = 147.09 ± 0.26 Mpc.', 'Fractional precision: 0.26/147.09 = 0.00176763 (0.177%).', 'Compare: Δ/σ_BAO = 0.00070736/0.00176763 = 0.400174.', '0.4002 > 0.1 — above the noise floor.', 'Δ is a resolvable feature of the acoustic spectrum.'], 'r_s_mpc': 147.09, 'r_s...
```

**`mtheory_compactification`** — Compactification scale = Δ — 11 = 4+7, G₂ holonomy, one vacuum
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('mtheory_compactification', {})['result']
{'derivation': ['M-theory runs on 11 dimensions.', 'Split: 4 observable + 7 compact.', 'Check the count exactly: 11 − 4 = 7 = 7 imaginary octonion units.', 'G₂ = Aut(𝕆), the automorphism group of the octonions.', 'The 7 compact directions are e₁..e₇ — algebraic units, never spatial.', 'The compac...
```

**`validate`** — Validation — all 7 checks
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('validate', {})['result']
{'derivation': ['Run gap_value(): Δ > 0 and in range.', 'Run gap_identity(): Δ = 1/(1000√2), D* pinned inside its last digit.', 'Run spectral_residue(): the BAO residue reproduces Δ exactly.', 'Run bao_consistency(): Δ resolvable against Planck 2018.', 'Run mtheory_compactification(): 4 + 7 = 11 ...
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`gap`, `identity`, `residue`, `validate`

---

### Running via the registry

```python
from ValaQuenta.modules.bao_mass_gap.tools import BaoMassGapModule

m = BaoMassGapModule()
m.formulary()                              # list every Equation this module exposes
m.run('summary', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('summary', {}, 'text')     # -> {'text': '...formatted...'}
```
