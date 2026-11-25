"""
ValaQuenta.modules.aizawa_attractor.tools
=========================================
THE AIZAWA ATTRACTOR ENGINE -- Module Tools (EquationModule registry contract: formulary, run(), viewer_data(), shell_commands()).  See maths.py.

Version: 1.0
"""
from typing import Any, Dict, List
import numpy as np
from ...engine.registry import EquationModule, Equation
from . import maths as M

def _eq(name, display, latex, radian, params, compute, process, conf='ESTABLISHED'):
    return Equation(name=name, display=display, latex=latex, radian_form=radian, confidence=conf, code_verified=True, params=params,
                    compute=compute, display_options=['text'], process=process)

class AizawaAttractorModule(EquationModule):
    """THE AIZAWA ATTRACTOR ENGINE."""
    @property
    def name(self): return "aizawa_attractor"
    @property
    def display_name(self): return "The Aizawa Attractor (rotation with a radial driver)"
    @property
    def version(self): return "1.0"
    @property
    def description(self):
        return ("The Aizawa strange attractor as a rotation about the z axis at the constant rate d with a radius driven by dr/dt = (z-b) r: RK4 orbit, the exact cylindrical form, "
                "the axisymmetric reduction (f = 0), the fixed points on the axis, the largest Lyapunov exponent, and the JavaScript animation's buffer layout.")
    @property
    def confidence_floor(self): return "ESTABLISHED"

    def formulary(self) -> List[Equation]:
        s0 = (0.8, 0.3, 0.9)
        return [
            _eq('field', 'AIZAWA VECTOR FIELD', r'\dot x=(z-b)x-dy,\ \dot y=dx+(z-b)y,\ \dot z=c+az-z^3/3-(x^2+y^2)(1+ez)+fzx^3',
                'standard a=.95 b=.7 c=.6 d=3.5 e=.25 f=.1', ['x', 'y', 'z'], lambda x=s0[0], y=s0[1], z=s0[2]: dict(zip('xyz', M.rhs((x, y, z)).tolist())), 'the field at a point'),
            _eq('cylindrical', 'CYLINDRICAL FORM: dr/dt = (z-b) r, dphi/dt = d (exact)', r'\dot r=(z-b)r,\ \dot\varphi=d',
                'the orbit turns at constant rate d; z is the radial growth rate; r cannot reach 0', ['x', 'y', 'z'],
                lambda x=s0[0], y=s0[1], z=s0[2]: {'from_field': M.cylindrical_rates((x, y, z))[0], 'closed_form': M.cylindrical_rates((x, y, z))[1]}, 'rotation plus radial driver'),
            _eq('fixed_points', 'FIXED POINTS (on the axis) and their eigenvalues', r'c+az-z^3/3=0,\ \lambda=(z-b)\pm id,\ a-z^2', 'spiral saddles on the axis',
                [], lambda: [dict(point=f['point'], eigenvalues=[complex(v) for v in f['eigenvalues']]) for f in M.fixed_points()], 'where the orbit cannot stay'),
            _eq('orbit', 'RK4 ORBIT (seeded start, burn-in discarded)', r'x_{n+1}=x_n+\tfrac h6(k_1+2k_2+2k_3+k_4)', 'extent of 2000 points', ['points', 'h'],
                lambda points=2000, h=0.0045: {'min': M.bounds(M.orbit(points, 3000, h))[0].tolist(), 'max': M.bounds(M.orbit(points, 3000, h))[1].tolist()}, 'the attractor size'),
            _eq('lyapunov', 'LARGEST LYAPUNOV EXPONENT (Benettin)', r'\lambda_1=\lim\tfrac1t\ln\tfrac{|\delta(t)|}{|\delta(0)|}', 'positive = chaos', ['steps'],
                lambda steps=20000: {'lambda_max': M.lyapunov_max(steps=steps)}, 'is the orbit chaotic'),
            _eq('js_layout', "JAVASCRIPT PAGE BUFFER LAYOUT (x, z, y) and lineDistances", r'\mathrm{pos}[3i..3i+2]=(x,z,y)\cdot s,\ \mathrm{line}[i]=i/n', 'what the animation page draws',
                ['points'], lambda points=1000: {'n_floats': int(M.js_layout(M.orbit(points, 3000))[0].size), 'line_last': float(M.js_layout(M.orbit(points, 3000))[1][-1])}, 'the drawn geometry'),
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
        return {'az_field': lambda x, y, z: M.rhs((x, y, z)).tolist(), 'az_orbit': lambda n=2000: M.orbit(n, 3000).tolist(),
                'az_lyapunov': lambda steps=20000: M.lyapunov_max(steps=steps), 'az_fixed': lambda: M.fixed_points()}
