# The Archimedes Screw (Prime Coordinate Engine)

**Module:** `ValaQuenta.modules.archimedes_screw`
**Import:** `from ValaQuenta.modules.archimedes_screw.tools import ArchimedesScrewModule`
**Theory page:** [`../archimedes_screw.md`](../archimedes_screw.md)

---

`archimedes_screw` · v0.3 · confidence floor **THEORETICAL**

The machine that does the work, distinct from the medium it lifts: 0_RB is the water, the screw is the logarithm. Converts rotation into lift, one pitch of ln p per prime. Provides the four-coordinate search-term interface (Ordinal Value, Zeta Index Value, Number of Digits, Total Spaces Between) on the single axis u = ln x, bound by the von Mangoldt explicit formula. Chebyshev psi jumps by exactly ln p at x = p -- the leaf-drop event's magnitude IS the prime. Includes the Lambert-W inverse of the zero-counting function (the same W whose fixed point W(1) = OMEGA_ZS pins sigma = 1/2), the amplitude-envelope form of RH, and the N-specific ramification leg in Q(sqrt N) where the Euler factor degenerates at exactly the factors of N. Also carries the L_(I|O) slot decomposition: Chebyshev psi is the counterpart of L_(I|O) (the actual bent path), the main term x is L (the clean path of least primes), and the newly named zero_sum is the counterpart of the Fermat/lensing potential -- the bend. v0.2 adds the composite side the screw was blind to: the leaf falls at gpf(N) (14 = 2*7 falls at 7, not at 2), the fall-time distribution is Dickman rho in the coordinate u = lnN/ln(gpf N), the harvest at step p is Psi(X/p, p) in closed form, and fall_split reports the imbalance delta that is a semiprime's entire hidden content -- collapsing to zero for balanced RSA, which is why the two fall events coincide there. v0.3 adds the NEGATIVE SPACE psi had no counterpart for: mu is the exclusion operator, M(x)=SUM mu(n) is psi's mirror, RH on that side is M(x)=O(x^(1/2+eps)) -- the same 1/2 -- and sieve_extinction gives the THREE motions: grown (zeta), extinct at lpf (negative), identified at gpf (bulk). domain_ladder settles what 'the domain' means: not 2..N but 2..sqrt(N), only the primes in it, and restricting to exactly-size primes buys exactly ONE BIT because half of all primes below any bound live in the top octave. The only target that matters is GNFS at 2^112.

### Equations (`formulary()`)

Call any of these via `module.run('<name>', {params})`, or `module.viewer_data('<name>', {params}, 'text')` for a formatted string.

**`screw_coordinates`** — Search-term interface: four coordinates, one axis
  params: `term, value`  ·  confidence: `ESTABLISHED`  ·  signature: `(term, value)`

**`screw_pitch`** — One turn of the screw = one prime = lift of ln p
  params: `p`  ·  confidence: `ESTABLISHED`  ·  signature: `(p)`

**`chebyshev_psi_explicit`** — THE BINDING EQUATION: explicit formula on the screw axis
  params: `x, zeros`  ·  confidence: `ESTABLISHED`  ·  signature: `(x, zeros=None)`

**`zero_sum`** — THE PRIME-SIDE FERMAT POTENTIAL — the bend
  params: `x, zeros`  ·  confidence: `ESTABLISHED`  ·  signature: `(x, zeros=None)`

**`clean_path_L`** — L — the clean path: "the path of least primes", computed
  params: `x`  ·  confidence: `ESTABLISHED`  ·  signature: `(x)`

**`l_io_decomposition`** — The three L_(I|O) slots by role: L, psi_bend, L_IO
  params: `x, zeros`  ·  confidence: `THEORETICAL`  ·  signature: `(x, zeros=None)`

**`chebyshev_psi_exact`** — psi(x) by sieve -- the ground truth the tones rebuild
  params: `x`  ·  confidence: `ESTABLISHED`  ·  signature: `(x)`

**`shake_order`** — The shake order: every leaf-drop, in sequence, with its prime
  params: `x, zeros`  ·  confidence: `ESTABLISHED`  ·  signature: `(x, zeros=None)`

**`fall_height`** — WHEN THE LEAF FALLS: u_fall = ln(gpf N)
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n)`

**`discovery_height`** — Where the first strike lands: ln(lpf N)
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n)`

