# Bracketing, Firing Order, and Set Membership

**Module:** `ValaQuenta.modules.bracketing_firing_order`
**Import:** `from ValaQuenta.modules.bracketing_firing_order.maths import ...`
**Theory page:** [`../bracketing_firing_order.md`](../bracketing_firing_order.md)

---

## `bell_number(n: int) -> int`

Exact count of unordered groupings of `n` distinct things.

```python
from ValaQuenta.modules.bracketing_firing_order.maths import bell_number

bell_number(3)   # -> 5
bell_number(16)  # -> 10480142147
```

Raises `ValueError` if `n < 0`. No upper limit — always returns the exact
integer, however large.

---

## `set_partitions(items: Sequence[Any]) -> List[List[List[Any]]]`

Every unordered partition of `items` into non-empty groups.

```python
from ValaQuenta.modules.bracketing_firing_order.maths import set_partitions

set_partitions(['Add', 'Scale', 'Sign'])
# -> [[['Add','Scale','Sign']],
#     [['Add'],['Scale','Sign']],
#     [['Add','Scale'],['Sign']],
#     [['Scale'],['Add','Sign']],
#     [['Add'],['Scale'],['Sign']]]
```

**Raises `ValueError` if `len(items) > 12`** — use `bell_number(n)` for
the count instead; this function will not attempt to build a list that
large.

---

## `bracketing_report(items: Sequence[Any]) -> Dict[str, Any]`

Count always; list only when feasible (`len(items) <= 12`).

```python
from ValaQuenta.modules.bracketing_firing_order.maths import bracketing_report

bracketing_report(list(range(16)))
# -> {'n': 16, 'bell_number': 10480142147, 'enumerable': False,
#     'items': [0, 1, ..., 15],
#     'note': 'Bell(16)=10480142147 exceeds the enumeration ceiling (12) -- counted exactly, not listed.'}

bracketing_report(['Add', 'Scale', 'Sign'])
# -> {'n': 3, 'bell_number': 5, 'enumerable': True,
#     'items': [...], 'partitions': [...]}  # the full list, as in set_partitions()
```

**Keys:** `n`, `bell_number`, `enumerable` (bool), `items`. If
`enumerable` is `True`, also `partitions` (the full list). If `False`,
also `note` (why it wasn't listed).

---

## `firing_order_count(n: int) -> int`

Exact count of ways to sequence `n` distinct things (`n!`).

```python
from ValaQuenta.modules.bracketing_firing_order.maths import firing_order_count

firing_order_count(3)   # -> 6
firing_order_count(10)  # -> 3628800
```

Raises `ValueError` if `n < 0`.

---

## `apply_firing_order(written: Sequence[Any], firing_order: Sequence[int]) -> List[Any]`

Resequence `written` by `firing_order`. `firing_order` is **1-indexed**:
`firing_order[k]` names which position in `written` fires k-th.

```python
from ValaQuenta.modules.bracketing_firing_order.maths import apply_firing_order

apply_firing_order(['Scale', 'Sign', 'Add'], (3, 1, 2))
# -> ['Add', 'Scale', 'Sign']
```

Raises `ValueError` if `firing_order` is not a permutation of
`1..len(written)`.

---

## `all_firing_orders(items: Sequence[Any]) -> List[Tuple[Any, ...]]`

Every possible sequencing of `items`, exhaustive.

```python
from ValaQuenta.modules.bracketing_firing_order.maths import all_firing_orders

all_firing_orders(['A', 'B', 'C'])
# -> [('A','B','C'), ('A','C','B'), ('B','A','C'),
#     ('B','C','A'), ('C','A','B'), ('C','B','A')]
```

No guard on `n` — caller keeps `n` small (`n!` grows fast: `10! ≈ 3.6M`).

---

## `trajectory(steps: Sequence[Callable[[float], float]], x0: float = 1.0) -> Tuple[float, ...]`

The sequence of positions visited: `x0`, then the result after each
`steps[i]` fires in order.

```python
from ValaQuenta.modules.bracketing_firing_order.maths import trajectory

steps = [lambda x: x + 2, lambda x: x - 2]
trajectory(steps, x0=1.0)
# -> (1.0, 3.0, 1.0)
```

Works with any callables `float -> float` — not limited to `ASS`
elements.

---

## `visited_positions(steps, x0=1.0, tol=1e-9) -> Dict[float, List[int]]`

Which trajectory positions repeat, and at which step indices (keys are
positions rounded to `tol`; values are every trajectory index landing
there).

```python
from ValaQuenta.modules.bracketing_firing_order.maths import visited_positions

visited_positions([lambda x: x + 2, lambda x: x - 2], x0=1.0)
# -> {1.0: [0, 2], 3.0: [1]}
```

---

## `collisions(steps, x0=1.0, tol=1e-9) -> List[Tuple[int, int, float]]`

Every `(earlier_index, later_index, position)` where the trajectory
revisits an earlier position.

```python
from ValaQuenta.modules.bracketing_firing_order.maths import collisions

collisions([lambda x: x + 2, lambda x: x - 2], x0=1.0)
# -> [(0, 2, 1.0)]

collisions([lambda x: x + 2, lambda x: x * 3], x0=1.0)
# -> []   (self-avoiding — no revisits)
```

---

## `would_collide(steps_so_far, candidate_next, x0=1.0, tol=1e-9) -> bool`

Would firing `candidate_next` (not yet appended) land on a position
already in the trajectory so far?

```python
from ValaQuenta.modules.bracketing_firing_order.maths import would_collide

steps_so_far = [lambda x: x + 2]   # trajectory so far: (1.0, 3.0)
would_collide(steps_so_far, lambda x: x - 2, x0=1.0)   # -> True  (3-2=1, already visited)
would_collide(steps_so_far, lambda x: x + 5, x0=1.0)   # -> False (3+5=8, novel)
```

---

## `jurisdiction_violation(object_name: str, requested_operation: str, jurisdiction_map: Dict[str, Set[str]]) -> Dict[str, Any]`

Is `requested_operation` legal for `object_name`, per the supplied map?
**You provide the map** — this function does not carry one internally.

```python
from ValaQuenta.modules.bracketing_firing_order.maths import jurisdiction_violation

jmap = {
    'lineage': {'descend'},
    'emerger': {'build_up'},
    'box_kite': {'descend', 'build_up'},
}

jurisdiction_violation('lineage', 'build_up', jmap)
# -> {'object': 'lineage', 'operation': 'build_up', 'known': True,
#     'legal_operations': ['descend'], 'violation': True,
#     'note': "'build_up' is NOT legal for 'lineage' (legal set: ['descend'])"}

jurisdiction_violation('box_kite', 'build_up', jmap)
# -> {..., 'violation': False, ...}

jurisdiction_violation('unknown_thing', 'descend', jmap)
# -> {'object': 'unknown_thing', 'operation': 'descend', 'known': False,
#     'violation': None, 'note': "'unknown_thing' not present in the supplied jurisdiction map"}
```

**Return keys:** `object`, `operation`, `known` (bool). If `known` is
`True`: `legal_operations` (sorted list), `violation` (bool), `note`
(string). If `known` is `False`: `violation` is `None`, `note` explains why.

---

## Running via the ValaQuenta Tab / registry

```python
from ValaQuenta.modules.bracketing_firing_order import BracketingFiringOrderModule

m = BracketingFiringOrderModule()
m.formulary()                                      # list every Equation this module exposes
m.run('bell_number', {'n': 16})                     # -> {'result': 10480142147, ...}
m.viewer_data('bell_number', {'n': 16}, 'text')     # -> {'text': '...formatted...'}
```
