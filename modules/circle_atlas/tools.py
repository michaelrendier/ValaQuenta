"""
ValaQuenta.modules.circle_atlas.tools
=====================================
THE CIRCLE ATLAS.  Module Tools (EquationModule registry contract: formulary(), run(), viewer_data(), shell_commands()).

Version: 0.1
"""
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from . import maths as M


class CircleAtlasModule(EquationModule):
    """The Circle Atlas."""

    @property
    def name(self): return "circle_atlas"

    @property
    def display_name(self): return "The Circle Atlas (H_hat_RB and the Complete Shape of Mathematics)"

    @property
    def version(self): return "0.1"

    @property
    def description(self):
        return ("A map of every way the project's mathematics meets a circle. Each viewport (waveform, Hamiltonian, Lagrangian, Berry-Keating, "
                "cardioid, epicycles, Smith chart, Apollonian gasket, inversion, Hopf fibre, roots of unity, the sedenion's 15 circles and zero-divisor "
                "circles, ADD:SCALE:SIGN, prime wheels, ring, BAO ring, polygons, the normalising retraction, winding, sphere and hypersphere, recursive field axes, the native units ln 10 and π, the box-kite spectrum) is run as TO (the "
                "transformation that enters fixed-point space and whether the result closes on the circle) and FROM (the transformation out, with "
                "the fibre of choices it needs). Each carries its pi route (module pi_derivations). A census counts circle-bearing tokens over the "
                "repositories and an import probe records which modules do not load.")

    @property
    def confidence_floor(self): return "THEORETICAL"

    @property
    def process_description(self):
        return "Runs the viewports, reports where each enters and leaves the circle, and lists what is not yet mapped."

    def formulary(self) -> List[Equation]:
        def eq(name, display, latex, radian, conf, params, fn, process):
            return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf, code_verified=True,
                            params=params, compute=fn, display_options=["text"], process=process)
        return [
            eq("verify", "VERIFY: every viewport closes (or fails as recorded)", r"|z|=1", "a failed TO is printed, not smoothed", "ESTABLISHED", [], lambda: M.verify(),
               "Runs all viewports and checks TO/FROM, the Wick transform of xp, the sign carriers and the emergent π."),
            eq("atlas", "ATLAS: every viewport, TO and FROM", r"\text{viewport}\to S^1\to\text{viewport}", "FROM is a relation with a fibre, not an inverse", "ESTABLISHED", [],
               lambda: M.atlas(), "Runs every viewport and returns its TO/FROM results and pi route."),
            eq("entry", "ONE VIEWPORT", r"\text{TO},\text{FROM}", "see VIEWPORTS", "ESTABLISHED", ["name"], lambda name="waveform": M.entry(name),
               "Runs one named viewport."),
            eq("signposts", "SIGN-POSTS: the road in, the road out, the pi route", r"\text{enter}/\text{exit}", "entries are exits", "ESTABLISHED", [], lambda: M.signposts(),
               "The table of entries and exits per viewport."),
            eq("gaps", "GAPS: what is not yet mapped", r"\emptyset", "gaps are sign-posts to further mappings", "ESTABLISHED", [], lambda: M.gaps(),
               "Viewports without a pi route, viewports whose TO fails raw, and the named gaps."),
            eq("sign_carriers", "SIGN: which sedenion axes carry it", r"e_kx=x^*e_k", "the whole second octonion e8..e15", "ESTABLISHED", [], lambda: M.sign_carriers(),
               "Tests the doubling identity on every axis."),
            eq("ball_table", "N-BALL: volume, surface area, peak dimension", r"V_n=\\pi^{n/2}/\\Gamma(n/2+1)", "V_n = (2π/n) V_{n−2}; peaks at n = 5; surface peaks at n = 7", "ESTABLISHED", [], lambda: M.ball_table(),
               "The unit n-ball table and where the sedenion (n = 16) sits."),
            eq("kite_spectrum", "BOX-KITE SPECTRUM: emit and interpret", r"L_d^T=-L_d", "lines 0, √2, 2 with multiplicities 4, 8, 4; the nullspace names the kite", "ESTABLISHED", [], lambda: M.kite_spectrum(),
               "Spectrum of the left-multiplication operator of every zero-divisor diagonal, and the nullspace round trip to the kite."),
            eq("anchored_readings", "BOX-KITE FROM AN ANCHOR (the string)", r"\\sigma(L_aL_b)", "one bare spectrum becomes seven classes from any anchor; De Marrais vs Scalar vs Scaled constructs", "ESTABLISHED", [], lambda: M.anchored_readings(),
               "Splits the 84 zero-divisor diagonals by their reading from an anchor and notates the three constructs."),
            eq("real_component_effect", "THE 15 AXES ON THE REAL COMPONENT", r"\\mathrm{Re}(e^{\\theta e_k}z)=r\\cos\\theta-y_k\\sin\\theta", "each axis pairs Real with itself and the other 14 into 7 planes", "ESTABLISHED", [], lambda: M.real_component_effect(),
               "Checks the Real-part law and L² = −1 for every axis and lists the planes."),
            eq("census", "CENSUS: circle-bearing tokens over the repositories", r"\text{text count}", "where to look, not proof", "ESTABLISHED", [], lambda: M.census(),
               "Counts pi, trig, phase, circle and wave tokens in every Python file of the standing repository list."),
            eq("import_probe", "IMPORT PROBE: which modules load", r"\text{import}", "failures are data", "ESTABLISHED", [], lambda: M.import_probe(),
               "Imports every ValaQuenta module and GenerationalLineage toolset and records failures."),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"circle_atlas has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name, "text": repr(out["result"])}

    def shell_commands(self) -> Dict[str, Any]:
        return {"atlas_run": M.atlas, "atlas_signposts": M.signposts, "atlas_gaps": M.gaps, "atlas_census": M.census, "atlas_ball_table": M.ball_table, "atlas_kite_spectrum": M.kite_spectrum}
