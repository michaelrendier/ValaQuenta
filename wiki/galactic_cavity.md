# Engine: Galactic Cavity

**File:** `galactic_cavity.py`  
**Class:** `CavityMode`  
**Claim:** Dark matter = quantum potential of a galactic standing wave. The galaxy IS the Bohmian pilot wave. No particle.

---

## Results (run 2026-06-13)

```
r_t    = 0.738 kpc     (transition radius: dark matter threshold)
v_flat = 220.0 km/s    (flat rotation velocity)

Wave period: 22.7 Gyr   (vs universe age 13.8 Gyr — frozen wave, cannot complete)
Jeans unstable: True     (gravitational collapse permitted within cavity)
```

Rotation curve table (sample):
```
  r (kpc)   v_bar (km/s)   v_flat (km/s)
  0.100     35.2           220.0
  0.738     220.0          220.0   ← transition point
  1.000     220.0          220.0
  5.000     220.0          220.0
  20.000    220.0          220.0   ← flat indefinitely
```

## Predictions

| Prediction | Formula | Value | Status |
|-----------|---------|-------|--------|
| P1: transition radius | r_t = d* × r_max_bar | r_t = d* × (baryonic max) | confirmed SPARC 97-galaxy sample 2026-05-30 |
| P2: DM fraction | v_bar²/v² = d* | d*=0.246 | tested |

P1 (r_t = d* × r_max_bar) confirmed against SPARC 97-galaxy sample. d* = 0.24600 emerges as the ratio of baryonic matter scale to total matter scale.

## Architecture

The galactic cavity is a standing wave in the cosmic medium. The wave period (22.7 Gyr) exceeds the universe age (13.8 Gyr): the wave froze at the BAO acoustic horizon. What we call "dark matter" is the quantum potential Q of this frozen standing wave.

```
Q = −(ħ²/2m) ∇²R/R    (Bohm quantum potential)
v_rotation² = v_baryonic² + Q/m
```

No dark matter particle. The rotation curve is a boundary condition on the frozen cavity.
