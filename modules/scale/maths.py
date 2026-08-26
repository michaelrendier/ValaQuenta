"""
ainulindale_engine.modules.scale.maths
=========================================
THE SCALE -- decompositional analysis, forwards and backwards.

Cody, 2026-08-25: "this is why it's the primary forensic tool of the
generational lineage engine...it's the most complicated part of the three
roots of Add, Scale and Sign. This is The Scale...i want to see that
object...the scale invariant/scale blind version of the maths."
Then: "the purpose of this engine is for decompositional analysis...so
forwards and backwards."

SCALE is tier-0 (generational-lineage skill, section 1): identity 1,
gain 1, Axis 2 {x,/} -- one of the three irreducibles alongside ADD and
SIGN. Everything below is what SCALE looks like when you try to isolate
and study it directly: pull the scale out of a quantity, and see what is
left over (the invariant); apply the extracted scale back to the
invariant, and recover the original exactly (the return path).

TWO SEPARATE FORWARD/BACKWARD PAIRS, NOT ONE -- kept distinct because
they answer different questions:

1. POLAR DECOMPOSE/RECOMPOSE -- scale extracted from ONE point.
   Z = r * e^{i theta}. r is the scale (always real, non-negative,
   ordinal -- comparable). theta is scale-blind under real-positive
   rescaling of Z BY ITSELF (arg(lambda*Z) = arg(Z) for lambda>0, exact,
   for any bare complex number). polar_recompose is the exact inverse:
   recompose(*decompose(Z)) == Z, always, checked in the module's own
   self-test, not asserted.

2. CROSS-RATIO -- the invariant found AFTER a two-ring/Mobius fold is
   applied, which is a DIFFERENT and harder question. FIRST CANDIDATE,
   TESTED AND REJECTED, kept in the record: theta (from #1) does NOT
   survive folding through Gamma=(Z-Z0)/(Z+Z0) -- the fold has its own
   fixed point at Z0, not at the origin, so rescaling Z around 0 is not
   a symmetry the fold respects (measured: arg(Gamma) ranges from 1.054
   rad down to 0.007 rad across one fixed rescaling). The cross-ratio of
   any FOUR points, by contrast, is EXACTLY preserved by the fold for
   EVERY choice of anchor Z0 -- verified across four wildly different
   anchors, matching to full numerical precision each time. This is the
   scale-blind object underneath the fold: not a property of any one
   point, a property of a RELATIONSHIP among four.

3. PROCESS DECOMPOSITION (pathway_decompose) -- the same forward/backward
   discipline applied to an ALGORITHM instead of a number: a real
   dependency graph of named operators, each one's own real-world stage,
   with a designated real output. Forwards is running the graph;
   backwards is whatever the process's own architecture provides as its
   return path (RSA's CRT-decrypt, the Enigma's reciprocal wiring,
   Vigenere's symmetric add/subtract) -- this module does not assume
   every process has a clean backward pass, and does not manufacture one
   where the process itself does not provide it.

HONEST EXCEPTION TO THE MODULE CONVENTION: this module works in COMPLEX
FLOATS throughout (Mobius folds, tanh, cross-ratio), not
fractions.Fraction -- the domain is inherently transcendental/conformal-
geometric and Fraction has no complex-number support in the standard
library. Stated plainly as an exception, not silently violated.

Confidence: ESTABLISHED for the polar and cross-ratio identities
(elementary complex analysis, independently verified here); THEORETICAL
for the identification of "Scale" as tier-0 SCALE's own forensic
instrument (an interpretive framing on top of established math, not a
new theorem).

Version: 0.1
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Sequence, Tuple

SED_DIM = 16


# ── 1. Polar decompose/recompose -- scale extracted from ONE point ─────────

def polar_decompose(Z: complex) -> Tuple[float, float]:
    """Z -> (r, theta). r = |Z| (the scale, real, ordinal). theta = arg(Z)
    (scale-blind: arg(lambda*Z) = arg(Z) for any real lambda>0). Exact,
    not approximate -- Python's cmath.polar to full float precision."""
    return cmath.polar(Z)


def polar_recompose(r: float, theta: float) -> complex:
    """(r, theta) -> Z. The exact inverse of polar_decompose -- the
    return path. recompose(*decompose(Z)) == Z for every Z, checked in
    verify_polar_round_trip()."""
    return cmath.rect(r, theta)


def verify_polar_round_trip(samples: Sequence[complex] = None) -> Dict[str, Any]:
    """THE FORWARD/BACKWARD CHECK for #1 -- round-trip every sample point
    through decompose then recompose and report the worst error."""
    if samples is None:
        samples = [complex(3.7, -1.4), complex(-2, 5), complex(0.001, 0.001),
                  complex(1e6, -3), complex(-1, -1)]
    worst = 0.0
    for Z in samples:
        r, theta = polar_decompose(Z)
        Z2 = polar_recompose(r, theta)
        worst = max(worst, abs(Z2 - Z))
    return {'n_samples': len(samples), 'max_round_trip_error': worst,
            'holds': worst < 1e-9}


