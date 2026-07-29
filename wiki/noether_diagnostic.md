# Engine: Noether Currents  ∂_μJ^μ = 0

**Module:** `modules/noether/`  
**Version:** 0.111  
**Confidence floor:** THEORETICAL  
**Notebooks:** [core/05_noether.ipynb](../notebooks/core/05_noether.ipynb)  
**Claim:** Conservation ∂_μJ^μ = 0 is checked numerically per algebra level and the result is committed to a hash chain so a later run cannot quietly revise an earlier one.

---

## What it computes

Emmy Noether theorem applied to L_NN. Symmetry → conserved current. Violation = |∂_μJ^μ| — the training diagnostic with no GD analog. Blockchain ledger records every violation event. Resonance artifact detection identifies boundary oscillations.

This is `modules/noether/`, distinct from the top-level `noether.py` engine documented in [noether.md](noether.md). This one is the **diagnostic**: it measures violation rather than deriving σ.

`violation_scan` walks ℝ, ℂ, ℍ, 𝕆 and reports violation 0.0 / PASS at each. `blockchain_verify` returns `valid: True`.

The blockchain here is a tamper-evident log of conservation checks, not a distributed ledger and not a cryptocurrency.

## Results — run 2026-07-28

6/6 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `blockchain_record` | ESTABLISHED | ✓ | {'block_index': 0, 'hash': 'c7d6ee0dbb3bfd1d…', 'status': 'PASS', 'violation': 0.0} |
| `blockchain_summary` | ESTABLISHED | ✓ | {'total_blocks': 1, 'violations': 0, 'passes': 1, 'chain_valid': True, 'last_hash': 'c7d… |
| `blockchain_verify` | ESTABLISHED | ✓ | {'valid': True, 'broken_at': None, 'length': 1} |
| `conservation_diagnostic` | THEORETICAL | ✓ | {'J': [0.0054], 'J_prev': None, 'violation': 0.0, 'status': 'PASS', 'conserved': True, '… |
| `resonance_artifacts` | THEORETICAL | ✓ | {'oscillation_period': 40.0, 'amplitude': 0.005301460780390436, 'artifact_detected': Fal… |
| `violation_scan` | THEORETICAL | ✓ | {'ℝ': {'violation': 0.0, 'status': 'PASS', 'J': [0.0054]}, 'ℂ': {'violation': 0.0, 'stat… |

## Open

- A single run produces a chain of length 1. The audit property only has force once many runs have been appended over time.
- `resonance_artifacts` reports an oscillation of period 40.0 and amplitude 5.3e-3 which the module labels an artifact. Whether it is a numerical artifact or a signal is not settled.
