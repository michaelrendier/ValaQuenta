"""
ainulindale_engine.modules.add_scale_sign.maths
================================================
THE ADD:SCALE:SIGN DATATYPE — a value type for manipulating elements of the
tier-0 floor  Aff(1,ℝ) = ℝ ⋊ (ℝ_{>0} × ℤ/2) = ADD ⋊ (SCALE × SIGN),
i.e. the maps   x ↦ sign·scale·x + add.

WHY a datatype, not just functions: `str` carries its own manipulation methods
(split / strip / replace / join). ADD:SCALE:SIGN elements need the same — a
type you *compose*, *invert*, *decompose*, take *residuals* of (strip one
generator, keep the rest), read out on the *orthogonal Smith charts*, and whose
*firing order* is recorded. That firing order is the load-bearing content here
(`[SCALE, ADD] = ADD`, the one non-trivial bracket) — order matters at THIS
tier; the sedenion does not enter.

NO REDUNDANT MATHS: the four-question decomposition test, `classify`, `describe`,
the roll-down table and `AFF1` metadata live in `VAPMIP/add_scale_sign.py` and
are not re-implemented here. This module is the VALUE TYPE and its own
manipulation surface. The Möbius fold primitive is kept local per this repo's
module-independence convention (cf. modules/scale/maths.py `mobius_fold`).

Each generator carries its own equation part (the contribution to the
generalized-equation word  u = Σ_k [ g_k·ln s_k + a_k ] ,  Γ = tanh(u/2)):

    ADD      x ↦ x + a        Δ_ADD   = a           (translation; the flow / count)
    SCALE    x ↦ s·x          Δ_SCALE = ln s        (log-gain; the fold contribution)
    SIGN     x ↦ g·x          Δ_SIGN  = g ∈ {−1,+1} (one bit; det ±1)

    ground state  a=0, s=1, g=+1  ⇒  u=0  ⇒  Γ=0   (the identity / the "now")

Version: 0.1
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence, Tuple

# ── group constants — canonical source: VAPMIP/add_scale_sign.py ──────────
IDENTITIES = (0.0, 1.0, 1)                 # ADD, SCALE, SIGN  (the Mingling)
BRACKET = "[SCALE, ADD] = ADD"             # the one non-trivial bracket
CAMSHAFT = ("SIGN", "SCALE", "ADD")        # the three-phase firing order:
                                          # SIGN fires first (innermost),
                                          # then SCALE, then ADD —
                                          #   x ↦ ADD( SCALE( SIGN(x) ) )

_TANH, _LOG, _ATANH, _EXP = math.tanh, math.log, math.atanh, math.exp


def _gamma(u: float) -> float:
    """The Smith / Joukowsky fold in word coordinates:  Γ = tanh(u/2).
    Local copy per the module-independence convention; identical to
    modules/scale/maths.py `fold_is_log_tanh` on the real axis."""
    return _TANH(0.5 * u)


# ════════════════════════════════════════════════════════════════════════
#  THE DATATYPE
# ════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class ASS:
    """One element of Aff(1,ℝ):  x ↦ sign·scale·x + add.

    Immutable. Compose with `@` (or `.then`), invert with `~`, apply by
    calling. `.steps` records the atomic generators that built it, in
    APPLICATION order (first-applied first) — the record / Long Path.
    """
    add: float = 0.0
    scale: float = 1.0
    sign: int = 1
    steps: Tuple["ASS", ...] = field(default=(), compare=False, repr=False)

    # ── construction ────────────────────────────────────────────────────
    def __post_init__(self):
        if self.scale <= 0:
            raise ValueError(f"SCALE must be > 0 (got {self.scale}); a negative "
                             f"gain is SCALE∘SIGN — build it as ASS.SCALE(|s|) @ ASS.SIGN(-1)")
        if self.sign not in (-1, 1):
            raise ValueError(f"SIGN must be ±1 (got {self.sign})")
        if not self.steps:
            object.__setattr__(self, "steps", (self,))

    @classmethod
    def ADD(cls, a: float) -> "ASS":
        return cls(float(a), 1.0, 1)

    @classmethod
    def SCALE(cls, s: float) -> "ASS":
        return cls(0.0, float(s), 1)

    @classmethod
    def SIGN(cls, g: int) -> "ASS":
        return cls(0.0, 1.0, int(g))

    IDENTITY: "ASS" = None          # filled after class body
    GROUND: "ASS" = None            # alias — "the now"

    # ── apply ──────────────────────────────────────────────────────────
    def __call__(self, x: float) -> float:
        return self.sign * self.scale * x + self.add

    # ── compose:  (self @ other)(x) = self(other(x))  — other fires first
    def __matmul__(self, other: "ASS") -> "ASS":
        if not isinstance(other, ASS):
            return NotImplemented
        return ASS(
            self.add + self.sign * self.scale * other.add,
            self.scale * other.scale,
            self.sign * other.sign,
            steps=other.steps + self.steps,          # application order
        )

    def then(self, other: "ASS") -> "ASS":
        """Forward chaining: do `self`, THEN `other`.  self.then(o) == o @ self."""
        return other @ self

    # ── invert (backward) ─────────────────────────────────────────────
    def _is_atomic(self) -> bool:
        return len(self.steps) == 1 and self.steps[0] is self

    def __invert__(self) -> "ASS":
        a = -self.sign * self.add / self.scale + 0.0        # normalise −0.0
        s, g = 1.0 / self.scale, self.sign
        if self._is_atomic():
            return ASS(a, s, g)                         # steps ← (itself,) in __post_init__
        inv = ASS(a, s, g)
        object.__setattr__(inv, "steps",
                           tuple(~step for step in reversed(self.steps)))
        return inv

    def backward(self) -> "ASS":
        return ~self

    # ── residuals — the str.strip / str.replace analogue ─────────────
    def residual(self, without: str) -> "ASS":
        """Return this element with ONE generator reset to its identity —
        'strip the SIGN and keep the rest'. `without` ∈ {'ADD','SCALE','SIGN'}."""
        w = without.upper()
        if w == "ADD":
            return ASS(0.0, self.scale, self.sign)
        if w == "SCALE":
            return ASS(self.add, 1.0, self.sign)
        if w == "SIGN":
            return ASS(self.add, self.scale, 1)
        raise ValueError("without must be one of ADD, SCALE, SIGN")

    def only(self, part: str) -> "ASS":
        """The complementary move — keep ONE generator, drop the other two."""
        p = part.upper()
        if p == "ADD":
            return ASS.ADD(self.add)
        if p == "SCALE":
            return ASS.SCALE(self.scale)
        if p == "SIGN":
            return ASS.SIGN(self.sign)
        raise ValueError("part must be one of ADD, SCALE, SIGN")

    def parts(self) -> Tuple["ASS", "ASS", "ASS"]:
        """The three pure generators, in CAMSHAFT (firing) order:
        (SIGN, SCALE, ADD).  self == parts[2] @ parts[1] @ parts[0]."""
        return (ASS.SIGN(self.sign), ASS.SCALE(self.scale), ASS.ADD(self.add))

    def is_ground(self, tol: float = 1e-12) -> bool:
        return (abs(self.add) <= tol and abs(self.scale - 1.0) <= tol
                and self.sign == 1)

    # ── the equation parts / the generalized-equation word ───────────
    def u(self) -> float:
        """This element's contribution to the word  u = g·ln s + a."""
        return self.sign * _LOG(self.scale) + self.add

    def gamma(self) -> float:
        """Position on the fold:  Γ = tanh(u/2)."""
        return _gamma(self.u())

    def equation_parts(self) -> Dict[str, Any]:
        a, s, g = self.add, self.scale, self.sign
        u = self.u()
        return {
            "ADD":   {"map": "x ↦ x + a",   "Δ": a,        "part": f"a = {a:g}"},
            "SCALE": {"map": "x ↦ s·x",     "Δ": _LOG(s),  "part": f"ln s = ln {s:g} = {_LOG(s):.6g}"},
            "SIGN":  {"map": "x ↦ g·x",     "Δ": g,        "part": f"g = {g:+d}"},
            "word":  f"u = g·ln s + a = {g:+d}·{_LOG(s):.6g} + {a:g} = {u:.6g}",
            "fold":  f"Γ = tanh(u/2) = {self.gamma():.6g}",
            "additive": self.is_additive(),
        }

    def is_additive(self) -> bool:
        """True iff  u(self)  equals the plain sum of the parts' words
        u(ADD(a)) + u(SCALE(s)) + u(SIGN(g)) = a + ln s + 0.
        Since u(self) = g·ln s + a, this holds exactly when g == +1 or
        s == 1 — i.e. the SIGN does not flip a non-trivial SCALE. When it
        does, the word is order-sensitive: [SCALE, ADD] = ADD has bitten."""
        return self.sign == 1 or abs(self.scale - 1.0) < 1e-12

    # ── the orthogonal Smith charts ─────────────────────────────────
    def to_smith(self) -> Dict[str, Any]:
        """Read the element on the orthogonal 2-ring chart in the maths
        language it was built on:

            Γ_SCALE = tanh(½·ln s)     (the multiplicative / E–W ring)
            Γ_ADD   = tanh(½·a)        (the additive / N–S ring)
            parity  = g               (which quadrant sheet)

        ground state → (0, 0, +1) → the centre / the now.
        """
        g_scale = _gamma(_LOG(self.scale))
        g_add = _gamma(self.add)
        quad = {(True, True): "NE", (True, False): "SE",
                (False, True): "NW", (False, False): "SW"}[(g_add >= 0, g_scale >= 0)]
        if self.sign < 0:
            quad = quad + "′"           # the SIGN-flipped sheet
        return {
            "Γ_SCALE": g_scale, "Γ_ADD": g_add, "parity": self.sign,
            "quadrant": quad, "u": self.u(), "Γ": self.gamma(),
            "at_now": abs(g_scale) < 1e-12 and abs(g_add) < 1e-12 and self.sign == 1,
            "notation": (f"Γ_SCALE = tanh(½·ln {self.scale:g}) = {g_scale:.6g}   "
                         f"Γ_ADD = tanh(½·{self.add:g}) = {g_add:.6g}   parity {self.sign:+d}"),
        }

    # ── lineage — two orderings of the recorded steps ────────────────
    def lineage(self, order: str = "chrono") -> "ASSWord":
        """Return the recorded generator sequence as an ASSWord.

        order='chrono'  — application order (the record / when it fired).
        order='zeta'    — sorted by spectral weight |u_k| descending
                          (how much each step moves the fold — SCALE-heavy
                          steps first). The departure between the two
                          orderings is this datatype's ψ(x)−x.
        """
        steps = list(self.steps)
        if order == "zeta":
            steps.sort(key=lambda s: abs(s.u()), reverse=True)
        elif order != "chrono":
            raise ValueError("order must be 'chrono' or 'zeta'")
        return ASSWord(tuple(steps), order, self)

    def record(self) -> Tuple[Tuple[float, float, int], ...]:
        """The immutable log — (add, scale, sign) of every atomic step,
        application order. Paper's Hands / the Long Path."""
        return tuple((s.add, s.scale, s.sign) for s in self.steps)

    def camshaft(self) -> Tuple[str, ...]:
        return CAMSHAFT

    def __repr__(self) -> str:
        return f"ASS(add={self.add:g}, scale={self.scale:g}, sign={self.sign:+d})"

    def __str__(self) -> str:
        return f"x ↦ {self.sign:+d}·{self.scale:g}·x + {self.add:g}"


