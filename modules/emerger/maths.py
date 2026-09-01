"""
ainulindale_engine.modules.emerger.maths
==========================================
THE EMERGER -- Sedenion Bracketing & Firing Order.

    "the grouping of what sedenion operators creates what different domains
     ... which by need give the emergence a priority in a particular order"
                                    -- Cody Michael Allison, 2026-09-01

A dynamic permutative bracketer. It works only in the COMPLEX/imaginary
domain -- the real component e_0 is the tilt to the i axis: it is never
bracketed, it is the fixed anchor that every group is paired against so
the relationship between a bracket and the real reference stays visible.

Given a 2^k Cayley-Dickson algebra, a BRACKETING is an ordered partition
of the imaginary basis indices {1 .. dim-1} into named groups. Each group
G, paired with the anchor e_0, spans a sub-domain span({e_0} u G):
    |G| = 1, closed        -> C   (complex)
    |G| = 3, closed        -> H   (quaternion)
    |G| = 7, closed        -> O   (octonion)
    otherwise              -> FRAGMENT (a linear subspace, not a subalgebra;
                                        where zero divisors live)

The ORDER in which the groups are approached is the FIRING ORDER. It is
load-bearing: each bracket is conditioned on the ones fired before it
(conj/norm from {1:15} must exist before {2:14} can read a ladder
position, etc.). The firing order can be:
    canonical  -- the dependency order
    sigma_rb   -- sigma_RB's tilt-phase rotates the entry point into the
                  12-step precession (4 d* faces : 3 Lambert-W faces)
    explicit   -- any user permutation (legality is reported, not enforced)

The Emerger is the ascent-dual of Generational Lineage (SFR / lineage.py):
lineage tracks descent (what built this; differentiate down; writing);
the Emerger runs ascent (what emerges, in what order; integrate up;
reading).

Pure Python 3.  Fraction arithmetic throughout; float only at the output
boundary.  Every quantity here is CALCULATED and exactly reproducible.

Cross-references (this engine sits among):
    modules/box_kite       -- the exact PSL(2,7) ZD geometry (NOT G_2;
                              G_2 is the continuous blow-up that forgets
                              the labelling)
    modules/angular_rank   -- the 16D oscilloscope; {4,8,4} as a CHECK
    modules/archimedes_screw -- Ordinal / Zeta-Index / Digits / Spaces as
                              four coordinates on u = ln x; delta = 1/2 ln(q/p)
    modules/scale          -- decompositional analysis; RSA CRT as control
    TuringStack/the_emerger.py -- the first-pass numpy prototype
    TuringStack/wiki/ZD-locus-equatorial-geodesic-2026-09-01.md
"""
from __future__ import annotations

from fractions import Fraction as F
from typing import Dict, List, Tuple, Sequence, FrozenSet

SEDENION_DIM = 16
REAL_ANCHOR = 0                       # e_0 -- never bracketed; the tilt to i

Vec = Tuple[F, ...]


# ======================================================================
#  Cayley-Dickson algebra  (exact, over Fraction)
# ======================================================================

def zero_vec(dim: int = SEDENION_DIM) -> Vec:
    return tuple(F(0) for _ in range(dim))


def basis(k: int, dim: int = SEDENION_DIM) -> Vec:
    v = [F(0)] * dim
    v[k] = F(1)
    return tuple(v)


def cd_conj(x: Sequence[F]) -> Vec:
    return (x[0],) + tuple(-c for c in x[1:])


def cd_mul(a: Sequence[F], b: Sequence[F]) -> Vec:
    n = len(a)
    if n == 1:
        return (a[0] * b[0],)
    h = n // 2
    a1, a2 = a[:h], a[h:]
    b1, b2 = b[:h], b[h:]
    c1 = _sub(cd_mul(a1, b1), cd_mul(cd_conj(b2), a2))
    c2 = _add(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))
    return c1 + c2


def _add(u, v): return tuple(x + y for x, y in zip(u, v))
def _sub(u, v): return tuple(x - y for x, y in zip(u, v))


