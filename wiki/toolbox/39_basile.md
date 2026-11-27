# Basile: Invertible Location Maps (Library of Babel / Babelia)

**Module:** `ValaQuenta.modules.basile`
**Import:** `from ValaQuenta.modules.basile.tools import BasileModule`
**Theory page:** [basile.md](../basile.md)

---

`basile` · v1.3 · confidence floor **ESTABLISHED**

The invertible location-to-content maps of J. Basile's Library of Babel family. A location is a number and a page (or image) is computed from it, and back, with nothing stored: a linear congruential generator followed by shift/XOR steps, inverted with the modular inverse and the shifts undone in reverse. Provides the ordered (rank) address as the contrast case, a generic scrambler written from the recipe and checked exhaustively on a toy library, and the published Babelia engine run on its published constants (read from a local copy, never vendored): the two programs share their constants, a times a-inverse is 1 modulo m, the masks are powers of two, and the image reads fewer bits than the location space holds, so several locations show one image. Also the published Extended Euclid file with its fixed 25-entry array and the request the LobThis extension posts to the site. The text library's own algorithm is not published and is not reproduced.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`ordered_address`** — Ordered address: rank of a string among all strings over an alphabet
  params: `text`, `alphabet`  ·  confidence: `ESTABLISHED`  ·  signature: `(text='hello', alphabet='abcdefghijklmnopqrstuvwxyz')`
```python
>>> module.run('ordered_address', {})['result']
{'text': 'hello', 'address': 3752126, 'round_trip': True}
```

**`ordered_text_at`** — Ordered address, inverse: the string at a rank
  params: `address`, `alphabet`  ·  confidence: `ESTABLISHED`  ·  signature: `(address=702, alphabet='abcdefghijklmnopqrstuvwxyz')`
```python
>>> module.run('ordered_text_at', {})['result']
{'address': 702, 'text': 'aaa', 'round_trip': True}
```

**`scramble`** — Invertible scrambler of [0, N): LCG mod 2^e + xorshifts + cycle-walk
  params: `n`, `location`  ·  confidence: `ESTABLISHED`  ·  signature: `(n=24389, location=12345)`
```python
>>> module.run('scramble', {})['result']
{'n': 24389, 'location': 12345, 'scrambled': 5116, 'inverse_ok': True}
```

**`toy_library`** — Toy Library of Babel: the page at a location, scrambled and ordered
  params: `location`, `length`  ·  confidence: `ESTABLISHED`  ·  signature: `(location=0, length=3)`
```python
>>> module.run('toy_library', {})['result']
{'location': 0, 'pages': 24389, 'scrambled_page': 'blr', 'ordered_page': 'aaa', 'location_of_scrambled_page': 0}
```

