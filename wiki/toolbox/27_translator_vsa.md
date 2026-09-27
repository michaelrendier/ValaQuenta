# The Translator v2 — VSA / hyperdimensional (bind.bundle.permute)

**Module:** `ValaQuenta.modules.translator_vsa`
**Import:** `from ValaQuenta.modules.translator_vsa.tools import VSATranslatorModule`
**Theory page:** [`../translator_vsa.md`](../translator_vsa.md)

---

`translator_vsa` · v0.111 · confidence floor **OPEN**

Version 2 of two Translator constructions. Kanerva's vector-symbolic architecture: concepts are 4096-dimensional hypervectors, structure is built by non-commutative binding (P(a).b), superposing bundle, and cyclic permutation for sequence. Role vectors are the prime-channel expansions of their own names — no PRNG anywhere, so results are reproducible and no seed can be selected. Folds to the same 16 prime channels as translator_discocat so the two versions can be combined and cross-tested. Quasi-orthogonality, which textbook VSA assumes, is measured here instead.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`permute`** — Permute P — cyclic shift (sequence/position)
  params: `vector, shift`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`bind`** — Bind (x) — non-commutative role-filler pairing
  params: `a, b`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`bundle`** — Bundle (+) — superposition, un-normalised
  params: `vectors`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`sentence_hypervector`** — Bound-and-bundled sentence (4096-dim)
  params: `subject, verb, object`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`capacity_probe`** — Quasi-orthogonality of derived hypervectors
  params: `tokens`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`unbind_probe`** — Constituent recovery from the bundle
  params: `subject, verb, object`  ·  confidence: `THEORETICAL`  ·  signature: `None`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`vsa_selftest`, `vsa_capacity`, `vsa_unbind`

---

### Running via the registry

```python
from ValaQuenta.modules.translator_vsa.tools import VSATranslatorModule

m = VSATranslatorModule()
m.formulary()                              # list every Equation this module exposes
m.run('permute', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('permute', {}, 'text')     # -> {'text': '...formatted...'}
```
