# Engine: Addition Matrix — Columns as Rotors, the Law of the Factor Search

**Module:** `modules/addition_matrix/` (`maths.py`, `tools.py`)
**Class:** `AdditionMatrixModule` · **Version:** 1.0
**Claim:** the addition matrix of long multiplication is arithmetic modulo 10ᵏ. Its columns are rotors with exact periods; the maps `x → a·x + b` on ℤ/10ᵐ factor through ℤ/2ᵐ × ℤ/5ᵐ; and the digit-by-digit factor search keeps exactly the pairs (p, q) mod 10^(c+1) with p·q ≡ N, whose number is a closed form, a product over the primes 2 and 5. For N with both valuations below c+1 it is (v₂+1)(v₅+1)·φ(10^(c+1)) = (v₂+1)(v₅+1)·4·10ᶜ: unit-group torsors, ×10 per column.
**Status:** `ESTABLISHED` (elementary number theory; each statement is checked by the code, exhaustively over the stated range). The K = 0 address is a restatement and is reported with its neighbours (see below).
**Source of the problem:** the Multiplication Matrix Explorer (`github.com/michaelrendier/MultiplicationMatrixExplorer`), whose `matrix_math.py` and `factor_reconstruction.py` this engine reproduces; `tests/test_addition_matrix.py` cross-checks every row, carry and column count against them when the repository is found (`MME_PATH`).

---

## Mechanism

| Part | Functions | What it states |
|---|---|---|
| A. The matrix | `matrix_rows`, `carry_matrix` | one row per digit of `num2`, rows added one at a time so every carry is 0 or 1; total = `num1 × num2`; 21 columns for 10-digit inputs (the Explorer's `N_COLUMNS`) |
| B. Columns as rotors | `column_period`, `column_period_measured`, `affine_cycle_type`, `crt_combine`, `crt_rule_check`, `odometer_first_return`, `solenoid_cycles` | column *c* depends on `num2` modulo 10^(c+1) with period 10^(c+1)/gcd(num1, 10^(c+1)); cycle type of `x → a·x + b` on ℤ/10ᵐ = CRT combination of the types on ℤ/2ᵐ and ℤ/5ᵐ; the odometer's first return to multiples of 10 is the odometer one scale down; on ℤ/2ⁿ all cycle lengths are powers of two |
| C. The law | `prime_power_solutions`, `solution_count_closed`, `solution_count_brute`, `live_state_counts`, `torsor_orbits`, `unit_group_order`, `lift_branching` | #{(p, q) mod 10ᵏ : pq = N} = f₂·f₅ with f_p = (v+1)φ(pᵏ) for v < k and kφ(pᵏ)+pᵏ for N ≡ 0 mod pᵏ; unit solutions form (v₂+1)(v₅+1) torsors of (ℤ/10ᵏ)ˣ, of order 4·10^(k−1); every unit solution has exactly ten lifts |
| D. The address | `unit_solutions`, `address_profile` | for a unit solution mod 10ⁿ, K = (p′q′ − N)/10ⁿ is an integer; the true factorisation into two n-digit numbers is exactly K = 0 |

## Results (run)

```
live states per column vs closed form (columns below n agree exactly; from column n the size of the factors enters)
N=3233    n=2  live [4, 40, 6, 2]                       closed [4, 40]
N=14351   n=3  live [4, 40, 400, 48, 4, 2]              closed [4, 40, 400]
N=1022117 n=4  live [4, 40, 400, 4000, 406, 38, 8, 2]   closed [4, 40, 400, 4000]
N=420     (v2=2, v5=1)  live [27, 320, 32, 16]          closed [27, 320]
N=850     (v2=1, v5=2)  live [27, 260, 26, 6]           closed [27, 260]
N=5100    (v2=2, v5=2)  live [27, 520, 32, 4]           closed [27, 520]

closed form vs enumeration, N in [0, 2·10ᵏ+50) for k = 1, 2, 3: 0 mismatches
CRT rule: 18,040 affine maps on ℤ/10ᵐ (m = 1, 2, 3, every unit a): 0 failures
odometer first return = odometer one scale down: m = 2, 3, 4 all True
column periods, 7 values of num1 × 3 columns: formula = measured in every case
```

**The address**, 30 products of two 3-digit primes, n = 3: 400 unit solutions per N, exactly 2 with K = 0 (the pair and its swap); among the other solutions the smallest |K| ranges from 1 to 14 in the notebook's sample and 1 to 15 in the paper's (median over N of the median |K| about 164–171). **The address exists and is unique among zero-overflow solutions, but it is not isolated: near-misses with |K| = 1, 2, … exist, and no coordinate of the unit group distinguishes the true pair in advance.**

## What this is not

It is not a factoring method. The live-state count is the cost of the search, and the law says that cost is ×10 per digit until the size constraint (columns ≥ n) applies. The related digit-by-digit (branch-and-prune) technique is published for recovering RSA keys from partial bits (Heninger & Shacham 2009); this engine states the count for the decimal columns of the addition matrix.

## Confidence

| Item | Label |
|---|---|
| matrix, carries in {0,1}, product | ESTABLISHED:CALCULATED |
| column period formula | ESTABLISHED:CALCULATED (formula = measured divisor search) |
| CRT cycle rule | ESTABLISHED:CALCULATED (exhaustive over the stated maps) |
| odometer first return | ESTABLISHED:CALCULATED (m ≤ 4) |
| solution-count closed form | ESTABLISHED:CALCULATED (exhaustive N, k ≤ 3) |
| live states = closed form below column n | ESTABLISHED:CALCULATED (six N) |
| K = 0 address | OURS: restatement; not isolated |

## Files

`modules/addition_matrix/{__init__,maths,tools}.py` + `manifest.json` · `notebooks/addition_matrix/01_matrix_and_rotors.ipynb`, `02_law_and_address.ipynb` · `wiki/toolbox/40_addition_matrix.md` · `tests/test_addition_matrix.py` (11 tests) · narrative page `Ainulindale/wiki/125_addition_matrix_rotors_and_the_factor_search_law.md`.
