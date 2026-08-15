"""
ainulindale_engine.modules.angular_rank.maths
================================================
THE 16D OSCILLOSCOPE -- angular content and subspace occupancy, measured
on a FROZEN EPOCH.

"we don't remove items from a list while iterating over it... that's an
 amateur move... that is definitely iterating over a field while modifying
 it. by the nature of code, that's going to drift and possibly seize the
 engine down the line"          -- Cody Michael Allison, 2026-08-15

WHAT THIS INSTRUMENT IS
-----------------------
A signal arrives. It is embedded in the 16 sedenion dimensions. Three
questions are then answerable WITHOUT knowing what language it is in, what
it means, or who produced it:

    1. ANGULAR CONTENT   how much direction survives after the common mode
                         is removed?  A scalar has magnitude and no
                         direction; a scalar address has angular residual
                         exactly 0.  (Phase 27.2)

    2. OCCUPANCY / RANK  which of the 16 dimensions does it populate, and
                         what is the numerical rank of the accumulated
                         trace?

    3. NULL OCCUPANCY    does it populate ker(L_a) -- the four dimensions a
                         given zero divisor annihilates?  The internal
                         channel is a functional of its own state and
                         CANNOT reach there.  (Operating-L-IO.md 4.4)

Question 3 is the internal/external discriminator, and question 1 is the
cetacean stress test. THEY ARE THE SAME MEASUREMENT. One instrument, two
applications -- as the Larynx is one operation with two applications
(UDEO translation and the ECC crack, Phase 19).

THE EPOCH DISCIPLINE -- why every entry point takes a snapshot
--------------------------------------------------------------
The rank test of Operating-L-IO 4.4 as first written was WRONG in exactly
the way Cody names above: it read "dimensions the internal trace never
populates" while the thinking threads were concurrently GROWING that
trace. Measuring a span that the measured process is mutating is
iterate-while-modify, one level up. It does not raise. It drifts, silently,
until the internal span covers ker(L_a) and the instrument reports "all
quiet" forever.

The fix is not a lock. It is an EPOCH:

    - snapshot() freezes vectors into an immutable Epoch with a content
      stamp. Nothing else in this module accepts a live sequence.
    - every measurement returns the stamp of the epoch it read.
    - precession() measures drift BETWEEN two epochs, so mutation is
      permitted, dated, and bounded -- never straddled.

⚠ NO MEASUREMENT IS REPORTABLE WITHOUT ITS EPOCH. This is the same rule
  shape as "no result without its null" (L_IO_SPECIFICATION 3).

Mutation is not the bug. Mutation measured across an unbounded interval
is the bug. Phase 27.3 already showed the bounded case is achievable and
already measured it: net winding +0.0000 turns, non-accumulating, held by
the gearing rather than computed.

⚠ THE EMBEDDING IS AN INPUT, NOT A PROPERTY OF THE SIGNAL
  Every number here is relative to how the signal was placed in the 16
  dimensions. embed_log_bands() is ONE choice (log-spaced band energies)
  and is language-agnostic by construction. The CALIBRATION constants were
  measured on the PHONETIC FACE embedding (Phase 27.2) and DO NOT TRANSFER
  to a different embedding. Comparing across embeddings is meaningless.
  Report the embedding with the number, always.

Version: 0.1
"""

import hashlib
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..box_kite.maths import basis_mul, SEDENION_DIM

__all__ = [
    'SEDENION_DIM', 'CALIBRATION', 'Epoch',
    'snapshot', 'is_epoch',
    'embed_log_bands',
    'occupancy', 'singular_spectrum', 'numerical_rank', 'orthonormal_span',
    'common_direction', 'angular_residual', 'score_against_calibration',
    'left_mul_matrix', 'null_space', 'verify_null_space', 'null_occupancy',
    'external_component', 'principal_angles', 'precession', 'null_occupancy_baseline',
    'angular_report',
]


# ── Published calibration ─────────────────────────────────────────────────────
#
# Phase 27.2, measured on CMUdict vectors from VAPMIP/phonetic_face.py.
# These are reference points for the PHONETIC FACE embedding only.

