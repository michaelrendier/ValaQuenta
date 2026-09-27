# Noether Currents  ∂_μJ^μ = 0

**Module:** `ValaQuenta.modules.noether`
**Import:** `from ValaQuenta.modules.noether.tools import NoetherModule`
**Theory page:** [`../noether_diagnostic.md`](../noether_diagnostic.md)

---

`noether` · v0.111 · confidence floor **THEORETICAL**

Emmy Noether theorem applied to L_NN. Symmetry → conserved current. Violation = |∂_μJ^μ| — the training diagnostic with no GD analog. Blockchain ledger records every violation event. Resonance artifact detection identifies boundary oscillations.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`conservation_diagnostic`** — ∂_μJ^μ — full Noether conservation check
  params: `psi_norms, g, algebra`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`violation_scan`** — Violation scan across all algebra strata
  params: `psi_norms, g`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`resonance_artifacts`** — Resonance artifact detection (J history)
  params: `n_steps, g, algebra`  ·  confidence: `THEORETICAL`  ·  signature: `None`

**`blockchain_record`** — Record violation to NoetherLedger (blockchain)
  params: `algebra, violation, g`  ·  confidence: `ESTABLISHED`  ·  signature: `None`

**`blockchain_verify`** — Verify NoetherLedger chain integrity
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('blockchain_verify', {})['result']
{'valid': True, 'broken_at': None, 'length': 0}
```

**`blockchain_summary`** — NoetherLedger summary
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('blockchain_summary', {})['result']
{'total_blocks': 0, 'violations': 0, 'passes': 0, 'chain_valid': True, 'last_hash': '0000000000000000…'}
```

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`noether`, `ledger`, `verify`

---

### Running via the registry

```python
from ValaQuenta.modules.noether.tools import NoetherModule

m = NoetherModule()
m.formulary()                              # list every Equation this module exposes
m.run('conservation_diagnostic', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('conservation_diagnostic', {}, 'text')     # -> {'text': '...formatted...'}
```