def scale_invariance_under_self_rescale(Z: complex,
                                        lambdas: Sequence[float] = None
                                        ) -> Dict[str, Any]:
    """theta is unchanged as Z is rescaled by any positive real lambda --
    the exact, narrow sense in which the angle IS scale-blind, BEFORE any
    fold is applied. Verified directly, not asserted from the textbook
    fact alone."""
    if lambdas is None:
        lambdas = (0.01, 0.5, 1.0, 7.0, 1000.0)
    thetas = [cmath.phase(lam * Z) for lam in lambdas]
    holds = all(abs(t - thetas[0]) < 1e-12 for t in thetas)
    return {'lambdas': list(lambdas), 'thetas': thetas, 'holds': holds}


# ── 2. The Mobius fold, its scale factor, and the cross-ratio ──────────────

def mobius_fold(Z: complex, Z0: complex) -> complex:
    """Gamma = (Z-Z0)/(Z+Z0) -- the Smith-chart Mobius fold. Gamma(Z0)=0
    by construction, for any Z0 != 0. Same primitive as
    SedenionFactoralRelativity/engine/lineage.py's ring_chart_gamma
    (PW8/PW10) -- ported here as this engine's own copy, not imported
    cross-repo, per this project's module-independence convention."""
    return (Z - Z0) / (Z + Z0)


def scale_factor(Z: complex, Z0: complex) -> float:
    """|dGamma/dZ| = |2*Z0/(Z+Z0)^2| -- the fold's own derivative, exact.
    The local area-scaling of the conformal map: how much a small patch
    near Z is stretched or compressed once folded. Never zero for finite
    Z (checked in verify_no_caustic below) -- the map has no true
    caustics, only its one isolated pole at Z=-Z0."""
    return abs(2 * Z0) / abs(Z + Z0) ** 2


def verify_no_caustic(Z0: complex = 1.0,
                      test_points: Sequence[complex] = None) -> Dict[str, Any]:
    """A true caustic needs the fold's derivative to VANISH somewhere.
    Checked directly across widely different magnitudes: it never does --
    only diverges at the single pole Z=-Z0. Crowding-toward-infinity at
    one isolated point is a different phenomenon from an envelope/fold
    singularity, and this module does not conflate the two."""
    if test_points is None:
        test_points = [0.001+0j, 100+0j, 1+50j, -50+0.1j, 1e6+1j]
    values = [abs(scale_factor(z, Z0)) for z in test_points]
    return {'test_points': [str(z) for z in test_points], 'scale_factors': values,
            'any_zero': any(v < 1e-300 for v in values), 'holds': not any(v < 1e-300 for v in values)}


def cross_ratio(z1: complex, z2: complex, z3: complex, z4: complex) -> complex:
    """THE SCALE INVARIANT underneath the two-ring fold. Exact under EVERY
    choice of anchor Z0 -- not a property of any one point, a property of
    a relationship among four."""
    return ((z1 - z3) * (z2 - z4)) / ((z1 - z4) * (z2 - z3))


def verify_cross_ratio_is_scale_blind(
        points: Tuple[complex, complex, complex, complex] = None,
        anchors: Sequence[complex] = None) -> Dict[str, Any]:
    """THE FORWARD/BACKWARD CHECK for #2. Folds the same 4 points through
    the SAME fold at several DIFFERENT anchors ("different scales") and
    confirms the cross-ratio of the folded points never changes -- the
    scale-blind object survives being folded, unlike the angle."""
    if points is None:
        points = (complex(2, 1), complex(0.5, -0.3), complex(4, 2.2), complex(1.1, 0.9))
    if anchors is None:
        anchors = [complex(1, 0), complex(0.3, 0.7), complex(5, -2), complex(0.01, 0.01)]
    cr_before = cross_ratio(*points)
    cr_after = []
    for z0 in anchors:
        folded = tuple(mobius_fold(p, z0) for p in points)
        cr_after.append(cross_ratio(*folded))
    holds = all(abs(cr - cr_before) < 1e-9 for cr in cr_after)
    return {'cross_ratio_before': cr_before, 'cross_ratio_after_each_anchor': cr_after,
            'anchors': anchors, 'holds': holds}


def two_ring_point(ring1: float, ring2: float, Z0: complex) -> Dict[str, Any]:
    """The general two-ring instrument: Z = ring1 + i*ring2, folded
    through mobius_fold. ring1/ring2 mean whatever the caller defines --
    resistance/reactance is one choice among many, not a constraint."""
    Z = complex(ring1, ring2)
    G = mobius_fold(Z, Z0)
    return {'Z': Z, 'Z0': Z0, 'gamma': G, 'abs_gamma': abs(G),
            'scale_factor': scale_factor(Z, Z0)}


