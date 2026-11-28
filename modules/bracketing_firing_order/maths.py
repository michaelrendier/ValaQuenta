"""
ValaQuenta.modules.bracketing_firing_order.maths
====================================================
THE BRACKETING ENGINE, THE FIRING ORDER ENGINE, AND SET MEMBERSHIP --
three general-purpose tools, not one thing tied to `add_scale_sign`.

THREE TOOLS, KEPT SEPARATE ON PURPOSE:

1. BRACKETING -- "how many unordered ways can these n things be grouped?"

::

   Exact Bell-number count, always computable; exhaustive enumeration only
   when actually feasible (n small) -- an honest infeasibility report
   otherwise, never a silent truncation. `add_scale_sign`'s 3 generators:
   Bell(3)=5, fully enumerable. The sedenion's 16 components: Bell(16) is
   astronomically large -- count it exactly, do not attempt to list it.

2. FIRING ORDER -- "how many ways can these n things be SEQUENCED?" A

::

   permutation, not a partition -- n! orderings, and applying one is a
   literal permutation action on the written/reference sequence. Verified
   worked example: firing order (3,1,2) applied to [Scale,Sign,Add] gives
   [Add,Scale,Sign] -- the ASS engine's own canonical name, reached by
   resequencing, not by relabeling.

3. SET MEMBERSHIP -- serves BOTH tools, two distinct jobs:

   (a) has a firing occurred before? (trajectory/collision detection --
       generalizes ASSWord.trajectory()/.collisions()/.would_collide()
       from a single-repo extension into a domain-independent tool any
       sequence of callables can use, not just ASS elements)
   (b) did a bracketing cause one jurisdiction's maths to be used on an
       object that belongs to a DIFFERENT jurisdiction? -- new capability,
       grounded in GenerationalLineage/engine/lines.py's own already-named
       "two jurisdictions" (decomposition/descent vs emerger/ascent) --
       see jurisdiction_violation() below. Deliberately parametrized, not
       hardcoded to that repo's data (module-independence convention: this
       engine stays reusable, callers supply their own jurisdiction map).

4. PLANS -- the four orderings of brackets, run on a 16-component vector
   (added at version 0.2, ported from SedenionSpectralRelativity/firing_plan.py):

::

   A  bracketing                    grouping the written sequence, default orders
   B  firing order                  one flat bracket, any of the n! orders
   C  firing order of brackets      the written bracketing, an order at every bracket
   D  bracketing of firing orders   a firing order first, then a bracketing of the
                                    FIRED sequence (reaches groupings of items that
                                    were not adjacent in the written order)

   Every plan can be read two ways on 16-component vectors (exact Fractions):
   the OPERATOR reading composes left-multiplication matrices (associative, so only
   the firing order changes the output), the ELEMENT reading multiplies the
   sedenions themselves (not associative, so the bracketing changes it too).
   evolve_operator and evolve_value return every intermediate vector, so the
   input and the output can be watched side by side.

Version: 0.2 -- the plan layer; 0.1 -- first build.
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction as F
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

# ═══════════════════════════════════════════════════════════════════════
#  TOOL 1 — BRACKETING (unordered groupings — set partitions)
# ═══════════════════════════════════════════════════════════════════════

# Practical enumeration ceiling. Bell(12) ~ 4.2 million is already a lot to
# hold in memory; past this, count exactly but refuse to enumerate -- an
# honest infeasibility report, not a silent hang or truncation.
ENUMERATION_CEILING_N = 12


def bell_number(n: int) -> int:
    """
    Exact count of unordered partitions of n distinct things -- the
    Bell number B(n), via the Bell triangle (arbitrary precision, no
    approximation). B(0)=1, B(3)=5, B(16)=10480142147 (~1.05e10).

    :param n: number of distinct things
    :returns: B(n), exact
    :raises ValueError: n is negative
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    triangle = [[1]]
    for i in range(1, n + 1):
        row = [triangle[i - 1][-1]]
        for j in range(1, i + 1):
            row.append(row[j - 1] + triangle[i - 1][j - 1])
        triangle.append(row)
    return triangle[n][0]