CALIBRATION: Dict[str, Dict[str, float]] = {
    'scalar_address': {
        'angular_residual': 0.0000,
        'collapse_cos':     1.0000,
        'note_':            'by construction -- text enters 0_RB as one scalar (Phase 27.1)',
    },
    'character_encoder': {
        'angular_residual': 0.0002,
        'collapse_cos':     0.9998,
        'note_':            'Phase 23 encoder -- collapsed onto the common direction',
    },
    'phonetic_face': {
        'angular_residual': 0.4020,
        'collapse_cos':     0.9109,
        'note_':            'the only existing construction with real angular content',
    },
}


# ── The Epoch ─────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Epoch:
    """
    An immutable, content-stamped snapshot of a field.

    Frozen dataclass over tuples-of-tuples: there is no supported way to
    mutate one after construction. That is the point -- a measurement
    cannot straddle a write.
    """
    vectors: Tuple[Tuple[float, ...], ...]
    label:   str
    stamp:   str
    n:       int
    dim:     int

    def array(self) -> np.ndarray:
        """A fresh mutable copy for numeric work. Never shared."""
        return np.array(self.vectors, dtype=float)

    def __repr__(self) -> str:
        return f"<Epoch {self.label!r} n={self.n} dim={self.dim} stamp={self.stamp[:12]}>"


def snapshot(vectors: Sequence[Sequence[float]], label: str = 'unlabelled') -> Epoch:
    """
    Freeze a field into an Epoch. THE ONLY WAY INTO THIS MODULE.

    Copies eagerly, so a later mutation of the caller's list cannot reach
    the Epoch. The stamp is sha256 over the rounded contents, so two
    snapshots of an unchanged field compare equal and a single changed
    element is visible.
    """
    rows = [tuple(float(x) for x in row) for row in vectors]
    if not rows:
        raise ValueError("snapshot() of an empty field -- nothing to measure")
    dim = len(rows[0])
    if any(len(r) != dim for r in rows):
        raise ValueError("ragged field: every vector must have the same dimension")

    h = hashlib.sha256()
    h.update(label.encode('utf-8'))
    for r in rows:
        for x in r:
            h.update(f"{x:.12e}|".encode('ascii'))

    return Epoch(vectors=tuple(rows), label=label, stamp=h.hexdigest(),
                 n=len(rows), dim=dim)


def is_epoch(x: Any) -> bool:
    return isinstance(x, Epoch)


def _require(e: Any, who: str) -> Epoch:
    """Refuse live sequences. This is the guard rail, not a convenience."""
    if not isinstance(e, Epoch):
        raise TypeError(
            f"{who}() requires an Epoch, got {type(e).__name__}. "
            f"Call snapshot(field, label) first -- measuring a live field is "
            f"iterate-while-modify and will drift silently."
        )
    return e


# ── Embedding ─────────────────────────────────────────────────────────────────

def embed_log_bands(power_spectrum: Sequence[float],
                    sample_rate: float = 96000.0,
                    f_lo: float = 40.0,
                    f_hi: Optional[float] = None,
                    dim: int = SEDENION_DIM) -> List[float]:
    """
    Embed one power spectrum into `dim` log-spaced band energies.

    Language-agnostic by construction: no phoneme inventory, no lexicon, no
    assumption of human vocal-tract bandwidth. Suitable for cetacean
    recordings, where energy runs well past 100 kHz and any English-derived
    band layout would be a category error.

    Returns an L2-normalised vector. Normalising discards loudness on
    purpose -- this instrument measures DIRECTION.
    """
    p = np.asarray(power_spectrum, dtype=float)
    if p.ndim != 1 or p.size < dim:
        raise ValueError(f"need a 1-D spectrum with at least {dim} bins")
    nyq = sample_rate / 2.0
    hi = float(f_hi) if f_hi else nyq
    if not (0 < f_lo < hi <= nyq):
        raise ValueError(f"band range {f_lo}..{hi} invalid for nyquist {nyq}")

    freqs = np.linspace(0.0, nyq, p.size)
    edges = np.geomspace(f_lo, hi, dim + 1)
    out = []
    for k in range(dim):
        sel = (freqs >= edges[k]) & (freqs < edges[k + 1])
        out.append(float(p[sel].sum()) if sel.any() else 0.0)

    v = np.array(out, dtype=float)
    nrm = float(np.linalg.norm(v))
    return list(v / nrm) if nrm > 0 else list(v)