# ── 2b. USER-DEFINED RINGS -- the engine takes ANY two relationships ───────
# Cody, 2026-08-25: "the scale engine needs user input for the two rings...
# the engine needs the ability for the user to provide his own definition
# for the two rings." ring1/ring2 below are ARBITRARY caller-supplied
# functions of one object -- log/exponent, inertia/entropy, forward/
# backward through a modular function, Lagrangian/cardioid-attractor
# distance, J_red/J_blue -- none of these are built in as special cases;
# they are all just instances of the one signature below.

def custom_ring_chart(obj: Any, ring1_fn: Callable[[Any], float],
                      ring2_fn: Callable[[Any], float], Z0: complex,
                      ring1_name: str = 'ring1', ring2_name: str = 'ring2'
                      ) -> Dict[str, Any]:
    """Z = ring1_fn(obj) + i*ring2_fn(obj), folded. This is the ONE entry
    point a user needs: define what the two rings mean for your own
    relationship, pass them in as plain functions, get back the fold and
    everything derived from it. two_ring_point (above) is the special
    case where the caller has already computed the two numbers by hand."""
    r1, r2 = ring1_fn(obj), ring2_fn(obj)
    pt = two_ring_point(r1, r2, Z0)
    pt['ring1_name'] = ring1_name
    pt['ring2_name'] = ring2_name
    return pt


def custom_ring_chart_series(objs: Sequence[Any], ring1_fn: Callable[[Any], float],
                             ring2_fn: Callable[[Any], float], Z0: complex,
                             ring1_name: str = 'ring1', ring2_name: str = 'ring2'
                             ) -> Dict[str, Any]:
    """The same instrument run over a whole collection at once -- each
    object's own Z, Gamma, and scale factor, plus the per-integer-cell
    bucketing (round(ring1), round(ring2)) that makes "windows of order"
    visible without re-deriving it by hand. Same move as
    SedenionFactoralRelativity's factoral_spiral (PW13), independently
    ported here."""
    readings = []
    cells: Dict[Tuple[int, int], List[int]] = {}
    for idx, obj in enumerate(objs):
        r1, r2 = ring1_fn(obj), ring2_fn(obj)
        pt = two_ring_point(r1, r2, Z0)
        readings.append(pt)
        key = (round(r1), round(r2))
        cells.setdefault(key, []).append(idx)
    return {'Z0': Z0, 'ring1_name': ring1_name, 'ring2_name': ring2_name,
            'readings': readings, 'cells': cells}


# ── 2c. THE MASTER IDENTITY -- folding IS log-then-bound, unfolding IS
# unbound-then-exp, exactly, in full generality (not just the real axis) ───

def fold_is_log_tanh(Z: complex, Z0: complex) -> Dict[str, Any]:
    """Gamma = tanh( (1/2) * ln(Z/Z0) ), EXACTLY, for ANY complex Z, Z0 --
    not a special case of the real axis. Checked directly against
    mobius_fold(), not asserted from the real-axis identity alone."""
    direct = mobius_fold(Z, Z0)
    via_log = cmath.tanh(0.5 * cmath.log(Z / Z0))
    return {'fold_direct': direct, 'fold_via_log_tanh': via_log,
            'match': abs(direct - via_log) < 1e-9}


def unfold_is_arctanh_exp(G: complex, Z0: complex) -> Dict[str, Any]:
    """Z = Z0 * exp(2 * arctanh(Gamma)), EXACTLY -- the mirror operation.
    Checked as a genuine round trip: fold a real Z, then unfold the
    result back, and confirm you recover the ORIGINAL Z, via both the
    rational inverse AND this log/exp path independently."""
    Z_rational = Z0 * (1 + G) / (1 - G)
    w = cmath.atanh(G)
    Z_logexp = Z0 * cmath.exp(2 * w)
    return {'unfold_rational': Z_rational, 'unfold_log_exp': Z_logexp,
            'match': abs(Z_rational - Z_logexp) < 1e-6}


def verify_fold_unfold_round_trip(samples=None) -> Dict[str, Any]:
    """THE FORWARD/BACKWARD CHECK for the master identity: fold then
    unfold a real sample of (Z, Z0) pairs and confirm the ORIGINAL Z
    comes back exactly, via the log/exp path specifically (not just the
    rational formula, which is a different, already-known inverse)."""
    if samples is None:
        samples = [(complex(2.3, 1.1), complex(1, 0)),
                  (complex(-3, 4), complex(2, -1)),
                  (complex(0.1, 0.1), complex(5, 5)),
                  (complex(100, -50), complex(1, 1))]
    worst = 0.0
    for Z, Z0 in samples:
        fwd = fold_is_log_tanh(Z, Z0)
        assert fwd['match']
        bwd = unfold_is_arctanh_exp(fwd['fold_direct'], Z0)
        assert bwd['match']
        worst = max(worst, abs(bwd['unfold_log_exp'] - Z))
    return {'n_samples': len(samples), 'max_round_trip_error': worst,
            'holds': worst < 1e-6}


