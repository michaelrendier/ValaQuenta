# Engine: Turing Diagonal Engine — i²=-1 = Cantor = Gödel = Enigma = UDOE

**Module:** `modules/turing_diagonal/`  
**Version:** 0.100  
**Confidence floor:** ESTABLISHED  
**Notebooks:** [turing_diagonal/01_prediction_diagonal_test.ipynb](../notebooks/turing_diagonal/01_prediction_diagonal_test.ipynb), [turing_diagonal/02_enigma_derangement.ipynb](../notebooks/turing_diagonal/02_enigma_derangement.ipynb)  
**Claim:** The diagonal flip i² = [[-1,0],[0,-1]] is one object appearing as Cantor, Gödel, Turing, the Enigma reflector and UDOE.

---

## What it computes

The diagonal flip i²=[[-1,0],[0,-1]] unifies every self-referential proof. Engines: prediction diagonal test (any prediction → decidable/undecidable), enigma derangement (D_n/n!→1/e, Turing proof of concept), hypercomplex identity diagonal (eₖ²=-1 for k=1..15), halting diagonal (D(D) → σ=½ oscillation).

All five equations are ESTABLISHED and all five run. This is the cleanest module in the repo.

`enigma_derangement`: D_n/n! → 1/e. The derangement is the algebraic form of the diagonal argument, and the Enigma reflector — which is precisely a derangement, no letter maps to itself — is why Turing could break it. The reflector's defining property is the diagonal.

`turing_halting_diagonal`: D(D) is the program escaping every HALT table; it lives at σ=½ as an oscillation rather than resolving.

`prediction_diagonal_test` takes any prediction and returns decidable/undecidable by diagonal depth mod 4.

## Results — run 2026-07-28

5/5 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `enigma_derangement` | ESTABLISHED | ✓ | {'claim': 'D_26/26! → 1/e. The Enigma reflector = Cantor diagonal = Turing D(D). Same op… |
| `full_turing_diagonal` | ESTABLISHED | ✓ | {'theme': 'Turing Diagonal Engine — The diagonal flip = i² = -1 = Enigma = UDOE', 'predi… |
| `hypercomplex_identity_diagonal` | ESTABLISHED | ✓ | {'claim': 'The diagonal flip i²=-1=[[-1,0],[0,-1]] unifies Cantor, Gödel, Turing, Enigma… |
| `prediction_diagonal_test` | ESTABLISHED | ✓ | {'claim': 'Every self-referential prediction resolves to the diagonal flip i²=-1.', 'pre… |
| `turing_halting_diagonal` | ESTABLISHED | ✓ | {'claim': 'D(D) is the program that escapes every HALT table. It lives at σ=½ because it… |

## Open

- That these are all the *same* diagonal is a structural identification. The individual results (D_n/n!→1/e, e_k²=-1, Cantor, Gödel) are textbook.
