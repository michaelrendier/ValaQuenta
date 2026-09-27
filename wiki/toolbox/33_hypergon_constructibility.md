# Hypergon Constructibility — Gauss-Wantzel + Factorization Test

**Module:** `ValaQuenta.modules.hypergon_constructibility`
**Import:** `from ValaQuenta.modules.hypergon_constructibility.tools import HypergonConstructibilityModule`
**Theory page:** [`../hypergon_constructibility.md`](../hypergon_constructibility.md)

---

`hypergon_constructibility` · v0.100 · confidence floor **OPEN**

All 16 sedenion hyper-N-gons tested for Gauss-Wantzel constructibility (REAL result: 4/16 constructible, 12/16 holes). Phase 22's corrected nilpotent-split factorization conjecture re-tested against a magnitude-matched control (HONEST result: does not survive — likely address-mapping artifact, not a real factoring signal). Dual arithmetic/geometric prime definition, NOT unified into a working factoring mechanism.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`sedenion_hypergon_sweep`** — All 16 N-gons — Gauss-Wantzel constructibility, verified not assumed
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('sedenion_hypergon_sweep', {})['result']
{'rows': [{'channel': 'e0', 'prime': 2, 'fermat_prime': False, 'power_of_2': True, 'constructible': True}, {'channel': 'e1', 'prime': 3, 'fermat_prime': True, 'power_of_2': False, 'constructible': True}, {'channel': 'e2', 'prime': 5, 'fermat_prime': True, 'power_of_2': False, 'constructible': Tru...
```

**`verify_nilpotent_split_conjecture`** — Re-test: does p,q nilpotency survive a magnitude-matched control?
  params: `—`  ·  confidence: `OPEN`  ·  signature: `(seed: int = 20260711) -> Dict[str, Any]`
```python
>>> module.run('verify_nilpotent_split_conjecture', {})['result']
{'close_prime_pairs': {'n': 110, 'p_pct': 69.0909090909091, 'q_pct': 76.36363636363636, 'both_pct': 52.72727272727273}, 'far_apart_prime_pairs': {'n': 97, 'p_pct': 47.422680412371136, 'q_pct': 45.36082474226804, 'both_pct': 22.68041237113402}, 'random_pair_control': {'n': 97, 'p_pct': 50.51546391...
```

**`prime_definition_report`** — Dual definition of prime — arithmetic + geometric, not yet unified
  params: `—`  ·  confidence: `THEORETICAL`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('prime_definition_report', {})['result']
{'arithmetic_definition': "A prime has no non-trivial factorization — a<1<a<p with a*b=p impossible for 1<a,b<p. This is why AbrikosovTree's CD-tower structure has primes as leaves surviving all 9 levels: no factorization means no zero-divisor pair can form, so the norm never fails and the prime ...
```

---

### Running via the registry

```python
from ValaQuenta.modules.hypergon_constructibility.tools import HypergonConstructibilityModule

m = HypergonConstructibilityModule()
m.formulary()                              # list every Equation this module exposes
m.run('sedenion_hypergon_sweep', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('sedenion_hypergon_sweep', {}, 'text')     # -> {'text': '...formatted...'}
```
