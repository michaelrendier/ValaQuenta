"""
ainulindale_engine.modules.angular_rank.tools
================================================
The 16D Oscilloscope -- Module Tools

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

The instrument that answers "is this signal internal or external" without
deciding anything, and "does this signal carry direction" without knowing
what language it is in. See maths.py.

Version: 0.1
"""

import math
from typing import Any, Dict, List

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    SEDENION_DIM, CALIBRATION, Datum,
    datum, is_datum, sight,
    embed_log_bands,
    occupancy, singular_spectrum, numerical_rank, orthonormal_span,
    common_direction, angular_residual, score_against_calibration,
    left_mul_matrix, null_space, verify_null_space,
    null_occupancy, null_occupancy_baseline,
    external_component, principal_angles, bearing,
    angular_report,
)


def _demo_zd() -> List[float]:
    """a = (e_1 + e_10)/sqrt(2) -- Assessor (1,2), strut 3. The worked example."""
    a = [0.0] * SEDENION_DIM
    a[1] = a[10] = 1.0 / math.sqrt(2.0)
    return a


class AngularRankModule(EquationModule):
    """The 16D Oscilloscope -- angular content and subspace occupancy."""

    @property
    def name(self):
        return "angular_rank"

    @property
    def display_name(self):
        return "The 16D Oscilloscope (Angular Rank)"

    @property
    def version(self):
        return "0.1"

    @property
    def description(self):
        return (
            "Measures three things about any signal embedded in the 16 "
            "sedenion dimensions, without knowing its language, its "
            "meaning, or its author: ANGULAR CONTENT (how much direction "
            "survives once the common mode is removed -- a scalar address "
            "scores exactly 0, the Phase 23 character encoder 0.0002, the "
            "phonetic face 0.402), OCCUPANCY AND RANK (which dimensions "
            "are populated, and the numerical rank of the accumulated "
            "trace), and NULL OCCUPANCY (how much energy lands in "
            "ker(L_a), the four dimensions a zero divisor annihilates). "
            "The third is the internal/external provenance test: the "
            "internal channel is a functional of its own state and cannot "
            "emit into the kernel of its own operator. The first is the "
            "language-agnostic stress test. THEY ARE ONE MEASUREMENT. "
            "Every entry point takes an immutable content-stamped Datum "
            "and refuses a live sequence -- measuring a span that the "
            "measured process is concurrently growing is "
            "iterate-while-modify, and it does not raise, it drifts until "
            "the instrument reports 'all quiet' forever. Mutation is not "
            "forbidden; it is DATED, via bearing() between two datums. "
            "Two mandatory nulls are built in: the isotropic baseline for "
            "null occupancy is exactly nullity/dim = 4/16 = 0.25, so a raw "
            "fraction near 0.25 is evidence of NOTHING and only the excess "
            "is reportable; and the calibration constants are "
            "EMBEDDING-SPECIFIC and do not transfer. Reproduces the "
            "published {4,8,4} split (nullity 4, rank 12, singular values "
            "sqrt2 x4 / 1 x8 / 0 x4) as a CHECK, not an input, and "
            "cross-checks L_a against box_kite's independent multiply()."
        )

    @property
    def confidence_floor(self):
        return "ESTABLISHED"

    # -- Formulary ---------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='verify_null_space',
                display='THE HONEST CHECK: nullity 4, rank 12, {sqrt2 x4, 1 x8, 0 x4}',
                latex=r'\ker(L_a),\ a = (e_1 + e_{10})/\sqrt{2},\ \dim\ker = 4',
                radian_form='agreement with Null-Space-of-the-Zero-Divisor.md is a CHECK, not an input',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: verify_null_space(),
                display_options=['text'],
            ),
            Equation(
                name='null_occupancy_baseline',
                display='THE MANDATORY NULL: isotropic energy in ker(L_a) is exactly 4/16',
                latex=r'\mathbb{E}\left[\frac{\|P_{\ker}x\|^2}{\|x\|^2}\right] = \frac{\dim\ker}{16} = 0.25',
                radian_form='a raw fraction near 0.25 is evidence of NOTHING -- report the excess',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: null_occupancy_baseline(_demo_zd()),
                display_options=['text'],
            ),
            Equation(
                name='angular_residual',
                display='ANGULAR CONTENT: sin of the angle to the common direction',
                latex=r'r = \left\langle \sqrt{1 - \langle \hat{u}, \hat{c}\rangle^2} \right\rangle',
                radian_form='0 = a scalar wearing 16 coordinates; >0 = real direction',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['datum'],
                compute=lambda datum: angular_residual(datum),
                display_options=['text'],
            ),
            Equation(
                name='calibration',
                display='THE PUBLISHED REFERENCES: 0.0000 / 0.0002 / 0.4020 (Phase 27.2)',
                latex=r'r_{\text{scalar}} = 0,\ r_{\text{char}} = 0.0002,\ r_{\text{phon}} = 0.402',
                radian_form='EMBEDDING-SPECIFIC (phonetic face). Does not transfer to other embeddings',
                confidence='ESTABLISHED',
                code_verified=True,
                params=[],
                compute=lambda: CALIBRATION,
                display_options=['text'],
            ),
            Equation(
                name='null_occupancy',
                display='PROVENANCE: energy landing in ker(L_a) -- what the internal channel cannot reach',
                latex=r'\frac{\|P_{\ker(L_a)}\, x\|^2}{\|x\|^2} - \frac{\dim\ker}{16}',
                radian_form='zero is AMBIGUOUS: no external signal OR ear wired through L_a',
                confidence='THEORETICAL',
                code_verified=True,
                params=['datum'],
                compute=lambda datum: null_occupancy(datum, _demo_zd()),
                display_options=['text'],
            ),
            Equation(
                name='external_component',
                display='Energy of a signal outside a FROZEN internal span',
                latex=r'1 - \frac{\|P_{\mathrm{span}(I)}\, s\|^2}{\|s\|^2}',
                radian_form='both arguments are datums -- the span cannot move under the measurement',
                confidence='THEORETICAL',
                code_verified=True,
                params=['signal', 'internal'],
                compute=lambda signal, internal: external_component(signal, internal),
                display_options=['text'],
            ),
            Equation(
                name='bearing',
                display='THE DRIFT METER: how far the span moved between two datums',
                latex=r'\theta_{\max}(\mathrm{span}_{t_0}, \mathrm{span}_{t_1}),\ \Delta\,\mathrm{rank}',
                radian_form='mutation is permitted and DATED; bounded (Phase 27.3) vs accumulating = seizure',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['before', 'after'],
                compute=lambda before, after: bearing(before, after),
                display_options=['text'],
            ),
            Equation(
                name='numerical_rank',
                display='Rank of the accumulated trace, with its tolerance',
                latex=r'\mathrm{rank}_\tau(A) = \#\{\sigma_i > \tau\},\ \tau = \max(n,d)\,\epsilon\,\sigma_1',
                radian_form='a rank without its tolerance is not a measurement',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['datum'],
                compute=lambda datum: numerical_rank(datum),
                display_options=['text'],
            ),
            Equation(
                name='occupancy',
                display='Per-dimension energy fraction and participation ratio',
                latex=r'\mathrm{PR} = 1 \Big/ \sum_k f_k^2',
                radian_form='PR = effective number of dimensions actually carrying the signal',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['datum'],
                compute=lambda datum: occupancy(datum),
                display_options=['text'],
            ),
            Equation(
                name='embed_log_bands',
                display='THE LANGUAGE-AGNOSTIC EMBEDDING: 16 log-spaced band energies',
                latex=r'v_k = \sum_{f \in [f_k, f_{k+1})} P(f),\quad f_k \text{ geometric}',
                radian_form='no phoneme inventory, no lexicon, no human-bandwidth assumption',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['power_spectrum'],
                compute=lambda power_spectrum: embed_log_bands(power_spectrum),
                display_options=['text'],
            ),
            Equation(
                name='angular_report',
                display='THE STRESS TEST, one card -- every entry stamped with its datum',
                latex=r'\{r,\ \mathrm{rank},\ \mathrm{PR},\ \ker\text{-excess}\}\ @\ \mathrm{stamp}',
                radian_form='no measurement is reportable without its datum',
                confidence='THEORETICAL',
                code_verified=True,
                params=['datum'],
                compute=lambda datum: angular_report(datum, a=_demo_zd()),
                display_options=['text'],
            ),
            Equation(
                name='null_space',
                display='ker(L_a) for an arbitrary sedenion a',
                latex=r'\ker(L_a) = \{v : a \cdot v = 0\}',
                radian_form='L_a built from box_kite\'s CD table; cross-checked against multiply()',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['a'],
                compute=lambda a: null_space(a),
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
        return {'text': self._format_text(equation_name, self.run(equation_name, params))}

    def _format_text(self, equation_name: str, result: Dict) -> str:
        eq = result['equation']
        r = result['result']
        if isinstance(r, dict):
            body = '\n'.join(f"      {k:<28} {v}" for k, v in r.items()
                             if not isinstance(v, (list, dict)))
            summary = '\n' + body
        elif isinstance(r, list):
            summary = f"{r[:10]}{' ...' if len(r) > 10 else ''}  (n={len(r)})"
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
            'verify':    lambda: verify_null_space(),
            'baseline':  lambda a=None: null_occupancy_baseline(a or _demo_zd()),
            'snap':      lambda v, label='unlabelled': datum(v, label),
            'ang':       lambda e: angular_residual(e),
            'score':     lambda r: score_against_calibration(r),
            'calib':     lambda: CALIBRATION,
            'rank':      lambda e: numerical_rank(e),
            'occ':       lambda e: occupancy(e),
            'spec':      lambda e: singular_spectrum(e),
            'common':    lambda e: common_direction(e),
            'ker':       lambda a=None: null_space(a or _demo_zd()),
            'kerocc':    lambda e, a=None: null_occupancy(e, a or _demo_zd()),
            'ext':       lambda s, i: external_component(s, i),
            'bear':      lambda b, a: bearing(b, a),
            'sight':     lambda held, live: sight(held, live),
            'angles':    lambda P, Q: principal_angles(P, Q),
            'lmul':      lambda a: left_mul_matrix(a),
            'bands':     lambda p, sr=96000.0: embed_log_bands(p, sample_rate=sr),
            'report':    lambda e, a=None: angular_report(e, a=a or _demo_zd()),
        }

    def on_register(self, registry) -> None:
        pass
