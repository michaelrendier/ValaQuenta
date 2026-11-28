# Bracketing, Firing Order, and Set Membership

**Module:** `ValaQuenta.modules.bracketing_firing_order`
**Import:** `from ValaQuenta.modules.bracketing_firing_order.tools import BracketingFiringOrderModule`
**Theory page:** [bracketing_firing_order.md](../bracketing_firing_order.md)

---

`bracketing_firing_order` · v0.2 · confidence floor **ESTABLISHED**

Three general-purpose, domain-independent tools, not one thing tied to add_scale_sign. BRACKETING: how many unordered ways can n things be grouped (exact Bell-number count always; exhaustive enumeration only when feasible, n<=12 -- refuses rather than silently hangs above that). FIRING ORDER: how many ways can n things be sequenced (n!), and applying a specific firing order is a literal permutation action -- verified worked example: (3,1,2) applied to [Scale,Sign,Add] gives [Add,Scale,Sign], ASS's own canonical name reached by resequencing, not relabeling. SET MEMBERSHIP, two jobs: has a firing recurred before (trajectory/collision detection, generalizing Recaman's own defining rule to any sequence of callables); and did a bracketing cause one jurisdiction's maths to be used on an object native to a different jurisdiction (grounded in GenerationalLineage's own decomposition/emerger 'two jurisdictions', parametrized here not hardcoded).

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`bell_number`** — BRACKETING: exact count of unordered groupings — the Bell number
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n)`
```python
>>> module.run('bell_number', {...})['result']      # needs its arguments: BracketingFiringOrderModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 'n'
```

**`bracketing_report`** — BRACKETING: exact count always, exhaustive list only when feasible
  params: `items`  ·  confidence: `ESTABLISHED`  ·  signature: `(items)`
```python
>>> module.run('bracketing_report', {...})['result']      # needs its arguments: BracketingFiringOrderModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 'items'
```

**`firing_order_count`** — FIRING ORDER: exact count of sequencings — n!
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n)`
```python
>>> module.run('firing_order_count', {...})['result']      # needs its arguments: BracketingFiringOrderModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 'n'
```

**`apply_firing_order`** — FIRING ORDER: resequence a written order by a chosen permutation
  params: `written`, `firing_order`  ·  confidence: `ESTABLISHED`  ·  signature: `(written, firing_order)`
```python
>>> module.run('apply_firing_order', {...})['result']      # needs its arguments: BracketingFiringOrderModule.formulary.<locals>.<lambda>() missing 2 required positional arguments: 'written' and 'firing_order'
```

**`four_orderings`** — PLANS: bracketing, firing order, firing order of brackets, bracketing of firing orders: how many, and how many different outputs
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('four_orderings', {})['result']
{'counts_n3': {'A': 2, 'B': 6, 'C': 8, 'D': 12}, 'counts_n4': {'A': 5, 'B': 24, 'C': 40, 'D': 120}, 'counts_n5': {'A': 14, 'B': 120, 'C': 224, 'D': 1680}, 'fire_sequences ...
```

**`evolve`** — PLANS: watch a 16-component input evolve under a plan, step by step
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `() -> Dict[str, Any]`
```python
>>> module.run('evolve', {})['result']
{'plan': '((A B | 2 1) C | 2 1)', 'input': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 'fired': ['C', 'B', 'A'], 'output': ['-7', '1', '-28', '12', '30', '3', '-13' ...
```

**`collisions`** — SET MEMBERSHIP: has a firing recurred? (Recaman, generalized)
  params: `steps`, `x0`  ·  confidence: `ESTABLISHED`  ·  signature: `(steps, x0=1.0)`
```python
>>> module.run('collisions', {...})['result']      # needs its arguments: BracketingFiringOrderModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 'steps'
```

**`would_collide`** — SET MEMBERSHIP: the operator-level flip test, before committing
  params: `steps_so_far`, `candidate_next`, `x0`  ·  confidence: `ESTABLISHED`  ·  signature: `(steps_so_far, candidate_next, x0=1.0)`
```python
>>> module.run('would_collide', {...})['result']      # needs its arguments: BracketingFiringOrderModule.formulary.<locals>.<lambda>() missing 2 required positional arguments: 'steps_so_far' and 'candidate_next'
```

**`jurisdiction_violation`** — SET MEMBERSHIP: did a bracketing use another jurisdiction's language illegally?
  params: `object_name`, `requested_operation`, `jurisdiction_map`  ·  confidence: `ESTABLISHED`  ·  signature: `(object_name, requested_operation, jurisdiction_map)`
```python
>>> module.run('jurisdiction_violation', {...})['result']      # needs its arguments: BracketingFiringOrderModule.formulary.<locals>.<lambda>() missing 3 required positional arguments: 'object_name', 'requested_operation', and 'jurisdiction_map'
```

### Shell commands

`bell` · `partitions` · `bracket_report` · `fire_count` · `fire_apply` · `collisions` · `jurisdiction` · `orderings` · `evolve`


---

*Theory page: [`bracketing_firing_order.md`](../bracketing_firing_order.md).*
