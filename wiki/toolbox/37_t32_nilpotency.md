# T32 Nilpotency — Hyperwebster Address Primitives

**Module:** `ValaQuenta.modules.t32_nilpotency`
**Import:** `from ValaQuenta.modules.t32_nilpotency.tools import T32NilpotencyModule`
**Theory page:** [t32_nilpotency.md](../t32_nilpotency.md)

---

`t32_nilpotency` · v0.120 · confidence floor **ESTABLISHED**

Standalone, minimal, verified-correct primitives: Hyperwebster base-97 address encoding, T32/GF(2) Cayley-Dickson multiplication, nilpotency test. Meant to be imported by other engines (hypergon_constructibility, fermat_monster_engine.py) rather than each maintaining its own copy.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`prime_nilpotency_report`** — Nilpotency status of a set of primes in T32/GF(2)
  params: `primes`  ·  confidence: `ESTABLISHED`  ·  signature: `(primes=None)`
```python
>>> module.run('prime_nilpotency_report', {})['result']
{'rows': [{'prime': 2, 't32_word': 2, 'nilpotent': False}, {'prime': 3, 't32_word': 3, 'nilpotent': True}, {'prime': 5, 't32_word': 5, 'nilpotent': True}, {'prime': 7, 't ...
```

**`radical_census`** — GF(2) square law: nilpotent / involutory census, with the Δ(w) = w·𝟏 detector check
  params: `dim`  ·  confidence: `ESTABLISHED`  ·  signature: `(dim=8)`
```python
>>> module.run('radical_census', {})['result']
{'dim': 8, 'words': 256, 'nilpotent': 128, 'involutory': 128, 'other': 0, 'detector_agrees': True, 'one_is_annihilator': False}
```

**`nilpotency_control`** — Nilpotent rate of primes against composites, and the prime-matched chance control
  params: `lo`, `hi`, `subset`  ·  confidence: `ESTABLISHED`  ·  signature: `(lo=10, hi=100, subset=None)`
```python
>>> module.run('nilpotency_control', {})['result']
{'window': {'lo': 10, 'hi': 100, 'primes': {'nilpotent': 17, 'n': 21, 'rate': 0.8095238095238095}, 'composites': {'nilpotent': 29, 'n': 69, 'rate': 0.42028985507246375},  ...
```


---

*Theory page: [`t32_nilpotency.md`](../t32_nilpotency.md).*
