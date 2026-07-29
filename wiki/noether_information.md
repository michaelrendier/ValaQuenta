# Engine: J_info  Information Current

**Module:** `modules/noether_information/`  
**Version:** 0.111  
**Confidence floor:** CONJECTURE  
**Notebooks:** [core/06_noether_information.ipynb](../notebooks/core/06_noether_information.ipynb)  
**Claim:** An information current J_info accompanies the Noether currents, and its conservation defect gives the entropic arrow.

---

## What it computes

Noether current for information-translation symmetry of L_NN. I_information = Shannon entropy of activation distribution. Phi_flux = information flux through algebra boundary. t_e = entropic time (layer where I_info is maximal). Entropic arrow: ∂_l I_info ≥ 0.

The floor here is CONJECTURE — the lowest of any module in the repo, and correctly so. Three of four equations are CONJECTURE.

`delta_J_info` returns 2.22e-16, i.e. zero to machine epsilon. That is a consistency check on the arithmetic, not evidence for the conjecture.

`entropic_arrow` returns a run of exact -0.0 values before rising. The leading zeros are the degenerate regime, not missing data.

## Results — run 2026-07-28

3/4 equations run argument-free; 1 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `information_capacity` | THEORETICAL | needs params |  |
| `delta_J_info` | CONJECTURE | ✓ | {'delta_J_info': 2.220446049250313e-16, 'J_info_0_curr': 1.8427100815728608, 'J_info_0_p… |
| `entropic_arrow` | CONJECTURE | ✓ | {'I_values': [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.9649567669505685, 0.9649567669… |
| `information_current` | CONJECTURE | ✓ | {'J_info_0': 1.8427100815728608, 'J_info_1': 0.22000000000000003, 'I_info': 1.8427100815… |

*"needs params" means the equation takes arguments and was not called, not that it is broken. The module's own `shell_commands()` exercise these with its author's defaults.*

## Open

- The identification of J_info with a physical information current is unshown. CONJECTURE means: named direction, no formal derivation yet.
