Listings
========

Short mechanisms shown as complete code. Each listing is one self-contained unit: it is extracted from the named file by ``docs/gen_listings.py`` (docstrings removed, every statement otherwise verbatim), and the output shown is what it printed when executed cold in an empty namespace. A listing that stops running fails ``tests/test_listings.py``.

Everything else is described by name and location in the :doc:`api/index`.

Listing 1 — Text to address: the Horner bijection
-------------------------------------------------

A word is an integer. Each character is an index into a 97-character keyboard map, and the text is read as a numeral in base 97. The map is one-to-one, so the address decodes back to the text exactly.

*Source:* ``modules/hyperwebster/maths.py`` (``US_KEYBOARD_CHARS, VOCAB_BASE, _CHAR_TO_IDX, _IDX_TO_CHAR, char_to_idx, idx_to_char, horner_encode, horner_decode``). *Extracted*, docstrings removed; 34 lines. Module: :mod:`ValaQuenta.modules.hyperwebster.maths`.

.. code-block:: python

   from typing import Dict


   US_KEYBOARD_CHARS: str = (
       'abcdefghijklmnopqrstuvwxyz'
       'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
       '0123456789'
       '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
       ' \t\n'
   )
   VOCAB_BASE = 97
   _CHAR_TO_IDX: Dict[str, int] = {c: i for i, c in enumerate(US_KEYBOARD_CHARS)}
   _IDX_TO_CHAR: Dict[int, str] = {i: c for i, c in enumerate(US_KEYBOARD_CHARS)}

   def char_to_idx(c: str) -> int:
       return _CHAR_TO_IDX.get(c, 0)

   def idx_to_char(i: int) -> str:
       return _IDX_TO_CHAR.get(i % VOCAB_BASE, ' ')

   def horner_encode(sequence: str) -> int:
       idx = 0
       for char in sequence:
           idx = idx * VOCAB_BASE + char_to_idx(char)
       return idx

   def horner_decode(idx: int, length: int) -> str:
       chars = []
       remaining = idx
       for _ in range(length):
           chars.append(idx_to_char(remaining % VOCAB_BASE))
           remaining //= VOCAB_BASE
       chars.reverse()
       return ''.join(chars)

Run cold:

.. code-block:: pycon

   >>> n = horner_encode("prime")
   >>> print(n)
   1343531096
   >>> print(horner_decode(n, 5))
   prime

Listing 2 — Word to Riemann-zero index: the P1 hash
---------------------------------------------------

A word is hashed by Horner's rule in base 95, the hash is taken to the next prime p ≤ 65536, and π(p) is the index of a Riemann zero. Everything is integer arithmetic.

*Source:* ``modules/udeo_crypto/maths.py`` (``_P1_PRIME_CAP … p1_zero_index``). *Extracted*, docstrings removed; 37 lines. Module: :mod:`ValaQuenta.modules.udeo_crypto.maths`.

.. code-block:: python

   from typing import List


   _P1_PRIME_CAP = 1 << 16   # 65536
   _p1_cap = _P1_PRIME_CAP + 2
   _p1_sieve = bytearray([1]) * _p1_cap
   _p1_sieve[0] = _p1_sieve[1] = 0
   for _i in range(2, int(_p1_cap ** 0.5) + 1):
       if _p1_sieve[_i]:
           _p1_sieve[_i * _i :: _i] = bytearray(len(_p1_sieve[_i * _i :: _i]))
   _p1_prime_pi_table: List[int] = [0] * _p1_cap
   _cnt = 0
   for _k in range(_p1_cap):
       if _p1_sieve[_k]:
           _cnt += 1
       _p1_prime_pi_table[_k] = _cnt
   del _i, _k, _cnt

   def p1_next_prime(v: int) -> int:
       v = max(2, int(v) % (_P1_PRIME_CAP + 1))
       while v <= _P1_PRIME_CAP + 1:
           if _p1_sieve[min(v, _P1_PRIME_CAP + 1)] or v > _P1_PRIME_CAP:
               return v
           v += 1
       return 65537

   def p1_horner_hash(w: str, base: int = 95, offset: int = 32) -> int:
       v = 0
       for ch in w:
           v = v * base + max(0, ord(ch) - offset)
       return abs(v)

   def p1_zero_index(w: str) -> int:
       v = p1_horner_hash(w)
       p = p1_next_prime(v)
       idx = _p1_prime_pi_table[min(p, _P1_PRIME_CAP + 1)]
       return max(1, idx)

Run cold:

