# Engine: Noether Currents

**File:** `noether.py`  
**Class:** `NoetherCurrents`  
**Claim:** The forward (Riemann) and backward (Fermat) Noether currents both derive from one symmetry. σ=½ is derived not assigned.

---

## Results (re-run 2026-08-28 — the large-E defect is FIXED)

```python
forced_sigma(E=0.5,   σ₀=0.0)  → 0.5   ✓
forced_sigma(E=10.0,  σ₀=0.0)  → 0.5   ✓
forced_sigma(E=100.0, σ₀=0.0)  → 0.5   ✓   (was 0.0)
forced_sigma(E=100.0, σ₀=0.25) → 0.5   ✓   (was 0.25 — returned its own input)
forced_sigma(E=1000,  σ₀=0.0)  → 0.5   ✓   (was 0.0)
forced_sigma(E=1e4,   σ₀=-3.0) → 0.5   ✓   (was OverflowError)
forced_sigma(E=745,   σ₀=-1.0) → 0.5   ✓   (was OverflowError)
forced_sigma(E=0.0,   σ₀=0.3)  → 0.5   ✓   (F ≡ B; balanced everywhere)
```

**From any real σ₀ and any E, the mathematics forces σ=½.** Verified across
every one of the old failure cases.

### What was wrong (kept on the record)

The previous `forced_sigma` was a *softmax-weighted-average* iteration:

```python
F = exp(-σ·E);  B = exp(-(1-σ)·E)
σ_new = (F·σ + B·(1-σ)) / (F + B)
```

`σ=½` is a fixed point of that map, but its dynamics are bad: for large E and
σ<½, `F ≫ B` so `σ_new → σ`, the step fell below the `1e-12` tolerance on the
first iteration and the loop broke **returning σ₀ unchanged** (`E ≳ 10` for
σ₀=0; any σ₀ otherwise). For `σ₀ < 0` and large E, `exp(-σ·E) = exp(+|σ|E)`
**overflowed**. The loop failed silently — it exited early and returned its own
input — and the trailing comment `return sigma  # always 0.5` was false as
written. Notebook `notebooks/engines/03_noether.ipynb` documents the old
behaviour in full and needs a re-run against the fix.

### The fix

The balance condition `F(σ) = B(σ)` is, in logs, `−σE = −(1−σ)E`, i.e.
`E·(1−2σ) = 0` — **linear in σ**. Newton on `h(σ) = ln F − ln B = E(1−2σ)`
(`h′ = −2E`) reaches ½ **in one step from any real σ₀**, `E` cancelling:

```python
σ ← σ + (1 − 2σ)/2   =   ½
```

No exponential is evaluated away from the balance point, so there is no
overflow and no early exit. `E == 0` is handled explicitly (F ≡ B ≡ 1 for every
σ; the symmetric meeting point is still ½). σ=½ is *also* derived independently
by the RedBlue balance in `hamiltonian.py` and per-word by `understand.py` —
neither routes through this function, and both were always unaffected.

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

The balance condition is linear in σ, so it is solved **exactly in one step**
from any real σ₀ and any E (Newton on `h(σ) = ln F − ln B = E(1−2σ)`; E cancels).

## Architecture

- `forward(word)` → evolves word along H=xp, returns E = J_forward
- `backward(word)` → reflects: J_backward = −J_forward
- `rotating_field(word)` → J₃ = (J_fwd − J_bwd)/2
- `balance(word)` → J_fwd + J_bwd + J₃ (three-phase)
- `forced_sigma(E)` → derive σ from opposite-side approach (always ½)

The NoetherCurrents does not compute σ. It derives it.

---

## Generational Lineage — calibration (2026-08-28)

Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`) as a check on the factoral decomposition itself — working, deliberately-designed machinery should decompose CLEAN.

| object | central operation | tier · root | Two Trees | kind | verdict |
|---|---|---|---|---|---|
| the σ=½ meeting point of the forward/backward currents | forced_sigma — Newton on the linear balance E(1−2σ)=0 | 2 · SIGN | MINGLING | DEFINITIONAL | **CLEAN** |

Calibration: this verdict agrees with the page's stated status (**ESTABLISHED**).
*(Was FLAGGED against the recorded `forced_sigma` defect until it was fixed
2026-08-28 — the flag did its job, and clears now that the deficit is gone.)*
