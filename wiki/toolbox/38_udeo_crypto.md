# UDEO RSA Key-Recovery — Five Candidate Mechanisms, Honestly Scored

**Module:** `ValaQuenta.modules.udeo_crypto`
**Import:** `from ValaQuenta.modules.udeo_crypto.tools import UDEOCryptoModule`
**Theory page:** *(page pending — see `wiki/00_index.md`)*

---

`udeo_crypto` · v0.100 · confidence floor **OPEN**

Tests five candidate RSA private-key-recovery mechanisms against known toy keys, each scored against a random-guess control (not just reported as working). Includes one proven, ESTABLISHED-tier result (d = e mod 4, classical number theory) and four OPEN/CONJECTURE-tier results from the sedenion/zero-divisor/Zero-Lattice framework, none of which recover d from (n, e) alone.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`compare_all_methods`** — Side-by-side comparison of all five methods vs random-guess controls
  params: `—`  ·  confidence: `OPEN`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('compare_all_methods', {})['result']
{'claim': 'Side-by-side comparison of all five candidate RSA key-recovery mechanisms, each scored against a random-guess control on the same 6 toy keys.', 'baseline_reference': {'claim': 'Reference baseline only (requires full known key) — not an attack.', 'rows': [{'n': 143, 'e': 7, 'd': 103, 'p...
```

**`mod4_identity_theorem`** — d = e (mod 4) always — proven, classical number theory
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('mod4_identity_theorem', {})['result']
{'claim': 'd = e (mod 4) for every RSA key with odd primes p, q. Proven, not statistical.', 'proof': '4 | phi(n) since (p-1) and (q-1) are both even. e*d=1 (mod phi(n)) => e*d=1 (mod 4). (Z/4Z)*={1,3} has exponent 2, so every element is self-inverse, forcing d=e (mod 4).', 'empirical_verification...
```

**`rsa_control_baseline`** — Reference only: sedenion degeneracy given the FULL known key
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('rsa_control_baseline', {})['result']
{'claim': 'Reference baseline only (requires full known key) — not an attack.', 'rows': [{'n': 143, 'e': 7, 'd': 103, 'pq_norm_in_S16': 1.0, 'ed_norm_in_S16': 1.0, 'near_zero_divisor': False}, {'n': 253, 'e': 7, 'd': 63, 'pq_norm_in_S16': 1.0, 'ed_norm_in_S16': 1.0, 'near_zero_divisor': False}, {...
```

**`method1_zero_divisor_shadow`** — Method 1: does d_s align with e_s's near-annihilator direction in S^16?
  params: `—`  ·  confidence: `OPEN`  ·  signature: `(dim: int = 16) -> Dict[str, Any]`
```python
>>> module.run('method1_zero_divisor_shadow', {})['result']
{'claim': "Method 1 (zero-divisor shadow): does d_s align with e_s's near-annihilator direction?", 'per_key': [{'n': 143, 'e': 7, 'd': 103, 'smallest_singular_value': 0.447214, 'exact_zero_divisor': False, 'true_d_alignment': 0.632456, 'control_mean_alignment': 0.122523, 'true_d_percentile_vs_con...
```

**`method2_j2_involution_t256`** — Method 2: J2 asymmetry operator L_{e_s}-R_{e_s} eigenspectrum in T_256
  params: `—`  ·  confidence: `OPEN`  ·  signature: `(dim: int = 256) -> Dict[str, Any]`
```python
>>> module.run('method2_j2_involution_t256', {})['result']
{'claim': 'Method 2 (J2 involution / T_256): does d_s align with a dominant eigenvector of L_{e_s} - R_{e_s}?', 'per_key': [{'n': 143, 'e': 7, 'd': 103, 'asymmetry_operator_norm': 31.874755, 'true_d_alignment': 0.0, 'control_mean_alignment': 0.021868, 'true_d_percentile_vs_controls': 58.62}, {'n'...
```

**`method3_spectral_relativity`** — Method 3: sigma-face metric geodesic distance from e to d
  params: `—`  ·  confidence: `OPEN`  ·  signature: `(dim: int = 16) -> Dict[str, Any]`
```python
>>> module.run('method3_spectral_relativity', {})['result']
{'claim': 'Method 3 (Sedenion Spectral Relativity): is the sigma-metric geodesic to true d an outlier?', 'per_key': [{'n': 143, 'e': 7, 'd': 103, 'sigma_e': 0.001376, 'sigma_n': 0.412718, 'sigma_d_true': 0.406298, 'geodesic_dist_true_d': 2.9234, 'geodesic_dist_control_mean': 1.9588, 'true_d_perce...
```

**`method4_content_public_private_hash`** — Method 4: Content+Public-Hash recovers -Private_s exactly (Hash exposure required)
  params: `—`  ·  confidence: `CONJECTURE`  ·  signature: `(dim: int = 16, search_pool: int = 500) -> Dict[str, Any]`
```python
>>> module.run('method4_content_public_private_hash', {})['result']
{'claim': 'Method 4 (Content+Public+Private=Hash): does subtracting Hash recover d by search-matching against its embedding?', 'per_key': [{'n': 143, 'e': 7, 'd': 103, 'true_d_distance_to_recovered_vector': 0.0, 'control_mean_distance': 1.289079, 'true_d_is_closest_match_in_pool': True, 'exact_ha...
```

**`method5_zero_lattice_paths`** — Method 5: trace Content/Public/Private/Hash through the 9-level CD tower
  params: `—`  ·  confidence: `OPEN`  ·  signature: `(search_pool: int = 200) -> Dict[str, Any]`
```python
>>> module.run('method5_zero_lattice_paths', {})['result']
{'claim': 'Method 5 (Zero Lattice paths): trace Content/Public/Private/Hash through the 9-level CD tower; test both the Hash-exposed and public-key-only scenarios.', 'per_key': [{'n': 143, 'e': 7, 'd': 103, 'hash_n_plus_e_plus_d': 253, 'content_path': {'label': 'Content (n)', 'value': 143, 'nshap...
```

---

### Running via the registry

```python
from ValaQuenta.modules.udeo_crypto.tools import UDEOCryptoModule

m = UDEOCryptoModule()
m.formulary()                              # list every Equation this module exposes
m.run('compare_all_methods', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('compare_all_methods', {}, 'text')     # -> {'text': '...formatted...'}
```