**`scrambler_exhaustive`** — Every location of the toy library round-trips; the map is a bijection
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n=24389)`
```python
>>> module.run('scrambler_exhaustive', {})['result']
{'n': 24389, 'distinct_values': 24389, 'bijection': True, 'all_round_trip': True}
```

**`neighbour_statistics`** — Neighbouring locations: how many characters differ, ordered vs scrambled
  params: `length`  ·  confidence: `ESTABLISHED`  ·  signature: `(length=3)`
```python
>>> module.run('neighbour_statistics', {})['result']
{'pages': 24389, 'ordered_mean_chars_differing': 1.0355912743972446, 'scrambled_mean_chars_differing': 2.9101197310152536, 'independent_pages_expected': 2.896551724137931 ...
```

**`hull_dobell_check`** — Hull–Dobell conditions for a full-period LCG
  params: `m`, `a`, `c`, `prime_factors`  ·  confidence: `ESTABLISHED`  ·  signature: `(m=32768, a=1664525, c=1013904223, prime_factors=(2,))`
```python
>>> module.run('hull_dobell_check', {})['result']
{'gcd_m_c_is_1': True, 'a_minus_1_divisible_by_prime_factors': True, 'a_minus_1_divisible_by_4_if_4_divides_m': True, 'full_period': True}
```

**`xorshift_inverse_check`** — Exact inverses of the right xorshift and the masked left xorshift
  params: `width`, `s`, `samples`  ·  confidence: `ESTABLISHED`  ·  signature: `(width=64, s=7, samples=2000)`
```python
>>> module.run('xorshift_inverse_check', {})['result']
{'width': 64, 'shift': 7, 'samples': 2000, 'right_inverse_exact': True, 'left_masked_inverse_exact': True}
```

**`euclid_qarray_limit`** — Published Extended Euclid: the fixed 25-entry array vs random 64-bit inputs
  params: `bits`, `trials`  ·  confidence: `ESTABLISHED`  ·  signature: `(bits=64, trials=200)`
```python
>>> module.run('euclid_qarray_limit', {})['result']
{'bits': 64, 'trials': 200, 'overflow_count': 199, 'mean_divisions': 35.975, 'array_allows_divisions': 23}
```

**`address_parse`** — Site address fields: hexagon, wall, shelf, volume, page
  params: `address`  ·  confidence: `ESTABLISHED`  ·  signature: `(address='jeb0110jlb-w2-s4-v16:19')`
```python
>>> module.run('address_parse', {})['result']
{'hexagon': 'jeb0110jlb', 'wall': 2, 'shelf': 4, 'volume': 16, 'page': 19, 'volume_index': 271}
```

**`lobthis_request`** — The LobThis extension request, built as data and not sent
  params: `page_text`  ·  confidence: `ESTABLISHED`  ·  signature: `(page_text='text of the page in the browser')`
```python
>>> module.run('lobthis_request', {})['result']
{'method': 'POST', 'url': 'http://libraryofbabel.info/resourcelocator.cgi', 'fields': {'extension': 'text of the page in the browser'}}
```

**`library_scale`** — Scale of the text library, recomputed
  params: —  ·  confidence: `ESTABLISHED`  ·  signature: `()`
```python
>>> module.run('library_scale', {})['result']
{'log10_pages': 4679.67359327666, 'log10_books': 4677.06080941994, 'log10_full_books': 1918666.1732434304}
```

**`published_audit`** — Published Babelia constants: sizes, a·a⁻¹ ≡ 1, masks, palette, shared constants
  params: `cache_dir`  ·  confidence: `ESTABLISHED`  ·  signature: `(cache_dir=None)`
```python
>>> module.run('published_audit', {})['result']
{'bit_lengths': {'m': 3194897, 'a': 1597519, 'c': 1628205, 'maskone': 2496010, 'masktwo': 1697290, 'divver': 399362, 'ainverse': 3194897}, 'shared_constants_identical': { ...
```

**`published_roundtrip`** — Published forward and inverse transforms on the published constants
  params: `seed`, `cache_dir`  ·  confidence: `ESTABLISHED`  ·  signature: `(seed=1, cache_dir=None)`
```python
>>> module.run('published_roundtrip', {})['result']
{'location_bits': 3194895, 'value_bits': 3194895, 'inverse_of_forward_is_identity': True, 'forward_seconds': 0.030923034000807093, 'inverse_seconds': 0.051846487000148045 ...
```

**`published_multiplicity`** — Several locations show one image: bits of the transform the image never reads
  params: `seed`, `cache_dir`  ·  confidence: `ESTABLISHED`  ·  signature: `(seed=1, cache_dir=None)`
```python
>>> module.run('published_multiplicity', {})['result']
{'unread_bit_positions': 17, 'sampled_positions': [399360, 3194888, 3194896], 'witnesses': {399360: {'sibling_differs': True, 'forward_matches': True, 'same_image': True, ...
```

**`scrambler_cycles`** — Cycle structure of the scrambler: the spectrum of its permutation
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n=24389)`
```python
>>> module.run('scrambler_cycles', {})['result']
{'n': 24389, 'cycles': 11, 'longest': 9943, 'shortest': 1, 'fixed_points': 1, 'top_cycle_lengths': [9943, 6700, 6387, 770, 479, 34, 32, 28], 'single_cycle': False, 'lcg_a ...
```

**`published_sibling_structure`** — Sibling locations of one image: offsets add, and depend on the location
  params: `seed`, `cache_dir`, `pairs`  ·  confidence: `ESTABLISHED`  ·  signature: `(seed=1, cache_dir=None, pairs=6)`
```python
>>> module.run('published_sibling_structure', {})['result']
{'first_location': {'valid_unread_bits': 16, 'single_offsets_distinct': True, 'pairs_tested': 6, 'pairs_additive': True, 'all_bits_together_additive': True, 'offset_bit_l ...
```

### Shell commands

`babel` · `ordered` · `scale`


---

*Theory page: [`basile.md`](../basile.md).*
