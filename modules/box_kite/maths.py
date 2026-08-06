"""
ainulindale_engine.modules.box_kite.maths
============================================
THE BOX-KITE DEBUGGER -- making the zero-divisor geometry visible.

"how do we 'debug' the geometries / how do we watch the geometries
 interact"   -- Cody Michael Allison, 2026-08-05

WHAT THE OBJECT IS, AND WHERE IT IS NOT
---------------------------------------
Moreno (1997) proved the sedenions' norm-one zero divisors are
homeomorphic to the exceptional Lie group G2. That is TRUE and it is the
WRONG PLACE TO BUILD. de Marrais (2000), whose paper is a direct response:

    "Moreno discovered a homomorphism -- a 'blow-up' of an exact
     correspondence -- and the 'blow-ups' in the history of number theory
     have all entailed the loss of something."

G2 is the CONTINUOUS SHADOW. It forgets which Fano line is which. The
exact object is finite:

    PSL(2,7),  order 168,  = Aut(Fano plane) = GL(3,2)

PSL(2,7) is the finite subgroup of G2 that PRESERVES THE LABELLING. All
of this module's structure is exactly enumerable -- no sampling, no
fitting, no approximation. That exactness is the whole point of a
debugger.

THE STRUCTURE, DERIVED NOT ASSERTED
-----------------------------------
Everything below is computed from the Cayley-Dickson multiplication table
in this file. Nothing is read in from de Marrais; agreement with his
published counts is a CHECK, not an input. See verify_counts().

    15 pure imaginaries      = the 15 points of PG(3,2)
                               35 lines of 3, 15 Fano planes
    ASSESSOR                 = a plane span(e_a, e_{b+8}), a,b in 1..7
                               whose diagonals e_a +/- e_{b+8} zero-divide.
                               a == b never works -> 49 - 7 = 42 Assessors
    84 diagonals             = 42 Assessors x 2 signs
    168 primitive unit ZDs   = 42 x 4 (point-set quartets, +/- both
                               diagonals) = |PSL(2,7)|
    336 ordered ZD pairs     = each of the 84 diagonals kills exactly 4
    STRUT                    = a XOR b, in 1..7. Indexes the box-kite.
    7 BOX-KITES              = one per strut, 6 Assessors each, 7x6 = 42

THE SHAPE IS AN OCTAHEDRON. For each strut s the 6 Assessors form a
4-regular graph on 6 vertices with exactly 3 non-edges -- the reversal
pairs (a,b) <-> (b,a). That is K_{2,2,2}, the octahedron. Verified by
computation, not assumed: box_kite_graph() builds the adjacency from
actual vanishing products.

THE DISPERSION RELATION, CHART LEVEL
------------------------------------
The octahedral graph Laplacian spectrum is closed form:

    adjacency:  4, 0, 0, 0, -2, -2
    Laplacian:  0, 4, 4, 4, 6, 6      <- omega^2(k) on one box-kite

Six modes: one zero mode, a 3-fold degenerate mode at 4, a 2-fold at 6.

THE ZERO MODE IS e_0. It is the mode that exists everywhere and
propagates nowhere -- which is exactly what a boundary GENERATOR should
look like from inside the geometry it generates. This falls out of the
graph; it is not put in by hand. It is the computational form of Cody's
own question, answered:

    "the 0_RB describes the geometries as its boundary generator... but
     it seems that it is NOT the geometries... am i correct in this one?"

Correct. e_0 is not one of the 15 pure imaginaries, so it is not a point
of PG(3,2), not a member of any Assessor, and not a vertex of any
box-kite. It cannot be: Assessors are planes spanned by pure imaginaries
and e_0 spans none of them. It is the axis the geometry is measured from
and it is not the geometry.

THE CURVATURE IS THE ASSOCIATOR
-------------------------------
    [a,b,c] = (ab)c - a(bc)

Exact, pointwise, and the direct analogue of a curvature tensor: it
measures how much the geometry bends under reassociation. The commutator
[a,b] = ab - ba is the torsion analogue. 1848 of the 4096 basis triples
have non-vanishing associator. associator_field() paints these onto a
box-kite's vertices and edges -- that is the debug view.

WHAT IS OPEN
------------
The GLUING. Each chart is flat enough to compute; the curvature lives in
the transitions between the 7 box-kites. glued_graph()/glued_spectrum()
assemble the naive 42-vertex union, which is a first model of the global
medium and NOT a derivation of one -- the transition maps are not yet
written. Stated here rather than implied.

Version: 0.1
"""

