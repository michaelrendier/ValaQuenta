# Engine: Telperion

**File:** `telperion.py`  
**Class:** `BellPhase / LindbladMode / ResonanceCoupling`  
**Claim:** Galactic bell geometry: the bar contracts to a Witches Hat and expands to a brim, and the bell never closes and never reaches the shell.

---

## What it computes

```
telperion.py — The Swimming Engine  v0.100
==========================================
```

## Results — run 2026-07-28

The bell swings between two phases and the numbers are exact:

```
contracted (Witches Hat / bar):  13.8203°   tan = 0.246   = d*
expanded   (Brim / 2-arm spiral): 22.5000°   tan = 0.414213562 = √2−1
swing:                             8.6797°
bell amplitude (tan):              0.168213562
```

The contracted half-angle has **tan = d\* exactly**. The expanded half-angle is THE ANGLE, π/8, from the zero lattice. The bell swings between the spectral floor and the zero-divisor angle.

`bell_never_closes: True` and `bell_never_reaches_shell: True`, both enforced by GAP = 7.073575e-04. The gap is what keeps the geometry open.

The contracted phase sits at the OLR (outer Lindblad resonance) with a 1-arm bar; the expanded phase at the ILR with a 2-arm spiral.

**e₀ = The Null Operator.** `m87_axis` identifies the M87* spin axis with e₀ extended into physical space: the multiplicative identity, which never participates in ZD crossings, is the reference axis of the tower. The 5000 ly M87 jet is aligned with it, BAO shells stack perpendicular to it, and 'up' means away from the singularity, toward The Unit.


## The Null Operator

`e₀ = 1` is the multiplicative **identity** of the algebra — The Null Operator.
It never participates in zero-divisor crossings and it is the reference axis of
the Cayley-Dickson tower.

This matters when reading results from this engine: where a computation returns
the identity, or `V(0)=1`, or an unchanged value, **that is the answer, not a
missing one**. NULL-as-identity is the operative convention — nothing × nothing
= p; the prime IS a singularity in factor space. An engine reporting e₀ has not
failed to produce a result.

## Constants

| Name | Value |
|---|---|
| `BAO_MPC` | 150.0 |
| `BELL_AMPLITUDE` | 0.16821356237309515 |
| `BRIM_HALF_ANGLE` | 0.39269908169872414 |
| `C_SI` | 299792458.0 |
| `D_STAR` | 0.246 |
| `GAP` | 0.000707357533248576 |
| `G_SI` | 6.674e-11 |
| `H0_KMS_MPC` | 72.0 |
| `HAT_HALF_ANGLE` | 0.24121042848984825 |
| `L_PLANCK` | 1.616255e-35 |
| `M87_MASS_MSUN` | 6500000000.0 |
| `M87_RS_AU` | 128.34865985351038 |
| `M87_RS_M` | 19200959514085.152 |
| `MPC_TO_LY` | 3262000.0 |
| `MSUN_KG` | 1.989e+30 |
| `OBS_MPC` | 14127.0 |
| `OMEGA_ZS` | 0.5671432904097838 |
| `SIGMA_BRIM` | 0.5857864376269049 |
| `SIGMA_HAT` | 0.754 |
| `SIGMA_SHELL` | 0.5 |
| `SILVER` | 0.41421356237309515 |
| `THE_ANGLE` | 0.39269908169872414 |
| `UNIVERSE_AGE_YR` | 13800000000.0 |
| `VERSION` | '0.100' |
| `YR_TO_S` | 31560000.0 |

## Entry points

`bao_tower_mapping()`, `bell_geometry()`, `bell_phases()`, `galactic_rotation_lock()`, `galaxy_types()`, `lindblad_modes()`, `m87_axis()`, `m87_compression()`, `predictions()`, `resonance_coupling()`, `run_all()`, `stellar_halo_profile_comparison()`, `the_angle_in_lindblad()`, `the_swimming_engine()`

## Open

- The README records 10/10 predictions confirmed. Those predictions and their confirmations are recorded in the engine's own `predictions()`; each should be read with its own source.
- The jellyfish / swimming reading is a physical picture laid over the resonance coupling, not an additional result.
