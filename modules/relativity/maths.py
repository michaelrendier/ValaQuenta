# SPDX-License-Identifier: GPL-3.0-only
r"""
ValaQuenta.modules.relativity.maths
===================================
EINSTEIN'S RELATIVITY, special and general, as FOUR SPACES, each with its own jurisdiction.  Not a field-content engine (compare
``lagrangian_sm``): relativity is a family of spaces, and what is a legal operation depends on which space you stand in.

    minkowski   flat spacetime (special relativity).  Global inertial frames exist; the Poincare group acts; vectors at different
                events may be added; energy and momentum are conserved globally.
    curved      a Lorentzian manifold (general relativity).  Only LOCAL inertial frames exist; vectors at different events cannot be
                added without a path (parallel transport); conservation is the covariant divergence; there is no global boost.
    tangent     the local Minkowski space at one event: where special relativity is legal inside general relativity (the equivalence
                principle).  Gamma can be set to zero at the event; the curvature cannot.
    metric      the space of metrics: where Einstein's equations live.  A point is a whole geometry g_{mu nu}(x); a motion is a
                diffeomorphism (a gauge orbit); the Einstein-Hilbert action is a functional on it, and the Einstein equations are its
                stationary points.

Every space is declared with the same eight fields as the ``spatial-simulation`` skill (points, axes, motions, invariant, views,
acceptance test, repo engine, status) plus its jurisdiction: the set of operations legal in it.  ``jurisdiction_check`` is the
set-membership test of ``bracketing_firing_order.jurisdiction_violation``, reused, not rewritten.

The functions live in four sibling files, one per space: ``minkowski.py``, ``curved.py``, ``tangent.py`` and ``metric.py``, with
``crossings.py`` for the places where one jurisdiction hands over to another (weak field, flat limit, Euclidean continuation) and
``bridge.py`` for the project's own readings (labelled INTERPRETATION).  Units: SI where numbers are compared with measurement,
geometric (G = c = 1) in the symbolic derivations.  No framework constant is used.
"""
from __future__ import annotations
from ..bracketing_firing_order import maths as _B

# measured inputs (SI), with sources
C = 299792458.0                                  # exact by definition of the metre
G = 6.67430e-11                                  # CODATA 2018
GM_SUN = 1.32712440018e20                        # IAU nominal, m^3 s^-2
GM_EARTH = 3.986004418e14                        # IAU/EGM2008
R_SUN = 6.957e8                                  # IAU nominal solar radius, m
R_EARTH = 6.371e6                                # mean, m
HBAR = 1.054571817e-34
K_B = 1.380649e-23                               # exact
ARCSEC = 206264.80624709636                      # arcseconds per radian