ASS.IDENTITY = ASS(*IDENTITIES)
ASS.GROUND = ASS.IDENTITY


# ════════════════════════════════════════════════════════════════════════
#  THE DECOMPOSITION TYPE  (this datatype's own "type of decomposition")
# ════════════════════════════════════════════════════════════════════════
@dataclass(frozen=True)
class ASSWord:
    """The decomposition of an ASS element into an ordered word of atomic
    generators — the ADD:SCALE:SIGN analogue of what `str.split()` returns,
    plus the equation parts and the fold reading.
    """
    steps: Tuple[ASS, ...]
    order: str
    source: ASS

    def u_total(self) -> float:
        return self.source.u()

    def u_generators(self) -> float:
        """Σ u of the three canonical generators ADD(a)+SCALE(s)+SIGN(g)
        = a + ln s + 0 — the 'plain sum', order ignored."""
        return self.source.add + _LOG(self.source.scale)

    def u_sum_of_steps(self) -> float:
        """Σ u over the RECORDED atomic steps (informational for a
        multi-step word; equals u_total for an atomic one)."""
        return sum(s.u() for s in self.steps)

    def firing_defect(self) -> float:
        """u_total − Σ u_generators = (g − 1)·ln s : the amount the firing
        order (the SIGN sitting inside SCALE) contributed. Zero iff g=+1 or
        s=1; otherwise −2·ln s. [SCALE, ADD] = ADD has bitten. This is the
        datatype's own 'you defined it twice' residual — the same shape as
        the Bell composed-rotation defect."""
        return self.u_total() - self.u_generators()

    def additive(self) -> bool:
        return abs(self.firing_defect()) < 1e-9

    # kept for back-compat with earlier callers
    def u_sum_of_parts(self) -> float:
        return self.u_generators()

    def gamma(self) -> float:
        return self.source.gamma()

    def as_equation(self) -> str:
        s = self.source                    # the resulting element — g·ln s + a
        terms = []
        if abs(s.scale - 1.0) > 1e-12:
            terms.append(f"{s.sign:+d}·ln {s.scale:g}")
        if abs(s.add) > 1e-12 or not terms:
            terms.append(f"{s.add:+g}")
        body = " + ".join(terms)
        return (f"u = {body} = {self.u_total():.6g}    "
                f"Γ = tanh(u/2) = {self.gamma():.6g}"
                + ("" if self.additive() else
                   f"    [firing defect {self.firing_defect():+.3g}: SIGN flipped a non-trivial SCALE]"))

    def __iter__(self):
        return iter(self.steps)

    def __len__(self):
        return len(self.steps)

    def __str__(self) -> str:
        seq = "  ∘  ".join(
            ("SIGN(%+d)" % s.sign) if s.sign != 1 and s.scale == 1 and s.add == 0 else
            ("SCALE(%g)" % s.scale) if s.scale != 1 and s.add == 0 else
            ("ADD(%g)" % s.add) if s.add != 0 and s.scale == 1 else
            repr(s)
            for s in self.steps
        )
        return f"ASSWord[{self.order}]:  {seq or 'IDENTITY'}\n  {self.as_equation()}"


# ════════════════════════════════════════════════════════════════════════
#  helpers
# ════════════════════════════════════════════════════════════════════════
def compose(*elements: ASS) -> ASS:
    """Left-to-right application order: compose(a, b, c) applies a, then b,
    then c  ==  c @ b @ a.  The record holds exactly the elements given."""
    if not elements:
        return ASS.IDENTITY
    out = elements[0]
    for e in elements[1:]:
        out = e @ out
    return out


def from_map(add: float, scale: float, sign: int = 1) -> ASS:
    return ASS(add, scale, sign)


def word(u: float) -> ASS:
    """The pure-SCALE element whose word is u  (Γ = tanh(u/2))."""
    return ASS.SCALE(_EXP(u))


def ground() -> ASS:
    return ASS.GROUND