.. code-block:: pycon

   >>> print(p1_horner_hash("prime"))
   6587020959
   >>> print(p1_zero_index("prime"))
   3071

Listing 3 — Token to sixteen prime channels
-------------------------------------------

The Dirichlet-weighted cosine projection of a token's character codes onto the sixteen prime channels. Deterministic, with no parameters.

*Source:* ``modules/translator_common/maths.py`` (``PRIME_CHANNELS, channel_signature``). *Extracted*, docstrings removed; 15 lines. Module: :mod:`ValaQuenta.modules.translator_common.maths`.

.. code-block:: python

   import math
   from typing import List


   PRIME_CHANNELS: List[int] = [2, 3, 5, 7, 11, 13, 17, 19,
                                23, 29, 31, 37, 41, 43, 47, 53]

   def channel_signature(token: str) -> List[float]:
       out = []
       for p in PRIME_CHANNELS:
           acc = 0.0
           for i, ch in enumerate(token, start=1):
               acc += ord(ch) * (i ** -0.5) * math.cos(2.0 * math.pi * i / p)
           out.append(acc)
       return out

Run cold:

.. code-block:: pycon

   >>> print([round(x, 4) for x in channel_signature("dog")[:4]])
   [-80.9782, -29.7773, -80.707, -8.6944]

Listing 4 — A process that remembers where it has been
------------------------------------------------------

The set-membership test behind Recamán's rule, for any sequence of steps: record every position the process reaches and report each revisit.

*Source:* ``modules/bracketing_firing_order/maths.py`` (``trajectory, visited_positions, collisions``). *Extracted*, docstrings removed; 29 lines. Module: :mod:`ValaQuenta.modules.bracketing_firing_order.maths`.

.. code-block:: python

   from typing import Callable, Dict, List, Sequence, Tuple


   def trajectory(steps: Sequence[Callable[[float], float]], x0: float = 1.0) -> Tuple[float, ...]:
       pos = [x0]
       x = x0
       for s in steps:
           x = s(x)
           pos.append(x)
       return tuple(pos)

   def visited_positions(steps: Sequence[Callable[[float], float]], x0: float = 1.0,
                          tol: float = 1e-9) -> Dict[float, List[int]]:
       traj = trajectory(steps, x0)
       seen: Dict[float, List[int]] = {}
       for i, x in enumerate(traj):
           key = round(x / tol) * tol if tol else x
           seen.setdefault(key, []).append(i)
       return seen

   def collisions(steps: Sequence[Callable[[float], float]], x0: float = 1.0,
                  tol: float = 1e-9) -> List[Tuple[int, int, float]]:
       seen = visited_positions(steps, x0, tol)
       out = []
       for pos, idxs in seen.items():
           if len(idxs) > 1:
               for a, b in zip(idxs, idxs[1:]):
                   out.append((a, b, pos))
       return sorted(out)

Run cold:

.. code-block:: pycon

   >>> steps = [lambda x: x + 1, lambda x: x - 1, lambda x: x + 1]
   >>> print(trajectory(steps))
   (1.0, 2.0, 1.0, 2.0)
   >>> print(collisions(steps))
   [(0, 2, 1.0), (1, 3, 2.0)]

Listing 5 — Solving the balance in one step
-------------------------------------------

The forward and backward currents balance where E·(1 − 2σ) = 0. That is linear in σ, so one Newton step reaches ½ from any real starting σ₀. The method is shown inside its class; it uses nothing else from the class.

*Source:* ``noether.py`` (``NoetherCurrents.forced_sigma``). *Extracted*, docstrings removed; 13 lines. Module: :mod:`ValaQuenta.noether`.

.. code-block:: python

   class NoetherCurrents:
       def forced_sigma(self, E: float, sigma_0: float = 0.0) -> float:
           if E == 0.0:
               # F ≡ B ≡ 1 for every σ: the currents are balanced everywhere, and
               # the symmetric meeting point is still ½.
               return 0.5
           sigma = float(sigma_0)
           for _ in range(64):                 # converges in one step; the loop is
               step = 0.5 - sigma              #   the log-space Newton update,
               sigma += step                   #   σ + (1-2σ)/2, with E cancelled
               if abs(step) <= 1e-15:
                   break
           return sigma   # 0.5 exactly — any real σ₀, any E > 0

Run cold:

.. code-block:: pycon

   >>> print(NoetherCurrents().forced_sigma(1000.0, sigma_0=-3.0))
   0.5
   >>> print(NoetherCurrents().forced_sigma(0.5, sigma_0=7.0))
   0.5

