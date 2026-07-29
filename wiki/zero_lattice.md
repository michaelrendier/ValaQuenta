# Engine: Zero Lattice

**File:** `zero_lattice.py`  
**Class:** `ZLNode`  
**Claim:** In 𝕊 there exist non-zero a, b with a·b = 0, and their lattice has exactly 84 directed / 42 unordered zero-divisor pairs.

---

## What it computes

```
Zero Lattice Engine — Telperion
Paper: "How an Addition EQUALS a Subtraction"
```

## Results — run 2026-07-28

Paper: 'How an Addition EQUALS a Subtraction', FourthAgePapers.

The counts are exact and come out of the multiplication table, not a fit:

```
Found: 84 directed pairs
  Odd-sector: 12 (prime sector)
  Mixed:      72
  Even-sector: 0
Unordered classes: 42 (expect 42)
```

**THE ANGLE = π/8 = 22.5°**, with tan(π/8) = √2−1 = 0.414213562373095 reproduced to a residual of 1.11e-16 — machine epsilon. 16 × π/8 = 360°, one revolution.

The angle's job: before rotation the red and blue current sectors interleave (red at 0/90/180/270, blue at 45/135/225/315). After rotating by π/8 they **coincide** — both at 22.5/112.5/202.5/292.5. That coincidence is the engine's central geometric claim, and it is checked.

Telperion, the tree: ℝ is the leaf at σ=1, ℍ the equator at σ=½, 𝕊 the first ZD level at σ=0, and t_256 the root at σ=−1.

## Constants

| Name | Value |
|---|---|
| `CD_LEVELS` | 9 |
| `D_STAR` | 0.246 |
| `GAP` | 0.000707357533248576 |
| `OMEGA_ZS` | 0.5671432904097838 |
| `SEDENION_DIM` | 16 |
| `SIGMA_HALF` | 0.5 |
| `THE_ANGLE` | 0.39269908169872414 |
| `ZD_CLASSES` | 42 |
| `ZD_PAIRS` | 84 |

## Entry points

`basis_to_cell()`, `build_mul_table()`, `build_tree()`, `classify_zd_pairs()`, `critical_line_samples()`, `e_k()`, `find_zd_pairs()`, `laurelin_interface()`, `monster_gap_in_map()`, `multiply()`, `norm_sq()`, `run_all()`, `sedenion_point_map()`, `sphere_coordinates()`, `switch_scale()`, `the_angle()`, `universal_translator_structure()`, `verify_angle()`, `view_tree()`, `zd_path_coordinates()`, `zeta_dirichlet()`, `zeta_geometric()`

## Prediction P2 fails

`ZeroLattice/03_results.ipynb` asserts **P2: the Monster gap appears in ALL
odd-sector pairs.** Re-run 2026-07-28, it does not:

```
MONSTER_GAP = {1, 11, 15}
odd-sector directed pairs : 12
meet MONSTER_GAP          : 10/12
do NOT meet it            :  2/12   ((3,9),(7,13)) and its reverse
```

Two directed pairs miss, and they are the same unordered class in both
directions — so **5 of 6 unordered odd-sector classes** meet the Monster gap
and one, `{(3,9),(7,13)}`, does not.

This failure was previously invisible: the P2 line raised
`TypeError: unsupported operand type(s) for &: 'bool' and 'frozenset'` from a
misplaced parenthesis, so the scorecard cell crashed instead of scoring. With
the parenthesis corrected the notebook now reports `P2 [FAIL]` and
`Overall: FAILURES`.

Either P2 should be weakened to "almost all", or `{(3,9),(7,13)}` is a
distinguished class and the reason it is exempt needs saying. Not resolved here.

## Open

- The Monster gap appears at e[1, 11, 15]. Its significance is asserted, not derived.
- P2 above: one odd-sector class misses the Monster gap.