def set_partitions(items: Sequence[Any]) -> List[List[List[Any]]]:
    """
    Every unordered partition of `items` into non-empty groups --
    exhaustive, exact. Refuses (raises) above ENUMERATION_CEILING_N rather
    than silently hanging on an astronomically large output; use
    bell_number() for the exact count regardless of n.

    :param items: the distinct things
    :returns: every unordered partition into non-empty groups
    :raises ValueError: len(items) exceeds ENUMERATION_CEILING_N
    """
    n = len(items)
    if n > ENUMERATION_CEILING_N:
        raise ValueError(
            f"set_partitions refuses n={n} > {ENUMERATION_CEILING_N} -- "
            f"Bell({n})={bell_number(n)} partitions is not a listable "
            f"quantity. Use bell_number({n}) for the exact count.")
    if n == 0:
        return [[]]
    first, rest = items[0], items[1:]
    out: List[List[List[Any]]] = []
    for smaller in set_partitions(rest):
        # insert `first` into each existing group, one at a time
        for i in range(len(smaller)):
            new_partition = [g[:] for g in smaller]
            new_partition[i] = [first] + new_partition[i]
            out.append(new_partition)
        # or `first` as its own new group
        out.append([[first]] + [g[:] for g in smaller])
    return out


def bracketing_report(items: Sequence[Any]) -> Dict[str, Any]:
    """
    The arena, characterized for a specific set of things: the exact
    count always, the actual list only when feasible.

    :param items: the distinct things
    :returns: dict with the exact count, and the list when feasible
    """
    n = len(items)
    count = bell_number(n)
    feasible = n <= ENUMERATION_CEILING_N
    report = {
        "n": n, "bell_number": count, "enumerable": feasible,
        "items": list(items),
    }
    if feasible:
        report["partitions"] = set_partitions(list(items))
    else:
        report["note"] = (f"Bell({n})={count} exceeds the enumeration "
                           f"ceiling ({ENUMERATION_CEILING_N}) -- counted "
                           f"exactly, not listed.")
    return report


# ═══════════════════════════════════════════════════════════════════════
#  TOOL 2 — FIRING ORDER (sequenced orderings — permutations)
# ═══════════════════════════════════════════════════════════════════════

