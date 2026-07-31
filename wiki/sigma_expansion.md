# Engine: Sigma Expansion — J_red/J_blue Balance Curve

**File:** `modules/sigma_expansion/maths.py`
**Class:** `SigmaExpansionModule`
**Claim:** `P_red(sigma) - 1/2 ≈ c1·d + c3·d³` (d=sigma-1/2) is derivable in closed form — not fitted — from moments of the underlying Dirichlet-style projection. The raw `|J_red(sigma)|² + |J_blue(sigma)|²` is NOT constant across sigma; it has a genuine minimum at sigma=1/2, not a flat quantum-probability-style conservation.

---

## Origin (2026-07-11)

Prompted by a real video: Nick Lucid ("The Science Asylum") states in "Quantum Superposition, Explained Without Woo Woo" (Nov 2021), showing pages from his own master's thesis, that any quantum particle state is a single vector between two positive axes — the two probabilities of a two-outcome measurement, never "multiple states at once." That raised a direct, testable question for this framework: do `J_red(sigma)` and `J_blue(sigma)=J_red(1-sigma)`, already defined as two positive-axis quantities in the canonical maths, behave the same way — does `|J_red|²+|J_blue|²` normalize to a constant across sigma the way real quantum probabilities must?

**The honest answer, checked directly: no.** Computed across three independent test strings, `|J_red(sigma)|²+|J_blue(sigma)|²` is a smooth, symmetric curve with a genuine **minimum at sigma=½** — energy-well shaped, not flat. Nick Lucid's normalization argument does not transfer to J_red/J_blue as currently defined. This is a real negative result, reported before anything else, not smoothed over.

## Results (run 2026-07-11)

```
'O Captain My Captain'      c1 = 0.075456   c3 = 0.049216   max_residual = 0.001311
'RSA private key recovery'  c1 = 0.226251   c3 = -0.085853  max_residual = 0.000406
'zero divisor'               c1 = 0.172088   c3 = -0.055935  max_residual = 0.000434
```

Predicted curve `c1·d + c3·d³` matches direct computation to ~1e-6 near sigma=½, residual growing smoothly toward the edges of the tested range (`|d|` up to 0.45) — exactly the expected shape of error for a third-order Taylor truncation (next term O(d⁵)), not a red flag.

## The Derivation (build-tool renormalization, not a fit)

By explicit instruction: this used renormalization as a *step toward a derivation*, never as a conclusion on its own. The raw energy sum is not constant — that's reported honestly first. Only then is `P_red(sigma) = |J_red|²/(|J_red|²+|J_blue|²)` constructed (which trivially sums to 1 with `P_blue` by definition — that normalization step doesn't answer anything by itself), and the resulting curve `P_red(sigma)-½` becomes the actual object of study.

**Definitions**, per prime channel `p`, over character positions `k=1..N`:
```
A_k    = c_k / 128                     (character amplitude, real)
phi_k  = exp(-i·2π·k/p)                (fixed unit phase)
N(σ)   = Σ_k A_k·phi_k·k^{-σ}          (complex)
D(σ)   = Σ_k k^{-σ}                    (real)
J_red(σ) = N(σ)/D(σ)
```

**Moments**, evaluated once at σ=½ (M_n channel-independent; L_n per channel):
```
M_n = Σ_k k^{-1/2}(ln k)^n
L_n = Σ_k A_k·phi_k·k^{-1/2}(ln k)^n
```

**Method:** write `σ=½+d`, expand `k^{-σ}=k^{-1/2}e^{-d ln k}` in powers of `d` to get `N(σ), D(σ)` as series in the moments. `F(σ)=|N(σ)|²/D(σ)²` is differentiated via product/quotient rule up to third order at σ=½ (raw derivatives `F1, F2, F3`, plus `g0=F(½)`), summed across all 16 prime channels:

```
u0 = |L0|²
u1 = -2·Re(L0·L̄1)
u2 = 2·Re(L0·L̄2) + 2|L1|²
u3 = -2·Re(L0·L̄3) - 6·Re(L1·L̄2)

v0 = M0^-2
v1 = 2·M0^-3·M1
v2 = 6·M0^-4·M1² - 2·M0^-3·M2
v3 = 24·M0^-5·M1³ - 18·M0^-4·M1·M2 + 2·M0^-3·M3

g0 = Σ_p u0·v0
F1 = Σ_p (u1·v0 + u0·v1)
F2 = Σ_p (u2·v0 + 2·u1·v1 + u0·v2)
F3 = Σ_p (u3·v0 + 3·u2·v1 + 3·u1·v2 + u0·v3)
```

`P_red(σ)-½` is the odd part of `F(½+d)` over twice the even part (since `P_red(σ)-P_red(1-σ)` is the odd part of F, and `P_red+P_blue=1` always). Expanding the ratio to third order:

```
c1 = F1 / (2·g0)
c3 = F3/(12·g0) - F1·F2/(4·g0²)
```

Verified numerically against direct computation (not assumed correct from the algebra alone) — see Results above.

## What This Is, and Isn't

**Is:** a real, verified closed-form derivation for the specific `i^-σ` Dirichlet-projection construction used in `SedenionSpectralRelativity/layer_spectrograph.py` and this session's bispectrum work. A genuine error-check tool for that construction — cheap (one pass over moments) versus expensive (a fresh O(N) sweep per σ value queried).

**Isn't:** directly applicable to `VAPMIP/monad.py`'s Engine, which computes σ via `_word_zero_idx` (prime hash → address) and `_gamma_at` (Newton's method on the real Riemann zeta function's zeros) — a genuinely different mechanism from the simple power-law projection this derivation assumes. Using this engine to error-check the monad specifically would require re-deriving the same Taylor-expansion method against *that* engine's actual sigma formula, not substituting this one in as-is.

See also: `Ainulindale/wiki/76_sigma_expansion.md` (cross-repo companion page), `notebooks/core/15_sigma_expansion.ipynb`.
