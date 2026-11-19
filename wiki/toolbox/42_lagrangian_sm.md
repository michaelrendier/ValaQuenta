# L_SM: the Standard Model Lagrangian

**Module:** `ValaQuenta.modules.lagrangian_sm`
**Import:** `from ValaQuenta.modules.lagrangian_sm.tools import LagrangianSMModule`
**Theory page:** [lagrangian_sm.md](../lagrangian_sm.md)

---

`lagrangian_sm` · v0.1 · confidence floor **ESTABLISHED**

The Standard Model of particle physics as an engine: field content and gauge quantum numbers, anomaly cancellation, SU(2) and SU(3) structure constants, the symbolic derivation of the electroweak boson masses and the Higgs potential expansion, the count of independent parameters (19, 26, 28), tree-level relations against the PDG tables, CKM and PMNS mixing, Z couplings, one-loop running and the failure of gauge coupling unification, and a measured comparison of L_SM with the VAPMIP L_NN and with L_(I|O).

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify`** — VERIFY: closure checks
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify', {})['result']
{'anomalies_cancel': True, 'su2_closure': 0.0, 'su3_closure': 1.1102230246251565e-16, 'su3_jacobi': np.float64(3.3306690738754696e-16), 'boson_masses_match': True, 'param ...
```