def firing_order_count(n: int) -> int:
    """
    Exact count of ways to sequence n distinct things: n! .

    :param n: number of distinct things
    :returns: n!
    :raises ValueError: n is negative
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    return math.factorial(n)


def apply_firing_order(written: Sequence[Any], firing_order: Sequence[int]) -> List[Any]:
    """
    Resequence `written` (1-indexed positions) by `firing_order` --
    firing_order[k] names which ORIGINAL position fires k-th.

    Worked example, verified: written=[Scale,Sign,Add], firing_order=(3,1,2)
    -> [Add,Scale,Sign] -- ASS's own canonical name, reached by
    resequencing the written order, not by renaming anything.

    :param written: the items in written order
    :param firing_order: 1-indexed original positions in firing order
    :returns: the items resequenced
    :raises ValueError: firing_order is not a permutation of the positions
    """
    n = len(written)
    if sorted(firing_order) != list(range(1, n + 1)):
        raise ValueError(f"firing_order must be a permutation of 1..{n}, got {firing_order}")
    return [written[i - 1] for i in firing_order]


def all_firing_orders(items: Sequence[Any]) -> List[Tuple[Any, ...]]:
    """
    Every possible sequencing of `items` -- exhaustive. Caller's
    responsibility to keep n small (n! grows fast: 10!~3.6M); this
    function does not guard n the way set_partitions() does, since
    itertools.permutations is already lazy-friendly -- convert to list
    only for small, deliberately-chosen n.

    :param items: the distinct things; keep the count small, n! grows fast
    :returns: every sequencing, as tuples
    """
    return list(itertools.permutations(items))


# ═══════════════════════════════════════════════════════════════════════
#  TOOL 3a — SET MEMBERSHIP: has a firing occurred before?
#  Domain-independent generalization of ASSWord.trajectory()/.collisions()/
#  .would_collide() (ValaQuenta.modules.add_scale_sign, and its standalone
#  port GenerationalLineage/engine/add_scale_sign.py) -- works on ANY
#  sequence of callables applied to a starting point, not just ASS.
# ═══════════════════════════════════════════════════════════════════════

def trajectory(steps: Sequence[Callable[[float], float]], x0: float = 1.0) -> Tuple[float, ...]:
    """
    x0, then the position after each successive step fires, in order --
    the Long Path made explicit for any sequence of callables.

    :param steps: callables x → x, fired in order
    :param x0: starting position
    :returns: x0 followed by the position after each step
    """
    pos = [x0]
    x = x0
    for s in steps:
        x = s(x)
        pos.append(x)
    return tuple(pos)


def visited_positions(steps: Sequence[Callable[[float], float]], x0: float = 1.0,
                       tol: float = 1e-9) -> Dict[float, List[int]]:
    """
    Which trajectory positions repeat, and at which step indices.

    :param steps: callables x → x, fired in order
    :param x0: starting position
    :param tol: tolerance for calling two positions equal
    :returns: map from each repeated position to the step indices that reach it
    """
    traj = trajectory(steps, x0)
    seen: Dict[float, List[int]] = {}
    for i, x in enumerate(traj):
        key = round(x / tol) * tol if tol else x
        seen.setdefault(key, []).append(i)
    return seen


def collisions(steps: Sequence[Callable[[float], float]], x0: float = 1.0,
               tol: float = 1e-9) -> List[Tuple[int, int, float]]:
    """
    Every (earlier_index, later_index, position) where the trajectory
    revisits a position it already reached. Recaman's own defining rule,
    generalized: this IS the set-membership test that rule runs, applied
    to any stepped process, not just the integer line.

    :param steps: callables x → x, fired in order
    :param x0: starting position
    :param tol: tolerance for calling two positions equal
    :returns: (earlier_index, later_index, position) for each revisit
    """
    seen = visited_positions(steps, x0, tol)
    out = []
    for pos, idxs in seen.items():
        if len(idxs) > 1:
            for a, b in zip(idxs, idxs[1:]):
                out.append((a, b, pos))
    return sorted(out)


def would_collide(steps_so_far: Sequence[Callable[[float], float]],
                   candidate_next: Callable[[float], float],
                   x0: float = 1.0, tol: float = 1e-9) -> bool:
    """
    The operator-level flip test: would firing `candidate_next` land on
    a position already in the trajectory so far? Checkable BEFORE
    committing to the step -- Recaman's own a(n-1)-n candidate check,
    generalized to any process.

    :param steps_so_far: callables already fired
    :param candidate_next: the step under test
    :param x0: starting position
    :param tol: tolerance for calling two positions equal
    :returns: True if firing the candidate lands on a position already visited
    """
    traj = trajectory(steps_so_far, x0)
    candidate = candidate_next(traj[-1])
    visited = {round(x / tol) * tol if tol else x for x in traj}
    key = round(candidate / tol) * tol if tol else candidate
    return key in visited


# ═══════════════════════════════════════════════════════════════════════
#  TOOL 3b — SET MEMBERSHIP: jurisdiction violation
#  Grounded in GenerationalLineage/engine/lines.py's own "two
#  jurisdictions" (decomposition/descent vs emerger/ascent). Deliberately
#  parametrized -- this engine does not hardcode that repo's data; callers
#  supply their own jurisdiction map (module-independence convention).
# ═══════════════════════════════════════════════════════════════════════

def jurisdiction_violation(object_name: str, requested_operation: str,
                            jurisdiction_map: Dict[str, Set[str]]) -> Dict[str, Any]:
    """
    Is `requested_operation` a member of the set of operations legal
    for `object_name`'s own jurisdiction? `jurisdiction_map` is
    {object_name: {legal_operation, ...}}, supplied by the caller -- e.g.
    GenerationalLineage's own TOOLSETS/DECOMPOSITION_LINE/EMERGER_LINE,
    read and passed in, not duplicated here.

    A violation is exactly a failed set-membership test: the requested
    operation is not in the object's own legal-operations set. This is
    the formal version of "a bracketing caused one maths to use the
    language of another jurisdiction illegally" -- illegal, precisely
    because it fails membership in the set the object is actually native
    to.

    :param object_name: the object whose jurisdiction applies
    :param requested_operation: the operation requested
    :param jurisdiction_map: {object_name: {legal_operation, …}}, supplied by the caller
    :returns: dict with the verdict; a violation is a failed set-membership test
    """
    legal_ops = jurisdiction_map.get(object_name)
    if legal_ops is None:
        return {"object": object_name, "operation": requested_operation,
                "known": False, "violation": None,
                "note": f"'{object_name}' not present in the supplied jurisdiction map"}
    violated = requested_operation not in legal_ops
    return {
        "object": object_name, "operation": requested_operation,
        "known": True, "legal_operations": sorted(legal_ops),
        "violation": violated,
        "note": (f"'{requested_operation}' is NOT legal for '{object_name}' "
                 f"(legal set: {sorted(legal_ops)})" if violated else
                 f"'{requested_operation}' is legal for '{object_name}'"),
    }


# ═══════════════════════════════════════════════════════════════════════
#  TOOL 4 — PLANS: brackets that carry firing orders, on 16-vectors
#  Ported from SedenionSpectralRelativity/firing_plan.py (module-independence
#  convention: a local exact Cayley–Dickson product, no cross-engine import).
#  A plan is a Leaf (one operator or element) or a Bracket(children, order);
#  order is a permutation of 1..k, entry i names the child that fires i-th.
# ═══════════════════════════════════════════════════════════════════════

Vec = Tuple[F, ...]


def _conj(a: Sequence[F]) -> Vec:
    """Cayley–Dickson conjugate: the real part stays, every other component changes sign."""
    return (a[0],) + tuple(-x for x in a[1:])


def sedenion_mul(a: Sequence[Any], b: Sequence[Any]) -> Vec:
    """
    Exact Cayley–Dickson product (a1, a2)(b1, b2) = (a1 b1 − conj(b2) a2, b2 a1 + a2 conj(b1)), on any power-of-two length.

    :param a: left factor, length 1, 2, 4, 8 or 16
    :param b: right factor, same length
    :returns: the product, as a tuple of Fractions
    """
    a, b = tuple(F(x) for x in a), tuple(F(x) for x in b)
    n = len(a)
    if n == 1:
        return (a[0] * b[0],)
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    left = tuple(x - y for x, y in zip(sedenion_mul(a1, b1), sedenion_mul(_conj(b2), a2)))
    right = tuple(x + y for x, y in zip(sedenion_mul(b2, a1), sedenion_mul(a2, _conj(b1))))
    return left + right


def left_matrix(a: Sequence[Any]) -> List[List[F]]:
    """
    The left-multiplication matrix of a: column k is a·e_k, so left_matrix(a) @ x = a·x.

    :param a: the sedenion, as a sequence of numbers
    :returns: the matrix as a list of rows of Fractions
    """
    n = len(a)
    cols = [sedenion_mul(a, tuple(F(int(i == k)) for i in range(n))) for k in range(n)]
    return [[cols[k][r] for k in range(n)] for r in range(n)]


def _identity(n: int) -> List[List[F]]:
    return [[F(int(r == c)) for c in range(n)] for r in range(n)]


def _matmul(A: List[List[F]], B: List[List[F]]) -> List[List[F]]:
    Bt = list(zip(*B))
    return [[sum((a * b for a, b in zip(row, col)), F(0)) for col in Bt] for row in A]


def _matvec(M: List[List[F]], x: Sequence[F]) -> Vec:
    return tuple(sum((m * v for m, v in zip(row, x)), F(0)) for row in M)


class Leaf:
    """
    One item of a plan.

    :ivar name: the label printed in the notation
    :ivar matrix: the operator reading (a square matrix of Fractions), or None
    :ivar vec: the element reading (a sedenion as a tuple of Fractions), or None
    """

    def __init__(self, name: str, matrix: Optional[List[List[F]]] = None, vec: Optional[Sequence[Any]] = None):
        self.name, self.matrix = name, matrix
        self.vec = None if vec is None else tuple(F(x) for x in vec)

    @classmethod
    def of(cls, name: str, a: Sequence[Any]) -> "Leaf":
        """
        A leaf carrying both readings of one sedenion a: the element a and the operator L_a.

        :param name: the label
        :param a: the sedenion
        :returns: the leaf
        """
        return cls(name, left_matrix(a), a)

    def __repr__(self) -> str:
        return self.name


class Bracket:
    """
    A bracket: children fired in `order`, run as one operation inside its parent.

    :ivar children: the sub-plans, in written order
    :ivar order: a permutation of 1..k; entry i names the child that fires i-th
    :raises ValueError: `order` is not a permutation of 1..k
    """

    def __init__(self, children: Sequence[Any], order: Optional[Sequence[int]] = None):
        k = len(children)
        order = tuple(range(1, k + 1)) if order is None else tuple(order)
        if sorted(order) != list(range(1, k + 1)):
            raise ValueError(f"order must be a permutation of 1..{k}, got {order}")
        self.children, self.order = list(children), order

    def fired(self) -> List[Any]:
        """
        The children in the order they fire.

        :returns: the children, resequenced by `order`
        """
        return [self.children[i - 1] for i in self.order]

    def __repr__(self) -> str:
        return notation(self)


def notation(plan: Any) -> str:
    """
    Write a plan: (A B) default order; (A B | 2 1) the second child fires first; brackets nest.

    :param plan: a Leaf or a Bracket
    :returns: the notation string
    """
    if isinstance(plan, Leaf):
        return plan.name
    body = " ".join(notation(c) for c in plan.children)
    if plan.order != tuple(range(1, len(plan.children) + 1)):
        body += " | " + " ".join(str(i) for i in plan.order)
    return f"({body})"


def fire_sequence(plan: Any) -> List[str]:
    """
    The leaf names in the exact order they fire, the internal bracket orders included.

    :param plan: a Leaf or a Bracket
    :returns: the leaf names, first fired first
    """
    if isinstance(plan, Leaf):
        return [plan.name]
    return [n for c in plan.fired() for n in fire_sequence(c)]


def plan_operator(plan: Any) -> List[List[F]]:
    """
    The OPERATOR reading: the plan as one matrix, the fired children composed, first fired applied first (M_last · … · M_first).

    :param plan: a Leaf or a Bracket whose leaves carry matrices
    :returns: the matrix
    """
    if isinstance(plan, Leaf):
        return plan.matrix
    first = plan.children[0]
    n = len(first.matrix) if isinstance(first, Leaf) else len(plan_operator(first))
    M = _identity(n)
    for c in plan.fired():
        M = _matmul(plan_operator(c), M)
    return M


def plan_value(plan: Any) -> Vec:
    """
    The ELEMENT reading: a bracket is the sedenion product of its fired children, folded left to right ((f1 f2) f3 …); nested brackets give the other groupings. Not associative, so the bracketing changes the result.

    :param plan: a Leaf or a Bracket whose leaves carry vectors
    :returns: the resulting sedenion
    """
    if isinstance(plan, Leaf):
        return plan.vec
    kids = [plan_value(c) for c in plan.fired()]
    acc = kids[0]
    for k in kids[1:]:
        acc = sedenion_mul(acc, k)
    return acc


def apply_plan(plan: Any, x: Sequence[Any]) -> Vec:
    """
    Run the operator reading on an input vector: plan_operator(plan) @ x.

    :param plan: a Leaf or a Bracket whose leaves carry matrices
    :param x: the input sedenion
    :returns: the output sedenion
    """
    return _matvec(plan_operator(plan), tuple(F(v) for v in x))


def evolve_operator(plan: Any, x: Sequence[Any]) -> List[Tuple[str, Vec]]:
    """
    Watch the input vector evolve: the vector after each leaf fires, in firing order. The last state equals apply_plan(plan, x).

    :param plan: a Leaf or a Bracket whose leaves carry matrices
    :param x: the input sedenion
    :returns: [('input', x), (leaf name, vector after it), …]
    """
    leaves: List[Leaf] = []

    def walk(p: Any) -> None:
        if isinstance(p, Leaf):
            leaves.append(p)
        else:
            for c in p.fired():
                walk(c)
    walk(plan)
    v = tuple(F(a) for a in x)
    out: List[Tuple[str, Vec]] = [("input", v)]
    for lf in leaves:
        v = _matvec(lf.matrix, v)
        out.append((lf.name, v))
    return out


def evolve_value(plan: Any) -> List[Tuple[str, Vec]]:
    """
    Watch the element reading evaluate: every product, in the order it is computed (children before their bracket; inside a bracket, the running left fold). The last state equals plan_value(plan).

    :param plan: a Leaf or a Bracket whose leaves carry vectors
    :returns: [(label, vector), …]; a leaf's label is its name, a product's label is its factors in the order they were multiplied, e.g. '((B A) C)'
    """
    out: List[Tuple[str, Vec]] = []

    def go(p: Any) -> Tuple[Vec, str]:
        if isinstance(p, Leaf):
            out.append((p.name, p.vec))
            return p.vec, p.name
        vals = [go(c) for c in p.fired()]
        acc, label = vals[0]
        for v, lab in vals[1:]:
            acc = sedenion_mul(acc, v)
            label = f"({label} {lab})"
            out.append((label, acc))
        return acc, label
    go(plan)
    return out


def parse_plan(text: str, leaves: Dict[str, Leaf]) -> Any:
    """
    Read a plan from its notation, e.g. '((A B | 2 1) C)'.

    :param text: the notation, tokens separated by white space or brackets
    :param leaves: {name: Leaf}
    :returns: the plan
    :raises ValueError: the text has trailing tokens or an unknown leaf name
    """
    toks = text.replace("(", " ( ").replace(")", " ) ").replace("|", " | ").split()
    pos = [0]

    def group() -> Bracket:
        pos[0] += 1
        kids: List[Any] = []
        order: Optional[List[int]] = None
        while toks[pos[0]] != ")":
            if toks[pos[0]] == "(":
                kids.append(group())
            elif toks[pos[0]] == "|":
                pos[0] += 1
                order = []
                while toks[pos[0]] != ")":
                    order.append(int(toks[pos[0]]))
                    pos[0] += 1
            else:
                if toks[pos[0]] not in leaves:
                    raise ValueError(f"unknown leaf {toks[pos[0]]!r}")
                kids.append(leaves[toks[pos[0]]])
                pos[0] += 1
        pos[0] += 1
        return Bracket(kids, order)
    plan = group()
    if pos[0] != len(toks):
        raise ValueError("trailing tokens")
    return plan


# ── the four orderings, enumerated and counted ──────────────────────────

def _binary_plans(leaves: Sequence[Any], both_orders: bool) -> Any:
    n = len(leaves)
    if n == 1:
        yield leaves[0]
        return
    for cut in range(1, n):
        for L in _binary_plans(leaves[:cut], both_orders):
            for R in _binary_plans(leaves[cut:], both_orders):
                for order in ((1, 2), (2, 1)) if both_orders else ((1, 2),):
                    yield Bracket([L, R], order)


def plans_bracketing(leaves: Sequence[Leaf]) -> List[Any]:
    """
    A, BRACKETING: every binary grouping of the written sequence, every bracket in written order: Catalan(n−1) plans.

    :param leaves: the items, in written order
    :returns: the plans
    """
    return list(_binary_plans(list(leaves), False))


def plans_firing_order(leaves: Sequence[Leaf]) -> List[Any]:
    """
    B, FIRING ORDER: one flat bracket over all the items, in each of the n! orders.

    :param leaves: the items, in written order
    :returns: the plans
    """
    n = len(leaves)
    return [Bracket(list(leaves), o) for o in itertools.permutations(range(1, n + 1))]


def plans_firing_of_brackets(leaves: Sequence[Leaf]) -> List[Any]:
    """
    C, FIRING ORDER OF BRACKETS: every binary grouping of the written sequence with either order at every bracket: Catalan(n−1) · 2^(n−1) plans.

    :param leaves: the items, in written order
    :returns: the plans
    """
    return list(_binary_plans(list(leaves), True))


def plans_bracketing_of_firing(leaves: Sequence[Leaf]) -> List[Any]:
    """
    D, BRACKETING OF FIRING ORDERS: choose a firing order of the items, then bracket the FIRED sequence (each bracket in its own written order): n! · Catalan(n−1) plans. Reaches groupings the written-order plans cannot, such as (A C) B.

    :param leaves: the items, in written order
    :returns: the plans
    """
    out: List[Any] = []
    for perm in itertools.permutations(list(leaves)):
        out.extend(_binary_plans(list(perm), False))
    return out


def mode_counts(n: int) -> Dict[str, int]:
    """
    The exact number of binary plans of each kind over n written items.

    :param n: the number of items, at least 1
    :returns: {'A': Catalan(n−1), 'B': n!, 'C': Catalan(n−1)·2^(n−1), 'D': n!·Catalan(n−1)}
    :raises ValueError: n is less than 1
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    cat = math.comb(2 * (n - 1), n - 1) // n
    return {"A": cat, "B": math.factorial(n), "C": cat * 2 ** (n - 1), "D": math.factorial(n) * cat}


