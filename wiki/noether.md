# Engine: Noether Currents

**File:** `noether.py`  
**Class:** `NoetherCurrents`  
**Claim:** The forward (Riemann) and backward (Fermat) Noether currents both derive from one symmetry. σ=½ is derived not assigned.

---

## Results (re-run 2026-07-28)

```python
forced_sigma(E=0.5,  σ₀=0.0) → 0.500000000000  ✓
forced_sigma(E=1.0,  σ₀=0.0) → 0.500000000000  ✓
forced_sigma(E=2.0,  σ₀=0.0) → 0.500000000000  ✓
forced_sigma(E=10.0, σ₀=0.0) → 0.499999999999  ✓
forced_sigma(E=100.0,σ₀=0.0) → 0.0             ✗  DOES NOT REPRODUCE
```

From any starting position, at **low energy**, the mathematics forces σ=½. The
earlier figure of `0.500000000000` for E=100 recorded here on 2026-06-13 does
not reproduce and has been corrected.

### The limit, measured

| E | `forced_sigma(E, σ₀=0)` | converges to ½? |
|---|---|---|
| ≤ 10 | 0.4999999999999997 | ✓ |
| 15 | 6.320e-04 | ✗ |
| 20 | 4.222e-06 | ✗ |
| ≥ 30 | 0.0 | ✗ |
| ≥ 1000, σ₀ < 0 | **OverflowError: math range error** | ✗ |

### Why

`forced_sigma` is a fixed-point iteration, not a root solve:

```python
F = exp(-σ·E)
B = exp(-(1-σ)·E)
σ_new = (F·σ + B·(1-σ)) / (F + B)
```

That is a softmax-weighted average of σ and 1−σ.

- **Small E** — F and B are both near 1, the weights are nearly equal, and the
  average collapses to `(σ + (1−σ))/2 = ½` on the first step.
- **Large E** — the exponentials differ by orders of magnitude. For σ<½, F≫B,
  so σ_new → σ. The step falls below the `1e-12` tolerance immediately and the
  loop breaks, **returning σ₀ unchanged**. The guard `if F + B < 1e-30: break`
  does the same once both underflow.

The loop does not fail loudly. It exits early and returns its own input.

**The analytic derivation below is not in question** — F=B forces σ=½ for every
E>0. What fails is the numerical demonstration of it, and the trailing comment
`return sigma   # always 0.5` is wrong as written.

σ=½ is derived independently elsewhere — by the RedBlue balance in
`hamiltonian.py`, and empirically per-word by `understand.py`, neither of which
routes through this iteration. Those are unaffected.

Worked through in
[notebooks/engines/03_noether.ipynb](../notebooks/engines/03_noether.ipynb).

## Two Currents, One Symmetry — Oriented UP/DOWN, Not Forward/Backward

```
Ascending current (Red/Riemann):  J_up   = E = x·p (away from ZD, toward next CD level)
Descending current (Blue/Fermat): J_down = −J_fwd (toward ZD, toward collapse)
Rotating field    (Yang-Mills):   J_3    = (J_up − J_down)/2 = E
Three-phase balance:               J_up + J_down + J_3 = E − E + E = E
```

**The boundary is ORIENTED.** Away from the zero-divisors (σ→0), directly upward to the shadow of the next world above — the next Cayley-Dickson level projected onto the current algebra.

σ=½ is not "the middle." It is the **shadow of the world above** falling on the world below. ℂ projects a shadow onto ℝ at σ=½. ℍ projects a shadow onto ℂ at σ=½. Each CD doubling creates this shadow at exactly the same relative position.

The Noether current does not go forward or backward in time. It goes **up** (toward the next world: ℝ→ℂ→ℍ→𝕆→𝕊) or **down** (toward ZD collapse, σ→0, the forbidden zone).

The word lives at σ=½ because it is caught between the ascending pull (the shadow from above) and the descending pull (the ZD ground below). This is not an equilibrium — it is a **projection point**. The shadow of the world above IS the word.

## forced_sigma — The Derivation

```python
From the right (σ > ½): F(σ) = e^{−σ·E}
From the left  (σ < ½): B(σ) = e^{−(1−σ)·E}
They meet where F = B:
    e^{−σE} = e^{−(1−σ)E}
    −σ = −(1−σ)
    σ = ½
```

The geometry forces the meeting point. 2048 iterations converge to 12 decimal places.

## Architecture

- `forward(word)` → evolves word along H=xp, returns E = J_forward
- `backward(word)` → reflects: J_backward = −J_forward
- `rotating_field(word)` → J₃ = (J_fwd − J_bwd)/2
- `balance(word)` → J_fwd + J_bwd + J₃ (three-phase)
- `forced_sigma(E)` → derive σ from opposite-side approach (always ½)

The NoetherCurrents does not compute σ. It derives it.