# ── Occupancy and rank ────────────────────────────────────────────────────────

def occupancy(epoch: Epoch) -> Dict[str, Any]:
    """
    Per-dimension energy fraction, and the participation ratio.

    participation_ratio = 1 / sum(f_k^2), the effective number of
    dimensions carrying the signal. 1.0 = one dimension does everything;
    dim = perfectly spread.
    """
    e = _require(epoch, 'occupancy')
    A = e.array()
    energy = (A ** 2).sum(axis=0)
    total = float(energy.sum())
    frac = energy / total if total > 0 else energy
    pr = float(1.0 / (frac ** 2).sum()) if total > 0 else 0.0
    return {
        'stamp':               e.stamp,
        'label':               e.label,
        'per_dimension':       [float(x) for x in frac],
        'participation_ratio': pr,
        'dead_dimensions':     [int(k) for k in np.where(frac < 1e-12)[0]],
        'total_energy':        total,
    }


def singular_spectrum(epoch: Epoch) -> List[float]:
    """Singular values of the (n x dim) field, descending."""
    e = _require(epoch, 'singular_spectrum')
    return [float(x) for x in np.linalg.svd(e.array(), compute_uv=False)]


def numerical_rank(epoch: Epoch, tol: Optional[float] = None) -> Dict[str, Any]:
    """
    Numerical rank at a stated tolerance.

    Default tol follows the standard convention: max(n,dim) * eps * s_max.
    The tolerance is returned, because a rank without its tolerance is not
    a measurement.
    """
    e = _require(epoch, 'numerical_rank')
    s = np.linalg.svd(e.array(), compute_uv=False)
    smax = float(s[0]) if s.size else 0.0
    t = float(tol) if tol is not None else max(e.n, e.dim) * np.finfo(float).eps * smax
    return {
        'stamp':           e.stamp,
        'rank':            int((s > t).sum()),
        'full_rank':       int(min(e.n, e.dim)),
        'deficiency':      int(min(e.n, e.dim) - (s > t).sum()),
        'tolerance':       t,
        'singular_values': [float(x) for x in s],
    }


def orthonormal_span(epoch: Epoch, tol: Optional[float] = None) -> np.ndarray:
    """Orthonormal basis (dim x rank) of the row space. Columns are basis vectors."""
    e = _require(epoch, 'orthonormal_span')
    A = e.array()
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    smax = float(s[0]) if s.size else 0.0
    t = float(tol) if tol is not None else max(e.n, e.dim) * np.finfo(float).eps * smax
    return Vt[s > t].T


# ── Angular content ───────────────────────────────────────────────────────────

def common_direction(epoch: Epoch) -> List[float]:
    """The mean unit direction -- the common mode. Phase 23's `cbar`."""
    e = _require(epoch, 'common_direction')
    A = e.array()
    nrm = np.linalg.norm(A, axis=1, keepdims=True)
    nrm[nrm == 0] = 1.0
    m = (A / nrm).mean(axis=0)
    mn = float(np.linalg.norm(m))
    return [float(x) for x in (m / mn if mn > 0 else m)]