def reachable_orders(leaves: Sequence[Leaf], mode: str) -> int:
    """
    How many distinct firing sequences the plans of one kind can produce.

    :param leaves: the items, in written order
    :param mode: 'A', 'B', 'C' or 'D'
    :returns: the number of distinct fire_sequence results
    :raises ValueError: `mode` is not one of A, B, C, D
    """
    make = {"A": plans_bracketing, "B": plans_firing_order, "C": plans_firing_of_brackets, "D": plans_bracketing_of_firing}
    if mode not in make:
        raise ValueError("mode must be one of A, B, C, D")
    return len({tuple(fire_sequence(p)) for p in make[mode](leaves)})


def compare_modes(vectors: Sequence[Sequence[Any]], reading: str = "element", x: Optional[Sequence[Any]] = None) -> Dict[str, Any]:
    """
    Run all four kinds of plan over the same items and count how many different output vectors each makes.

    :param vectors: the items as sedenions (the element reading uses them; the operator reading uses their left-multiplication matrices)
    :param reading: 'element' (multiply the sedenions) or 'operator' (apply the composed matrices to `x`)
    :param x: the input sedenion, required for the operator reading
    :returns: {mode: {'plans': count, 'distinct_outputs': count}} for A, B, C, D, plus 'reading' and 'n'
    :raises ValueError: `reading` is not 'element' or 'operator', or the operator reading is asked without `x`
    """
    if reading not in ("element", "operator"):
        raise ValueError("reading must be 'element' or 'operator'")
    if reading == "operator" and x is None:
        raise ValueError("the operator reading needs the input vector x")
    leaves = [Leaf.of(chr(65 + i), v) for i, v in enumerate(vectors)]
    run = (lambda p: plan_value(p)) if reading == "element" else (lambda p: apply_plan(p, x))
    out: Dict[str, Any] = {"reading": reading, "n": len(leaves)}
    for mode, make in (("A", plans_bracketing), ("B", plans_firing_order), ("C", plans_firing_of_brackets), ("D", plans_bracketing_of_firing)):
        plans = make(leaves)
        out[mode] = {"plans": len(plans), "distinct_outputs": len({run(p) for p in plans})}
    return out
