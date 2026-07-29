# Engine: L_NN  Ainulindale Lagrangian

**Module:** `modules/lagrangian/`  
**Version:** 0.111  
**Confidence floor:** THEORETICAL  
**Notebooks:** [core/04_lagrangian.ipynb](../notebooks/core/04_lagrangian.ipynb)  
**Claim:** L_NN, the Ainulindale Lagrangian, assembled from kinetic, matter, bias and coupling terms over a Cayley-Dickson algebra.

---

## What it computes

The four-term SMNNIP Lagrangian density L_NN = (2/π)∮[L_kin + L_mat + (1/φ)L_bias + L_coup] r dr dθ. Running coupling α_NN(r) = g²/(4π·ħ_NN·ln(1/r)). RG flow per algebra stratum. Mastery crystallization condition.

Six of the eight equations require parameters (field component vectors, coupling constants) and therefore cannot be run argument-free. They are listed below as NEEDS PARAMS, which is a statement about their signature, not a failure. The `shell_commands()` entries exercise them with the module author's own defaults.

`rg_flow` runs argument-free and shows α descending from 0.01 — a renormalisation-group flow, monotone over the sampled range.

## Results — run 2026-07-28

2/8 equations run argument-free; 6 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `L_bias` | ESTABLISHED | needs params |  |
| `L_kinetic` | ESTABLISHED | needs params |  |
| `L_coupling` | THEORETICAL | needs params |  |
| `L_matter` | THEORETICAL | needs params |  |
| `alpha_nn_running` | THEORETICAL | needs params |  |
| `mastery_check` | THEORETICAL | needs params |  |
| `polar_lagrangian` | THEORETICAL | ✓ | {'kinetic': -2.5e-07, 'matter': 9.666666666666666e-08, 'bias': -1.9753125000000002, 'cou… |
| `rg_flow` | THEORETICAL | ✓ | {'alpha': [0.01, 0.00998898037659848, 0.00998254556138366, 0.009977985012883684, 0.00997… |

*"needs params" means the equation takes arguments and was not called, not that it is broken. The module's own `shell_commands()` exercise these with its author's defaults.*

## Open

- The module is THEORETICAL at floor. Only `L_kinetic` and `L_bias` are ESTABLISHED, and both are parameterised.
- The README notes a rename is pending: L_NN → the VAPMIP Lagrangian.