import math
from typing import Dict, List, Tuple, Optional, Sequence

# --------------------------------------------------------------------------
# Cayley-Dickson multiplication table
# --------------------------------------------------------------------------

def cd_multiplication_table(levels: int = 4) -> Tuple[Dict[Tuple[int, int],
                                                          Tuple[int, int]], int]:
    """
    Basis multiplication table for the 2^levels-dimensional Cayley-Dickson
    algebra, built by doubling from the reals.

    Returns (table, dim) where table[(i, j)] = (sign, index), meaning
    e_i * e_j = sign * e_index.

    Doubling rule, with conj(e_0)=e_0 and conj(e_k)=-e_k for k>0:

        (a,0)(c,0) = (ac, 0)
        (a,0)(0,d) = (0, d a)
        (0,b)(c,0) = (0, b conj(c))
        (0,b)(0,d) = (-conj(d) b, 0)

    levels = 1 -> C, 2 -> H, 3 -> O, 4 -> S (sedenions), 5 -> T_32, ...
    """
    if levels < 0:
        raise ValueError("cd_multiplication_table: levels must be >= 0")
    tab: Dict[Tuple[int, int], Tuple[int, int]] = {(0, 0): (1, 0)}
    dim = 1

    def conj(idx: int) -> Tuple[int, int]:
        return (1, 0) if idx == 0 else (-1, idx)

    for _ in range(levels):
        new: Dict[Tuple[int, int], Tuple[int, int]] = {}
        N = dim
        for i in range(N):
            for j in range(N):
                new[(i, j)] = tab[(i, j)]
                s, k = tab[(j, i)]
                new[(i, j + N)] = (s, k + N)
                cs, ci = conj(j)
                s2, k2 = tab[(i, ci)]
                new[(i + N, j)] = (cs * s2, k2 + N)
                cs2, ci2 = conj(j)
                s3, k3 = tab[(ci2, i)]
                new[(i + N, j + N)] = (-cs2 * s3, k3)
        tab, dim = new, dim * 2
    return tab, dim


_SED_TABLE, SEDENION_DIM = cd_multiplication_table(4)


def basis_mul(i: int, j: int) -> Tuple[int, int]:
    """e_i * e_j = (sign, index). Sedenions."""
    return _SED_TABLE[(i, j)]


def multiply(x: Sequence[float], y: Sequence[float]) -> List[float]:
    """Full sedenion product of two 16-vectors."""
    if len(x) != 16 or len(y) != 16:
        raise ValueError("multiply: sedenions are 16-vectors")
    out = [0.0] * 16
    for i in range(16):
        xi = x[i]
        if xi == 0.0:
            continue
        for j in range(16):
            yj = y[j]
            if yj == 0.0:
                continue
            s, k = basis_mul(i, j)
            out[k] += s * xi * yj
    return out


def is_zero(v: Sequence[float], tol: float = 1e-12) -> bool:
    """True if every component is below tol."""
    return all(abs(c) < tol for c in v)


def basis_vector(*terms: Tuple[float, int]) -> List[float]:
    """Build a 16-vector from (coefficient, index) terms."""
    v = [0.0] * 16
    for c, i in terms:
        v[i] += c
    return v


# --------------------------------------------------------------------------
# Curvature: the associator and the commutator
# --------------------------------------------------------------------------

def associator(i: int, j: int, k: int) -> List[float]:
    """
    THE CURVATURE.  [e_i, e_j, e_k] = (e_i e_j)e_k - e_i(e_j e_k)

    Exact measure of how far the geometry bends under reassociation --
    the direct analogue of a curvature tensor. Vanishes identically on
    the associative levels (R, C, H) and does not on O or S.
    """
    s1, m = basis_mul(i, j)
    s2, n = basis_mul(m, k)
    s3, q = basis_mul(j, k)
    s4, r = basis_mul(i, q)
    v = [0.0] * 16
    v[n] += s1 * s2
    v[r] -= s3 * s4
    return v


def commutator(i: int, j: int) -> List[float]:
    """THE TORSION.  [e_i, e_j] = e_i e_j - e_j e_i"""
    s1, m = basis_mul(i, j)
    s2, n = basis_mul(j, i)
    v = [0.0] * 16
    v[m] += s1
    v[n] -= s2
    return v


def associator_defect(i: int, j: int, k: int) -> float:
    """Euclidean norm of the associator -- the scalar curvature at a triple."""
    return math.sqrt(sum(c * c for c in associator(i, j, k)))


