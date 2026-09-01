"""
ainulindale_engine.modules.emerger.tools
==========================================
THE EMERGER -- Sedenion Bracketing & Firing Order.  Module Tools.

Implements the EquationModule registry contract:
    formulary(), run(), viewer_data(), shell_commands()

A dynamic permutative bracketer over the imaginary part of a Cayley-Dickson
algebra.  The real component e_0 is the fixed anchor -- the tilt to the i
axis -- never bracketed, always the reference each group is paired against.
Each imaginary group + the anchor spans a domain (C / H / O / FRAGMENT);
the order the groups are approached (the firing order) is load-bearing and
can be set canonically, by sigma_RB's tilt-phase, or by any permutation.

The Emerger is the ascent-dual of Generational Lineage: descent = what
built this (differentiate down, writing); ascent = what emerges and in
what order (integrate up, reading).

Version: 0.1
"""
from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation
from .maths import (
    SEDENION_DIM, basis, _add,
    cd_mul, cd_conj, norm_sq, left_matrix, mat_rank,
    is_zero_divisor, on_zd_equator,
    sigma_rb, firing_phase, firing_order,
    STANDARD_BRACKETINGS, CANONICAL_ORDER, BRACKET_ROLE,
    domain_of, gain_class, legal_orders,
    emerge, scale_partitions, verify, lineage_report,
)


def _parse_vec(v) -> tuple:
    """Accept a list/tuple of 16 numbers, or a name like 'e1+e10' / 'e0'."""
    if isinstance(v, (list, tuple)):
        return tuple(v)
    if isinstance(v, str):
        acc = [0] * SEDENION_DIM
        for tok in v.replace("-", "+-").split("+"):
            tok = tok.strip()
            if not tok:
                continue
            sign = -1 if tok.startswith("-") else 1
            tok = tok.lstrip("-")
            if tok.startswith("e"):
                acc[int(tok[1:])] += sign
            else:
                acc[0] += sign * float(tok)
        return tuple(acc)
    raise ValueError(f"cannot parse vector: {v!r}")


