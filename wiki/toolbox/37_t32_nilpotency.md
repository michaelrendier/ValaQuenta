# T32 Nilpotency — Hyperwebster Address Primitives

**Module:** `ValaQuenta.modules.t32_nilpotency`
**Import:** `from ValaQuenta.modules.t32_nilpotency.tools import T32NilpotencyModule`
**Theory page:** [`../t32_nilpotency.md`](../t32_nilpotency.md)

---

`t32_nilpotency` · v0.100 · confidence floor **ESTABLISHED**

Standalone, minimal, verified-correct primitives: Hyperwebster base-97 address encoding, T32/GF(2) Cayley-Dickson multiplication, nilpotency test. Meant to be imported by other engines (hypergon_constructibility, fermat_monster_engine.py) rather than each maintaining its own copy.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`prime_nilpotency_report`** — Nilpotency status of a set of primes in T32/GF(2)
  params: `primes`  ·  confidence: `ESTABLISHED`  ·  signature: `(primes=None)`
```python
>>> module.run('prime_nilpotency_report', {})['result']
{'rows': [{'prime': 2, 't32_word': 2, 'nilpotent': False}, {'prime': 3, 't32_word': 3, 'nilpotent': True}, {'prime': 5, 't32_word': 5, 'nilpotent': True}, {'prime': 7, 't32_word': 7, 'nilpotent': False}, {'prime': 11, 't32_word': 195, 'nilpotent': True}, {'prime': 13, 't32_word': 197, 'nilpotent'...
```

---

### Running via the registry

```python
from ValaQuenta.modules.t32_nilpotency.tools import T32NilpotencyModule

m = T32NilpotencyModule()
m.formulary()                              # list every Equation this module exposes
m.run('prime_nilpotency_report', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('prime_nilpotency_report', {}, 'text')     # -> {'text': '...formatted...'}
```