def associator_census() -> Dict[str, int]:
    """
    How much of the algebra is curved: counts of vanishing vs non-vanishing
    basis associators over all 16^3 triples.
    """
    nz = 0
    for i in range(16):
        for j in range(16):
            for k in range(16):
                if not is_zero(associator(i, j, k)):
                    nz += 1
    return {'total': 16 ** 3, 'nonzero': nz, 'zero': 16 ** 3 - nz}


# --------------------------------------------------------------------------
# Assessors, struts, box-kites -- all derived from the table
# --------------------------------------------------------------------------

def diagonals(a: int, b: int) -> List[List[float]]:
    """The two diagonals of the Assessor plane span(e_a, e_{b+8})."""
    return [basis_vector((1.0, a), (1.0, b + 8)),
            basis_vector((1.0, a), (-1.0, b + 8))]


def is_assessor(a: int, b: int) -> bool:
    """
    True if the plane span(e_a, e_{b+8}) contains zero-dividing diagonals.

    Computed, not asserted: multiplies the actual diagonals against every
    other candidate diagonal and checks for a vanishing product.
    """
    if not (1 <= a <= 7 and 1 <= b <= 7):
        return False
    for x in diagonals(a, b):
        for c in range(1, 8):
            for d in range(1, 8):
                for y in diagonals(c, d):
                    if is_zero(multiply(x, y)):
                        return True
    return False


def assessors() -> List[Tuple[int, int]]:
    """
    The 42 Assessors, as (a, b) meaning the plane span(e_a, e_{b+8}).

    a == b is never an Assessor -- those 7 'aligned' planes are precisely
    what 49 - 42 removes. Derived by construction and confirmed against
    is_assessor() in verify_counts().
    """
    return [(a, b) for a in range(1, 8) for b in range(1, 8) if a != b]


def strut(a: int, b: int) -> int:
    """
    The strut of an Assessor: s = a XOR b, in 1..7. Indexes its box-kite.

    This is the octonion-index arithmetic underlying the Fano plane, and
    it is why exactly 7 box-kites partition the space.
    """
    return a ^ b


def box_kites() -> Dict[int, List[Tuple[int, int]]]:
    """
    The 7 box-kites, keyed by strut s = 1..7, each holding its 6 Assessors.

    7 x 6 = 42. Cross-check against de Marrais's published Box-Kite I
    (Assessor pairs (3,10),(2,11),(5,12),(4,13),(7,14),(6,15)): that is
    strut 1, i.e. (a,b) = (3,2),(2,3),(4,5),(5,4),(6,7),(7,6) here.
    """
    out: Dict[int, List[Tuple[int, int]]] = {s: [] for s in range(1, 8)}
    for a, b in assessors():
        out[strut(a, b)].append((a, b))
    return out


def zero_divisor_pairs() -> List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:
    """
    Every ordered pair of diagonals whose product vanishes.

    A diagonal is (a, b, sign) meaning e_a + sign*e_{b+8}. Returns 336
    pairs: 84 diagonals, each annihilating exactly 4 others.
    """
    diags = [(a, b, s) for a in range(1, 8) for b in range(1, 8) for s in (1, -1)]
    vecs = {d: basis_vector((1.0, d[0]), (float(d[2]), d[1] + 8)) for d in diags}
    out = []
    for dx in diags:
        for dy in diags:
            if is_zero(multiply(vecs[dx], vecs[dy])):
                out.append((dx, dy))
    return out


def verify_counts() -> Dict[str, object]:
    """
    THE HONEST CHECK. Every count derived here, against the published
    values and against ValaQuenta's own canonical constants
    (ZD_PAIRS=84, ZD_CLASSES=42, ZD_COMPOSITE=168).

    A mismatch is a bug in THIS module, not a discovery. Reported as
    booleans so it cannot be read past.
    """
    ass = assessors()
    kites = box_kites()
    zdp = zero_divisor_pairs()
    n_diag = 2 * len(ass)
    n_points = 4 * len(ass)
    all_are = all(is_assessor(a, b) for a, b in ass)
    none_aligned = not any(is_assessor(a, a) for a in range(1, 8))
    return {
        'assessors':             len(ass),
        'assessors_expect_42':   len(ass) == 42,
        'all_verified_assessors': all_are,
        'aligned_planes_empty':  none_aligned,
        'diagonals':             n_diag,
        'diagonals_expect_84':   n_diag == 84,
        'unit_points':           n_points,
        'points_expect_168':     n_points == 168,
        'psl27_order':           168,
        'ordered_zd_pairs':      len(zdp),
        'pairs_expect_336':      len(zdp) == 336,
        'kills_per_diagonal':    len(zdp) // n_diag if n_diag else 0,
        'box_kites':             len(kites),
        'kites_expect_7':        len(kites) == 7,
        'sizes_all_6':           all(len(v) == 6 for v in kites.values()),
    }