def angular_residual(epoch: Epoch) -> Dict[str, Any]:
    """
    THE PHASE 27.2 MEASURE. How much direction survives the common mode.

    For each unit vector u: cos = <u, c>, residual = sqrt(1 - cos^2) --
    the sine of the angle to the common direction. Mean over the field.

    residual -> 0    the field is a scalar wearing 16 coordinates
    residual  > 0    there is real angular content
    """
    e = _require(epoch, 'angular_residual')
    A = e.array()
    nrm = np.linalg.norm(A, axis=1, keepdims=True)
    keep = (nrm.ravel() > 0)
    if not keep.any():
        raise ValueError("field is entirely zero -- no direction to measure")
    U = A[keep] / nrm[keep]
    c = np.asarray(common_direction(e), dtype=float)
    cos = np.clip(U @ c, -1.0, 1.0)
    res = np.sqrt(np.maximum(0.0, 1.0 - cos ** 2))
    return {
        'stamp':               e.stamp,
        'label':               e.label,
        'mean_angular_residual': float(res.mean()),
        'mean_collapse_cos':     float(cos.mean()),
        'min_residual':          float(res.min()),
        'max_residual':          float(res.max()),
        'n_measured':            int(keep.sum()),
        'n_zero_skipped':        int((~keep).sum()),
    }


def score_against_calibration(residual: float) -> Dict[str, Any]:
    """
    Place a measured residual against the published Phase 27.2 references.

    ⚠ Valid ONLY for the phonetic-face embedding. Returns the caveat with
      the answer so it cannot travel without it.
    """
    r = float(residual)
    refs = {k: v['angular_residual'] for k, v in CALIBRATION.items()}
    nearest = min(refs, key=lambda k: abs(refs[k] - r))
    if r < 0.01:
        verdict = 'SCALAR -- no angular content; this is an e_0 address, not a direction'
    elif r < 0.20:
        verdict = 'COLLAPSED -- near the common mode, like the Phase 23 character encoder'
    elif r < 0.60:
        verdict = 'ANGULAR -- real direction, comparable to the phonetic face'
    else:
        verdict = 'HIGHLY ANGULAR -- exceeds every English reference measured'
    return {
        'residual':          r,
        'nearest_reference': nearest,
        'references':        refs,
        'verdict':           verdict,
        'caveat':            'CALIBRATION IS EMBEDDING-SPECIFIC (phonetic face, Phase 27.2). '
                             'Does not transfer to embed_log_bands or any other embedding.',
    }


# ── The zero divisor, its null space, and provenance ──────────────────────────

def left_mul_matrix(a: Sequence[float]) -> np.ndarray:
    """
    The 16x16 matrix L_a with L_a v = a * v, built from the CD table in
    box_kite.maths. Not reimplemented here -- one multiplication table in
    the repo, and this borrows it.
    """
    a = np.asarray(a, dtype=float)
    if a.size != SEDENION_DIM:
        raise ValueError(f"need a {SEDENION_DIM}-vector")
    L = np.zeros((SEDENION_DIM, SEDENION_DIM), dtype=float)
    for j in range(SEDENION_DIM):
        for i in range(SEDENION_DIM):
            if a[i] == 0.0:
                continue
            sgn, k = basis_mul(i, j)      # box_kite returns (sign, index)
            L[k, j] += sgn * a[i]
    return L


def null_space(a: Sequence[float], tol: float = 1e-10) -> Dict[str, Any]:
    """
    ker(L_a) -- the dimensions `a` annihilates.

    For a true Assessor diagonal this returns nullity 4 and the {4,8,4}
    singular-value split. See Null-Space-of-the-Zero-Divisor.md.
    """
    L = left_mul_matrix(a)
    U, s, Vt = np.linalg.svd(L)
    ker = Vt[s <= tol]
    return {
        'nullity':         int(ker.shape[0]),
        'rank':            int((s > tol).sum()),
        'singular_values': [float(x) for x in s],
        'basis':           [[float(x) for x in row] for row in ker],
        'is_zero_divisor': bool((s <= tol).any()),
    }