class EmergerModule(EquationModule):
    """The Emerger -- sedenion bracketing & firing order of emergence."""

    @property
    def name(self):
        return "emerger"

    @property
    def display_name(self):
        return "The Emerger (Sedenion Bracketing & Firing Order)"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "A dynamic permutative bracketer for Cayley-Dickson algebras. "
            "The real component e_0 is the fixed anchor -- the tilt to the "
            "i axis -- never bracketed; every imaginary group is paired "
            "against it so the bracket-vs-real relationship stays visible. "
            "A BRACKETING is an ordered partition of the imaginary indices "
            "{1..15}; each group + the anchor spans span({e_0} u G), "
            "classified by closure as C / H / O / FRAGMENT (the fragment "
            "is where zero divisors live). Five canonical brackets: {1:15} "
            "grades the algebra (Re, N, conj, inverse); {2:14} is the "
            "pointer plane (e_0, e_8) carrying Omega_ZS; {8:8} is the CD "
            "double (J_red/J_blue, the ZD equator, the J_2 L-vs-R "
            "asymmetry); {4:4:4:4} is four SU(2) phases and the sigma_RB "
            "tilt/axis (Sigma_tilt = net work around the loop, = 0 iff "
            "sigma=1/2); {4:8:4} is the gain spectrum 0/1/sqrt2. The FIRING "
            "ORDER -- the order groups are approached -- is load-bearing: "
            "each bracket is conditioned on the ones before it. It can be "
            "canonical (dependency), sigma_RB-phased (Sigma_tilt rotates "
            "the entry point into the 12-step precession, 4 d* faces : 3 "
            "Lambert-W faces), or any permutation (legality reported, not "
            "enforced -- a finding: some sigma_RB phases select a "
            "non-dependency-legal order). ZD tests are exact "
            "(rank-deficiency of L_x; equator = purely imaginary + "
            "norm-balanced across the CD-double boundary). The exact ZD "
            "geometry is box_kite's PSL(2,7); G_2 is the continuous "
            "blow-up. The Emerger is the ascent-dual of Generational "
            "Lineage: descent tracks what built a thing, the Emerger runs "
            "what emerges and in what order -- reading, spectroscopy, "
            "factoral decomposition."
        )

    @property
    def confidence_floor(self):
        return "THEORETICAL"

    @property
    def process_description(self):
        return (
            "Brackets a Cayley-Dickson 16-vector five ways ({1:15} {2:14} {8:8} "
            "{4:4:4:4} {4:8:4}) with e0 held as the fixed anchor, classifies each "
            "group as C/H/O/FRAGMENT by closure, and walks the brackets in a "
            "sigma_RB-phased firing order, reporting what each grouping lets "
            "emerge and in what order -- the ascent dual of Generational Lineage.")

    # -- Formulary -------------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name="verify",
                display="THE HONEST CHECKS: 14 exact self-checks + legal firing orders",
                latex=r"\text{Sigma\_axis}=0;\ e_1{+}e_{10}\in\mathrm{ZD}\cap\mathrm{equator};\ "
                      r"\dim_{\!C/H/O}",
                radian_form="all derived from the CD table; a mismatch is a bug here, not a discovery",
                confidence="ESTABLISHED",
                code_verified=True,
                params=[],
                compute=lambda: verify(),
                display_options=["text"],
                process=(
                    "Runs 14 exact self-checks of the bracketing algebra straight from the CD table (Sigma_axis vanishes, e1+e10 is a zero divisor on the equator, domain_of classifies C/H/O/FRAGMENT, 4 of 120 firing orders are dependency-legal); a mismatch is a code fault, not a result."),
            ),
            Equation(
                name="emerge",
                display="THE READOUT: run x through the 5 brackets in firing order",
                latex=r"x \mapsto \big[(\mathrm{bracket},\ \mathrm{domain},\ "
                      r"\mathrm{emergent})\big]_{\text{firing order}}",
                radian_form="each bracket conditioned on the ones fired before it; "
                            "order set by sigma_RB tilt-phase",
                confidence="THEORETICAL",
                code_verified=True,
                params=["x", "mode"],
                compute=lambda x="e1+e10", mode="sigma_rb": emerge(_parse_vec(x), mode=mode),
                display_options=["text"],
                process=(
                    "Takes a 16-vector, computes its sigma_RB tilt-phase to fix the entry bracket, then walks the five brackets in that firing order, each step conditioned on the ones before it, reporting what each grouping exposes."),
            ),
            Equation(
                name="firing_order",
                display="THE CLOCK: sigma_RB tilt-phase -> entry bracket in the 12-step precession",
                latex=r"\Sigma\mathrm{tilt} \to \tau \to \lfloor 12\tau\rfloor \bmod 5",
                radian_form="gcd(12,5)=1 so the 12-phase clock cycles all five brackets; "
                            "4 d* faces : 3 Lambert-W faces",
                confidence="THEORETICAL",
                code_verified=True,
                params=["x", "mode"],
                compute=lambda x="e1+e10", mode="sigma_rb": firing_order(_parse_vec(x), mode=mode),
                display_options=["text"],
                process=(
                    "Computes Sigma_tilt from the 16-vector, squashes it rationally into the 12-step precession (4 d* faces : 3 Lambert-W faces), and reads off which bracket fires first and the resulting order."),
            ),
            Equation(
                name="sigma_rb",
                display="tilt (Scale / Perfect Perturbation) and axis (Flow); Sigma_axis = 0 identically",
                latex=r"s[k]=\psi[k]\,\overline{\psi[k\oplus4]};\ "
                      r"\mathrm{tilt}=\mathrm{Re}\,s,\ \mathrm{axis}=\mathrm{Im}\,s",
                radian_form="Sigma_tilt = 0  <=>  sigma = 1/2  (Oblique-Gear T4); Sigma_axis = 0 by T1",
                confidence="DERIVED" if False else "THEORETICAL",
                code_verified=True,
                params=["x"],
                compute=lambda x="e1+e10": {
                    k: (float(v) if not isinstance(v, tuple) else [float(c) for c in v])
                    if not isinstance(v, bool) else v
                    for k, v in sigma_rb(_parse_vec(x)).items()},
                display_options=["text"],
                process=(
                    "Forms psi[k] = x[k] + i*x[k+8], multiplies each by the conjugate of its XOR-4 partner, and splits the result into tilt (Re, the Scale channel) and axis (Im, the Flow channel); Sigma_axis is zero identically, Sigma_tilt is zero exactly on sigma = 1/2."),
            ),
            Equation(
                name="domain_of",
                display="CLASSIFY a bracket group: C / H / O / FRAGMENT (by closure)",
                latex=r"\mathrm{span}(\{e_0\}\cup G):\ |G|{=}1{\to}\mathbb{C},\ 3{\to}\mathbb{H},\ "
                      r"7{\to}\mathbb{O},\ \text{else FRAGMENT}",
                radian_form="closed under its own generator products <=> a subalgebra; else the "
                            "fragment where zero divisors live",
                confidence="ESTABLISHED",
                code_verified=True,
                params=["indices"],
                compute=lambda indices=(1, 2, 3): domain_of(frozenset(indices)),
                display_options=["text"],
                process=(
                    "Takes a set of imaginary indices, adjoins e0, and tests closure under the CD product to classify the span as C, H, O, or a FRAGMENT (a subspace that is not a subalgebra)."),
            ),
            Equation(
                name="scale_partitions",
                display="THE PERMUTATION SPACE: partitions of {1..15} into C/H/O-sized groups",
                latex=r"\{1,3,7\}\text{-compositions of }15;\ \text{which close, which fragment}",
                radian_form="the different brackets of different scales the permutative bracketer "
                            "moves between",
                confidence="ESTABLISHED",
                code_verified=True,
                params=[],
                compute=lambda: scale_partitions(),
                display_options=["text"],
                process=(
                    "Enumerates the ways to partition the 15 imaginary indices into C/H/O-sized groups and reports, for a contiguous representative of each shape, which groups close into subalgebras and which are fragments."),
            ),
            Equation(
                name="legal_orders",
                display="THE DEPENDENCY LATTICE: firing orders that respect emergence prerequisites",
                latex=r"\{1{:}15\}\prec\{2{:}14\},\{8{:}8\},\{4{:}8{:}4\};\ "
                      r"\{8{:}8\}\prec\{4{:}4{:}4{:}4\}\prec\{4{:}8{:}4\}",
                radian_form="4 of 120 permutations are dependency-legal; the canonical order is one",
                confidence="THEORETICAL",
                code_verified=True,
                params=[],
                compute=lambda: {"legal_orders": legal_orders(),
                                 "count": len(legal_orders())},
                display_options=["text"],
                process=(
                    "Enumerates the permutations of the five brackets that respect the emergence prerequisites and returns the 4 that survive the dependency lattice."),
            ),
            Equation(
                name="lineage_report",
                display="ASCENT DUAL: per bracket -- tier, what it descends from, what it emerges",
                latex=r"\text{emerger} = \text{ascent}(\text{tower});\ "
                      r"\text{lineage} = \text{descent}(\text{tower})",
                radian_form="reading = integrate up = the Emerger; writing = differentiate down = lineage",
                confidence="THEORETICAL",
                code_verified=True,
                params=[],
                compute=lambda: lineage_report(),
                display_options=["text"],
                process=(
                    "Lists, per bracket, its confidence tier, what it descends from, and what it lets emerge -- the ascent-side table dual to Generational Lineage's descent."),
            ),
        ]

    # -- run ----------------------------------------------------------------

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eqs = {e.name: e for e in self.formulary()}
        if equation_name not in eqs:
            raise KeyError(f"emerger has no equation '{equation_name}'")
        eq = eqs[equation_name]
        result = eq.compute(**{k: v for k, v in params.items() if k in eq.params}) \
            if params else eq.compute()
        return {"result": result, "equation": eq, "params": params}

    # -- viewer_data ------------------------------------------------------------

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        out = self.run(equation_name, params)
        return {"mode": display_mode, "equation": equation_name,
                "text": repr(out["result"])}

    # -- shell_commands ------------------------------------------------------

    def shell_commands(self) -> Dict[str, Any]:
        return {
            "emerge": lambda x="e1+e10", mode="sigma_rb": emerge(_parse_vec(x), mode=mode),
            "firing_order": lambda x="e1+e10": firing_order(_parse_vec(x)),
            "emerger_verify": verify,
        }
