# Engine: PrimeGate

**File:** `prime_gate.py`
**Classes:** `BoundaryAlarm`, `PrimeGateEngine`
**Claim:** `BoundaryAlarm` is the reusable primitive — fires once per crossing of a boundary condition, blind to everything except that the crossing happened. π(x) is `BoundaryAlarm(is_prime)` scanned over the integers; the Holcus FIRING signal (Ainulindale wiki/44, a computation reaching σ=½) is the same primitive scanned over a σ-trajectory instead. The engine's purpose is the alarm — not a test of any dataset.

---

## BoundaryAlarm — the reusable primitive

```python
alarm = BoundaryAlarm(boundary_fn)
alarm.scan(sequence)        # every (index, value) where boundary_fn fired, in order
alarm.count_at(sequence, upto)   # how many crossings by position `upto`
```

Any `boundary_fn: value -> bool` works. Two instantiations on record:

```python
sigma_half_alarm([0.1, 0.3, 0.45, 0.4999995, 0.5000003, 0.7, 0.5000001, 0.9], eps=1e-5)
  -> fires at [(3, 0.4999995), (4, 0.5000003), (6, 0.5000001)]
```

That's the Holcus-style crossing detector (wiki/44's "does it stop HERE, at this depth" reframe) built on the exact same primitive as the prime gate below — proof the alarm isn't prime-specific.

## PrimeGateEngine — the prime instantiation

**Results (limit=50000, 5133 primes):**

```python
gate_alarm(200) = 46            # 46 primes <= 200 -- fast bisection path
BoundaryAlarm(e.is_prime).count_at(range(2,201), 199) = 46   # equivalent, slower, general path
alarm_events[:5] = [(2,1), (3,2), (5,3), (7,4), (11,5)]   # (prime, pi(prime))
```

π(x) is a monotone staircase: it steps up by exactly 1 at each prime and is flat everywhere else. Every alarm event is identical regardless of the gap that preceded it — gap-blind by construction, not by approximation. `gate_alarm` is a fast bisection shortcut; `BoundaryAlarm(is_prime)` is the same result via the general primitive, kept as an equivalence check.

## The Gap Channel — deliberately not part of the alarm

```python
gap_scaling_fit() -> {
  slope: 0.9615, intercept: 0.4264, n_gaps: 5132,
  pnt_prediction: 'slope ~ 1.0 (average gap near p ~ ln(p))'
}
```

g_n = p_(n+1) − p_n carries everything the alarm leaves out: the size-14 gap near x≈108 (limit=200 run) is a single indistinguishable step in π(x) but a visible spike in g_n. Linear regression of g_n against ln(p_n) gives slope ≈ 0.96 ≈ 1 — numerical confirmation of the PNT average-gap prediction. This is a separate query, only pulled in when a task actually needs spacing, not folded into the alarm.

## Two Spirals — Ordinal vs Value Address

```python
ordinal_spiral()[-1] = (-2598.8, 4426.5)     # T(n) = n * e^{i d* ln n}
value_spiral()[-1]   = (-44350.4, 23085.5)   # T(p_n) = p_n * e^{i d* ln p_n}
```

`ordinal_spiral` addresses by **count** — matches the P1 hash convention already running in `monad.py` (`word → prime p → π(p) ordinal index → γ_index`), and is gap-blind by the same design choice as the alarm itself. `value_spiral` addresses by **magnitude** — radius grows as p_n ~ n·ln(n) (PNT), a genuinely different curve, not a rescaled copy.

## Architecture

```
BoundaryAlarm(boundary_fn)  -- THE ENGINE: general crossing detector
  |- is_prime  -> PrimeGateEngine.gate_alarm  = pi(x)
  |- |sigma-1/2|<eps -> sigma_half_alarm      = Holcus FIRING (wiki/44)

GAP g_n          -- interval channel, deliberately outside the alarm
ORDINAL T(n)     -- spiral addressed by count (P1 hash convention)
VALUE   T(p_n)   -- spiral addressed by magnitude (PNT growth n*ln n)
```

## Aside — not the engine's purpose, kept on record

A side investigation happened while building this: does prime-gap curvature look like a true Euler spiral (clothoid)? `curvature_spiral` (heading from κ_n=ln(p_n), correcting an earlier `cumsum(gap_n)` attempt that telescoped trivially back to p_n−p_0) and `is_true_euler_spiral` answer **no** — ln(p_n) never reverses sign, so the curve only ever tightens into one inward spiral, never the clothoid's two-eye structure. True, and on record, but a tangent from the alarm — not what this engine is for.
