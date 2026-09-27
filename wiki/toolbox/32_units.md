# Units (The Equation Index)

**Module:** `ValaQuenta.modules.units`
**Import:** `from ValaQuenta.modules.units.tools import UnitsModule`
**Theory page:** [`../units.md`](../units.md)

---

`units` · v0.1 · confidence floor **ESTABLISHED**

A unit is a point in the 7-axis SI base-dimension lattice (kg,m,s,A,K,mol,cd) -- the same leaf/composite structure this project already runs on numbers (factor_lineage) and processes (pathway_decompose), a fourth domain, not a new mechanism. Every named compound (Newton, Joule, Watt, Tesla...) has an exact, computable lineage back to the 7 leaves; cancellation is exact vector arithmetic, not string bookkeeping. A unit carries no numeric content and does no work itself -- a geometry, in this project's established sense -- but it determines which permutations of content (which equations) are even dimensionally possible: EQUATION_INDEX makes that claim concrete, looking up the standard physical laws that produce a given dimension signature.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`unit_compose`** — UNIT ARITHMETIC: multiply/divide as exponent-vector add/subtract
  params: `a, b, op`  ·  confidence: `ESTABLISHED`  ·  signature: `(a, b, op='mul')`

**`lineage_table_verified`** — THE UNIT LINEAGE: named compounds trace exactly back to the 7 leaves
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('lineage_table_verified', {})['result']
{'results': {'N': True, 'J': True, 'W': True, 'Pa': True, 'C': True, 'V': True, 'Ω': True, 'F': True, 'Wb': True, 'T': True, 'H': True}, 'holds': True, 'tesla_path': ['T', 'Wb', 'V', 'W', 'J', 'N', 'kg', 'm', 's', 'm', 's', 'A', 's', 'm']}
```

**`cancellation_demo`** — THE CHEMISTRY CASE: mol/L * L cancels back to mol exactly
  params: `—`  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('cancellation_demo', {})['result']
{'concentration_exponents': (0, -3, 0, 0, 0, 1, 0), 'recombined_exponents': (0, 0, 0, 0, 0, 1, 0), 'mol_exponents': (0, 0, 0, 0, 0, 1, 0), 'holds': True}
```

**`equation_index`** — THE EQUATION INDEX: a dimension signature narrows the candidate laws
  params: `exponents`  ·  confidence: `ESTABLISHED`  ·  signature: `(exponents)`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`uvec`, `umul`, `udiv`, `upow`, `ulineage`, `ucancel`, `eqindex`

---

### Running via the registry

```python
from ValaQuenta.modules.units.tools import UnitsModule

m = UnitsModule()
m.formulary()                              # list every Equation this module exposes
m.run('unit_compose', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('unit_compose', {}, 'text')     # -> {'text': '...formatted...'}
```
