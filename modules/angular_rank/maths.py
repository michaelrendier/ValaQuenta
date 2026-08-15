"""
ainulindale_engine.modules.angular_rank.maths
================================================
THE 16D OSCILLOSCOPE -- angular content and subspace occupancy, measured
on a FROZEN DATUM.

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

THE DATUM DISCIPLINE -- why every entry point takes a datum
--------------------------------------------------------------
The rank test of Operating-L_(I|O) 4.4 as first written was WRONG in exactly
the way Cody names above: it read "dimensions the internal trace never
populates" while the thinking threads were concurrently GROWING that
trace. Measuring a span that the measured process is mutating is
iterate-while-modify, one level up. It does not raise. It drifts, silently,
until the internal span covers ker(L_a) and the instrument reports "all
quiet" forever.

The fix is not a lock. It is a DATUM.

WHICH CALL TO MAKE
------------------
    datum(field, label)   -> Datum
        Freeze a field. DEFINITIONAL: self-contained, content-stamped,
        meaningful with no other datum present. The only way in -- every
        other entry point refuses a live sequence.

    sight(held, live)     -> {'moved': bool, 'datum': Datum, ...}
        ONE guarded read against a datum you already hold. Binary: did it
        move under you? Cheap -- one re-stamp, no SVD, no second state
        retained. USE THIS IN A LOOP. When it reports moved, re-datum from
        the Datum it hands back rather than hashing twice.

    bearing(before, after) -> principal angles, rank delta, stale flag
        RELATIONAL: how FAR did it move, and is the drift bounded or
        accumulating? Needs both states. USE THIS WHEN THE ANSWER HAS TO BE
        REPORTABLE.

⚠ DO NOT substitute sight() for bearing(). A moved-flag is not a drift
  meter: bounded and unbounded drift both set moved=True, and only a bearing
  separates them. That separation is the difference between a healthy engine
  and a seizure.

⚠ DO NOT name anything here 'precession'. That word is taken, with a
  kinematic meaning -- the ZD wobble's signature, "one L_(I|O) cycle = one
  precession revolution" (Ainulindale wiki/68, h_rb_hat.precession_stroke,
  tier7_cosmos, telperion). It is a property of the rotor, never a
  difference between two readings.

⚠ NO MEASUREMENT IS REPORTABLE WITHOUT ITS DATUM. This is the same rule
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
    'SEDENION_DIM', 'CALIBRATION', 'Datum',
    'datum', 'is_datum', 'sight',
    'embed_log_bands',
    'occupancy', 'singular_spectrum', 'numerical_rank', 'orthonormal_span',
    'common_direction', 'angular_residual', 'score_against_calibration',
    'left_mul_matrix', 'null_space', 'verify_null_space', 'null_occupancy',
    'external_component', 'principal_angles', 'bearing', 'null_occupancy_baseline',
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


# ── The Datum ─────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Datum:
    """An immutable, content-stamped reference point for a field.

    Frozen dataclass over tuples-of-tuples: there is no supported way to
    mutate one after construction. That is the point -- a measurement cannot
    straddle a write.

    Build one with :func:`datum`; do not construct directly.

    :ivar vectors: the frozen field.
    :ivar label: name carried onto every measurement read from this Datum.
    :ivar stamp: sha256 over label and contents.
    :ivar n: number of vectors.
    :ivar dim: dimension of each vector.
    """
    vectors: Tuple[Tuple[float, ...], ...]
    label:   str
    stamp:   str
    n:       int
    dim:     int

    def array(self) -> np.ndarray:
        """Return a fresh mutable copy for numeric work. Never shared.

        :returns: a new array of the frozen vectors.
        :rtype: numpy.ndarray
        """
        return np.array(self.vectors, dtype=float)

    def __repr__(self) -> str:
        return f"<Datum {self.label!r} n={self.n} dim={self.dim} stamp={self.stamp[:12]}>"


def datum(vectors: Sequence[Sequence[float]], label: str = 'unlabelled') -> Datum:
    """Freeze a field into a :class:`Datum`. The only way into this module.

    Copies eagerly, so a later mutation of the caller's list cannot reach the
    returned Datum. The stamp is a sha256 over the rounded contents, so two
    datums of an unchanged field compare equal and a single changed element
    is visible.

    :param vectors: the field to freeze; rows must all share a dimension.
    :type vectors: collections.abc.Sequence[collections.abc.Sequence[float]]
    :param label: name carried on every measurement read from this Datum.
    :type label: str
    :returns: an immutable, content-stamped reference point.
    :rtype: Datum
    :raises ValueError: if ``vectors`` is empty or ragged.
    """
    rows = [tuple(float(x) for x in row) for row in vectors]
    if not rows:
        raise ValueError("datum() of an empty field -- nothing to measure")
    dim = len(rows[0])
    if any(len(r) != dim for r in rows):
        raise ValueError("ragged field: every vector must have the same dimension")

    h = hashlib.sha256()
    h.update(label.encode('utf-8'))
    for r in rows:
        for x in r:
            h.update(f"{x:.12e}|".encode('ascii'))

    return Datum(vectors=tuple(rows), label=label, stamp=h.hexdigest(),
                 n=len(rows), dim=dim)


def is_datum(x: Any) -> bool:
    """Test whether an object is a :class:`Datum`.

    :param x: any object.
    :returns: True if ``x`` is a Datum.
    :rtype: bool
    """
    return isinstance(x, Datum)


def sight(held: Datum, live: Sequence[Sequence[float]]) -> Dict[str, Any]:
    """Take one guarded read against a held datum: did the field move?

    Re-stamps ``live`` and compares it to ``held``. Cheap -- one hash, no
    SVD, no second state retained. This is the seqlock pattern. Call it in a
    loop; when it reports movement, re-datum from the Datum it returns
    rather than hashing twice.

    .. warning::
       Do not substitute this for :func:`bearing`. A moved-flag is not a
       drift meter: bounded and unbounded drift both set ``moved`` True, and
       only a bearing separates them.

    :param held: the reference point you are already holding.
    :type held: Datum
    :param live: the field as it stands now.
    :type live: collections.abc.Sequence[collections.abc.Sequence[float]]
    :returns: keys ``moved``, ``shape_changed``, ``held_stamp``,
              ``live_stamp``, ``datum`` (the fresh Datum), ``label``, ``note``.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if ``held`` is not a :class:`Datum`.

    .. seealso:: :func:`bearing` for how far it moved.
    """
    h = _require(held, 'sight')
    now = datum(live, h.label)
    return {
        'label':       h.label,
        'held_stamp':  h.stamp,
        'live_stamp':  now.stamp,
        'moved':       now.stamp != h.stamp,
        'shape_changed': (now.n, now.dim) != (h.n, h.dim),
        'datum':       now,
        'note': 'binary detection only -- use bearing() for how far, and '
                'for whether the drift is bounded or accumulating',
    }


def _require(e: Any, who: str) -> Datum:
    """Refuse a live sequence. The guard rail, not a convenience.

    :param e: the object a public entry point was handed.
    :param who: caller name, used in the error message.
    :returns: ``e`` unchanged when it is a Datum.
    :rtype: Datum
    :raises TypeError: if ``e`` is not a Datum, explaining that measuring a
        live field is iterate-while-modify and drifts silently.
    """
    if not isinstance(e, Datum):
        raise TypeError(
            f"{who}() requires an Datum, got {type(e).__name__}. "
            f"Call datum(field, label) first -- measuring a live field is "
            f"iterate-while-modify and will drift silently."
        )
    return e


# ── Embedding ─────────────────────────────────────────────────────────────────

def embed_log_bands(power_spectrum: Sequence[float],
                    sample_rate: float = 96000.0,
                    f_lo: float = 40.0,
                    f_hi: Optional[float] = None,
                    dim: int = SEDENION_DIM) -> List[float]:
    """Embed one power spectrum into ``dim`` log-spaced band energies.

    Language-agnostic by construction: no phoneme inventory, no lexicon, no
    assumption of human vocal-tract bandwidth. Use for cetacean recordings,
    where energy runs past 100 kHz and an English-derived band layout is a
    category error.

    L2-normalises, discarding loudness on purpose -- this instrument measures
    direction.

    :param power_spectrum: one-dimensional power spectrum.
    :param sample_rate: sample rate in Hz; sets the Nyquist edge.
    :type sample_rate: float
    :param f_lo: low edge of the lowest band, Hz.
    :type f_lo: float
    :param f_hi: high edge of the highest band, Hz. Defaults to Nyquist.
    :type f_hi: float | None
    :param dim: number of bands to produce.
    :type dim: int
    :returns: an L2-normalised vector of length ``dim``.
    :rtype: list[float]
    :raises ValueError: if the spectrum is not 1-D with at least ``dim``
        bins, or the band range is invalid for the Nyquist frequency.

    .. warning::
       The embedding is an INPUT, not a property of the signal. The
       :data:`CALIBRATION` constants were measured on the phonetic-face
       embedding and do NOT transfer here. Report the embedding with the
       number, always.
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

