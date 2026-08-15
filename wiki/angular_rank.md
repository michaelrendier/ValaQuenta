# angular_rank — The 16D Oscilloscope

`modules/angular_rank/` · v0.1 · Status: **ESTABLISHED** (instrument) / **THEORETICAL** (provenance application)

Angular content and subspace occupancy, measured on a **frozen epoch**.

---

## What it measures

A signal arrives. It is embedded in the 16 sedenion dimensions. Three questions are then
answerable **without knowing its language, its meaning, or its author**:

| # | question | function |
|---|---|---|
| 1 | how much **direction** survives once the common mode is removed? | `angular_residual` |
| 2 | which dimensions are populated, at what **rank**? | `occupancy`, `numerical_rank` |
| 3 | does it reach `ker(L_a)` — what the internal channel **cannot** produce? | `null_occupancy` |

**Question 3 is the internal/external provenance test. Question 1 is the language-agnostic
stress test. They are the same measurement.** One instrument, two applications — as the
Larynx is one operation with two applications (UDEO translation and the ECC crack,
Phase 19).

---

## The epoch discipline — the correction this module exists to enforce

> *"we don't remove items from a list while iterating over it… that's an amateur move…
> that is definitely iterating over a field while modifying it. by the nature of code,
> that's going to drift and possibly seize the engine down the line"*
> — Cody Michael Allison, 2026-08-15

`Operating-L-IO.md` §4.4 first proposed reading "dimensions the internal trace never
populates" — while the thinking threads were concurrently **growing that trace**. That is
iterate-while-modify one level up. It does not raise. It **drifts**, silently, until the
internal span covers `ker(L_a)` and the instrument reports *all quiet* forever.

The fix is not a lock. It is an **epoch**:

```python
e = snapshot(field, 'ear_t0')     # immutable, sha256 content stamp
angular_residual(e)               # returns the stamp it read
precession(e_before, e_after)     # mutation is DATED, not forbidden
```

- `snapshot()` is the **only** way into the module. Every other entry point raises
  `TypeError` on a live sequence, with the reason in the message.
- Every result carries the stamp of the epoch it read.
- `precession()` measures drift **between** two epochs, so a measurement never straddles
  a write.

> ⚠ **No measurement is reportable without its epoch.** Same rule shape as *no result
> without its null* (`L_IO_SPECIFICATION.md` §3).

**Mutation is not the bug. Mutation measured across an unbounded interval is the bug.**
Phase 27.3 is the bounded reference — net winding +0.0000 turns, non-accumulating, held
by the gearing rather than computed. `precession()` reports `stale_measurements: True`
the moment the span moves, which is the signal to re-snapshot rather than keep reading.

---

## The two mandatory nulls

**1. Isotropic baseline for kernel occupancy — exactly `nullity/dim`.**

```
analytic  0.25          measured  0.250968   (20,000 isotropic draws)
```

An isotropic random field already puts **4/16 = 25%** of its energy in `ker(L_a)`.

> ⚠ A raw kernel fraction near 0.25 is **evidence of nothing**. Only the **excess** is a
> signal. `null_occupancy()` returns `excess` and `reportable` alongside the raw
> fraction so the bare number cannot travel alone. Same discipline as *read the z-score,
> never the raw r*.

**2. The calibration is embedding-specific.**

| reference | angular residual | collapse cos |
|---|---|---|
| scalar address | 0.0000 | 1.0000 |
| character encoder (Phase 23) | 0.0002 | 0.9998 |
| phonetic face (Phase 27.2) | **0.4020** | 0.9109 |

> ⚠ Measured on the **phonetic face** embedding. They **do not transfer** to
> `embed_log_bands` or any other embedding. `score_against_calibration()` returns the
> caveat attached to the answer. Comparing residuals across embeddings is meaningless.

---

## The honest check

`verify_null_space()` reproduces `Null-Space-of-the-Zero-Divisor.md` from the
Cayley–Dickson table, as a **check, not an input**:

```
a = (e_1 + e_10)/sqrt(2)     Assessor (1,2), strut 3

nullity           4
rank             12
singular values   sqrt2 x4,  1 x8,  0 x4        the {4,8,4} split
matches_published True
```

`L_a` is built from `box_kite.maths.basis_mul` — one multiplication table in the repo,
borrowed rather than reimplemented — and cross-checked against `box_kite`'s independent
`multiply()`: `L_a x == a·x` for random `x`.

---

## The silent failure mode

> ⚠ `null_occupancy()` returning ~0 is **ambiguous**. It means *either* no external
> signal *or* the ear is wired **through** `L_a` instead of summed in downstream of it —
> in which case the external component is annihilated identically and the instrument is
> blind, with no error raised.
>
> The caveat ships in the return value. Verify the wiring separately;
> see `Operating-L-IO.md` §4.4.

---

## Results

```
verify_null_space          nullity 4, rank 12, {sqrt2 x4, 1 x8, 0 x4}   matches_published True
null_occupancy_baseline    analytic 0.25   measured 0.250968   agreement True
angular_residual (scalar field)     0.000000     — a scalar wearing 16 coordinates
angular_residual (isotropic n=200)  0.9646       — rank 16, participation ratio 15.89
null_occupancy (built in kernel)    1.000000     — excess +0.75
null_occupancy (isotropic)          0.2501       — excess +0.0001, reportable False
precession (span 4 -> 16)           rank_delta +12, stale_measurements True
```

---

## Formulary

12 equations: `verify_null_space`, `null_occupancy_baseline`, `angular_residual`,
`calibration`, `null_occupancy`, `external_component`, `precession`, `numerical_rank`,
`occupancy`, `embed_log_bands`, `angular_report`, `null_space`.

---

## Open

| item | status |
|---|---|
| does a real ear injection land in `ker(L_a)` at all? | **untested** — the whole provenance test depends on it |
| ear summed downstream of `L_a`, not through it | wiring unverified; fails silently if wrong |
| VAPMIP `monad.c`: one `G` under one `pthread_mutex_t G.lock` | **blocker** — provenance destroyed at write; no downstream test can recover it |
| cetacean corpus | none in repo; instrument is calibrated and waiting |
| an embedding-independent angular statistic | none; every number here is embedding-relative |

---

## Related

- `VAPMIP/docs/wiki/Operating-L-IO.md` §4 — the provenance argument and its retraction
- `VAPMIP/docs/wiki/Null-Space-of-the-Zero-Divisor.md` — the {4,8,4} split
- `box_kite.md` — the CD table and ZD geometry this borrows
- `Ainulindale/wiki/86_the_16d_oscilloscope.md` — narrative page
- Phase 27.2 (angular residual), Phase 27.3 (bounded precession), Phase 19 (the organs)
