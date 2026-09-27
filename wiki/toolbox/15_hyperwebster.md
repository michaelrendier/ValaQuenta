# HyperWebster  Horner Bijection

**Module:** `ValaQuenta.modules.hyperwebster`
**Import:** `from ValaQuenta.modules.hyperwebster.tools import HyperWebsterModule`
**Theory page:** [`../hyperwebster.md`](../hyperwebster.md)

---

`hyperwebster` · v0.111 · confidence floor **THEORETICAL**

HyperWebster hypergallery. Coordinates instead of pointers. Horner bijection (base-97): lossless text-to-integer address. Fano address (base-7): octonion generator path. SemanticWord: text + Horner + Fano + algebra coords. Monad: HyperWebster + Cayley-Dickson SMNNIP integrated.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`horner_encode`** — Horner base-97 bijection: text → integer address
  params: `text`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`fano_encode`** — Fano base-7 octonion path address
  params: `text`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`semantic_word`** — SemanticWord — Horner + Fano + hash
  params: `text`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`monad_address`** — Monad: word → algebra tower coordinates
  params: `text, algebra`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`address_range`** — n consecutive Horner addresses from start_text
  params: `text, n`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`fano_path`** — Fano generator path → nearest keyword
  params: `text`  ·  confidence: `THEORETICAL`  ·  signature: `None`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`hw`, `horner`, `fano`, `monad`

---

### Running via the registry

```python
from ValaQuenta.modules.hyperwebster.tools import HyperWebsterModule

m = HyperWebsterModule()
m.formulary()                              # list every Equation this module exposes
m.run('horner_encode', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('horner_encode', {}, 'text')     # -> {'text': '...formatted...'}
```