SPACES = {
    "minkowski": {
        "display": "Minkowski space (special relativity)",
        "points": "events (ct, x, y, z)", "axes": "R^4, one per coordinate, flat metric eta = diag(-1, 1, 1, 1)",
        "motions": "Poincare group: boosts, rotations, translations", "invariant": "s^2 = -(c dt)^2 + dx^2 + dy^2 + dz^2",
        "views": "spacetime diagram with 45-degree light cones; the observer's past cone; rapidity plane",
        "acceptance_test": "Lorentz-invariance residual |L^T eta L - eta| < 1e-12 for every composed boost",
        "repo": "ValaQuenta.modules.relativity.minkowski; skill spatial-simulation SS1 (assets/minkowski.py)", "status": "ESTABLISHED",
        "legal": {"global_boost", "global_rotation", "translation", "velocity_addition", "add_vectors_at_different_events",
                  "global_simultaneity_within_a_frame", "global_energy_momentum_conservation", "four_momentum_invariant_mass",
                  "interval_classification", "proper_time_along_worldline", "doppler_shift"},
        "illegal": {"gravitational_potential", "curvature", "tidal_tensor", "gravitational_redshift_between_static_observers",
                    "superluminal_signal"},
    },
    "curved": {
        "display": "Curved spacetime (general relativity)",
        "points": "events on a Lorentzian manifold with metric g(x)", "axes": "coordinates are labels, not distances; the metric turns them into distances",
        "motions": "diffeomorphisms (any smooth relabelling); geodesic flow; parallel transport", "invariant": "scalars: R, Kretschmann K = R_{abcd}R^{abcd}, proper time",
        "views": "embedding diagrams; Penrose-Carter conformal diagram; orbit plots in the equatorial plane; tidal ellipsoids",
        "acceptance_test": "Ricci = 0 for Schwarzschild; K = 48 M^2/r^6; Bianchi nabla_m G^{mn} = 0 for a generic FLRW",
        "repo": "ValaQuenta.modules.relativity.curved", "status": "ESTABLISHED",
        "legal": {"local_lorentz_frame", "geodesic", "parallel_transport", "covariant_conservation", "curvature_tensor", "tidal_tensor",
                  "coordinate_transformation", "proper_time_along_worldline", "gravitational_redshift_between_static_observers",
                  "interval_classification", "horizon_radius"},
        "illegal": {"add_vectors_at_different_events", "global_boost", "global_inertial_frame", "global_simultaneity",
                    "global_velocity_addition_of_distant_objects", "global_energy_momentum_conservation", "global_lorentz_invariance",
                    "translation"},
    },
    "tangent": {
        "display": "The tangent space at an event (the equivalence principle)",
        "points": "vectors at one event p", "axes": "R^4 with eta; normal coordinates make g = eta + O(x^2) at p",
        "motions": "Lorentz group at p", "invariant": "eta at p; the curvature tensor R(p) is the first thing that cannot be removed",
        "views": "the local light cone; the tidal ellipsoid built from R(p)",
        "acceptance_test": "Gamma(p) -> 0 in suitable coordinates while Kretschmann(p) is unchanged",
        "repo": "ValaQuenta.modules.relativity.tangent", "status": "ESTABLISHED",
        "legal": {"local_lorentz_frame", "global_boost", "velocity_addition", "four_momentum_invariant_mass", "interval_classification",
                  "doppler_shift", "add_vectors_at_different_events"},
        "illegal": {"curvature_removal", "tidal_tensor_removal", "global_inertial_frame", "measure_beyond_second_order_in_distance"},
    },
    "metric": {
        "display": "The space of metrics (where Einstein's equations live)",
        "points": "a whole geometry g_{mu nu}(x) on a fixed manifold", "axes": "each metric component is a field over spacetime (ten fields; four are gauge)",
        "motions": "diffeomorphisms (gauge orbits); variations delta g; the lapse N is a Lagrange multiplier", "invariant": "the Einstein-Hilbert action S[g] on a gauge orbit",
        "views": "minisuperspace slices (a, N); the linearised h_{mu nu} modulo gauge; ADM constraint surfaces",
        "acceptance_test": "the lapse variation of the FLRW action gives the first Friedmann equation; linearised Riemann is gauge invariant",
        "repo": "ValaQuenta.modules.relativity.metric", "status": "ESTABLISHED",
        "legal": {"vary_action", "diffeo_gauge_orbit", "linearise_about_background", "constraint_from_lapse", "minisuperspace_reduction",
                  "covariant_conservation"},
        "illegal": {"evolve_in_absolute_time", "fixed_background_assumption", "global_energy_momentum_conservation", "unique_coordinate_description"},
    },
}


def jurisdiction_map():
    """{space: set of legal operations}, in the form ``bracketing_firing_order.jurisdiction_violation`` takes."""
    return {k: set(v["legal"]) for k, v in SPACES.items()}


def jurisdiction_check(space: str, operation: str):
    """Is ``operation`` legal in ``space``?  The set-membership test of bracketing_firing_order.jurisdiction_violation, plus a
    flag when the space itself names the operation as explicitly illegal (not merely absent).

    :param space: one of the four spaces
    :param operation: the operation to test
    :returns: the verdict dict of jurisdiction_violation plus declared_illegal
    """
    r = _B.jurisdiction_violation(space, operation, jurisdiction_map())
    r["declared_illegal"] = bool(space in SPACES and operation in SPACES[space]["illegal"])
    return r


def crossing_table():
    """For every operation named anywhere: where it is legal and where illegal.  An operation legal in one space and illegal in another is
    a crossing: a place where using one jurisdiction's language in another is the error."""
    ops = set()
    for v in SPACES.values(): ops |= v["legal"] | v["illegal"]
    out = {}
    for op in sorted(ops):
        legal = [k for k, v in SPACES.items() if op in v["legal"]]; illegal = [k for k, v in SPACES.items() if op in v["illegal"]]
        out[op] = {"legal_in": legal, "illegal_in": illegal, "crossing": bool(legal and illegal)}
    return out