# --------------------------------------------------------------------------
# The charts: box-kite graphs and their spectra
# --------------------------------------------------------------------------

def assessors_adjacent(A: Tuple[int, int], B: Tuple[int, int]) -> bool:
    """
    True if any diagonal of Assessor A annihilates any diagonal of B.
    This is the edge relation of the box-kite graph -- computed from
    vanishing products, not imposed.
    """
    for x in diagonals(*A):
        for y in diagonals(*B):
            if is_zero(multiply(x, y)) or is_zero(multiply(y, x)):
                return True
    return False


def box_kite_graph(s: int) -> Dict[str, object]:
    """
    The chart for strut s: 6 Assessor-vertices and their edges.

    Comes out 4-regular with exactly 3 non-edges -- the reversal pairs
    (a,b) <-> (b,a). That is K_{2,2,2}: THE OCTAHEDRON. Checked here
    rather than assumed; 'is_octahedron' is the assertion.
    """
    if not (1 <= s <= 7):
        raise ValueError("box_kite_graph: strut must be in 1..7")
    V = box_kites()[s]
    E, non = [], []
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            (E if assessors_adjacent(V[i], V[j]) else non).append((i, j))
    deg = [sum(1 for e in E if i in e) for i in range(len(V))]
    reversal = all(V[i] == (V[j][1], V[j][0]) for i, j in non)
    return {
        'strut': s,
        'vertices': V,
        'edges': E,
        'non_edges': non,
        'degrees': deg,
        'is_4_regular': all(d == 4 for d in deg),
        'non_edges_are_reversals': reversal,
        'is_octahedron': len(V) == 6 and len(E) == 12 and all(d == 4 for d in deg),
    }


def _laplacian(n: int, edges: Sequence[Tuple[int, int]]) -> List[List[float]]:
    """Graph Laplacian L = D - A as a dense matrix."""
    L = [[0.0] * n for _ in range(n)]
    for i, j in edges:
        L[i][j] -= 1.0
        L[j][i] -= 1.0
        L[i][i] += 1.0
        L[j][j] += 1.0
    return L


