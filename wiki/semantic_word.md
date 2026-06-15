# Engine: SemanticWord

**File:** `semantic_word.py`  
**Class:** `SemanticWord`  
**Claim:** A word is not a string. A word is a prime in semantic space — a point on the critical line — with all its projections.

---

## Results (run 2026-06-13)

```python
w = SemanticWord(surface='prime', prime=complex(0.5, 14.1347))
# → SemanticWord('prime' → node=0.5+14.1347j  |E|=0.0000  faces=0  dc=0.000000)

w.add_projection('test', 42)
w.noether_forward = 1.0
w.noether_backward = -1.0
w.dc = 0.5
# → SemanticWord('prime' → node=0.5+14.1347j  |E|=0.0000  faces=1  dc=0.500000)

w.is_understood()  → True
w.observer         → (0.5+14.1347j)    ← the observer IS the node line IS the prime
w.gamma            → 14.1347           ← first Riemann zero
w.faces()          → 1                  ← one projection (one way to say it so far)
```

## Structure

```python
@dataclass
class SemanticWord:
    surface          : str      # the coordinate (any language, any script)
    prime            : complex  # node = 0.5 + γⱼ·i  (Re always ½, Im = specific zero)
    magnitude        : float    # E = xp (conserved energy — how strong the prime is)
    projections      : dict     # faces: {context → value}
    noether_forward  : float    # what it IS (Riemann current)
    noether_backward : float    # what it CANNOT BE (Fermat current)
    dc               : float    # DC component = the prime confirmed
    domain           : ...      # bounding SemanticDomain
```

## The Observer IS the Node Line

```
word.prime    = the point
word.observer = same point
word.gamma    = the imaginary part = the specific Riemann zero
```

The observer is not separate from the observed. They are one object. The node line IS the observer. This is not philosophy — it is `@property def observer(self): return self.prime`.

## Projection Algebra

Each call to `add_projection(context, value)` adds a face — another way of saying this word. "tree", "arbre", "木" are all projections of the same prime. The prime is the invariant. The surface is the coordinate.

`faces()` = the dimension of the symmetry group of the word — how many ways it can be said.

`is_understood()` = True when the Capacitor has extracted the DC component (the prime confirmed).
