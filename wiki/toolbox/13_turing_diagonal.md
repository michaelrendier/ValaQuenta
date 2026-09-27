# Turing Diagonal Engine — i²=-1 = Cantor = Gödel = Enigma = UDOE

**Module:** `ValaQuenta.modules.turing_diagonal`
**Import:** `from ValaQuenta.modules.turing_diagonal.tools import TuringDiagonalModule`
**Theory page:** [`../turing_diagonal.md`](../turing_diagonal.md)

---

`turing_diagonal` · v0.100 · confidence floor **ESTABLISHED**

The diagonal flip i²=[[-1,0],[0,-1]] unifies every self-referential proof. Engines: prediction diagonal test (any prediction → decidable/undecidable), enigma derangement (D_n/n!→1/e, Turing proof of concept), hypercomplex identity diagonal (eₖ²=-1 for k=1..15), halting diagonal (D(D) → σ=½ oscillation).

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`full_turing_diagonal`** — All 4 Turing Diagonal engines
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('full_turing_diagonal', {})['result']
{'theme': 'Turing Diagonal Engine — The diagonal flip = i² = -1 = Enigma = UDOE', 'prediction_diagonal_test': {'claim': 'Every self-referential prediction resolves to the diagonal flip i²=-1.', 'prediction': 'this statement is false', 'self_reference': {'detected': True, 'keywords_hit': ['this st...
```

**`prediction_diagonal_test`** — Apply Turing diagonal to any prediction → decidable/undecidable
  params: `prediction`  ·  confidence: `ESTABLISHED`  ·  signature: `(prediction='this statement is false')`
```python
>>> module.run('prediction_diagonal_test', {})['result']
{'claim': 'Every self-referential prediction resolves to the diagonal flip i²=-1.', 'prediction': 'this statement is false', 'self_reference': {'detected': True, 'keywords_hit': ['this statement', 'false'], 'negation_hit': ['false'], 'hedge_hit': []}, 'diagonal_depth': 2, 'i_power_analysis': {'de...
```

**`enigma_derangement`** — D_n/n! → 1/e. Enigma reflector = Cantor diagonal = Turing D(D).
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n=26)`
```python
>>> module.run('enigma_derangement', {})['result']
{'claim': 'D_26/26! → 1/e. The Enigma reflector = Cantor diagonal = Turing D(D). Same operation.', 'n': 26, 'D_n': 148362637348470135821287825, 'n_factorial': 403291461126605635584000000, 'P_derangement': 0.3678794412, '1_over_e': 0.3678794412, 'delta_from_e': 0.0, 'table_small_n': [{'n': 1, 'D_n...
```

**`hypercomplex_identity_diagonal`** — i²=[[-1,0],[0,-1]]. Cantor=Gödel=Turing=Enigma=sedenion.
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('hypercomplex_identity_diagonal', {})['result']
{'claim': 'The diagonal flip i²=-1=[[-1,0],[0,-1]] unifies Cantor, Gödel, Turing, Enigma, sedenion.', 'i_matrix_powers': {'i¹': '[[0,-1],[1,0]]', 'i²': '[[-1,0],[0,-1]]', 'i³': '[[0,1],[-1,0]]', 'i⁴': '[[1,0],[0,1]]', 'i²_is_neg_I': True, 'i⁴_is_pos_I': True, 'period': 4, 'the_flip': 'i² = [[-1,0...
```

**`turing_halting_diagonal`** — D(D): the program that escapes HALT. Oscillates at σ=½.
  params: `n_programs`  ·  confidence: `ESTABLISHED`  ·  signature: `(n_programs=50)`
```python
>>> module.run('turing_halting_diagonal', {})['result']
{'claim': 'D(D) is the program that escapes every HALT table. It lives at σ=½ because it oscillates between YES (σ→1) and NO (σ→0).', 'n_programs': 50, 'halting_table': {'shape': '50×50', 'halt_fraction': 0.5044, 'diagonal_halt': 0.46, 'diagonal_flip_D': [1, 1, 0, 1, 0, 0, 1, 0, 0, 1], 'first_10_...
```

---

### Running via the registry

```python
from ValaQuenta.modules.turing_diagonal.tools import TuringDiagonalModule

m = TuringDiagonalModule()
m.formulary()                              # list every Equation this module exposes
m.run('full_turing_diagonal', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('full_turing_diagonal', {}, 'text')     # -> {'text': '...formatted...'}
```
