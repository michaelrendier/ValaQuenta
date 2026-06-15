# Engine: SemanticDomain

**File:** `semantic_domain.py`  
**Class:** `SemanticDomain`  
**Claim:** The description creates the domain. The domain selects which Riemann zeros (instruments) can play. The music creates the instruments.

---

## Results (run 2026-06-13)

```python
U = Understand()
domain = U.describe("mass gap Yang-Mills quantum field theory")
  description: 'mass gap Yang-Mills quantum field theory'
  γ_min: 52.9703
  γ_max: 65.1125
  coherence_time: 13.0 zeros
```

The description maps to a Riemann zero γ_center, then spans ±half_width zeros. Width derives from description complexity (token count ÷ 3).

## Architecture

```
describe(text)
  → read(text)            ← find center zero
  → center_idx           ← index of nearest Riemann zero
  → half_width = max(1, len(tokens) // 3)
  → [lo, hi] window      ← the active instruments
  → SemanticDomain(γ_min, γ_max)

word placement within domain:
  angle t ∈ [0,1]  → snap to nearest zero within [lo, hi]
```

## Thermal Interpretation

```
coherence_time(zeros) = number of active zeros in domain

Cold domain (many zeros): τ large → meaning stable → strong semantic identity
Hot domain (few zeros):   τ small → meaning volatile → polysemous

At domain collapse (is_collapsed): τ = 1
  → Hawking radiation: all meaning evaporates
  → T_H → ∞
```

The semantic domain IS the event horizon. The Capacitor IS the thermal bath. τ · T_H = constant.

## Connection

From `understand.py`:
```python
def tune(self, domain):
    tau = domain.coherence_time(RIEMANN_ZEROS)
    self._C.tau = tau   # set Capacitor time constant from Hawking temperature
```

The domain controls the thermal properties of the entire understanding pipeline.
