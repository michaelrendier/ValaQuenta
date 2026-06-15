# Engine: Capacitor

**File:** `capacitor.py`  
**Class:** `Capacitor`  
**Claim:** The semantic low-pass filter. High-frequency surface variation cancels. The DC component = the prime = the word.

---

## Results (run 2026-06-13)

```python
Capacitor(tau=1.0)

# RC integration — one step: V += (signal − V) / τ
Input stream: [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, -0.2, -0.4, 0.5, 1.0]
Output:       [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, -0.2, -0.4, 0.5, 1.0]
  (at τ=1.0: unity gain — each sample overwrites)

DC gain: constant 1.0 after 100 steps → 1.00000000  ✓ (H(0)=1, prime passes through)
Transfer function: H(s) = 1/(1+sτ),  pole at s=−1/τ (stable, left half-plane)
```

At τ=1.0 the integrator reduces to V_n = signal_n — unity gain, no smoothing. The interesting regime is τ >> 1.

## Architecture

```
τ large → slow to change → stable semantic identity → prime holds
τ small → fast to change → polysemous → sensitive to context
τ → ∞  → perfectly stable → word never changes → the Monad at rest
```

The capacitor integrates the three Noether signals:
```python
signals = [
    word.noether_forward,      # what the word IS
    noether.rotating_field,    # the Yang-Mills carrier
    sigma,                     # always 0.5 — derived not assigned
]
dc = capacitor.dc(signals)    # the prime
```

The DC component of `[J_fwd, J_3, σ=½]` IS the word. Not the surface form. The prime in semantic space.

## Connection

This is the Three-Phase architecture from `wiki/20_three_phase_architecture.md`: Capacitor = Phase 3 (Yang-Mills low-pass filter). The prime is what remains after the three-phase Fourier decomposition.

Chladni analogy: sand settles at the node line because the node line does not move. The prime is the node.