def occupancy(ref: Datum) -> Dict[str, Any]:
    """Report per-dimension energy fraction and participation ratio.

    ``participation_ratio`` is ``1 / sum(f_k**2)``: the effective number of
    dimensions carrying the signal. 1.0 means one dimension does everything;
    ``dim`` means perfectly spread.

    :param ref: the frozen field to measure.
    :type ref: Datum
    :returns: keys ``per_dimension``, ``participation_ratio``,
              ``dead_dimensions``, ``total_energy``, ``stamp``, ``label``.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    """
    e = _require(ref, 'occupancy')
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


def singular_spectrum(ref: Datum) -> List[float]:
    """Return the singular values of the field, descending.

    :param ref: the frozen field.
    :type ref: Datum
    :returns: singular values, largest first.
    :rtype: list[float]
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    """
    e = _require(ref, 'singular_spectrum')
    return [float(x) for x in np.linalg.svd(e.array(), compute_uv=False)]


def numerical_rank(ref: Datum, tol: Optional[float] = None) -> Dict[str, Any]:
    """Compute numerical rank at a stated tolerance.

    A rank without its tolerance is not a measurement, so the tolerance is
    returned alongside. The default follows the standard convention:
    ``max(n, dim) * eps * s_max``.

    :param ref: the frozen field.
    :type ref: Datum
    :param tol: singular values above this count toward the rank.
    :type tol: float | None
    :returns: keys ``rank``, ``full_rank``, ``deficiency``, ``tolerance``,
              ``singular_values``, ``stamp``.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    """
    e = _require(ref, 'numerical_rank')
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


