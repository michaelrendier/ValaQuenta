"""
ainulindale_engine.modules.archimedes_screw.tools
====================================================
The Archimedes Screw -- Module Tools

Implements the EquationModule registry contract.
Provides: formulary, run(), viewer_data(), shell_commands()

0_RB is the water. This module is the screw -- the machine that lifts it.
The screw is the logarithm: rotation into lift, one quantised pitch per
turn, ln p per prime, reversible as a turbine.

Four search terms (Ordinal Value, Zeta Index Value, Number of Digits,
Total Spaces Between) are four coordinates on one axis u = ln x. The
explicit formula binds them. See maths.py for the full statement.

Version: 0.3
"""

from typing import Dict, List, Any

from ...engine.registry import EquationModule, Equation, CONFIDENCE
from .maths import (
    lambert_w, screw_pitch, u_axis, digits_of,
    li, prime_count_log10, nth_prime_estimate,
    zero_count_smooth, zero_height_lambert, zero_height, zeros_upto,
    mean_gap, total_spaces, gap_at_zero_scale,
    von_mangoldt, chebyshev_psi_exact, chebyshev_psi_explicit,
    leaf_drops, tone, tone_sum, interference_profile,
    clean_path_L, zero_sum, l_io_decomposition,
    lpf, gpf, fall_height, discovery_height, smoothness_u,
    dickman_rho, gpf_table, psi_smooth, harvest, harvest_curve,
    semiprime_harvest, fall_split, domain_ladder,
    mobius, mertens, mertens_envelope, sieve_extinction,
    amplitude_envelope, envelope_ratio,
    kronecker, fundamental_discriminant, splitting_type,
    splitting_vector, ramified_primes,
    screw_coordinates, shake_order,
    OMEGA_ZS, ZEROS_KNOWN,
)