def verify_null_space() -> Dict[str, Any]:
    """
    THE HONEST CHECK. a = (e_1 + e_10)/sqrt(2), Assessor (1,2), strut 3.

    Agreement with Null-Space-of-the-Zero-Divisor.md is a CHECK, not an
    input: nullity 4, rank 12, singular values {1.414 x4, 1.000 x8, 0 x4}.
    """
    a = [0.0] * SEDENION_DIM
    a[1] = a[10] = 1.0 / math.sqrt(2.0)
    ns = null_space(a)
    s = np.asarray(ns['singular_values'])
    counts = {
        'sqrt2': int((np.abs(s - math.sqrt(2.0)) < 1e-9).sum()),
        'one':   int((np.abs(s - 1.0) < 1e-9).sum()),
        'zero':  int((np.abs(s) < 1e-9).sum()),
    }
    return {
        'assessor':          (1, 2),
        'strut':             1 ^ 2,
        'nullity':           ns['nullity'],
        'rank':              ns['rank'],
        'singular_counts':   counts,
        'expected_counts':   {'sqrt2': 4, 'one': 8, 'zero': 4},
        'matches_published': (ns['nullity'] == 4 and ns['rank'] == 12
                              and counts == {'sqrt2': 4, 'one': 8, 'zero': 4}),
    }


def null_occupancy(epoch: Epoch, a: Sequence[float], tol: float = 1e-10) -> Dict[str, Any]:
    """
    What fraction of the field's energy lies in ker(L_a)?

    THE EXTERNAL-SIGNAL INDICATOR. The internal channel is a functional of
    its own state and cannot emit into the four dimensions its own
    operator annihilates. Energy there did not come from L_a.

    ⚠ SILENT FAILURE MODE (Operating-L-IO 4.4): if the ear is wired
      THROUGH L_a rather than summed in downstream of it, the external
      signal is annihilated identically and this returns ~0 with no error.
      A zero here means EITHER nothing external OR a wiring fault. It does
      not distinguish them. Verify the wiring separately.
    """
    e = _require(epoch, 'null_occupancy')
    if e.dim != SEDENION_DIM:
        raise ValueError(f"null occupancy needs {SEDENION_DIM}-D vectors, got {e.dim}")
    ns = null_space(a, tol=tol)
    if not ns['is_zero_divisor']:
        raise ValueError("a is not a zero divisor -- ker(L_a) is trivial, nothing to test")
    K = np.asarray(ns['basis'], dtype=float).T
    A = e.array()
    total = float((A ** 2).sum())
    in_ker = float(((A @ K) ** 2).sum())
    frac = (in_ker / total) if total > 0 else 0.0
    base = ns['nullity'] / float(SEDENION_DIM)
    return {
        'stamp':            e.stamp,
        'nullity':          ns['nullity'],
        'energy_in_kernel': in_ker,
        'energy_total':     total,
        'fraction':         frac,
        'isotropic_baseline': base,
        'excess':           frac - base,
        'reportable':       frac > base,
        'caveat':           'zero is ambiguous: no external signal OR ear wired through L_a',
    }


def null_occupancy_baseline(a: Sequence[float], tol: float = 1e-10) -> Dict[str, Any]:
    """
    THE MANDATORY NULL for null_occupancy().

    An isotropic random field puts nullity/dim of its energy in ker(L_a) --
    for a sedenion Assessor diagonal that is 4/16 = 0.25 exactly. Verified
    numerically here rather than asserted.

    ⚠ A raw fraction near 0.25 is therefore EVIDENCE OF NOTHING. Only the
      EXCESS over this baseline is a signal. Report the excess, never the
      raw fraction -- the same rule as 'read the z-score, never the raw r'
      (L_IO_SPECIFICATION 3).
    """
    ns = null_space(a, tol=tol)
    if not ns['is_zero_divisor']:
        raise ValueError("a is not a zero divisor -- no kernel to baseline")
    rng = np.random.default_rng(20260815)
    K = np.asarray(ns['basis'], dtype=float).T
    A = rng.standard_normal((20000, SEDENION_DIM))
    measured = float(((A @ K) ** 2).sum() / (A ** 2).sum())
    analytic = ns['nullity'] / float(SEDENION_DIM)
    return {
        'nullity':          ns['nullity'],
        'analytic_baseline': analytic,
        'measured_baseline': measured,
        'agreement':        abs(measured - analytic) < 5e-3,
        'rule':             'report EXCESS over baseline, never the raw fraction',
    }


