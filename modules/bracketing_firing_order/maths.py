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

Version: 0.1 -- first build.
"""
from __future__ import annotations

import itertools
import math
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
