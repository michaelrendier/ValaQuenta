# Engine: HyperWebster  Horner Bijection

**Module:** `modules/hyperwebster/`  
**Version:** 0.111  
**Confidence floor:** THEORETICAL  
**Notebooks:** [core/09_hyperwebster.ipynb](../notebooks/core/09_hyperwebster.ipynb)  
**Claim:** Zipf's law and the Prime Number Theorem are the same statement. Every word has an exact integer address via a Horner bijection.

---

## What it computes

HyperWebster hypergallery. Coordinates instead of pointers. Horner bijection (base-97): lossless text-to-integer address. Fano address (base-7): octonion generator path. SemanticWord: text + Horner + Fano + algebra coords. Monad: HyperWebster + Cayley-Dickson SMNNIP integrated.

`horner_encode` is a genuine bijection and `verify: True` in the result confirms the round trip. 'hello' → 623460239 → 'hello'.

`monad_address` is the integrated engine: HyperWebster address plus Cayley-Dickson tower coordinates for the same word. This is the Monad.


## The Null Operator

`e₀ = 1` is the multiplicative **identity** of the algebra — The Null Operator.
It never participates in zero-divisor crossings and it is the reference axis of
the Cayley-Dickson tower.

This matters when reading results from this engine: where a computation returns
the identity, or `V(0)=1`, or an unchanged value, **that is the answer, not a
missing one**. NULL-as-identity is the operative convention — nothing × nothing
= p; the prime IS a singularity in factor space. An engine reporting e₀ has not
failed to produce a result.

## Results — run 2026-07-28

6/6 equations run argument-free; 0 require parameters; 0 fail.

| Equation | Tier | Run | Result |
|---|---|---|---|
| `address_range` | ESTABLISHED | ✓ | {'base_text': 'hello', 'range': [{'text': 'hello', 'length': 5, 'horner_idx': 623460239,… |
| `fano_encode` | ESTABLISHED | ✓ | {'text': 'hello', 'fano_idx': 1596, 'generators': [0, 4, 4, 4, 0], 'length': 5} |
| `horner_encode` | ESTABLISHED | ✓ | {'text': 'hello', 'horner_idx': 623460239, 'length': 5, 'verify': True} |
| `fano_path` | THEORETICAL | ✓ | {'input': 'hello', 'generators': [0, 4, 4, 4, 0], 'canonical_word': 'aeeea', 'fano_idx':… |
| `monad_address` | THEORETICAL | ✓ | {'word': 'hello', 'horner': 623460239, 'fano': 1596, 'fano_path': [0, 4, 4, 4, 0], 'coor… |
| `semantic_word` | THEORETICAL | ✓ | {'text': 'hello', 'length': 5, 'horner_idx': 623460239, 'fano_idx': 1596, 'hash': '2cf24… |

## Open

- `semantic_word`, `monad_address` and `fano_path` are THEORETICAL. The encoding is exact; the claim that the address is *semantic* is not shown.
