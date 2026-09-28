# Engine: UDEO RSA key recovery — six mechanisms, honestly scored

**Module:** `modules/udeo_crypto/` (`maths.py`, `tools.py`)
**Class:** `UDEOCryptoModule`
**Claim tested:** whether a sedenion / zero-divisor / Zero-Lattice mechanism recovers an RSA private exponent d from the public key (n, e).
**Status:** `OPEN` — no mechanism takes only (n, e) and outputs d. One classical result is `ESTABLISHED`.

---

## Results (run, 6 toy keys, 200 valid wrong guesses per key)

Each method is scored as a percentile rank: how unusual the true d looks under that method's geometry against the random-but-valid wrong guesses. 50 is indistinguishable from chance.

| method | mean percentile | verdict |
|---|---|---|
| 1 — zero-divisor shadow (𝕊¹⁶) | 38.5 | at chance |
| 1b — Ptolemy NULL operator | 18.79 | generic hash artifact: true-e mean 18.8 vs unrelated-e mean 17.8 |
| 2 — J₂ involution / T₂₅₆ eigenspectrum | 33.33 | weak, inconsistent |
| 3 — Sedenion Spectral Relativity geodesic | 38.82 | at chance |
| 4 — Content + Public + Private = Hash | 0.0 | exact, but only when Hash is exposed, and not unique |
| 5 — Zero Lattice paths, public key only | 50.45 | at chance |
| 6 — emergent rotation signature | 52.59 | at chance on 40 keys (the 6-key sample showed 31.2 and did not survive scale-up) |

`mod4_identity_theorem` is proven, not statistical: d ≡ e (mod 4) for every RSA key with odd primes. It follows because 4 | φ(n), so ed ≡ 1 (mod 4), and (ℤ/4ℤ)\* has exponent 2. It removes one bit of the search space, has no connection to the sedenion framework, and is cryptographically insignificant at real key sizes (2000/2000 random keys satisfy it).

## What this page records

- Methods 4 and 5 (Hash-exposed) are exact only when a value that itself requires d is separately exposed. Neither is a public-key-only attack.
- Method 1b looked strong on both the 6-key and 40-key tests; a control that replaced e with an unrelated exponent produced the same bias, so it is an artifact of the hash construction.

## Reference

Every equation with its parameters: [toolbox](toolbox/38_udeo_crypto.md) · API: [udeo_crypto](https://michaelrendier.github.io/ValaQuenta/api/modules/udeo_crypto.html).

---

## Provenance

Moved from the module docstring: a docstring instructs the caller and holds no history; this section is the record.

> Author:  Claude, at Cody's direction — 2026-07-09
> Version: 0.100 — first pass, all three methods, all honestly scored