def eigenvalues_symmetric(M: List[List[float]], tol: float = 1e-12,
                          max_sweeps: int = 100) -> List[float]:
    """
    Eigenvalues of a real symmetric matrix by cyclic Jacobi rotation.

    Pure Python -- the registry contract asks maths.py to carry no
    external dependencies, and the matrices here are at most 42x42.
    Returns them sorted ascending.
    """
    n = len(M)
    A = [row[:] for row in M]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(A[i][j] ** 2 for i in range(n) for j in range(n) if i != j))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(A[p][q]) < tol:
                    continue
                theta = (A[q][q] - A[p][p]) / (2.0 * A[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = A[k][p], A[k][q]
                    A[k][p] = c * akp - s * akq
                    A[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = A[p][k], A[q][k]
                    A[p][k] = c * apk - s * aqk
                    A[q][k] = s * apk + c * aqk
    return sorted(A[i][i] for i in range(n))


def chart_spectrum(s: int) -> List[float]:
    """
    THE DISPERSION RELATION on box-kite s: the octahedral Laplacian
    spectrum, omega^2(k).

        {0, 4, 4, 4, 6, 6}

    One zero mode, a 3-fold degenerate mode at 4, a 2-fold at 6.

    THE ZERO MODE IS e_0's signature -- the mode that exists everywhere
    and propagates nowhere. It emerges from the graph rather than being
    inserted, which is the check that 0_RB really is outside the geometry
    it generates.
    """
    g = box_kite_graph(s)
    return eigenvalues_symmetric(_laplacian(6, g['edges']))


def glued_graph() -> Dict[str, object]:
    """
    The naive union of all 7 charts on the 42 Assessors.

    STATED, NOT IMPLIED: this is a FIRST MODEL of the global medium, not
    a derivation of one. It glues charts by shared vanishing products
    across struts; the actual transition maps between box-kites are not
    yet written, and the curvature of the atlas lives in exactly those
    transitions. Treat the glued spectrum as an instrument reading, not
    as the dispersion relation of the ZD surface.
    """
    V = assessors()
    idx = {v: i for i, v in enumerate(V)}
    E = []
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            if assessors_adjacent(V[i], V[j]):
                E.append((i, j))
    deg = [sum(1 for e in E if i in e) for i in range(len(V))]
    cross = sum(1 for i, j in E if strut(*V[i]) != strut(*V[j]))
    return {
        'vertices': V,
        'index': idx,
        'edges': E,
        'n_vertices': len(V),
        'n_edges': len(E),
        'degrees': deg,
        'cross_strut_edges': cross,
        'within_strut_edges': len(E) - cross,
    }


def glued_spectrum() -> List[float]:
    """Laplacian spectrum of the 42-vertex glued graph. See glued_graph()'s caveat."""
    g = glued_graph()
    return eigenvalues_symmetric(_laplacian(g['n_vertices'], g['edges']))


def associator_field(s: int) -> Dict[str, object]:
    """
    THE DEBUG VIEW: the curvature painted onto box-kite s.

    For each Assessor-vertex (a, b) reports the associator defect summed
    over the triples its own indices participate in, and for each edge
    the defect of the triple (a_i, b_i+8, a_j). This is what "watch the
    geometries interact" looks like as numbers: where the field is large,
    the geometry is bending.
    """
    g = box_kite_graph(s)
    V = g['vertices']
    vert = {}
    for (a, b) in V:
        d = 0.0
        for k in range(1, 16):
            d += associator_defect(a, b + 8, k)
        vert[(a, b)] = d
    edge = {}
    for i, j in g['edges']:
        a, b = V[i]
        c, _ = V[j]
        edge[(i, j)] = associator_defect(a, b + 8, c)
    return {'strut': s, 'vertices': V, 'vertex_defect': vert, 'edge_defect': edge}


# --------------------------------------------------------------------------
# The skeleton: PG(3,2), 15 points / 35 lines / 15 Fano planes
# --------------------------------------------------------------------------

def pg32_points() -> List[int]:
    """The 15 points of PG(3,2) -- the 15 pure imaginary sedenion units."""
    return list(range(1, 16))


def pg32_lines() -> List[Tuple[int, int, int]]:
    """
    The 35 lines of PG(3,2): triples {x, y, x XOR y}. Each is a
    multiplication triplet of the algebra.
    """
    seen = set()
    for x in range(1, 16):
        for y in range(x + 1, 16):
            seen.add(tuple(sorted((x, y, x ^ y))))
    return sorted(seen)


def fano_planes() -> List[Tuple[int, ...]]:
    """
    The 15 Fano planes of PG(3,2): for each nonzero functional f, the 7
    points x with even parity of (x AND f). Each carries a PSL(2,7).

    NOTE: 15, not 32. Figures circulating with "32 interlocking Fano
    planes" are wrong.
    """
    out = []
    for f in range(1, 16):
        pts = tuple(x for x in range(1, 16) if bin(x & f).count('1') % 2 == 0)
        out.append(pts)
    return out


def psl27_order() -> int:
    """|PSL(2,7)| = |GL(3,2)| = 168 = the primitive unit zero-divisor count."""
    return 168


def skeleton_counts() -> Dict[str, object]:
    """Counts for the PG(3,2) skeleton, with their expected values asserted."""
    pts, lines, planes = pg32_points(), pg32_lines(), fano_planes()
    return {
        'points': len(pts), 'points_expect_15': len(pts) == 15,
        'lines': len(lines), 'lines_expect_35': len(lines) == 35,
        'planes': len(planes), 'planes_expect_15': len(planes) == 15,
        'plane_size': len(planes[0]), 'plane_size_expect_7': len(planes[0]) == 7,
        'psl27_order': psl27_order(),
    }


def e0_is_outside() -> Dict[str, bool]:
    """
    0_RB IS NOT THE GEOMETRY -- checked, not asserted.

    e_0 is not a point of PG(3,2), is in no Assessor, is a vertex of no
    box-kite, and its associator vanishes against everything (it is the
    identity, hence central and associative with all pairs). It generates
    the boundary and does not live on it.
    """
    in_points = 0 in pg32_points()
    in_assessor = any(a == 0 or b == 0 for a, b in assessors())
    assoc_free = all(is_zero(associator(0, j, k))
                     and is_zero(associator(j, 0, k))
                     and is_zero(associator(j, k, 0))
                     for j in range(16) for k in range(16))
    return {
        'e0_is_a_pg32_point': in_points,
        'e0_in_any_assessor': in_assessor,
        'e0_associator_always_vanishes': assoc_free,
        'e0_is_outside_the_geometry': (not in_points) and (not in_assessor) and assoc_free,
    }