**`fields`** — FIELDS: content and degrees of freedom
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('fields', {})['result']
{'content': [{'name': 'Q_L', 'su3': 3, 'su2': 2, 'Y': Fraction(1, 6), 'chirality': 'L', 'generations': 3}, {'name': 'u_R', 'su3': 3, 'su2': 1, 'Y': Fraction(2, 3), 'chira ...
```

**`anomalies`** — ANOMALIES: why this content is consistent
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('anomalies', {})['result']
{'U1^3': Fraction(0, 1), 'SU3^2 U1': Fraction(0, 1), 'SU2^2 U1': Fraction(0, 1), 'grav^2 U1': Fraction(0, 1), 'witten_doublets_per_generation': 4, 'witten_ok': True, 'all ...
```

**`hypercharges`** — HYPERCHARGES: derived, not measured
  params: `n_colours`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_colours=3)`
```python
>>> module.run('hypercharges', {})['result']
{'solutions': [{'Y_Q': Fraction(1, 6), 'Y_L': Fraction(-1, 2), 'Y_u': Fraction(2, 3), 'Y_d': Fraction(-1, 3), 'Y_e': Fraction(-1, 1)}], 'unique': True, 'sm': {'Y_Q': Frac ...
```

**`su5`** — SU(5) EMBEDDING: where the anomaly cancellation comes from
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('su5', {})['result']
{'Y_5bar': [Fraction(-1, 2), Fraction(-1, 2), Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)], 'Y_10': [Fraction(-2, 3), Fraction(-2, 3), Fraction(-2, 3), Fraction(1, 6), ...
```

**`groups`** — GROUPS: SU(2), SU(3) structure constants
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('groups', {})['result']
{'SU2': {'generators': 3, 'closure_residual': 0.0, 'jacobi_residual': 0.0, 'casimir_residual': 0.0, 'nonzero_f': 6}, 'SU3': {'generators': 8, 'closure_residual': 1.110223 ...
```

**`parameters`** — PARAMETERS: how many numbers L_SM has
  params: `neutrinos`  ·  confidence: `ESTABLISHED`  ·  signature: `(neutrinos='massless')`
```python
>>> module.run('parameters', {})['result']
{'neutrinos': 'massless', 'gauge_couplings': 3, 'higgs': 2, 'theta_QCD': 1, 'yukawa_real': 54, 'flavour_generators': 45, 'unbroken_generators': 4, 'flavour_physical': 13, ...
```

**`ew_symbolic`** — ELECTROWEAK MASSES, derived
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('ew_symbolic', {})['result']
{'quadratic_form': 'v**2*(g**2*(W1 - I*W2)*(W1 + I*W2) + (B*gp - W3*g)**2)/8', 'm_W2': 'g**2*v**2/4', 'm_Z2': 'v**2*(g**2 + gp**2)/4', 'm_photon2': '0'}
```

**`higgs_symbolic`** — HIGGS POTENTIAL, expanded
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('higgs_symbolic', {})['result']
{'m_h2': '2*lam*v**2', 'coefficients': {0: '-lam*v**4/4', 1: '0', 2: 'lam*v**2', 3: 'lam*v', 4: 'lam/4'}}
```

**`higgs`** — HIGGS SECTOR: numbers
  params: `m_h`, `v`  ·  confidence: `ESTABLISHED`  ·  signature: `(m_h=None, v=None)`
```python
>>> module.run('higgs', {})['result']
{'m_h': 125.13, 'v': 246.21964023926205, 'lam': 0.12913605313016874, 'mu2': 7828.758449999999, 'depth_GeV4': 118652880.78509493, 'trilinear': 31.79583254362838, 'quartic' ...
```

**`ew_tree`** — ELECTROWEAK TREE LEVEL
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('ew_tree', {})['result']
{'e': 0.31338852459296573, 'g': 0.6517340199093395, 'gp': 0.3574226344275484, 'm_W_tree': 80.23485795688282, 'm_Z_tree': 91.50862923623751, 'rho_tree': 1.0, 'm_W_pdg': 80 ...
```

**`yukawas`** — YUKAWA COUPLINGS
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('yukawas', {})['result']
{'u': 1.2406407920007937e-05, 'd': 2.699542464075801e-05, 's': 0.0005335904147077488, 'c': 0.007311739482486158, 'b': 0.02404315905238575, 't': 0.9913638921265601, 'e': 2 ...
```

**`ckm`** — CKM and PMNS
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('ckm', {})['result']
{'CKM_J': 3.1169935287554706e-05, 'CKM_unitarity': 1.1102230246251565e-16, 'PMNS_J': -0.009793886924193728}
```

**`zcouplings`** — Z COUPLINGS
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('zcouplings', {})['result']
{'nu': {'T3': 0.5, 'Q': 0.0, 'g_L': 0.5, 'g_R': -0.0, 'g_V': 0.5, 'g_A': 0.5}, 'e': {'T3': -0.5, 'Q': -1.0, 'g_L': -0.26878, 'g_R': 0.23122, 'g_V': -0.03755999999999998,  ...
```

**`vertices`** — VERTEX INVENTORY
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('vertices', {})['result']
{'bosonic_electroweak': 12, 'bosonic_qcd': 2, 'photon_fermion': 9, 'Z_fermion': 12, 'W_lepton': 3, 'W_quark_CKM_entries': 9, 'Higgs_fermion': 9, 'gluon_quark_flavours': 6 ...
```

**`running`** — RUNNING and the failure to unify
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('running', {})['result']
{'mu_12': 10308964978996.443, 'mu_23': 9.710475730988976e+16, 'mu_13': 243011179441012.12, 'log10_spread': 3.974025442909511}
```

**`compare`** — COMPARE: L_SM, L_NN, L_(I|O), L_dynamic
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('compare', {})['result']
[{'name': 'L_SM', 'role': 'the measured theory of the fundamental interactions', 'form': 'L_gauge + L_fermion + L_Higgs + L_Yukawa', 'gauge_group': 'SU(3)×SU(2)×U(1), non ...
```

**`exponents`** — COMPARE: degree of each term
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('exponents', {})['result']
{'gauge kinetic': {'SM': {'A': 4.0}, 'NN': {'A': 2.0}}, 'matter (fermion-gauge)': {'SM': {'psi': 2.0, 'A': 1.0}, 'NN': {'psi': 2.0, 'A': 2.0}}, 'bias / Higgs potential':  ...
```

**`hat`** — THE HAT, for the path-of-action tools
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('hat', {})['result']
{'model': 'standard_model', 'mu2': 7828.758449999999, 'lam': 0.12913605313016874, 'brim_radius': 246.21964023926205, 'depth': 118652880.78509493, 'm_over_v': 0.5082047877 ...
```

### Shell commands

`sm_verify` · `sm_fields` · `sm_anomalies` · `sm_groups` · `sm_parameters` · `sm_higgs` · `sm_ew_tree` · `sm_yukawas` · `sm_ckm` · `sm_running` · `sm_compare` · `sm_exponents` · `sm_hat`


---

*Theory page: [`lagrangian_sm.md`](../lagrangian_sm.md).*
