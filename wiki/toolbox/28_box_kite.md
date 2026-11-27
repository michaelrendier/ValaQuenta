# The Box-Kite Debugger (ZD Geometry)

**Module:** `ValaQuenta.modules.box_kite`
**Import:** `from ValaQuenta.modules.box_kite.tools import BoxKiteModule`
**Theory page:** [box_kite.md](../box_kite.md)

---

`box_kite` · v0.3 · confidence floor **ESTABLISHED**

Makes the sedenion zero-divisor geometry visible and exactly enumerable. The object is PSL(2,7) -- order 168, Aut(Fano plane) -- NOT G2: Moreno's G2 homeomorphism is a blow-up that forgets which Fano line is which. Everything here derives from the Cayley-Dickson multiplication table: 42 Assessors (planes span(e_a, e_b+8) whose diagonals zero-divide; a==b never works, so 49-7=42), 84 diagonals, 168 primitive unit points, 336 ordered annihilating pairs, and 7 box-kites of 6 Assessors each. Each box-kite is an OCTAHEDRON (K_2,2,2), verified from vanishing products, with Laplacian spectrum {0,4,4,4,6,6} -- the chart-level dispersion relation. The zero mode is e_0's signature: exists everywhere, propagates nowhere. The associator [a,b,c]=(ab)c-a(bc) is the curvature and the debug view. Agreement with ZD_PAIRS=84 / ZD_CLASSES=42 / 168 is a CHECK, not an input. v0.2 adds THE CHART OF ADDRESSES: given a monad sedenion address (VAPMIP/monad_sedenion_addresses.pkl), chart_of() reports which of the 7 charts it occupies, its nearest Assessor and diagonals, its local associator curvature, and its FIXED-POINT WEIGHT. And it resolves the disconnection: the charts touch in the SKELETON (every usable index sits in 6 of 7 charts; only e_0 and e_8 are orphans) even though they have zero cross-strut adjacency edges. The 7 zero modes are 7 copies of one constant, and they identify at e_0 -- the fixed point is where the boundary generator and the geometry coincide.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`verify_counts`** — THE HONEST CHECK: 42 / 84 / 168 / 336 / 7, all derived
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('verify_counts', {})['result']
{'assessors': 42, 'assessors_expect_42': True, 'all_verified_assessors': True, 'aligned_planes_empty': True, 'diagonals': 84, 'diagonals_expect_84': True, 'unit_points':  ...
```

**`box_kites`** — The 7 box-kites, keyed by strut s = a XOR b
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('box_kites', {})['result']
{1: [(2, 3), (3, 2), (4, 5), (5, 4), (6, 7), (7, 6)], 2: [(1, 3), (3, 1), (4, 6), (5, 7), (6, 4), (7, 5)], 3: [(1, 2), (2, 1), (4, 7), (5, 6), (6, 5), (7, 4)], 4: [(1, 5) ...
```

**`box_kite_graph`** — THE SHAPE: each chart is an octahedron K_2,2,2
  params: `s`  ·  confidence: `ESTABLISHED`  ·  signature: `(s)`
```python
>>> module.run('box_kite_graph', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 's'
```

**`chart_spectrum`** — THE DISPERSION RELATION, chart level: {0,4,4,4,6,6}
  params: `s`  ·  confidence: `ESTABLISHED`  ·  signature: `(s)`
```python
>>> module.run('chart_spectrum', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 's'
```

**`associator`** — THE CURVATURE: [a,b,c] = (ab)c - a(bc)
  params: `i`, `j`, `k`  ·  confidence: `ESTABLISHED`  ·  signature: `(i, j, k)`
```python
>>> module.run('associator', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 3 required positional arguments: 'i', 'j', and 'k'
```

**`associator_field`** — THE DEBUG VIEW: curvature painted on a box-kite
  params: `s`  ·  confidence: `ESTABLISHED`  ·  signature: `(s)`
```python
>>> module.run('associator_field', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 's'
```

**`commutator`** — THE TORSION: [a,b] = ab - ba
  params: `i`, `j`  ·  confidence: `ESTABLISHED`  ·  signature: `(i, j)`
```python
>>> module.run('commutator', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 2 required positional arguments: 'i' and 'j'
```

**`glued_graph`** — The 42-vertex atlas — and its cross-strut edge count
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('glued_graph', {})['result']
{'vertices': [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 1), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7), (4, 1), (4,  ...
```

**`glued_spectrum`** — Laplacian spectrum of the whole atlas
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('glued_spectrum', {})['result']
[-2.578245350937398e-16, -2.578245350937398e-16, -1.7672181421110489e-16, -1.9925244047026614e-17, -2.618422140095473e-18, -4.284025584375216e-20, 2.23629093583609e-17, 3 ...
```

**`chart_of`** — THE CHART OF ADDRESSES: where a monad address sits in the atlas
  params: `v`, `check_zd`  ·  confidence: `ESTABLISHED`  ·  signature: `(v, check_zd=True)`
```python
>>> module.run('chart_of', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 'v'
```

**`address_census`** — Exhaustive census over a corpus of monad addresses
  params: `addresses`, `limit`, `check_zd`  ·  confidence: `ESTABLISHED`  ·  signature: `(addresses, limit=None, check_zd=False)`
```python
>>> module.run('address_census', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 'addresses'
```

**`skeleton_overlap`** — THE CHARTS DO TOUCH — in the skeleton, not the adjacency
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('skeleton_overlap', {})['result']
{'indices_used': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15], 'indices_in_no_chart': [0, 8], 'charts_per_index': {1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 9: 6, 10: ...
```

**`fixed_point_gluing`** — WHERE THE ATLAS GLUES: at e_0
  params: —  ·  confidence: `THEORETICAL`  ·  signature: `()`
```python
>>> module.run('fixed_point_gluing', {})['result']
{'indices_in_no_assessor': [0, 8], 'e0_is_orphan': True, 'e8_is_orphan': True, 'orphan_count': 2, 'zero_modes_total': 7, 'components': 7, 'after_identification': 1, 'read ...
```

**`fixed_point_weight`** — How much of an address is pure 0_RB
  params: `v`  ·  confidence: `ESTABLISHED`  ·  signature: `(v)`
```python
>>> module.run('fixed_point_weight', {...})['result']      # needs its arguments: BoxKiteModule.formulary.<locals>.<lambda>() missing 1 required positional argument: 'v'
```

**`skeleton_counts`** — PG(3,2): 15 points, 35 lines, 15 Fano planes (NOT 32)
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('skeleton_counts', {})['result']
{'points': 15, 'points_expect_15': True, 'lines': 35, 'lines_expect_35': True, 'planes': 15, 'planes_expect_15': True, 'plane_size': 7, 'plane_size_expect_7': True, 'psl2 ...
```

**`labelled_automorphisms`** — The labelled octonion group: order 1344 = 8 x 168, transitive on the 168 unit zero-divisor points
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('labelled_automorphisms', {})['result']
{'fano_permutations': 168, 'signed_automorphisms': 1344, 'sign_kernel': 8, 'quotient_order': 168, 'extend_to_sedenions': True, 'unit_points': 168, 'orbits_on_unit_points' ...
```

**`e0_is_outside`** — 0_RB IS NOT THE GEOMETRY — checked, not asserted
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('e0_is_outside', {})['result']
{'e0_is_a_pg32_point': False, 'e0_in_any_assessor': False, 'e0_associator_always_vanishes': True, 'e0_is_outside_the_geometry': True}
```

**`associator_census`** — How much of the algebra is curved
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('associator_census', {})['result']
{'total': 4096, 'nonzero': 1848, 'zero': 2248}
```

**`zero_divisor_pairs`** — All 336 ordered annihilating diagonal pairs
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('zero_divisor_pairs', {})['result']
[((1, 2, 1), (4, 7, -1)), ((1, 2, 1), (5, 6, 1)), ((1, 2, 1), (6, 5, -1)), ((1, 2, 1), (7, 4, 1)), ((1, 2, -1), (4, 7, 1)), ((1, 2, -1), (5, 6, -1)), ((1, 2, -1), (6, 5,  ...
```

### Shell commands

`verify` · `kites` · `kite` · `spec` · `assoc` · `defect` · `field` · `comm` · `atlas` · `atlas_spec` · `skeleton` · `lines` · `fano` · `e0` · `census` · `zds` · `mul` · `chart` · `overlap` · `glue` · `fpw` · `split` · `assess` · `proj` · `curv` · `membership`


---

*Theory page: [`box_kite.md`](../box_kite.md).*
