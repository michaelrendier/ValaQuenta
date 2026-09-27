# The Translator v1 — DisCoCat (pregroup . tensor)

**Module:** `ValaQuenta.modules.translator_discocat`
**Import:** `from ValaQuenta.modules.translator_discocat.tools import DisCoCatTranslatorModule`
**Theory page:** [`../translator_discocat.md`](../translator_discocat.md)

---

`translator_discocat` · v0.111 · confidence floor **OPEN**

Version 1 of two Translator constructions. Categorical compositional distributional semantics: syntax is a pregroup grammar, semantics is vector spaces, and the pregroup reduction n.(n^r.s.n^l).n -> s maps functorially onto contraction of an order-3 verb tensor against subject and object vectors. Noun and sentence spaces are the 16 prime channels (the sedenion basis); the verb tensor is 16^3 = 4096 and is the verb token's own prime-channel harmonics reshaped — derived, never trained. Shares its vector space with translator_vsa so the two versions can be combined and cross-tested.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`pregroup_reduction`** — Pregroup type reduction  x^(a) x^(a+1) -> 1
  params: `atoms`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`grammaticality`** — Transitive clause reduces to s
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`functor_contraction`** — Functor: reduction -> tensor contraction
  params: `subject, verb, object`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`sentence_meaning`** — Composed sentence vector in S (16-dim)
  params: `subject, verb, object`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`word_order_sensitivity`** — DOG BITES MAN vs MAN BITES DOG
  params: `subject, verb, object`  ·  confidence: `THEORETICAL`  ·  signature: `None`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`discocat_selftest`, `discocat_compose`

---

### Running via the registry

```python
from ValaQuenta.modules.translator_discocat.tools import DisCoCatTranslatorModule

m = DisCoCatTranslatorModule()
m.formulary()                              # list every Equation this module exposes
m.run('pregroup_reduction', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('pregroup_reduction', {}, 'text')     # -> {'text': '...formatted...'}
```