**`smoothness_u`** — The Dickman coordinate: u = ln N / ln(gpf N)
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n)`

**`dickman_rho`** — THE FALL-TIME DISTRIBUTION: Dickman rho(u)
  params: `u`  ·  confidence: `ESTABLISHED`  ·  signature: `(u)`

**`harvest`** — THE HARVEST: leaves falling at sieve step p
  params: `X, p`  ·  confidence: `ESTABLISHED`  ·  signature: `(X, p)`

**`semiprime_harvest`** — Two-parent leaves falling at step p
  params: `X, p`  ·  confidence: `ESTABLISHED`  ·  signature: `(X, p)`

**`fall_split`** — The birth record: both falls, delta, and the collapse
  params: `N`  ·  confidence: `ESTABLISHED`  ·  signature: `(N)`

**`mertens`** — THE NEGATIVE-SPACE STAIRCASE: M(x) = Σ μ(n)
  params: `x`  ·  confidence: `ESTABLISHED`  ·  signature: `(x)`

**`mobius`** — THE NEGATIVE-SPACE OPERATOR: μ, the Dirichlet inverse of 1
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n)`

**`mertens_envelope`** — RH on the exclusion side: M(x) = O(x^(1/2+eps))
  params: `x, eps`  ·  confidence: `ESTABLISHED`  ·  signature: `(x, eps=0.0)`

**`sieve_extinction`** — THE THREE-MOTION RECORD: grown / extinct / identified
  params: `N`  ·  confidence: `ESTABLISHED`  ·  signature: `(N)`

**`domain_ladder`** — THE PROJECTION LEDGER: what the domain actually is
  params: `modulus_bits, gnfs_bits`  ·  confidence: `ESTABLISHED`  ·  signature: `(modulus_bits=2048, gnfs_bits=112.0)`
```python
>>> module.run('domain_ladder', {})['result']
{'all_integers': 2048.0, 'integers_to_sqrt': 1024.0, 'primes_to_sqrt': 1014.5308032728003, 'primes_exact_size': 1013.5293903247435, 'gnfs': 112.0, 'saving_sqrt_bound': 1024.0, 'saving_primes_only': 9.469196727199687, 'saving_size_restriction': 1.0014129480567817, 'saving_gnfs': 901.5293903247435}
```

**`zero_height_lambert`** — Lambert inverse of the zero count: gamma_n = 2*pi*n/W(n/e)
  params: `n`  ·  confidence: `ESTABLISHED`  ·  signature: `(n)`

**`zero_count_smooth`** — Riemann-von Mangoldt zero count N(T)
  params: `T`  ·  confidence: `ESTABLISHED`  ·  signature: `(T)`

**`amplitude_envelope`** — RH in the prime domain: one shared envelope 2*sqrt(x)
  params: `x, sigma`  ·  confidence: `THEORETICAL`  ·  signature: `(x, sigma=0.5)`

**`envelope_ratio`** — How loudly an off-line zero would drown the others
  params: `x, sigma_off`  ·  confidence: `ESTABLISHED`  ·  signature: `(x, sigma_off)`

**`interference_profile`** — Per-zero tones at x -- primes are the antinodes
  params: `x, zeros`  ·  confidence: `ESTABLISHED`  ·  signature: `(x, zeros=None)`

**`prime_count_log10`** — log10 pi(10^d) -- the finiteness readout at RSA scale
  params: `digits`  ·  confidence: `ESTABLISHED`  ·  signature: `(digits)`

**`splitting_vector`** — chi_N readout: the cheapest N-specific shadow there is
  params: `N, limit`  ·  confidence: `ESTABLISHED`  ·  signature: `(N, limit=100)`

**`ramified_primes`** — Ramification = detachment: Euler factor degenerates at the factors
  params: `N, limit`  ·  confidence: `THEORETICAL`  ·  signature: `(N, limit=1000000)`

**`lambert_w`** — The screw gear ratio: W(x)e^{W(x)} = x, W(1) = OMEGA_ZS
  params: `x`  ·  confidence: `ESTABLISHED`  ·  signature: `(x)`

### Shell commands (`shell_commands()`)

Direct callables for the QTermWidget shell interface:

`screw`, `pitch`, `psi`, `psi_tones`, `zero_sum`, `L`, `slots`, `fall`, `disc`, `gpf`, `lpf`, `u`, `rho`, `harvest`, `crop`, `sp_harvest`, `birth`, `ladder`, `mu`, `M`, `M_bound`, `extinct`, `shake`, `gamma`, `gamma_w`, `N`, `tones`, `envelope`, `drown`, `chi`, `ramified`, `W`, `pi_log10`

---

### Running via the registry

```python
from ValaQuenta.modules.archimedes_screw.tools import ArchimedesScrewModule

m = ArchimedesScrewModule()
m.formulary()                              # list every Equation this module exposes
m.run('screw_coordinates', {})                     # -> {'result': ..., 'equation': ..., 'params': ...}
m.viewer_data('screw_coordinates', {}, 'text')     # -> {'text': '...formatted...'}
```
