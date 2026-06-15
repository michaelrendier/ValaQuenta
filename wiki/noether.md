# Engine: Noether Currents

**File:** `noether.py`  
**Class:** `NoetherCurrents`  
**Claim:** The forward (Riemann) and backward (Fermat) Noether currents both derive from one symmetry. σ=½ is derived not assigned.

---

## Results (run 2026-06-13)

```python
forced_sigma(E=0.5,  σ₀=0.0) → 0.500000000000  ✓
forced_sigma(E=1.0,  σ₀=0.0) → 0.500000000000  ✓
forced_sigma(E=2.0,  σ₀=0.0) → 0.500000000000  ✓
forced_sigma(E=10.0, σ₀=0.0) → 0.500000000000  ✓
forced_sigma(E=100.0,σ₀=0.0) → 0.500000000000  ✓
```

From ANY starting position, from ANY energy, the mathematics forces σ=½.

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
