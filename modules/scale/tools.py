"""
ainulindale_engine.modules.scale.tools
=========================================
THE SCALE -- Module Tools

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

Decompositional analysis, forwards and backwards -- SCALE (tier-0,
alongside ADD and SIGN) pulled out of a quantity and named as its own
object. See maths.py for the full derivation and honest boundaries.

Version: 0.1
"""

from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    polar_decompose, polar_recompose, verify_polar_round_trip,
    scale_invariance_under_self_rescale,
    mobius_fold, scale_factor, verify_no_caustic,
    cross_ratio, verify_cross_ratio_is_scale_blind,
    two_ring_point, custom_ring_chart,
    fold_is_log_tanh, unfold_is_arctanh_exp, verify_fold_unfold_round_trip,
    verify_locally_square,
    ProcessOperator, pathway_decompose,
)


def _demo_rsa_pathway() -> Dict[str, Any]:
    """p=61, q=53 -- real, small, pedagogical primes (verified prime by
    trial division at build time, not recalled). The control case for
    process decomposition: m1/m2 are independent, h combines both, the
    final value depends on h AND m2 again -- a genuine fan-out a linear
    chain cannot represent."""
    p, q, e_pub = 61, 53, 17
    n, phi = p * q, (p - 1) * (q - 1)
    d = pow(e_pub, -1, phi)
    m = 65
    c = pow(m, e_pub, n)
    dP, dQ, qInv = d % (p - 1), d % (q - 1), pow(q, -1, p)
    ops = [
        ProcessOperator('m1', lambda cc: pow(cc, dP, p), depends_on=('input',)),
        ProcessOperator('m2', lambda cc: pow(cc, dQ, q), depends_on=('input',)),
        ProcessOperator('h', lambda m1, m2: (qInv * (m1 - m2)) % p,
                        depends_on=('m1', 'm2')),
        ProcessOperator('m_out', lambda h, m2: m2 + h * q, depends_on=('h', 'm2')),
    ]
    return pathway_decompose(c, ops, output_name='m_out')