def coerce_vec(v, dim: int = SEDENION_DIM) -> Vec:
    """Accept a length-dim sequence of numbers, or a name like 'e1+e10',
    'e0', '2*e3-e11', '1.5+e2'.  Returns a tuple of Fraction."""
    if isinstance(v, str):
        acc = [F(0)] * dim
        for tok in v.replace(" ", "").replace("-", "+-").split("+"):
            if not tok:
                continue
            sign = F(-1) if tok.startswith("-") else F(1)
            tok = tok.lstrip("-")
            if "*e" in tok:
                coef, idx = tok.split("*e")
                acc[int(idx)] += sign * F(coef)
            elif tok.startswith("e"):
                acc[int(tok[1:])] += sign
            else:
                acc[0] += sign * F(tok)
        return tuple(acc)
    return tuple(F(c) for c in v)


def norm_sq(x: Sequence[F]) -> F:
    return sum((c * c for c in x), F(0))


def left_matrix(a: Sequence[F]) -> List[List[F]]:
    """L_a with  L_a . x == cd_mul(a, x).  Columns = a * e_k."""
    dim = len(a)
    cols = [cd_mul(a, basis(k, dim)) for k in range(dim)]
    return [[cols[k][r] for k in range(dim)] for r in range(dim)]


def mat_rank(M: List[List[F]]) -> int:
    """Exact rank by Gaussian elimination over Fraction."""
    M = [row[:] for row in M]
    rows, cols = len(M), len(M[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c]
        M[r] = [v / inv for v in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == rows:
            break
    return r


def is_zero_divisor(x: Sequence[F]) -> bool:
    """x != 0 has a partner y != 0 with x*y = 0  <=>  L_x is rank-deficient."""
    if all(c == 0 for c in x):
        return False
    return mat_rank(left_matrix(x)) < len(x)


# ======================================================================
#  The ZD equator  (see TuringStack ZD-locus note; box_kite for the exact
#  PSL(2,7) enumeration)
# ======================================================================

def on_zd_equator(x: Sequence[F]) -> bool:
    """
    Purely imaginary AND norm-balanced across the CD-double boundary:
        Re(a) = Re(b) = 0 ,  |a| = |b| ,  a,b != 0
    where x = (a, b), a = first half, b = second half.  This is the fixed
    set of the J_red <-> J_blue hemisphere swap -- the balance equator the
    zero divisors sit on.  (Sufficient for the basis assessor pairs; the
    exact locus is box_kite's 42 assessors -- G_2 is the blow-up.)
    """
    h = len(x) // 2
    a, b = x[:h], x[h:]
    na, nb = norm_sq(a), norm_sq(b)
    return (a[0] == 0 and b[0] == 0 and na == nb and na != 0)


# ======================================================================
#  sigma_RB  --  tilt (Scale) and axis (Flow)
# ======================================================================

def sigma_rb(x: Sequence[F]) -> Dict[str, object]:
    """
    psi[k] = x[k] + i x[(k+8) mod 16].
    s[k]   = psi[k] * conj(psi[k XOR 4])
        tilt[k] = Re s[k] = x[k] x[k^4]  +  x[k+8] x[(k^4)+8]
        axis[k] = Im s[k] = x[k+8] x[k^4]  -  x[k] x[(k^4)+8]
    T1 (Oblique-Gear): s[k^4] = conj s[k]  =>  Sigma_axis = 0 identically.
    tilt = Perfect Perturbation (Scale);  axis = Perfect Turbulent Flow.
    Sigma_tilt = 0  <=>  sigma = 1/2.
    """
    dim = len(x)

    def g(i):  # x[(i+8) mod dim]
        return x[(i + 8) % dim]

    tilt, axis = [], []
    for k in range(dim):
        m = k ^ 4
        tilt.append(x[k] * x[m] + g(k) * g(m))
        axis.append(g(k) * x[m] - x[k] * g(m))
    st = sum(tilt, F(0))
    sa = sum(axis, F(0))
    t1 = all(tilt[k] == tilt[k ^ 4] and axis[k] == -axis[k ^ 4] for k in range(dim))
    return {
        "tilt": tuple(tilt), "axis": tuple(axis),
        "Sigma_tilt": st, "Sigma_axis": sa,
        "sigma_is_half": st == 0,
        "T1_holds": t1,
    }


def firing_phase(sigma_tilt: F) -> Tuple[int, int]:
    """
    Rational squash of Sigma_tilt into the 12-step precession, then mod 5
    (gcd(12,5)=1 so the 12-phase clock cycles all five brackets).
        s = St / (1 + |St|)  in (-1, 1) ;  u = (s+1)/2 in (0,1)
        step12 = floor(12 u) ;  entry bracket = step12 mod 5
    """
    a = sigma_tilt if sigma_tilt >= 0 else -sigma_tilt
    s = sigma_tilt / (1 + a)
    u = (s + 1) / 2
    step12 = int(u * 12)
    step12 = 0 if step12 < 0 else (11 if step12 > 11 else step12)
    return step12, step12 % 5


# ======================================================================
#  Bracketings
# ======================================================================

def _grp(*idx) -> FrozenSet[int]:
    return frozenset(idx)


# The five canonical brackets of R^16 = S.  Order here IS the dependency
# (canonical firing) order.
STANDARD_BRACKETINGS: Dict[str, Tuple[FrozenSet[int], ...]] = {
    "{1:15}":     (_grp(*range(1, 16)),),
    "{2:14}":     (_grp(8), _grp(*[i for i in range(1, 16) if i != 8])),
    "{8:8}":      (_grp(1, 2, 3, 4, 5, 6, 7), _grp(8, 9, 10, 11, 12, 13, 14, 15)),
    "{4:4:4:4}":  (_grp(1, 2, 3), _grp(4, 5, 6, 7),
                   _grp(8, 9, 10, 11), _grp(12, 13, 14, 15)),
    "{4:8:4}":    (_grp(4, 5, 6, 7),                       # gain 0  (annihilator)
                   _grp(1, 2, 3, 8, 9, 10, 11),            # gain 1  (unit / NOW)
                   _grp(12, 13, 14, 15)),                  # gain sqrt2 (amplifier)
}

CANONICAL_ORDER = ["{1:15}", "{2:14}", "{8:8}", "{4:4:4:4}", "{4:8:4}"]

# what each bracket lets emerge, and what it descends from (lineage sec.9)
BRACKET_ROLE = {
    "{1:15}":    ("DERIVED",     "the CD grading",
                  "Re, N=|x|^2, conj, inverse -- grades the algebra"),
    "{2:14}":    ("THEORETICAL", "{1:15} (needs Re)",
                  "the pointer z = x0 + i x8; |z|; |z| - Omega_ZS -- read head"),
    "{8:8}":     ("DERIVED",     "{1:15} (needs conj/norm)",
                  "|a|-|b| (dist. from ZD equator); sheet; J_2 (L vs R)"),
    "{4:4:4:4}": ("DERIVED",     "{8:8} (refines the halves)",
                  "four SU(2) phases; sigma_RB tilt/axis; Sigma_tilt = net work"),
    "{4:8:4}":   ("THEORETICAL", "{1:15} + {4:4:4:4} (needs norms and the gain split)",
                  "dominant gain class 0/1/sqrt2 -- multiplicative role"),
}


def domain_of(group: FrozenSet[int], dim: int = SEDENION_DIM) -> str:
    """Classify span({e_0} u group): C / H / O / FRAGMENT (by closure)."""
    idx = sorted(group)
    n = len(idx)
    if n == 0:
        return "R"
    full = [0] + idx
    sset = set(full)
    # closed (up to sign) under products of its own generators?
    for i in full:
        for j in full:
            p = cd_mul(basis(i, dim), basis(j, dim))
            support = [k for k, c in enumerate(p) if c != 0]
            if len(support) != 1 or support[0] not in sset:
                closed = False
                break
        else:
            continue
        closed = False
        break
    else:
        closed = True
    if closed:
        return {1: "C", 3: "H", 7: "O"}.get(n, f"closed({n})")
    return "FRAGMENT"


GAIN_LABEL = {0: "annihilator (gain 0)", 1: "unit (gain 1, NOW)",
              2: "amplifier (gain sqrt2)"}


def gain_class(x: Sequence[F]) -> str:
    """Dominant {4:8:4} block by norm.  G0={4..7}, G1={1,2,3,8..11}, Gr2={12..15}."""
    g0 = sum((x[i] * x[i] for i in (4, 5, 6, 7)), F(0))
    g1 = sum((x[i] * x[i] for i in (1, 2, 3, 8, 9, 10, 11)), F(0))
    g2 = sum((x[i] * x[i] for i in (12, 13, 14, 15)), F(0))
    m = max(((g0, 0), (g1, 1), (g2, 2)))
    return GAIN_LABEL[m[1]]


# ======================================================================
#  Firing order
# ======================================================================

def legal_orders() -> List[List[str]]:
    """
    Dependency-respecting permutations of the five canonical brackets.
    Constraints:
        {1:15} before {2:14}, {8:8}, {4:8:4}
        {8:8}  before {4:4:4:4}
        {4:4:4:4} before {4:8:4}
    """
    from itertools import permutations
    dep = {
        "{2:14}": {"{1:15}"},
        "{8:8}": {"{1:15}"},
        "{4:4:4:4}": {"{1:15}", "{8:8}"},
        "{4:8:4}": {"{1:15}", "{4:4:4:4}"},
    }
    out = []
    for p in permutations(CANONICAL_ORDER):
        pos = {name: i for i, name in enumerate(p)}
        if all(pos[b] > max(pos[d] for d in ds) for b, ds in dep.items()):
            out.append(list(p))
    return out


def firing_order(x: Sequence[F], mode: str = "sigma_rb") -> Dict[str, object]:
    x = coerce_vec(x)
    sig = sigma_rb(x)
    step12, entry = firing_phase(sig["Sigma_tilt"])
    canonical = CANONICAL_ORDER[:]
    phased = [CANONICAL_ORDER[(entry + i) % 5] for i in range(5)]
    order = phased if mode == "sigma_rb" else canonical
    return {
        "Sigma_tilt": float(sig["Sigma_tilt"]),
        "precession_step_of_12": step12,
        "entry_bracket_index": entry,
        "canonical": canonical,
        "sigma_rb_phased": phased,
        "order": order,
        "phased_is_legal": phased in legal_orders(),
    }


# ======================================================================
#  Emergence  --  the spectroscopy readout
# ======================================================================

def emerge(x: Sequence[F], mode: str = "sigma_rb") -> Dict[str, object]:
    """
    Run x through the five brackets in firing order.  For each bracket:
    its groups, each group's domain type, ZD-equator membership, gain
    class, and the emergent scalar -- conditioned on the brackets fired
    before it.
    """
    x = coerce_vec(x)
    fo = firing_order(x, mode=mode)
    sig = sigma_rb(x)
    steps = []
    fired: List[str] = []
    for name in fo["order"]:
        groups = STANDARD_BRACKETINGS[name]
        tier, descends, emerges = BRACKET_ROLE[name]
        gdata = []
        for g in groups:
            gvec = tuple(x[i] if i in g or i == 0 else F(0) for i in range(len(x)))
            gdata.append({
                "indices": sorted(g),
                "domain": domain_of(g),
                "|group|": float(norm_sq(gvec) ** F(1, 1)) ** 0.5,
            })
        step = {
            "bracket": name,
            "tier": tier,
            "descends_from": descends,
            "emerges": emerges,
            "conditioned_on": fired[:],
            "groups": gdata,
        }
        # bracket-specific scalars
        if name == "{1:15}":
            step["Re"] = float(x[0])
            step["N"] = float(norm_sq(x))
            step["is_unit"] = norm_sq(x) == 1
        elif name == "{2:14}":
            re_z, im_z = float(x[0]), float(x[8])
            step["pointer_z"] = (re_z, im_z)
            step["|z|"] = (re_z * re_z + im_z * im_z) ** 0.5
            step["|z|_minus_Omega_ZS"] = step["|z|"] - 0.5671432904097838
        elif name == "{8:8}":
            h = len(x) // 2
            na = float(norm_sq(x[:h])) ** 0.5
            nb = float(norm_sq(x[h:])) ** 0.5
            step["balance_|a|-|b|"] = na - nb
            step["on_zd_equator"] = on_zd_equator(x)
            step["is_zero_divisor"] = is_zero_divisor(x)
        elif name == "{4:4:4:4}":
            step["Sigma_tilt"] = float(sig["Sigma_tilt"])
            step["Sigma_axis"] = float(sig["Sigma_axis"])
            step["sigma_is_half"] = sig["sigma_is_half"]
            step["T1_holds"] = sig["T1_holds"]
        elif name == "{4:8:4}":
            step["gain_class"] = gain_class(x)
        steps.append(step)
        fired.append(name)
    return {
        "input_norm": float(norm_sq(x)) ** 0.5,
        "firing_order": fo,
        "steps": steps,
    }


# ======================================================================
#  Cross-scale permutation  (C / H / O brackets in different orders)
# ======================================================================

def scale_partitions(dim: int = SEDENION_DIM) -> Dict[str, object]:
    """
    Enumerate the ways to partition the dim-1 imaginary indices into
    C-, H-, O-sized groups (1 / 3 / 7), and report how many partitions
    are all-subalgebra vs contain a FRAGMENT.  This is the "different
    brackets of different scales" space the permutative bracketer moves in.
    """
    imag = list(range(1, dim))
    m = len(imag)

    # integer compositions of m into parts from {1,3,7}
    def comps(target):
        if target == 0:
            yield []
            return
        for p in (7, 3, 1):
            if p <= target:
                for rest in comps(target - p):
                    yield [p] + rest

    shapes = set(tuple(sorted(c, reverse=True)) for c in comps(m))
    # for one representative contiguous partition per shape, classify groups
    rep = {}
    for shape in shapes:
        cur, gs = 0, []
        for size in shape:
            gs.append(frozenset(imag[cur:cur + size]))
            cur += size
        rep[shape] = [domain_of(g, dim) for g in gs]
    return {
        "imaginary_count": m,
        "part_sizes_allowed": [1, 3, 7],
        "distinct_shapes": sorted(shapes, reverse=True),
        "shape_domain_classes_contiguous_rep": {str(k): v for k, v in rep.items()},
        "note": "contiguous representative only; a fragment means that contiguous "
                "grouping is not a subalgebra -- other index choices of the same "
                "shape may or may not close.",
    }


# ======================================================================
#  Self-checks  &  lineage report
# ======================================================================

def verify() -> Dict[str, object]:
    e = lambda k: basis(k)
    e1_e10 = _add(e(1), e(10))
    e1_e2 = _add(e(1), e(2))
    checks = {
        "Sigma_axis == 0 for e1+e10": sigma_rb(e1_e10)["Sigma_axis"] == 0,
        "Sigma_axis == 0 for random-ish": sigma_rb(
            tuple(F(i * 3 % 7 - 3, 4) for i in range(16)))["Sigma_axis"] == 0,
        "T1 holds (e1+e10)": sigma_rb(e1_e10)["T1_holds"],
        "e1+e10 is a zero divisor": is_zero_divisor(e1_e10),
        "e1+e10 on the ZD equator": on_zd_equator(e1_e10),
        "e1+e2 is NOT a zero divisor": not is_zero_divisor(e1_e2),
        "e1+e2 NOT on the ZD equator": not on_zd_equator(e1_e2),
        "e0 is a unit (not ZD)": not is_zero_divisor(e(0)),
        "domain_of({1}) == C": domain_of(_grp(1)) == "C",
        "domain_of({1,2,3}) == H": domain_of(_grp(1, 2, 3)) == "H",
        "domain_of({1..7}) == O": domain_of(_grp(1, 2, 3, 4, 5, 6, 7)) == "O",
        "domain_of({1,5,9}) == FRAGMENT": domain_of(_grp(1, 5, 9)) == "FRAGMENT",
        "legal_orders nonempty": len(legal_orders()) > 0,
        "canonical order is legal": CANONICAL_ORDER in legal_orders(),
    }
    return {"all_pass": all(checks.values()), "checks": checks,
            "n_legal_firing_orders": len(legal_orders())}


def lineage_report() -> List[Dict[str, str]]:
    return [
        {"bracket": b, "tier": BRACKET_ROLE[b][0],
         "descends_from": BRACKET_ROLE[b][1], "emerges": BRACKET_ROLE[b][2]}
        for b in CANONICAL_ORDER
    ]