def orthonormal_span(ref: Datum, tol: Optional[float] = None) -> np.ndarray:
    """Return an orthonormal basis of the field's row space.

    :param ref: the frozen field.
    :type ref: Datum
    :param tol: rank tolerance; defaults to the standard SVD convention.
    :type tol: float | None
    :returns: a ``(dim, rank)`` array whose columns are basis vectors.
    :rtype: numpy.ndarray
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    """
    e = _require(ref, 'orthonormal_span')
    A = e.array()
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    smax = float(s[0]) if s.size else 0.0
    t = float(tol) if tol is not None else max(e.n, e.dim) * np.finfo(float).eps * smax
    return Vt[s > t].T


# ── Angular content ───────────────────────────────────────────────────────────

def common_direction(ref: Datum) -> List[float]:
    """Return the mean unit direction -- the common mode, Phase 23's ``cbar``.

    :param ref: the frozen field.
    :type ref: Datum
    :returns: a unit vector.
    :rtype: list[float]
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    """
    e = _require(ref, 'common_direction')
    A = e.array()
    nrm = np.linalg.norm(A, axis=1, keepdims=True)
    nrm[nrm == 0] = 1.0
    m = (A / nrm).mean(axis=0)
    mn = float(np.linalg.norm(m))
    return [float(x) for x in (m / mn if mn > 0 else m)]