class ScaleModule(EquationModule):
    """THE SCALE -- decompositional analysis, forwards and backwards."""

    @property
    def name(self):
        return "scale"

    @property
    def display_name(self):
        return "The Scale (Decompositional Analysis, Forwards and Backwards)"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "SCALE is tier-0 (ADD, SCALE, SIGN) -- this module pulls it out "
            "of a quantity and names what is left over, both directions. "
            "polar_decompose/recompose is the exact forward/backward pair "
            "for ONE point (r=scale, theta=scale-blind under self-"
            "rescaling, verified round-trip). The two-ring Mobius fold "
            "(mobius_fold/scale_factor) has its OWN scale-blind object, a "
            "different and harder question: the raw angle does NOT "
            "survive the fold (a rejected candidate, kept in the record), "
            "but the cross-ratio of any four points is exactly invariant "
            "under every choice of anchor -- verified directly, not "
            "asserted. pathway_decompose applies the same forward/backward "
            "discipline to a real algorithm (RSA CRT-decrypt as the "
            "control case), representing genuine dependency fan-out "
            "rather than forcing a linear chain."
        )

    @property
    def confidence_floor(self):
        return "ESTABLISHED"

    # -- Formulary ---------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='polar_round_trip',
                display='THE RETURN PATH: recompose(*decompose(Z)) == Z, exactly',
                latex=r'Z = r\,e^{i\theta},\quad r=|Z|,\ \theta=\arg(Z)',
                radian_form='r is the scale (ordinal); theta is scale-blind under Z -> lambda*Z, lambda>0',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: verify_polar_round_trip(),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='scale_invariance_under_self_rescale',
                display='theta is unchanged as Z is rescaled by any positive real',
                latex=r'\arg(\lambda Z) = \arg(Z),\quad \lambda > 0',
                radian_form='the narrow, exact sense in which the angle is scale-blind BEFORE any fold',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['Z'],
                compute=lambda Z: scale_invariance_under_self_rescale(Z),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='scale_factor',
                display='THE FLATTENING ARTIFACT: |dGamma/dZ|, exact',
                latex=r'\left|\frac{d\Gamma}{dZ}\right| = \left|\frac{2Z_0}{(Z+Z_0)^2}\right|',
                radian_form='the local area-scaling of the two-ring fold -- what a flat reading loses',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['Z', 'Z0'],
                compute=lambda Z, Z0: scale_factor(Z, Z0),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='verify_no_caustic',
                display='NO TRUE CAUSTIC: the fold\'s derivative never vanishes, only diverges at one pole',
                latex=r'\frac{d\Gamma}{dZ} \neq 0\ \forall\ Z \neq -Z_0',
                radian_form='crowding-toward-infinity at one point is not an envelope/fold singularity',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: verify_no_caustic(),
                display_options=['text'],
            ),
            Equation(
                name='cross_ratio_is_scale_blind',
                display='THE SCALE INVARIANT: cross-ratio survives every anchor; the angle does not',
                latex=r'(z_1,z_2;z_3,z_4) = \frac{(z_1-z_3)(z_2-z_4)}{(z_1-z_4)(z_2-z_3)}',
                radian_form='a property of a relationship among FOUR points, not of any one point',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: verify_cross_ratio_is_scale_blind(),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='two_ring_point',
                display='THE TWO-RING INSTRUMENT: any pair of readings, folded',
                latex=r'Z = \mathrm{ring}_1 + i\cdot\mathrm{ring}_2,\quad \Gamma = \mathrm{mobius\_fold}(Z, Z_0)',
                radian_form='ring1/ring2 mean whatever the caller defines -- not constrained to impedance',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['ring1', 'ring2', 'Z0'],
                compute=lambda ring1, ring2, Z0: two_ring_point(ring1, ring2, Z0),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='fold_unfold_round_trip',
                display='THE MASTER IDENTITY: Gamma=tanh(log(Z/Z0)/2), exact, any complex Z',
                latex=r'\Gamma = \tanh\!\left(\tfrac{1}{2}\ln\tfrac{Z}{Z_0}\right),\quad '
                      r'Z = Z_0\,e^{2\,\mathrm{artanh}(\Gamma)}',
                radian_form='folding IS log-then-bound; unfolding IS unbound-then-exp -- not a metaphor',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: verify_fold_unfold_round_trip(),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='locally_square',
                display='AUTOMATIC, NOT CONDITIONAL: any two rings give locally-square cells',
                latex=r'|\partial_{r_1}\Gamma| = |\partial_{r_2}\Gamma|,\quad '
                      r'\angle(\partial_{r_1}\Gamma,\ \partial_{r_2}\Gamma) = 90^\circ',
                radian_form='a property of the fold being holomorphic in Z, independent of what ring1/ring2 mean',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['Z', 'Z0'],
                compute=lambda Z, Z0: verify_locally_square(Z, Z0),
                display_options=['text', 'complex_plane'],
            ),
            Equation(
                name='custom_ring_chart_demo',
                display='USER-DEFINED RINGS: any two functions of any object, folded',
                latex=r'Z = r_1(\mathrm{obj}) + i\,r_2(\mathrm{obj})',
                radian_form='ring1/ring2 are arbitrary caller-supplied callables -- not built-in special cases',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['obj', 'ring1_fn', 'ring2_fn', 'Z0'],
                compute=lambda obj, ring1_fn, ring2_fn, Z0: custom_ring_chart(obj, ring1_fn, ring2_fn, Z0),
                display_options=['text'],
            ),
            Equation(
                name='rsa_pathway_control',
                display='PROCESS DECOMPOSITION CONTROL CASE: RSA CRT-decrypt, a genuine fan-out',
                latex=r'm_1(c),\ m_2(c)\ \text{siblings};\ h(m_1,m_2);\ m(h,m_2)',
                radian_form='m2 feeds BOTH h and the final m -- not representable as a linear chain',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: _demo_rsa_pathway(),
                display_options=['text'],
            ),
        ]

    # -- Run ---------------------------------------------------------------

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None:
            raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    # -- Viewer data -------------------------------------------------------

    def viewer_data(self, equation_name: str, params: Dict[str, Any],
                    display_mode: str) -> Dict[str, Any]:
        return {'text': self._format_text(self.run(equation_name, params))}

    def _format_text(self, result: Dict) -> str:
        eq = result['equation']
        r = result['result']
        if isinstance(r, dict):
            body = '\n'.join(f"      {k:<28} {v}" for k, v in r.items()
                             if not isinstance(v, (list, dict, tuple)))
            summary = '\n' + body
        else:
            summary = r
        return (
            f"  {eq.display}\n"
            f"  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n"
            f"  Radian form: {eq.radian_form}\n"
            f"  Result: {summary}"
        )

    # -- Shell commands ----------------------------------------------------

    def shell_commands(self) -> Dict[str, Any]:
        return {
            'polar':    lambda Z: polar_decompose(Z),
            'unpolar':  lambda r, theta: polar_recompose(r, theta),
            'roundtrip': lambda: verify_polar_round_trip(),
            'fold':     lambda Z, Z0: mobius_fold(Z, Z0),
            'sf':       lambda Z, Z0: scale_factor(Z, Z0),
            'nocaustic': lambda: verify_no_caustic(),
            'cr':       lambda z1, z2, z3, z4: cross_ratio(z1, z2, z3, z4),
            'crblind':  lambda: verify_cross_ratio_is_scale_blind(),
            'tworing':  lambda r1, r2, Z0: two_ring_point(r1, r2, Z0),
            'custom':   lambda obj, r1fn, r2fn, Z0: custom_ring_chart(obj, r1fn, r2fn, Z0),
            'fold_log': lambda Z, Z0: fold_is_log_tanh(Z, Z0),
            'unfold_exp': lambda G, Z0: unfold_is_arctanh_exp(G, Z0),
            'roundtrip2': lambda: verify_fold_unfold_round_trip(),
            'square':   lambda Z, Z0: verify_locally_square(Z, Z0),
            'rsapath':  lambda: _demo_rsa_pathway(),
        }

    def on_register(self, registry) -> None:
        pass
