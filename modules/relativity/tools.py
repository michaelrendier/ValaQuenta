"""
ValaQuenta.modules.relativity.tools
===================================
EINSTEIN'S RELATIVITY: FOUR SPACES, EACH WITH ITS OWN JURISDICTION.  Module Tools (EquationModule registry contract: formulary(), run(), viewer_data(), shell_commands()).

Version: 0.1
"""
from typing import Dict, List, Any
from fractions import Fraction

from ...engine.registry import EquationModule, Equation
from . import maths as R
from . import minkowski as Mk
from . import curved as Cv
from . import tangent as Tg
from . import metric as Me
from . import crossings as Cr
from . import bridge as Br
from . import checks as Ck


class RelativityModule(EquationModule):
    """Einstein's relativity as four spaces: Minkowski, curved, tangent, metric."""

    @property
    def name(self): return "relativity"

    @property
    def display_name(self): return "Relativity: Minkowski, curved, tangent and metric spaces"

    @property
    def version(self): return "0.1"

    @property
    def description(self):
        return ("Einstein's special and general relativity organised as four spaces with their own jurisdictions: Minkowski space (boosts, rapidity, the "
                "Lorentz algebra, Thomas-Wigner rotation, invariant mass, hyperbolic motion), curved spacetime (curvature from any metric, the standard "
                "solutions, perihelion, light deflection, clocks, tides, the binary pulsar, gravitational waves), the tangent space where the equivalence "
                "principle holds, and the space of metrics where the Einstein equations live (the lapse constraint, gauge invariance). Each space "
                "declares what operations are legal in it; the crossings between them are measured.")

    @property
    def confidence_floor(self): return "ESTABLISHED"

    @property
    def process_description(self):
        return "Builds each of the four spaces of relativity, checks them against measured numbers and against each other, and tests which operations are legal where."

    def formulary(self) -> List[Equation]:
        def eq(name, display, formula, radian, conf, params, fn, process):
            return Equation(name=name, display=display, latex=formula, radian_form=radian, confidence=conf, code_verified=True,
                            params=params, compute=fn, display_options=["text"], process=process)
        E = "ESTABLISHED"; I = "THEORETICAL"   # the registry tiers are ESTABLISHED / THEORETICAL / CONJECTURE / OPEN; the prose labels these INTERPRETATION
        return [
            eq("verify", "VERIFY: numeric checks across all four spaces", "boosts, algebra, measured numbers, jurisdictions", "each against a stated tolerance", E, [], lambda: Ck.verify(),
               "Fast numeric checks; the symbolic ones are in verify_symbolic."),
            eq("verify_symbolic", "VERIFY: symbolic checks", "Ricci = 0, K = 48 M^2/r^6, Bianchi, Friedmann from the lapse, gauge invariance", "sympy", E, [], lambda: Ck.verify_symbolic(),
               "The slower symbolic derivations (tens of seconds)."),
            eq("spaces", "SPACES: the four declarations", "points, axes, motions, invariant, views, test, engine, status", "the eight fields of the spatial-simulation skill", E, [],
               lambda: {k: {kk: vv for kk, vv in v.items() if kk not in ("legal", "illegal")} for k, v in R.SPACES.items()}, "What each space is."),
            eq("jurisdiction", "JURISDICTION: is an operation legal in a space?", "operation in legal(space)", "set membership (bracketing_firing_order.jurisdiction_violation)", E, ["space", "operation"],
               lambda space="curved", operation="global_boost": R.jurisdiction_check(space, operation), "The legal-operation test, and whether the space names it illegal."),
            eq("crossings", "CROSSINGS: operations legal in one space and illegal in another", "table", "from the four jurisdictions", E, [], lambda: {k: v for k, v in R.crossing_table().items() if v["crossing"]},
               "Where using one space's language in another is the error."),
            # ---- Minkowski
            eq("mink_boost", "MINKOWSKI: the boost", "L(beta), gamma = 1/sqrt(1-beta^2)", "Lorentz-invariance residual", E, ["beta"],
               lambda beta=0.6: {"gamma": Mk.gamma(beta), "rapidity": Mk.rapidity(beta), "invariance_residual": Mk.invariance_residual(Mk.boost([beta, 0, 0])), "time_dilation": Mk.time_dilation(beta), "length_contraction": Mk.length_contraction(beta)},
               "Boost along x and what it does to clocks and rods."),
            eq("mink_rapidity", "MINKOWSKI: velocity addition is addition of rapidities", "atanh((a+b)/(1+ab)) = atanh a + atanh b", "residual", E, ["b1", "b2"],
               lambda b1=0.6, b2=0.7: Mk.rapidity_additivity(b1, b2), "Composition of collinear boosts."),
            eq("mink_interval", "MINKOWSKI: the interval", "s^2 = -(c dt)^2 + dx^2", "timelike / null / spacelike", E, ["dt", "dx"],
               lambda dt=2.0, dx=1.0: Mk.interval([dt, dx, 0, 0]), "Causal kind of the separation of two events."),
            eq("mink_lightcone", "MINKOWSKI: a boost is a dilation of the light-cone coordinates", "u -> u/k, v -> k v, k = sqrt((1+b)/(1-b))", "residual", E, ["beta"],
               lambda beta=0.6: Mk.lightcone_dilation_check(beta), "Boosts as scalings of u and v (the Doppler factor)."),
            eq("mink_thomas_wigner", "MINKOWSKI: the Thomas-Wigner rotation", "cos(theta) = (g1 + g2)/(1 + g1 g2)", "perpendicular boosts", E, ["beta1", "beta2"],
               lambda beta1=0.6, beta2=0.7: Mk.thomas_wigner(beta1, beta2), "Two perpendicular boosts compose to a boost and a rotation."),
            eq("mink_algebra", "MINKOWSKI: the Lorentz algebra so(3,1)", "[J,J] = J, [J,K] = K, [K,K] = -J", "six generators", E, [], lambda: Mk.lorentz_algebra(), "Closure of the six generators."),
            eq("mink_threshold", "MINKOWSKI: fixed-target threshold", "T = (M^2 - (m1+m2)^2)/(2 m2)", "p + p -> p + p + p + pbar: 6 m_p", E, ["m_beam", "m_target", "m_products"],
               lambda m_beam=1.0, m_target=1.0, m_products=4.0: {"T_threshold": Mk.fixed_target_threshold(m_beam, m_target, m_products)}, "Minimum beam kinetic energy."),
            eq("mink_trip", "MINKOWSKI: a trip at constant proper acceleration", "tau = 2 (c/a) acosh(1 + a d/(2c^2))", "accelerate half, decelerate half", E, ["distance_ly", "a_g"],
               lambda distance_ly=4.37, a_g=1.0: {"proper_years": Mk.trip_proper_time(distance_ly * 9.4607304725808e15, a_g * 9.80665) / 3.15576e7},
               "Proper time of the traveller."),
            eq("mink_em", "MINKOWSKI: the electromagnetic invariants", "E^2 - c^2 B^2, E.B", "unchanged by a boost", E, [],
               lambda: (lambda E0, B0: {"before": Mk.em_field_invariants(E0, B0), "after": Mk.em_field_invariants(*Mk.em_boost(E0, B0, [0.3, 0.2, 0.1]))})([1.0, 0.5, 0.2], [0.1, 0.4, 0.3]),
               "The two scalars of the field tensor."),
            eq("mink_derivation", "MINKOWSKI: the boost derived from the interval", "g^2 (1 - b^2) = 1", "sympy", E, [], lambda: {k: str(v) for k, v in Mk.lorentz_derivation().items()}, "From invariance of the interval."),
            # ---- curved
            eq("curved_solutions", "CURVED: the standard solutions and the Bianchi identity", "Ricci = 0, K = 48M^2/r^6, G = -Lambda g", "symbolic", E, [], lambda: Cv.solution_checks(), "Vacuum, de Sitter, FLRW, Bianchi."),
            eq("curved_orbit", "CURVED: perihelion advance", "6 pi M / p per orbit", "integrated orbit against formula", E, ["p", "e"],
               lambda p=200.0, e=0.3: Cv.orbit_precession_numeric(p, e), "Integrates u'' + u = M/L^2 + 3Mu^2."),
            eq("curved_mercury", "CURVED: Mercury", "42.98 arcsec per century", "from 6 pi GM/(c^2 a (1-e^2))", E, [], lambda: {"arcsec_per_century": Cv.mercury_arcsec_per_century()}, "The measured anomaly."),
            eq("curved_deflection", "CURVED: light deflection", "4M/b (1 + 15 pi M/(16 b))", "null geodesic integrated", E, ["b"], lambda b=2000.0: Cv.light_deflection_numeric(b), "Null geodesic against the formula."),
            eq("curved_solar_deflection", "CURVED: grazing the Sun", "4GM/(c^2 R) = 1.751 arcsec", "", E, [], lambda: {"arcsec": Cv.solar_deflection_arcsec()}, "The 1919 number."),
            eq("curved_clocks", "CURVED: GPS clock offsets", "GM/c^2 (1/R - 1/r) - v^2/2c^2", "microseconds per day", E, ["r_orbit"], lambda r_orbit=26561750.0: Cv.clock_rate_offsets(r_orbit), "Gravitational and velocity terms."),
            eq("curved_tidal", "CURVED: the tidal tensor", "R_trtr = -2M/r^3; xi'' = 2M/r^3 xi", "symbolic and by geodesic deviation", E, [],
               lambda: {"symbolic": {k: str(v) for k, v in Cv.tidal_component_schwarzschild().items()}, "numeric": Cv.geodesic_deviation_numeric()}, "Curvature seen as separation of free fallers."),
            eq("curved_horizons", "CURVED: horizon, photon sphere, ISCO", "2GM/c^2, 3GM/c^2, 6GM/c^2", "SI", E, ["solar_masses"],
               lambda solar_masses=1.0: {"r_s": Cv.schwarzschild_radius(solar_masses * R.GM_SUN), "photon_sphere": Cv.photon_sphere(solar_masses * R.GM_SUN), "isco": Cv.isco(solar_masses * R.GM_SUN),
                                         "hawking_T": Cv.hawking_temperature(solar_masses * R.GM_SUN / R.G)}, "Characteristic radii and the Hawking temperature."),
            eq("curved_kerr", "CURVED: Kerr horizons", "r+- = M +- sqrt(M^2 - a^2)", "geometric units", E, ["M", "a"], lambda M=1.0, a=0.9: Cv.kerr_horizons(M, a), "Horizons and ergosphere."),
            eq("curved_binary_pulsar", "CURVED: orbital decay of a binary pulsar", "Peters (1964)", "Hulse-Taylor elements", E, [], lambda: Cv.binary_pulsar_pdot(), "Energy lost to gravitational waves."),
            eq("curved_gw", "CURVED: gravitational waves in vacuum", "w^2 = k^2", "linearised Ricci of a TT plane wave", E, [], lambda: Cv.gravitational_wave_vacuum_check(), "The wave equation from the field equations."),
            # ---- tangent
            eq("tangent_equivalence", "TANGENT: the equivalence principle", "Gamma(p) -> 0, K(p) unchanged", "transformation law", E, ["r0"], lambda r0=10.0: Tg.equivalence_principle_report(r0), "The connection can be removed at a point; the curvature cannot."),
            eq("tangent_tidal", "TANGENT: the tidal ellipsoid", "radial +2M/r^3, tangential -M/r^3", "trace zero", E, ["r"], lambda r=10.0: Tg.tidal_ellipsoid(r), "What is left of gravity inside a freely falling lab."),
            # ---- metric
            eq("metric_friedmann", "METRIC: the Friedmann equation as a lapse constraint", "delta S / delta N = 0", "sympy Euler-Lagrange", E, [], lambda: Me.minisuperspace_friedmann(), "The action on the (a, N) slice of the space of metrics."),
            eq("metric_gauge", "METRIC: gauge invariance of the linearised curvature", "R^(1)[h + d xi] = R^(1)[h]", "explicit xi", E, [], lambda: Me.linearised_gauge_invariance(), "A diffeomorphism does not change linearised curvature."),
            # ---- crossings
            eq("cross_newton", "CROSSING curved -> Newton: the weak field", "R_00 = nabla^2 Phi", "arbitrary Phi(x,y,z)", E, [], lambda: Cr.newtonian_limit(), "Poisson's equation from the field equations."),
            eq("cross_euclid", "CROSSING curved -> Euclidean: horizon smoothness", "period = 8 pi M", "kappa = 1/4M", E, [], lambda: Cr.euclidean_horizon_period(), "Why the horizon has a temperature."),
            eq("cross_conversion_field", "CROSSING: the conversion field of the Witch's Hat as a 1+1 spacetime", "R = -2 v''/v", "wiki 140", I, [], lambda: Cr.hat_conversion_field(), "Reads wiki 140's conversion field v(q) as a metric: the hilltop zero is horizon-like with kappa = 1."),
            eq("cross_flat", "CROSSING curved -> Minkowski: the flat limit", "K -> 0 as M -> 0", "48 M^2/r^6", E, [], lambda: Cr.flat_limit_scaling(), "How the curved space hands over to the flat one."),
            # ---- bridge
            eq("bridge_prime_boost", "BRIDGE: the boost with Doppler factor p", "beta = (p^2-1)/(p^2+1), triple (p^2-1, 2p, p^2+1)", "rational velocity, Pythagorean triple", I, ["p"], lambda p=2: {k: str(v) for k, v in Br.prime_boost(p).items()},
               "ESTABLISHED arithmetic; the reading in terms of the Null Operator's prime shifts is INTERPRETATION."),
            eq("bridge_compose", "BRIDGE: composing prime boosts", "boost(p) o boost(q) = boost(pq)", "exact", I, ["p", "q"], lambda p=2, q=3: {k: str(v) for k, v in Br.compose_prime_boosts(p, q).items()}, "Lorentz composition along a line is multiplication of Doppler factors."),
            eq("bridge_factorise", "BRIDGE: factor a boost into prime boosts", "k = a/b -> exponents over primes", "unique factorisation", I, ["num", "den"],
               lambda num=12, den=5: {k: str(v) for k, v in Br.boost_factorisation(Fraction(num, den)).items()}, "Rapidity = sum e_p ln p."),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"relativity has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name, "text": repr(out["result"])[:4000]}

    def shell_commands(self) -> Dict[str, Any]:
        return {"rel_verify": Ck.verify, "rel_spaces": lambda: R.SPACES, "rel_jurisdiction": R.jurisdiction_check, "rel_crossings": R.crossing_table,
                "rel_boost": Mk.boost, "rel_thomas_wigner": Mk.thomas_wigner, "rel_curvature": Cv.curvature, "rel_schwarzschild": Cv.schwarzschild,
                "rel_orbit": Cv.orbit_precession_numeric, "rel_deflection": Cv.light_deflection_numeric, "rel_clocks": Cv.clock_rate_offsets,
                "rel_equivalence": Tg.equivalence_principle_report, "rel_friedmann": Me.minisuperspace_friedmann, "rel_prime_boost": Br.prime_boost,
                "rel_factorise_boost": Br.boost_factorisation}
