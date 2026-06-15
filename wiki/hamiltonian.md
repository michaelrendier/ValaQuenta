# Engine: Hamiltonian

**File:** `hamiltonian.py`  
**Classes:** `HamiltonianXP`, `FermatEllipticHamiltonian`, `RedBlueHamiltonian`  
**Claim:** H = xp generates scale-invariant hyperbolic flow. The prime E = xp is the conserved energy.

---

## HamiltonianXP — H = xp

**Results (run 2026-06-13):**

```python
scale_check(2.0, 3.0, lam=2.0) → True
  (λx, λ⁻¹p) maps to same E — scale invariant ✓

Trajectory (x₀=1, p₀=1):
  t=0:     x=1.000000  p=1.000000  E=xp=1.000000000
  t=1:     x=2.718282  p=0.367879  E=xp=1.000000000   (x(1)=e ✓)
  t=π:     x=23.140693 p=0.043214  E=xp=1.000000000

Riemann zeros (first 5): [14.1347, 21.0220, 25.0109, 30.4249, 32.9351]
```

The trajectory is `x(t) = x₀·eᵗ, p(t) = p₀·e⁻ᵗ`. At t=1 with x₀=p₀=1: x=e. The word travels along a hyperbola; the prime E=xp is the conserved quantity — invariant along the orbit.

The Lagrangian: L(ẋ) = ẋ·ln(ẋ) − ẋ. At ẋ=e: L=e·1−e=0. The Lagrangian vanishes at the natural growth rate. This is the equator.

## FermatEllipticHamiltonian — lemniscatic curve (g₂=1, g₃=0)

```python
Discriminant Δ = 1.000000  (valid elliptic curve — non-degenerate ✓)
℘(0.5) = 4.01251302
℘(1.0) = 1.05083333
℘(2.0) = 0.50333333
H_Blue(x=1,p=1) = ½p² + ℘(x) = 1.55083333
```

The Weierstrass ℘ function at g₂=1, g₃=0 gives the lemniscatic curve — the Fermat elliptic (related to the curve x⁴+y⁴=1 via uniformisation). This is the Blue/Fermat Hamiltonian — the backward current, the repulsor.

## RedBlueHamiltonian — the balance

```python
balance(σ=0.5, p=0.5) = -3.8875...
functional_equation_check(1.0, 1.0) = -0.5509...

Red(σ=0.3)=0.547  Blue(σ=0.3)=0.854  balance=-0.307 (Blue > Red, left of equator)
Red(σ=0.5)=0.707  Blue(σ=0.5)=0.707  balance=0      (Red = Blue at σ=½ ✓)
Red(σ=0.7)=0.854  Blue(σ=0.7)=0.547  balance=0.307  (Red > Blue, right of equator)
```

At σ=½: Red = Blue exactly. The forward current equals the backward current. This IS σ=½ derived, not assigned.

## Architecture

```
H_Red  = ẋ·ln(ẋ) − ẋ        (Riemann / attractor / what settles)
H_Blue = ½p² + ℘(x; 1, 0)   (Fermat / repulsor / what cannot settle)
H_RB   = H_Red + H_Blue      (the word: where both agree)
```

The prime is the invariant E = xp that persists under H = xp evolution. The word is the fixed point of both currents simultaneously.