def angular_residual(ref: Datum) -> Dict[str, Any]:
    """Measure how much direction survives the common mode. Phase 27.2.

    For each unit vector ``u``: ``cos = <u, c>`` and
    ``residual = sqrt(1 - cos**2)`` -- the sine of the angle to the common
    direction. Averaged over the field.

    A residual near 0 means the field is a scalar wearing ``dim``
    coordinates; above 0 means real angular content.

    :param ref: the frozen field to measure.
    :type ref: Datum
    :returns: keys ``mean_angular_residual``, ``mean_collapse_cos``,
              ``min_residual``, ``max_residual``, ``n_measured``,
              ``n_zero_skipped``, ``stamp``, ``label``.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    :raises ValueError: if the field is entirely zero.

    .. seealso:: :func:`score_against_calibration`
    """
    e = _require(ref, 'angular_residual')
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
    """Place a measured residual against the published Phase 27.2 references.

    .. warning::
       Valid ONLY for the phonetic-face embedding. The caveat is returned
       with the answer so it cannot travel without it.

    :param residual: a mean angular residual.
    :type residual: float
    :returns: keys ``residual``, ``nearest_reference``, ``references``,
              ``verdict``, ``caveat``.
    :rtype: dict[str, typing.Any]
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
    """Build the matrix ``L_a`` satisfying ``L_a v == a * v``.

    Built from the Cayley-Dickson table in :mod:`box_kite.maths` -- one
    multiplication table in the repo, borrowed rather than reimplemented.

    :param a: a 16-vector.
    :type a: collections.abc.Sequence[float]
    :returns: the ``(16, 16)`` left-multiplication matrix.
    :rtype: numpy.ndarray
    :raises ValueError: if ``a`` is not a 16-vector.
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
    """Compute ``ker(L_a)`` -- the dimensions ``a`` annihilates.

    For a true Assessor diagonal this returns nullity 4 and the {4, 8, 4}
    singular-value split.

    :param a: a 16-vector.
    :type a: collections.abc.Sequence[float]
    :param tol: singular values below this count as zero.
    :type tol: float
    :returns: keys ``nullity``, ``rank``, ``singular_values``, ``basis``,
              ``is_zero_divisor``.
    :rtype: dict[str, typing.Any]
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
    """Reproduce the published {4, 8, 4} split as a CHECK, not an input.

    Uses ``a = (e_1 + e_10)/sqrt(2)``, Assessor (1, 2), strut 3. Agreement
    with ``Null-Space-of-the-Zero-Divisor.md`` is verified here rather than
    assumed: nullity 4, rank 12, singular values sqrt2 x4 / 1 x8 / 0 x4.

    :returns: keys ``assessor``, ``strut``, ``nullity``, ``rank``,
              ``singular_counts``, ``expected_counts``, ``matches_published``.
    :rtype: dict[str, typing.Any]
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