class ArchimedesScrewModule(EquationModule):
    """The Archimedes Screw -- prime coordinate engine on the axis u = ln x."""

    @property
    def name(self):
        return "archimedes_screw"

    @property
    def display_name(self):
        return "The Archimedes Screw (Prime Coordinate Engine)"

    @property
    def version(self):
        return "0.3"

    @property
    def description(self):
        return (
            "The machine that does the work, distinct from the medium it "
            "lifts: 0_RB is the water, the screw is the logarithm. Converts "
            "rotation into lift, one pitch of ln p per prime. Provides the "
            "four-coordinate search-term interface (Ordinal Value, Zeta "
            "Index Value, Number of Digits, Total Spaces Between) on the "
            "single axis u = ln x, bound by the von Mangoldt explicit "
            "formula. Chebyshev psi jumps by exactly ln p at x = p -- the "
            "leaf-drop event's magnitude IS the prime. Includes the "
            "Lambert-W inverse of the zero-counting function (the same W "
            "whose fixed point W(1) = OMEGA_ZS pins sigma = 1/2), the "
            "amplitude-envelope form of RH, and the N-specific "
            "ramification leg in Q(sqrt N) where the Euler factor "
            "degenerates at exactly the factors of N. Also carries the "
            "L_(I|O) slot decomposition: Chebyshev psi is the counterpart "
            "of L_(I|O) (the actual bent path), the main term x is L (the "
            "clean path of least primes), and the newly named zero_sum is "
            "the counterpart of the Fermat/lensing potential -- the bend. "
            "v0.2 adds the composite side the screw was blind to: the leaf "
            "falls at gpf(N) (14 = 2*7 falls at 7, not at 2), the fall-time "
            "distribution is Dickman rho in the coordinate u = lnN/ln(gpf N), "
            "the harvest at step p is Psi(X/p, p) in closed form, and "
            "fall_split reports the imbalance delta that is a semiprime's "
            "entire hidden content -- collapsing to zero for balanced RSA, "
            "which is why the two fall events coincide there. v0.3 adds the "
            "NEGATIVE SPACE psi had no counterpart for: mu is the exclusion "
            "operator, M(x)=SUM mu(n) is psi's mirror, RH on that side is "
            "M(x)=O(x^(1/2+eps)) -- the same 1/2 -- and sieve_extinction gives "
            "the THREE motions: grown (zeta), extinct at lpf (negative), "
            "identified at gpf (bulk). domain_ladder """
            "settles what 'the domain' means: not 2..N but 2..sqrt(N), only """
            "the primes in it, and restricting to exactly-size primes buys """
            "exactly ONE BIT because half of all primes below any bound live """
            "in the top octave. The only target that matters is GNFS at 2^112."
        )

    @property
    def confidence_floor(self):
        return "THEORETICAL"

    # -- Formulary ---------------------------------------------------------

    def formulary(self) -> List[Equation]:
        return [
            Equation(
                name='screw_coordinates',
                display='Search-term interface: four coordinates, one axis',
                latex=r'u = \ln x;\quad \{d,\ n,\ k,\ \bar g\} \leftrightarrow u',
                radian_form='enter on magnitude|digits|ordinal|zeta_index, leave on all',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['term', 'value'],
                compute=lambda term, value: screw_coordinates(term, value),
                display_options=['text'],
            ),
            Equation(
                name='screw_pitch',
                display='One turn of the screw = one prime = lift of ln p',
                latex=r'\Lambda(p^m) = \ln p',
                radian_form='pitch(p) = ln p  (the exact jump of psi at x=p)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['p'],
                compute=lambda p: screw_pitch(p),
                display_options=['text'],
            ),
            Equation(
                name='chebyshev_psi_explicit',
                display='THE BINDING EQUATION: explicit formula on the screw axis',
                latex=(r'\psi(e^u) = e^u - 2e^{u/2}\sum_k '
                       r'\frac{\cos(\gamma_k u - \arg\rho_k)}{|\rho_k|} '
                       r'- \ln 2\pi - \tfrac12\ln(1-e^{-2u})'),
                radian_form=('psi(x) = x - 2*sqrt(x)*SUM cos(gamma_k*ln x - arg rho_k)/|rho_k| '
                             '- ln(2pi) - 0.5*ln(1-x^-2)'),
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x', 'zeros'],
                compute=lambda x, zeros=None: chebyshev_psi_explicit(x, zeros),
                display_options=['text'],
            ),
            Equation(
                name='zero_sum',
                display='THE PRIME-SIDE FERMAT POTENTIAL — the bend',
                latex=r'\sum_\rho \frac{x^\rho}{\rho} = 2\sqrt{x}\sum_k \frac{\cos(\gamma_k u - \arg\rho_k)}{|\rho_k|}',
                radian_form='zero_sum(x) = 2*sqrt(x)*SUM cos(gamma_k*ln x - arg rho_k)/|rho_k|',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x', 'zeros'],
                compute=lambda x, zeros=None: zero_sum(x, zeros),
                display_options=['text'],
            ),
            Equation(
                name='clean_path_L',
                display='L — the clean path: "the path of least primes", computed',
                latex=r'L(x) = x \quad \text{(the pole term; no zero contributes)}',
                radian_form='L(x) = x  — what psi would be with no zeros at all',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x'],
                compute=lambda x: clean_path_L(x),
                display_options=['text'],
            ),
            Equation(
                name='l_io_decomposition',
                display='The three L_(I|O) slots by role: L, psi_bend, L_IO',
                latex=r'L_{(I|O)} = L - \psi_{\text{bend}} + \text{trivial}',
                radian_form='psi_Cheb <-> L_(I|O);  x <-> L;  zero_sum <-> psi_Fermat',
                confidence='THEORETICAL',
                code_verified=True,
                params=['x', 'zeros'],
                compute=lambda x, zeros=None: l_io_decomposition(x, zeros),
                display_options=['text'],
            ),
            Equation(
                name='chebyshev_psi_exact',
                display='psi(x) by sieve -- the ground truth the tones rebuild',
                latex=r'\psi(x) = \sum_{p^m \le x} \ln p',
                radian_form='psi(x) = sum of ln p over all prime powers <= x',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x'],
                compute=lambda x: chebyshev_psi_exact(x),
                display_options=['text'],
            ),
            Equation(
                name='shake_order',
                display='The shake order: every leaf-drop, in sequence, with its prime',
                latex=r'\{(n,\ \Lambda(n)) : n \le x,\ \Lambda(n) \neq 0\}',
                radian_form='drops = [(n, ln p)]; jump height IS the prime, in log form',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x', 'zeros'],
                compute=lambda x, zeros=None: shake_order(x, zeros),
                display_options=['text'],
            ),
            Equation(
                name='fall_height',
                display='WHEN THE LEAF FALLS: u_fall = ln(gpf N)',
                latex=r'u_{\text{fall}}(N) = \ln\big(\mathrm{gpf}\,N\big)',
                radian_form='fall_height(N) = ln(greatest prime factor of N); 14 falls at 7',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n'],
                compute=lambda n: fall_height(n),
                display_options=['text'],
            ),
            Equation(
                name='discovery_height',
                display='Where the first strike lands: ln(lpf N)',
                latex=r'u_{\text{disc}}(N) = \ln\big(\mathrm{lpf}\,N\big)',
                radian_form='discovery_height(N) = ln(least prime factor); 14 is struck at 2',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n'],
                compute=lambda n: discovery_height(n),
                display_options=['text'],
            ),
            Equation(
                name='smoothness_u',
                display='The Dickman coordinate: u = ln N / ln(gpf N)',
                latex=r'u = \frac{\ln N}{\ln(\mathrm{gpf}\,N)}',
                radian_form='u = 1 for a prime, u = 2 for a balanced semiprime (exponent 1/2)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n'],
                compute=lambda n: smoothness_u(n),
                display_options=['text'],
            ),
            Equation(
                name='dickman_rho',
                display='THE FALL-TIME DISTRIBUTION: Dickman rho(u)',
                latex=r'u\rho\,\!\'(u) = -\rho(u-1),\quad \Psi(x,x^{1/u}) \sim x\,\rho(u)',
                radian_form='rho(1)=1; rho(2)=1-ln2=0.3068528; rho(3)=0.0486083',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['u'],
                compute=lambda u: dickman_rho(u),
                display_options=['text'],
            ),
            Equation(
                name='harvest',
                display='THE HARVEST: leaves falling at sieve step p',
                latex=r'\#\{n \le X : \mathrm{gpf}\,n = p\} = \Psi(X/p,\ p)',
                radian_form='harvest(X,p) = psi_smooth(X//p, p) — closed form, no search',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['X', 'p'],
                compute=lambda X, p: harvest(X, p),
                display_options=['text'],
            ),
            Equation(
                name='semiprime_harvest',
                display='Two-parent leaves falling at step p',
                latex=r'\#\{N = qp \le X,\ q \le p\ \text{prime}\} = \pi(\min(p, X/p))',
                radian_form='semiprime_harvest(X,p) = pi(min(p, X//p)), exact sieve count',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['X', 'p'],
                compute=lambda X, p: semiprime_harvest(X, p),
                display_options=['text'],
            ),
            Equation(
                name='fall_split',
                display='The birth record: both falls, delta, and the collapse',
                latex=r'\ln p_1 + \ln p_2 = \ln N;\quad \delta = \tfrac12\ln(p_2/p_1)',
                radian_form='delta is the ENTIRE hidden content; collapse=2*delta -> 0 for balanced N',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['N'],
                compute=lambda N: fall_split(N),
                display_options=['text'],
            ),
            Equation(
                name='mertens',
                display='THE NEGATIVE-SPACE STAIRCASE: M(x) = Σ μ(n)',
                latex=r'M(x) = \sum_{n \le x} \mu(n),\quad 1/\zeta(s) = \sum \mu(n)n^{-s}',
                radian_form='psi is the bulk; M is the exclusion. M(10)=-1, M(100)=1, M(1000)=2',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x'],
                compute=lambda x: mertens(x),
                display_options=['text'],
            ),
            Equation(
                name='mobius',
                display='THE NEGATIVE-SPACE OPERATOR: μ, the Dirichlet inverse of 1',
                latex=r'\sum_{d \mid n} \mu(d) = [n = 1]',
                radian_form='the sieve is inclusion-exclusion; mu is what it runs on',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n'],
                compute=lambda n: mobius(n),
                display_options=['text'],
            ),
            Equation(
                name='mertens_envelope',
                display='RH on the exclusion side: M(x) = O(x^(1/2+eps))',
                latex=r'\mathrm{RH} \iff M(x) = O\!\left(x^{1/2+\epsilon}\right)',
                radian_form='the SAME 1/2 as the critical line and as the 2*sqrt(x) tone envelope',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x', 'eps'],
                compute=lambda x, eps=0.0: mertens_envelope(x, eps),
                display_options=['text'],
            ),
            Equation(
                name='sieve_extinction',
                display='THE THREE-MOTION RECORD: grown / extinct / identified',
                latex=r'\ln N,\ \ln(\mathrm{lpf}\,N),\ \ln(\mathrm{gpf}\,N)',
                radian_form='extinct at lpf (negative space), identified at gpf (bulk); gap = 2*delta',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['N'],
                compute=lambda N: sieve_extinction(N),
                display_options=['text'],
            ),
            Equation(
                name='domain_ladder',
                display='THE PROJECTION LEDGER: what the domain actually is',
                latex=r'2^{b} \to 2^{b/2} \to \pi(2^{b/2}) \to 2^{112}',
                radian_form=('all ints 2^b; ints to sqrt 2^(b/2); primes to sqrt pi(2^(b/2)); '
                             'exact-size primes (1 bit less); GNFS 2^112'),
                confidence='ESTABLISHED',
                code_verified=True,
                params=['modulus_bits', 'gnfs_bits'],
                compute=lambda modulus_bits=2048, gnfs_bits=112.0: domain_ladder(modulus_bits, gnfs_bits),
                display_options=['text'],
            ),
            Equation(
                name='zero_height_lambert',
                display='Lambert inverse of the zero count: gamma_n = 2*pi*n/W(n/e)',
                latex=r'\gamma_n \sim \frac{2\pi n}{W(n/e)}',
                radian_form='gamma_n = 2*pi*n / lambert_w(n/e)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['n'],
                compute=lambda n: zero_height_lambert(n),
                display_options=['text'],
            ),
            Equation(
                name='zero_count_smooth',
                display='Riemann-von Mangoldt zero count N(T)',
                latex=r'N(T) = \frac{T}{2\pi}\ln\frac{T}{2\pi e} + \frac78 + S(T)',
                radian_form='N(T) = (T/2pi)*ln(T/(2pi*e)) + 7/8   (S(T) omitted)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['T'],
                compute=lambda T: zero_count_smooth(T),
                display_options=['text'],
            ),
            Equation(
                name='amplitude_envelope',
                display='RH in the prime domain: one shared envelope 2*sqrt(x)',
                latex=r'|\text{tone}_k| \le 2x^{\sigma},\quad \sigma = \tfrac12 \ \forall k',
                radian_form='envelope(x, sigma) = 2*x^sigma; RH <=> sigma=1/2 for every zero',
                confidence='THEORETICAL',
                code_verified=True,
                params=['x', 'sigma'],
                compute=lambda x, sigma=0.5: amplitude_envelope(x, sigma),
                display_options=['text'],
            ),
            Equation(
                name='envelope_ratio',
                display='How loudly an off-line zero would drown the others',
                latex=r'x^{\sigma-1/2} \to \infty \ \text{ for } \sigma > 1/2',
                radian_form='ratio(x, sigma_off) = x^(sigma_off - 0.5)',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x', 'sigma_off'],
                compute=lambda x, sigma_off: envelope_ratio(x, sigma_off),
                display_options=['text'],
            ),
            Equation(
                name='interference_profile',
                display='Per-zero tones at x -- primes are the antinodes',
                latex=r'\text{tone}_k(u) = \frac{2e^{u/2}\cos(\gamma_k u - \arg\rho_k)}{|\rho_k|}',
                radian_form='[(gamma_k, tone_k)] at u = ln x',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x', 'zeros'],
                compute=lambda x, zeros=None: interference_profile(x, zeros),
                display_options=['text'],
            ),
            Equation(
                name='prime_count_log10',
                display='log10 pi(10^d) -- the finiteness readout at RSA scale',
                latex=r'\pi(x) \sim \frac{x}{\ln x}\left(1+\frac1L+\frac2{L^2}+\frac6{L^3}\right)',
                radian_form='log10 pi(10^d) = d - log10(L) + log10(series), L = d*ln10',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['digits'],
                compute=lambda digits: prime_count_log10(digits),
                display_options=['text'],
            ),
            Equation(
                name='splitting_vector',
                display='chi_N readout: the cheapest N-specific shadow there is',
                latex=r'\chi_N(p) = \left(\frac{D}{p}\right),\quad D = \mathrm{disc}\,\mathbb{Q}(\sqrt N)',
                radian_form='[(p, kronecker(D,p))] for p <= limit; +1 split, -1 inert, 0 ramified',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['N', 'limit'],
                compute=lambda N, limit=100: splitting_vector(N, limit),
                display_options=['text'],
            ),
            Equation(
                name='ramified_primes',
                display='Ramification = detachment: Euler factor degenerates at the factors',
                latex=r'p \mid D \iff p \text{ ramifies in } \mathbb{Q}(\sqrt N)',
                radian_form='ramified(N) = primes p<=limit with chi_N(p)=0; for N=pq these ARE p,q',
                confidence='THEORETICAL',
                code_verified=True,
                params=['N', 'limit'],
                compute=lambda N, limit=10 ** 6: ramified_primes(N, limit),
                display_options=['text'],
            ),
            Equation(
                name='lambert_w',
                display='The screw gear ratio: W(x)e^{W(x)} = x, W(1) = OMEGA_ZS',
                latex=r'W(x)e^{W(x)} = x,\quad W(1) = \Omega_{Z\Sigma} = 0.5671432904\ldots',
                radian_form='lambert_w(x) by Halley iteration; W(1) = OMEGA_ZS',
                confidence='ESTABLISHED',
                code_verified=True,
                params=['x'],
                compute=lambda x: lambert_w(x),
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
        result = self.run(equation_name, params)
        return {'text': self._format_text(equation_name, result)}

    def _format_text(self, equation_name: str, result: Dict) -> str:
        eq = result['equation']
        r = result['result']
        if isinstance(r, dict):
            summary = '\n'.join(
                f"      {k:<12} = {v}" for k, v in r.items()
                if not isinstance(v, list)
            )
            summary = '\n' + summary
        elif isinstance(r, list):
            head = r[:12]
            summary = f"{head}{' ...' if len(r) > 12 else ''}  (n={len(r)})"
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
            'screw':      lambda term, value: screw_coordinates(term, value),
            'pitch':      lambda p: screw_pitch(p),
            'psi':        lambda x: chebyshev_psi_exact(x),
            'psi_tones':  lambda x, k=50: chebyshev_psi_explicit(x, zeros_upto(k)),
            'zero_sum':   lambda x, k=50: zero_sum(x, zeros_upto(k)),
            'L':          lambda x: clean_path_L(x),
            'slots':      lambda x, k=50: l_io_decomposition(x, zeros_upto(k)),
            'fall':       lambda n: fall_height(n),
            'disc':       lambda n: discovery_height(n),
            'gpf':        lambda n: gpf(n),
            'lpf':        lambda n: lpf(n),
            'u':          lambda n: smoothness_u(n),
            'rho':        lambda u: dickman_rho(u),
            'harvest':    lambda X, p: harvest(X, p),
            'crop':       lambda X: harvest_curve(X),
            'sp_harvest': lambda X, p: semiprime_harvest(X, p),
            'birth':      lambda N: fall_split(N),
            'ladder':     lambda b=2048: domain_ladder(b),
            'mu':         lambda n: mobius(n),
            'M':          lambda x: mertens(x),
            'M_bound':    lambda x: mertens_envelope(x),
            'extinct':    lambda N: sieve_extinction(N),
            'shake':      lambda x, k=50: shake_order(x, zeros_upto(k)),
            'gamma':      lambda n: zero_height(n),
            'gamma_w':    lambda n: zero_height_lambert(n),
            'N':          lambda T: zero_count_smooth(T),
            'tones':      lambda x, k=20: interference_profile(x, zeros_upto(k)),
            'envelope':   lambda x, sigma=0.5: amplitude_envelope(x, sigma),
            'drown':      lambda x, s: envelope_ratio(x, s),
            'chi':        lambda N, limit=100: splitting_vector(N, limit),
            'ramified':   lambda N, limit=10 ** 6: ramified_primes(N, limit),
            'W':          lambda x: lambert_w(x),
            'pi_log10':   lambda d: prime_count_log10(d),
        }

    def on_register(self, registry) -> None:
        pass
