"""
ValaQuenta.modules.zeta_uns_path.tools
======================================
THE ZETA PATHWAY IN UNS -- Module Tools (EquationModule registry contract).  See maths.py.

Version: 1.0
"""
from typing import Any, Dict, List
import numpy as np
from ...engine.registry import EquationModule, Equation
from . import maths as M

def _eq(name, display, latex, radian, params, compute, process, conf='ESTABLISHED'):
    return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf, code_verified=True, params=params,
                    compute=compute, display_options=['text'], process=process)

def _cx(z): return [float(np.real(z)), float(np.imag(z))]

class ZetaUNSPathModule(EquationModule):
    """THE ZETA PATHWAY IN UNIVERSAL NATIVE SPACE."""
    @property
    def name(self): return "zeta_uns_path"
    @property
    def display_name(self): return "The Zeta Pathway in Universal Native Space (rotation, spring, primes)"
    @property
    def version(self): return "1.0"
    @property
    def description(self):
        return ("The critical-line path zeta(1/2 + it) = exp(-i theta) Z as a rotation at rate -theta'(t) with a signed radius Z(t): fast Riemann-Siegel evaluation, the UNS cylinder and sphere charts, "
                "the radial driver Z'/Z as a sum of zero poles, the prime spring (Euler path), prime resonance heights, and the zero spectrum whose spikes sit at ln p^k.")
    @property
    def confidence_floor(self): return "ESTABLISHED"

    def formulary(self) -> List[Equation]:
        return [
            _eq('theta', 'RIEMANN-SIEGEL THETA and the rotation rate', r"\theta(t)=\tfrac t2\ln\tfrac t{2\pi}-\tfrac t2-\tfrac\pi8+\tfrac1{48t}+\dots,\ \ \theta'(t)\approx\tfrac12\ln\tfrac t{2\pi}",
                'the flat point turns at -theta\'(t), slowly increasing', ['t'], lambda t=100.0: {'theta': float(M.theta(t)), 'rate': float(M.rotation_rate(t))}, 'how fast the path turns'),
            _eq('hardy_z', 'HARDY Z by Riemann-Siegel, against mpmath', r'Z(t)=2\sum_{n\le N}\frac{\cos(\theta-t\ln n)}{\sqrt n}+(-1)^{N-1}(t/2\pi)^{-1/4}C_0(p)',
                'error 3e-3 at t=100, 1e-4 at t=2000, 5e-6 at t=1e4 (measured)', ['t'], lambda t=100.0: {'Z_rs': float(M.Z_rs(t)[0]), 'Z_exact': M.Z_exact(t), 'abs_err': abs(float(M.Z_rs(t)[0]) - M.Z_exact(t))}, 'the real radius of the path'),
            _eq('pathway', 'THE PATH POINT: zeta, UNS cylinder, sphere', r'\zeta(\tfrac12+it)=e^{-i\theta}Z,\ \rho=\log_{10}|\zeta|+3,\ \varphi=\arg\zeta',
                'a point in the three charts', ['t'], lambda t=100.0: (lambda z: {'zeta': _cx(z[0]), 'cylinder_rho_phi_t': [float(v[0]) for v in M.uns_cylinder(z, [t])], 'sphere': M.sphere_point(z[0]).tolist()})(M.zeta_line(t)), 'where the path is'),
            _eq('driver', 'THE RADIAL DRIVER Z\'/Z as a sum over the zero poles (first 60 zeros)', r"Z'/Z=\sum_n \frac{2t}{t^2-\gamma_n^2}+\text{smooth}",
                'the analogue of Aizawa\'s z - b = (dr/dt)/r', ['t'], lambda t=40.3: {'Z_prime_over_Z': float(M.driver(t)[0]), 'zero_sum_60': float(M.driver_from_zeros(t, M.zeros_mp(60))[0])}, 'what drives the radius'),
            _eq('prime_resonance', 'PRIME RESONANCE HEIGHTS', r't_k=2\pi k/\ln p', 'where prime p\'s phasor is back at angle 0', ['p', 'T'],
                lambda p=2, T=60.0: {'t': M.prime_resonance_times(p, T).round(4).tolist()}, 'ticks on the spring for a prime', 'CALCULATED'),
            _eq('euler_path', 'THE PRIME SPRING (Euler path) at height t', r'\sum_p -\ln(1-p^{-1/2-it})', 'one step per prime, length ~ p^(-1/2), turned by -t ln p', ['t', 'n'],
                lambda t=14.1347, n=12: (lambda P: {'primes': P.tolist(), 'steps': [_cx(x) for x in M.euler_path(t, P)[1]], 'path_end': _cx(M.euler_path(t, P)[0][-1])})(M.primes_upto(60)[:n]), 'where the primes are on the path', 'CALCULATED'),
            _eq('spectrum_ticks', 'WHERE THE ZERO SPECTRUM SPIKES: x = ln p^k, weight ln p / p^(k/2)', r'\sum_\gamma\cos(\gamma x)\ \text{spikes at}\ x=\ln p^k', 'explicit formula, dual side', ['xmax'],
                lambda xmax=2.5: [dict(x=round(a, 4), p=b, k=c, weight=round(d, 4)) for a, b, c, d in M.prime_power_ticks(xmax)], 'the primes read off the zeros', 'CALCULATED'),
        ]

    def run(self, equation_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        eq = next((e for e in self.formulary() if e.name == equation_name), None)
        if eq is None: raise KeyError(f"Equation '{equation_name}' not found in {self.name} module")
        result = eq.compute(**params) if params else eq.compute()
        return {'equation': eq, 'params': params, 'result': result, 'module': self.name}

    def viewer_data(self, equation_name: str, params: Dict[str, Any], display_mode: str) -> Dict[str, Any]:
        r = self.run(equation_name, params); eq, res = r['equation'], r['result']
        body = '\n'.join(f"      {k:<22} {v}" for k, v in res.items()) if isinstance(res, dict) else str(res)
        return {'text': f"  {eq.display}\n  Status: {eq.confidence}  |  Code-verified: {eq.code_verified}\n  {eq.radian_form}\n{body}"}

    def shell_commands(self) -> Dict[str, Any]:
        return {'zuns_zeta': lambda t: complex(M.zeta_line(t)[0]), 'zuns_theta': lambda t: float(M.theta(t)), 'zuns_Z': lambda t: float(M.Z_rs(t)[0]),
                'zuns_path': lambda n=1000, per=16: M.zeta_line(M.sample_by_phase(10.0, n, per)).tolist()}