def null_occupancy(ref: Datum, a: Sequence[float], tol: float = 1e-10) -> Dict[str, Any]:
    """Measure what fraction of the field's energy lies in ``ker(L_a)``.

    The external-signal indicator. The internal channel is a functional of
    its own state and cannot emit into the dimensions its own operator
    annihilates, so energy there did not come from ``L_a``.

    .. warning::
       Report ``excess``, never ``fraction``. An isotropic field already puts
       ``nullity/dim`` of its energy in the kernel -- exactly 0.25 for a
       sedenion Assessor diagonal. See :func:`null_occupancy_baseline`.

    .. warning::
       A result near zero is AMBIGUOUS: either there is no external signal,
       or the ear is wired *through* ``L_a`` instead of summed in downstream
       of it, in which case the external component is annihilated
       identically and this returns ~0 with no error raised. Verify the
       wiring separately.

    :param ref: the frozen field to measure.
    :type ref: Datum
    :param a: the zero divisor whose kernel is tested.
    :type a: collections.abc.Sequence[float]
    :param tol: singular values below this count as zero.
    :type tol: float
    :returns: keys ``fraction``, ``excess``, ``reportable``,
              ``isotropic_baseline``, ``nullity``, ``energy_in_kernel``,
              ``energy_total``, ``stamp``, ``caveat``.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    :raises ValueError: if the field is not 16-dimensional, or ``a`` is not a
        zero divisor.
    """
    e = _require(ref, 'null_occupancy')
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
    """Compute the mandatory null for :func:`null_occupancy`.

    An isotropic random field puts ``nullity/dim`` of its energy in
    ``ker(L_a)`` -- exactly 4/16 = 0.25 for a sedenion Assessor diagonal.
    Verified numerically here rather than asserted.

    .. warning::
       A raw fraction near 0.25 is therefore EVIDENCE OF NOTHING. Report the
       excess over this baseline, never the raw fraction -- the same rule as
       "read the z-score, never the raw r".

    :param a: the zero divisor whose kernel is baselined.
    :type a: collections.abc.Sequence[float]
    :param tol: singular values below this count as zero.
    :type tol: float
    :returns: keys ``nullity``, ``analytic_baseline``, ``measured_baseline``,
              ``agreement``, ``rule``.
    :rtype: dict[str, typing.Any]
    :raises ValueError: if ``a`` is not a zero divisor.
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
    """Return principal angles between two orthonormal column spans.

    :param P: first span, columns orthonormal.
    :type P: numpy.ndarray
    :param Q: second span, columns orthonormal.
    :type Q: numpy.ndarray
    :returns: angles in radians, ascending.
    :rtype: list[float]
    """
    if P.size == 0 or Q.size == 0:
        return []
    s = np.linalg.svd(P.T @ Q, compute_uv=False)
    return [float(math.acos(min(1.0, max(-1.0, x)))) for x in s]


def external_component(signal: Datum, internal: Datum,
                       tol: Optional[float] = None) -> Dict[str, Any]:
    """Measure the energy of a signal outside a frozen internal span.

    Both arguments are datums. That is the correction: the internal span is
    frozen at a stated stamp, so the measurement cannot be taken across a
    concurrent write to the thinking threads.

    :param signal: the field under test.
    :type signal: Datum
    :param internal: the internal span it is measured against.
    :type internal: Datum
    :param tol: rank tolerance; defaults to the standard SVD convention.
    :type tol: float | None
    :returns: keys ``fraction_outside``, ``energy_outside``,
              ``energy_inside``, ``energy_total``, ``internal_rank``,
              ``principal_angles``, ``signal_stamp``, ``internal_stamp``.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if either argument is not a :class:`Datum`.
    :raises ValueError: if the two datums have different dimensions.
    """
    s_ = _require(signal, 'external_component')
    i_ = _require(internal, 'external_component')
    if s_.dim != i_.dim:
        raise ValueError("signal and internal datums must share a dimension")
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


def bearing(before: Datum, after: Datum,
               tol: Optional[float] = None) -> Dict[str, Any]:
    """Measure how far a field's span moved between two datums.

    RELATIONAL: this reading does not exist until something has moved, and
    what it measures is the relation, not either state. Mutation is
    permitted; what is forbidden is measuring across it, so this dates the
    mutation instead.

    ``rank_delta`` above zero means the span GREW, and any earlier
    external-occupancy result taken against ``before`` is now stale.

    Phase 27.3 is the bounded reference: net winding +0.0000 turns,
    non-accumulating, held by the gearing rather than computed. Growth that
    does not level off is the seizure warning.

    :param before: the earlier reference point.
    :type before: Datum
    :param after: the later reference point.
    :type after: Datum
    :param tol: rank tolerance; defaults to the standard SVD convention.
    :type tol: float | None
    :returns: keys ``rank_before``, ``rank_after``, ``rank_delta``,
              ``principal_angles``, ``largest_principal_angle``,
              ``stale_measurements``, ``unchanged``, ``before_stamp``,
              ``after_stamp``.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if either argument is not a :class:`Datum`.
    :raises ValueError: if the two datums have different dimensions.

    .. seealso:: :func:`sight` for the cheap binary check.
    """
    b = _require(before, 'bearing')
    a = _require(after, 'bearing')
    if b.dim != a.dim:
        raise ValueError("datums must share a dimension")
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

def angular_report(ref: Datum,
                   a: Optional[Sequence[float]] = None,
                   internal: Optional[Datum] = None,
                   embedding: str = 'unstated') -> Dict[str, Any]:
    """Produce the full stress-test card for one field.

    Every entry carries the stamp it was read from and the embedding it is
    relative to.

    .. warning::
       No measurement is reportable without its datum.

    :param ref: the frozen field to measure.
    :type ref: Datum
    :param a: optional zero divisor; adds ``null_occupancy`` to the card.
    :type a: collections.abc.Sequence[float] | None
    :param internal: optional internal span; adds ``external`` to the card.
    :type internal: Datum | None
    :param embedding: name of the embedding used, recorded on the card.
    :type embedding: str
    :returns: the report card.
    :rtype: dict[str, typing.Any]
    :raises TypeError: if ``ref`` is not a :class:`Datum`.
    """
    e = _require(ref, 'angular_report')
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