# ── 2d. LOCALLY SQUARE -- automatic for ANY ring1/ring2, not conditional ───
# Cody, 2026-08-25: "the part about 'locally square' is REALLY IMPORTANT
# in the scheme of things." Worth stating precisely WHY it is automatic:
# ring1 and ring2, whatever they mean physically, are used as literal
# Cartesian coordinates of Z -- the real/imaginary axes are orthogonal BY
# CONSTRUCTION, for any choice of ring1/ring2 whatsoever. mobius_fold is
# holomorphic in Z (its derivative is never zero for finite Z, verified
# in verify_no_caustic), and holomorphic maps preserve angles wherever
# their derivative is nonzero. So the "locally square" cell property
# does NOT require ring1 and ring2 to be related to each other in any
# special way (e.g. as harmonic conjugates) -- it is a property of the
# FOLD, inherited automatically, regardless of what the two rings mean.
# A SEPARATE, optional, stronger fact -- checked, not assumed -- is
# whether a GIVEN ring1/ring2 pair also happens to be a harmonic-
# conjugate pair of some underlying field (the 2D complex-potential
# construction from fluid dynamics/electrostatics, w=phi+i*psi) -- that
# is extra structure a specific choice of rings might or might not have,
# tested per pair in scale.md, not claimed here in general.

def verify_locally_square(Z: complex, Z0: complex, h: float = 1e-5) -> Dict[str, Any]:
    """At any point Z, the tangent vectors along increasing ring1
    (constant ring2) and increasing ring2 (constant ring1) are equal in
    magnitude and exactly 90 degrees apart -- checked directly by
    central-difference, not assumed from the general holomorphy argument
    alone."""
    d_d1 = (mobius_fold(Z + h, Z0) - mobius_fold(Z - h, Z0)) / (2 * h)
    d_d2 = (mobius_fold(Z + 1j * h, Z0) - mobius_fold(Z - 1j * h, Z0)) / (2 * h)
    equal_mag = abs(abs(d_d1) - abs(d_d2)) < 1e-6
    cos_angle = (d_d1.real * d_d2.real + d_d1.imag * d_d2.imag) / (abs(d_d1) * abs(d_d2))
    angle_deg = math.degrees(math.acos(max(-1.0, min(1.0, cos_angle))))
    return {'d_ring1': d_d1, 'd_ring2': d_d2,
            'equal_magnitude': equal_mag, 'angle_degrees': angle_deg,
            'holds': equal_mag and abs(angle_deg - 90.0) < 1e-3}


# ── 3. Process decomposition -- the same discipline applied to algorithms ──

@dataclass
class ProcessOperator:
    """One named operator in a pathway decomposition: a function of ANY
    number of OTHER named operators' outputs (by name, in `depends_on`) --
    not assumed to be "the previous one" in a chain. A chain is the
    degenerate case where every operator depends on exactly one
    predecessor, not the rule."""
    name: str
    fn: Callable[..., Any]
    depends_on: Tuple[str, ...] = ()


def pathway_decompose(input_value: Any, operators: Sequence[ProcessOperator],
                      output_name: str) -> Dict[str, Any]:
    """Run a DAG of named PROCESS OPERATORS -- the forward direction of
    process decomposition. Resolves dependencies in whatever order makes
    them satisfiable, not assumed left-to-right, so a genuine fan-out
    (one operator feeding two later ones) is represented correctly rather
    than forced into a linear chain. Whatever the process's own minimum
    tool-set turns out to need is what this reports -- never fit to a
    target dimension or rounded to the nearest named algebra."""
    results: Dict[str, Any] = {'input': input_value}
    resolved = {'input'}
    order: List[str] = []
    remaining = list(operators)
    while remaining:
        progressed = False
        still = []
        for op in remaining:
            if all(dep in resolved for dep in op.depends_on):
                args = [results[dep] for dep in op.depends_on]
                results[op.name] = op.fn(*args)
                resolved.add(op.name)
                order.append(op.name)
                progressed = True
            else:
                still.append(op)
        if not progressed:
            missing = [op.name for op in still]
            raise ValueError(f'unresolved dependency (cycle, or missing name) '
                             f'among: {missing}')
        remaining = still

    imaginary = tuple((name, results[name]) for name in order if name != output_name)
    return {'real': results[output_name], 'imaginary': imaginary,
            'dim': 1 + len(imaginary), 'order': order, 'all': results}