def principal_angles(P: np.ndarray, Q: np.ndarray) -> List[float]:
    """Principal angles (radians, ascending) between two orthonormal column spans."""
    if P.size == 0 or Q.size == 0:
        return []
    s = np.linalg.svd(P.T @ Q, compute_uv=False)
    return [float(math.acos(min(1.0, max(-1.0, x)))) for x in s]


def external_component(signal: Epoch, internal: Epoch,
                       tol: Optional[float] = None) -> Dict[str, Any]:
    """
    Energy of `signal` outside the span of `internal`.

    BOTH ARGUMENTS ARE EPOCHS. That is the whole correction: the internal
    span is frozen at a stated stamp, so the measurement cannot be taken
    across a concurrent write to the thinking threads.
    """
    s_ = _require(signal, 'external_component')
    i_ = _require(internal, 'external_component')
    if s_.dim != i_.dim:
        raise ValueError("signal and internal epochs must share a dimension")
    B = orthonormal_span(i_, tol=tol)
    A = s_.array()
    total = float((A ** 2).sum())
    inside = float(((A @ B) ** 2).sum()) if B.size else 0.0
    return {
        'signal_stamp':      s_.stamp,
        'internal_stamp':    i_.stamp,
        'internal_rank':     int(B.shape[1]) if B.size else 0,
        'energy_total':      total,
        'energy_inside':     inside,
        'energy_outside':    total - inside,
        'fraction_outside':  ((total - inside) / total) if total > 0 else 0.0,
        'principal_angles':  principal_angles(orthonormal_span(s_, tol=tol), B),
    }


def precession(before: Epoch, after: Epoch,
               tol: Optional[float] = None) -> Dict[str, Any]:
    """
    Drift between two epochs of the same channel.

    Mutation is permitted. What is forbidden is measuring ACROSS it. This
    dates the mutation instead, and reports whether it is the bounded kind.

    largest_principal_angle -> 0     the span held
    rank_delta > 0                   the internal span GREW; any earlier
                                     external-occupancy result taken
                                     against `before` is now stale

    Phase 27.3 is the bounded reference: net winding +0.0000 turns,
    non-accumulating, held by the gearing rather than computed. Growth
    that does not level off is the seizure warning.
    """
    b = _require(before, 'precession')
    a = _require(after, 'precession')
    if b.dim != a.dim:
        raise ValueError("epochs must share a dimension")
    Pb, Pa = orthonormal_span(b, tol=tol), orthonormal_span(a, tol=tol)
    ang = principal_angles(Pb, Pa)
    rb = int(Pb.shape[1]) if Pb.size else 0
    ra = int(Pa.shape[1]) if Pa.size else 0
    return {
        'before_stamp':           b.stamp,
        'after_stamp':            a.stamp,
        'unchanged':              b.stamp == a.stamp,
        'rank_before':            rb,
        'rank_after':             ra,
        'rank_delta':             ra - rb,
        'principal_angles':       ang,
        'largest_principal_angle': max(ang) if ang else 0.0,
        'stale_measurements':     ra != rb or (max(ang) if ang else 0.0) > 1e-9,
    }


# ── The report card ───────────────────────────────────────────────────────────

def angular_report(epoch: Epoch,
                   a: Optional[Sequence[float]] = None,
                   internal: Optional[Epoch] = None,
                   embedding: str = 'unstated') -> Dict[str, Any]:
    """
    THE STRESS TEST, one card. Every entry carries the epoch stamp it was
    read from, and the embedding it is relative to.
    """
    e = _require(epoch, 'angular_report')
    ang = angular_residual(e)
    card: Dict[str, Any] = {
        'label':       e.label,
        'stamp':       e.stamp,
        'embedding':   embedding,
        'n_vectors':   e.n,
        'dimension':   e.dim,
        'rank':        numerical_rank(e),
        'occupancy':   occupancy(e),
        'angular':     ang,
        'calibration': score_against_calibration(ang['mean_angular_residual']),
    }
    if a is not None:
        card['null_occupancy'] = null_occupancy(e, a)
    if internal is not None:
        card['external'] = external_component(e, internal)
    return card
