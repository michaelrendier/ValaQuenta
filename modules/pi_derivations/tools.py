"""
ValaQuenta.modules.pi_derivations.tools
=======================================
THE PI DERIVATION TOOLSET.  Module Tools (EquationModule registry contract: formulary(), run(), viewer_data(), shell_commands()).

Version: 0.1
"""
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from . import maths as M


class PiDerivationsModule(EquationModule):
    """The Pi Derivation Toolset."""

    @property
    def name(self): return "pi_derivations"

    @property
    def display_name(self): return "Pi Derivations (every route to π, labelled by what of the circle it already holds)"

    @property
    def version(self): return "0.1"

    @property
    def description(self):
        return ("Every route to π the project meets, each computed without reading math.pi: the emergent π (first zero of the cosine series), "
                "the orbit routes (x'' = -x, the Lagrangian conjugate point), polygons, series, products, Basel and the Euler product, integrals, "
                "AGM, Ramanujan/Chudnovsky/BBP, the Cauchy residue around a square, the Smith chart, the cardioid, the sedenion exponential, "
                "the ring eigenvalue, and the project's U(1) normalisation (an identity, not a derivation). Each route carries circle_in: what of "
                "the circle its inputs already contain.")

    @property
    def confidence_floor(self): return "ESTABLISHED"

    @property
    def process_description(self):
        return "Runs a route to π from its own inputs, reports the value against math.pi (comparison only) and classifies what of the circle the route assumed."

    def formulary(self) -> List[Equation]:
        def eq(name, display, latex, radian, conf, params, fn, process):
            return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf, code_verified=True,
                            params=params, compute=fn, display_options=["text"], process=process)
        return [
            eq("verify", "VERIFY: every route lands within its stated tolerance", r"\pi\ \text{from each route}", "a route that misses is a bug, not a result", "ESTABLISHED", [],
               lambda: M.verify(), "Runs every route and checks it against its tolerance; the identity route must return no value."),
            eq("all_routes", "ALL ROUTES: value, error, circle_in", r"\pi=\ldots", "circle_in classifies what the inputs already contain", "ESTABLISHED", [],
               lambda: M.all_routes(), "Runs every route with default parameters."),
            eq("derive", "ONE ROUTE", r"\pi=f(\text{route})", "see ROUTES", "ESTABLISHED", ["name"],
               lambda name="cos_zero": M.derive(name), "Runs one named route."),
            eq("emergent", "THE EMERGENT π: twice the first zero of the cosine power series", r"\cos x=\sum(-1)^kx^{2k}/(2k)!;\ \pi=2x_0",
               "no diameter, circumference, angle or polygon in the inputs", "ESTABLISHED", [], lambda: M.emergent_pi(), "Computes π from the series alone and states what it was computed from."),
            eq("circle_audit", "CIRCLE AUDIT: routes grouped by what of the circle their inputs hold", r"\text{none/orbit/constructed/dual/path/library/identity}",
               "the search for literal π everywhere starts from the none/orbit/path groups", "ESTABLISHED", [], lambda: M.circle_audit(), "Lists the routes under each circle_in label."),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"pi_derivations has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name, "text": repr(out["result"])}

    def shell_commands(self) -> Dict[str, Any]:
        return {"pi_emergent": M.emergent_pi, "pi_all": M.all_routes, "pi_audit": M.circle_audit}
