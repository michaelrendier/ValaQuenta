# Hypergon Constructibility — Gauss-Wantzel + Factorization Test

**Module:** `ValaQuenta.modules.hypergon_constructibility`
**Import:** `from ValaQuenta.modules.hypergon_constructibility.tools import HypergonConstructibilityModule`
**Theory page:** [hypergon_constructibility.md](../hypergon_constructibility.md)

---

`hypergon_constructibility` · v0.200 · confidence floor **OPEN**

All 16 sedenion hyper-N-gons tested for Gauss-Wantzel constructibility (REAL result: 4/16 constructible, 12/16 holes). Phase 22's corrected nilpotent-split factorization conjecture re-tested against a magnitude-matched control (HONEST result: does not survive — likely address-mapping artifact, not a real factoring signal). Dual arithmetic/geometric prime definition, NOT unified into a working factoring mechanism.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`sedenion_hypergon_sweep`** — All 16 N-gons — Gauss-Wantzel constructibility, verified not assumed
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('sedenion_hypergon_sweep', {})['result']
{'rows': [{'channel': 'e0', 'prime': 2, 'fermat_prime': False, 'power_of_2': True, 'constructible': True}, {'channel': 'e1', 'prime': 3, 'fermat_prime': True, 'power_of_2 ...
```

**`verify_nilpotent_split_conjecture`** — Re-test: does p,q nilpotency survive a magnitude-matched control?
  params: —  ·  confidence: `OPEN`  ·  signature: `(seed: int = 20260711) -> Dict[str, Any]`
```python
>>> module.run('verify_nilpotent_split_conjecture', {})['result']
{'close_prime_pairs': {'n': 110, 'p_pct': 69.0909090909091, 'q_pct': 76.36363636363636, 'both_pct': 52.72727272727273}, 'far_apart_prime_pairs': {'n': 97, 'p_pct': 47.422 ...
```

**`prime_definition_report`** — Dual definition of prime — arithmetic + geometric, not yet unified
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('prime_definition_report', {})['result']
{'arithmetic_definition': "A prime has no non-trivial factorization — a<1<a<p with a*b=p impossible for 1<a,b<p. This is why AbrikosovTree's CD-tower structure has primes ...
```

**`niemeier_gap_theorem`** — The Niemeier gap: h mod 16 of the 23 Niemeier root systems misses {1, 11, 15}
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `(rank: int = 24, modulus: int = 16) -> Dict[str, Any]`
```python
>>> module.run('niemeier_gap_theorem', {})['result']
{'root_systems': [{'h': 2, 'multiplicities': {'A1': 24}, 'label': 'A1^24'}, {'h': 3, 'multiplicities': {'A2': 12}, 'label': 'A2^12'}, {'h': 4, 'multiplicities': {'A3': 8} ...
```

**`moonshine_gap_fill`** — Moonshine primes modulo 16: which residues they reach
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `(modulus: int = 16) -> Dict[str, Any]`
```python
>>> module.run('moonshine_gap_fill', {})['result']
{'by_residue': {1: [17], 2: [2], 3: [3, 19], 5: [5], 7: [7, 23, 71], 9: [41], 11: [11, 59], 13: [13, 29], 15: [31, 47]}, 'gap': [1, 11, 15], 'gap_filled': [1, 11, 15], 'o ...
```

**`moonshine_fill_control`** — Control: how often 14 of the 19 odd primes up to 71 cover the gap
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `(modulus: int = 16) -> Dict[str, Any]`
```python
>>> module.run('moonshine_fill_control', {})['result']
{'pool_size': 19, 'subsets': 11628, 'cover_gap': 7904, 'cover_all_odd': 5283, 'p_cover_gap': 0.6797385620915033, 'p_cover_all_odd': 0.45433436532507737}
```

**`totient_constructibility_check`** — Gauss-Wantzel by Euler phi, with no list of Fermat primes
  params: `limit`  ·  confidence: `ESTABLISHED`  ·  signature: `(limit: int = 70000) -> Dict[str, Any]`
```python
>>> module.run('totient_constructibility_check', {})['result']
{'limit': 70000, 'constructible': 139, 'mismatches': []}
```


---

*Theory page: [`hypergon_constructibility.md`](../hypergon_constructibility.md).*
