"""
ValaQuenta.modules.factoral_decomposition.tools
================================================
EquationModule wrapper for the Factoral Decomposition engine.

Version: 0.100 — 2026-09-15
"""

from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation
from .maths import (
    blueprint, reconstruct, consistency_check,
    row_width_threshold, digit_split_candidates,
)


class FactoralDecompositionModule(EquationModule):
    """
    Factoral Decomposition — the construction blueprint, and its undo.
    Long multiplication as an exact forward pathway (blueprint); the
    factoring problem as that same pathway read backward by exact
    elimination (reconstruct), never brute-force search.
    """

    @property
    def name(self) -> str:
        return "factoral_decomposition"

    @property
    def display_name(self) -> str:
        return "Factoral Decomposition Engine — the construction blueprint, and its undo"

    @property
    def version(self) -> str:
        return "0.100"

    @property
    def description(self) -> str:
        return (
            "Long multiplication is a two-stage forward pathway: a "
            "convolution of digit sequences (row products), then a "
            "carry-propagating recurrence, twice (within each row, then "
            "across all rows). blueprint() computes that pathway exactly "
            "for any (a,b) — verified digit-for-digit against a real "
            "hand-worked example. reconstruct() reads the SAME pathway "
            "backward from the answer alone, via exact elimination on "
            "digit-length windows (Fraction, never float) — not search, "
            "not heuristic pruning: an empty window is a proof, not a "
            "guess. Honest scope, measured not assumed: fast and complete "
            "on unbalanced/smooth numbers; exponential on balanced, "
            "prime-factor numbers — the identical wall independently "
            "confirmed this session by AbrikosovTree's winding-field "
            "equidistribution result, via a completely unrelated method."
        )

    @property
    def confidence_floor(self) -> str:
        return "ESTABLISHED"

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                "blueprint",
                "The full construction pathway for (a,b): every row, its own carry chain "
                "and width, the single-line cross-row carry, the exact answer.",
                r"N = \sum_r a\cdot b_r\cdot 10^r,\ \text{carried exactly}",
                "one row = a times one digit, shifted by that digit's own place",
                "ESTABLISHED", True, ["a", "b"],
                lambda a, b: blueprint(a, b), ["text"],
                process="Multiply forward, row by row, and carry exactly — the pathway, not just the product.",
            ),
            Equation(
                "reconstruct",
                "Exact elimination from N alone: every divisor pair found, cost reported "
                "honestly, never silently truncated.",
                r"a\cdot b = N,\ \text{windows on } b=N/a \text{ pruned only by proof}",
                "top-down digit windows, each either empty (proof) or not",
                "ESTABLISHED", True, ["N"],
                lambda N: reconstruct(N), ["text"],
                process="Read the answer's digits backward through the same pathway that built it.",
            ),
            Equation(
                "consistency_check",
                "Cross-check a candidate (a,b) against the row/threshold structure directly.",
                r"\text{blueprint}(a,b) \stackrel{?}{=} N",
                "does the reconstructed pathway land exactly on the given answer",
                "ESTABLISHED", True, ["a", "b"],
                lambda a, b: consistency_check(a, b), ["text"],
                process="Verify a candidate pair by walking the forward pathway and checking it lands exactly.",
            ),
            Equation(
                "row_width_threshold",
                "The single number, fixed by `a` alone, that decides which rows grow a digit.",
                r"t = \lceil 10^{D_a} / a \rceil",
                "one threshold, fixed before any digit of the other factor is known",
                "ESTABLISHED", True, ["a", "Da"],
                lambda a, Da: row_width_threshold(a, Da), ["text"],
                process="Compute the one threshold that decides every row's width, before touching the other factor.",
            ),
            Equation(
                "digit_split_candidates",
                "Every (Da,Db) factor-length split consistent with N's own digit count.",
                r"D_a + D_b \in \{\mathrm{digits}(N),\ \mathrm{digits}(N)+1\}",
                "a free fact off N's digit count, no search",
                "ESTABLISHED", True, ["N"],
                lambda N: digit_split_candidates(N), ["text"],
                process="List the digit-length splits N's own size allows, before searching anything.",
            ),
        ]

    # ── run / viewer ─────────────────────────────────────────────────────
    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"'{equation_name}' not in factoral_decomposition")
        result = eq.compute(**params) if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "module": self.name,
                "equation": equation_name, "data": out["result"]}
