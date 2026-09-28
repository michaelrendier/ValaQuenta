# Engine: Spectral Representation of the Primes (spin / wobble)

**Module:** `modules/spectral_primes/` (`maths.py`, `tools.py`)
**Class:** `SpectralPrimesModule`
**Claim:** the Riemann-Siegel theta-spiral splits into a *spin* (the major loop, θ′(t), non-resonant) and a *wobble* (the minor loop, resonant at the primes). Primes are the wobble's genuine spectral content — classical von Mangoldt/Weil, demonstrated by reconstructing ψ(x) from the same zero set.
**Status:** `OPEN` for the two new hypotheses below; the classical parts are `ESTABLISHED`.

---

## Results (run, 60 zeros)

```python
spin_is_monotonic(n_zeros=60)
  n_non_monotonic = 0            # no resonance in the spin           ESTABLISHED
  range           = [0.4053, 1.6280]

tilt_vs_wobble_correlation(n_zeros=60)
  correlation = 0.0367           # REFUTED AS TESTED
  # tilt is sampled pointwise at each zero; wobble is an interval quantity between
  # consecutive zeros. An interval-averaged tilt is a named follow-up, not done.

crossing_does_not_drift(n_zeros=60, n_test=5)
  crossing sigma = 0.5 at gamma = 14.1347, 21.0220, 25.0109, 30.4249, 32.9351
  min |value|    ~ 1e-30 at each     # pinned at sigma = 0.500000 to machine precision
```

The crossing of the Real Tilt and the central t-axis is an isolated, simple zero. It moves up the t-axis, a new crossing at each γₙ, and never sideways in σ.

## Open

- Tilt = wobble by minimum-information identification: refuted as tested (correlation ≈ 0.037). The pointwise-versus-interval sampling gap is named and left open.

## Reference

Every equation with its parameters: [toolbox](toolbox/17_spectral_primes.md) · API: [spectral_primes](https://michaelrendier.github.io/ValaQuenta/api/modules/spectral_primes.html).

---

## Provenance

Moved from the module docstring: a docstring instructs the caller and holds no history; this section is the record.

> Born 2026-09-26 from a live conversation walking the theta(t)-rotation
> construction through: two spirals (carrier vs trajectory) -> spin (major
> loop, theta'(t), non-resonant) vs wobble (minor loop, resonant at the
> primes) -> "primes are the spin... and wobble" -> corrected: primes are
> the wobble's genuine spectral content (classical Weil/von Mangoldt), not
> an artifact of it -> the crossing of the Real Tilt (the real-axis domain,
> not Re(z)) and the Axis (the central t-axis of the helix).
