# Addition Matrix: Columns as Rotors, the Law of the Factor Search

**Module:** `ValaQuenta.modules.addition_matrix`
**Import:** `from ValaQuenta.modules.addition_matrix.tools import AdditionMatrixModule`
**Theory page:** [addition_matrix.md](../addition_matrix.md)

---

`addition_matrix` · v1.0 · confidence floor **ESTABLISHED**

The addition matrix of long multiplication read as arithmetic modulo 10^k. The rows, running sums and carry matrix of num1 x num2 (the core of the Multiplication Matrix Explorer), checked against Python's product. The digit in column c has an exact period in num2; x -> a x + b on Z/10^m has a cycle type that factors through Z/2^m x Z/5^m; the odometer returns to a coarser odometer. Digit-by-digit factor reconstruction keeps exactly the pairs (p, q) mod 10^(c+1) with p q = N there, and their number is a closed form, a product over the primes 2 and 5: for N with both valuations below c+1 it is (v2+1)(v5+1) phi(10^(c+1)), unit-group torsors, times ten per column. For each unit solution mod 10^n the overflow K = (p q - N)/10^n is an integer and the true factorisation is exactly K = 0; the address exists but is not isolated, since near-misses with small |K| exist. Nothing here is a faster factoring method; the live-state count is the quantity measured.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`matrix_trace`** — Addition matrix and carry matrix of num1 x num2, checked against *
  params: `num1`, `num2`  ·  confidence: `ESTABLISHED`  ·  signature: `(num1=1234567890, num2=9876543210)`
```python
>>> module.run('matrix_trace', {})['result']
{'num1': 1234567890, 'num2': 9876543210, 'product': 12193263111263526900, 'matches_python': True, 'max_carry': 1, 'rows': 10}
```

**`column_period`** — Exact period of the digit in column c of num1 x num2, in num2
  params: `num1`, `c`  ·  confidence: `ESTABLISHED`  ·  signature: `(num1=7, c=2)`
```python
>>> module.run('column_period', {})['result']
{'num1': 7, 'column': 2, 'period_formula': 1000, 'period_measured': 1000, 'agree': True}
```

**`crt_cycle_rule`** — Cycle type of x -> a x + b on Z/10^m is the CRT combination of Z/2^m and Z/5^m
  params: `a`, `b`, `m`  ·  confidence: `ESTABLISHED`  ·  signature: `(a=3, b=1, m=3)`
```python
>>> module.run('crt_cycle_rule', {})['result']
{'a': 3, 'b': 1, 'm': 3, 'cycle_type_Z_10m': {100: 8, 20: 8, 4: 10}, 'cycle_type_Z_2m': {4: 2}, 'cycle_type_Z_5m': {100: 1, 20: 1, 4: 1, 1: 1}, 'crt_rule_holds': True}
```

**`odometer_first_return`** — First-return map of the odometer to multiples of 10 is the odometer one scale down
  params: `m`  ·  confidence: `ESTABLISHED`  ·  signature: `(m=3)`
```python
>>> module.run('odometer_first_return', {})['result']
{'m': 3, 'return_set_size': 100, 'is_odometer_one_scale_down': True}
```

**`solenoid_cycles`** — x -> a x + b on Z/2^n (a odd): every cycle length is a power of two
  params: `a`, `b`, `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(a=3, b=1, n=10)`
```python
>>> module.run('solenoid_cycles', {})['result']
{'a': 3, 'b': 1, 'n': 10, 'cycle_type': {512: 2}, 'all_lengths_powers_of_two': True}
```

**`solution_count`** — Number of (p, q) mod 10^k with p q = N: closed form vs enumeration
  params: `N`, `k`  ·  confidence: `ESTABLISHED`  ·  signature: `(N=420, k=2)`
```python
>>> module.run('solution_count', {})['result']
{'N': 420, 'k': 2, 'closed_form': 320, 'enumerated': 320, 'agree': True}
```

**`live_state_law`** — The factor search's live states per column vs the closed form
  params: `N`, `n_digits`  ·  confidence: `ESTABLISHED`  ·  signature: `(N=14351, n_digits=3)`
```python
>>> module.run('live_state_law', {})['result']
{'N': 14351, 'n_digits': 3, 'live_states_per_column': [4, 40, 400, 48, 4, 2], 'closed_form_first_columns': [4, 40, 400], 'agree_for_columns_below_n': True}
```

**`torsor_structure`** — Unit-group orbits of the solution set, and the x10 per column
  params: `N`, `k`  ·  confidence: `ESTABLISHED`  ·  signature: `(N=14351, k=3)`
```python
>>> module.run('torsor_structure', {})['result']
{'N': 14351, 'k': 3, 'unit_group_order': 400, 'orbits': 1, 'solutions_closed_form': 400, 'orbits_times_unit_group': 400}
```

**`overflow_address`** — The K = 0 address of the final answer among the unit solutions mod 10^n
  params: `N`, `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(N=1022117, n=4)`
```python
>>> module.run('overflow_address', {})['result']
{'n': 4, 'solutions': 4000, 'zero_overflow': 2, 'smallest_nonzero_K': 1, 'median_nonzero_K': 1741.0, 'largest_K': 9796, 'median_K_all': 1741.0, 'zero_overflow_pairs': [(1 ...
```

**`lift_branching`** — Children per solution when one digit is added: uniformly ten
  params: `N`, `k`  ·  confidence: `ESTABLISHED`  ·  signature: `(N=3233, k=2)`
```python
>>> module.run('lift_branching', {})['result']
{'N': 3233, 'k': 2, 'children_per_solution': {10: 40}}
```

### Shell commands

`amlaw` · `amaddress`


---

*Theory page: [`addition_matrix.md`](../addition_matrix.md).*
